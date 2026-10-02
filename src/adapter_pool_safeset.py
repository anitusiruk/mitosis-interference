import copy

import torch

from signal_scan import (
    encode,
    trainable_params,
)

from src.adapter_pool import AdapterPool

from experiments.day2_predictor_scan_rngsafe import (
    capture_rng_state,
    restore_rng_state,
)


class SafeSetAdapterPool(AdapterPool):

    def profile(
        self,
        name,
        texts,
        labels,
    ):
        """
        One optimizer-faithful counterfactual update.

        Returns:

        harm:
            historical protected-memory loss increase

        gain:
            incoming-batch loss reduction

        Neither the model, optimizer nor RNG state is
        permanently changed.
        """

        state = self.states[name]

        if len(state.memory.items) < self.memory_probe:
            raise RuntimeError(
                f"{name} lacks protected memory"
            )

        self.activate(name)

        mem_texts, mem_labels = state.memory.sample(
            self.memory_probe
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

            self.model.eval()

            with torch.no_grad():

                cur_before = self.model(
                    **cur_x,
                    labels=cur_y,
                ).loss.item()

                mem_before = self.model(
                    **mem_x,
                    labels=mem_y,
                ).loss.item()

            # Exact real-training update.
            self.model.train()

            state.optimizer.zero_grad(
                set_to_none=True
            )

            loss = self.model(
                **cur_x,
                labels=cur_y,
            ).loss

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                params,
                1.0,
            )

            state.optimizer.step()

            self.model.eval()

            with torch.no_grad():

                cur_after = self.model(
                    **cur_x,
                    labels=cur_y,
                ).loss.item()

                mem_after = self.model(
                    **mem_x,
                    labels=mem_y,
                ).loss.item()

            return {
                "harm":
                    mem_after - mem_before,

                "gain":
                    cur_before - cur_after,

                "cur_before": cur_before,
                "cur_after": cur_after,

                "mem_before": mem_before,
                "mem_after": mem_after,
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
        # Warm-up rule inherited conceptually from V1.
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

        # SAFETY IS A CONSTRAINT.
        safe = [
            name
            for name, p in profiles.items()
            if p["harm"] <= self.threshold
        ]

        risks = {
            name: p["harm"]
            for name, p in profiles.items()
        }

        if safe:
            # PLASTICITY IS THE OBJECTIVE.
            best_name = max(
                safe,
                key=lambda n: (
                    profiles[n]["gain"],
                    -profiles[n]["cur_after"],
                ),
            )

            self.activate(best_name)

            return (
                best_name,
                {
                    "decision": "reuse",
                    "best_risk":
                        profiles[best_name]["harm"],
                    "best_gain":
                        profiles[best_name]["gain"],
                    "risks": risks,
                    "profiles": profiles,
                },
            )

        # No existing adapter is prospectively safe.
        new_name = self.spawn()

        return (
            new_name,
            {
                "decision": "spawn",
                "best_risk":
                    min(risks.values()),
                "best_gain": None,
                "risks": risks,
                "profiles": profiles,
            },
        )
