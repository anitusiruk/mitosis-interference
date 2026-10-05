from src.adapter_pool_cau_v0 import (
    CAUV0AdapterPool,
)


class CAUV1AdapterPool(
    CAUV0AdapterPool
):
    """
    CAU-v1: learning-continuous capacity allocation.

    Relative to CAU-v0:

    - fresh-capacity evidence is unchanged
    - confirmation is unchanged
    - cross-fold retention feasibility is unchanged
    - full-batch retention feasibility is unchanged
    - DEFER remains literal no-learning

    The only conceptual policy change is:

        retention-feasible existing adapters may receive
        the real supervised update even when their
        one-step system utility is <= 0.

    Thus action utility controls capacity allocation
    without normally discarding supervision.
    """

    _REASON_MAP = {
        "positive_guarded_reuse":
            "safe_existing_reuse",

        "pending_fresh_guarded_reuse":
            "pending_fresh_safe_existing_reuse",

        "no_positive_guarded_reuse":
            "no_retention_feasible_reuse",

        "pending_fresh_no_guarded_reuse":
            "pending_fresh_no_retention_feasible_reuse",
    }

    def _full_batch_guarded_reuse(
        self,
        texts,
        labels,
        restore_name,
        utility,
    ):
        """
        CAU-v1 existing-capacity feasibility layer.

        Unlike CAU-v0, a cross-fold-feasible existing
        adapter is prospectively full-batch checked
        REGARDLESS of the sign of its one-step utility.

        Full-batch gain remains diagnostic only.

        Ranking among surviving candidates is the frozen
        cross-fitted ranking:

            1. higher system utility
            2. lower worst-fold harm LCB
            3. lower mean harm
            4. lexicographically lower adapter name
        """

        reuse_profiles = utility.get(
            "reuse_profiles",
            {},
        )

        guard_profiles = {}
        surviving = []

        for name in sorted(
            reuse_profiles
        ):
            cross = reuse_profiles[
                name
            ]

            cross_utility = cross.get(
                "system_utility"
            )

            cross_feasible = bool(
                cross.get(
                    "feasible_both",
                    False,
                )
            )

            # CAU-v1 change:
            #
            # DO NOT require:
            #
            #     cross_utility > 0
            #
            # before allowing ordinary supervised
            # adaptation through existing capacity.
            if (
                not cross_feasible
                or cross_utility is None
            ):
                continue

            state = self.states[
                name
            ]

            memory_rng_state = (
                state.memory.rng
                .getstate()
            )

            try:
                full = self.profile(
                    name,
                    texts,
                    labels,
                )

            finally:
                # profile() already restores:
                #
                # - parameters
                # - optimizer state
                # - global RNG
                # - train/eval mode
                #
                # Explicitly restore the Reservoir's
                # private RNG and the real active adapter.
                state.memory.rng.setstate(
                    memory_rng_state
                )

                self.activate(
                    restore_name
                )

            full_safe = (
                full[
                    "harm_lcb"
                ]
                <= self.threshold
            )

            guard_profiles[
                name
            ] = {
                "crossfit_utility":
                    cross_utility,

                "crossfit_feasible":
                    cross_feasible,

                "crossfit_utility_positive":
                    bool(
                        cross_utility > 0.0
                    ),

                "full_batch_safe":
                    bool(
                        full_safe
                    ),

                "full_batch_harm":
                    full[
                        "harm"
                    ],

                "full_batch_harm_se":
                    full[
                        "harm_se"
                    ],

                "full_batch_harm_lcb":
                    full[
                        "harm_lcb"
                    ],

                "full_batch_harm_ucb":
                    full[
                        "harm_ucb"
                    ],

                "full_batch_gain":
                    full[
                        "gain"
                    ],

                "full_batch_cur_before":
                    full[
                        "cur_before"
                    ],

                "full_batch_cur_after":
                    full[
                        "cur_after"
                    ],
            }

            if full_safe:
                surviving.append(
                    name
                )

        if not surviving:
            self.activate(
                restore_name
            )

            return (
                None,
                guard_profiles,
            )

        best_name = min(
            surviving,
            key=lambda name: (
                -reuse_profiles[
                    name
                ][
                    "system_utility"
                ],

                reuse_profiles[
                    name
                ][
                    "harm_lcb_max"
                ],

                reuse_profiles[
                    name
                ][
                    "harm_mean"
                ],

                name,
            ),
        )

        self.activate(
            restore_name
        )

        return (
            best_name,
            guard_profiles,
        )

    def select_action(
        self,
        texts,
        labels,
        restore_name,
    ):
        """
        Use the already-audited CAU-v0 state machine with
        the CAU-v1 candidate feasibility semantics above.

        Only reason labels are normalized so logs do not
        incorrectly describe a negative-utility but safe
        reuse as "positive".
        """

        (
            name,
            info,
        ) = super().select_action(
            texts=texts,
            labels=labels,
            restore_name=restore_name,
        )

        info = dict(
            info
        )

        reason = info.get(
            "reason"
        )

        if reason in self._REASON_MAP:
            info[
                "reason"
            ] = self._REASON_MAP[
                reason
            ]

        info[
            "policy_version"
        ] = "cau_v1"

        return (
            name,
            info,
        )
