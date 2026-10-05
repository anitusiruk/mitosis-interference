from src.adapter_pool_action_utility import (
    ActionUtilityShadowPool,
)


class CAUV0AdapterPool(
    ActionUtilityShadowPool
):
    """
    Live Counterfactual Action Utility controller.

    Frozen actions:
        WARMUP
        REUSE
        SPAWN
        DEFER

    No task, domain, occurrence, or segment identity is used.
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

        self.pending_fresh = False

    def _full_batch_guarded_reuse(
        self,
        texts,
        labels,
        restore_name,
        utility,
    ):
        """
        Apply the predeclared full-batch protected-harm
        guard to every positive-utility cross-fold-feasible
        reuse candidate.

        Returns:
            best surviving reuse name or None
            guard diagnostics
        """

        reuse_profiles = (
            utility.get(
                "reuse_profiles",
                {},
            )
        )

        guard_profiles = {}
        surviving = []

        for name in sorted(
            reuse_profiles
        ):
            cross = (
                reuse_profiles[
                    name
                ]
            )

            cross_utility = (
                cross.get(
                    "system_utility"
                )
            )

            cross_feasible = bool(
                cross.get(
                    "feasible_both",
                    False,
                )
            )

            # Only provisional positive-utility,
            # cross-fold-feasible reuse candidates
            # receive the full-batch guard.
            if (
                not cross_feasible
                or cross_utility is None
                or not (
                    cross_utility > 0.0
                )
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
                # profile() restores model params,
                # optimizer and global RNG, but the
                # Reservoir owns its own random.Random.
                state.memory.rng.setstate(
                    memory_rng_state
                )

                # profile() activates the candidate.
                # Restore the true real active adapter.
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

        # Preserve the frozen cross-fit ranking.
        #
        # Full-batch profile is feasibility-only.
        # Frozen ranking:
        #   1. maximum cross-fitted system utility
        #   2. lower worst-fold harm LCB
        #   3. lower mean harm
        #   4. lexicographically LOWER adapter name
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
        Select the live action without applying the real
        training update.

        live_step() is the canonical public training path.
        """

        pending_before = bool(
            self.pending_fresh
        )

        # -------------------------------------------------
        # Existing warmup semantics.
        # -------------------------------------------------

        if self.warmup_name is not None:

            warm_name = (
                self.warmup_name
            )

            state = self.states[
                warm_name
            ]

            if (
                len(
                    state.memory.items
                )
                < self.memory_probe
            ):
                self.pending_fresh = False

                self.activate(
                    warm_name
                )

                return (
                    warm_name,
                    {
                        "decision":
                            "warmup",

                        "reason":
                            "existing_warmup",

                        "pending_before":
                            pending_before,

                        "pending_after":
                            False,

                        "utility_status":
                            "warmup",

                        "fresh_positive":
                            None,

                        "fresh_utility":
                            None,

                        "best_reuse":
                            None,

                        "best_reuse_utility":
                            None,

                        "guarded_best_reuse":
                            None,

                        "full_batch_guards":
                            {},
                    },
                )

            # Adapter has matured.
            self.warmup_name = None

        # -------------------------------------------------
        # Observational cross-fitted action utility.
        # -------------------------------------------------

        utility = (
            self.crossfit_action_utility(
                texts=texts,
                labels=labels,
                restore_name=restore_name,
            )
        )

        status = utility.get(
            "status"
        )

        if status != "ok":

            self.pending_fresh = False

            self.activate(
                restore_name
            )

            return (
                None,
                {
                    "decision":
                        "defer",

                    "reason":
                        "utility_unavailable",

                    "pending_before":
                        pending_before,

                    "pending_after":
                        False,

                    "utility_status":
                        status,

                    "fresh_positive":
                        None,

                    "fresh_utility":
                        None,

                    "best_reuse":
                        None,

                    "best_reuse_utility":
                        None,

                    "guarded_best_reuse":
                        None,

                    "full_batch_guards":
                        {},

                    "utility":
                        utility,
                },
            )

        fresh_positive = bool(
            utility.get(
                "fresh_positive",
                False,
            )
        )

        # -------------------------------------------------
        # Two consecutive fresh-positive windows:
        # permanent capacity creation has priority.
        # -------------------------------------------------

        if (
            pending_before
            and fresh_positive
        ):
            new_name = self.spawn()

            self.pending_fresh = False

            return (
                new_name,
                {
                    "decision":
                        "spawn",

                    "reason":
                        "confirmed_fresh",

                    "pending_before":
                        True,

                    "pending_after":
                        False,

                    "utility_status":
                        "ok",

                    "fresh_positive":
                        True,

                    "fresh_utility":
                        utility.get(
                            "fresh_utility"
                        ),

                    "fresh_advantage":
                        utility.get(
                            "fresh_advantage"
                        ),

                    "best_reuse":
                        utility.get(
                            "best_reuse"
                        ),

                    "best_reuse_utility":
                        utility.get(
                            "best_reuse_utility"
                        ),

                    "guarded_best_reuse":
                        None,

                    "full_batch_guards":
                        {},

                    "utility":
                        utility,
                },
            )

        # -------------------------------------------------
        # For all non-confirmed-fresh cases, determine
        # whether positive reuse survives the exact
        # full-batch protected-harm guard.
        # -------------------------------------------------

        (
            guarded_best,
            guard_profiles,
        ) = self._full_batch_guarded_reuse(
            texts=texts,
            labels=labels,
            restore_name=restore_name,
            utility=utility,
        )

        if fresh_positive:

            # First fresh-positive window:
            # evidence is pending but does not spawn.
            self.pending_fresh = True

            if guarded_best is not None:

                self.activate(
                    guarded_best
                )

                return (
                    guarded_best,
                    {
                        "decision":
                            "reuse",

                        "reason":
                            "pending_fresh_guarded_reuse",

                        "pending_before":
                            False,

                        "pending_after":
                            True,

                        "utility_status":
                            "ok",

                        "fresh_positive":
                            True,

                        "fresh_utility":
                            utility.get(
                                "fresh_utility"
                            ),

                        "fresh_advantage":
                            utility.get(
                                "fresh_advantage"
                            ),

                        "best_reuse":
                            utility.get(
                                "best_reuse"
                            ),

                        "best_reuse_utility":
                            utility.get(
                                "best_reuse_utility"
                            ),

                        "guarded_best_reuse":
                            guarded_best,

                        "full_batch_guards":
                            guard_profiles,

                        "utility":
                            utility,
                    },
                )

            self.activate(
                restore_name
            )

            return (
                None,
                {
                    "decision":
                        "defer",

                    "reason":
                        "pending_fresh_no_guarded_reuse",

                    "pending_before":
                        False,

                    "pending_after":
                        True,

                    "utility_status":
                        "ok",

                    "fresh_positive":
                        True,

                    "fresh_utility":
                        utility.get(
                            "fresh_utility"
                        ),

                    "fresh_advantage":
                        utility.get(
                            "fresh_advantage"
                        ),

                    "best_reuse":
                        utility.get(
                            "best_reuse"
                        ),

                    "best_reuse_utility":
                        utility.get(
                            "best_reuse_utility"
                        ),

                    "guarded_best_reuse":
                        None,

                    "full_batch_guards":
                        guard_profiles,

                    "utility":
                        utility,
                },
            )

        # -------------------------------------------------
        # No current fresh evidence.
        # -------------------------------------------------

        self.pending_fresh = False

        if guarded_best is not None:

            self.activate(
                guarded_best
            )

            return (
                guarded_best,
                {
                    "decision":
                        "reuse",

                    "reason":
                        "positive_guarded_reuse",

                    "pending_before":
                        pending_before,

                    "pending_after":
                        False,

                    "utility_status":
                        "ok",

                    "fresh_positive":
                        False,

                    "fresh_utility":
                        utility.get(
                            "fresh_utility"
                        ),

                    "fresh_advantage":
                        utility.get(
                            "fresh_advantage"
                        ),

                    "best_reuse":
                        utility.get(
                            "best_reuse"
                        ),

                    "best_reuse_utility":
                        utility.get(
                            "best_reuse_utility"
                        ),

                    "guarded_best_reuse":
                        guarded_best,

                    "full_batch_guards":
                        guard_profiles,

                    "utility":
                        utility,
                },
            )

        self.activate(
            restore_name
        )

        return (
            None,
            {
                "decision":
                    "defer",

                "reason":
                    "no_positive_guarded_reuse",

                "pending_before":
                    pending_before,

                "pending_after":
                    False,

                "utility_status":
                    "ok",

                "fresh_positive":
                    False,

                "fresh_utility":
                    utility.get(
                        "fresh_utility"
                    ),

                "fresh_advantage":
                    utility.get(
                        "fresh_advantage"
                    ),

                "best_reuse":
                    utility.get(
                        "best_reuse"
                    ),

                "best_reuse_utility":
                    utility.get(
                        "best_reuse_utility"
                    ),

                "guarded_best_reuse":
                    None,

                "full_batch_guards":
                    guard_profiles,

                "utility":
                    utility,
            },
        )

    def live_step(
        self,
        texts,
        labels,
        restore_name,
    ):
        """
        Canonical CAU-v0 real-training entry point.

        Returns:
            active_name_after_action
            info
            train_loss_or_None
        """

        (
            selected_name,
            info,
        ) = self.select_action(
            texts=texts,
            labels=labels,
            restore_name=restore_name,
        )

        decision = info[
            "decision"
        ]

        if decision == "defer":

            # Literal no-learning action.
            self.activate(
                restore_name
            )

            info[
                "num_adapters"
            ] = len(
                self.states
            )

            return (
                restore_name,
                info,
                None,
            )

        if selected_name is None:
            raise RuntimeError(
                "Non-defer action lacks adapter"
            )

        train_loss = self.train_step(
            selected_name,
            texts,
            labels,
        )

        info[
            "num_adapters"
        ] = len(
            self.states
        )

        return (
            selected_name,
            info,
            train_loss,
        )
