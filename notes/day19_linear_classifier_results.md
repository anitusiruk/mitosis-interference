# Frozen hidden pre-classifier allocation diagnostic

Completed trajectories 1/20; paired controls 0/10. Incomplete attempts: [].

Both controls use the same DistilBERT backbone and fixed hidden pre-classifier. The private condition trains LoRA and the linear output classifier; the other trains only the output classifier, keeping LoRA output zero. This removes hidden pre-classifier learning, with its associated optimizer state, in both conditions. It is an allocation diagnostic, not a tuned competitive benchmark. The retained PEFT pre-classifier copies are dormant stored parameters.

## Every allocation pair

|  |
|  |

## All deviations from the trainable-stack reference and stored resources

| seed | order | architecture | allocation_disagreements_vs_trainable_stack | spawn_steps | learning_updates | adapters | stored_lora_parameters | stored_output_classifier_parameters | stored_frozen_preclassifier_parameters | optimizer_bytes | maximum_training_texts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | private | 0 | [18, 50] | 80 | 3 | 442368 | 177639 | 1771776 | 4960368 | 510 |

## All private-minus-output-classifier-only accuracy differences

| rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- |

## Every deployment outcome

| seed | order | architecture | rule | final_macro_accuracy |
| --- | --- | --- | --- | --- |
| 2027 | canonical | private | frozen_centroid | 0.0433 |
| 2027 | canonical | private | last_active | 0.0473 |
| 2027 | canonical | private | uniform_probability | 0.0137 |

Intervals are descriptive over paired training seeds and fixed repeatedly examined development examples. Neither agreement nor disagreement establishes a universal capacity principle. Existing controls with trainable hidden classifiers must not be described as having no learned hidden representation capacity.
