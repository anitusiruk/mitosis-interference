from src.adapter_pool_shadow import (
    ShadowAdapterPool,
)


class CounterfactualAdapterPool(
    ShadowAdapterPool
):
    """
    Live support/query action allocator.

    Pilot objective:
        choose the lower-query-loss action
        among safe reuse and fresh capacity.

    capacity_cost=0 is fixed for this mechanistic
    pilot and is NOT tuned on seed 2026.
    """

    def __init__(
        self,
        *args,
        capacity_cost=0.0,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        self.capacity_cost = (
            float(capacity_cost)
        )

        self.active_name = "default"


    def activate(self, name):
        super().activate(name)
        self.active_name = name


    def select(
        self,
        texts,
        labels,
    ):
        # Preserve the existing warmup semantics.
        if self.warmup_name is not None:

            state = self.states[
                self.warmup_name
            ]

            if (
                len(state.memory.items)
                < self.memory_probe
            ):
                self.activate(
                    self.warmup_name
                )

                return (
                    self.warmup_name,
                    {
                        "decision": "warmup",
                        "best_risk": None,
                        "best_gain": None,
                        "best_lcb": None,
                        "best_ucb": None,
                        "risks": {},
                        "profiles": {},
                        "cf_reason": "warmup",
                        "cf_best_reuse": None,
                        "cf_reuse_query_after": None,
                        "cf_fresh_query_after": None,
                        "cf_fresh_advantage": None,
                        "cf_capacity_cost":
                            self.capacity_cost,
                    },
                )

            self.warmup_name = None

        restore_name = self.active_name

        if restore_name not in self.states:
            restore_name = "default"

        cf = self.shadow_compare(
            texts=texts,
            labels=labels,
            restore_name=restore_name,
        )

        if cf.get("status") != "ok":
            raise RuntimeError(
                "Counterfactual scorer unavailable: "
                f"{cf}"
            )

        profiles = cf[
            "reuse_profiles"
        ]

        risks = {
            name: profile["harm"]
            for name, profile
            in profiles.items()
        }

        best_reuse = cf[
            "best_reuse"
        ]

        fresh_query = cf[
            "fresh_query_after"
        ]

        # Reference profile for compatible logging.
        reference_name = best_reuse

        if (
            reference_name is None
            and profiles
        ):
            reference_name = min(
                profiles,
                key=lambda name:
                    profiles[name][
                        "harm_lcb"
                    ],
            )

        reference = (
            None
            if reference_name is None
            else profiles[
                reference_name
            ]
        )

        # If no existing action satisfies the
        # protected-harm feasibility constraint,
        # isolated fresh capacity is mandatory.
        if best_reuse is None:

            new_name = self.spawn()

            return (
                new_name,
                {
                    "decision": "spawn",
                    "best_risk":
                        None if reference is None
                        else reference["harm"],
                    "best_gain": None,
                    "best_lcb":
                        None if reference is None
                        else reference[
                            "harm_lcb"
                        ],
                    "best_ucb":
                        None if reference is None
                        else reference[
                            "harm_ucb"
                        ],
                    "risks": risks,
                    "profiles": profiles,
                    "cf_reason":
                        "no_safe_reuse",
                    "cf_best_reuse": None,
                    "cf_reuse_query_after": None,
                    "cf_fresh_query_after":
                        fresh_query,
                    "cf_fresh_advantage": None,
                    "cf_capacity_cost":
                        self.capacity_cost,
                },
            )

        reuse_query = cf[
            "best_reuse_query_after"
        ]

        fresh_advantage = (
            reuse_query
            - fresh_query
        )

        fresh_score = (
            fresh_query
            + self.capacity_cost
        )

        reuse_score = reuse_query

        # Predeclared pilot rule:
        # lower predicted query loss wins.
        if fresh_score < reuse_score:

            new_name = self.spawn()

            return (
                new_name,
                {
                    "decision": "spawn",
                    "best_risk":
                        cf["best_reuse_harm"],
                    "best_gain": None,
                    "best_lcb":
                        cf["best_reuse_lcb"],
                    "best_ucb":
                        profiles[
                            best_reuse
                        ]["harm_ucb"],
                    "risks": risks,
                    "profiles": profiles,
                    "cf_reason":
                        "fresh_lower_query_loss",
                    "cf_best_reuse":
                        best_reuse,
                    "cf_reuse_query_after":
                        reuse_query,
                    "cf_fresh_query_after":
                        fresh_query,
                    "cf_fresh_advantage":
                        fresh_advantage,
                    "cf_capacity_cost":
                        self.capacity_cost,
                },
            )

        # Existing safe capacity predicts better
        # support->query generalization.
        self.activate(
            best_reuse
        )

        return (
            best_reuse,
            {
                "decision": "reuse",
                "best_risk":
                    cf["best_reuse_harm"],
                "best_gain":
                    cf[
                        "best_reuse_query_gain"
                    ],
                "best_lcb":
                    cf["best_reuse_lcb"],
                "best_ucb":
                    profiles[
                        best_reuse
                    ]["harm_ucb"],
                "risks": risks,
                "profiles": profiles,
                "cf_reason":
                    "reuse_lower_query_loss",
                "cf_best_reuse":
                    best_reuse,
                "cf_reuse_query_after":
                    reuse_query,
                "cf_fresh_query_after":
                    fresh_query,
                "cf_fresh_advantage":
                    fresh_advantage,
                "cf_capacity_cost":
                    self.capacity_cost,
            },
        )
