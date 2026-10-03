# Day 2 Live Counterfactual Allocation Pilot

Seed: 2026
Stream: balanced A1 -> B1 -> A2 -> C1 -> B2

Live policy:
- support/query counterfactual scoring
- protected-harm feasibility for reuse
- fresh action instantiated exactly as a real new PEFT adapter
- capacity_cost = 0.0
- no task/segment ID provided to controller

Routing:

A1 -> default
B1 -> adapter_1
A2 -> default
C1 -> adapter_2
B2 -> adapter_1

Spawns:
- step 17, B1: fresh_lower_query_loss
  fresh advantage = +0.47827
- step 49, C1: fresh_lower_query_loss
  fresh advantage = +0.56034

Final adapter count: 3

Held-out global accuracy:

After A1:
- default A = 0.2749

After B1:
- adapter_1 B = 0.1226
- default A = 0.2749

After A2:
- default A = 0.2234
- adapter_1 B = 0.1226

After C1:
- adapter_2 C = 0.2637
- default A = 0.2234
- adapter_1 B = 0.1226

After B2:
- adapter_1 B = 0.3290
- adapter_2 C = 0.2637
- default A = 0.2234

Interpretation:
The live action-level counterfactual produced specialized capacity for
novel B and C segments, reused the A adapter on A recurrence, and reused
the B adapter on B recurrence.

This is a single-seed mechanistic pilot, not a robustness claim.

No capacity penalty was tuned.
