# Day 5 causal audit — frozen before new experiment outcomes

Date: 2026-10-05 (Dallas). Baseline checkpoint: `91e2fff`.
Status: development; seed 2026 remains development only.

## Questions and interpretation lock

1. Is the original BANKING fresh-package advantage attributable to a new LoRA,
   a fresh private classification stack, optimizer reset, or their interaction?
2. Does allocation remain useful with a physically shared classification stack?
3. How much protected loss increase is admitted by the frozen lower-bound gate?

Do not change CAU-v1 thresholds, z=1.96, learning rate, LoRA rank, confirmation
length, or original stream after viewing these outcomes. Preserve unsuccessful
results. Do not interpret an architectural failure as permission to tune until
success. New seeds and orders will be confirmation only after causal decisions.

## Original-model component audit

Run the frozen private-package CAU-v1 stream, with optional strictly observational
paired probes before eligible updates. Every probe starts from the same learner
state, uses the original complementary support/query folds, and restores model,
optimizers, adapter registry, RNGs, reservoir state, gradients and trainability.

At each chosen checkpoint compare a 2x2 intervention: existing versus fresh LoRA,
and inherited versus original fresh classification stack (pre-classifier AND
classifier). Preserve AdamW state for inherited components; fresh components get
new parameter-wise AdamW state. Include reset-optimizer controls separately.
The existing source is the real active adapter before the window, fixed before
candidate scoring (not the hindsight winner among candidate adapters). Pair
dropout randomness across component trials by restoring a common pre-trial RNG
state after temporary initialization; real spawn RNG semantics are checked
separately in the shared-head live architecture. Include a common frozen-head
pair as a restrictive diagnostic, not a substitute for the shared trainable head.
Matched-head contrasts identify the marginal LoRA intervention at a common
starting head. They are conditional one-step diagnostics, not proof of the
long-run causal effect of structural capacity. Report all four cells and the
interaction; a head-only explanation narrows the claim to adapter/head packages.

## Physically shared-head sensitivity run

One pre-classifier and one 77-way (BANKING) or 2-way (Amazon) classifier are shared
by every LoRA. No private PEFT `modules_to_save` copies are allowed. Use a feature
extraction PEFT wrapper around the classification model and explicitly train the
single shared stack. One AdamW optimizer stores one moment/step state per shared
head parameter and separate states per LoRA parameter. Candidate fresh LoRA
inherits current head parameters AND head moments; only LoRA is newly initialized.

Retain the CAU-v1 utility definition and two-window confirmation. Because every
head update can affect every adapter, every prospective update (reuse, fresh,
and post-spawn warmup) must check each mature adapter's protected reservoir.
Each protected adapter uses the frozen lower-bound rule, and all must pass.
Fresh utility evidence must pass in both folds and, before permanent spawn,
in an exact full-batch trial. A rejected full-batch fresh trial resets pending
evidence and falls back to guarded reuse, otherwise DEFER. Warmup on newly
created capacity is guarded against all mature old adapters; the initial
default warmup has no old protected history. This is a predeclared architecture
sensitivity extension, not the identical Day-4 private-package policy.

## Gate semantics and resource accounting

For loss increase H, `H - 1.96*SE <= 0` means the probe has not provided strong
positive evidence of harm. It does NOT establish that H is nonpositive. Log
mean harm, lower/upper bounds, number of admitted positive-mean updates, and
counterfactual held-out retention. Do not call this a formal 95% safety guarantee.
Do not silently replace the frozen gate with an upper-bound gate.

Log LoRA/head parameter counts separately, total unique trainable parameter
count, actual optimizer tensor bytes, replay items, elapsed time, GPU peak
memory, learning coverage, spawns and defers. Per-adapter replay grows with
capacity in this development audit; it is not a fixed-total-memory comparison.
Replay reservoirs here protect/route; original real training uses incoming data
without rehearsal. Describe this distinction in the paper.

## Evaluation discipline

BANKING: load only the train split, retain the existing fixed train-derived dev
split and disjoint recurrence examples. Amazon: only train and validation.
Never inspect official test examples/labels or use them for selection.
Segment and concept annotations are evaluation-only. Oracle adapter accuracy
and concept-restricted accuracy are diagnostics, not task-free deployed accuracy.
The unchanged active adapter is the status-quo loss baseline, not a deployable
label-free router. Report this scope explicitly.

## Integrity gates before live runs

Check physical head identity, optimizer parameter uniqueness, inherited shared
head moments, new-LoRA empty moments, counterfactual versus real one-step equality,
full state restoration including gradients/trainability, temporary adapter
cleanup, protection of nonselected adapters, and both warmup/fresh guards.
Require finite metrics and no official-test access. Save hashes of code, stream,
environment and predeclaration alongside outputs. Write logs and intermediate
rows incrementally so browser/terminal failure cannot erase completed work.

## Stop and interpretation

Record every completed run; no window-level statistical significance claims.
Use seed/order as the inferential unit in the later confirmation suite. Finish
or checkpoint active work by 22:30 America/Chicago; do not schedule unrestricted
jobs beyond that time or terminate the user's pod. A failure of the shared-head
run would refute representation-only capacity claims for this setting, while
leaving a narrower package-allocation finding possible pending component audits.
