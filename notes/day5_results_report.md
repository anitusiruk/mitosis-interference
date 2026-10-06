# Day-5 development audit results

Seed 2026 only. Descriptive measurements, not independent replications. Oracle and restricted accuracies are diagnostic; label-free full-label-space metrics are reported separately. No official test data were used.

## day5_amazon_private_cau_seed2026

Status: summary recorded.
Completed steps: 80. Learned batches: 79. Decisions: {'warmup': 4, 'reuse': 75, 'defer': 1}. Final pool: 1.

Spawns: none.

Selected guarded reuse updates: 75; positive measured mean protected loss increase admitted: 15. Maximum measured mean harm: 0.00672922. This is an empirical probe statistic, not a formal retention guarantee.

Factorial contrasts: positive values favor the named intervention. These are means over dependent development windows; no confidence intervals are attached.

| segment | new_lora_gain_inherited_head | fresh_head_gain_reused_lora | new_lora_gain_fresh_head | joint_package_gain | new_lora_gain_common_frozen_head | retained_optimizer_gain |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | -0.001983 | -0.030044 | -0.001173 | -0.031218 | -0.001953 | -0.003460 |
| B1 | -0.033179 | -0.109859 | -0.004561 | -0.114420 | -0.032070 | 0.011042 |
| A2 | -0.153131 | -0.292879 | -0.027246 | -0.320124 | -0.152802 | -0.001592 |
| C1 | -0.148060 | -0.247157 | -0.036477 | -0.283634 | -0.151481 | 0.008534 |
| B2 | -0.156797 | -0.277534 | -0.041458 | -0.318991 | -0.154401 | 0.010967 |

Active-source one-step utility sign changed by resetting all optimizer state: 17/76 windows. This is not a count of full-policy allocation reversals.

Final recorded label-free full-space development accuracy:

| concept | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- |
| A | 0.8750 | 0.8750 | 0.8750 |
| B | 0.8906 | 0.8906 | 0.8906 |
| C | 0.7969 | 0.7969 | 0.7969 |

Macro accuracy over already observed concepts: frozen_centroid=0.8542, last_active=0.8542, uniform_probability=0.8542.

Timings separate method execution from the extra attribution and evaluation probes:

```json
{
  "component_audit_seconds": 243.738349981606,
  "live_training_seconds": 46.841760132461786,
  "evaluation_seconds": 2.8454120475798845
}
```

Paired frozen Day-4 routing reproduction check: 0 disagreements over 80 comparable steps.

## day5_amazon_private_single_seed2026

Status: summary recorded.
Completed steps: 80. Learned batches: 80. Decisions: {'single_update': 80}. Final pool: 1.

Spawns: none.

Final recorded label-free full-space development accuracy:

| concept | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- |
| A | 0.8672 | 0.8672 | 0.8672 |
| B | 0.8828 | 0.8828 | 0.8828 |
| C | 0.8047 | 0.8047 | 0.8047 |

Macro accuracy over already observed concepts: frozen_centroid=0.8516, last_active=0.8516, uniform_probability=0.8516.

Timings separate method execution from the extra attribution and evaluation probes:

```json
{
  "component_audit_seconds": 0.0,
  "live_training_seconds": 2.309300057590008,
  "evaluation_seconds": 2.8991800267249346
}
```

## day5_amazon_shared_cau_seed2026

Status: summary recorded.
Completed steps: 80. Learned batches: 79. Decisions: {'warmup': 4, 'reuse': 75, 'defer': 1}. Final pool: 1.

Spawns: none.

Selected guarded reuse updates: 75; positive measured mean protected loss increase admitted: 15. Maximum measured mean harm: 0.00672922. This is an empirical probe statistic, not a formal retention guarantee.

Final recorded label-free full-space development accuracy:

| concept | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- |
| A | 0.8750 | 0.8750 | 0.8750 |
| B | 0.8906 | 0.8906 | 0.8906 |
| C | 0.7969 | 0.7969 | 0.7969 |

Macro accuracy over already observed concepts: frozen_centroid=0.8542, last_active=0.8542, uniform_probability=0.8542.

Timings separate method execution from the extra attribution and evaluation probes:

```json
{
  "component_audit_seconds": 0.0,
  "live_training_seconds": 35.68940112553537,
  "evaluation_seconds": 2.8422590531408787
}
```

## day5_banking_head_only_cau_seed2026

Status: summary recorded.
Completed steps: 80. Learned batches: 80. Decisions: {'warmup': 10, 'reuse': 68, 'spawn': 2}. Final pool: 3.

Spawns: [{"step":18,"segment":"B1","adapter":"adapter_1"},{"step":50,"segment":"C1","adapter":"adapter_2"}].

Selected guarded reuse updates: 68; positive measured mean protected loss increase admitted: 0. Maximum measured mean harm: -0.0316887. This is an empirical probe statistic, not a formal retention guarantee.

Final recorded label-free full-space development accuracy:

| concept | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- |
| A | 0.1615 | 0.0000 | 0.0103 |
| B | 0.1097 | 0.2323 | 0.2032 |
| C | 0.1026 | 0.0000 | 0.0000 |

Macro accuracy over already observed concepts: frozen_centroid=0.1246, last_active=0.0774, uniform_probability=0.0712.

Timings separate method execution from the extra attribution and evaluation probes:

```json
{
  "component_audit_seconds": 0.0,
  "live_training_seconds": 35.961955927312374,
  "evaluation_seconds": 7.787906605750322
}
```

## day5_banking_private_cau_seed2026

Status: summary recorded.
Completed steps: 80. Learned batches: 80. Decisions: {'warmup': 10, 'reuse': 68, 'spawn': 2}. Final pool: 3.

Spawns: [{"step":18,"segment":"B1","adapter":"adapter_1"},{"step":50,"segment":"C1","adapter":"adapter_2"}].

Selected guarded reuse updates: 68; positive measured mean protected loss increase admitted: 0. Maximum measured mean harm: -0.0130035. This is an empirical probe statistic, not a formal retention guarantee.

Factorial contrasts: positive values favor the named intervention. These are means over dependent development windows; no confidence intervals are attached.

| segment | new_lora_gain_inherited_head | fresh_head_gain_reused_lora | new_lora_gain_fresh_head | joint_package_gain | new_lora_gain_common_frozen_head | retained_optimizer_gain |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | -0.059591 | -0.555188 | -0.009514 | -0.564703 | -0.054217 | 0.017561 |
| B1 | -0.034676 | -0.433528 | -0.011045 | -0.444572 | -0.031704 | -0.008090 |
| A2 | -0.341016 | -1.521827 | -0.050059 | -1.571886 | -0.345299 | 0.001786 |
| C1 | 0.085987 | -0.220403 | -0.016997 | -0.237401 | 0.084865 | -0.022232 |
| B2 | -0.339116 | -1.559199 | -0.056639 | -1.615838 | -0.345108 | 0.011177 |

Matched active-source contrasts at the actual spawn windows (not a best-adapter attribution):

| step | segment | source_adapter | new_lora_gain_inherited_head | fresh_head_gain_reused_lora | new_lora_gain_fresh_head | joint_package_gain | new_lora_gain_common_frozen_head | retained_optimizer_gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 18 | B1 | default | 0.124856 | 0.404217 | -0.007501 | 0.396715 | 0.111663 | -0.093136 |
| 50 | C1 | adapter_1 | 0.137778 | 0.520982 | -0.028679 | 0.492303 | 0.127340 | -0.127707 |

A fresh LoRA factor also resets its optimizer moments; a fresh head factor resets its head moments. These contrasts attribute component interventions under that exact optimizer convention. They do not isolate weight initialization from moment initialization.

Active-source one-step utility sign changed by resetting all optimizer state: 13/70 windows. This is not a count of full-policy allocation reversals.

Final recorded label-free full-space development accuracy:

| concept | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- |
| A | 0.1718 | 0.0000 | 0.1409 |
| B | 0.1839 | 0.3065 | 0.2258 |
| C | 0.1282 | 0.0000 | 0.0000 |

Macro accuracy over already observed concepts: frozen_centroid=0.1613, last_active=0.1022, uniform_probability=0.1222.

Timings separate method execution from the extra attribution and evaluation probes:

```json
{
  "component_audit_seconds": 248.78936588019133,
  "live_training_seconds": 58.13847642764449,
  "evaluation_seconds": 7.352193161845207
}
```

Paired frozen Day-4 routing reproduction check: 0 disagreements over 80 comparable steps.

## day5_banking_private_single_seed2026

Status: summary recorded.
Completed steps: 80. Learned batches: 80. Decisions: {'single_update': 80}. Final pool: 1.

Spawns: none.

Final recorded label-free full-space development accuracy:

| concept | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- |
| A | 0.1821 | 0.1821 | 0.1821 |
| B | 0.3258 | 0.3258 | 0.3258 |
| C | 0.0000 | 0.0000 | 0.0000 |

Macro accuracy over already observed concepts: frozen_centroid=0.1693, last_active=0.1693, uniform_probability=0.1693.

Timings separate method execution from the extra attribution and evaluation probes:

```json
{
  "component_audit_seconds": 0.0,
  "live_training_seconds": 2.352510826662183,
  "evaluation_seconds": 4.422095039859414
}
```

## day5_banking_shared_cau_seed2026

Status: summary recorded.
Completed steps: 80. Learned batches: 58. Decisions: {'warmup': 7, 'reuse': 50, 'spawn': 1, 'defer': 22}. Final pool: 2.

Spawns: [{"step":18,"segment":"B1","adapter":"adapter_1"}].

Selected guarded reuse updates: 50; positive measured mean protected loss increase admitted: 0. Maximum measured mean harm: -0.0127971. This is an empirical probe statistic, not a formal retention guarantee.

Final recorded label-free full-space development accuracy:

| concept | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- |
| A | 0.1753 | 0.1924 | 0.1959 |
| B | 0.0000 | 0.0000 | 0.0000 |
| C | 0.0000 | 0.0000 | 0.0000 |

Macro accuracy over already observed concepts: frozen_centroid=0.0584, last_active=0.0641, uniform_probability=0.0653.

Timings separate method execution from the extra attribution and evaluation probes:

```json
{
  "component_audit_seconds": 0.0,
  "live_training_seconds": 51.82546214014292,
  "evaluation_seconds": 6.4938712157309055
}
```

## Development comparison

| run | steps | updates | adapters | frozen_centroid | last_active | uniform_probability |
| --- | --- | --- | --- | --- | --- | --- |
| day5_amazon_private_cau_seed2026 | 80 | 79 | 1 | 0.8542 | 0.8542 | 0.8542 |
| day5_amazon_private_single_seed2026 | 80 | 80 | 1 | 0.8516 | 0.8516 | 0.8516 |
| day5_amazon_shared_cau_seed2026 | 80 | 79 | 1 | 0.8542 | 0.8542 | 0.8542 |
| day5_banking_head_only_cau_seed2026 | 80 | 80 | 3 | 0.1246 | 0.0774 | 0.0712 |
| day5_banking_private_cau_seed2026 | 80 | 80 | 3 | 0.1613 | 0.1022 | 0.1222 |
| day5_banking_private_single_seed2026 | 80 | 80 | 1 | 0.1693 | 0.1693 | 0.1693 |
| day5_banking_shared_cau_seed2026 | 80 | 58 | 2 | 0.0584 | 0.0641 | 0.0653 |

## Interpretation limits

The shared-head architecture adds all-adapter guards, including fresh and post-spawn warmup guards. It is a predeclared sensitivity extension. It differs from the private-package architecture in head sharing, moment sharing and protection scope; its between-run difference cannot isolate just one cause. The matched-state component contrasts provide more specific one-step attribution.

Centroids use stored training texts with gold labels ignored. No rule is selected by development accuracy. Replay capacity in these runs is per adapter and grows with the pool; fixed-total-resource comparisons and unseen seed/order confirmation remain required.

The runs do not establish TMLR readiness, a 95% retention guarantee, or LoRA-specific causal benefit without the corresponding positive matched-head evidence.
