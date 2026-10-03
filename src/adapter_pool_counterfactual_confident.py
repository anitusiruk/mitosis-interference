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

from src.adapter_pool_counterfactual_inherit import (
    InheritedHeadCounterfactualPool,
)


class ConfidentInheritedHeadPool(
    InheritedHeadCounterfactualPool
):
    """
    Inherited-head counterfactual allocator with
    paired uncertainty on fresh-vs-reuse query loss.

    Fresh is selected only when its query-loss
    advantage has positive lower confidence bound.

    Uses the already-fixed confidence_z.
    """

    def _split_support_query(
        self,
        texts,
        labels,
    ):
        support_idx = list(
            range(0, len(texts), 2)
        )

        query_idx = list(
            range(1, len(texts), 2)
        )

        return (
            [texts[i] for i in support_idx],
            [labels[i] for i in support_idx],
            [texts[i] for i in query_idx],
            [labels[i] for i in query_idx],
        )


    def _reuse_query_vector(
        self,
        name,
        support_texts,
        support_labels,
        query_texts,
        query_labels,
        restore_name,
    ):
        state = self.states[name]

        rng_state = capture_rng_state()
        was_training = self.model.training

        self.activate(name)

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

            self.model.train()

            state.optimizer.zero_grad(
                set_to_none=True
            )

            loss = self.model(
                **sx,
                labels=sy,
            ).loss

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                params,
                1.0,
            )

            state.optimizer.step()

            self.model.eval()

            with torch.no_grad():
                logits = self.model(
                    **qx
                ).logits

                vec = F.cross_entropy(
                    logits,
                    qy,
                    reduction="none",
                )

            return (
                vec.detach()
                .cpu()
                .double()
            )

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


    def _fresh_query_vector(
        self,
        source,
        support_texts,
        support_labels,
        query_texts,
        query_labels,
        restore_name,
    ):
        temp_name = (
            "__shadow_conf_fresh__"
        )

        if temp_name in self.model.peft_config:
            raise RuntimeError(
                "Temporary confidence adapter exists"
            )

        rng_state = capture_rng_state()
        was_training = self.model.training
        optimizer = None

        try:
            self.model.add_adapter(
                adapter_name=temp_name,
                peft_config=self.cfg,
            )

            self.activate(
                temp_name
            )

            # Inherited-head fresh action.
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

            self.model.train()

            optimizer.zero_grad(
                set_to_none=True
            )

            loss = self.model(
                **sx,
                labels=sy,
            ).loss

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                params,
                1.0,
            )

            optimizer.step()

            self.model.eval()

            with torch.no_grad():
                logits = self.model(
                    **qx
                ).logits

                vec = F.cross_entropy(
                    logits,
                    qy,
                    reduction="none",
                )

            return (
                vec.detach()
                .cpu()
                .double()
            )

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


    def _fresh_advantage_stats(
        self,
        best_reuse,
        source,
        texts,
        labels,
        restore_name,
    ):
        (
            support_texts,
            support_labels,
            query_texts,
            query_labels,
        ) = self._split_support_query(
            texts,
            labels,
        )

        reuse_vec = (
            self._reuse_query_vector(
                name=best_reuse,
                support_texts=support_texts,
                support_labels=support_labels,
                query_texts=query_texts,
                query_labels=query_labels,
                restore_name=restore_name,
            )
        )

        fresh_vec = (
            self._fresh_query_vector(
                source=source,
                support_texts=support_texts,
                support_labels=support_labels,
                query_texts=query_texts,
                query_labels=query_labels,
                restore_name=restore_name,
            )
        )

        # Positive delta means fresh has lower loss.
        delta = (
            reuse_vec
            - fresh_vec
        )

        mean = float(
            delta.mean().item()
        )

        if delta.numel() > 1:
            se = float(
                delta.std(
                    unbiased=True
                ).item()
                / math.sqrt(
                    delta.numel()
                )
            )
        else:
            se = 0.0

        lcb = (
            mean
            - self.confidence_z
            * se
        )

        ucb = (
            mean
            + self.confidence_z
            * se
        )

        return {
            "n": int(
                delta.numel()
            ),
            "mean": mean,
            "se": se,
            "lcb": lcb,
            "ucb": ucb,
        }


    def select(
        self,
        texts,
        labels,
    ):
        # Preserve existing warmup policy.
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
                        "cf_advantage_se": None,
                        "cf_advantage_lcb": None,
                        "cf_advantage_ucb": None,
                        "cf_query_n": None,
                        "cf_capacity_cost":
                            self.capacity_cost,
                    },
                )

            self.warmup_name = None

        restore_name = self.active_name

        if restore_name not in self.states:
            restore_name = "default"

        # Existing inherited-head support/query
        # counterfactual calculation.
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

        # No safe reuse action: expansion remains
        # mandatory exactly as before.
        if best_reuse is None:

            reference_name = min(
                profiles,
                key=lambda name:
                    profiles[name][
                        "harm_lcb"
                    ],
            )

            reference = profiles[
                reference_name
            ]

            new_name = self.spawn()

            return (
                new_name,
                {
                    "decision": "spawn",
                    "best_risk":
                        reference["harm"],
                    "best_gain": None,
                    "best_lcb":
                        reference["harm_lcb"],
                    "best_ucb":
                        reference["harm_ucb"],
                    "risks": risks,
                    "profiles": profiles,
                    "cf_reason":
                        "no_safe_reuse",
                    "cf_best_reuse": None,
                    "cf_reuse_query_after": None,
                    "cf_fresh_query_after":
                        cf[
                            "fresh_query_after"
                        ],
                    "cf_fresh_advantage": None,
                    "cf_advantage_se": None,
                    "cf_advantage_lcb": None,
                    "cf_advantage_ucb": None,
                    "cf_query_n": None,
                    "cf_capacity_cost":
                        self.capacity_cost,
                },
            )

        source = self._fresh_head_source

        if source is None:
            source = best_reuse

        stats = (
            self._fresh_advantage_stats(
                best_reuse=best_reuse,
                source=source,
                texts=texts,
                labels=labels,
                restore_name=restore_name,
            )
        )

        profile = profiles[
            best_reuse
        ]

        # Fresh must be confidently better,
        # not merely infinitesimally better.
        if stats["lcb"] > 0.0:

            new_name = self.spawn()

            return (
                new_name,
                {
                    "decision": "spawn",
                    "best_risk":
                        profile["harm"],
                    "best_gain": None,
                    "best_lcb":
                        profile["harm_lcb"],
                    "best_ucb":
                        profile["harm_ucb"],
                    "risks": risks,
                    "profiles": profiles,
                    "cf_reason":
                        "fresh_confidently_better",
                    "cf_best_reuse":
                        best_reuse,
                    "cf_reuse_query_after":
                        cf[
                            "best_reuse_query_after"
                        ],
                    "cf_fresh_query_after":
                        cf[
                            "fresh_query_after"
                        ],
                    "cf_fresh_advantage":
                        stats["mean"],
                    "cf_advantage_se":
                        stats["se"],
                    "cf_advantage_lcb":
                        stats["lcb"],
                    "cf_advantage_ucb":
                        stats["ucb"],
                    "cf_query_n":
                        stats["n"],
                    "cf_capacity_cost":
                        self.capacity_cost,
                },
            )

        # Insufficient evidence to pay for
        # additional capacity: reuse.
        self.activate(
            best_reuse
        )

        self._fresh_head_source = None

        return (
            best_reuse,
            {
                "decision": "reuse",
                "best_risk":
                    profile["harm"],
                "best_gain":
                    cf[
                        "best_reuse_query_gain"
                    ],
                "best_lcb":
                    profile["harm_lcb"],
                "best_ucb":
                    profile["harm_ucb"],
                "risks": risks,
                "profiles": profiles,
                "cf_reason":
                    "fresh_not_confidently_better",
                "cf_best_reuse":
                    best_reuse,
                "cf_reuse_query_after":
                    cf[
                        "best_reuse_query_after"
                    ],
                "cf_fresh_query_after":
                    cf[
                        "fresh_query_after"
                    ],
                "cf_fresh_advantage":
                    stats["mean"],
                "cf_advantage_se":
                    stats["se"],
                "cf_advantage_lcb":
                    stats["lcb"],
                "cf_advantage_ucb":
                    stats["ucb"],
                "cf_query_n":
                    stats["n"],
                "cf_capacity_cost":
                    self.capacity_cost,
            },
        )
