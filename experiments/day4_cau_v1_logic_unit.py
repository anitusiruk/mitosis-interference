import copy
import random

from src.adapter_pool_cau_v1 import (
    CAUV1AdapterPool,
)


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
                ("old-1", 0),
                ("old-2", 1),
                ("old-3", 0),
                ("old-4", 1),
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


def reuse_profile(
    utility,
    feasible=True,
    harm_lcb_max=-0.10,
    harm_mean=-0.05,
):
    return {
        "system_utility":
            utility,

        "feasible_both":
            feasible,

        "harm_lcb_max":
            harm_lcb_max,

        "harm_mean":
            harm_mean,
    }


def full_profile(
    harm_lcb=-0.10,
):
    return {
        "harm":
            harm_lcb,

        "harm_se":
            0.01,

        "harm_lcb":
            harm_lcb,

        "harm_ucb":
            harm_lcb + 0.02,

        "gain":
            0.05,

        "cur_before":
            1.0,

        "cur_after":
            0.95,
    }


def utility_result(
    reuses,
    fresh_positive=False,
    fresh_utility=None,
    status="ok",
):
    if status != "ok":
        return {
            "status":
                status,
        }

    feasible = [
        name
        for name, profile
        in reuses.items()
        if profile[
            "feasible_both"
        ]
    ]

    if feasible:
        best = min(
            feasible,
            key=lambda name: (
                -reuses[
                    name
                ][
                    "system_utility"
                ],

                reuses[
                    name
                ][
                    "harm_lcb_max"
                ],

                reuses[
                    name
                ][
                    "harm_mean"
                ],

                name,
            ),
        )

        best_u = reuses[
            best
        ][
            "system_utility"
        ]

    else:
        best = None
        best_u = None

    if fresh_utility is None:
        fresh_utility = (
            0.20
            if fresh_positive
            else -0.20
        )

    advantage = (
        None
        if best_u is None
        else (
            fresh_utility
            - best_u
        )
    )

    return {
        "status":
            "ok",

        "reuse_profiles":
            copy.deepcopy(
                reuses
            ),

        "best_reuse":
            best,

        "best_reuse_utility":
            best_u,

        "fresh_positive":
            bool(
                fresh_positive
            ),

        "fresh_utility":
            fresh_utility,

        "fresh_advantage":
            advantage,
    }


class LogicPoolV1(
    CAUV1AdapterPool
):
    def __init__(self):

        # Neural parent constructor intentionally omitted.
        # This exercises real CAU-v1 controller logic with
        # deterministic lightweight action outcomes.

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
            utility_result(
                {
                    "default":
                        reuse_profile(
                            -0.05
                        )
                }
            )
        )

        self.profile_table = {
            "default":
                full_profile(
                    -0.10
                )
        }

        self.train_calls = 0

    def activate(
        self,
        name,
    ):
        if name not in self.states:
            raise RuntimeError(
                f"Unknown adapter: {name}"
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
        self.activate(
            name
        )

        # Deliberately advance private RNG.
        # CAU guard wrapper must restore it.
        self.states[
            name
        ].memory.rng.random()

        return copy.deepcopy(
            self.profile_table[
                name
            ]
        )

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

        state.updates += 1
        self.train_calls += 1

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

    def add_mature(
        self,
        name,
        seed,
        harm_lcb=-0.10,
    ):
        self.states[
            name
        ] = FakeState(
            seed=seed,
            mature=True,
        )

        self.profile_table[
            name
        ] = full_profile(
            harm_lcb
        )


def check(
    label,
    condition,
):
    print(
        f"{label:58s}",
        "PASS"
        if condition
        else "FAIL"
    )

    if not condition:
        raise AssertionError(
            label
        )


TEXTS = [
    "incoming-a",
    "incoming-b",
]

LABELS = [
    0,
    1,
]


# =========================================================
# 1. CORE V1 CHANGE:
#    SAFE NEGATIVE-UTILITY EXISTING ADAPTER STILL TRAINS
# =========================================================

print()
print(
    "=== NEGATIVE ONE-STEP UTILITY, SAFE EXISTING CAPACITY ==="
)

p = LogicPoolV1()

p.fake_utility = utility_result({
    "default":
        reuse_profile(
            utility=-0.05
        )
})

before_updates = (
    p.states[
        "default"
    ].updates
)

rng_before = (
    p.states[
        "default"
    ].memory.rng
    .getstate()
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "negative utility does NOT cause defer",
    info[
        "decision"
    ] == "reuse",
)

check(
    "v1 reason identifies safe existing reuse",
    info[
        "reason"
    ] == "safe_existing_reuse",
)

check(
    "default selected",
    name == "default",
)

check(
    "real update executed",
    p.states[
        "default"
    ].updates
    == before_updates + 1,
)

check(
    "real loss returned",
    loss is not None,
)

check(
    "negative candidate was full-batch checked",
    "default"
    in info[
        "full_batch_guards"
    ],
)

check(
    "guard records utility as negative",
    info[
        "full_batch_guards"
    ][
        "default"
    ][
        "crossfit_utility"
    ] < 0.0,
)

check(
    "guard records utility positivity false",
    info[
        "full_batch_guards"
    ][
        "default"
    ][
        "crossfit_utility_positive"
    ] is False,
)

# profile advanced RNG, wrapper restored it, then real
# train_step in this lightweight test does not touch RNG.
check(
    "prospective guard private RNG restored",
    rng_before
    ==
    p.states[
        "default"
    ].memory.rng
    .getstate(),
)


# =========================================================
# 2. FIRST FRESH-POSITIVE WINDOW:
#    SAFE NEGATIVE EXISTING CAPACITY STILL LEARNS
# =========================================================

print()
print(
    "=== FIRST FRESH POSITIVE + NEGATIVE SAFE REUSE ==="
)

p = LogicPoolV1()

p.fake_utility = utility_result(
    {
        "default":
            reuse_profile(
                utility=-0.05
            )
    },
    fresh_positive=True,
    fresh_utility=0.10,
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "first fresh-positive does not spawn",
    info[
        "decision"
    ] == "reuse",
)

check(
    "pending fresh evidence becomes true",
    p.pending_fresh is True,
)

check(
    "first-fresh reuse reason updated",
    info[
        "reason"
    ]
    ==
    "pending_fresh_safe_existing_reuse",
)

check(
    "supervised batch is still learned",
    loss is not None,
)

check(
    "adapter count unchanged",
    len(
        p.states
    ) == 1,
)


# =========================================================
# 3. ALL UTILITIES NEGATIVE:
#    PICK THE LEAST-BAD SAFE EXISTING ACTION
# =========================================================

print()
print(
    "=== BEST SAFE EXISTING ACTION MAY BE NEGATIVE ==="
)

p = LogicPoolV1()

p.add_mature(
    "adapter_1",
    seed=200,
)

p.fake_utility = utility_result({
    "default":
        reuse_profile(
            utility=-0.30
        ),

    "adapter_1":
        reuse_profile(
            utility=-0.05
        ),
})

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "higher utility among negative actions selected",
    name == "adapter_1",
)

check(
    "negative winner receives update",
    p.states[
        "adapter_1"
    ].updates == 1,
)

check(
    "decision remains reuse",
    info[
        "decision"
    ] == "reuse",
)


# =========================================================
# 4. RETENTION UNSAFE EXISTING CAPACITY STILL DEFERS
# =========================================================

print()
print(
    "=== NO RETENTION-FEASIBLE EXISTING ACTION -> DEFER ==="
)

p = LogicPoolV1()

p.fake_utility = utility_result({
    "default":
        reuse_profile(
            utility=-0.05
        )
})

p.profile_table[
    "default"
] = full_profile(
    harm_lcb=0.05
)

before_updates = (
    p.states[
        "default"
    ].updates
)

before_seen = (
    p.states[
        "default"
    ].memory.seen
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "unsafe existing action defers",
    info[
        "decision"
    ] == "defer",
)

check(
    "reason means retention infeasible",
    info[
        "reason"
    ] == "no_retention_feasible_reuse",
)

check(
    "no optimizer-equivalent update executed",
    p.states[
        "default"
    ].updates
    == before_updates,
)

check(
    "no replay addition executed",
    p.states[
        "default"
    ].memory.seen
    == before_seen,
)

check(
    "defer returns no train loss",
    loss is None,
)


# =========================================================
# 5. CROSS-FOLD INFEASIBLE ACTION STILL DEFERS
# =========================================================

print()
print(
    "=== CROSS-FOLD INFEASIBLE EXISTING ACTION -> DEFER ==="
)

p = LogicPoolV1()

p.fake_utility = utility_result({
    "default":
        reuse_profile(
            utility=0.50,
            feasible=False,
        )
})

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "cross-fold infeasible action not trained",
    info[
        "decision"
    ] == "defer",
)

check(
    "no prospective full-batch guard run",
    info[
        "full_batch_guards"
    ] == {},
)

check(
    "defer has no train loss",
    loss is None,
)


# =========================================================
# 6. UNAVAILABLE DIAGNOSTIC STILL DEFERS
# =========================================================

print()
print(
    "=== UNAVAILABLE DIAGNOSTIC -> DEFER ==="
)

p = LogicPoolV1()

p.fake_utility = utility_result(
    {},
    status="unavailable",
)

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "unavailable remains defer",
    info[
        "decision"
    ] == "defer",
)

check(
    "unavailable reason unchanged",
    info[
        "reason"
    ] == "utility_unavailable",
)

check(
    "unavailable executes no update",
    loss is None,
)


# =========================================================
# 7. CONFIRMED FRESH STILL SPAWNS
# =========================================================

print()
print(
    "=== CONFIRMED FRESH STILL SPAWNS ==="
)

p = LogicPoolV1()

p.pending_fresh = True

p.fake_utility = utility_result(
    {
        "default":
            reuse_profile(
                utility=-0.05
            )
    },
    fresh_positive=True,
    fresh_utility=0.10,
)

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
    "confirmed fresh decision is spawn",
    info[
        "decision"
    ] == "spawn",
)

check(
    "one adapter added",
    len(
        p.states
    )
    == before_count + 1,
)

check(
    "new adapter trained",
    p.states[
        name
    ].updates == 1,
)

check(
    "pending evidence clears",
    p.pending_fresh is False,
)

check(
    "spawn still establishes warmup",
    p.warmup_name == name,
)

check(
    "spawn returns train loss",
    loss is not None,
)


# =========================================================
# 8. EXACT NEGATIVE-UTILITY TIE:
#    LOWER ADAPTER NAME STILL WINS
# =========================================================

print()
print(
    "=== NEGATIVE EXACT TIE ==="
)

p = LogicPoolV1()

p.add_mature(
    "adapter_1",
    seed=201,
)

p.add_mature(
    "adapter_2",
    seed=202,
)

p.fake_utility = utility_result({
    "default":
        reuse_profile(
            utility=-0.50
        ),

    "adapter_1": {
        "system_utility": -0.05,
        "feasible_both": True,
        "harm_lcb_max": -0.10,
        "harm_mean": -0.05,
    },

    "adapter_2": {
        "system_utility": -0.05,
        "feasible_both": True,
        "harm_lcb_max": -0.10,
        "harm_mean": -0.05,
    },
})

name, info, loss = (
    p.live_step(
        TEXTS,
        LABELS,
        restore_name="default",
    )
)

check(
    "lower adapter name wins exact negative tie",
    name == "adapter_1",
)

check(
    "tie winner really trained",
    p.states[
        "adapter_1"
    ].updates == 1,
)


print()
print(
    "============================================"
)

print(
    "CAU-v1 LEARNING-CONTINUITY LOGIC AUDIT: PASS"
)

print(
    "============================================"
)
