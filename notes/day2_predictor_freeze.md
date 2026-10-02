# Day 2 Prospective Predictor Freeze

## Frozen primary signal

AdamW-I1 is the primary prospective interference signal.

AdamW-I3 and AdamW-I5 remain ablations only.
They will not replace I1 based on later results.

## Original five-run result

AdamW-I1 AUROC:
mean = 0.9354

The original predeclared robustness gate passed.

## Strict backward-only audit

Strict historical targets exclude the current phase.

AdamW-I1:
mean AUROC = 0.9324
std        = 0.0299
min        = 0.9085
max        = 0.9844

I1 > gradient conflict: 5/5
I1 > CABLE-style risk: 4/5

The predeclared strict robustness gate FAILED because
the all-five-stream CABLE condition was not met.

This failure must not be relabeled as a pass.

## Boundary-crossing sensitivity

The 10-update future target can cross into a distribution
that was unavailable at probe time.

On non-boundary-crossing probes, I1 was consistently strong
and exceeded CABLE-style risk in all five streams.

This is a sensitivity analysis, not a replacement primary result.

## Fixed class-balanced sentinel sensitivity

Five-run fixed-sentinel I1 AUROC:
mean = 0.9368
min  = 0.9194
max  = 0.9844

Continuous association:
mean Pearson  = 0.7439
mean Spearman = 0.7754

Fixed sentinel versus random strict target:
mean target MAE change = 0.0760
total sign disagreements = 1 / 211 probes

Evaluation-only changes produced:
max signal trajectory difference = 0.0

Therefore the predictor result is robust to deterministic,
class-balanced historical evaluation.

## Methodological freeze

No further predictor tuning will be performed.

Primary signal:
AdamW-I1

Strict gate:
FAIL

The official BANKING77 test set remains frozen until the
method/controller design is frozen.

Future work now concerns controller robustness, inference,
capacity accounting, and cross-dataset generalization.
