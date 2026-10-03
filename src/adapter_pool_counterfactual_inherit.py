import torch

from src.adapter_pool_counterfactual import (
    CounterfactualAdapterPool,
)


class InheritedHeadCounterfactualPool(
    CounterfactualAdapterPool
):
    """
    Counterfactual allocator ablation.

    Fresh adapters receive fresh LoRA parameters,
    but classifier/pre-classifier state is copied
    from the best feasible reuse candidate rather
    than reset to original-module initialization.
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

        self._fresh_head_source = None


    def _saved_param(
        self,
        module_name,
        adapter_name,
        field,
    ):
        matches = []

        for name, param in (
            self.model.named_parameters()
        ):
            parts = name.split(".")

            if (
                len(parts) >= 4
                and parts[-4] == module_name
                and parts[-3] == "modules_to_save"
                and parts[-2] == adapter_name
                and parts[-1] == field
            ):
                matches.append(
                    (name, param)
                )

        if len(matches) != 1:
            raise RuntimeError(
                f"{module_name}/"
                f"{adapter_name}/"
                f"{field}: "
                f"expected 1 parameter, "
                f"got {len(matches)}"
            )

        return matches[0][1]


    def _copy_head(
        self,
        source,
        target,
    ):
        with torch.no_grad():

            for module_name in [
                "pre_classifier",
                "classifier",
            ]:
                for field in [
                    "weight",
                    "bias",
                ]:
                    src = self._saved_param(
                        module_name,
                        source,
                        field,
                    )

                    dst = self._saved_param(
                        module_name,
                        target,
                        field,
                    )

                    dst.copy_(src)


    def shadow_fresh(
        self,
        support_texts,
        support_labels,
        query_texts,
        query_labels,
        restore_name,
    ):
        """
        Same temporary action as parent, except
        the fresh head is inherited from the
        selected reuse reference.
        """

        temp_name = "__shadow_fresh__"

        if temp_name in self.model.peft_config:
            raise RuntimeError(
                "Shadow fresh adapter already exists"
            )

        from experiments.signal_scan import (
            encode,
            trainable_params,
        )

        from experiments.day2_predictor_scan_rngsafe import (
            capture_rng_state,
            restore_rng_state,
        )

        import torch.nn.functional as F

        rng_state = capture_rng_state()
        was_training = self.model.training
        optimizer = None

        source = self._fresh_head_source

        if source is None:
            source = restore_name

        try:
            self.model.add_adapter(
                adapter_name=temp_name,
                peft_config=self.cfg,
            )

            self.activate(temp_name)

            self._copy_head(
                source,
                temp_name,
            )

            optimizer = self._new_optimizer()

            params = trainable_params(
                self.model
            )

            sx = encode(
                self.tok,
                support_texts,
                self.device,
            )

            sy = torch.tensor(
                support_labels,
                dtype=torch.long,
                device=self.device,
            )

            qx = encode(
                self.tok,
                query_texts,
                self.device,
            )

            qy = torch.tensor(
                query_labels,
                dtype=torch.long,
                device=self.device,
            )

            self.model.eval()

            with torch.no_grad():
                query_before = float(
                    F.cross_entropy(
                        self.model(**qx).logits,
                        qy,
                    ).item()
                )

            self.model.train()

            optimizer.zero_grad(
                set_to_none=True
            )

            support_loss = self.model(
                **sx,
                labels=sy,
            ).loss

            support_loss.backward()

            torch.nn.utils.clip_grad_norm_(
                params,
                1.0,
            )

            optimizer.step()

            self.model.eval()

            with torch.no_grad():
                query_after = float(
                    F.cross_entropy(
                        self.model(**qx).logits,
                        qy,
                    ).item()
                )

            return {
                "query_before": query_before,
                "query_after": query_after,
                "query_gain":
                    query_before - query_after,
                "support_loss":
                    float(
                        support_loss
                        .detach()
                        .item()
                    ),
            }

        finally:
            if optimizer is not None:
                optimizer.zero_grad(
                    set_to_none=True
                )

            if temp_name in self.model.peft_config:
                self.activate(
                    restore_name
                )

                self.model.delete_adapter(
                    temp_name
                )

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


    def shadow_compare(
        self,
        texts,
        labels,
        restore_name,
    ):
        """
        Parent logic reproduced only so the fresh
        action can inherit from best feasible reuse.
        """

        n = len(texts)

        if n < 2:
            return {
                "status": "too_small",
            }

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

        support_idx = list(
            range(0, n, 2)
        )

        query_idx = list(
            range(1, n, 2)
        )

        support_texts = [
            texts[i]
            for i in support_idx
        ]

        support_labels = [
            labels[i]
            for i in support_idx
        ]

        query_texts = [
            texts[i]
            for i in query_idx
        ]

        query_labels = [
            labels[i]
            for i in query_idx
        ]

        mature = [
            name
            for name, state
            in self.states.items()
            if len(
                state.memory.items
            ) >= self.memory_probe
        ]

        if not mature:
            return {
                "status": "no_mature",
            }

        reuse_profiles = {}

        for name in mature:
            reuse_profiles[name] = (
                self.shadow_reuse(
                    name=name,
                    support_texts=support_texts,
                    support_labels=support_labels,
                    query_texts=query_texts,
                    query_labels=query_labels,
                    restore_name=restore_name,
                )
            )

        feasible = [
            name
            for name in mature
            if (
                reuse_profiles[name][
                    "harm_lcb"
                ]
                <= self.threshold
            )
        ]

        if feasible:
            best_reuse = min(
                feasible,
                key=lambda name: (
                    reuse_profiles[name][
                        "query_after"
                    ],
                    reuse_profiles[name][
                        "harm"
                    ],
                ),
            )
        else:
            best_reuse = None

        # If no reuse action is safe, use the
        # least harmful existing adapter solely
        # as the head-initialization reference.
        if best_reuse is not None:
            source = best_reuse
        else:
            source = min(
                mature,
                key=lambda name:
                    reuse_profiles[name][
                        "harm_lcb"
                    ],
            )

        self._fresh_head_source = source

        fresh = self.shadow_fresh(
            support_texts=support_texts,
            support_labels=support_labels,
            query_texts=query_texts,
            query_labels=query_labels,
            restore_name=restore_name,
        )

        if best_reuse is not None:
            r = reuse_profiles[
                best_reuse
            ]

            fresh_advantage = (
                r["query_after"]
                - fresh["query_after"]
            )
        else:
            r = None
            fresh_advantage = None

        return {
            "status": "ok",
            "support_n":
                len(support_idx),
            "query_n":
                len(query_idx),
            "best_reuse":
                best_reuse,
            "best_reuse_query_before":
                None if r is None
                else r["query_before"],
            "best_reuse_query_after":
                None if r is None
                else r["query_after"],
            "best_reuse_query_gain":
                None if r is None
                else r["query_gain"],
            "best_reuse_harm":
                None if r is None
                else r["harm"],
            "best_reuse_lcb":
                None if r is None
                else r["harm_lcb"],
            "fresh_query_before":
                fresh["query_before"],
            "fresh_query_after":
                fresh["query_after"],
            "fresh_query_gain":
                fresh["query_gain"],
            "fresh_advantage":
                fresh_advantage,
            "reuse_profiles":
                reuse_profiles,
        }


    def spawn(self):
        source = self._fresh_head_source

        name = super().spawn()

        if source is not None:
            self._copy_head(
                source,
                name,
            )

        self._fresh_head_source = None

        return name
