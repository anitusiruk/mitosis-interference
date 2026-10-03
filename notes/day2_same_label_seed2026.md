# Same-Label Domain Recurrence — Seed 2026

Dataset:
Amazon Reviews Multi, English.

Domains:
- A = home
- B = apparel
- C = drugstore

Shared labels in every domain:
- 0 = negative (1-2 stars)
- 1 = positive (4-5 stars)

Schedule:
A1 -> B1 -> A2 -> C1 -> B2

## V3

V3 mostly reused default and learned all three domains jointly.

After C1, default validation accuracy:
- A: 0.8750
- B: 0.8594
- C: 0.8281

At B2 step 71 V3 spawned:
- harm = +0.01907
- LCB = +0.00151

The spawned adapter collapsed to one-class prediction:
- A/B/C accuracy = 0.5000
- negative accuracy = 0
- positive accuracy = 1

The original default remained strong after B2:
- A: 0.8594
- B: 0.8750
- C: 0.8047

Therefore predicted backward harm alone did not imply that fresh
capacity was a useful learning action.

## CF-v0

CF-v0 over-expanded:

step 7 A1:
- fresh advantage +0.04965

step 11 A1:
- fresh advantage +0.00843

step 23 B1:
- fresh advantage +0.00105

Final adapter count: 4.

Most early fresh adapters were approximately chance-level on balanced
validation while the shared default later became strong across all
three domains.

Interpretation:
The single deterministic 8/8 support-query estimate is too noisy and
myopic in the same-label shared-transfer regime.

CF-v0 therefore does NOT currently generalize cleanly beyond the
BANKING77 disjoint-label recurrence experiment.

No margin, lambda, z, or spawn threshold will be tuned from this run.

Next diagnostic:
strictly observational two-fold support/query cross-fitting on the
unchanged V3 trajectory.
