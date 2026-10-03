from src.adapter_pool_shadow import (
    ShadowAdapterPool,
)


class CrossFitShadowAdapterPool(
    ShadowAdapterPool
):
    """
    Observational two-fold support/query scoring.

    Fold A:
        even -> support
        odd  -> query

    Fold B:
        odd  -> support
        even -> query

    Both calls are individually transactional and
    restore model, optimizer, RNG, reservoir RNG,
    and active adapter state.
    """

    def crossfit_compare(
        self,
        texts,
        labels,
        restore_name,
    ):
        if len(texts) < 2:
            return {
                "status": "too_small",
            }

        fold_a = self.shadow_compare(
            texts=texts,
            labels=labels,
            restore_name=restore_name,
        )

        # Swap each adjacent pair so the parent's
        # even/odd split is reversed.
        order = []

        i = 0

        while i + 1 < len(texts):
            order.extend([
                i + 1,
                i,
            ])
            i += 2

        if i < len(texts):
            order.append(i)

        swapped_texts = [
            texts[j]
            for j in order
        ]

        swapped_labels = [
            labels[j]
            for j in order
        ]

        fold_b = self.shadow_compare(
            texts=swapped_texts,
            labels=swapped_labels,
            restore_name=restore_name,
        )

        if (
            fold_a.get("status")
            != "ok"
            or fold_b.get("status")
            != "ok"
        ):
            return {
                "status": "unavailable",
                "fold_a_status":
                    fold_a.get("status"),
                "fold_b_status":
                    fold_b.get("status"),
            }

        advantages = [
            x
            for x in [
                fold_a.get(
                    "fresh_advantage"
                ),
                fold_b.get(
                    "fresh_advantage"
                ),
            ]
            if x is not None
        ]

        fresh_gains = [
            fold_a[
                "fresh_query_gain"
            ],
            fold_b[
                "fresh_query_gain"
            ],
        ]

        reuse_gains = [
            x
            for x in [
                fold_a.get(
                    "best_reuse_query_gain"
                ),
                fold_b.get(
                    "best_reuse_query_gain"
                ),
            ]
            if x is not None
        ]

        return {
            "status": "ok",

            "fold_a_best_reuse":
                fold_a.get(
                    "best_reuse"
                ),

            "fold_b_best_reuse":
                fold_b.get(
                    "best_reuse"
                ),

            "fold_a_advantage":
                fold_a.get(
                    "fresh_advantage"
                ),

            "fold_b_advantage":
                fold_b.get(
                    "fresh_advantage"
                ),

            "crossfit_advantage":
                None
                if not advantages
                else sum(advantages)
                / len(advantages),

            "fold_a_fresh_gain":
                fold_a[
                    "fresh_query_gain"
                ],

            "fold_b_fresh_gain":
                fold_b[
                    "fresh_query_gain"
                ],

            "crossfit_fresh_gain":
                sum(fresh_gains)
                / len(fresh_gains),

            "crossfit_reuse_gain":
                None
                if not reuse_gains
                else sum(reuse_gains)
                / len(reuse_gains),

            "fold_a_reuse_after":
                fold_a.get(
                    "best_reuse_query_after"
                ),

            "fold_b_reuse_after":
                fold_b.get(
                    "best_reuse_query_after"
                ),

            "fold_a_fresh_after":
                fold_a[
                    "fresh_query_after"
                ],

            "fold_b_fresh_after":
                fold_b[
                    "fresh_query_after"
                ],
        }
