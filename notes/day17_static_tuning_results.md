# Tuned fixed-capacity development baselines

Completed pilot trajectories: 6/24.

The full equal-budget learning-rate grid and its pilot-only selection rule were committed before tuning outcomes. Both ranks and all adaptive deployment rules are retained. Development examples and the adaptive reference outcomes were already examined; this is not untouched final evaluation.

## Every pilot

| run | rank | learning_rate | seed | order | final_macro_accuracy | updates |
| --- | --- | --- | --- | --- | --- | --- |
| day17_pilot_rank8_lr100_seed2026_b_first | 8 | 0.0001 | 2026 | b_first | 0.1089 | 80 |
| day17_pilot_rank8_lr100_seed2026_canonical | 8 | 0.0001 | 2026 | canonical | 0.1183 | 80 |
| day17_pilot_rank8_lr20_seed2026_b_first | 8 | 0.0000 | 2026 | b_first | 0.0412 | 80 |
| day17_pilot_rank8_lr20_seed2026_canonical | 8 | 0.0000 | 2026 | canonical | 0.0321 | 80 |
| day17_pilot_rank8_lr50_seed2026_b_first | 8 | 0.0001 | 2026 | b_first | 0.0602 | 80 |
| day17_pilot_rank8_lr50_seed2026_canonical | 8 | 0.0001 | 2026 | canonical | 0.0458 | 80 |

Completed paired-development static trajectories: 0/20; incomplete attempts: [].

Intervals are descriptive over paired training seeds and fixed development examples. Repeatedly evaluated orders, batches, and classes are not independent replicates. This is a learning-rate study, not exhaustive hyperparameter optimization. Static and adaptive models differ in classifier multiplicity and update/inference compute. Equal retained-text budgets are not universal resource matching. No modern named-method or final-test claim follows.
