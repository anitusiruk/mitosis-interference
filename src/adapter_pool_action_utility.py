import torch
import torch.nn.functional as F

from src.adapter_pool import (
    capture_rng_state,
    restore_rng_state,
    encode,
)

from src.adapter_pool_crossfit_shadow import (
    CrossFitShadowAdapterPool,
)


class ActionUtilityShadowPool(
    CrossFitShadowAdapterPool
):
    """
    Strictly observational common-baseline action evaluator.

    Candidate system actions:
        - DEFER: leave real active adapter unchanged
        - REUSE(j): switch to mature adapter j and apply
          its exact prospective AdamW support update
        - FRESH: instantiate temporary fresh capacity and
          apply its exact prospective AdamW support update

    No method in this class alters the real routing decision.
    """

    def _statusquo_query_loss(
        self,
        query_texts,
        query_labels,
        restore_name,
    ):
        """
        Query loss of the REAL current active adapter with
        no prospective update.

        This is the common utility baseline.
        """

        rng_state = capture_rng_state()
        was_training = self.model.training

        try:
            self.activate(
                restore_name
            )

            query_x = encode(
                self.tok,
                query_texts,
                self.device,
            )

            query_y = torch.tensor(
                query_labels,
                dtype=torch.long,
                device=self.device,
            )

            self.model.eval()

            with torch.no_grad():
                loss = float(
                    F.cross_entropy(
                        self.model(
                            **query_x
                        ).logits,
                        query_y,
                    ).item()
                )

            return loss

        finally:
            restore_rng_state(
                rng_state
            )

            self.activate(
                restore_name
            )

            if was_training:
                self.model.train()
            else:
                self.model.eval()

    def _fold_action_utility(
        self,
        support_texts,
        support_labels,
        query_texts,
        query_labels,
        restore_name,
    ):
        """
        Score one explicit support->query fold.

        All prospective actions use the existing proven
        shadow transaction methods.
        """

        if (
            not support_texts
            or not query_texts
        ):
            return {
                "status": "too_small",
            }

        mature = [
            name
            for name, state
            in self.states.items()
            if (
                len(state.memory.items)
                >= self.memory_probe
            )
        ]

        if not mature:
            return {
                "status": "no_mature",
            }

        statusquo_loss = (
            self._statusquo_query_loss(
                query_texts=query_texts,
                query_labels=query_labels,
                restore_name=restore_name,
            )
        )

        reuse_profiles = {}

        for name in mature:
            raw = self.shadow_reuse(
                name=name,
                support_texts=support_texts,
                support_labels=support_labels,
                query_texts=query_texts,
                query_labels=query_labels,
                restore_name=restore_name,
            )

            utility = (
                statusquo_loss
                - raw["query_after"]
            )

            local_trainability = (
                raw["query_before"]
                - raw["query_after"]
            )

            reuse_profiles[name] = {
                **raw,

                "system_utility":
                    utility,

                "local_trainability":
                    local_trainability,

                "feasible":
                    raw["harm_lcb"]
                    <= self.threshold,
            }

        fresh_raw = self.shadow_fresh(
            support_texts=support_texts,
            support_labels=support_labels,
            query_texts=query_texts,
            query_labels=query_labels,
            restore_name=restore_name,
        )

        fresh_utility = (
            statusquo_loss
            - fresh_raw["query_after"]
        )

        fresh_trainability = (
            fresh_raw["query_before"]
            - fresh_raw["query_after"]
        )

        return {
            "status": "ok",

            "support_n":
                len(support_texts),

            "query_n":
                len(query_texts),

            "statusquo_loss":
                statusquo_loss,

            "reuse_profiles":
                reuse_profiles,

            "fresh": {
                **fresh_raw,

                "system_utility":
                    fresh_utility,

                "local_trainability":
                    fresh_trainability,
            },
        }

    @staticmethod
    def _weighted(
        value_a,
        n_a,
        value_b,
        n_b,
    ):
        total = n_a + n_b

        if total <= 0:
            raise RuntimeError(
                "Invalid cross-fit query count"
            )

        return (
            n_a * value_a
            + n_b * value_b
        ) / total

    def crossfit_action_utility(
        self,
        texts,
        labels,
        restore_name,
    ):
        """
        Two-fold common-baseline action utility.

        Fold A:
            even -> support
            odd  -> query

        Fold B:
            odd  -> support
            even -> query

        This explicit construction handles odd batch sizes
        correctly: every example appears exactly once as query.
        """

        n = len(texts)

        if n < 2:
            return {
                "status": "too_small",
            }

        # Match V3 warmup semantics.
        if self.warmup_name is not None:
            warm = self.states[
                self.warmup_name
            ]

            if (
                len(warm.memory.items)
                < self.memory_probe
            ):
                return {
                    "status": "warmup",
                }

        even_idx = list(
            range(0, n, 2)
        )

        odd_idx = list(
            range(1, n, 2)
        )

        if (
            not even_idx
            or not odd_idx
        ):
            return {
                "status": "too_small",
            }

        fold_a = self._fold_action_utility(
            support_texts=[
                texts[i]
                for i in even_idx
            ],
            support_labels=[
                labels[i]
                for i in even_idx
            ],
            query_texts=[
                texts[i]
                for i in odd_idx
            ],
            query_labels=[
                labels[i]
                for i in odd_idx
            ],
            restore_name=restore_name,
        )

        fold_b = self._fold_action_utility(
            support_texts=[
                texts[i]
                for i in odd_idx
            ],
            support_labels=[
                labels[i]
                for i in odd_idx
            ],
            query_texts=[
                texts[i]
                for i in even_idx
            ],
            query_labels=[
                labels[i]
                for i in even_idx
            ],
            restore_name=restore_name,
        )

        if (
            fold_a.get("status") != "ok"
            or fold_b.get("status") != "ok"
        ):
            return {
                "status": "unavailable",

                "fold_a_status":
                    fold_a.get("status"),

                "fold_b_status":
                    fold_b.get("status"),
            }

        names_a = set(
            fold_a[
                "reuse_profiles"
            ]
        )

        names_b = set(
            fold_b[
                "reuse_profiles"
            ]
        )

        if names_a != names_b:
            raise RuntimeError(
                "Cross-fit mature candidate sets differ"
            )

        q_a = fold_a[
            "query_n"
        ]

        q_b = fold_b[
            "query_n"
        ]

        statusquo_loss = self._weighted(
            fold_a[
                "statusquo_loss"
            ],
            q_a,
            fold_b[
                "statusquo_loss"
            ],
            q_b,
        )

        reuse_profiles = {}

        for name in sorted(
            names_a
        ):
            a = fold_a[
                "reuse_profiles"
            ][name]

            b = fold_b[
                "reuse_profiles"
            ][name]

            utility = self._weighted(
                a[
                    "system_utility"
                ],
                q_a,
                b[
                    "system_utility"
                ],
                q_b,
            )

            query_before = self._weighted(
                a["query_before"],
                q_a,
                b["query_before"],
                q_b,
            )

            query_after = self._weighted(
                a["query_after"],
                q_a,
                b["query_after"],
                q_b,
            )

            trainability = self._weighted(
                a[
                    "local_trainability"
                ],
                q_a,
                b[
                    "local_trainability"
                ],
                q_b,
            )

            # Protected-memory quantities are not
            # query-set statistics, so use equal fold
            # weighting for descriptive summaries.
            harm_mean = (
                a["harm"]
                + b["harm"]
            ) / 2.0

            harm_se_mean = (
                a["harm_se"]
                + b["harm_se"]
            ) / 2.0

            harm_lcb_max = max(
                a["harm_lcb"],
                b["harm_lcb"],
            )

            harm_ucb_max = max(
                a["harm_ucb"],
                b["harm_ucb"],
            )

            feasible_both = (
                a["harm_lcb"]
                <= self.threshold
                and
                b["harm_lcb"]
                <= self.threshold
            )

            reuse_profiles[name] = {
                "system_utility":
                    utility,

                "query_before":
                    query_before,

                "query_after":
                    query_after,

                "local_trainability":
                    trainability,

                "feasible_both":
                    feasible_both,

                "harm_mean":
                    harm_mean,

                "harm_se_mean":
                    harm_se_mean,

                "harm_lcb_max":
                    harm_lcb_max,

                "harm_ucb_max":
                    harm_ucb_max,

                "fold_a_harm":
                    a["harm"],

                "fold_b_harm":
                    b["harm"],

                "fold_a_lcb":
                    a["harm_lcb"],

                "fold_b_lcb":
                    b["harm_lcb"],

                "fold_a_utility":
                    a[
                        "system_utility"
                    ],

                "fold_b_utility":
                    b[
                        "system_utility"
                    ],

                "fold_a_query_after":
                    a["query_after"],

                "fold_b_query_after":
                    b["query_after"],
            }

        feasible = [
            name
            for name, profile
            in reuse_profiles.items()
            if profile[
                "feasible_both"
            ]
        ]

        if feasible:
            best_reuse = max(
                feasible,
                key=lambda name: (
                    reuse_profiles[name][
                        "system_utility"
                    ],
                    -reuse_profiles[name][
                        "harm_lcb_max"
                    ],
                    -reuse_profiles[name][
                        "harm_mean"
                    ],
                    name,
                ),
            )

            best_reuse_utility = (
                reuse_profiles[
                    best_reuse
                ][
                    "system_utility"
                ]
            )

            best_reuse_after = (
                reuse_profiles[
                    best_reuse
                ][
                    "query_after"
                ]
            )

        else:
            best_reuse = None
            best_reuse_utility = None
            best_reuse_after = None

        fresh_a = fold_a[
            "fresh"
        ]

        fresh_b = fold_b[
            "fresh"
        ]

        fresh_utility = self._weighted(
            fresh_a[
                "system_utility"
            ],
            q_a,
            fresh_b[
                "system_utility"
            ],
            q_b,
        )

        fresh_query_before = (
            self._weighted(
                fresh_a[
                    "query_before"
                ],
                q_a,
                fresh_b[
                    "query_before"
                ],
                q_b,
            )
        )

        fresh_query_after = (
            self._weighted(
                fresh_a[
                    "query_after"
                ],
                q_a,
                fresh_b[
                    "query_after"
                ],
                q_b,
            )
        )

        fresh_trainability = (
            self._weighted(
                fresh_a[
                    "local_trainability"
                ],
                q_a,
                fresh_b[
                    "local_trainability"
                ],
                q_b,
            )
        )

        if best_reuse is None:
            fresh_advantage = None

            fresh_positive = (
                fresh_utility > 0.0
            )

        else:
            fresh_advantage = (
                fresh_utility
                - best_reuse_utility
            )

            fresh_positive = (
                fresh_utility > 0.0
                and
                fresh_utility
                > best_reuse_utility
            )

        return {
            "status": "ok",

            "batch_n":
                n,

            "fold_a_support_n":
                fold_a[
                    "support_n"
                ],

            "fold_a_query_n":
                q_a,

            "fold_b_support_n":
                fold_b[
                    "support_n"
                ],

            "fold_b_query_n":
                q_b,

            "statusquo_loss":
                statusquo_loss,

            # DEFER is the common reference.
            "defer_utility":
                0.0,

            "best_reuse":
                best_reuse,

            "best_reuse_utility":
                best_reuse_utility,

            "best_reuse_query_after":
                best_reuse_after,

            "fresh_utility":
                fresh_utility,

            "fresh_query_before":
                fresh_query_before,

            "fresh_query_after":
                fresh_query_after,

            "fresh_local_trainability":
                fresh_trainability,

            "fresh_advantage":
                fresh_advantage,

            "fresh_positive":
                bool(
                    fresh_positive
                ),

            "fold_a_fresh_utility":
                fresh_a[
                    "system_utility"
                ],

            "fold_b_fresh_utility":
                fresh_b[
                    "system_utility"
                ],

            "reuse_profiles":
                reuse_profiles,
        }
