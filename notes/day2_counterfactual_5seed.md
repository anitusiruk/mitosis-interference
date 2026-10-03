# Day 2 Counterfactual Allocator — Five-Seed Result

Seeds:
2026, 1337, 17, 31415, 4242

Policy:
- optimizer-faithful support/query action comparison
- protected-harm constraint on reuse
- fresh capacity is an explicit candidate action
- capacity_cost = 0.0
- no task/segment ID supplied to controller

## Routing robustness

Across all 5 seeds:

- A1 dominant adapter = default
- B1 dominant adapter = adapter_1
- A2 dominant adapter = default
- C1 dominant adapter = adapter_2
- B2 dominant adapter = adapter_1
- A recurrence reuse = 5/5
- B recurrence reuse = 5/5
- exactly 2 spawns per run
- zero recurrence spawns
- exactly 3 final adapters

## Mean held-out target accuracy

CF:
- A after A1: 0.1814
- A after A2: 0.3251
- B after B1: 0.1348
- B after B2: 0.3355
- C after C1: 0.2103

V3:
- A after A1: 0.1814
- A after A2: 0.4048
- B after B1: 0.0000
- B after B2: 0.1297
- C after C1: 0.0000

Paired CF - V3:
- A after A1: +0.0000
- A after A2: -0.0797
- B after B1: +0.1348
- B after B2: +0.2058
- C after C1: +0.2103

## Important interpretation

CF improves its own mean A accuracy from 0.1814 after A1
to 0.3251 after A2. Therefore the lower A2 accuracy relative
to V3 is not simply catastrophic forgetting.

V3 trains default on B and C as well, so some of its higher
A performance may come from beneficial cross-concept transfer.

The five-seed result establishes robust mechanistic behavior,
not yet final end-to-end superiority.

Fresh capacity currently consists of:
- fresh LoRA
- fresh pre-classifier
- fresh classifier

Therefore a head-initialization/isolation ablation is required.
