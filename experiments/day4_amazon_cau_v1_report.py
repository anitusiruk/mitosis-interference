import json
from pathlib import Path

import pandas as pd


ROOT = Path(
    "results"
)

PATHS = {
    "v3":
        ROOT
        / "controller_domain_recurrence_v3_seed2026",

    "cau_v0":
        ROOT
        / "controller_domain_recurrence_cau_v0_seed2026",

    "cau_v1":
        ROOT
        / "controller_domain_recurrence_cau_v1_seed2026",
}


def longest_true_run(
    values,
):
    best = 0
    current = 0

    for value in values:
        if bool(value):
            current += 1
            best = max(
                best,
                current,
            )
        else:
            current = 0

    return best


def read_routing(
    name,
):
    return pd.read_csv(
        PATHS[name]
        / "routing.csv"
    )


def read_eval(
    name,
):
    return pd.read_csv(
        PATHS[name]
        / "eval_matrix.csv"
    )


v3 = read_routing(
    "v3"
)

v0 = read_routing(
    "cau_v0"
)

v1 = read_routing(
    "cau_v1"
)


print(
    "=" * 96
)

print(
    "AMAZON CAU-v1 PREDECLARED DEVELOPMENT REPORT"
)

print(
    "=" * 96
)


# =========================================================
# ACTION COUNTS
# =========================================================

print()
print(
    "=== GLOBAL ACTION COUNTS ==="
)

for name, df in [
    ("V3", v3),
    ("CAU-v0", v0),
    ("CAU-v1", v1),
]:
    counts = (
        df[
            "decision"
        ]
        .value_counts()
        .to_dict()
    )

    print(
        f"{name:8s}",
        counts,
    )


print()
print(
    "=== CAU-v1 ACTIONS BY SEGMENT ==="
)

print(
    pd.crosstab(
        v1[
            "segment"
        ],
        v1[
            "decision"
        ],
    )
    .to_string()
)


# =========================================================
# LEARNING CONTINUITY
# =========================================================

print()
print(
    "=== LEARNING CONTINUITY ==="
)

continuity_rows = []

for name, df in [
    ("CAU-v0", v0),
    ("CAU-v1", v1),
]:

    for segment, g in df.groupby(
        "segment",
        sort=False,
    ):
        defer_mask = (
            g[
                "decision"
            ]
            == "defer"
        )

        continuity_rows.append({
            "method":
                name,

            "segment":
                segment,

            "n":
                len(g),

            "updates":
                int(
                    (
                        ~defer_mask
                    ).sum()
                ),

            "defers":
                int(
                    defer_mask.sum()
                ),

            "update_fraction":
                float(
                    (
                        ~defer_mask
                    ).mean()
                ),

            "longest_defer_streak":
                longest_true_run(
                    defer_mask.tolist()
                ),
        })


continuity = pd.DataFrame(
    continuity_rows
)

print(
    continuity
    .round(4)
    .to_string(
        index=False
    )
)


# =========================================================
# REASONS
# =========================================================

print()
print(
    "=== CAU-v1 REASONS ==="
)

print(
    v1[
        "cau_reason"
    ]
    .fillna(
        "__NA__"
    )
    .value_counts()
    .to_string()
)


# =========================================================
# SPAWNS
# =========================================================

print()
print(
    "=== CAU-v1 SPAWNS ==="
)

spawn_cols = [
    c
    for c in [
        "step",
        "segment",
        "domain",
        "adapter",
        "decision",
        "cau_reason",
        "cau_pending_before",
        "cau_pending_after",
        "statusquo_loss",
        "best_reuse",
        "best_reuse_utility",
        "cau_guarded_best_reuse",
        "fresh_utility",
        "fresh_advantage",
        "fold_a_fresh_utility",
        "fold_b_fresh_utility",
        "loss",
        "num_adapters",
    ]
    if c in v1.columns
]

spawns = v1[
    v1[
        "decision"
    ]
    == "spawn"
]

if spawns.empty:
    print(
        "NONE"
    )

else:
    print(
        spawns[
            spawn_cols
        ]
        .round(5)
        .to_string(
            index=False
        )
    )


# =========================================================
# FULL-BATCH GUARDS
# =========================================================

guard_rows = []

for _, row in v1.iterrows():

    raw = row.get(
        "cau_full_batch_guards"
    )

    if pd.isna(raw):
        continue

    guards = json.loads(
        raw
    )

    for candidate, guard in (
        guards.items()
    ):
        guard_rows.append({
            "step":
                int(
                    row[
                        "step"
                    ]
                ),

            "segment":
                row[
                    "segment"
                ],

            "candidate":
                candidate,

            "utility":
                guard.get(
                    "crossfit_utility"
                ),

            "utility_positive":
                guard.get(
                    "crossfit_utility_positive"
                ),

            "safe":
                guard.get(
                    "full_batch_safe"
                ),

            "harm_lcb":
                guard.get(
                    "full_batch_harm_lcb"
                ),
        })


guards = pd.DataFrame(
    guard_rows
)

print()
print(
    "=== CAU-v1 FULL-BATCH GUARDS ==="
)

if guards.empty:
    print(
        "NO GUARD EVALUATIONS"
    )

else:
    print(
        "evaluations:",
        len(
            guards
        )
    )

    print(
        "safe:",
        int(
            guards[
                "safe"
            ]
            .fillna(
                False
            )
            .sum()
        )
    )

    print(
        "negative/nonpositive utility evaluated:",
        int(
            (
                guards[
                    "utility"
                ]
                <= 0.0
            ).sum()
        )
    )

    print(
        "negative/nonpositive utility AND safe:",
        int(
            (
                (
                    guards[
                        "utility"
                    ]
                    <= 0.0
                )
                &
                (
                    guards[
                        "safe"
                    ]
                    == True
                )
            ).sum()
        )
    )


# =========================================================
# KEY WINDOWS
# =========================================================

print()
print(
    "=== KEY CAU-v1 WINDOWS ==="
)

key_steps = [
    7,
    11,
    14,
    17,
    20,
    23,
    30,
    33,
    35,
    36,
    46,
    47,
    50,
    69,
    70,
    71,
    80,
]

key_cols = [
    c
    for c in [
        "step",
        "segment",
        "adapter",
        "decision",
        "cau_reason",
        "cau_pending_before",
        "cau_pending_after",
        "statusquo_loss",
        "best_reuse",
        "best_reuse_utility",
        "cau_guarded_best_reuse",
        "fresh_positive",
        "fresh_utility",
        "fresh_advantage",
        "fold_a_fresh_utility",
        "fold_b_fresh_utility",
        "loss",
        "num_adapters",
    ]
    if c in v1.columns
]

print(
    v1[
        v1[
            "step"
        ]
        .isin(
            key_steps
        )
    ][
        key_cols
    ]
    .round(5)
    .to_string(
        index=False
    )
)


# =========================================================
# HELDOUT DEFAULT COMPARISON
# =========================================================

print()
print(
    "=== DEFAULT-ADAPTER HELDOUT ACCURACY ==="
)

eval_frames = []

for name in [
    "v3",
    "cau_v0",
    "cau_v1",
]:

    e = read_eval(
        name
    )

    e = e[
        e[
            "adapter"
        ]
        == "default"
    ][
        [
            "checkpoint",
            "concept",
            "accuracy",
            "loss",
        ]
    ].copy()

    e[
        "method"
    ] = name

    eval_frames.append(
        e
    )


all_eval = pd.concat(
    eval_frames,
    ignore_index=True,
)

acc = (
    all_eval
    .pivot_table(
        index=[
            "checkpoint",
            "concept",
        ],
        columns="method",
        values="accuracy",
        aggfunc="first",
    )
)

print(
    acc
    .round(5)
    .to_string()
)


print()
print(
    "=== MEAN DEFAULT HELDOUT ACCURACY BY CHECKPOINT ==="
)

mean_acc = (
    all_eval
    .groupby(
        [
            "method",
            "checkpoint",
        ],
        sort=False,
    )[
        "accuracy"
    ]
    .mean()
    .unstack(
        "method"
    )
)

print(
    mean_acc
    .round(5)
    .to_string()
)


# =========================================================
# FINAL DESCRIPTIVE SUMMARY
# =========================================================

print()
print(
    "=== DESCRIPTIVE SUMMARY ==="
)

for name, df in [
    ("CAU-v0", v0),
    ("CAU-v1", v1),
]:

    print(
        name,
        {
            "defers":
                int(
                    (
                        df[
                            "decision"
                        ]
                        == "defer"
                    ).sum()
                ),

            "spawns":
                int(
                    (
                        df[
                            "decision"
                        ]
                        == "spawn"
                    ).sum()
                ),

            "max_adapters":
                int(
                    df[
                        "num_adapters"
                    ].max()
                ),

            "updates":
                int(
                    (
                        df[
                            "decision"
                        ]
                        != "defer"
                    ).sum()
                ),
        },
    )


print()
print(
    "No numerical pass threshold is imposed by this report."
)

print(
    "Interpret qualitative structural behavior before any further revision."
)
