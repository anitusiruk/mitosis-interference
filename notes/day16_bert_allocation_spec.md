# Classifier architecture transfer diagnostic

Freeze before BERT research outcomes. The DistilBERT allocation findings and the
novelty audit motivated this extension. It is a development-stage transfer check,
not a new independent test-set confirmation or a competitive benchmark.

Question: Does the observed equivalence between full-package and classifier-only
allocation survive replacing DistilBERT's trainable pre-classifier/classifier stack
with BERT's single linear classifier on a frozen pooler? A different result is a
valuable boundary of the finding; it must not be suppressed or “repaired” by tuning.

Use google-bert/bert-base-uncased, resolving and hashing one immutable revision
before execution. Store config, tokenizer and backbone SHA256 manifest; do not
substitute a later model snapshot. Use rank-8/alpha-16 LoRA on every query/value
attention projection, zero LoRA dropout, the original clipped AdamW lr=0.0002
training recipe, 64-token context, 512-total-item reservoirs, 64-item probes,
maximum eight packages, and unchanged CAU-v1 allocation/protection semantics.
Pretrained backbone and pooler remain frozen. The head-only control keeps LoRA
outputs identically zero and optimizes only the private linear classifier.

Run BANKING seeds 2027–2031, both canonical/B-first orders, private and head-only:
20 trajectories, exact stream SHA matches to corresponding Day-8 references.
Queue seed, order, private then head-only. No task identities are supplied to
allocation or prediction. Evaluation-only concept metadata remain in the data
builder and metrics. Official test sets are not evaluated. Dataset/pretraining
exposure limits already recorded for the project still apply.

Primary outcome: complete decision/selected-package disagreement count between
private and head-only within each BERT seed/order. Also retain all spawn steps,
learning updates, package counts, initial/predicted utilities and all three frozen
label-free deployment rules. Compare these descriptive allocation outcomes with
DistilBERT on the same streams. A changed training/backbone recipe cannot be a
causal attribution solely to classifier design: backbone depth, representations,
tokenization, frozen pooler and classifier all differ. This is cross-architecture
transfer evidence, not a one-factor classifier experiment.

Average two orders within seed for descriptive accuracy differences and show all
five seed values. Five seeds and fixed repeatedly inspected development examples
do not support broad population inference. No best routing rule or favorable seed
is selected. There is no tuned fixed-single baseline in this extension, so no claim
that BERT allocation outperforms a fair static alternative is permitted. Learning
curves are diagnostics; if learning is weak, say so and plan separate fair tuning.

Before execution, pass real tiny BERT/PEFT tests for private classifier detection,
zero-output head-only LoRA, frozen pooler, exact transactional crossfit restoration,
bounded-memory lifecycle, and cloned inherited update equivalence. Preserve all
failed attempts, halt on nonfinite losses or budget/data mismatch, refuse to
overwrite outputs, and save complete checkpoints and raw logs to the existing
mitosis-interference branch. Run one GPU experiment at a time; wall time is
descriptive and is not a dedicated hardware benchmark.
