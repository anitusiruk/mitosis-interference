# Within-backbone linear-classifier allocation control

Designed after the primary DistilBERT, BERT and first weight/state development
outcomes, before this control's outcomes. The original DistilBERT head-only control
trains both the hidden pre-classifier and the output classifier. It rules out a
need for LoRA in the observed allocation sequences, but is not a control without
learned hidden representation capacity. BERT's frozen-pooler linear classifier
changes several architecture components together and does not isolate this issue.

Keep DistilBERT, its explicit pinned backbone, tokenizer, model initialization,
rank-8 Q/V adapters, dropout, clipping, optimizer rate, incoming updates, stream,
allocation rule and fixed 512-text memory unchanged. Freeze the pre-classifier
for every real and temporary package. Compare private LoRA-plus-output-classifier
learning with zero-output, frozen-LoRA, output-classifier-only learning. Both have
the same fixed hidden pre-classifier. The trainable output classifier is linear
in this fixed head representation; input-to-logit prediction is not a globally
linear function of text. PEFT retains dormant private pre-classifier copies; report
that stored cost explicitly rather than counting it as learned capacity.

Use BANKING seeds 2027–2031, both original orders, and both learning controls:
20 complete trajectories. Preserve every original deployment rule. Report all
private/head-only allocation pairs, all deviations from their trainable-stack
references, all three deployment rules and all actual storage counts. Average
orders inside training seeds before descriptive Student intervals. There is no
selection of windows, seeds, prediction rules, or architecture by outcomes.
This is a development diagnostic, not a tuned performance benchmark, untouched
confirmation, or universal capacity theorem. Freezing the hidden layer also
removes its optimizer state; that consequence is part of this training ablation,
not an independent weight-versus-state causal isolation.

Before research, pass tiny CPU and CUDA real PEFT/AdamW gates: the pre-classifier
and its copies stay bitwise equal to the original; only the declared output
classifier and, in the private condition, LoRA parameters train; zero-LoRA behavior;
exact shadow restoration; equality of inherited shadow and actual update; and
spawn/memory invariants. Then run an 80-step unchanged-wrapper replay with freezing
disabled against the complete head-only seed-2031 B-first fixed-memory reference.
Require the entire final learner state and adapter tensors to be bitwise equal.
Any gate failure is preserved and halts research. Never relax tolerances quietly.

Commit the protocol, source and tiny gate logs before research to the existing
`day17-static-tuning-20261006` branch of `anitusiruk/mitosis-interference`. Wait for
the static worker's independently verified save, then reuse its isolated worktree
and lock. Continue sharing the GPU with the original factorial queue; timings are
descriptive. Save every attempt and independently fetch/hash every new checkpoint.
The branch integrator can acquire this lock only after the diagnostic finishes;
its combined snapshot verification will include these checkpoints. Keep the
original administrative cutoff and deadline, preserving partial coverage if needed.
