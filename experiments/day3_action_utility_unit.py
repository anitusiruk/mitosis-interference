import copy
import hashlib

import numpy as np
import torch

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
)

from src.adapter_pool import (
    capture_rng_state,
)

from src.adapter_pool_action_utility import (
    ActionUtilityShadowPool,
)


SEED = 2026


def nested_equal(a, b):
    if torch.is_tensor(a):
        return (
            torch.is_tensor(b)
            and a.dtype == b.dtype
            and tuple(a.shape) == tuple(b.shape)
            and torch.equal(a, b)
        )

    if isinstance(a, np.ndarray):
        return (
            isinstance(b, np.ndarray)
            and a.dtype == b.dtype
            and a.shape == b.shape
            and np.array_equal(a, b)
        )

    if isinstance(a, dict):
        return (
            isinstance(b, dict)
            and list(a.keys()) == list(b.keys())
            and all(
                nested_equal(
                    a[k],
                    b[k],
                )
                for k in a
            )
        )

    if isinstance(
        a,
        (list, tuple),
    ):
        return (
            isinstance(b, type(a))
            and len(a) == len(b)
            and all(
                nested_equal(x, y)
                for x, y in zip(a, b)
            )
        )

    return a == b


def model_digest(model):
    """
    SHA256 over every tensor in model.state_dict().

    This checks the complete frozen backbone plus all PEFT/head
    parameters, not merely currently trainable tensors.
    """
    h = hashlib.sha256()

    state = model.state_dict()

    for name in sorted(
        state.keys()
    ):
        t = (
            state[name]
            .detach()
            .cpu()
            .contiguous()
        )

        h.update(
            name.encode("utf-8")
        )

        h.update(
            str(t.dtype).encode(
                "utf-8"
            )
        )

        h.update(
            repr(
                tuple(t.shape)
            ).encode(
                "utf-8"
            )
        )

        raw = (
            t.view(torch.uint8)
            .numpy()
            .tobytes()
        )

        h.update(raw)

    return h.hexdigest()


def snapshot_pool(pool):
    states = {}

    for name, state in (
        pool.states.items()
    ):
        states[name] = {
            "optimizer":
                copy.deepcopy(
                    state.optimizer
                    .state_dict()
                ),

            "memory_items":
                copy.deepcopy(
                    state.memory.items
                ),

            "memory_seen":
                state.memory.seen,

            "memory_rng":
                copy.deepcopy(
                    state.memory.rng
                    .getstate()
                ),

            "updates":
                state.updates,
        }

    return {
        "model_digest":
            model_digest(
                pool.model
            ),

        "peft_configs":
            tuple(
                pool.model
                .peft_config
                .keys()
            ),

        "active_adapter":
            repr(
                getattr(
                    pool.model,
                    "active_adapter",
                    None,
                )
            ),

        "training":
            pool.model.training,

        "next_id":
            pool.next_id,

        "warmup_name":
            pool.warmup_name,

        "state_names":
            tuple(
                pool.states.keys()
            ),

        "states":
            states,

        "global_rng":
            copy.deepcopy(
                capture_rng_state()
            ),
    }


def compare_snapshots(
    before,
    after,
):
    checks = {}

    checks[
        "model_state"
    ] = (
        before[
            "model_digest"
        ]
        == after[
            "model_digest"
        ]
    )

    checks[
        "adapter_registry"
    ] = (
        before[
            "peft_configs"
        ]
        == after[
            "peft_configs"
        ]
    )

    checks[
        "active_adapter"
    ] = (
        before[
            "active_adapter"
        ]
        == after[
            "active_adapter"
        ]
    )

    checks[
        "model_mode"
    ] = (
        before[
            "training"
        ]
        == after[
            "training"
        ]
    )

    checks[
        "next_id"
    ] = (
        before[
            "next_id"
        ]
        == after[
            "next_id"
        ]
    )

    checks[
        "warmup_name"
    ] = (
        before[
            "warmup_name"
        ]
        == after[
            "warmup_name"
        ]
    )

    checks[
        "state_registry"
    ] = (
        before[
            "state_names"
        ]
        == after[
            "state_names"
        ]
    )

    checks[
        "global_rng"
    ] = nested_equal(
        before[
            "global_rng"
        ],
        after[
            "global_rng"
        ],
    )

    for name in before[
        "states"
    ]:
        a = before[
            "states"
        ][name]

        b = after[
            "states"
        ][name]

        checks[
            f"{name}:optimizer"
        ] = nested_equal(
            a["optimizer"],
            b["optimizer"],
        )

        checks[
            f"{name}:memory_items"
        ] = nested_equal(
            a["memory_items"],
            b["memory_items"],
        )

        checks[
            f"{name}:memory_seen"
        ] = (
            a["memory_seen"]
            == b["memory_seen"]
        )

        checks[
            f"{name}:memory_rng"
        ] = nested_equal(
            a["memory_rng"],
            b["memory_rng"],
        )

        checks[
            f"{name}:updates"
        ] = (
            a["updates"]
            == b["updates"]
        )

    return checks


def main():
    seed_all(
        SEED
    )

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA required"
        )

    device = torch.device(
        "cuda"
    )

    print(
        "GPU:",
        torch.cuda.get_device_name(0),
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

    pool = ActionUtilityShadowPool(
        model=model,
        tokenizer=tok,
        lora_config=cfg,
        device=device,
        lr=2e-4,
        memory_size=32,
        memory_probe=4,
        threshold=0.0,
        confidence_z=1.96,
        seed=SEED,
    )

    state_names = list(
        pool.states.keys()
    )

    if len(state_names) != 1:
        raise RuntimeError(
            f"Expected one initial adapter, got {state_names}"
        )

    real_name = (
        state_names[0]
    )

    # Establish:
    # - optimizer moments
    # - mature protected memory
    # without creating another adapter.
    train_texts = [
        "This product works very well.",
        "This purchase was a terrible mistake.",
        "I am very happy with this item.",
        "The quality was disappointing.",
    ]

    train_labels = [
        1,
        0,
        1,
        0,
    ]

    pool.train_step(
        real_name,
        train_texts,
        train_labels,
    )

    if (
        len(
            pool.states[
                real_name
            ].memory.items
        )
        < pool.memory_probe
    ):
        raise RuntimeError(
            "Initial adapter did not mature"
        )

    # Deliberately ODD batch size.
    #
    # Expected complementary folds:
    #
    # Fold A:
    #   support = 3
    #   query   = 2
    #
    # Fold B:
    #   support = 2
    #   query   = 3
    #
    # Total held-out query appearances = 5.
    texts = [
        "The package arrived quickly.",
        "This was not worth the money.",
        "Everything worked as expected.",
        "The item broke almost immediately.",
        "I would buy this again.",
    ]

    labels = [
        1,
        0,
        1,
        0,
        1,
    ]

    pool.activate(
        real_name
    )

    before = snapshot_pool(
        pool
    )

    result = (
        pool.crossfit_action_utility(
            texts=texts,
            labels=labels,
            restore_name=real_name,
        )
    )

    after = snapshot_pool(
        pool
    )

    print()
    print(
        "=== ACTION UTILITY STATUS ==="
    )

    print(
        "status:",
        result.get(
            "status"
        ),
    )

    if (
        result.get(
            "status"
        )
        != "ok"
    ):
        raise RuntimeError(
            f"Unexpected result: {result}"
        )

    print()
    print(
        "=== ODD-BATCH CROSS-FIT ==="
    )

    fold_checks = {
        "batch_n":
            result[
                "batch_n"
            ] == 5,

        "fold_a_support":
            result[
                "fold_a_support_n"
            ] == 3,

        "fold_a_query":
            result[
                "fold_a_query_n"
            ] == 2,

        "fold_b_support":
            result[
                "fold_b_support_n"
            ] == 2,

        "fold_b_query":
            result[
                "fold_b_query_n"
            ] == 3,

        "all_examples_query_once":
            (
                result[
                    "fold_a_query_n"
                ]
                + result[
                    "fold_b_query_n"
                ]
            ) == 5,
    }

    for name, ok in (
        fold_checks.items()
    ):
        print(
            f"{name:28s}",
            "PASS"
            if ok
            else "FAIL",
        )

    print()
    print(
        "=== STATE RESTORATION ==="
    )

    state_checks = (
        compare_snapshots(
            before,
            after,
        )
    )

    for name, ok in (
        state_checks.items()
    ):
        print(
            f"{name:28s}",
            "PASS"
            if ok
            else "FAIL",
        )

    print()
    print(
        "temporary fresh exists:",
        "__shadow_fresh__"
        in pool.model.peft_config,
    )

    all_ok = (
        all(
            fold_checks.values()
        )
        and
        all(
            state_checks.values()
        )
        and
        "__shadow_fresh__"
        not in pool.model.peft_config
    )

    print()
    print(
        "=== FINAL UNIT AUDIT ==="
    )

    print(
        "PASS"
        if all_ok
        else "FAIL"
    )

    if not all_ok:
        raise RuntimeError(
            "Action-utility unit audit failed"
        )


if __name__ == "__main__":
    main()
