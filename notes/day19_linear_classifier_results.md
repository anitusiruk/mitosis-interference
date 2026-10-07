# Frozen hidden pre-classifier allocation diagnostic

Completed trajectories 9/20; paired controls 4/10. Incomplete attempts: [].

Both controls use the same DistilBERT backbone and fixed hidden pre-classifier. The private condition trains LoRA and the linear output classifier; the other trains only the output classifier, keeping LoRA output zero. This removes hidden pre-classifier learning, with its associated optimizer state, in both conditions. It is an allocation diagnostic, not a tuned competitive benchmark. The retained PEFT pre-classifier copies are dormant stored parameters.

## Every allocation pair

| seed | order | allocation_disagreements | private_spawn_steps | head_only_spawn_steps | private_learning_updates | head_only_learning_updates |
| --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2027 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |

## All deviations from the trainable-stack reference and stored resources

| seed | order | architecture | allocation_disagreements_vs_trainable_stack | spawn_steps | learning_updates | adapters | stored_lora_parameters | stored_output_classifier_parameters | stored_frozen_preclassifier_parameters | optimizer_bytes | maximum_training_texts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | private | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 4960368 | 510 |
| 2027 | canonical | head_only | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 1421136 | 510 |
| 2027 | b_first | private | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 4960368 | 510 |
| 2027 | b_first | head_only | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 1421136 | 510 |
| 2028 | canonical | private | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 4960368 | 510 |
| 2028 | canonical | head_only | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 1421136 | 510 |
| 2028 | b_first | private | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 4960368 | 510 |
| 2028 | b_first | head_only | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 1421136 | 510 |
| 2029 | canonical | private | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 4960368 | 510 |

## All private-minus-output-classifier-only accuracy differences

| rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- |
| frozen_centroid | 2 | -0.0038 | -0.0167 | 0.0091 |
| last_active | 2 | 0.0013 | -0.0552 | 0.0578 |
| uniform_probability | 2 | -0.0029 | -0.0035 | -0.0023 |

## Every deployment outcome

| seed | order | architecture | rule | final_macro_accuracy |
| --- | --- | --- | --- | --- |
| 2027 | canonical | private | frozen_centroid | 0.0433 |
| 2027 | canonical | private | last_active | 0.0473 |
| 2027 | canonical | private | uniform_probability | 0.0137 |
| 2027 | canonical | head_only | frozen_centroid | 0.0491 |
| 2027 | canonical | head_only | last_active | 0.0301 |
| 2027 | canonical | head_only | uniform_probability | 0.0183 |
| 2027 | b_first | private | frozen_centroid | 0.0601 |
| 2027 | b_first | private | last_active | 0.0149 |
| 2027 | b_first | private | uniform_probability | 0.0137 |
| 2027 | b_first | head_only | frozen_centroid | 0.0638 |
| 2027 | b_first | head_only | last_active | 0.0206 |
| 2027 | b_first | head_only | uniform_probability | 0.0149 |
| 2028 | canonical | private | frozen_centroid | 0.0524 |
| 2028 | canonical | private | last_active | 0.0312 |
| 2028 | canonical | private | uniform_probability | 0.0333 |
| 2028 | canonical | head_only | frozen_centroid | 0.0569 |
| 2028 | canonical | head_only | last_active | 0.0398 |
| 2028 | canonical | head_only | uniform_probability | 0.0344 |
| 2028 | b_first | private | frozen_centroid | 0.0565 |
| 2028 | b_first | private | last_active | 0.0401 |
| 2028 | b_first | private | uniform_probability | 0.0345 |
| 2028 | b_first | head_only | frozen_centroid | 0.0575 |
| 2028 | b_first | head_only | last_active | 0.0378 |
| 2028 | b_first | head_only | uniform_probability | 0.0393 |
| 2029 | canonical | private | frozen_centroid | 0.0611 |
| 2029 | canonical | private | last_active | 0.0333 |
| 2029 | canonical | private | uniform_probability | 0.0323 |

Intervals are descriptive over paired training seeds and fixed repeatedly examined development examples. Neither agreement nor disagreement establishes a universal capacity principle. Existing controls with trainable hidden classifiers must not be described as having no learned hidden representation capacity.
