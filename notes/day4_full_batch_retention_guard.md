# Day 4 Amendment — Full-Batch Retention Guard

Date: 2026-10-04

Status:
PREDECLARED BEFORE CAU-v0 IMPLEMENTATION AND BEFORE ANY
LIVE CAU-v0 RESULTS.

This amendment supplements, but does not replace, the frozen
Day-3 live action policy.

## Motivation

The frozen cross-fitted action-utility estimator performs one
optimizer-faithful update on a support half of the incoming batch
and evaluates incoming utility on the complementary held-out half.

The eventual live REUSE action, however, performs the real update
on the entire incoming batch.

Therefore the cross-fitted harm feasibility estimate is not exactly
the protected-harm consequence of the full-batch update that would
actually be committed.

Cross-fitted system utility remains the selection signal.

Before committing a REUSE action, an additional exact prospective
full-batch protected-harm guard is required.

No new numerical threshold is introduced.

## Cross-fitted reuse candidate set

For every mature existing adapter j, retain the frozen Day-3
quantities:

U_reuse_j

and the two-fold protected-harm feasibility rule.

A candidate enters the provisional reuse set only if:

1. it is cross-fold feasible under the frozen rule

AND

2. U_reuse_j > 0

Strict positivity is retained.

## Full-batch prospective guard

For every provisional positive-utility reuse candidate j:

1. snapshot its private reservoir RNG state
2. run the existing optimizer-faithful full-batch prospective
   profile on the actual incoming full batch
3. record:
   - harm
   - harm_se
   - harm_lcb
   - harm_ucb
   - gain
   - cur_before
   - cur_after
4. restore the reservoir RNG state
5. rely on the existing profile transaction to restore:
   - parameters
   - optimizer state
   - global RNG
   - model train/eval state

Define:

full_batch_safe_j =
    full_batch_harm_lcb_j <= threshold

The existing threshold remains exactly 0.0.

No new confidence constant or margin is introduced.

## Final reusable candidate

Among candidates satisfying:

- positive cross-fitted system utility
- frozen cross-fold harm feasibility
- full-batch protected-harm feasibility

choose the candidate with maximum cross-fitted system utility.

The full-batch current-batch gain is diagnostic only.

It is NOT used to rank candidates.

It is NOT used as another threshold.

If no candidate survives the full-batch guard:

REUSE is unavailable.

## Interaction with fresh confirmation

The frozen fresh-positive definition is unchanged.

If fresh-positive is confirmed on two consecutive eligible windows:

    SPAWN

The confirmed fresh action has priority over reuse exactly as frozen
in the Day-3 live policy.

On the FIRST fresh-positive window:

    pending_fresh = True

Then:

    if a guarded positive-utility reuse candidate exists:
        REUSE it
    else:
        DEFER

If the current window is not fresh-positive:

    pending_fresh = False

Then:

    if a guarded positive-utility reuse candidate exists:
        REUSE it
    else:
        DEFER

Warmup or unavailable windows break pending confirmation exactly as
specified previously.

## DEFER

DEFER remains a literal no-learning action:

- no optimizer step
- no replay-memory addition
- no update-counter increment
- no new adapter

No pending-example replay buffer is introduced in CAU-v0.

## Fresh action

The current fresh action retains the already-audited PEFT semantics:

- fresh LoRA
- fresh pre-classifier
- fresh classifier

No separate full-batch old-memory guard is added to fresh in this
development architecture because the fresh adapter package does not
modify the stored parameters of mature existing adapters.

This assumption MUST be revisited in the planned shared-head
architecture, where a shared classifier may be modified.

## Interpretation

The cross-fitted quantity is described as:

    a cross-fitted prospective action-utility estimate

It is NOT described as an unbiased estimate of the exact full-batch
intervention.

The full-batch guard closes the mismatch between half-batch
prospective harm estimation and the actual full-batch reuse update.

## No tuning

This amendment:

- introduces no magnitude threshold
- introduces no lambda
- does not use task/domain/segment identity
- was frozen before live CAU-v0 results
