# Day 2 Prospective Signal Freeze

## Decision

The primary prospective absorbability signal is frozen as:

    AdamW-I1

Definition:

Apply one temporary optimizer-faithful AdamW update to the
currently considered adapter using the incoming window.

Measure the change in protected historical loss:

    I1 = L_memory(theta_virtual) - L_memory(theta)

Restore:

- trainable parameters
- optimizer state
- CPU RNG
- CUDA RNG
- NumPy RNG
- Python RNG

before real training continues.

Positive I1 means the candidate adapter is predicted to incur
backward harm from absorbing the incoming update.

## Five-run BANKING77 development result

AdamW-I1:

    mean AUROC = 0.9354
    std AUROC  = 0.0292
    min AUROC  = 0.9040
    max AUROC  = 0.9683
    mean AUPRC = 0.9144

It beat gradient conflict in 5/5 streams.

It beat the CABLE-style affinity risk signal in 5/5 streams.

Mean paired AUROC advantage over CABLE-style risk:

    +0.2742

## Important scope

These results establish predictive signal quality.

They DO NOT yet establish that an adapter expansion policy based
on I1 improves continual-learning accuracy, forgetting, or
parameter efficiency.

The next experiment is an end-to-end reuse-versus-spawn controller.

## Primary hypothesis going forward

Distribution novelty is not equivalent to need for parameter
isolation.

Allocate new adapter capacity only when no existing adapter is
predicted to safely absorb the incoming update.

## Frozen main signal

Use AdamW-I1 as the primary signal.

AdamW-I3 and AdamW-I5 remain ablations only.
