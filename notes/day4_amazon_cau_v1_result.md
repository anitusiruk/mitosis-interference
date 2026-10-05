# Day 4 — Amazon CAU-v1 Development Result

Date: 2026-10-04

Status:
DEVELOPMENT RESULT — SEED 2026

This is not confirmation-seed evidence and is not a final test result.

## Context

CAU-v0 failed its first live Amazon development pilot because it
discarded supervision whenever no existing adapter had positive
one-step action utility.

Observed CAU-v0:

- 80 batches
- 33 DEFER
- 47 learning updates
- 2 permanent spawns
- 3 final adapters
- B1 update fraction = 2 / 16
- longest B1 DEFER streak = 11

The full-batch retention guard was not the primary source of
starvation:

- 51 candidate guard evaluations
- 51 safe
- 0 unsafe

CAU-v1 was therefore predeclared with one conceptual revision:

    separate capacity allocation from learning continuity

Retention-feasible existing adapters are allowed to receive the
real supervised update regardless of the sign of their one-step
action utility.

Fresh-capacity positivity and two-window confirmation remain
unchanged.

## Amazon CAU-v1 result

Observed CAU-v1:

- 80 batches
- 79 learning updates
- 1 DEFER
- 75 REUSE
- 4 warmup
- 0 permanent spawns
- final adapter count = 1

Actions by segment:

A1:
- 12 reuse
- 4 warmup
- 0 defer
- 0 spawn

B1:
- 16 reuse
- 0 defer
- 0 spawn

A2:
- 16 reuse
- 0 defer
- 0 spawn

C1:
- 15 reuse
- 1 defer
- 0 spawn

B2:
- 16 reuse
- 0 defer
- 0 spawn

## Full-batch guard behavior

CAU-v1 candidate guard evaluations:

- total = 75
- safe = 75

Negative or zero one-step utility candidates evaluated:

- 27

Negative or zero utility candidates that were retention-safe:

- 27

This directly supports the CAU-v1 correction.

CAU-v0 would have treated these nonpositive one-step utilities as a
reason not to learn.

CAU-v1 correctly separated:

    one-step capacity-allocation evidence

from:

    whether ordinary supervised adaptation should continue

## Fresh-capacity behavior

The isolated Amazon fresh-positive windows remained isolated.

Examples:

- step 7: fresh-positive
- step 11: fresh-positive
- step 14: fresh-positive
- step 50: fresh-positive

No persistent confirmation produced a permanent Amazon expansion.

At the previous V3 problem region around B2:

- step 69: fresh utility strongly negative
- step 70: fresh utility strongly negative
- step 71: fresh utility strongly negative
- step 80: fresh utility strongly negative

CAU-v1 did not create capacity.

## Held-out behavior

Mean default-adapter held-out accuracy:

Checkpoint   V3       CAU-v0    CAU-v1
A1           0.73438   0.50260   0.73438
B1           0.82812   0.50000   0.82812
A2           0.84635   0.50000   0.84635
C1           0.85417   0.50521   0.83594
B2           0.84635   0.76562   0.85417

Interpretation:

CAU-v1 restored the healthy shared-learning trajectory destroyed by
CAU-v0.

It avoided unnecessary same-label adapter fragmentation.

The result does NOT establish superiority over V3.

The important result is structural:

    CAU-v1 preserved ordinary shared learning while refusing
    unsupported permanent expansion.

## Development conclusion

Amazon CAU-v1 clears the qualitative negative-control development
gate.

Specifically:

1. no supervision starvation
2. no repeated DEFER deadlock
3. no unnecessary permanent expansion
4. same-label recurrence remained on shared capacity
5. held-out learning recovered to approximately the healthy V3
   trajectory

Therefore the next predeclared development test is BANKING77.

BANKING must determine whether the same frozen CAU-v1 controller can
also allocate new capacity when persistent fresh evidence exists.

No CAU-v1 rule or threshold is changed before BANKING.
