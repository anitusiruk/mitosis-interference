# Day 2 Strict Backward-Only Predictor Audit

The predeclared strict robustness gate FAILED.

This result must not be relabeled as a pass.

## Five-run strict AdamW-I1

Mean AUROC: 0.9324
Std:        0.0299
Minimum:    0.9085
Maximum:    0.9844

Original five-run I1 mean: 0.9354
Strict five-run I1 mean:   0.9324
Mean change:               -0.0030

## Comparisons

I1 > gradient conflict: 5/5 streams

I1 > CABLE-style risk: 4/5 streams

Run 5:
I1 AUROC:   0.9278
CABLE:      0.9472
Difference: -0.0194

Therefore the predeclared condition requiring I1 to beat
CABLE in all five streams was not met.

## Interpretation

The optimizer-faithful I1 signal remains strongly validated
as a predictor of strict backward harm.

The experiment does NOT establish uniform dominance over the
CABLE-style affinity signal.

The non-boundary-crossing analysis is a sensitivity analysis
and must not be used to retroactively change the gate.

## Boundary-crossing sensitivity

The predeclared strict gate remains FAIL.

However, in the separately defined non-boundary-crossing sensitivity,
AdamW-I1 AUROC was:

canonical: 0.9698
altorder:  0.9770
run3:      0.9902
run4:      1.0000
run5:      0.9857

I1 exceeded CABLE-style risk on all 5 non-crossing subsets.

This does NOT replace the failed main gate.

Interpretation:
AdamW-I1 simulates the consequence of the currently available update.
A 10-step target that crosses a phase boundary additionally depends on
future batches from a distribution unavailable at probe time.

The crossing analysis therefore diagnoses a horizon/action mismatch,
not a revised primary evaluation.
