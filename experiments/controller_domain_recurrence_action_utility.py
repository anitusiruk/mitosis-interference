import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
)

from experiments.signal_scan import (
    seed_all,
    encode,
)

from experiments.domain_recurrence_data import (
    DOMAINS,
    build_domain_recurrence,
)

from src.adapter_pool_confidence import (
    ConfidenceAdapterPool,
)

from src.adapter_pool_counterfactual import (
    CounterfactualAdapterPool,
)

from src.adapter_pool_action_utility import (
    ActionUtilityShadowPool,
)


def evaluate_adapter_domain(
    pool,
    adapter_name,
    restore_name,
    eval_set,
    batch_size=64,
):
    """
    Strictly observational evaluation on one fixed
    validation domain.
    """

    py_state = random.getstate()
    np_state = np.random.get_state()
    torch_state = torch.get_rng_state()

    cuda_state = (
        torch.cuda.get_rng_state_all()
        if torch.cuda.is_available()
        else None
    )

    was_training = pool.model.training

    texts = eval_set["texts"]
    labels = eval_set["labels"]

    total_loss = 0.0
    total_correct = 0
    total_n = 0

    class_correct = {
        0: 0,
        1: 0,
    }

    class_total = {
        0: 0,
        1: 0,
    }

    try:
        pool.activate(
            adapter_name
        )

        pool.model.eval()

        for start in range(
            0,
            len(texts),
            batch_size,
        ):
            bt = texts[
                start:
                start + batch_size
            ]

            bl = labels[
                start:
                start + batch_size
            ]

            x = encode(
                pool.tok,
                bt,
                pool.device,
            )

            y = torch.tensor(
                bl,
                dtype=torch.long,
                device=pool.device,
            )

            with torch.no_grad():
                logits = pool.model(
                    **x
                ).logits

                loss_sum = (
                    F.cross_entropy(
                        logits,
                        y,
                        reduction="sum",
                    )
                )

                pred = logits.argmax(
                    dim=-1
                )

            total_loss += float(
                loss_sum.item()
            )

            total_correct += int(
                (pred == y)
                .sum()
                .item()
            )

            total_n += len(bl)

            for cls in [0, 1]:
                mask = (
                    y == cls
                )

                class_total[cls] += int(
                    mask.sum().item()
                )

                class_correct[cls] += int(
                    (
                        (pred == y)
                        & mask
                    )
                    .sum()
                    .item()
                )

        return {
            "n": total_n,

            "loss":
                total_loss / total_n,

            "accuracy":
                total_correct / total_n,

            "neg_accuracy":
                class_correct[0]
                / class_total[0],

            "pos_accuracy":
                class_correct[1]
                / class_total[1],
        }

    finally:
        pool.activate(
            restore_name
        )

        random.setstate(
            py_state
        )

        np.random.set_state(
            np_state
        )

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

    parser.add_argument(
        "--method",
        choices=[
            "v3",
            "cf_v0",
            "utility",
        ],
        required=True,
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

    (
        stream,
        boundaries,
        eval_sets,
    ) = build_domain_recurrence(
        seed=args.seed,
        batch_size=args.batch_size,
        train_per_class=128,
        eval_per_class=64,
    )

    print(
        "GPU:",
        torch.cuda.get_device_name(0),
        flush=True,
    )

    print(
        "method:",
        args.method,
        flush=True,
    )

    print(
        "domains:",
        DOMAINS,
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

    print(
        "shared labels:",
        "{0=negative, 1=positive}",
        flush=True,
    )

    tok = (
        AutoTokenizer
        .from_pretrained(
            "distilbert-base-uncased"
        )
    )

    base = (
        AutoModelForSequenceClassification
        .from_pretrained(
            "distilbert-base-uncased",
            num_labels=2,
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

    common = dict(
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

    if args.method == "v3":
        pool = ConfidenceAdapterPool(
            **common
        )

    elif args.method == "cf_v0":
        pool = CounterfactualAdapterPool(
            **common,
            capacity_cost=0.0,
        )

    else:
        # REAL routing remains V3.
        # Cross-fit scores are observational only.
        pool = ActionUtilityShadowPool(
            **common
        )

    rows = []
    eval_rows = []

    segment_adapter = defaultdict(
        Counter
    )

    previous_segment = None

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
                "(",
                batch["domain"],
                ") at step",
                step,
                "===",
                flush=True,
            )

            previous_segment = (
                segment
            )

        # Controller gets ONLY texts + binary labels.
        #
        # In shadow mode this diagnostic MUST NOT
        # influence the real V3 decision.
        if args.method == "utility":
            utility = pool.crossfit_action_utility(
                texts=batch["texts"],
                labels=batch["labels"],
                restore_name=last_real_name,
            )
        else:
            utility = {
                "status": "not_run",
            }

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

        row = {
            "step": step,
            "concept":
                batch["concept"],
            "occurrence":
                batch["occurrence"],
            "segment":
                segment,
            "domain":
                batch["domain"],

            "adapter":
                name,

            "decision":
                info.get(
                    "decision"
                ),

            "best_risk":
                info.get(
                    "best_risk"
                ),

            "best_lcb":
                info.get(
                    "best_lcb"
                ),

            "best_ucb":
                info.get(
                    "best_ucb"
                ),

            "best_gain":
                info.get(
                    "best_gain"
                ),

            "num_adapters":
                len(
                    pool.states
                ),

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

            # Present for CF-v0, null for V3.
            "cf_reason":
                info.get(
                    "cf_reason"
                ),

            "cf_best_reuse":
                info.get(
                    "cf_best_reuse"
                ),

            "cf_reuse_query_after":
                info.get(
                    "cf_reuse_query_after"
                ),

            "cf_fresh_query_after":
                info.get(
                    "cf_fresh_query_after"
                ),

            "cf_fresh_advantage":
                info.get(
                    "cf_fresh_advantage"
                ),


            "utility_status":
                utility.get(
                    "status"
                ),

            "statusquo_loss":
                utility.get(
                    "statusquo_loss"
                ),

            "defer_utility":
                utility.get(
                    "defer_utility"
                ),

            "best_reuse":
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
        }

        rows.append(
            row
        )

        if (
            step % 10 == 0
            or info.get(
                "decision"
            ) == "spawn"
        ):
            print(
                "step",
                step,
                "segment",
                segment,
                "adapter",
                name,
                "decision",
                info.get(
                    "decision"
                ),
                "risk",
                info.get(
                    "best_risk"
                ),
                "loss",
                round(
                    loss,
                    5,
                ),
                "pool",
                len(
                    pool.states
                ),
                flush=True,
            )

        # Since `step` is 1-indexed, stream[step]
        # is the NEXT batch whenever step < len(stream).
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
                "=== HELDOUT DOMAIN EVAL AFTER",
                segment,
                "===",
                flush=True,
            )

            adapter_names = list(
                pool.states.keys()
            )

            for adapter_name in (
                adapter_names
            ):
                for concept in [
                    "A",
                    "B",
                    "C",
                ]:
                    metrics = (
                        evaluate_adapter_domain(
                            pool=pool,
                            adapter_name=adapter_name,
                            restore_name=name,
                            eval_set=eval_sets[
                                concept
                            ],
                        )
                    )

                    eval_rows.append({
                        "checkpoint":
                            segment,

                        "step":
                            step,

                        "adapter":
                            adapter_name,

                        "concept":
                            concept,

                        "domain":
                            DOMAINS[
                                concept
                            ],

                        "n":
                            metrics[
                                "n"
                            ],

                        "loss":
                            metrics[
                                "loss"
                            ],

                        "accuracy":
                            metrics[
                                "accuracy"
                            ],

                        "neg_accuracy":
                            metrics[
                                "neg_accuracy"
                            ],

                        "pos_accuracy":
                            metrics[
                                "pos_accuracy"
                            ],
                    })

                    print(
                        f"{adapter_name:12s} "
                        f"{concept}/"
                        f"{DOMAINS[concept]:10s} "
                        f"loss="
                        f"{metrics['loss']:.4f} "
                        f"acc="
                        f"{metrics['accuracy']:.4f} "
                        f"neg="
                        f"{metrics['neg_accuracy']:.4f} "
                        f"pos="
                        f"{metrics['pos_accuracy']:.4f}",
                        flush=True,
                    )

    out = Path(
        "results/"
        f"controller_domain_recurrence_"
        f"{args.method}_seed"
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

    print()
    print(
        "=== SEGMENT / ADAPTER COUNTS ==="
    )

    print(
        pd.crosstab(
            df.segment,
            df.adapter,
        ).to_string()
    )

    print()
    print(
        "=== DECISIONS ==="
    )

    print(
        pd.crosstab(
            df.segment,
            df.decision,
        ).to_string()
    )

    print()
    print(
        "=== SPAWNS ==="
    )

    spawn_cols = [
        "step",
        "segment",
        "domain",
        "adapter",
        "decision",
        "best_risk",
        "best_lcb",
        "num_adapters",
    ]

    if args.method == "cf_v0":
        spawn_cols += [
            "cf_reason",
            "cf_best_reuse",
            "cf_reuse_query_after",
            "cf_fresh_query_after",
            "cf_fresh_advantage",
        ]

    print(
        df[
            df.decision
            == "spawn"
        ][spawn_cols]
        .round(5)
        .to_string(
            index=False
        )
    )

    print()
    print(
        "final adapters:",
        int(
            df.num_adapters.max()
        ),
    )

    print(
        "saved:",
        out,
    )


if __name__ == "__main__":
    main()
