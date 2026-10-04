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


# Amendment 1 — Common Status-Quo No-Update Baseline

Date: 2026-10-03

Status:
PREDECLARED BEFORE IMPLEMENTATION AND BEFORE ANY NEW
ACTION-UTILITY RESULTS.

This amendment supersedes Sections 4, 6, 7, and 8 wherever
their definition of "absolute gain" conflicts with the definitions
below.

## Motivation

The original specification defined fresh absolute gain relative to
the fresh adapter's own pre-update state.

That quantity measures whether a fresh adapter can learn from its
support data, but it does not measure whether spawning fresh
capacity improves the system relative to doing nothing.

Example:

- active existing adapter query loss = 0.30
- fresh before update = 0.69
- fresh after update = 0.50

Fresh has positive within-adapter training gain:

0.69 - 0.50 = +0.19

but fresh is still much worse than the current system:

0.30 - 0.50 = -0.20

Therefore a common action baseline is required.

## Common status-quo baseline

For each cross-fit fold, define:

L_statusquo

as the query loss of the REAL currently active adapter before any
prospective action is applied.

The real active adapter is inherited from the unchanged V3
trajectory.

No adapter is selected using segment/domain identity.

No prospective optimizer step is performed for the status-quo
reference.

This represents the DEFER / NO-COMMIT action.

Define:

U_defer = 0

by construction.

## Reuse action utility

For every mature existing adapter j:

1. evaluate the common status-quo query loss
2. activate candidate adapter j
3. apply the exact prospective AdamW support update
4. evaluate candidate j on the held-out query examples
5. restore all state exactly

Define:

U_reuse_j =
    L_statusquo
    - L_reuse_j_after

Interpretation:

U_reuse_j > 0:
    updating candidate j improves query performance relative
    to leaving the real current model unchanged

U_reuse_j < 0:
    the status quo is better than prospective reuse action j

Also log candidate-local trainability:

T_reuse_j =
    L_reuse_j_before
    - L_reuse_j_after

T_reuse_j is diagnostic only.

It is NOT the system-level action utility.

## Fresh action utility

For the temporary fresh adapter:

1. evaluate L_statusquo on the unchanged real active adapter
2. instantiate the exact existing fresh-capacity action
3. evaluate fresh query loss before update
4. apply one exact AdamW support update
5. evaluate fresh query loss after update
6. delete the temporary adapter
7. restore all state exactly

Define:

U_fresh =
    L_statusquo
    - L_fresh_after

This is the PRIMARY fresh absolute-utility quantity.

Positive U_fresh means fresh capacity predicts lower query loss
than simply leaving the current real adapter unchanged.

Also log:

T_fresh =
    L_fresh_before
    - L_fresh_after

T_fresh measures fresh-adapter trainability only.

It is NOT sufficient evidence for expansion.

## Relative fresh advantage

Among protected-harm-feasible mature reuse candidates, define:

U_best_reuse =
    max_j U_reuse_j

If at least one feasible reuse candidate exists:

A_fresh =
    U_fresh
    - U_best_reuse

If no feasible reuse candidate exists:

fresh is compared directly against defer:

A_fresh_vs_defer =
    U_fresh

"No feasible reuse" must NOT imply mandatory spawn.

## Fresh-positive window

A window is fresh-positive only when:

If feasible reuse exists:

    U_fresh > 0

AND

    U_fresh > U_best_reuse

If no feasible reuse exists:

    U_fresh > 0

Strict inequalities are used.

No magnitude threshold is introduced.

This means fresh must beat:

1. the status quo / defer action
2. the best feasible reuse action, when one exists

## Two-window diagnostic

fresh_confirmed_2window is true only when two consecutive
eligible windows are fresh-positive.

Task/segment IDs are not used.

Two-window confirmation remains an offline diagnostic in Day 3.

It does not yet alter the real V3 trajectory.

## Why this amendment matters

This amendment explicitly represents the previously missing
third possibility:

- reuse is harmful or unhelpful
- fresh is also harmful or unhelpful
- therefore DEFER is preferable

This addresses the previously observed Amazon failures:

- step 11: both prospective update actions had negative gain
- step 71: no safe reuse existed, but fresh prospective gain
  was also negative

The live controller will not be changed during this diagnostic.

## Interpretation discipline

Positive candidate-local trainability T_fresh is not evidence that
fresh capacity is globally useful.

Relative superiority to reuse is not sufficient either.

The primary quantity is common-baseline system utility U.

This amendment was frozen before implementation and before
observing any results produced by this definition.


# Amendment 2 — Cross-Fold Candidate Aggregation

Date: 2026-10-04

Status:
PREDECLARED BEFORE ACTION-UTILITY IMPLEMENTATION AND BEFORE
ANY ACTION-UTILITY RESULTS.

This amendment defines how the two folds are combined and fixes
the behavior for odd-sized batches.

## Explicit complementary folds

For a batch with indices 0 ... n-1:

Fold A:
- support = even indices
- query = odd indices

Fold B:
- support = odd indices
- query = even indices

Therefore every example is used exactly once as held-out query
evidence, including when n is odd.

The prior adjacent-pair swapping implementation is NOT reused for
this diagnostic because for odd n it leaves the final example in
the same side in both folds.

## Query-count-weighted aggregation

Fold-level query losses and utilities are means over their
respective query examples.

Because odd batches produce unequal query-set sizes, cross-fitted
query quantities are aggregated by query example count.

For quantity Q:

Q_crossfit =
    (n_query_A * Q_A + n_query_B * Q_B)
    / (n_query_A + n_query_B)

Thus every example contributes equal held-out query weight.

For even batches this reduces to the ordinary mean of the two folds.

## Candidate-level aggregation before selection

Reuse candidates are NOT selected independently in Fold A and
Fold B and then averaged.

For every mature adapter j:

1. compute Fold-A action utility
2. compute Fold-B action utility
3. aggregate adapter j's utility across folds
4. aggregate its query loss/trainability across folds
5. retain both fold-specific protected-harm measurements

Only after candidate-level cross-fitting is complete is the best
reuse candidate selected.

This avoids combining two different fold-specific winning adapters
into a synthetic "best reuse" action.

## Cross-fold protected-harm feasibility

No new harm threshold is introduced.

Candidate adapter j is cross-fold feasible only if the existing
frozen V3 criterion holds in BOTH prospective support directions:

harm_lcb_A <= threshold

AND

harm_lcb_B <= threshold

This is intentionally conservative.

Both fold-specific harm, SE, LCB and UCB values remain logged.

The candidate's mean harm is diagnostic only.

## Best reuse candidate

Among cross-fold-feasible mature adapters:

best_reuse =
    argmax_j U_reuse_j_crossfit

Ties are broken by:

1. lower maximum fold harm LCB
2. lower mean prospective harm
3. adapter name for deterministic final tie breaking

No segment identity is used.

## Fresh action

Fresh utility is aggregated using the same query-count-weighted
cross-fitting rule.

The temporary fresh adapter initialization is generated through the
existing shadow-fresh transaction.

Because that transaction restores RNG state, the two folds start
their fresh candidate from the same stochastic initialization state.

## Fresh-positive diagnostic

If at least one cross-fold-feasible reuse candidate exists:

fresh_positive =
    U_fresh > 0
    AND
    U_fresh > U_best_reuse

If no cross-fold-feasible reuse candidate exists:

fresh_positive =
    U_fresh > 0

"No feasible reuse" never implies fresh-positive by itself.

## Two-window confirmation

Two-window confirmation remains an OFFLINE diagnostic.

It is not stored as mutable controller state in the action-utility
pool.

It will be computed from the logged sequence after the run:

confirmed at t iff
    fresh_positive[t-1]
    AND
    fresh_positive[t]

Only consecutive ELIGIBLE action-utility windows count.

Warmup/unavailable windows break the consecutive sequence.

No task, domain, phase, or segment identity is used.

## Interpretation

The resulting comparison is between complete system actions:

- DEFER / unchanged active adapter
- switch to + update existing adapter j
- instantiate + update fresh capacity

Therefore U_reuse_j includes any effect of switching from the
currently active adapter to candidate j.

It should be described as SYSTEM ACTION UTILITY, not isolated
optimizer-update utility.

This amendment was frozen before implementation and before seeing
results from this definition.
