# Day 3 Amazon Action-Utility Diagnostic

Date: 2026-10-04
Seed: 2026
Status: DEVELOPMENT DIAGNOSTIC

Methodology was frozen before this analysis.

## Integrity

The action-utility scorer was run observationally on the unchanged
V3 Amazon trajectory.

Full 80-step trajectory non-invasiveness:

- row count identical
- segment metadata identical
- domain metadata identical
- adapter choices identical
- decisions identical
- training loss max absolute difference = 0
- best_risk max absolute difference = 0
- best_lcb max absolute difference = 0
- best_ucb max absolute difference = 0
- best_gain max absolute difference = 0

PASS.

## Global action-utility result

Total stream rows: 80
Eligible action-utility windows: 73
Warmup windows: 7

Fresh-positive windows: 4 / 73
Two-window confirmed fresh events: 0

Therefore no Amazon event produced sustained fresh-capacity evidence
under the predeclared two-window diagnostic.

## Segment summary

A1:
- eligible: 12
- fresh-positive: 3
- fresh utility mean: -0.02635
- best-reuse utility mean: +0.00487
- confirmed: 0

B1:
- eligible: 16
- fresh-positive: 0
- fresh utility mean: -0.10876
- best-reuse utility mean: +0.00566
- confirmed: 0

A2:
- eligible: 16
- fresh-positive: 0
- fresh utility mean: -0.31424
- best-reuse utility mean: +0.00589
- confirmed: 0

C1:
- eligible: 16
- fresh-positive: 1
- fresh utility mean: -0.27700
- best-reuse utility mean: -0.00197
- confirmed: 0

B2:
- eligible: 13
- fresh-positive: 0
- fresh utility mean: -0.20188
- best-reuse utility mean: +0.02059
- confirmed: 0

## Fresh-positive events

Step 7 / A1:
- best reuse utility: -0.00747
- fresh utility: +0.02337
- fresh advantage: +0.03084
- fresh local trainability: +0.01587
- not confirmed

Step 11 / A1:
- best reuse utility: -0.00327
- fresh utility: +0.02106
- fresh advantage: +0.02433
- fresh local trainability: -0.01570
- not confirmed

Step 14 / A1:
- best reuse utility: +0.01031
- fresh utility: +0.02711
- fresh advantage: +0.01680
- fresh local trainability: +0.01838
- not confirmed

Step 50 / C1:
- best reuse utility: -0.01744
- fresh utility: +0.07869
- fresh advantage: +0.09613
- fold A fresh utility: -0.59356
- fold B fresh utility: +0.75094
- fresh local trainability: +0.00213
- not confirmed

Step 50 shows extreme fold disagreement and therefore illustrates
why a single-window expansion rule is unstable.

## Previously important failures

Step 23 / B1:
- best reuse utility: +0.00189
- fresh utility: -0.03352
- fresh advantage: -0.03541
- fresh-positive: false

This corrects the old CF-v0 false B1 expansion signal.

Step 71 / B2:
- existing V3 harm LCB: +0.00151
- no cross-fold-feasible reuse
- fresh utility: -0.42014
- fresh-positive: false

Therefore:

"no safe reuse" does NOT imply "fresh capacity is useful."

The status-quo/defer action is essential.

## Absolute utility sign structure

Fresh utility > 0:
7 / 73

Cross-fold feasible reuse exists:
71 / 73

Best reuse utility > 0:
46 / 73

Both fresh and reuse utility <= 0:
24 windows

Fresh utility > 0 but fresh did not beat reuse:
3 windows

## Interpretation

The same-label Amazon regime strongly favors shared adaptation.

Fresh-positive evidence is sparse and transient.

No event survives the predeclared two-window confirmation rule.

This is development evidence only.

Seed 2026 and the fixed Amazon validation sets have been repeatedly
inspected and must not be treated as independent final confirmation.

## Important unresolved confound

At step 11 fresh system utility is positive while fresh local
trainability is negative.

This indicates that fresh initialization itself can contribute to
system-level utility under the current separate-head PEFT semantics.

No decision rule is changed based on this observation.

The predeclared shared-classifier-head experiment remains necessary
before final causal claims about LoRA capacity.
