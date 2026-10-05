# Day 4 CAU-v0 Implementation Clarifications

Date: 2026-10-04

Status:
PREDECLARED BEFORE CAU-v0 IMPLEMENTATION AND BEFORE ANY
LIVE CAU-v0 RESULTS.

These are implementation clarifications only.

They introduce no threshold and do not alter the frozen
counterfactual action-utility definitions.

## 1. Warmup

Existing warmup semantics are retained exactly.

If warmup_name is not None and its replay memory contains fewer
than memory_probe examples:

- pending_fresh is reset to False
- the warmup adapter is activated
- action utility is NOT evaluated
- the warmup adapter receives the real full-batch training update

Once its replay memory reaches memory_probe, warmup_name is cleared
before the next action-utility evaluation.

## 2. Unavailable diagnostic

If cross-fitted action utility returns any status other than "ok":

- pending_fresh is reset to False
- no candidate intervention is supported by the diagnostic
- the controller DEFERs
- the previously real active adapter remains active
- no optimizer update or replay-memory addition occurs

This is the conservative interpretation of an unavailable decision.

## 3. Full-batch guard state restoration

For every provisional positive-utility reuse candidate:

- snapshot that adapter's private reservoir RNG
- call the existing exact full-batch profile()
- restore the private reservoir RNG
- explicitly reactivate the real pre-decision adapter

profile() already restores:

- candidate trainable parameters
- candidate optimizer state
- global RNG
- train/eval mode

The additional wrapper therefore closes the remaining private-RNG
and active-adapter restoration requirements.

## 4. Full-batch candidate ranking

The full-batch guard is feasibility-only.

Among candidates that have:

- positive cross-fitted system utility
- frozen cross-fold feasibility
- full-batch protected-harm feasibility

ranking remains based on the frozen cross-fitted system utility.

No full-batch incoming gain or loss is used as a new ranking score.

## 5. Canonical live call

CAU-v0 exposes one canonical real-training entry point:

live_step(texts, labels, restore_name)

It:

1. makes the action decision
2. executes the real train_step only for:
   - warmup
   - reuse
   - spawn
3. executes NO train_step for DEFER
4. returns the adapter that is truly active after the action

This centralizes DEFER semantics so experiment harnesses cannot
accidentally train after a defer decision.

## 6. Confirmed fresh priority

If two consecutive eligible fresh-positive windows are observed:

SPAWN has priority.

A full-batch reuse guard does not override an already confirmed
fresh action.

This matches the frozen Day-3 policy.

## 7. No live-result tuning

No behavior in this note may be changed based on the first Amazon
or BANKING live pilot.

If one of these choices produces a structural failure, the failure
will be recorded before any subsequent method revision.
