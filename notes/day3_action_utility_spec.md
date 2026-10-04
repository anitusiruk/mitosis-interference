# Day 3 Counterfactual Action-Utility Specification

Date: 2026-10-03

Status:
PREDECLARED BEFORE IMPLEMENTATION AND BEFORE NEW ACTION-UTILITY RUNS.

This document freezes the next diagnostic methodology.

No live routing decisions will be changed in this stage.

## 1. Research question

The diagnostic asks:

Does an incoming batch actually benefit from fresh capacity,
rather than merely making fresh capacity look better than reuse?

This explicitly separates:

1. protected-retention safety
2. absolute incoming plasticity
3. relative fresh-vs-reuse advantage

Distribution novelty itself is not used as an allocation criterion.

## 2. Real trajectory

The real learner continues to use the previously defined V3 controller.

The new scorer is observational only.

It must not alter:

- real adapter selection
- real optimizer state
- trainable parameters
- memory contents
- reservoir RNG state
- Python RNG
- NumPy RNG
- Torch CPU RNG
- CUDA RNG
- model mode
- active adapter

Exact trajectory equality is a prerequisite for interpreting results.

## 3. Cross-fitting

For each eligible incoming batch:

Fold A:
- even-index examples = support
- odd-index examples = query

Fold B:
- odd-index examples = support
- even-index examples = query

Both folds must be evaluated transactionally and restored exactly.

All query examples are therefore used once for held-out action evaluation.

No random fold selection is introduced.

## 4. No-update reference

For each fold, evaluate query loss BEFORE any prospective update.

Call this:

L_noop

This is the reference required for absolute action utility.

## 5. Existing-adapter action

For every mature existing adapter j:

1. activate j
2. evaluate query loss before update
3. apply the exact prospective AdamW update on support
4. evaluate query loss after update
5. evaluate protected-memory harm
6. restore state exactly

Define cross-fitted prospective query loss:

L_reuse_j

Define absolute reuse gain:

G_reuse_j =
    L_noop_j - L_reuse_j

Positive G_reuse_j means the prospective reuse update
improves held-out incoming query loss.

Protected harm remains:

H_reuse_j =
    L_protected_after_j
    - L_protected_before_j

The existing frozen V3 harm-feasibility semantics remain observationally logged.

No new harm threshold is introduced here.

## 6. Fresh action

Instantiate the same fresh-capacity action used by the
existing shadow implementation.

For each fold:

1. create temporary fresh adapter
2. evaluate its query loss before update
3. apply one exact support AdamW update
4. evaluate query loss after update
5. delete temporary adapter
6. restore all state exactly

Define:

L_fresh

Absolute fresh gain:

G_fresh =
    L_fresh_before
    - L_fresh_after

Positive G_fresh means the fresh action actually improves
its own held-out query performance.

## 7. Relative fresh advantage

For the best feasible reuse candidate j*:

A_fresh =
    L_reuse_j*
    - L_fresh

Equivalently when baselines are comparable:

A_fresh =
    G_fresh
    - G_reuse_j*

Positive A_fresh means fresh is better than reuse.

However:

A_fresh > 0

is NOT sufficient evidence that fresh capacity is useful.

The same batch must also satisfy:

G_fresh > 0

This rule is motivated by the previously observed Amazon
step-11 failure, where fresh was relatively better than reuse
while both actions worsened query loss.

## 8. Fresh-positive window

For offline diagnostic purposes only, define a window as
fresh-positive when:

1. G_fresh > 0
2. A_fresh > 0

No magnitude threshold is used.

This is NOT yet a live allocation rule.

## 9. Two-window confirmation diagnostic

Also log an offline indicator:

fresh_confirmed_2window = true

only when two consecutive eligible windows are both
fresh-positive.

This is stabilization machinery, not claimed novelty.

Two-window confirmation is treated as prior-art-inspired
engineering and will not be claimed as an original contribution.

No segment/task labels may be used to compute confirmation.

## 10. Warmup

Warmup batches for which mature action comparison is unavailable
remain marked unavailable.

They must not be silently treated as negative evidence.

## 11. Development benchmarks

Initial diagnostics are development experiments only.

BANKING77:
- existing balanced recurrence
- A1 -> B1 -> A2 -> C1 -> B2
- official test remains frozen from the clean-development phase

Amazon:
- home -> apparel -> home -> drugstore -> apparel
- same binary sentiment labels
- fixed validation sets are development data
- official test remains unaccessed for development

Segment IDs are evaluation metadata only.

They are never provided to the allocator/scorer.

## 12. Primary diagnostic question

The method is promising only if absolute action utility provides
qualitatively different evidence in the two regimes:

BANKING77:
- sustained fresh-positive evidence should occur where additional
  capacity is genuinely useful
- recurrence should favor reuse rather than fresh capacity

Amazon:
- fresh-positive evidence should generally be absent or transient
  when shared adaptation is already useful
- isolated positive events should not become sustained evidence

These are development diagnostics, not final statistical tests.

## 13. Failure criteria

Stop and redesign rather than tune thresholds if any of the following occur:

1. non-invasiveness fails
2. fresh-positive evidence remains broadly persistent in Amazon
   despite fresh adapters being held-out inferior
3. BANKING77 isolation-needed periods do not produce stronger
   fresh evidence than recurrence
4. results depend on arbitrary magnitude thresholds
5. apparent success is attributable only to separate classifier heads

No scalar advantage threshold will be tuned from these runs.

## 14. Shared-head follow-up

The current diagnostic intentionally keeps existing PEFT semantics
to isolate the change in action-value estimation.

If the action-utility diagnostic succeeds, the next architectural
audit will make shared classifier-head experiments primary.

That experiment will test whether allocation behavior survives when:

new capacity = new LoRA capacity

rather than:

new capacity = new LoRA + isolated classifier head

## 15. Novelty claim permitted by this stage

Do NOT claim novelty for:

- lookahead itself
- dynamic adapters
- reuse/spawn/defer
- two-window confirmation
- sequential evidence
- predicted forgetting

The candidate contribution is:

direct evaluation of the absolute utility and protected-retention
consequences of candidate optimizer actions for capacity allocation,
rather than treating relative adapter preference or distribution
shift as sufficient evidence that expansion is useful.

This claim remains provisional until contemporary baseline
comparisons are completed.
