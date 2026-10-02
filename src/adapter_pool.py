from dataclasses import dataclass

import torch

from signal_scan import (
    Reservoir,
    encode,
    trainable_params,
)

from experiments.day2_predictor_scan_rngsafe import (
    capture_rng_state,
    restore_rng_state,
    exact_adamw_interference,
)


@dataclass
class AdapterState:
    name: str
    optimizer: object
    memory: object
    updates: int = 0


class AdapterPool:

    def __init__(
        self,
        model,
        tokenizer,
        lora_config,
        device,
        lr=2e-4,
        memory_size=512,
        memory_probe=64,
        threshold=0.0,
        seed=2026,
    ):
        self.model = model
        self.tok = tokenizer
        self.cfg = lora_config
        self.device = device

        self.lr = lr
        self.memory_size = memory_size
        self.memory_probe = memory_probe
        self.threshold = threshold
        self.seed = seed

        self.states = {}
        self.next_id = 1

        # get_peft_model() creates "default".
        self.model.set_adapter("default")

        self.states["default"] = AdapterState(
            name="default",
            optimizer=self._new_optimizer(),
            memory=Reservoir(
                memory_size,
                seed + 1000,
            ),
        )

        # Do not spawn until initial adapter has enough
        # protected history to evaluate the frozen I1 signal.
        self.warmup_name = "default"


    def _new_optimizer(self):
        params = trainable_params(self.model)

        return torch.optim.AdamW(
            params,
            lr=self.lr,
        )


    def activate(self, name):
        self.model.set_adapter(name)


    def spawn(self):
        name = f"adapter_{self.next_id}"
        self.next_id += 1

        self.model.add_adapter(
            adapter_name=name,
            peft_config=self.cfg,
        )

        self.activate(name)

        state = AdapterState(
            name=name,
            optimizer=self._new_optimizer(),
            memory=Reservoir(
                self.memory_size,
                self.seed + 1000 + self.next_id,
            ),
        )

        self.states[name] = state

        # Newly created capacity gets enough observations
        # to establish its protected reservoir before another
        # expansion decision can be made.
        self.warmup_name = name

        return name


    def score(self, name, texts, labels):

        state = self.states[name]

        if len(state.memory.items) < self.memory_probe:
            raise RuntimeError(
                f"{name} does not have enough memory "
                f"({len(state.memory.items)} < {self.memory_probe})"
            )

        self.activate(name)

        mem_texts, mem_labels = state.memory.sample(
            self.memory_probe
        )

        # Make the counterfactual completely non-invasive.
        rng_state = capture_rng_state()

        try:
            result = exact_adamw_interference(
                model=self.model,
                optimizer=state.optimizer,
                tok=self.tok,
                cur_texts=texts,
                cur_labels=labels,
                mem_texts=mem_texts,
                mem_labels=mem_labels,
                device=self.device,
                horizons=(1,),
            )
        finally:
            restore_rng_state(rng_state)

        return float(result["adamw_I1"])


    def select(self, texts, labels):
        """
        Controller:

        1. Warm up newly created capacity.
        2. Score every mature adapter with frozen AdamW-I1.
        3. Choose minimum-risk adapter.
        4. Reuse if min risk <= 0.
        5. Otherwise spawn.
        """

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
                        "risks": {},
                    },
                )

            self.warmup_name = None

        risks = {}

        for name, state in self.states.items():

            if (
                len(state.memory.items)
                >= self.memory_probe
            ):
                risks[name] = self.score(
                    name,
                    texts,
                    labels,
                )

        if not risks:
            raise RuntimeError(
                "No mature adapter available."
            )

        best_name = min(
            risks,
            key=risks.get,
        )

        best_risk = risks[best_name]

        if best_risk <= self.threshold:

            self.activate(best_name)

            return (
                best_name,
                {
                    "decision": "reuse",
                    "best_risk": best_risk,
                    "risks": risks,
                },
            )

        new_name = self.spawn()

        return (
            new_name,
            {
                "decision": "spawn",
                "best_risk": best_risk,
                "risks": risks,
            },
        )


    def train_step(
        self,
        name,
        texts,
        labels,
    ):
        self.activate(name)

        state = self.states[name]

        self.model.train()

        x = encode(
            self.tok,
            texts,
            self.device,
        )

        y = torch.tensor(
            labels,
            dtype=torch.long,
            device=self.device,
        )

        state.optimizer.zero_grad(
            set_to_none=True
        )

        loss = self.model(
            **x,
            labels=y,
        ).loss

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            trainable_params(self.model),
            1.0,
        )

        state.optimizer.step()

        for text, label in zip(
            texts,
            labels,
        ):
            state.memory.add(
                text,
                int(label),
            )

        state.updates += 1

        return float(
            loss.detach().item()
        )


    def summary(self):
        return {
            name: {
                "updates": state.updates,
                "memory":
                    len(state.memory.items),
            }
            for name, state
            in self.states.items()
        }
