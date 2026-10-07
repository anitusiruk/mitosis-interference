# Tuned fixed-capacity development baselines

Completed pilot trajectories: 24/24.

The full equal-budget learning-rate grid and its pilot-only selection rule were committed before tuning outcomes. Both ranks and all adaptive deployment rules are retained. Development examples and the adaptive reference outcomes were already examined; this is not untouched final evaluation.

## Every pilot

| run | rank | learning_rate | seed | order | final_macro_accuracy | updates |
| --- | --- | --- | --- | --- | --- | --- |
| day17_pilot_rank8_lr100_seed2026_b_first | 8 | 0.0001 | 2026 | b_first | 0.1089 | 80 |
| day17_pilot_rank8_lr100_seed2026_canonical | 8 | 0.0001 | 2026 | canonical | 0.1183 | 80 |
| day17_pilot_rank8_lr200_seed2026_b_first | 8 | 0.0002 | 2026 | b_first | 0.2026 | 80 |
| day17_pilot_rank8_lr200_seed2026_canonical | 8 | 0.0002 | 2026 | canonical | 0.1693 | 80 |
| day17_pilot_rank8_lr20_seed2026_b_first | 8 | 0.0000 | 2026 | b_first | 0.0412 | 80 |
| day17_pilot_rank8_lr20_seed2026_canonical | 8 | 0.0000 | 2026 | canonical | 0.0321 | 80 |
| day17_pilot_rank8_lr400_seed2026_b_first | 8 | 0.0004 | 2026 | b_first | 0.1975 | 80 |
| day17_pilot_rank8_lr400_seed2026_canonical | 8 | 0.0004 | 2026 | canonical | 0.0355 | 80 |
| day17_pilot_rank8_lr50_seed2026_b_first | 8 | 0.0001 | 2026 | b_first | 0.0602 | 80 |
| day17_pilot_rank8_lr50_seed2026_canonical | 8 | 0.0001 | 2026 | canonical | 0.0458 | 80 |
| day17_pilot_rank8_lr800_seed2026_b_first | 8 | 0.0008 | 2026 | b_first | 0.0286 | 80 |
| day17_pilot_rank8_lr800_seed2026_canonical | 8 | 0.0008 | 2026 | canonical | 0.0398 | 80 |
| day17_pilot_rank96_lr100_seed2026_b_first | 96 | 0.0001 | 2026 | b_first | 0.1965 | 80 |
| day17_pilot_rank96_lr100_seed2026_canonical | 96 | 0.0001 | 2026 | canonical | 0.1013 | 80 |
| day17_pilot_rank96_lr200_seed2026_b_first | 96 | 0.0002 | 2026 | b_first | 0.0286 | 80 |
| day17_pilot_rank96_lr200_seed2026_canonical | 96 | 0.0002 | 2026 | canonical | 0.0679 | 80 |
| day17_pilot_rank96_lr20_seed2026_b_first | 96 | 0.0000 | 2026 | b_first | 0.0335 | 80 |
| day17_pilot_rank96_lr20_seed2026_canonical | 96 | 0.0000 | 2026 | canonical | 0.0477 | 80 |
| day17_pilot_rank96_lr400_seed2026_b_first | 96 | 0.0004 | 2026 | b_first | 0.0412 | 80 |
| day17_pilot_rank96_lr400_seed2026_canonical | 96 | 0.0004 | 2026 | canonical | 0.0301 | 80 |
| day17_pilot_rank96_lr50_seed2026_b_first | 96 | 0.0001 | 2026 | b_first | 0.0547 | 80 |
| day17_pilot_rank96_lr50_seed2026_canonical | 96 | 0.0001 | 2026 | canonical | 0.0481 | 80 |
| day17_pilot_rank96_lr800_seed2026_b_first | 96 | 0.0008 | 2026 | b_first | 0.0355 | 80 |
| day17_pilot_rank96_lr800_seed2026_canonical | 96 | 0.0008 | 2026 | canonical | 0.0301 | 80 |

## Frozen pilot selection

| rank | learning_rate | pilot_accuracy_mean |
| --- | --- | --- |
| 8 | 0.0000 | 0.0366 |
| 8 | 0.0001 | 0.0530 |
| 8 | 0.0001 | 0.1136 |
| 8 | 0.0002 | 0.1859 |
| 8 | 0.0004 | 0.1165 |
| 8 | 0.0008 | 0.0342 |
| 96 | 0.0000 | 0.0406 |
| 96 | 0.0001 | 0.0514 |
| 96 | 0.0001 | 0.1489 |
| 96 | 0.0002 | 0.0483 |
| 96 | 0.0004 | 0.0357 |
| 96 | 0.0008 | 0.0328 |

Selected rates: {"8": 0.0002, "96": 0.0001}.

Completed paired-development static trajectories: 11/20; incomplete attempts: [].

## Every rule and rank

| rank | adaptive_rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| 8 | frozen_centroid | 3 | 0.0145 | -0.0323 | 0.0613 |
| 8 | last_active | 3 | -0.0360 | -0.0856 | 0.0136 |
| 8 | linear_hard | 3 | 0.0761 | 0.0373 | 0.1148 |
| 8 | linear_probability_mixture | 3 | 0.0770 | 0.0449 | 0.1091 |
| 8 | uniform_probability | 3 | -0.0308 | -0.1414 | 0.0797 |
| 96 | frozen_centroid | 2 | 0.0562 | -0.1103 | 0.2228 |
| 96 | last_active | 2 | 0.0091 | -0.2068 | 0.2250 |
| 96 | linear_hard | 2 | 0.1155 | 0.0199 | 0.2111 |
| 96 | linear_probability_mixture | 2 | 0.1175 | 0.0953 | 0.1397 |
| 96 | uniform_probability | 2 | 0.0083 | -0.4934 | 0.5100 |

## Every trajectory and actual resource count

| rank | learning_rate | seed | order | adaptive_rule | static_accuracy | adaptive_accuracy | adaptive_minus_static | static_adaptation_parameters | adaptive_adaptation_parameters | static_optimizer_bytes | adaptive_optimizer_bytes | static_training_texts | adaptive_training_texts | static_training_seconds | static_evaluation_seconds | static_gpu_peak_allocated_bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 0.0002 | 2027 | b_first | frozen_centroid | 0.1136 | 0.1532 | 0.0396 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2988 | 4.6516 | 538011648 |
| 8 | 0.0002 | 2027 | b_first | last_active | 0.1136 | 0.0641 | -0.0495 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2988 | 4.6516 | 538011648 |
| 8 | 0.0002 | 2027 | b_first | linear_hard | 0.1136 | 0.2180 | 0.1044 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2988 | 4.6516 | 538011648 |
| 8 | 0.0002 | 2027 | b_first | linear_probability_mixture | 0.1136 | 0.2114 | 0.0978 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2988 | 4.6516 | 538011648 |
| 8 | 0.0002 | 2027 | b_first | uniform_probability | 0.1136 | 0.0778 | -0.0358 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2988 | 4.6516 | 538011648 |
| 8 | 0.0002 | 2027 | canonical | frozen_centroid | 0.2131 | 0.1593 | -0.0538 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2570 | 4.6091 | 538142720 |
| 8 | 0.0002 | 2027 | canonical | last_active | 0.2131 | 0.1462 | -0.0669 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2570 | 4.6091 | 538142720 |
| 8 | 0.0002 | 2027 | canonical | linear_hard | 0.2131 | 0.2542 | 0.0411 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2570 | 4.6091 | 538142720 |
| 8 | 0.0002 | 2027 | canonical | linear_probability_mixture | 0.2131 | 0.2532 | 0.0401 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2570 | 4.6091 | 538142720 |
| 8 | 0.0002 | 2027 | canonical | uniform_probability | 0.2131 | 0.0860 | -0.1271 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.2570 | 4.6091 | 538142720 |
| 8 | 0.0002 | 2028 | b_first | frozen_centroid | 0.1550 | 0.1022 | -0.0528 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1206 | 4.6986 | 501880832 |
| 8 | 0.0002 | 2028 | b_first | last_active | 0.1550 | 0.0733 | -0.0817 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1206 | 4.6986 | 501880832 |
| 8 | 0.0002 | 2028 | b_first | linear_hard | 0.1550 | 0.1354 | -0.0196 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1206 | 4.6986 | 501880832 |
| 8 | 0.0002 | 2028 | b_first | linear_probability_mixture | 0.1550 | 0.1398 | -0.0151 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1206 | 4.6986 | 501880832 |
| 8 | 0.0002 | 2028 | b_first | uniform_probability | 0.1550 | 0.0972 | -0.0578 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1206 | 4.6986 | 501880832 |
| 8 | 0.0002 | 2028 | canonical | frozen_centroid | 0.0820 | 0.1824 | 0.1004 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.3579 | 4.7148 | 500406272 |
| 8 | 0.0002 | 2028 | canonical | last_active | 0.0820 | 0.1247 | 0.0428 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.3579 | 4.7148 | 500406272 |
| 8 | 0.0002 | 2028 | canonical | linear_hard | 0.0820 | 0.2264 | 0.1444 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.3579 | 4.7148 | 500406272 |
| 8 | 0.0002 | 2028 | canonical | linear_probability_mixture | 0.0820 | 0.2375 | 0.1555 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.3579 | 4.7148 | 500406272 |
| 8 | 0.0002 | 2028 | canonical | uniform_probability | 0.0820 | 0.1442 | 0.0623 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.3579 | 4.7148 | 500406272 |
| 8 | 0.0002 | 2029 | b_first | frozen_centroid | 0.0820 | 0.1657 | 0.0837 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.0740 | 4.6337 | 538339328 |
| 8 | 0.0002 | 2029 | b_first | last_active | 0.0820 | 0.1283 | 0.0463 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.0740 | 4.6337 | 538339328 |
| 8 | 0.0002 | 2029 | b_first | linear_hard | 0.0820 | 0.2313 | 0.1493 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.0740 | 4.6337 | 538339328 |
| 8 | 0.0002 | 2029 | b_first | linear_probability_mixture | 0.0820 | 0.2272 | 0.1452 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.0740 | 4.6337 | 538339328 |
| 8 | 0.0002 | 2029 | b_first | uniform_probability | 0.0820 | 0.1142 | 0.0322 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.0740 | 4.6337 | 538339328 |
| 8 | 0.0002 | 2029 | canonical | frozen_centroid | 0.2200 | 0.1902 | -0.0298 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1874 | 4.5880 | 538142720 |
| 8 | 0.0002 | 2029 | canonical | last_active | 0.2200 | 0.1129 | -0.1071 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1874 | 4.5880 | 538142720 |
| 8 | 0.0002 | 2029 | canonical | linear_hard | 0.2200 | 0.2568 | 0.0368 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1874 | 4.5880 | 538142720 |
| 8 | 0.0002 | 2029 | canonical | linear_probability_mixture | 0.2200 | 0.2587 | 0.0386 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1874 | 4.5880 | 538142720 |
| 8 | 0.0002 | 2029 | canonical | uniform_probability | 0.2200 | 0.1612 | -0.0588 | 797261 | 2391783 | 6378200 | 19134600 | 512 | 510 | 2.1874 | 4.5880 | 538142720 |
| 96 | 0.0001 | 2027 | b_first | frozen_centroid | 0.0624 | 0.1532 | 0.0908 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.0673 | 4.6642 | 561801216 |
| 96 | 0.0001 | 2027 | b_first | last_active | 0.0624 | 0.0641 | 0.0018 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.0673 | 4.6642 | 561801216 |
| 96 | 0.0001 | 2027 | b_first | linear_hard | 0.0624 | 0.2180 | 0.1556 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.0673 | 4.6642 | 561801216 |
| 96 | 0.0001 | 2027 | b_first | linear_probability_mixture | 0.0624 | 0.2114 | 0.1490 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.0673 | 4.6642 | 561801216 |
| 96 | 0.0001 | 2027 | b_first | uniform_probability | 0.0624 | 0.0778 | 0.0154 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.0673 | 4.6642 | 561801216 |
| 96 | 0.0001 | 2027 | canonical | frozen_centroid | 0.1638 | 0.1593 | -0.0046 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.1635 | 4.6456 | 561932288 |
| 96 | 0.0001 | 2027 | canonical | last_active | 0.1638 | 0.1462 | -0.0176 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.1635 | 4.6456 | 561932288 |
| 96 | 0.0001 | 2027 | canonical | linear_hard | 0.1638 | 0.2542 | 0.0904 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.1635 | 4.6456 | 561932288 |
| 96 | 0.0001 | 2027 | canonical | linear_probability_mixture | 0.1638 | 0.2532 | 0.0894 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.1635 | 4.6456 | 561932288 |
| 96 | 0.0001 | 2027 | canonical | uniform_probability | 0.1638 | 0.0860 | -0.0778 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.1635 | 4.6456 | 561932288 |
| 96 | 0.0001 | 2028 | b_first | frozen_centroid | 0.0989 | 0.1022 | 0.0032 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2743 | 4.8517 | 524994560 |
| 96 | 0.0001 | 2028 | b_first | last_active | 0.0989 | 0.0733 | -0.0256 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2743 | 4.8517 | 524994560 |
| 96 | 0.0001 | 2028 | b_first | linear_hard | 0.0989 | 0.1354 | 0.0365 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2743 | 4.8517 | 524994560 |
| 96 | 0.0001 | 2028 | b_first | linear_probability_mixture | 0.0989 | 0.1398 | 0.0409 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2743 | 4.8517 | 524994560 |
| 96 | 0.0001 | 2028 | b_first | uniform_probability | 0.0989 | 0.0972 | -0.0017 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2743 | 4.8517 | 524994560 |
| 96 | 0.0001 | 2028 | canonical | frozen_centroid | 0.0470 | 0.1824 | 0.1354 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2546 | 4.7359 | 523520000 |
| 96 | 0.0001 | 2028 | canonical | last_active | 0.0470 | 0.1247 | 0.0778 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2546 | 4.7359 | 523520000 |
| 96 | 0.0001 | 2028 | canonical | linear_hard | 0.0470 | 0.2264 | 0.1794 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2546 | 4.7359 | 523520000 |
| 96 | 0.0001 | 2028 | canonical | linear_probability_mixture | 0.0470 | 0.2375 | 0.1905 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2546 | 4.7359 | 523520000 |
| 96 | 0.0001 | 2028 | canonical | uniform_probability | 0.0470 | 0.1442 | 0.0973 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.2546 | 4.7359 | 523520000 |
| 96 | 0.0001 | 2029 | canonical | frozen_centroid | 0.1317 | 0.1902 | 0.0585 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.3310 | 4.6636 | 561932288 |
| 96 | 0.0001 | 2029 | canonical | last_active | 0.1317 | 0.1129 | -0.0188 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.3310 | 4.6636 | 561932288 |
| 96 | 0.0001 | 2029 | canonical | linear_hard | 0.1317 | 0.2568 | 0.1251 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.3310 | 4.6636 | 561932288 |
| 96 | 0.0001 | 2029 | canonical | linear_probability_mixture | 0.1317 | 0.2587 | 0.1269 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.3310 | 4.6636 | 561932288 |
| 96 | 0.0001 | 2029 | canonical | uniform_probability | 0.1317 | 0.1612 | 0.0295 | 2419277 | 2391783 | 19354328 | 19134600 | 512 | 510 | 2.3310 | 4.6636 | 561932288 |

Intervals are descriptive over paired training seeds and fixed development examples. Repeatedly evaluated orders, batches, and classes are not independent replicates. This is a learning-rate study, not exhaustive hyperparameter optimization. Static and adaptive models differ in classifier multiplicity and update/inference compute. Equal retained-text budgets are not universal resource matching. No modern named-method or final-test claim follows.
