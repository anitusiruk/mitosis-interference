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

from src.adapter_pool_cau_v1 import (
    CAUV1AdapterPool,
)


SEED = 2026


def nested_equal(
    a,
    b,
):
    if torch.is_tensor(a):
        return (
            torch.is_tensor(b)
            and a.dtype == b.dtype
            and tuple(a.shape)
                == tuple(b.shape)
            and torch.equal(a, b)
        )

    if isinstance(
        a,
        np.ndarray,
    ):
        return (
            isinstance(
                b,
                np.ndarray,
            )
            and a.dtype == b.dtype
            and a.shape == b.shape
            and np.array_equal(
                a,
                b,
            )
        )

    if isinstance(
        a,
        dict,
    ):
        return (
            isinstance(b, dict)
            and set(a)
                == set(b)
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
            isinstance(
                b,
                type(a),
            )
            and len(a) == len(b)
            and all(
                nested_equal(
                    x,
                    y,
                )
                for x, y
                in zip(a, b)
            )
        )

    return a == b


def model_digest(
    model,
):
    h = hashlib.sha256()

    for name, tensor in sorted(
        model.state_dict().items()
    ):
        t = (
            tensor.detach()
            .cpu()
            .contiguous()
        )

        h.update(
            name.encode(
                "utf-8"
            )
        )

        h.update(
            t.view(
                torch.uint8
            )
            .numpy()
            .tobytes()
        )

    return h.hexdigest()


def snapshot(
    pool,
):
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

            "items":
                copy.deepcopy(
                    state.memory.items
                ),

            "seen":
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
        "model":
            model_digest(
                pool.model
            ),

        "states":
            states,

        "registry":
            tuple(
                pool.model
                .peft_config
                .keys()
            ),

        "active":
            repr(
                getattr(
                    pool.model,
                    "active_adapter",
                    None,
                )
            ),

        "mode":
            pool.model.training,

        "next_id":
            pool.next_id,

        "warmup":
            pool.warmup_name,

        "global_rng":
            copy.deepcopy(
                capture_rng_state()
            ),
    }


def check(
    label,
    condition,
):
    print(
        f"{label:55s}",
        "PASS"
        if condition
        else "FAIL"
    )

    if not condition:
        raise AssertionError(
            label
        )


class ForcedV1Pool(
    CAUV1AdapterPool
):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        self.forced_utility = {
            "status":
                "unavailable"
        }

    def crossfit_action_utility(
        self,
        texts,
        labels,
        restore_name,
    ):
        return copy.deepcopy(
            self.forced_utility
        )

    def profile(
        self,
        name,
        texts,
        labels,
    ):
        # Execute the REAL prospective profile so all
        # actual PEFT/AdamW/reservoir transaction code runs.
        result = super().profile(
            name,
            texts,
            labels,
        )

        # This test is for the CAU-v1 NEGATIVE-UTILITY
        # reuse branch, not statistical harm calibration.
        #
        # Force only the returned feasibility bit through
        # harm_lcb so the branch is deterministic.
        result = dict(
            result
        )

        result[
            "harm_lcb"
        ] = min(
            float(
                result[
                    "harm_lcb"
                ]
            ),
            -1e-6,
        )

        return result


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

pool = ForcedV1Pool(
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


TEXTS = [
    "This product is excellent.",
    "This product is terrible.",
    "I would buy this again.",
    "I regret buying this.",
]

LABELS = [
    1,
    0,
    1,
    0,
]


default = list(
    pool.states.keys()
)[0]


# Establish mature real optimizer + reservoir state.
pool.train_step(
    default,
    TEXTS,
    LABELS,
)

check(
    "default adapter mature",
    len(
        pool.states[
            default
        ].memory.items
    )
    >= pool.memory_probe,
)

# Normalize lifecycle bookkeeping for this focused test.
pool.warmup_name = None


negative_utility = {
    "status":
        "ok",

    "reuse_profiles": {
        default: {
            "system_utility":
                -0.05,

            "feasible_both":
                True,

            "harm_lcb_max":
                -0.01,

            "harm_mean":
                -0.01,
        },
    },

    "best_reuse":
        default,

    "best_reuse_utility":
        -0.05,

    "fresh_positive":
        False,

    "fresh_utility":
        -0.10,

    "fresh_advantage":
        -0.05,
}


# =========================================================
# Real prospective transaction with NEGATIVE utility
# =========================================================

print()
print(
    "=== REAL NEGATIVE-UTILITY GUARD TRANSACTION ==="
)

before = snapshot(
    pool
)

best, guards = (
    pool._full_batch_guarded_reuse(
        texts=TEXTS,
        labels=LABELS,
        restore_name=default,
        utility=negative_utility,
    )
)

after = snapshot(
    pool
)

check(
    "negative utility candidate is evaluated",
    default in guards,
)

check(
    "negative utility candidate can survive",
    best == default,
)

check(
    "negative sign explicitly recorded",
    guards[
        default
    ][
        "crossfit_utility_positive"
    ] is False,
)

check(
    "prospective transaction exactly restores learner",
    nested_equal(
        before,
        after,
    ),
)


# =========================================================
# Real live_step must now TRAIN that safe negative action
# =========================================================

print()
print(
    "=== REAL NEGATIVE-UTILITY LIVE REUSE ==="
)

pool.forced_utility = (
    negative_utility
)

before_updates = (
    pool.states[
        default
    ].updates
)

before_seen = (
    pool.states[
        default
    ].memory.seen
)

name, info, loss = (
    pool.live_step(
        TEXTS,
        LABELS,
        restore_name=default,
    )
)

check(
    "decision is reuse",
    info[
        "decision"
    ] == "reuse",
)

check(
    "reason is safe existing reuse",
    info[
        "reason"
    ] == "safe_existing_reuse",
)

check(
    "same real adapter selected",
    name == default,
)

check(
    "real optimizer update occurred",
    pool.states[
        default
    ].updates
    == before_updates + 1,
)

check(
    "real replay observation occurred",
    pool.states[
        default
    ].memory.seen
    > before_seen,
)

check(
    "real training loss returned",
    loss is not None,
)

check(
    "no temporary shadow adapter remains",
    "__shadow_fresh__"
    not in pool.model.peft_config,
)


print()
print(
    "========================================="
)

print(
    "CAU-v1 REAL NEGATIVE-UTILITY SMOKE: PASS"
)

print(
    "========================================="
)
