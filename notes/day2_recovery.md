# Day 2 Recovery Notes

Day-2 local files were lost before being pushed to GitHub.
The following results were preserved in the research conversation.

## Independent-memory exploratory scan

BANKING77, seed 2026.

- novelty AUROC: 0.6993
- gradient conflict AUROC: 0.8039
- simple virtual interference AUROC: 0.8039
- AdamW-I1 AUROC: 0.9542
- AdamW-I3 AUROC: 0.9706
- AdamW-I5 AUROC: 0.9760

This experiment used separate predictor and evaluation memories.

## Official-test exploratory scan

This experiment used held-out BANKING77 test examples as the
future-harm target. Because these results were inspected during method
development, they are exploratory only and the official test set
should no longer be used for tuning.

- novelty AUROC: 0.6282
- gradient conflict AUROC: 0.7694
- virtual interference AUROC: 0.7543
- AdamW-I1 AUROC: 0.9440
- AdamW-I3 AUROC: 0.9386
- AdamW-I5 AUROC: 0.9192

## Clean development protocol

A fixed 20 percent per-class development split was created from
BANKING77 training data. These development examples never receive
gradient updates. The official test set is untouched.

Canonical seed/order:

- novelty AUROC: 0.6321
- gradient conflict AUROC: 0.8311
- virtual interference AUROC: 0.7843
- AdamW-I1 AUROC: 0.9732
- AdamW-I3 AUROC: 0.9716
- AdamW-I5 AUROC: 0.9599

Alternate seed and class order:

- novelty AUROC: 0.6300
- gradient conflict AUROC: 0.8483
- virtual interference AUROC: 0.8267
- AdamW-I1 AUROC: 0.9783
- AdamW-I3 AUROC: 0.9767
- AdamW-I5 AUROC: 0.9683

## Important methodological audit

The development runs above did not restore global RNG state after
counterfactual diagnostics. Virtual forward passes can consume dropout
randomness and therefore potentially perturb the subsequent real
training trajectory.

The recovered final script fixes this by snapshotting and restoring:

- Python RNG
- NumPy RNG
- PyTorch CPU RNG
- PyTorch CUDA RNG

around all virtual diagnostics.

Therefore the next experiment is to replicate the canonical and
alternate-order development runs using the RNG-safe implementation.

## Working interpretation

The current evidence supports prospective optimizer-aware interference
as a substantially stronger predictor of future held-out forgetting
than representation novelty.

AdamW-I1 is currently the primary candidate because it gives the
strongest binary harm discrimination while being simpler and cheaper
than repeated 3/5-step adaptation.

I3 and I5 should be treated as adaptation-depth sensitivity analyses,
not literal predictions of future unseen batches.

## Novelty positioning

Do NOT claim that hypothetical updates, interference-aware replay,
dynamic adapter allocation, or adapter expansion are individually new.

Closest prior concepts include MIR, CABLE, SEMA, Online-LoRA and
related dynamic adapter/routing methods.

The intended contribution is narrower:

Distribution novelty is not the same decision variable as safe
absorbability. A task-free continual learner should reuse existing
capacity when an incoming update can be absorbed without predicted
backward harm and expand only when existing adapters are unsafe.

The next closest-prior-work experiment after RNG-safe replication is
a direct CABLE-style one-step lookahead baseline.
