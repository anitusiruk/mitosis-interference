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

from experiments.signal_scan import seed_all

from src.adapter_pool import (
    capture_rng_state,
)

from src.adapter_pool_cau_v0 import (
    CAUV0AdapterPool,
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
    h = hashlib.sha256()

    for name, tensor in sorted(
        model.state_dict().items()
    ):
        t = (
            tensor
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

        h.update(
            t.view(torch.uint8)
            .numpy()
            .tobytes()
        )

    return h.hexdigest()


def snapshot_learner(pool):
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

        "adapter_registry":
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


def snapshots_equal(a, b):
    return nested_equal(
        a,
        b,
    )


def show_snapshot_diff(
    before,
    after,
):
    """
    Diagnostic only.
    Prints the smallest paths that differ.
    """

    def walk(
        path,
        a,
        b,
    ):
        if torch.is_tensor(a):
            if not torch.is_tensor(b):
                print(
                    "DIFF",
                    path,
                    "type:",
                    type(a),
                    type(b),
                )
                return

            if (
                a.dtype != b.dtype
                or tuple(a.shape)
                != tuple(b.shape)
            ):
                print(
                    "DIFF",
                    path,
                    "tensor metadata",
                    a.dtype,
                    tuple(a.shape),
                    b.dtype,
                    tuple(b.shape),
                )
                return

            if not torch.equal(
                a,
                b,
            ):
                aa = (
                    a.detach()
                    .float()
                    .cpu()
                )

                bb = (
                    b.detach()
                    .float()
                    .cpu()
                )

                print(
                    "DIFF",
                    path,
                    "tensor max_abs=",
                    float(
                        (
                            aa - bb
                        )
                        .abs()
                        .max()
                        .item()
                    ),
                )

            return

        if isinstance(
            a,
            np.ndarray,
        ):
            if (
                not isinstance(
                    b,
                    np.ndarray,
                )
                or a.dtype != b.dtype
                or a.shape != b.shape
                or not np.array_equal(
                    a,
                    b,
                )
            ):
                print(
                    "DIFF",
                    path,
                    "numpy array",
                )

            return

        if isinstance(
            a,
            dict,
        ):
            if not isinstance(
                b,
                dict,
            ):
                print(
                    "DIFF",
                    path,
                    "dict/type mismatch",
                )
                return

            keys = sorted(
                set(a)
                | set(b)
            )

            for key in keys:
                if key not in a:
                    print(
                        "DIFF",
                        f"{path}.{key}",
                        "missing before",
                    )
                    continue

                if key not in b:
                    print(
                        "DIFF",
                        f"{path}.{key}",
                        "missing after",
                    )
                    continue

                walk(
                    f"{path}.{key}",
                    a[key],
                    b[key],
                )

            return

        if isinstance(
            a,
            (list, tuple),
        ):
            if (
                not isinstance(
                    b,
                    type(a),
                )
                or len(a) != len(b)
            ):
                print(
                    "DIFF",
                    path,
                    "sequence metadata",
                    type(a),
                    len(a),
                    type(b),
                    (
                        len(b)
                        if hasattr(
                            b,
                            "__len__",
                        )
                        else None
                    ),
                )
                return

            for i, (x, y) in enumerate(
                zip(a, b)
            ):
                walk(
                    f"{path}[{i}]",
                    x,
                    y,
                )

            return

        if a != b:
            print(
                "DIFF",
                path,
                "before=",
                repr(a),
                "after=",
                repr(b),
            )

    print()
    print(
        "=== SNAPSHOT DIFFERENCES ==="
    )

    walk(
        "snapshot",
        before,
        after,
    )

    print(
        "=== END SNAPSHOT DIFFERENCES ==="
    )
    print()



def check(
    name,
    condition,
):
    print(
        f"{name:48s}",
        "PASS"
        if condition
        else "FAIL"
    )

    if not condition:
        raise AssertionError(
            name
        )


def reuse_profile(
    utility,
    feasible=True,
):
    return {
        "system_utility":
            utility,

        "feasible_both":
            feasible,

        "harm_lcb_max":
            -0.01,

        "harm_mean":
            -0.01,
    }


class ForcedCAUPool(
    CAUV0AdapterPool
):
    """
    Real neural model / optimizer / reservoir state.

    Only the cross-fitted utility OUTPUT is forced so
    individual live branches can be tested deterministically.

    profile(), spawn(), train_step(), adapter state,
    optimizer state, memory and RNG are all real.
    """

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
                "unavailable",
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


def make_pool():
    seed_all(
        SEED
    )

    device = torch.device(
        "cuda"
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

    pool = ForcedCAUPool(
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

    return pool


TEXTS = [
    "The product works perfectly.",
    "This item was a terrible purchase.",
    "I am very pleased with the quality.",
    "The product failed immediately.",
]

LABELS = [
    1,
    0,
    1,
    0,
]


print(
    "GPU:",
    torch.cuda.get_device_name(0),
)


# =========================================================
# Establish a real mature learner.
# =========================================================

pool = make_pool()

default = list(
    pool.states.keys()
)[0]

pool.train_step(
    default,
    TEXTS,
    LABELS,
)

check(
    "default mature",
    len(
        pool.states[
            default
        ].memory.items
    )
    >= pool.memory_probe,
)


# =========================================================
# 0. MATURE-WARMUP -> DECISION-READY TRANSITION
#
# train_step() has made the initial adapter mature, but
# existing semantics intentionally leave warmup_name set
# until the NEXT decision. select_action() must clear only
# that controller bookkeeping flag before evaluating
# utility.
# =========================================================

print()
print(
    "=== MATURE WARMUP TRANSITION ==="
)

check(
    "mature adapter still marked warmup before decision",
    pool.warmup_name == default,
)

before_transition = snapshot_learner(
    pool
)

selected0, info0 = (
    pool.select_action(
        TEXTS,
        LABELS,
        restore_name=default,
    )
)

after_transition = snapshot_learner(
    pool
)

expected_transition = copy.deepcopy(
    before_transition
)

expected_transition[
    "warmup_name"
] = None

if not snapshots_equal(
    expected_transition,
    after_transition,
):
    show_snapshot_diff(
        expected_transition,
        after_transition,
    )

check(
    "mature warmup clears before utility decision",
    pool.warmup_name is None,
)

check(
    "unavailable transition decision is defer",
    info0[
        "decision"
    ] == "defer",
)

check(
    "maturation transition changes only warmup flag",
    snapshots_equal(
        expected_transition,
        after_transition,
    ),
)


# =========================================================
# 1. Exact real full-batch guard transaction
# =========================================================

print()
print(
    "=== REAL FULL-BATCH GUARD TRANSACTION ==="
)

utility = {
    "status":
        "ok",

    "reuse_profiles": {
        default:
            reuse_profile(
                utility=0.2,
                feasible=True,
            ),
    },

    "best_reuse":
        default,

    "best_reuse_utility":
        0.2,

    "fresh_positive":
        False,

    "fresh_utility":
        -0.1,

    "fresh_advantage":
        -0.3,
}


before = snapshot_learner(
    pool
)

best, guards = (
    pool._full_batch_guarded_reuse(
        texts=TEXTS,
        labels=LABELS,
        restore_name=default,
        utility=utility,
    )
)

after = snapshot_learner(
    pool
)

check(
    "guard produces diagnostic for default",
    default in guards,
)

check(
    "guard exact learner-state restoration",
    snapshots_equal(
        before,
        after,
    ),
)

check(
    "guard removes no adapters",
    tuple(
        pool.states.keys()
    )
    == (
        default,
    ),
)


# =========================================================
# 2. Utility unavailable -> exact literal DEFER
# =========================================================

print()
print(
    "=== REAL UNAVAILABLE -> DEFER ==="
)

pool.forced_utility = {
    "status":
        "unavailable",
}

pool.pending_fresh = True

before = snapshot_learner(
    pool
)

name, info, loss = (
    pool.live_step(
        TEXTS,
        LABELS,
        restore_name=default,
    )
)

after = snapshot_learner(
    pool
)

check(
    "decision is defer",
    info[
        "decision"
    ] == "defer",
)

check(
    "reason is utility unavailable",
    info[
        "reason"
    ] == "utility_unavailable",
)

check(
    "real adapter preserved",
    name == default,
)

check(
    "no training loss on defer",
    loss is None,
)

check(
    "pending evidence cleared",
    pool.pending_fresh is False,
)

if not snapshots_equal(
    before,
    after,
):
    show_snapshot_diff(
        before,
        after,
    )

check(
    "unavailable defer exactly non-mutating",
    snapshots_equal(
        before,
        after,
    ),
)


# =========================================================
# 3. Exact zero reuse utility -> literal DEFER
# =========================================================

print()
print(
    "=== REAL ZERO UTILITY -> DEFER ==="
)

pool.forced_utility = {
    "status":
        "ok",

    "reuse_profiles": {
        default:
            reuse_profile(
                utility=0.0,
                feasible=True,
            ),
    },

    "best_reuse":
        default,

    "best_reuse_utility":
        0.0,

    "fresh_positive":
        False,

    "fresh_utility":
        -0.1,

    "fresh_advantage":
        -0.1,
}

before = snapshot_learner(
    pool
)

name, info, loss = (
    pool.live_step(
        TEXTS,
        LABELS,
        restore_name=default,
    )
)

after = snapshot_learner(
    pool
)

check(
    "zero utility defers",
    info[
        "decision"
    ] == "defer",
)

check(
    "zero utility has no loss",
    loss is None,
)

check(
    "zero utility exactly non-mutating",
    snapshots_equal(
        before,
        after,
    ),
)


# =========================================================
# 4. First fresh-positive with no positive reuse:
#    DEFER changes evidence state only.
# =========================================================

print()
print(
    "=== REAL FIRST FRESH -> DEFER ==="
)

pool.pending_fresh = False

pool.forced_utility = {
    "status":
        "ok",

    "reuse_profiles": {
        default:
            reuse_profile(
                utility=-0.1,
                feasible=True,
            ),
    },

    "best_reuse":
        default,

    "best_reuse_utility":
        -0.1,

    "fresh_positive":
        True,

    "fresh_utility":
        0.3,

    "fresh_advantage":
        0.4,
}

before = snapshot_learner(
    pool
)

name, info, loss = (
    pool.live_step(
        TEXTS,
        LABELS,
        restore_name=default,
    )
)

after = snapshot_learner(
    pool
)

check(
    "first fresh defers",
    info[
        "decision"
    ] == "defer",
)

check(
    "first fresh sets pending evidence",
    pool.pending_fresh is True,
)

check(
    "first fresh no training loss",
    loss is None,
)

check(
    "first fresh defer learner-state exact",
    snapshots_equal(
        before,
        after,
    ),
)


# =========================================================
# 5. Second consecutive fresh-positive:
#    real permanent adapter spawn + one real update.
# =========================================================

print()
print(
    "=== REAL CONFIRMED FRESH -> SPAWN ==="
)

before_names = tuple(
    pool.states.keys()
)

before_next_id = (
    pool.next_id
)

name, info, loss = (
    pool.live_step(
        TEXTS,
        LABELS,
        restore_name=default,
    )
)

after_names = tuple(
    pool.states.keys()
)

check(
    "confirmed fresh decision spawn",
    info[
        "decision"
    ] == "spawn",
)

check(
    "exactly one real adapter added",
    len(
        after_names
    )
    == len(
        before_names
    ) + 1,
)

check(
    "spawn increments next_id",
    pool.next_id
    == before_next_id + 1,
)

check(
    "spawned name is real state",
    name in pool.states,
)

check(
    "spawned adapter trained once",
    pool.states[
        name
    ].updates == 1,
)

check(
    "spawned memory received batch",
    len(
        pool.states[
            name
        ].memory.items
    )
    == len(
        TEXTS
    ),
)

check(
    "spawn train loss exists",
    loss is not None,
)

check(
    "pending fresh cleared after spawn",
    pool.pending_fresh is False,
)

check(
    "temporary shadow adapter absent",
    "__shadow_fresh__"
    not in pool.model.peft_config,
)


print()
print(
    "=============================================="
)

print(
    "CAU-v0 REAL STATE-INTEGRITY AUDIT: PASS"
)

print(
    "=============================================="
)
