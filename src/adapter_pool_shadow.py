import copy
import math

import torch
import torch.nn.functional as F

from experiments.signal_scan import (
    encode,
    trainable_params,
)

from experiments.day2_predictor_scan_rngsafe import (
    capture_rng_state,
    restore_rng_state,
)

from src.adapter_pool_confidence import (
    ConfidenceAdapterPool,
)


class ShadowAdapterPool(ConfidenceAdapterPool):
    """
    V3 controller plus strictly observational support/query
    counterfactual scoring.

    Shadow scores NEVER determine real routing.
    """

    def shadow_reuse(
        self,
        name,
        support_texts,
        support_labels,
        query_texts,
        query_labels,
        restore_name,
    ):
        state = self.states[name]

        if len(state.memory.items) < self.memory_probe:
            raise RuntimeError(
                f"{name} lacks protected memory"
            )

        # Critical: Reservoir owns a private random.Random.
        memory_rng_state = (
            state.memory.rng.getstate()
        )

        rng_state = capture_rng_state()
        was_training = self.model.training

        self.activate(name)

        mem_texts, mem_labels = (
            state.memory.sample(
                self.memory_probe
            )
        )

        params = trainable_params(
            self.model
        )

        param_backup = [
            p.detach().clone()
            for p in params
        ]

        optimizer_backup = copy.deepcopy(
            state.optimizer.state_dict()
        )

        try:
            support_x = encode(
                self.tok,
                support_texts,
                self.device,
            )

            support_y = torch.tensor(
                support_labels,
                dtype=torch.long,
                device=self.device,
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

            mem_x = encode(
                self.tok,
                mem_texts,
                self.device,
            )

            mem_y = torch.tensor(
                mem_labels,
                dtype=torch.long,
                device=self.device,
            )

            # Before prospective update.
            self.model.eval()

            with torch.no_grad():
                query_before = float(
                    F.cross_entropy(
                        self.model(
                            **query_x
                        ).logits,
                        query_y,
                    ).item()
                )

                mem_before = self._loss_vector(
                    mem_x,
                    mem_y,
                )

            # Exact real optimizer semantics:
            # one AdamW update on SUPPORT.
            self.model.train()

            state.optimizer.zero_grad(
                set_to_none=True
            )

            support_loss = self.model(
                **support_x,
                labels=support_y,
            ).loss

            support_loss.backward()

            torch.nn.utils.clip_grad_norm_(
                params,
                1.0,
            )

            state.optimizer.step()

            # Evaluate generalization on QUERY and
            # backward damage on protected memory.
            self.model.eval()

            with torch.no_grad():
                query_after = float(
                    F.cross_entropy(
                        self.model(
                            **query_x
                        ).logits,
                        query_y,
                    ).item()
                )

                mem_after = self._loss_vector(
                    mem_x,
                    mem_y,
                )

            delta = (
                mem_after
                - mem_before
            )

            harm = float(
                delta.mean().item()
            )

            if delta.numel() > 1:
                harm_se = float(
                    delta.std(
                        unbiased=True
                    ).item()
                    / math.sqrt(
                        delta.numel()
                    )
                )
            else:
                harm_se = 0.0

            harm_lcb = (
                harm
                - self.confidence_z
                * harm_se
            )

            harm_ucb = (
                harm
                + self.confidence_z
                * harm_se
            )

            return {
                "query_before": query_before,
                "query_after": query_after,
                "query_gain":
                    query_before - query_after,
                "support_loss":
                    float(support_loss.detach().item()),
                "harm": harm,
                "harm_se": harm_se,
                "harm_lcb": harm_lcb,
                "harm_ucb": harm_ucb,
            }

        finally:
            with torch.no_grad():
                for p, old in zip(
                    params,
                    param_backup,
                ):
                    p.copy_(old)

            state.optimizer.load_state_dict(
                optimizer_backup
            )

            state.optimizer.zero_grad(
                set_to_none=True
            )

            # Restore private reservoir RNG.
            state.memory.rng.setstate(
                memory_rng_state
            )

            # Restore global RNG.
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

    def shadow_fresh(
        self,
        support_texts,
        support_labels,
        query_texts,
        query_labels,
        restore_name,
    ):
        temp_name = "__shadow_fresh__"

        if temp_name in self.model.peft_config:
            raise RuntimeError(
                "Shadow fresh adapter already exists"
            )

        rng_state = capture_rng_state()
        was_training = self.model.training

        optimizer = None

        try:
            # Direct PEFT add: does NOT mutate pool.states,
            # next_id, warmup_name, or reservoirs.
            self.model.add_adapter(
                adapter_name=temp_name,
                peft_config=self.cfg,
            )

            self.activate(
                temp_name
            )

            # Same optimizer construction as real spawn().
            optimizer = self._new_optimizer()

            params = trainable_params(
                self.model
            )

            support_x = encode(
                self.tok,
                support_texts,
                self.device,
            )

            support_y = torch.tensor(
                support_labels,
                dtype=torch.long,
                device=self.device,
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
                query_before = float(
                    F.cross_entropy(
                        self.model(
                            **query_x
                        ).logits,
                        query_y,
                    ).item()
                )

            self.model.train()

            optimizer.zero_grad(
                set_to_none=True
            )

            support_loss = self.model(
                **support_x,
                labels=support_y,
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
                        self.model(
                            **query_x
                        ).logits,
                        query_y,
                    ).item()
                )

            return {
                "query_before": query_before,
                "query_after": query_after,
                "query_gain":
                    query_before - query_after,
                "support_loss":
                    float(support_loss.detach().item()),
            }

        finally:
            if optimizer is not None:
                optimizer.zero_grad(
                    set_to_none=True
                )

            # Semantics audit showed this is reversible.
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
        Observational only.

        Deterministically splits current batch:
        even indices -> support
        odd indices  -> query.
        """

        n = len(texts)

        if n < 2:
            return {
                "status": "too_small",
            }

        # During true warmup V3 is not yet making an
        # allocation decision, so do not shadow-score.
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

        if (
            not support_idx
            or not query_idx
        ):
            return {
                "status": "too_small",
            }

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
            if (
                len(state.memory.items)
                >= self.memory_probe
            )
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
