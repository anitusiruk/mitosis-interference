# BERT allocation transfer diagnostic

Complete trajectories 3/20; complete private/head-only pairs 1/10. Partial attempts: [].

This transfer check replaces the backbone, representations, tokenizer, pooler and classifier. It does not isolate classifier design alone or compare against a tuned static BERT baseline. All deployment rules and both allocation controls are retained.

## Every allocation pair

| seed | order | allocation_disagreements | private_spawn_steps | head_only_spawn_steps | private_learning_updates | head_only_learning_updates |
| --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |

## Descriptive cross-backbone accuracy differences

| architecture | rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| head_only | frozen_centroid | 0 | nan | nan | nan |
| head_only | last_active | 0 | nan | nan | nan |
| head_only | uniform_probability | 0 | nan | nan | nan |
| private | frozen_centroid | 1 | -0.1246 | nan | nan |
| private | last_active | 1 | -0.0727 | nan | nan |
| private | uniform_probability | 1 | -0.0423 | nan | nan |

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

Intervals average both orders within each independent seed. The fixed development examples have been repeatedly examined; this is development evidence. Scope is the BANKING label-group stress test, the frozen training recipe and the declared memory budget. Neither allocation equivalence nor disagreement alone establishes competitive utility or a general capacity principle.
