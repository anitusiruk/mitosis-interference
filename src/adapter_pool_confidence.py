import copy
import math

import torch
import torch.nn.functional as F

from signal_scan import (
    encode,
    trainable_params,
)

from src.adapter_pool import AdapterPool

from experiments.day2_predictor_scan_rngsafe import (
    capture_rng_state,
    restore_rng_state,
)


class ConfidenceAdapterPool(AdapterPool):

    def __init__(
        self,
        *args,
        confidence_z=1.96,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # Fixed BEFORE looking at this controller's result.
        # Two-sided 95% normal interval.
        self.confidence_z = confidence_z


    def _loss_vector(
        self,
        x,
        y,
    ):
        logits = self.model(
            **x
        ).logits

        return F.cross_entropy(
            logits,
            y,
            reduction="none",
        )


    def profile(
        self,
        name,
        texts,
        labels,
    ):
        state = self.states[name]

        if len(state.memory.items) < self.memory_probe:
            raise RuntimeError(
                f"{name} lacks protected memory"
            )

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

        was_training = self.model.training
        rng_state = capture_rng_state()

        try:
            cur_x = encode(
                self.tok,
                texts,
                self.device,
            )

            cur_y = torch.tensor(
                labels,
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

            # -------------------------
            # BEFORE virtual update
            # -------------------------

            self.model.eval()

            with torch.no_grad():

                cur_before_vec = (
                    self._loss_vector(
                        cur_x,
                        cur_y,
                    )
                )

                mem_before_vec = (
                    self._loss_vector(
                        mem_x,
                        mem_y,
                    )
                )

            cur_before = float(
                cur_before_vec.mean().item()
            )

            # -------------------------
            # Exact training update
            # -------------------------

            self.model.train()

            state.optimizer.zero_grad(
                set_to_none=True
            )

            train_loss = self.model(
                **cur_x,
                labels=cur_y,
            ).loss

            train_loss.backward()

            torch.nn.utils.clip_grad_norm_(
                params,
                1.0,
            )

            state.optimizer.step()

            # -------------------------
            # AFTER virtual update
            # -------------------------

            self.model.eval()

            with torch.no_grad():

                cur_after_vec = (
                    self._loss_vector(
                        cur_x,
                        cur_y,
                    )
                )

                mem_after_vec = (
                    self._loss_vector(
                        mem_x,
                        mem_y,
                    )
                )

            cur_after = float(
                cur_after_vec.mean().item()
            )

            delta = (
                mem_after_vec
                - mem_before_vec
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

            gain = (
                cur_before
                - cur_after
            )

            return {
                "harm": harm,
                "harm_se": harm_se,
                "harm_lcb": harm_lcb,
                "harm_ucb": harm_ucb,
                "gain": gain,
                "cur_before": cur_before,
                "cur_after": cur_after,
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

            restore_rng_state(
                rng_state
            )

            if was_training:
                self.model.train()
            else:
                self.model.eval()


    def select(
        self,
        texts,
        labels,
    ):
        # ---------------------------------
        # Warm up newly spawned capacity.
        # ---------------------------------

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
                        "profiles": {},
                    },
                )

            self.warmup_name = None

        # ---------------------------------
        # Counterfactual profile of every
        # mature adapter.
        # ---------------------------------

        profiles = {}

        for name, state in self.states.items():

            if (
                len(state.memory.items)
                >= self.memory_probe
            ):

                profiles[name] = (
                    self.profile(
                        name,
                        texts,
                        labels,
                    )
                )

        if not profiles:
            raise RuntimeError(
                "No mature adapter available."
            )

        # ---------------------------------
        # CONFIDENCE-GATED SAFETY SET
        #
        # Unsafe only if we have positive
        # evidence that expected protected
        # harm is > threshold.
        # ---------------------------------

        feasible = [
            name
            for name, p
            in profiles.items()
            if p["harm_lcb"]
            <= self.threshold
        ]

        if feasible:

            # Same current batch across all
            # adapters -> directly comparable.
            best_name = min(
                feasible,
                key=lambda n: (
                    profiles[n]["cur_after"],
                    profiles[n]["harm"],
                ),
            )

            p = profiles[best_name]

            self.activate(best_name)

            return (
                best_name,
                {
                    "decision": "reuse",
                    "best_risk":
                        p["harm"],
                    "best_gain":
                        p["gain"],
                    "best_lcb":
                        p["harm_lcb"],
                    "best_ucb":
                        p["harm_ucb"],
                    "profiles":
                        profiles,
                },
            )

        # ---------------------------------
        # No existing capacity is
        # confidently feasible.
        # ---------------------------------

        least_bad = min(
            profiles,
            key=lambda n:
                profiles[n]["harm_lcb"],
        )

        p = profiles[least_bad]

        new_name = self.spawn()

        return (
            new_name,
            {
                "decision": "spawn",
                "best_risk":
                    p["harm"],
                "best_gain": None,
                "best_lcb":
                    p["harm_lcb"],
                "best_ucb":
                    p["harm_ucb"],
                "profiles":
                    profiles,
            },
        )
