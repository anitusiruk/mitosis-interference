# BERT allocation transfer diagnostic

Complete trajectories 12/20; complete private/head-only pairs 6/10. Partial attempts: [].

This transfer check replaces the backbone, representations, tokenizer, pooler and classifier. It does not isolate classifier design alone or compare against a tuned static BERT baseline. All deployment rules and both allocation controls are retained.

## Every allocation pair

| seed | order | allocation_disagreements | private_spawn_steps | head_only_spawn_steps | private_learning_updates | head_only_learning_updates |
| --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2027 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |

## Descriptive cross-backbone accuracy differences

| architecture | rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| head_only | frozen_centroid | 3 | -0.0652 | -0.1188 | -0.0116 |
| head_only | last_active | 3 | -0.0300 | -0.0854 | 0.0253 |
| head_only | uniform_probability | 3 | -0.0389 | -0.1712 | 0.0933 |
| private | frozen_centroid | 3 | -0.1095 | -0.1567 | -0.0624 |
| private | last_active | 3 | -0.0759 | -0.1058 | -0.0460 |
| private | uniform_probability | 3 | -0.0753 | -0.1477 | -0.0029 |

## Every trajectory and prediction rule

| seed | order | architecture | rule | bert_macro_accuracy | distilbert_macro_accuracy | bert_minus_distilbert | updates | adapters | adaptation_parameters | maximum_training_texts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | private | frozen_centroid | 0.0293 | 0.1593 | -0.1299 | 80 | 3 | 1062375 | 510 |
| 2027 | canonical | private | last_active | 0.0237 | 0.1462 | -0.1226 | 80 | 3 | 1062375 | 510 |
| 2027 | canonical | private | uniform_probability | 0.0357 | 0.0860 | -0.0503 | 80 | 3 | 1062375 | 510 |
| 2027 | canonical | head_only | frozen_centroid | 0.0590 | 0.1107 | -0.0517 | 80 | 3 | 1062375 | 510 |
| 2027 | canonical | head_only | last_active | 0.0387 | 0.0978 | -0.0591 | 80 | 3 | 1062375 | 510 |
| 2027 | canonical | head_only | uniform_probability | 0.0362 | 0.0137 | 0.0224 | 80 | 3 | 1062375 | 510 |
| 2027 | b_first | private | frozen_centroid | 0.0340 | 0.1532 | -0.1192 | 80 | 3 | 1062375 | 510 |
| 2027 | b_first | private | last_active | 0.0412 | 0.0641 | -0.0229 | 80 | 3 | 1062375 | 510 |
| 2027 | b_first | private | uniform_probability | 0.0435 | 0.0778 | -0.0342 | 80 | 3 | 1062375 | 510 |
| 2027 | b_first | head_only | frozen_centroid | 0.0570 | 0.0900 | -0.0330 | 80 | 3 | 1062375 | 510 |
| 2027 | b_first | head_only | last_active | 0.0493 | 0.0137 | 0.0355 | 80 | 3 | 1062375 | 510 |
| 2027 | b_first | head_only | uniform_probability | 0.0355 | 0.0137 | 0.0218 | 80 | 3 | 1062375 | 510 |
| 2028 | canonical | private | frozen_centroid | 0.0534 | 0.1824 | -0.1290 | 80 | 3 | 1062375 | 510 |
| 2028 | canonical | private | last_active | 0.0333 | 0.1247 | -0.0914 | 80 | 3 | 1062375 | 510 |
| 2028 | canonical | private | uniform_probability | 0.0323 | 0.1442 | -0.1120 | 80 | 3 | 1062375 | 510 |
| 2028 | canonical | head_only | frozen_centroid | 0.0336 | 0.1244 | -0.0907 | 80 | 3 | 1062375 | 510 |
| 2028 | canonical | head_only | last_active | 0.0398 | 0.0591 | -0.0194 | 80 | 3 | 1062375 | 510 |
| 2028 | canonical | head_only | uniform_probability | 0.0373 | 0.1219 | -0.0845 | 80 | 3 | 1062375 | 510 |
| 2028 | b_first | private | frozen_centroid | 0.0548 | 0.1022 | -0.0474 | 80 | 3 | 1062375 | 510 |
| 2028 | b_first | private | last_active | 0.0332 | 0.0733 | -0.0401 | 80 | 3 | 1062375 | 510 |
| 2028 | b_first | private | uniform_probability | 0.0368 | 0.0972 | -0.0603 | 80 | 3 | 1062375 | 510 |
| 2028 | b_first | head_only | frozen_centroid | 0.0574 | 0.1027 | -0.0453 | 80 | 3 | 1062375 | 510 |
| 2028 | b_first | head_only | last_active | 0.0447 | 0.0722 | -0.0275 | 80 | 3 | 1062375 | 510 |
| 2028 | b_first | head_only | uniform_probability | 0.0445 | 0.0864 | -0.0419 | 80 | 3 | 1062375 | 510 |
| 2029 | canonical | private | frozen_centroid | 0.0618 | 0.1902 | -0.1284 | 80 | 3 | 1062375 | 510 |
| 2029 | canonical | private | last_active | 0.0376 | 0.1129 | -0.0753 | 80 | 3 | 1062375 | 510 |
| 2029 | canonical | private | uniform_probability | 0.0478 | 0.1612 | -0.1134 | 80 | 3 | 1062375 | 510 |
| 2029 | canonical | head_only | frozen_centroid | 0.0526 | 0.1477 | -0.0950 | 80 | 3 | 1062375 | 510 |
| 2029 | canonical | head_only | last_active | 0.0355 | 0.1086 | -0.0731 | 80 | 3 | 1062375 | 510 |
| 2029 | canonical | head_only | uniform_probability | 0.0378 | 0.0933 | -0.0555 | 80 | 3 | 1062375 | 510 |
| 2029 | b_first | private | frozen_centroid | 0.0624 | 0.1657 | -0.1033 | 80 | 3 | 1062375 | 510 |
| 2029 | b_first | private | last_active | 0.0252 | 0.1283 | -0.1031 | 80 | 3 | 1062375 | 510 |
| 2029 | b_first | private | uniform_probability | 0.0327 | 0.1142 | -0.0814 | 80 | 3 | 1062375 | 510 |
| 2029 | b_first | head_only | frozen_centroid | 0.0546 | 0.1301 | -0.0754 | 80 | 3 | 1062375 | 510 |
| 2029 | b_first | head_only | last_active | 0.0458 | 0.0825 | -0.0367 | 80 | 3 | 1062375 | 510 |
| 2029 | b_first | head_only | uniform_probability | 0.0382 | 0.1340 | -0.0959 | 80 | 3 | 1062375 | 510 |

Intervals average both orders within each independent seed. The fixed development examples have been repeatedly examined; this is development evidence. Scope is the BANKING label-group stress test, the frozen training recipe and the declared memory budget. Neither allocation equivalence nor disagreement alone establishes competitive utility or a general capacity principle.
