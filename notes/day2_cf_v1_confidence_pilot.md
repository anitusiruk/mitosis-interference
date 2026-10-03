# Day 2 CF-v1 Confidence-Gated Pilot

Seed: 2026

CF-v1 combines:
- inherited-head fresh capacity
- optimizer-faithful support/query action scoring
- protected-harm feasibility for reuse
- paired per-example query-loss uncertainty
- fixed confidence_z = 1.96
- spawn only when fresh-advantage LCB > 0

Routing:
- A1 -> default
- B1 -> adapter_1
- A2 -> default
- C1 -> adapter_2
- B2 -> adapter_1

Spawns:
- B1 step 17
  mean fresh advantage = 0.18098
  SE = 0.01948
  LCB = 0.14280

- C1 step 49
  mean fresh advantage = 0.07092
  SE = 0.01540
  LCB = 0.04073

Final adapters: 3
Recurrence spawns: 0

Target accuracy:
- A1 A = 0.2749
- B1 B = 0.1516
- A2 A = 0.2234
- C1 C = 0.2271
- B2 B = 0.2774

Important result:
The uncertainty gate suppressed the tiny positive fresh advantages that
caused redundant spawning in the inherited-head zero-cost ablation.

This is a single-seed pilot. No z value or other threshold was tuned
after observing this result.
