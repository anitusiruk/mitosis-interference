# Bounded continuation results and interpretation

Both original seed-2029 B-first factorial cells passed exact pre-training stream gates and full final learner/adapter replay. The independent saved-receipt checker passed all twelve trajectories. Each regime now has three paired training seeds; both orders are averaged within seed. All 56 marginal metric rows, conditional cells and two-factor interactions remain in the derived evidence. No test split was newly accessed.

The following table retains every factor in both regimes for the declared post-update loss estimand. Positive values mean resetting the factor lowers loss. Intervals are descriptive Student-t intervals over only three training seeds, with fixed development data and no multiplicity correction.

| regime | factor | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| amazon | reset_head_optimizer | 3 | 0.0028 | -0.0040 | 0.0096 |
| amazon | reset_head_weights | 3 | -0.1473 | -0.1774 | -0.1173 |
| amazon | reset_lora_optimizer | 3 | 0.0006 | -0.0019 | 0.0030 |
| amazon | reset_lora_weights | 3 | -0.0632 | -0.0834 | -0.0430 |
| banking | reset_head_optimizer | 3 | -0.0028 | -0.0085 | 0.0029 |
| banking | reset_head_weights | 3 | -0.8551 | -0.8645 | -0.8457 |
| banking | reset_lora_optimizer | 3 | 0.0021 | 0.0020 | 0.0023 |
| banking | reset_lora_weights | 3 | -0.0818 | -0.1104 | -0.0532 |

Resetting trained classifier weights worsens initial and post-update prediction in these all-mature-batch averages. This does not contradict a fresh-package advantage at selected allocation windows: the source and averaging estimands differ. The factorial averages every eligible mature batch and all eight settings of the other factors, including artificial reset-weight/inherited-state combinations. It does not establish a generally useful deployment reset. Small or zero-crossing state intervals are not evidence of equivalence.

Current historical data provenance has a limitation: the original full dataset revision and per-example development hashes were not recorded. This restart pins the current Hub revisions, verifies the original full training-stream digest before updates, reproduces the saved learner bitwise, and reproduces every recorded development aggregate exactly. Aggregate equality is not a proof of historical per-example identity.

The auxiliary Online-LoRA source probe passed ten synthetic CPU checks and is not a published benchmark reproduction. Close prior work limits theory and optimizer-reset novelty. Complete author-method comparisons, a substantially learning natural same-label regime, the remaining eight original factorial cells and a frozen complete-method final evaluation remain necessary before a serious submission.
