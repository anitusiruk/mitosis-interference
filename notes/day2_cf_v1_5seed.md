# CF-v1 Five-Seed Result

CF-v1:
- inherited-head fresh capacity
- paired support/query uncertainty gate
- spawn if fresh-advantage LCB > 0
- confidence_z = 1.96

Five-seed summary:

A recurrence reuse: 5/5
B recurrence reuse: 4/5

Spawns:
- [2, 3, 2, 2, 3]
- mean 2.4

Recurrence spawns:
- zero in all runs

Final adapters:
- [3, 4, 3, 3, 4]

Mean accuracy:
- A after A1: 0.1814
- A after A2: 0.3251
- B after B1: 0.1161
- B after B2: 0.2103
- C after C1: 0.2037

Compared with CF-v0:
- A after A2: +0.0000
- B after B1: -0.0187
- B after B2: -0.1252
- C after C1: -0.0066

Interpretation:

The uncertainty gate removed tiny redundant spawns in seed 2026,
but this did not generalize into a superior allocator across five
seeds.

CF-v1 still fragmented capacity in seeds 1337 and 4242 and broke
B recurrence in seed 1337.

This result does NOT isolate the effect of uncertainty gating because
CF-v1 differs from CF-v0 in both:
1. fresh-head initialization semantics
2. confidence-gated selection

Therefore CF-v0 remains the strongest mechanistic allocator so far,
while CF-v1 is retained as an ablation rather than the primary method.

No z or advantage threshold will be retuned from these results.
