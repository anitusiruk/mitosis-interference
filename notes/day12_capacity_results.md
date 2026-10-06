# Larger fixed-capacity baseline

Rank 96 was selected by parameter arithmetic before outcomes, near the storage of three rank-8 packages. It is a standard fixed-capacity alternative, not a named modern-method reproduction or universally parameter-matched algorithm. All predictors use the full 77-class label space. Official tests remain unused.

Completed trajectories 2/11; incomplete folders: [].

## Seed-cluster paired differences

| rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| frozen_centroid | rank96_minus_rank8 | 0 | nan | nan | nan |
| frozen_centroid | rank96_minus_adaptive | 0 | nan | nan | nan |
| last_active | rank96_minus_rank8 | 0 | nan | nan | nan |
| last_active | rank96_minus_adaptive | 0 | nan | nan | nan |
| uniform_probability | rank96_minus_rank8 | 0 | nan | nan | nan |
| uniform_probability | rank96_minus_adaptive | 0 | nan | nan | nan |

Both orders are averaged inside each fresh seed before descriptive Student-t intervals; seed 2026 is excluded. Fixed examples and this rank choice define the scope of these intervals.

## Actual resources and every run

| seed | order | rule | rank96_accuracy | rank8_single_accuracy | adaptive_accuracy | rank96_minus_rank8 | rank96_minus_adaptive | rank96_adaptation_parameters | adaptive_adaptation_parameters | adaptive_larger_than_rank96 | rank96_live_training_seconds | rank96_optimizer_bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | canonical | frozen_centroid | 0.0679 | 0.1693 | 0.1613 | -0.1014 | -0.0934 | 2419277 | 2391783 | False | 2.0514 | 19354328 |
| 2026 | canonical | last_active | 0.0679 | 0.1693 | 0.1022 | -0.1014 | -0.0343 | 2419277 | 2391783 | False | 2.0514 | 19354328 |
| 2026 | canonical | uniform_probability | 0.0679 | 0.1693 | 0.1222 | -0.1014 | -0.0543 | 2419277 | 2391783 | False | 2.0514 | 19354328 |
| 2027 | canonical | frozen_centroid | 0.0677 | 0.2131 | 0.1584 | -0.1454 | -0.0906 | 2419277 | 2391783 | False | 1.8808 | 19354328 |
| 2027 | canonical | last_active | 0.0677 | 0.2131 | 0.1462 | -0.1454 | -0.0785 | 2419277 | 2391783 | False | 1.8808 | 19354328 |
| 2027 | canonical | uniform_probability | 0.0677 | 0.2131 | 0.0860 | -0.1454 | -0.0183 | 2419277 | 2391783 | False | 1.8808 | 19354328 |

Growing pools store multiple classifier heads; rank 96 spends that budget on LoRA while retaining one head. Stored parameters, active-update compute, inference compute, and optimizer state are different resources. Report these differences instead of equating all of them. Modern source-faithful baseline reproductions and untouched final evaluation remain required.
