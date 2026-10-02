import argparse
import copy
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

from experiments.signal_scan import (
    seed_all,
    encode,
    trainable_params,
    measure_signals,
    memory_loss,
    Reservoir,
)


def capture_rng_state():
    state = {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch_cpu": torch.get_rng_state(),
    }

    if torch.cuda.is_available():
        state["torch_cuda"] = torch.cuda.get_rng_state_all()

    return state


def restore_rng_state(state):
    random.setstate(state["python"])
    np.random.set_state(state["numpy"])
    torch.set_rng_state(state["torch_cpu"])

    if torch.cuda.is_available():
        torch.cuda.set_rng_state_all(
            state["torch_cuda"]
        )


def exact_adamw_interference(
    model,
    optimizer,
    tok,
    cur_texts,
    cur_labels,
    mem_texts,
    mem_labels,
    device,
    horizons=(1, 3, 5),
):
    """
    Repeated-adaptation counterfactual.

    Temporarily perform exact AdamW updates on the current
    incoming batch and measure damage to historical sentinel
    data after 1, 3 and 5 updates.

    Model parameters and optimizer state are restored exactly.
    """

    params = trainable_params(model)

    param_backup = [
        p.detach().clone()
        for p in params
    ]

    optimizer_backup = copy.deepcopy(
        optimizer.state_dict()
    )

    was_training = model.training

    mem_before = memory_loss(
        model,
        tok,
        mem_texts,
        mem_labels,
        device,
    )

    x = encode(
        tok,
        cur_texts,
        device,
    )

    y = torch.tensor(
        cur_labels,
        dtype=torch.long,
        device=device,
    )

    output = {}

    model.train()

    for k in range(1, max(horizons) + 1):

        optimizer.zero_grad(set_to_none=True)

        loss = model(
            **x,
            labels=y,
        ).loss

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            params,
            1.0,
        )

        optimizer.step()

        if k in horizons:
            after = memory_loss(
                model,
                tok,
                mem_texts,
                mem_labels,
                device,
            )

            output[f"adamw_I{k}"] = (
                after - mem_before
            )

            model.train()

    with torch.no_grad():
        for p, old in zip(
            params,
            param_backup,
        ):
            p.copy_(old)

    optimizer.load_state_dict(
        optimizer_backup
    )

    optimizer.zero_grad(set_to_none=True)

    if was_training:
        model.train()
    else:
        model.eval()

    return output


def make_stream_ordered(
    ds,
    batch_size,
    data_seed,
    class_order_seed,
):
    labels = np.asarray(ds["label"])

    classes = np.arange(77)

    if class_order_seed >= 0:
        order_rng = np.random.default_rng(
            class_order_seed
        )
        order_rng.shuffle(classes)

    groups = np.array_split(
        classes,
        7,
    )

    rng = np.random.default_rng(
        data_seed
    )

    stream = []
    boundaries = []

    for phase, group in enumerate(groups):

        ids = np.flatnonzero(
            np.isin(labels, group)
        ).copy()

        rng.shuffle(ids)

        if phase > 0:
            boundaries.append(
                len(stream) + 1
            )

        for start in range(
            0,
            len(ids),
            batch_size,
        ):
            chunk = ids[
                start:start + batch_size
            ]

            stream.append({
                "phase": phase,
                "texts": [
                    ds[int(i)]["text"]
                    for i in chunk
                ],
                "labels": [
                    int(ds[int(i)]["label"])
                    for i in chunk
                ],
            })

    groups_out = [
        [int(x) for x in group]
        for group in groups
    ]

    return stream, boundaries, groups_out


def sample_heldout(
    dev_ds,
    seen_labels,
    n,
    rng,
):
    labels = np.asarray(
        dev_ds["label"]
    )

    eligible = np.flatnonzero(
        np.isin(
            labels,
            np.asarray(
                sorted(seen_labels)
            ),
        )
    )

    if len(eligible) == 0:
        raise RuntimeError(
            "No held-out examples available."
        )

    chosen = rng.choice(
        eligible,
        size=min(n, len(eligible)),
        replace=False,
    )

    texts = [
        dev_ds[int(i)]["text"]
        for i in chosen
    ]

    ys = [
        int(dev_ds[int(i)]["label"])
        for i in chosen
    ]

    return texts, ys


def main():

    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--seed",
        type=int,
        default=2026,
    )

    ap.add_argument(
        "--batch-size",
        type=int,
        default=16,
    )

    ap.add_argument(
        "--probe-every",
        type=int,
        default=10,
    )

    ap.add_argument(
        "--future-horizon",
        type=int,
        default=10,
    )

    ap.add_argument(
        "--memory-size",
        type=int,
        default=512,
    )

    ap.add_argument(
        "--memory-probe",
        type=int,
        default=64,
    )

    ap.add_argument(
        "--lr",
        type=float,
        default=2e-4,
    )

    ap.add_argument(
        "--max-steps",
        type=int,
        default=0,
    )

    ap.add_argument(
        "--tag",
        type=str,
        default="rngsafe",
    )

    ap.add_argument(
        "--class-order-seed",
        type=int,
        default=-1,
    )

    args = ap.parse_args()

    seed_all(args.seed)

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA required"
        )

    device = torch.device("cuda")

    print(
        "GPU:",
        torch.cuda.get_device_name(0),
        flush=True,
    )

    banking = load_dataset(
        "PolyAI/banking77",
        trust_remote_code=True,
    )

    full_train = banking["train"]

    # ------------------------------------------
    # FIXED DEVELOPMENT SPLIT
    #
    # 80% of each class becomes the CL stream.
    # 20% is permanently held out.
    #
    # Official BANKING77 test data is untouched.
    # ------------------------------------------

    all_labels = np.asarray(
        full_train["label"]
    )

    split_rng = np.random.default_rng(
        424242
    )

    train_ids = []
    dev_ids = []

    for cls in range(77):

        ids = np.flatnonzero(
            all_labels == cls
        ).copy()

        split_rng.shuffle(ids)

        n_dev = max(
            1,
            int(round(0.20 * len(ids))),
        )

        dev_ids.extend(
            ids[:n_dev].tolist()
        )

        train_ids.extend(
            ids[n_dev:].tolist()
        )

    train_ids = sorted(train_ids)
    dev_ids = sorted(dev_ids)

    ds = full_train.select(
        train_ids
    )

    dev_ds = full_train.select(
        dev_ids
    )

    print(
        "development split:",
        len(ds),
        "stream /",
        len(dev_ds),
        "held-out",
        flush=True,
    )

    stream, boundaries, phase_groups = (
        make_stream_ordered(
            ds,
            args.batch_size,
            args.seed,
            args.class_order_seed,
        )
    )

    print(
        "steps:",
        len(stream),
        flush=True,
    )

    print(
        "hidden boundaries:",
        boundaries,
        flush=True,
    )

    print(
        "phase groups:",
        phase_groups,
        flush=True,
    )

    tok = AutoTokenizer.from_pretrained(
        "distilbert-base-uncased"
    )

    base = (
        AutoModelForSequenceClassification
        .from_pretrained(
            "distilbert-base-uncased",
            num_labels=77,
        )
    )

    cfg = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=8,
        lora_alpha=16,
        lora_dropout=0.0,
        target_modules=[
            "q_lin",
            "v_lin",
        ],
        bias="none",
    )

    model = get_peft_model(
        base,
        cfg,
    ).to(device)

    optimizer = torch.optim.AdamW(
        trainable_params(model),
        lr=args.lr,
    )

    # Only this historical memory is visible
    # to the prospective predictor.
    signal_reservoir = Reservoir(
        args.memory_size,
        args.seed + 1,
    )

    # Independent RNG for held-out evaluation.
    eval_rng = np.random.default_rng(
        args.seed + 2
    )

    seen_labels = set()

    rows = []
    pending = []

    for step, batch in enumerate(
        stream,
        start=1,
    ):

        # ----------------------------------
        # Resolve future-harm measurements.
        #
        # At this point exactly
        # future_horizon real updates have
        # occurred since the original probe.
        # ----------------------------------

        keep = []

        for item in pending:

            if item["due"] == step:

                future = memory_loss(
                    model,
                    tok,
                    item["texts"],
                    item["labels"],
                    device,
                )

                rows[
                    item["row"]
                ]["future_harm"] = (
                    future
                    - item["baseline"]
                )

            else:
                keep.append(item)

        pending = keep

        # ----------------------------------
        # Prospective diagnostic.
        # ----------------------------------

        if (
            step % args.probe_every == 0
            and len(signal_reservoir.items)
                >= args.memory_probe
            and len(seen_labels) > 0
        ):

            mt, ml = signal_reservoir.sample(
                args.memory_probe
            )

            # Future-harm target comes from
            # unseen DEV examples only.
            et, el = sample_heldout(
                dev_ds,
                seen_labels,
                args.memory_probe,
                eval_rng,
            )

            eval_before = memory_loss(
                model,
                tok,
                et,
                el,
                device,
            )

            # ------------------------------
            # Existing Day-1 signals.
            # Restore RNG afterwards so
            # diagnostics cannot alter real
            # training dropout trajectories.
            # ------------------------------

            rng_state = capture_rng_state()

            try:
                old = measure_signals(
                    model=model,
                    optimizer=optimizer,
                    tok=tok,
                    cur_texts=batch["texts"],
                    cur_labels=batch["labels"],
                    mem_texts=mt,
                    mem_labels=ml,
                    device=device,
                    virtual_lr=args.lr,
                )
            finally:
                restore_rng_state(
                    rng_state
                )

            # ------------------------------
            # Exact AdamW counterfactual.
            # ------------------------------

            rng_state = capture_rng_state()

            try:
                exact = (
                    exact_adamw_interference(
                        model=model,
                        optimizer=optimizer,
                        tok=tok,
                        cur_texts=batch["texts"],
                        cur_labels=batch["labels"],
                        mem_texts=mt,
                        mem_labels=ml,
                        device=device,
                    )
                )
            finally:
                restore_rng_state(
                    rng_state
                )

            row = {
                "step": step,
                "true_phase": batch["phase"],
                "distance_to_boundary":
                    min(
                        abs(step - b)
                        for b in boundaries
                    ),
                **old,
                **exact,
                "eval_memory_loss_before":
                    eval_before,
                "future_harm": np.nan,
            }

            rows.append(row)

            pending.append({
                "row": len(rows) - 1,
                "due":
                    step
                    + args.future_horizon,
                "texts": list(et),
                "labels": list(el),
                "baseline": eval_before,
            })

            print(
                f"step={step:4d} "
                f"phase(eval)={batch['phase']} "
                f"N={old['novelty']:+.4f} "
                f"G={old['grad_conflict']:+.4f} "
                f"SGD1={old['virtual_interference']:+.6f} "
                f"A1={exact['adamw_I1']:+.6f} "
                f"A3={exact['adamw_I3']:+.6f} "
                f"A5={exact['adamw_I5']:+.6f}",
                flush=True,
            )

        # ----------------------------------
        # REAL optimizer update.
        # ----------------------------------

        model.train()

        x = encode(
            tok,
            batch["texts"],
            device,
        )

        y = torch.tensor(
            batch["labels"],
            dtype=torch.long,
            device=device,
        )

        optimizer.zero_grad(
            set_to_none=True
        )

        loss = model(
            **x,
            labels=y,
        ).loss

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            trainable_params(model),
            1.0,
        )

        optimizer.step()

        # Historical predictor memory.
        for text, label in zip(
            batch["texts"],
            batch["labels"],
        ):
            signal_reservoir.add(
                text,
                label,
            )

            seen_labels.add(
                int(label)
            )

        if (
            args.max_steps
            and step >= args.max_steps
        ):
            print(
                "Reached max-steps.",
                flush=True,
            )
            break

    out = Path(
        f"results/"
        f"{args.tag}_seed{args.seed}"
    )

    out.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.DataFrame(rows)

    df.to_csv(
        out / "signals.csv",
        index=False,
    )

    print()
    print("DONE")
    print(
        "saved:",
        out / "signals.csv",
    )


if __name__ == "__main__":
    main()
