import copy
import random

from src.adapter_pool_cau_v0 import (
    CAUV0AdapterPool,
)


# ---------------------------------------------------------
# Lightweight deterministic state objects.
#
# We are testing LIVE CONTROLLER LOGIC here.
#
# Exact real-model transactional restoration was already
# independently tested during Day 3.
# ---------------------------------------------------------


class FakeMemory:
    def __init__(
        self,
        seed,
        mature=True,
    ):
        self.rng = random.Random(
            seed
        )

        if mature:
            self.items = [
                ("old a", 0),
                ("old b", 1),
                ("old c", 0),
                ("old d", 1),
            ]
            self.seen = 4

        else:
            self.items = []
            self.seen = 0


class FakeState:
    def __init__(
        self,
        seed,
        mature=True,
    ):
        self.memory = FakeMemory(
            seed=seed,
            mature=mature,
        )

        self.updates = 0


def profile_result(
    harm_lcb=-0.1,
):
    return {
        "harm": harm_lcb,
        "harm_se": 0.01,
        "harm_lcb": harm_lcb,
        "harm_ucb":
            harm_lcb + 0.02,

        "gain": 0.1,
        "cur_before": 1.0,
        "cur_after": 0.9,
    }


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
            -0.1,

        "harm_mean":
            -0.05,
    }


def utility_result(
    reuses=None,
    fresh_positive=False,
    status="ok",
):
    if status != "ok":
        return {
            "status": status,
        }

    if reuses is None:
        reuses = {
            "default":
                reuse_profile(
                    utility=0.2
                )
        }

    feasible = [
        name
        for name, p
        in reuses.items()
        if p[
            "feasible_both"
        ]
    ]

    if feasible:
        best = max(
            feasible,
            key=lambda name:
                reuses[name][
                    "system_utility"
                ],
        )

        best_u = (
            reuses[
                best
            ][
                "system_utility"
            ]
        )

    else:
        best = None
        best_u = None

    fresh_u = (
        0.5
        if fresh_positive
        else -0.1
    )

    fresh_adv = (
        None
        if best_u is None
        else fresh_u - best_u
    )

    return {
        "status": "ok",

        "reuse_profiles":
            copy.deepcopy(
                reuses
            ),

        "best_reuse":
            best,

        "best_reuse_utility":
            best_u,

        "fresh_positive":
            fresh_positive,

        "fresh_utility":
            fresh_u,

        "fresh_advantage":
            fresh_adv,
    }


class LogicPool(
    CAUV0AdapterPool
):
    """
    Deterministic controller harness.

    Overrides expensive neural operations but runs the
    REAL CAUV0AdapterPool decision code.
    """

    def __init__(self):
        # Do NOT call neural parent constructor.

        self.threshold = 0.0
        self.memory_probe = 4

        self.pending_fresh = False
        self.warmup_name = None

        self.next_id = 1

        self.states = {
            "default":
                FakeState(
                    seed=100,
                    mature=True,
                )
        }

        self.active = "default"

        self.fake_utility = (
            utility_result()
        )

        self.profile_table = {
            "default":
                profile_result(
                    harm_lcb=-0.1
                )
        }

        self.train_calls = 0

    def activate(
        self,
        name,
    ):
        if name not in self.states:
            raise RuntimeError(
                f"Unknown adapter {name}"
            )

        self.active = name

    def crossfit_action_utility(
        self,
        texts,
        labels,
        restore_name,
    ):
        return copy.deepcopy(
            self.fake_utility
        )

    def profile(
        self,
        name,
        texts,
        labels,
    ):
        # Deliberately perturb the private reservoir RNG.
        # _full_batch_guarded_reuse() must restore it.
        self.activate(name)

        self.states[
            name
        ].memory.rng.random()

        return copy.deepcopy(
            self.profile_table[
                name
            ]
        )

    def spawn(self):
        name = (
            f"adapter_{self.next_id}"
        )

        self.next_id += 1

        self.states[
            name
        ] = FakeState(
            seed=1000
            + self.next_id,
            mature=False,
        )

        self.warmup_name = name

        self.activate(
            name
        )

        return name

    def train_step(
        self,
        name,
        texts,
        labels,
    ):
        self.activate(
            name
        )

        state = self.states[
            name
        ]

        self.train_calls += 1
        state.updates += 1

        for text, label in zip(
            texts,
            labels,
        ):
            state.memory.items.append(
                (
                    text,
                    int(label),
                )
            )

            state.memory.seen += 1

        return 0.123

    def add_mature_adapter(
        self,
        name,
        seed,
    ):
        self.states[
            name
        ] = FakeState(
            seed=seed,
            mature=True,
        )

        self.profile_table[
            name
        ] = profile_result(
            harm_lcb=-0.1
        )


def learner_snapshot(
    pool,
):
    """
    Learning-system state only.

    pending_fresh is intentionally excluded because it is
    controller evidence state and MAY change during DEFER.
    """

    states = {}

    for name, state in (
        pool.states.items()
    ):
        states[name] = {
            "items":
                copy.deepcopy(
                    state.memory.items
                ),

            "seen":
                state.memory.seen,

            "rng":
                copy.deepcopy(
                    state.memory.rng
                    .getstate()
                ),

            "updates":
                state.updates,
        }

    return {
        "active":
            pool.active,

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

        "train_calls":
            pool.train_calls,
    }


def check(
    name,
    condition,
):
    print(
        f"{name:46s}",
        "PASS"
        if condition
        else "FAIL"
    )

    if not condition:
        raise AssertionError(
            name
        )


TEXTS = [
    "incoming one",
    "incoming two",
]

LABELS = [
    0,
    1,
]


# =========================================================
# 1. FULL-BATCH GUARD RESTORES PRIVATE RNG + ACTIVE ADAPTER
# =========================================================

print()
print(
    "=== FULL-BATCH GUARD TRANSACTION ==="
)

p = LogicPool()

rng_before = (
    p.states[
        "default"
    ].memory.rng
    .getstate()
)

best, guards = (
    p._full_batch_guarded_reuse(
        texts=TEXTS,
        labels=LABELS,
        restore_name="default",
        utility=p.fake_utility,
    )
)

rng_after = (
    p.states[
        "default"
    ].memory.rng
    .getstate()
)

check(
    "guard returns safe default",
    best == "default",
)

check(
    "private reservoir RNG restored",
    rng_before == rng_after,
)

check(
    "active adapter restored",
    p.active == "default",
)

check(
    "full-batch safe recorded",
    guards[
        "default"
    ][
        "full_batch_safe"
    ] is True,
)


# =========================================================
# 2. ORDINARY POSITIVE GUARDED REUSE
# =========================================================

print()
print(
    "=== POSITIVE GUARDED REUSE ==="
)

p = LogicPool()

before_updates = (
    p.states[
        "default"
    ].updates
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "reuse decision",
    info[
        "decision"
    ] == "reuse",
)

check(
    "reuse reason",
    info[
        "reason"
    ] == "positive_guarded_reuse",
)

check(
    "correct reuse adapter",
    name == "default",
)

check(
    "real update executed once",
    p.states[
        "default"
    ].updates
    == before_updates + 1,
)

check(
    "train loss returned",
    loss is not None,
)


# =========================================================
# 3. FULL-BATCH GUARD REJECTION -> LITERAL DEFER
# =========================================================

print()
print(
    "=== FULL-BATCH REJECTION -> DEFER ==="
)

p = LogicPool()

p.profile_table[
    "default"
] = profile_result(
    harm_lcb=0.05
)

before = learner_snapshot(
    p
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

after = learner_snapshot(
    p
)

check(
    "guard rejection defers",
    info[
        "decision"
    ] == "defer",
)

check(
    "guard rejection reason",
    info[
        "reason"
    ] == "no_positive_guarded_reuse",
)

check(
    "defer returns real adapter",
    name == "default",
)

check(
    "defer has no train loss",
    loss is None,
)

check(
    "defer leaves learner state identical",
    before == after,
)


# =========================================================
# 4. STRICT ZERO UTILITY -> DEFER
# =========================================================

print()
print(
    "=== ZERO UTILITY -> DEFER ==="
)

p = LogicPool()

p.fake_utility = utility_result(
    reuses={
        "default":
            reuse_profile(
                utility=0.0
            )
    },
    fresh_positive=False,
)

before = learner_snapshot(
    p
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

after = learner_snapshot(
    p
)

check(
    "zero reuse utility defers",
    info[
        "decision"
    ] == "defer",
)

check(
    "strict zero causes no update",
    before == after,
)


# =========================================================
# 5. FIRST FRESH-POSITIVE + SAFE REUSE
# =========================================================

print()
print(
    "=== FIRST FRESH POSITIVE + REUSE ==="
)

p = LogicPool()

p.fake_utility = utility_result(
    fresh_positive=True
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "first fresh does not spawn",
    info[
        "decision"
    ] == "reuse",
)

check(
    "pending fresh becomes true",
    p.pending_fresh is True,
)

check(
    "pending-fresh reuse reason",
    info[
        "reason"
    ]
    ==
    "pending_fresh_guarded_reuse",
)

check(
    "reuse update executed",
    loss is not None,
)

check(
    "adapter count unchanged",
    len(
        p.states
    ) == 1,
)


# =========================================================
# 6. FIRST FRESH-POSITIVE + NO SAFE REUSE -> DEFER
# =========================================================

print()
print(
    "=== FIRST FRESH POSITIVE + DEFER ==="
)

p = LogicPool()

p.fake_utility = utility_result(
    fresh_positive=True
)

p.profile_table[
    "default"
] = profile_result(
    harm_lcb=0.05
)

before = learner_snapshot(
    p
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

after = learner_snapshot(
    p
)

check(
    "first fresh unsafe reuse defers",
    info[
        "decision"
    ] == "defer",
)

check(
    "fresh evidence remains pending",
    p.pending_fresh is True,
)

check(
    "defer reason",
    info[
        "reason"
    ]
    ==
    "pending_fresh_no_guarded_reuse",
)

check(
    "no real learner-state mutation",
    before == after,
)


# =========================================================
# 7. SECOND FRESH-POSITIVE -> SPAWN
# =========================================================

print()
print(
    "=== CONFIRMED FRESH -> SPAWN ==="
)

p = LogicPool()

p.fake_utility = utility_result(
    fresh_positive=True
)

p.pending_fresh = True

before_count = len(
    p.states
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "confirmed fresh spawns",
    info[
        "decision"
    ] == "spawn",
)

check(
    "spawn reason",
    info[
        "reason"
    ] == "confirmed_fresh",
)

check(
    "one permanent adapter created",
    len(
        p.states
    )
    == before_count + 1,
)

check(
    "new adapter selected",
    name == "adapter_1",
)

check(
    "new adapter trained",
    p.states[
        "adapter_1"
    ].updates == 1,
)

check(
    "spawn establishes warmup",
    p.warmup_name
    == "adapter_1",
)

check(
    "pending evidence cleared",
    p.pending_fresh is False,
)

check(
    "spawn training loss returned",
    loss is not None,
)


# =========================================================
# 8. POST-SPAWN WARMUP
# =========================================================

print()
print(
    "=== POST-SPAWN WARMUP ==="
)

# adapter_1 has 2 examples from the spawn update,
# below memory_probe=4.

p.pending_fresh = True

name2, info2, loss2 = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="adapter_1",
    )
)

check(
    "warmup decision",
    info2[
        "decision"
    ] == "warmup",
)

check(
    "warmup uses spawned adapter",
    name2 == "adapter_1",
)

check(
    "warmup resets pending evidence",
    p.pending_fresh is False,
)

check(
    "warmup executes training",
    loss2 is not None,
)

check(
    "spawned adapter now mature-sized",
    len(
        p.states[
            "adapter_1"
        ].memory.items
    )
    >= p.memory_probe,
)


# =========================================================
# 9. UNAVAILABLE UTILITY -> DEFER
# =========================================================

print()
print(
    "=== UNAVAILABLE UTILITY -> DEFER ==="
)

p = LogicPool()

p.fake_utility = (
    utility_result(
        status="unavailable"
    )
)

p.pending_fresh = True

before = learner_snapshot(
    p
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

after = learner_snapshot(
    p
)

check(
    "unavailable diagnostic defers",
    info[
        "decision"
    ] == "defer",
)

check(
    "unavailable clears pending",
    p.pending_fresh is False,
)

check(
    "unavailable leaves learner state unchanged",
    before == after,
)


# =========================================================
# 10. BEST CROSS-FIT CANDIDATE FAILS GUARD;
#     LOWER-UTILITY SAFE CANDIDATE SURVIVES
# =========================================================

print()
print(
    "=== GUARDED FALLBACK CANDIDATE ==="
)

p = LogicPool()

p.add_mature_adapter(
    name="adapter_1",
    seed=200,
)

p.fake_utility = utility_result(
    reuses={
        "default":
            reuse_profile(
                utility=0.20
            ),

        "adapter_1":
            reuse_profile(
                utility=0.30
            ),
    },
    fresh_positive=False,
)

# Highest-utility adapter fails the exact
# full-batch retention guard.
p.profile_table[
    "adapter_1"
] = profile_result(
    harm_lcb=0.05
)

# Lower-utility default remains safe.
p.profile_table[
    "default"
] = profile_result(
    harm_lcb=-0.05
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "unsafe best candidate rejected",
    info[
        "full_batch_guards"
    ][
        "adapter_1"
    ][
        "full_batch_safe"
    ] is False,
)

check(
    "safe fallback candidate retained",
    info[
        "full_batch_guards"
    ][
        "default"
    ][
        "full_batch_safe"
    ] is True,
)

check(
    "safe fallback selected",
    name == "default",
)

check(
    "fallback still performs reuse",
    info[
        "decision"
    ] == "reuse",
)


print()
print(
    "============================================"
)

print(
    "CAU-v0 LOGIC UNIT AUDIT: PASS"
)

print(
    "============================================"
)
