# BERT allocation transfer diagnostic

Complete trajectories 1/20; complete private/head-only pairs 0/10. Partial attempts: [].

This transfer check replaces the backbone, representations, tokenizer, pooler and classifier. It does not isolate classifier design alone or compare against a tuned static BERT baseline. All deployment rules and both allocation controls are retained.

## Every allocation pair

|  |
|  |

## Descriptive cross-backbone accuracy differences

| architecture | rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| private | frozen_centroid | 0 | nan | nan | nan |
| private | last_active | 0 | nan | nan | nan |
| private | uniform_probability | 0 | nan | nan | nan |

## Every trajectory and prediction rule

| seed | order | architecture | rule | bert_macro_accuracy | distilbert_macro_accuracy | bert_minus_distilbert | updates | adapters | adaptation_parameters | maximum_training_texts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | private | frozen_centroid | 0.0293 | 0.1593 | -0.1299 | 80 | 3 | 1062375 | 510 |
| 2027 | canonical | private | last_active | 0.0237 | 0.1462 | -0.1226 | 80 | 3 | 1062375 | 510 |
| 2027 | canonical | private | uniform_probability | 0.0357 | 0.0860 | -0.0503 | 80 | 3 | 1062375 | 510 |

Intervals average both orders within each independent seed. The fixed development examples have been repeatedly examined; this is development evidence. Scope is the BANKING label-group stress test, the frozen training recipe and the declared memory budget. Neither allocation equivalence nor disagreement alone establishes competitive utility or a general capacity principle.
