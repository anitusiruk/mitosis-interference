import copy
import math

import torch
import torch.nn.functional as F

from experiments.signal_scan import (
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

        # Fixed 95% normal-approximation confidence gate.
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

            # BEFORE virtual update.
            self.model.eval()

            with torch.no_grad():
                cur_before_vec = self._loss_vector(
                    cur_x,
                    cur_y,
                )

                mem_before_vec = self._loss_vector(
                    mem_x,
                    mem_y,
                )

            cur_before = float(
                cur_before_vec.mean().item()
            )

            # Exact optimizer-faithful virtual update.
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

            # AFTER virtual update.
            self.model.eval()

            with torch.no_grad():
                cur_after_vec = self._loss_vector(
                    cur_x,
                    cur_y,
                )

                mem_after_vec = self._loss_vector(
                    mem_x,
                    mem_y,
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
            # Restore parameters.
            with torch.no_grad():
                for p, old in zip(
                    params,
                    param_backup,
                ):
                    p.copy_(old)

            # Restore this adapter's optimizer.
            state.optimizer.load_state_dict(
                optimizer_backup
            )

            state.optimizer.zero_grad(
                set_to_none=True
            )

            # Restore all RNG state so diagnostics
            # cannot perturb real training.
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
        # Newly created adapter must first accumulate
        # enough protected history for scoring.
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
                    },
                )

            self.warmup_name = None

        profiles = {}

        for name, state in self.states.items():

            if (
                len(state.memory.items)
                >= self.memory_probe
            ):
                profiles[name] = self.profile(
                    name,
                    texts,
                    labels,
                )

        if not profiles:
            raise RuntimeError(
                "No mature adapter available."
            )

        # Always expose risks for logging.
        risks = {
            name: profile["harm"]
            for name, profile
            in profiles.items()
        }

        # Adapter is feasible unless we have
        # positive-confidence evidence that
        # expected harm exceeds the threshold.
        feasible = [
            name
            for name, profile
            in profiles.items()
            if (
                profile["harm_lcb"]
                <= self.threshold
            )
        ]

        if feasible:
            # All candidates see the SAME incoming
            # batch, so post-update current loss is
            # directly comparable across adapters.
            best_name = min(
                feasible,
                key=lambda name: (
                    profiles[name]["cur_after"],
                    profiles[name]["harm"],
                ),
            )

            profile = profiles[
                best_name
            ]

            self.activate(
                best_name
            )

            return (
                best_name,
                {
                    "decision": "reuse",
                    "best_risk":
                        profile["harm"],
                    "best_gain":
                        profile["gain"],
                    "best_lcb":
                        profile["harm_lcb"],
                    "best_ucb":
                        profile["harm_ucb"],
                    "risks": risks,
                    "profiles": profiles,
                },
            )

        # No existing adapter is confidently safe.
        least_bad = min(
            profiles,
            key=lambda name:
                profiles[name]["harm_lcb"],
        )

        profile = profiles[
            least_bad
        ]

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
            },
        )
