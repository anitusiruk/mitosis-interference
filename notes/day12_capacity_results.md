# Larger fixed-capacity baseline

Rank 96 was selected by parameter arithmetic before outcomes, near the storage of three rank-8 packages. It is a standard fixed-capacity alternative, not a named modern-method reproduction or universally parameter-matched algorithm. All predictors use the full 77-class label space. Official tests remain unused.

Completed trajectories 11/11; incomplete folders: [].

## Seed-cluster paired differences

| rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| frozen_centroid | rank96_minus_rank8 | 5 | -0.0946 | -0.1406 | -0.0486 |
| frozen_centroid | rank96_minus_adaptive | 5 | -0.0892 | -0.1235 | -0.0549 |
| last_active | rank96_minus_rank8 | 5 | -0.0946 | -0.1406 | -0.0486 |
| last_active | rank96_minus_adaptive | 5 | -0.0345 | -0.0755 | 0.0066 |
| uniform_probability | rank96_minus_rank8 | 5 | -0.0946 | -0.1406 | -0.0486 |
| uniform_probability | rank96_minus_adaptive | 5 | -0.0611 | -0.0900 | -0.0323 |

Both orders are averaged inside each fresh seed before descriptive Student-t intervals; seed 2026 is excluded. Fixed examples and this rank choice define the scope of these intervals.

## Actual resources and every run

| seed | order | rule | rank96_accuracy | rank8_single_accuracy | adaptive_accuracy | rank96_minus_rank8 | rank96_minus_adaptive | rank96_adaptation_parameters | adaptive_adaptation_parameters | adaptive_larger_than_rank96 | rank96_live_training_seconds | rank96_optimizer_bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | canonical | frozen_centroid | 0.0679 | 0.1693 | 0.1613 | -0.1014 | -0.0934 | 2419277 | 2391783 | False | 2.0514 | 19354328 |
| 2026 | canonical | last_active | 0.0679 | 0.1693 | 0.1022 | -0.1014 | -0.0343 | 2419277 | 2391783 | False | 2.0514 | 19354328 |
| 2026 | canonical | uniform_probability | 0.0679 | 0.1693 | 0.1222 | -0.1014 | -0.0543 | 2419277 | 2391783 | False | 2.0514 | 19354328 |
| 2027 | b_first | frozen_centroid | 0.0183 | 0.1136 | 0.1423 | -0.0953 | -0.1240 | 2419277 | 2391783 | False | 2.3555 | 19354328 |
| 2027 | b_first | last_active | 0.0183 | 0.1136 | 0.0641 | -0.0953 | -0.0458 | 2419277 | 2391783 | False | 2.3555 | 19354328 |
| 2027 | b_first | uniform_probability | 0.0183 | 0.1136 | 0.0778 | -0.0953 | -0.0594 | 2419277 | 2391783 | False | 2.3555 | 19354328 |
| 2027 | canonical | frozen_centroid | 0.0677 | 0.2131 | 0.1584 | -0.1454 | -0.0906 | 2419277 | 2391783 | False | 1.8808 | 19354328 |
| 2027 | canonical | last_active | 0.0677 | 0.2131 | 0.1462 | -0.1454 | -0.0785 | 2419277 | 2391783 | False | 1.8808 | 19354328 |
| 2027 | canonical | uniform_probability | 0.0677 | 0.2131 | 0.0860 | -0.1454 | -0.0183 | 2419277 | 2391783 | False | 1.8808 | 19354328 |
| 2028 | b_first | frozen_centroid | 0.0355 | 0.1550 | 0.1043 | -0.1195 | -0.0688 | 2419277 | 2391783 | False | 2.2008 | 19354328 |
| 2028 | b_first | last_active | 0.0355 | 0.1550 | 0.0733 | -0.1195 | -0.0378 | 2419277 | 2391783 | False | 2.2008 | 19354328 |
| 2028 | b_first | uniform_probability | 0.0355 | 0.1550 | 0.0972 | -0.1195 | -0.0617 | 2419277 | 2391783 | False | 2.2008 | 19354328 |
| 2028 | canonical | frozen_centroid | 0.0237 | 0.0820 | 0.1750 | -0.0583 | -0.1513 | 2419277 | 2391783 | False | 2.2241 | 19354328 |
| 2028 | canonical | last_active | 0.0237 | 0.0820 | 0.1247 | -0.0583 | -0.1011 | 2419277 | 2391783 | False | 2.2241 | 19354328 |
| 2028 | canonical | uniform_probability | 0.0237 | 0.0820 | 0.1442 | -0.0583 | -0.1206 | 2419277 | 2391783 | False | 2.2241 | 19354328 |
| 2029 | b_first | frozen_centroid | 0.1443 | 0.0820 | 0.1602 | 0.0624 | -0.0159 | 2419277 | 2391783 | False | 2.2623 | 19354328 |
| 2029 | b_first | last_active | 0.1443 | 0.0820 | 0.1283 | 0.0624 | 0.0160 | 2419277 | 2391783 | False | 2.2623 | 19354328 |
| 2029 | b_first | uniform_probability | 0.1443 | 0.0820 | 0.1142 | 0.0624 | 0.0302 | 2419277 | 2391783 | False | 2.2623 | 19354328 |
| 2029 | canonical | frozen_centroid | 0.0584 | 0.2200 | 0.1942 | -0.1616 | -0.1358 | 2419277 | 2391783 | False | 2.0321 | 19354328 |
| 2029 | canonical | last_active | 0.0584 | 0.2200 | 0.1129 | -0.1616 | -0.0545 | 2419277 | 2391783 | False | 2.0321 | 19354328 |
| 2029 | canonical | uniform_probability | 0.0584 | 0.2200 | 0.1612 | -0.1616 | -0.1028 | 2419277 | 2391783 | False | 2.0321 | 19354328 |
| 2030 | b_first | frozen_centroid | 0.0550 | 0.1513 | 0.1772 | -0.0963 | -0.1222 | 2419277 | 2391783 | False | 2.2395 | 19354328 |
| 2030 | b_first | last_active | 0.0550 | 0.1513 | 0.1397 | -0.0963 | -0.0848 | 2419277 | 2391783 | False | 2.2395 | 19354328 |
| 2030 | b_first | uniform_probability | 0.0550 | 0.1513 | 0.2052 | -0.0963 | -0.1502 | 2419277 | 2391783 | False | 2.2395 | 19354328 |
| 2030 | canonical | frozen_centroid | 0.1882 | 0.2359 | 0.1589 | -0.0477 | 0.0292 | 2419277 | 2391783 | False | 2.2260 | 19354328 |
| 2030 | canonical | last_active | 0.1882 | 0.2359 | 0.0796 | -0.0477 | 0.1086 | 2419277 | 2391783 | False | 2.2260 | 19354328 |
| 2030 | canonical | uniform_probability | 0.1882 | 0.2359 | 0.1776 | -0.0477 | 0.0106 | 2419277 | 2391783 | False | 2.2260 | 19354328 |
| 2031 | b_first | frozen_centroid | 0.0367 | 0.1616 | 0.1656 | -0.1249 | -0.1289 | 2419277 | 2391783 | False | 2.2435 | 19354328 |
| 2031 | b_first | last_active | 0.0367 | 0.1616 | 0.1054 | -0.1249 | -0.0687 | 2419277 | 2391783 | False | 2.2435 | 19354328 |
| 2031 | b_first | uniform_probability | 0.0367 | 0.1616 | 0.1296 | -0.1249 | -0.0929 | 2419277 | 2391783 | False | 2.2435 | 19354328 |
| 2031 | canonical | frozen_centroid | 0.0705 | 0.2298 | 0.1543 | -0.1593 | -0.0838 | 2419277 | 2391783 | False | 2.2279 | 19354328 |
| 2031 | canonical | last_active | 0.0705 | 0.2298 | 0.0688 | -0.1593 | 0.0017 | 2419277 | 2391783 | False | 2.2279 | 19354328 |
| 2031 | canonical | uniform_probability | 0.0705 | 0.2298 | 0.1167 | -0.1593 | -0.0463 | 2419277 | 2391783 | False | 2.2279 | 19354328 |

Growing pools store multiple classifier heads; rank 96 spends that budget on LoRA while retaining one head. Stored parameters, active-update compute, inference compute, and optimizer state are different resources. Report these differences instead of equating all of them. Modern source-faithful baseline reproductions and untouched final evaluation remain required.
