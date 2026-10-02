import argparse
import json

from collections import (
    Counter,
    defaultdict,
)

from pathlib import Path

import numpy as np
import pandas as pd
import torch

from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
)

from experiments.signal_scan import seed_all

from experiments.day2_predictor_scan_rngsafe import (
    make_stream_ordered,
)

from src.adapter_pool_confidence import (
    ConfidenceAdapterPool,
)


def make_dev_split(ds):

    labels = np.asarray(
        ds["label"]
    )

    rng = np.random.default_rng(
        424242
    )

    train_ids = []
    dev_ids = []

    for cls in range(77):

        ids = np.flatnonzero(
            labels == cls
        ).copy()

        rng.shuffle(ids)

        n_dev = max(
            1,
            int(round(
                0.20 * len(ids)
            )),
        )

        dev_ids.extend(
            ids[:n_dev].tolist()
        )

        train_ids.extend(
            ids[n_dev:].tolist()
        )

    return (
        ds.select(
            sorted(train_ids)
        ),
        ds.select(
            sorted(dev_ids)
        ),
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
    )

    parser.add_argument(
        "--class-order-seed",
        type=int,
        default=-1,
    )

    parser.add_argument(
        "--max-steps",
        type=int,
        default=240,
    )

    args = parser.parse_args()

    seed_all(
        args.seed
    )

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA required"
        )

    device = torch.device(
        "cuda"
    )

    banking = load_dataset(
        "PolyAI/banking77",
        trust_remote_code=True,
    )

    train_ds, dev_ds = (
        make_dev_split(
            banking["train"]
        )
    )

    stream, boundaries, groups = (
        make_stream_ordered(
            train_ds,
            16,
            args.seed,
            args.class_order_seed,
        )
    )

    print(
        "GPU:",
        torch.cuda.get_device_name(0),
        flush=True,
    )

    print(
        "boundaries (EVAL ONLY):",
        boundaries,
        flush=True,
    )

    print(
        "phase groups (EVAL ONLY):",
        groups,
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

    pool = ConfidenceAdapterPool(
        model=model,
        tokenizer=tok,
        lora_config=cfg,
        device=device,
        lr=2e-4,
        memory_size=512,
        memory_probe=64,
        threshold=0.0,
        confidence_z=1.96,
        seed=args.seed,
    )

    rows = []

    phase_adapter = defaultdict(
        Counter
    )

    for step, batch in enumerate(
        stream,
        start=1,
    ):

        name, info = pool.select(
            batch["texts"],
            batch["labels"],
        )

        loss = pool.train_step(
            name,
            batch["texts"],
            batch["labels"],
        )

        phase = int(
            batch["phase"]
        )

        phase_adapter[
            phase
        ][name] += 1

        # Defensive .get() calls mean logging itself
        # cannot crash if a diagnostic field is absent.
        risks = info.get(
            "risks",
            {},
        )

        profiles = info.get(
            "profiles",
            {},
        )

        row = {
            "step": step,
            "true_phase": phase,
            "adapter": name,
            "decision":
                info.get("decision"),
            "best_risk":
                info.get("best_risk"),
            "best_gain":
                info.get("best_gain"),
            "best_lcb":
                info.get("best_lcb"),
            "best_ucb":
                info.get("best_ucb"),
            "num_adapters":
                len(pool.states),
            "loss": loss,
            "risks":
                json.dumps(
                    risks,
                    sort_keys=True,
                ),
            "profiles":
                json.dumps(
                    profiles,
                    sort_keys=True,
                ),
        }

        rows.append(row)

        if (
            info.get("decision") == "spawn"
            or step % 10 == 0
        ):
            print(
                f"step={step:4d} "
                f"phase(eval)={phase} "
                f"adapter={name:12s} "
                f"decision={info.get('decision')} "
                f"risk={info.get('best_risk')} "
                f"LCB={info.get('best_lcb')} "
                f"UCB={info.get('best_ucb')} "
                f"gain={info.get('best_gain')} "
                f"pool={len(pool.states)} "
                f"loss={loss:.4f}",
                flush=True,
            )

        if step >= args.max_steps:
            break

    out = Path(
        f"results/"
        f"controller_confidence_smoke_seed{args.seed}"
    )

    out.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.DataFrame(
        rows
    )

    df.to_csv(
        out / "routing.csv",
        index=False,
    )

    print()
    print(
        "=== ADAPTER SUMMARY ==="
    )

    print(
        json.dumps(
            pool.summary(),
            indent=2,
        )
    )

    print()
    print(
        "=== PHASE / ADAPTER COUNTS ==="
    )

    for phase in sorted(
        phase_adapter
    ):
        print(
            "phase",
            phase,
            dict(
                phase_adapter[
                    phase
                ]
            ),
        )

    print()
    print(
        "=== SPAWNS ==="
    )

    spawn_df = df[
        df["decision"] == "spawn"
    ]

    if len(spawn_df):
        print(
            spawn_df[
                [
                    "step",
                    "true_phase",
                    "adapter",
                    "best_risk",
                    "best_lcb",
                    "best_ucb",
                    "num_adapters",
                ]
            ].to_string(
                index=False
            )
        )
    else:
        print(
            "No spawns."
        )

    print()
    print(
        "saved:",
        out / "routing.csv",
    )


if __name__ == "__main__":
    main()
