# Separate weight and optimizer-state attribution

This extension was designed after the Day-5/6 classifier-only allocation equivalence
and Day-10 initial-loss-ranking results were observed. It is a development-stage
causal diagnostic, not untouched confirmation of a newly discovered hypothesis.
Its four-factor intervention and analysis are frozen before its research outcomes.
Tiny implementation-integrity checks are not research outcomes.

## Question and estimand

Does the measured one-step fresh-package advantage reflect classifier weight
reset, the optimizer-state reset accompanying it, LoRA reset, or interactions
among them? The original component factorial changed weights and corresponding
AdamW states together. Its results cannot distinguish those mechanisms.

At each mature incoming batch of the existing private CAU-v1 fixed-512 trajectory,
cross all four binary factors: inherited/reset LoRA weights, inherited/reset
classifier-stack weights, inherited/empty LoRA AdamW state, and inherited/empty
classifier-stack AdamW state. Run all 16 cells in both complementary even/odd
support/query folds. Use every incoming example exactly once as a query in every
cell. Observe every mature batch, including batches without expansion and with
negative or zero measured contrasts; do not select windows by effect size.

“Reset head” means PEFT's original classifier/pre-classifier initializer, which is
copied from the original frozen modules. It is not an independent new random draw.
LoRA initialization and support dropout randomness are matched across cells.
Inherited optimizer state includes AdamW step, first moment and second moment,
not moments alone. Attaching inherited state to reset weights is an artificial
causal intervention; it need not be a useful deployment recipe. Transported states
are matched by normalized parameter name and exact shape. The AdamW parameter
group, learning rate, clipping at 1.0 and update count remain unchanged.

The reference predictor is the inherited-weight source before the update.
For every cell, record initial query loss, post-update query loss, local improvement,
per-example query losses, component update norm, and hashes of supplied weights
and optimizer state. For source r and candidate a, report the exact identity

U(a) = L(r before) - L(a after)
     = [L(r before) - L(a before)] + [L(a before) - L(a after)].

This algebra is elementary and is not claimed as a novel theorem. Initial predictor
quality is legitimate evidence for an immediate post-update prediction objective;
it is insufficient by itself to identify a need for additional LoRA capacity or
enhanced trainability. A reset need not imply recovered plasticity on future data.

Also decompose each already-computed query cross entropy into the loss of
probability mass assigned to its label group and the conditional classification
loss inside that group: CE(y over full output space) = -log P(group|x) +
CE(y conditioned on group). BANKING uses its three predeclared 11-label groups;
Amazon uses the full shared two-label group, whose mass loss is exactly zero.
Group identities are evaluator-only metadata used to interpret already computed
logits. They never enter allocation, gradients, training or deployed routing.
Save both components before/after every cell and report all factor effects on
them. The identity is elementary, not a new theorem. Decomposition agreement
uses absolute 1e-5 tolerance for float32 reductions. Do not interpret conditional
group accuracy as a label-free deployed result or an oracle advantage.

This label-mass analysis was added before any Day-15/16 research outcomes or
GitHub preregistration, after the first CPU implementation gates. The pending
installer was paused for the amendment; the original frozen GPU queue continued.

## Frozen coverage and comparisons

Use BANKING and Amazon, the two existing orders, and seeds 2027–2031: 20 observer
trajectories, each paired to its saved complete private CAU fixed-512 reference.
Do not tune on these measurements. Historical aggregate backbone reload equality
is not byte-identity proof. Every observer must additionally reproduce its complete
reference action/memory trajectory, training losses within absolute 1e-6, and final
learner state and adapter tensors bitwise. Independently check full state restoration
around every batch's observer. A failed verification halts the queue, preserves the
attempt and excludes its contrasts from causal aggregation until the discrepancy
is resolved transparently. Never quietly relabel a failed audit as a replicate.

The analysis source is the actual active package at that batch, not a retrospectively
chosen best adapter. These contrasts therefore attribute the active-package probe,
not every best-feasible-reuse controller comparison. This distinction must remain
in the paper. The observer does not participate in allocation or training.

Report simple conditional effects of each factor at all eight settings of the other
three factors; also report equal-weight marginal effects and two-factor interactions.
Use post-update query-loss decrease as the effect orientation (positive is better).
Split every post-update contrast into its initial-loss contrast and local-improvement
contrast. Verify this decomposition numerically at every paired batch/cell/fold.
Weight folds by query count; average mature batches within each trajectory; average
the two orders within a seed; then give all five seed values and descriptive Student
95% intervals. The independent unit is training seed, not batch, fold, or example.
Report every conditional contrast and both regimes. Do not select a favorable cell
or sign. Per-batch displays are descriptive. Ratios are omitted when denominators
are near zero; do not report unbounded “fraction explained” as a causal share.

BANKING's disjoint label-group stream and Amazon's same-label domain stream supply
different conditions, not two interchangeable replications. Existing MultiNLI
results are near chance and cannot establish a competitive natural-language
adaptation claim. Broader backbones and stronger natural same-label training remain
necessary to support claims beyond this allocator and these small stress tests.

## Gates and preservation

Before research execution, pass CPU and CUDA tiny real PEFT/AdamW tests for all 16
cells, exact live-state restoration, matched fresh initialization, independent state
transport, initial-prediction invariance to moments, equality with original coupled
cells, equality with a real inherited update, odd-batch coverage, and cell-order
invariance. Save passing logs and the earlier implementation failure/repair record.

Commit this spec and implementation to the existing day5-causal-audit branch before
launch. Never overwrite an existing result folder. Queue in seed, order, regime
order (BANKING then Amazon within each seed/order), independent of observed effects.
An administrative launch cutoff or interrupted run does not change hypotheses;
report incomplete coverage explicitly and resume only previously unlaunched jobs.
Preserve every raw attempt, complete checkpoints, code, provenance, and summaries
in anitusiruk/mitosis-interference only. Official test sets are not evaluated here.
