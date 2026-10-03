# Day 2 Shadow Fresh-vs-Reuse Result

The support/query counterfactual scorer was run observationally on the
balanced A1 -> B1 -> A2 -> C1 -> B2 recurrence stream, seed 2026.

## Non-invasiveness

The shadow run reproduced the original balanced V3 trajectory exactly:

- routing rows: 80 / 80
- adapters identical: true
- decisions identical: true
- training loss max abs diff: 0
- best_risk max abs diff: 0
- best_lcb max abs diff: 0
- best_ucb max abs diff: 0
- best_gain max abs diff: 0

Therefore the shadow counterfactual measurements did not perturb real
training.

## Fresh advantage

fresh_advantage =
    best feasible reuse query-after loss
    - fresh query-after loss

Positive values favor fresh isolated capacity.

A1:
- mean = -0.56901
- fresh better = 0 / 12

B1:
- mean = +0.06068
- fresh better = 9 / 16
- fresh wins strongly at segment entry
- reuse becomes better later as the existing adapter adapts

A2 recurrence:
- mean = -1.39975
- fresh better = 0 / 16

C1:
- mean = +1.39338
- fresh better = 16 / 16

B2 recurrence:
- mean = -0.55989 on comparable feasible-reuse events
- fresh better = 0
- one V3 event had no feasible reuse and therefore no direct advantage value

Boundary behavior:
- B1 step 17: fresh advantage +0.47827
- A2 step 33: fresh advantage -1.22122
- C1 step 49: fresh advantage +2.30854
- B2 step 65: fresh advantage -0.43001

## Interpretation

The action-level support/query signal distinguishes new-distribution
plasticity needs from recurrence without using segment IDs.

This is a single-seed mechanistic result, not yet a final performance
claim.

No capacity penalty or fresh-advantage threshold was tuned on this run.
