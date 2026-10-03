# Counterfactual Allocator Replication Plan

This plan was written AFTER inspecting the seed-2026 mechanistic pilot
but BEFORE running the four replication seeds below.

Replication seeds:
- 1337
- 17
- 31415
- 4242

For every seed, run:
1. unchanged balanced V3 confidence controller
2. zero-cost live counterfactual allocator

No hyperparameters will be changed between replication seeds.

Primary descriptive outcomes:

1. Recurrence consistency
   - dominant adapter A1 == dominant adapter A2
   - dominant adapter B1 == dominant adapter B2

2. Expansion behavior
   - spawn count by segment
   - final adapter count
   - recurrence-segment spawns on A2/B2

3. Specialization
   - held-out target-concept accuracy of the dominant adapter
   - A after A1/A2
   - B after B1/B2
   - C after C1

4. Comparison to V3
   - target-concept held-out accuracy
   - recurrence reuse
   - number/timing of spawns

5. Resource behavior
   - number of adapters
   - no capacity penalty is used in this replication suite

No success threshold will be tuned after seeing individual seeds.

The zero-cost allocator remains a mechanistic policy, not the final
resource-aware method.
