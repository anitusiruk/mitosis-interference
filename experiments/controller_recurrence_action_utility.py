import argparse
import random
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

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
from src.adapter_pool_action_utility import ActionUtilityShadowPool
from src.adapter_pool import encode


def make_dev_split(ds):
    labels = np.asarray(ds["label"])

    rng = np.random.default_rng(424242)

    train_ids = []
    dev_ids = []

    for cls in range(77):
        ids = np.flatnonzero(labels == cls).copy()
        rng.shuffle(ids)

        n_dev = max(
            1,
            int(round(0.20 * len(ids)))
        )

        dev_ids.extend(ids[:n_dev].tolist())
        train_ids.extend(ids[n_dev:].tolist())

    return (
        ds.select(sorted(train_ids)),
        ds.select(sorted(dev_ids)),
    )


def batches_from_ids(
    ds,
    ids,
    batch_size,
    rng,
    concept,
    occurrence,
):
    ids = np.asarray(ids).copy()
    rng.shuffle(ids)

    batches = []

    for start in range(
        0,
        len(ids),
        batch_size,
    ):
        chunk = ids[
            start:start + batch_size
        ]

        if len(chunk) == 0:
            continue

        batches.append({
            # EVAL ONLY.
            "concept": concept,
            "occurrence": occurrence,

            "texts": [
                ds[int(i)]["text"]
                for i in chunk
            ],

            "labels": [
                int(ds[int(i)]["label"])
                for i in chunk
            ],
        })

    return batches


def make_recurrence_stream(
    ds,
    batch_size,
    seed,
):
    rng = np.random.default_rng(
        seed + 9000
    )

    labels = np.asarray(
        ds["label"]
    )

    A = list(range(0, 11))
    B = list(range(11, 22))
    C = list(range(22, 33))

    # Find the largest equal per-class sample budget
    # that allows A and B to appear twice using
    # disjoint examples, while C appears once.
    capacity = []

    for cls in A + B:
        n = int(
            np.sum(labels == cls)
        )
        capacity.append(
            n // 2
        )

    for cls in C:
        n = int(
            np.sum(labels == cls)
        )
        capacity.append(n)

    per_class = min(capacity)

    if per_class < 1:
        raise RuntimeError(
            "Insufficient examples for balanced recurrence."
        )

    def two_occurrences(classes):
        first = []
        second = []

        for cls in classes:
            ids = np.flatnonzero(
                labels == cls
            ).copy()

            rng.shuffle(ids)

            first.extend(
                ids[:per_class].tolist()
            )

            second.extend(
                ids[
                    per_class:
                    2 * per_class
                ].tolist()
            )

        return first, second

    def one_occurrence(classes):
        chosen = []

        for cls in classes:
            ids = np.flatnonzero(
                labels == cls
            ).copy()

            rng.shuffle(ids)

            chosen.extend(
                ids[:per_class].tolist()
            )

        return chosen

    A1_ids, A2_ids = two_occurrences(A)
    B1_ids, B2_ids = two_occurrences(B)
    C1_ids = one_occurrence(C)

    # Recurrences must be genuinely disjoint.
    assert set(A1_ids).isdisjoint(
        set(A2_ids)
    )

    assert set(B1_ids).isdisjoint(
        set(B2_ids)
    )

    expected = (
        len(A) * per_class
    )

    assert len(A1_ids) == expected
    assert len(A2_ids) == expected
    assert len(B1_ids) == expected
    assert len(B2_ids) == expected
    assert len(C1_ids) == expected

    print(
        "balanced examples/class:",
        per_class,
        flush=True,
    )

    print(
        "balanced examples/segment:",
        expected,
        flush=True,
    )

    segments = [
        ("A", 1, A1_ids),
        ("B", 1, B1_ids),
        ("A", 2, A2_ids),
        ("C", 1, C1_ids),
        ("B", 2, B2_ids),
    ]

    stream = []
    boundaries = []

    for index, (
        concept,
        occurrence,
        ids,
    ) in enumerate(segments):

        if index > 0:
            boundaries.append(
                len(stream) + 1
            )

        segment_batches = batches_from_ids(
            ds=ds,
            ids=ids,
            batch_size=batch_size,
            rng=rng,
            concept=concept,
            occurrence=occurrence,
        )

        stream.extend(
            segment_batches
        )

    return stream, boundaries


def evaluate_adapter_concept(
    pool,
    adapter_name,
    restore_name,
    ds,
    allowed_labels,
    batch_size=64,
):
    """Eval-only measurement with full RNG/mode restoration."""

    py_state = random.getstate()
    np_state = np.random.get_state()
    torch_state = torch.get_rng_state()

    cuda_state = (
        torch.cuda.get_rng_state_all()
        if torch.cuda.is_available()
        else None
    )

    was_training = pool.model.training

    labels_all = np.asarray(
        ds["label"]
    )

    ids = np.flatnonzero(
        np.isin(
            labels_all,
            list(allowed_labels),
        )
    )

    total_loss = 0.0
    total_correct = 0
    restricted_correct = 0
    concept_mass_sum = 0.0
    concept_margin_sum = 0.0
    total_n = 0

    allowed = sorted(
        int(v)
        for v in allowed_labels
    )

    allowed_tensor = torch.tensor(
        allowed,
        dtype=torch.long,
        device=pool.device,
    )

    try:
        pool.activate(adapter_name)
        pool.model.eval()

        for start in range(
            0,
            len(ids),
            batch_size,
        ):
            chunk = ids[
                start:start + batch_size
            ]

            texts = [
                ds[int(i)]["text"]
                for i in chunk
            ]

            labels = [
                int(ds[int(i)]["label"])
                for i in chunk
            ]

            x = encode(
                pool.tok,
                texts,
                pool.device,
            )

            y = torch.tensor(
                labels,
                dtype=torch.long,
                device=pool.device,
            )

            with torch.no_grad():
                logits = pool.model(
                    **x
                ).logits

                loss_sum = F.cross_entropy(
                    logits,
                    y,
                    reduction="sum",
                )

            total_loss += float(
                loss_sum.item()
            )

            full_pred = logits.argmax(
                dim=-1
            )

            total_correct += int(
                (
                    full_pred
                    == y
                ).sum().item()
            )

            # Accuracy if prediction is restricted
            # to this concept's 11 labels.
            allowed_logits = logits.index_select(
                1,
                allowed_tensor,
            )

            restricted_idx = (
                allowed_logits.argmax(
                    dim=-1
                )
            )

            restricted_pred = (
                allowed_tensor[
                    restricted_idx
                ]
            )

            restricted_correct += int(
                (
                    restricted_pred
                    == y
                ).sum().item()
            )

            # How much total model probability is
            # assigned to this concept's labels?
            probs = torch.softmax(
                logits,
                dim=-1,
            )

            concept_mass = (
                probs.index_select(
                    1,
                    allowed_tensor,
                )
                .sum(dim=-1)
            )

            concept_mass_sum += float(
                concept_mass.sum().item()
            )

            # Positive means the strongest logit
            # belongs to this concept rather than
            # to one of the other 66 labels.
            outside_mask = torch.ones(
                logits.shape[-1],
                dtype=torch.bool,
                device=logits.device,
            )

            outside_mask[
                allowed_tensor
            ] = False

            concept_best = (
                allowed_logits.max(
                    dim=-1
                ).values
            )

            outside_best = (
                logits[:, outside_mask]
                .max(dim=-1)
                .values
            )

            concept_margin_sum += float(
                (
                    concept_best
                    - outside_best
                ).sum().item()
            )

            total_n += len(labels)

        return {
            "n": total_n,
            "loss": (
                total_loss / total_n
            ),
            "accuracy": (
                total_correct / total_n
            ),
            "restricted_accuracy": (
                restricted_correct
                / total_n
            ),
            "concept_prob_mass": (
                concept_mass_sum
                / total_n
            ),
            "concept_logit_margin": (
                concept_margin_sum
                / total_n
            ),
        }

    finally:
        # Restore the adapter that real training
        # had active before this diagnostic.
        pool.activate(restore_name)

        random.setstate(py_state)
        np.random.set_state(np_state)
        torch.set_rng_state(
            torch_state
        )

        if cuda_state is not None:
            torch.cuda.set_rng_state_all(
                cuda_state
            )

        if was_training:
            pool.model.train()
        else:
            pool.model.eval()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
    )

    args = parser.parse_args()

    seed_all(args.seed)

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

    train_ds, dev_ds = make_dev_split(
        banking["train"]
    )

    stream, boundaries = (
        make_recurrence_stream(
            train_ds,
            args.batch_size,
            args.seed,
        )
    )

    print(
        "GPU:",
        torch.cuda.get_device_name(0),
        flush=True,
    )

    print(
        "stream steps:",
        len(stream),
        flush=True,
    )

    print(
        "boundaries (EVAL ONLY):",
        boundaries,
        flush=True,
    )

    print(
        "schedule (EVAL ONLY):",
        "A1 -> B1 -> A2 -> C1 -> B2",
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

    pool = ActionUtilityShadowPool(
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
    eval_rows = []

    # Offline evaluation labels only.
    # Never exposed to the controller.
    concept_labels = {
        "A": list(range(0, 11)),
        "B": list(range(11, 22)),
        "C": list(range(22, 33)),
    }

    segment_adapter = defaultdict(
        Counter
    )

    previous_segment = None

    # Tracks the adapter active after the previous
    # REAL training update. Shadow scoring must
    # restore exactly to this adapter.
    last_real_name = "default"

    for step, batch in enumerate(
        stream,
        start=1,
    ):
        segment = (
            f"{batch['concept']}"
            f"{batch['occurrence']}"
        )

        if segment != previous_segment:
            print()
            print(
                "=== ENTER",
                segment,
                "at step",
                step,
                "===",
                flush=True,
            )

            previous_segment = segment

        # OBSERVATIONAL ONLY.
        # Must leave the real V3 trajectory unchanged.
        utility = pool.crossfit_action_utility(
            texts=batch["texts"],
            labels=batch["labels"],
            restore_name=last_real_name,
        )

        # Real controller decision remains V3.
        name, info = pool.select(
            batch["texts"],
            batch["labels"],
        )

        loss = pool.train_step(
            name,
            batch["texts"],
            batch["labels"],
        )

        last_real_name = name

        segment_adapter[
            segment
        ][name] += 1

        rows.append({
            "step": step,
            "concept":
                batch["concept"],
            "occurrence":
                batch["occurrence"],
            "segment":
                segment,
            "adapter":
                name,
            "decision":
                info.get("decision"),
            "best_risk":
                info.get("best_risk"),
            "best_lcb":
                info.get("best_lcb"),
            "best_ucb":
                info.get("best_ucb"),
            "best_gain":
                info.get("best_gain"),
            "num_adapters":
                len(pool.states),
            "loss":
                loss,
            "risks":
                json.dumps(
                    info.get(
                        "risks",
                        {},
                    ),
                    sort_keys=True,
                ),

            # Common-baseline action utility.
            "utility_status":
                utility.get(
                    "status"
                ),

            "utility_batch_n":
                utility.get(
                    "batch_n"
                ),

            "fold_a_support_n":
                utility.get(
                    "fold_a_support_n"
                ),

            "fold_a_query_n":
                utility.get(
                    "fold_a_query_n"
                ),

            "fold_b_support_n":
                utility.get(
                    "fold_b_support_n"
                ),

            "fold_b_query_n":
                utility.get(
                    "fold_b_query_n"
                ),

            "statusquo_loss":
                utility.get(
                    "statusquo_loss"
                ),

            "defer_utility":
                utility.get(
                    "defer_utility"
                ),

            "utility_best_reuse":
                utility.get(
                    "best_reuse"
                ),

            "best_reuse_utility":
                utility.get(
                    "best_reuse_utility"
                ),

            "best_reuse_query_after":
                utility.get(
                    "best_reuse_query_after"
                ),

            "fresh_utility":
                utility.get(
                    "fresh_utility"
                ),

            "fresh_query_before":
                utility.get(
                    "fresh_query_before"
                ),

            "fresh_query_after":
                utility.get(
                    "fresh_query_after"
                ),

            "fresh_local_trainability":
                utility.get(
                    "fresh_local_trainability"
                ),

            "fresh_advantage":
                utility.get(
                    "fresh_advantage"
                ),

            "fresh_positive":
                utility.get(
                    "fresh_positive"
                ),

            "fold_a_fresh_utility":
                utility.get(
                    "fold_a_fresh_utility"
                ),

            "fold_b_fresh_utility":
                utility.get(
                    "fold_b_fresh_utility"
                ),

            "utility_reuse_profiles":
                json.dumps(
                    utility.get(
                        "reuse_profiles",
                        {},
                    ),
                    sort_keys=True,
                ),
        })

        if (
            info.get("decision")
            == "spawn"
            or step % 10 == 0
        ):
            print(
                f"step={step:4d} "
                f"segment(eval)={segment:2s} "
                f"adapter={name:12s} "
                f"decision={info.get('decision'):6s} "
                f"risk={info.get('best_risk')} "
                f"LCB={info.get('best_lcb')} "
                f"pool={len(pool.states)} "
                f"loss={loss:.4f}",
                flush=True,
            )


        # -------------------------------------------------
        # EVAL ONLY: held-out A/B/C performance matrix.
        #
        # Detect the final batch of the current segment.
        # `step` is 1-indexed, so stream[step] is the next
        # batch whenever step < len(stream).
        # -------------------------------------------------
        is_segment_end = (
            step == len(stream)
            or (
                f"{stream[step]['concept']}"
                f"{stream[step]['occurrence']}"
                != segment
            )
        )

        if is_segment_end:
            print()
            print(
                "=== HELDOUT EVAL AFTER",
                segment,
                "===",
                flush=True,
            )

            # Snapshot names so evaluation itself
            # cannot change iteration behavior.
            adapter_names = list(
                pool.states.keys()
            )

            for adapter_name in adapter_names:
                for concept_name, allowed in (
                    concept_labels.items()
                ):
                    metrics = (
                        evaluate_adapter_concept(
                            pool=pool,
                            adapter_name=adapter_name,
                            restore_name=name,
                            ds=dev_ds,
                            allowed_labels=allowed,
                        )
                    )

                    eval_rows.append({
                        "checkpoint": segment,
                        "step": step,
                        "adapter": adapter_name,
                        "concept": concept_name,
                        "n": metrics["n"],
                        "loss": metrics["loss"],
                        "accuracy":
                            metrics["accuracy"],
                        "restricted_accuracy":
                            metrics[
                                "restricted_accuracy"
                            ],
                        "concept_prob_mass":
                            metrics[
                                "concept_prob_mass"
                            ],
                        "concept_logit_margin":
                            metrics[
                                "concept_logit_margin"
                            ],
                    })

                    print(
                        f"{adapter_name:12s} "
                        f"{concept_name}: "
                        f"n={metrics['n']:4d} "
                        f"loss={metrics['loss']:.4f} "
                        f"acc={metrics['accuracy']:.4f}",
                        flush=True,
                    )

    out = Path(
        f"results/"
        f"controller_recurrence_action_utility_seed"
        f"{args.seed}"
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

    eval_df = pd.DataFrame(
        eval_rows
    )

    eval_df.to_csv(
        out / "eval_matrix.csv",
        index=False,
    )

    print(
        "saved eval:",
        out / "eval_matrix.csv",
    )

    print()
    print(
        "=== SEGMENT / ADAPTER COUNTS ==="
    )

    dominant = {}

    for segment in [
        "A1",
        "B1",
        "A2",
        "C1",
        "B2",
    ]:
        counts = segment_adapter[
            segment
        ]

        print(
            segment,
            dict(counts),
        )

        if counts:
            dominant[segment] = (
                counts.most_common(1)[0][0]
            )

    print()
    print(
        "=== RECURRENCE CHECK ==="
    )

    print(
        "A1 dominant:",
        dominant.get("A1"),
    )

    print(
        "A2 dominant:",
        dominant.get("A2"),
    )

    print(
        "A reused:",
        (
            dominant.get("A1")
            == dominant.get("A2")
        ),
    )

    print(
        "B1 dominant:",
        dominant.get("B1"),
    )

    print(
        "B2 dominant:",
        dominant.get("B2"),
    )

    print(
        "B reused:",
        (
            dominant.get("B1")
            == dominant.get("B2")
        ),
    )

    print()
    print(
        "=== SPAWNS ==="
    )

    spawns = df[
        df["decision"] == "spawn"
    ]

    if len(spawns):
        print(
            spawns[
                [
                    "step",
                    "segment",
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
        "final adapter count:",
        len(pool.states),
    )

    print(
        "saved:",
        out / "routing.csv",
    )


if __name__ == "__main__":
    main()
