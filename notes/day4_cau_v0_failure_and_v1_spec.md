# Day 4 — CAU-v0 Failure Diagnosis and CAU-v1 Amendment

Date: 2026-10-04

Status:
PREDECLARED AFTER THE FIRST CAU-v0 AMAZON DEVELOPMENT FAILURE
AND BEFORE ANY CAU-v1 IMPLEMENTATION OR RESULTS.

This is a development-only method revision.

No confirmation seed or official final test result has been observed.

# 1. CAU-v0 failure

CAU-v0 was frozen before its first live Amazon run.

Observed Amazon seed-2026 behavior:

- 80 stream batches
- 33 DEFER actions
- 41.25% overall defer fraction
- B1 updates: 2 / 16
- B1 longest defer streak: 11 batches
- two permanent A2 spawns
- final adapter count: 3

The same-label Amazon regime was predeclared as a negative control
for unnecessary expansion.

Therefore CAU-v0 FAILED its structural development criterion.

This failure is retained and not relabeled as success.

# 2. Failure mechanism

The full-batch retention guard was NOT the dominant cause.

Observed full-batch candidate guard evaluations:

- total: 51
- safe: 51
- unsafe: 0

Therefore the live failure was primarily caused by the policy rule:

    no positive one-step reuse utility
        ->
    DEFER
        ->
    discard the supervised batch

This caused undertraining.

The resulting learner state diverged substantially from the healthy
V3 development trajectory.

Later action-utility estimates were therefore computed from a new
closed-loop state distribution.

The two A2 spawns occurred only after this divergence.

# 3. Methodological conclusion

A local prospective action-utility estimate is state-dependent:

    U(a | S_t)

Action utility measured on the V3 trajectory does not guarantee the
same action utility after a live controller changes the state
trajectory through repeated DEFER actions.

CAU-v0 incorrectly coupled:

1. capacity allocation
2. whether supervised learning occurs at all

These must be separated.

# 4. CAU-v1 principle

Working name:

CAU-v1 — learning-continuous capacity allocation

CAU-v1 uses action utility to decide WHERE learning should occur
and whether NEW capacity is warranted.

It does not normally use a nonpositive one-step utility estimate as
a reason to discard supervision.

No new numerical threshold is introduced.

# 5. Existing-adapter candidate set

For every mature existing adapter j:

1. compute the already-frozen cross-fitted action utility
2. require the already-frozen cross-fold retention-feasibility rule
3. apply the already-frozen exact full-batch retention guard

IMPORTANT CHANGE FROM CAU-v0:

A reuse candidate is NOT required to have:

    U_reuse_j > 0

in order to receive the real update.

Among all existing adapters satisfying both retention guards,
choose:

    argmax_j U_reuse_j

using the already-frozen tie-breaking rule:

1. higher system utility
2. lower worst-fold harm LCB
3. lower mean harm
4. lexicographically lower adapter name

The selected existing action may have negative one-step utility.

This is intentional.

# 6. Why nonpositive reuse may still train

The action-utility estimator is a one-step held-out estimate.

A one-step negative estimate does not establish that continued
supervised adaptation has negative long-horizon value.

Ordinary continual learning can require a sequence of updates before
held-out loss improves.

Therefore CAU-v1 does not interpret:

    U_reuse <= 0

as sufficient evidence to discard a labeled incoming batch.

Absolute positivity remains meaningful for NEW capacity because
permanent expansion is a structural intervention that requires
additional evidence.

# 7. Fresh-capacity evidence

The frozen fresh-positive definition is unchanged.

If a feasible existing reuse candidate exists:

    fresh_positive =
        U_fresh > 0
        AND
        U_fresh > U_best_reuse

If no cross-fold-feasible existing reuse candidate exists:

    fresh_positive =
        U_fresh > 0

No epsilon or magnitude threshold is added.

# 8. First fresh-positive window

A first fresh-positive window does NOT spawn.

Set:

    pending_fresh = True

Then:

If at least one existing adapter survives both retention guards:

    train the highest-utility safe existing adapter

even if its one-step utility is <= 0.

Otherwise:

    DEFER

# 9. Confirmed fresh action

If:

    pending_fresh == True

AND the current eligible window is fresh-positive:

    SPAWN

The new adapter receives the real full-batch update.

Then:

    pending_fresh = False

Fresh confirmation therefore remains a capacity-allocation gate.

# 10. Ordinary non-fresh window

If the current window is not fresh-positive:

    pending_fresh = False

If one or more existing adapters survive both retention guards:

    train the highest-utility safe existing adapter

regardless of utility sign.

If no existing adapter survives both retention guards:

    DEFER

# 11. Meaning of DEFER in CAU-v1

DEFER is now an EXCEPTIONAL safety/capacity state.

It is used only when:

- no existing adapter is retention-feasible for the update

AND

- fresh capacity is not yet confirmed

or when action-utility evaluation is unavailable.

DEFER still means:

- no optimizer update
- no replay-memory addition
- no update-counter increment
- no capacity creation

The main change is that negative one-step reuse utility alone no
longer triggers DEFER.

# 12. Warmup

Existing warmup semantics remain unchanged.

A spawned adapter receives normal warmup updates until mature.

Warmup breaks pending fresh confirmation.

# 13. Full-batch guard

The Day-4 full-batch retention amendment remains unchanged.

CAU-v1 applies the full-batch guard to cross-fold-feasible existing
candidates regardless of the sign of their action utility.

The full-batch guard remains feasibility-only.

It does NOT rank candidates.

# 14. What remains unchanged

CAU-v1 does NOT change:

- action-utility equations
- status-quo/no-update diagnostic baseline
- cross-fit folds
- query-count weighting
- harm threshold
- confidence z
- two-window fresh confirmation
- optimizer semantics
- LoRA configuration
- replay size
- warmup size
- fresh adapter initialization
- segment/task blindness
- evaluation sets

# 15. Development prediction

Amazon seed 2026:

CAU-v1 should restore learning continuity relative to CAU-v0.

Desired qualitative behavior:

- substantially fewer DEFER actions than CAU-v0
- no repeated supervision starvation
- no unnecessary same-label capacity fragmentation
- no harmful V3-style B2 expansion when fresh utility is negative

This is NOT a numerical pass threshold.

BANKING77 seed 2026:

Only if Amazon no longer exhibits structural failure, CAU-v1 will
be tested on BANKING.

Expected qualitative behavior:

- B1/C1 sustained fresh evidence can still trigger specialization
- recurrence should reuse existing capacity
- ordinary learning should continue between allocation events

# 16. Failure discipline

No thresholds will be tuned from the CAU-v1 Amazon result.

If CAU-v1 still exhibits major Amazon fragmentation or starvation,
record the result as another failure before any further revision.

Only one conceptual change is introduced in CAU-v1:

    separate capacity allocation from the decision to consume
    supervised training data.

# 17. Scientific interpretation

CAU-v0 demonstrated that a locally sensible no-update baseline can
be unsuitable as the default live action in continual adaptation.

The revised hypothesis is:

    prospective action utility is useful for deciding capacity
    allocation, but ordinary supervised learning should continue
    through retention-feasible existing capacity unless expansion
    is justified.

This distinction is part of the scientific result and not hidden
implementation behavior.
