# Day 3 Live Action-Utility Controller Specification

Date: 2026-10-04

Status:
PREDECLARED BEFORE LIVE CONTROLLER IMPLEMENTATION AND BEFORE
ANY LIVE ACTION-UTILITY RESULTS.

Working name:
Counterfactual Action Utility controller (CAU-v0)

This is a development method name only.

# 1. Candidate actions

At each eligible decision window:

1. REUSE existing adapter j
2. FRESH permanent adapter
3. DEFER / no parameter update

The controller receives:

- current texts
- current labels
- adapter memories
- optimizer/model state

It does NOT receive:

- task ID
- concept ID
- domain ID
- segment boundary

# 2. Utility estimator

Use the already frozen two-fold common-baseline action-utility
estimator.

For candidate action a:

U_a =
    L_statusquo
    - L_query_after_action_a

DEFER has:

U_defer = 0

Reuse candidates must satisfy the frozen cross-fold protected-harm
feasibility rule in BOTH support directions.

No new magnitude threshold is introduced.

# 3. Persistent fresh evidence

Maintain one controller state variable:

pending_fresh

Initial value:

False

A fresh-positive eligible window satisfies the already frozen rule:

If feasible reuse exists:

    U_fresh > 0
    AND
    U_fresh > U_best_reuse

If no feasible reuse exists:

    U_fresh > 0

Fresh capacity is permanently spawned only if:

1. the immediately previous eligible window was fresh-positive
2. the current eligible window is fresh-positive

Warmup or unavailable diagnostic windows break the pending sequence.

Segment/task boundaries are not used.

# 4. Action on first fresh-positive window

A single fresh-positive window does NOT spawn.

Set:

pending_fresh = True

Then:

If a feasible reuse candidate exists AND:

    U_best_reuse > 0

train that best reuse adapter on the real full batch.

Otherwise:

DEFER.

This means a first positive fresh signal does not force harmful
reuse while waiting for confirmation.

# 5. Confirmed fresh action

If:

pending_fresh == True

and the current eligible window is fresh-positive:

spawn one new adapter using the existing pool's exact `spawn()`
semantics.

Train the new adapter on the current full real batch.

Then:

pending_fresh = False

The current development implementation therefore uses the same
fresh PEFT semantics already audited:

- fresh LoRA
- fresh pre-classifier
- fresh classifier

The separate-head semantics are NOT claimed as the final
architecture.

# 6. Ordinary reuse action

If the current window is NOT fresh-positive:

pending_fresh = False

If a cross-fold-feasible reuse candidate exists AND:

    U_best_reuse > 0

activate and train that best reuse adapter on the current full batch.

Otherwise:

DEFER.

# 7. DEFER semantics

DEFER means:

- preserve the currently active real adapter
- perform no optimizer step
- do not add the current batch to any adapter replay reservoir
- do not increment any adapter update counter
- do not create capacity

The incoming batch may still be logged for experimental analysis.

DEFER is therefore a literal no-learning system action for that
window.

This choice is intentionally simple for the first live pilot.

No auxiliary pending-data buffer is introduced.

# 8. Warmup after spawn

Existing spawn warmup semantics are retained.

A newly spawned adapter is trained during its existing memory
warmup until it becomes mature.

Warmup windows:

- do not evaluate action utility
- break fresh confirmation
- do not contribute positive or negative evidence

No warmup duration is tuned.

# 9. Ties

Strict inequalities are used.

Fresh requires strictly positive utility.

Reuse requires strictly positive utility.

Exact zero utility selects DEFER.

No epsilon is introduced.

# 10. Development pilot

The first live pilot will use only already-inspected development
seed 2026.

This run is for mechanism debugging, not confirmation.

No new threshold may be tuned from it.

The primary qualitative expectations are:

Amazon:
- unnecessary permanent expansion should be strongly reduced
  relative to CF-v0/V3
- if expansion occurs, its held-out consequence must be examined
  rather than relabeled as success

BANKING77:
- sustained B1/C1 fresh evidence should translate into useful
  specialized capacity
- A2/B2 recurrence should favor existing capacity rather than
  additional fresh capacity

These expectations do NOT define final statistical acceptance
criteria.

# 11. Structural failure conditions

Stop and redesign rather than tune thresholds if:

1. the live controller repeatedly spawns in same-label Amazon
   without held-out benefit

2. the live controller fails to create useful capacity in the
   BANKING isolation-needed periods

3. the method fragments recurrent concepts into unnecessary new
   adapters

4. DEFER causes persistent learning deadlock

5. results depend on introducing an arbitrary magnitude threshold

6. non-invasive prospective scoring ceases to restore state exactly

# 12. Methodological interpretation

The live controller tests the following principle:

Retention feasibility and incoming action utility are separate.

No-safe-reuse does not imply fresh capacity.

Fresh-better-than-reuse does not imply fresh capacity.

Permanent expansion requires:

- positive fresh utility relative to the unchanged learner
- superiority to feasible reuse
- persistence across consecutive evidence windows

Two-window persistence is stabilization machinery and is not
claimed as an original contribution.

# 13. Novelty discipline

Do NOT claim:

- first dynamic adapter expansion
- first adapter reuse
- first lookahead
- first predicted forgetting
- first reuse/spawn/defer controller
- first sequential evidence
- first delayed expansion

The candidate contribution remains:

optimizer-faithful evaluation of the absolute system utility of
candidate capacity interventions relative to the unchanged learner,
with prospective retention treated as a separate feasibility
constraint.

This claim remains provisional until comparison with contemporary
baselines.
