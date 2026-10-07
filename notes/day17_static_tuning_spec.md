# Matched learning-rate tuning for fixed-capacity baselines

This development extension was designed after the untuned rank-96 results and
the existing adaptive development results were inspected. It repairs a weak
comparator; it is not an untouched test or a source-faithful modern-method
reproduction. Commit the full grid and selection rule before new tuning results.

## Frozen protocol

Use the unchanged Day-12 static trainer, with scoped overrides of only LoRA rank,
alpha and the AdamW learning rate. All runs use DistilBERT at the explicitly pinned
restart revision, full 77-class BANKING predictions, the original train-derived
development split, 80 incoming batches of 16, Q/V LoRA, zero LoRA dropout, gradient
clipping 1.0, and one update per incoming batch. The classifier/pre-classifier is
private and trainable. Each run has exactly one package and at most 512 retained
training examples. Retained examples do not supply rehearsal updates. No expansion,
adaptive selection, early stopping, or router tuning is used for these statics.

Compare ranks 8 and 96 with alpha twice the rank. For EACH rank, use the SAME
learning-rate grid: 0.00002, 0.00005, 0.0001, 0.0002, 0.0004, 0.0008. Run both
canonical and B-first streams at pilot seed 2026: 24 pilot trajectories. Give every
candidate 80 updates and identical evaluation checkpoints. Retain every result,
including poor runs. Halt and preserve any nonfinite or incomplete attempt.

For each rank separately, select the rate maximizing the average of the two pilot
orders' final concept-macro development accuracy under last-active prediction.
Tie-break by the smaller numerical learning rate. Require all 24 pilots before
selection. Commit and push the selected rates, full pilot grid, source/spec hashes
and selection receipt before running the selected rates at seeds 2027–2031, both
orders: 20 trajectories. These seed streams and development examples already
support adaptive analyses, so call this paired development confirmation, never an
untouched final evaluation. Only pilot outcomes determine the baseline rates.

Pair to the completed private CAU fixed-512 trajectories, using exact stream hashes.
Report all three original deployment rules and both frozen learned-routing rules
of the adaptive reference. Static models have one classifier, so their routing
rules are equivalent; verify this. Report both static ranks, every seed/order and
all rules. Average orders within a seed for descriptive 95% Student-t intervals,
with all five seed values retained. No winner is selected from confirmation data.

Report actual adaptation parameters, optimizer bytes, retained examples, GPU peak
and training/evaluation times per trajectory. Equal text memory is not equal
parameter storage or compute. Rank 96 approximates three rank-8 private packages,
but classifier multiplicity and actual pool size still differ. Timings are
descriptive under this shared pod, not a dedicated performance benchmark.

## Implementation and preservation gates

Before pilot outcomes, replay the original rank-96, rate-0.0002 protocol at seed
2031 B-first through the scoped wrapper. Require the current saved Day-12 action
and loss trajectory, bitwise final learner state and saved adapter tensors to
match. This checks the port against a reference produced on the current pinned
environment; it does not establish historical backbone byte identity.

Never overwrite existing outputs. A failed replay or research run halts this
extension and preserves all attempts. Hold the shared GPU-worker lock and start
only after the previous forty diagnostics and their remote checkpoint verification
finish successfully. Launch new jobs before 2026-10-07 03:00 UTC; training deadline
is 03:15 UTC. If coverage is administratively incomplete, record it and omit
unpaired seed summaries. Save code, logs, raw outcomes and every checkpoint to the
existing anitusiruk/mitosis-interference day5-causal-audit branch, with GitHub ref
verification after progress pushes and a fresh LFS roundtrip after the extension.
