# Longer-context fixed-package NLI development pilot

Completed candidates: 6/6. Pending: []. Failed: [].

| rate | orders | pilot_training_seeds | final_macro_accuracy | untrained_macro_accuracy | learning_gain | A_accuracy | B_accuracy | C_accuracy | learnability_gate_passed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0001 | 2 | 1 | 0.5043 | 0.3524 | 0.1519 | 0.5208 | 0.5599 | 0.4323 | True |
| 0.0002 | 2 | 1 | 0.6042 | 0.3524 | 0.2517 | 0.5911 | 0.6745 | 0.5469 | True |
| 0.0008 | 2 | 1 | 0.6085 | 0.3524 | 0.2561 | 0.6146 | 0.6667 | 0.5443 | True |

Selected rate: 0.0008; operational learnability gate passed: True.

All candidates use seed 2026 and the same 5760 fit examples and 576 development examples, with both orders paired before rate selection. These examples and this seed are development material. Orders, checkpoints and examples are not independent training replicates; no pilot significance interval is reported. The fixed learning-rate grid and thresholds were declared before pilot learning outcomes. A passing single learner would establish learnability of this development recipe, not an allocation benefit, a new mechanism or comparative superiority. A failed gate is retained without expanding the grid. Source-level preparation failures and amendments remain preserved. A separate fresh-seed comparison specification and complete published-method reproduction are still needed.
