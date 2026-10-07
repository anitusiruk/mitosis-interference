# When allocation selects a classifier reset: auditing prospective utility in continual adapter learning

**Working draft, October 2026. Development evidence only; incomplete comparator and final-evaluation sections.**

## Abstract

Continual adapter systems often create packages containing both a low-rank update and a trainable classifier. A successful fresh-package intervention can therefore reflect classifier initialization, optimizer state, or inference routing rather than a need for additional low-rank adaptation capacity. We study this distinction in a batch-level allocator that compares prospective, clipped AdamW updates against a common no-update state while separately checking protected-memory loss. Matched component interventions show classifier-reset effects at the original BANKING allocation windows; the broader all-mature-batch audit separately measures effects across the continuing trajectory. Across five development training seeds and two orders, a classifier-only allocator makes the same structural decisions as the full adapter allocator on BANKING, although training low-rank parameters improves prediction. The BERT transfer diagnostic also preserves allocation decisions under its declared recipe. Initial-loss ranking preserves BANKING decisions across three canonical-order development seeds, but changes decisions on the third Amazon seed. Learning-gain relevance is therefore regime-dependent. We additionally evaluate label-free deployment, shared classifiers, fixed training-memory budgets and same-label MultiNLI genre shifts. These results delimit what prospective package utility establishes and motivate resource-specific controls. They do not establish competitive superiority or a new general-purpose continual-learning method.

## 1. Motivation and scope

Distribution change, predicted forgetting and a requirement for new capacity are different claims. A prospective learning intervention is useful only if its manipulated resources match the interpretation of its outcome. In a classifier-bearing LoRA package, the replacement intervention simultaneously changes low-rank parameters, classifier weights, and AdamW state. Its performance cannot be attributed to LoRA capacity without controls.

Our subject is the frozen CAU-v1 reference in this repository, not every published adapter allocator. Existing dynamic adapter systems, counterfactual adaptation and learned routing already cover much of the broad design space. The related-work audit and comparator-port matrix identify the close CABLE, SEMA, SAFM, Online-LoRA, HESTIA, FiUni and TORA comparisons. A contribution framed only as evaluating an actual learning consequence would overstate novelty. The eventual paper must demonstrate a useful, distinctive finding and reproduce the closest relevant baselines.

## 2. Decision protocol

For candidate action a, denote the current incoming-query loss before and after one support update by L(a,before) and L(a,after). The no-update reference is the actual active package. The system utility is

$$U(a)=L(real,before)-L(a,after).$$

The exact prospective intervention performs one clipped AdamW step with the candidate's inherited or fresh moments and the declared dropout/RNG convention. Complementary even/odd support-query folds use every incoming example once as a query. Protected-reservoir loss is a separate feasibility condition. Ordinary feasible reuse can proceed even when its utility is nonpositive. New capacity requires positive fresh utility that beats the best feasible reuse, followed by two eligible windows. The full incoming-batch reuse guard precedes the actual update. Reservoirs protect and route; they do not supply rehearsal updates.

The protected-harm rule uses a lower confidence bound at zero. Its correct interpretation is a permissive probe rule; repeated adaptive application does not establish a formal retention guarantee. Discarded batches are recorded as DEFER and included in learning-continuity statistics.

## 3. A decomposition and attribution caveat

The utility separates into an initial prediction change and a learning gain:

$$U(a)=[L(real,before)-L(a,before)]+[L(a,before)-L(a,after)].$$

For fresh versus reuse, the common no-update baseline cancels. Subtracting it does not create a new relative ranking principle; it matters for the absolute requirement that a fresh action be useful. At the original BANKING spawn windows, roughly 87% of fresh-versus-best-reuse advantage arose before the prospective update. This initial term changes the entire package and is not a classifier-only effect.

The component factorial separately crosses inherited/fresh LoRA with inherited/fresh classifier stacks, preserves corresponding inherited AdamW moments, and empties moments for fresh components. Additional controls reset all moments and hold a common classifier fixed. Component weight and moment changes remain coupled in this factorial. The separately preregistered four-factor extension crosses LoRA weights, classifier weights, LoRA AdamW state and classifier AdamW state in all sixteen cells. Every mature incoming batch and both complementary query folds are retained. It additionally decomposes full-space cross entropy into label-group probability loss and conditional within-group loss, using evaluator-only group metadata. These are known probability identities, consistent with the WP/TP factorization in Kim et al. (2022, 2023), not new theory. Only observers that reproduce their full reference learner state and adapter tensors bitwise enter the analysis.

## 4. Experimental design

The reference backbone is DistilBERT with rank-8 Q/V LoRA, alpha 16, private pre-classifier/classifier stacks, one incoming-batch update, clipping, learning rate 0.0002, 64-token context, and 512-item reservoirs per package. The shared-head sensitivity uses one global classifier and optimizer with protection of all old adapters; this changes more than head sharing alone. The control named head-only keeps all LoRA outputs exactly zero and trains the private pre-classifier/classifier stack. Its hidden pre-classifier is a learned representation transform; this control rules out a need for LoRA in the observed allocation decisions, not all hidden representation learning. Fixed-single learners update each incoming batch without allocation probes.

BANKING uses a fixed train-derived development split, 33 observed classes within a full 77-way output space, and A1/B1/A2/C1/B2 recurrence with disjoint examples across repeated occurrences. Amazon uses train/validation sentiment recurrence over home, apparel and drugstore. Five fresh seeds 2027–2031 each have canonical and B-first orders. Both orders are averaged inside each seed before descriptive Student-t intervals. The evaluation examples are fixed, and interval scope does not include dataset-sampling uncertainty.

MultiNLI uses training-only fiction/government/telephone genres, three labels, a normalized-premise-grouped development holdout and genuine pair tokenization. Sharp/blurry variants preserve the same 1440 examples and labels. Its small short-context setting is a stress test, not a competitive NLI evaluation. Seed 2026 is a development pilot; 2027/2028 are descriptive transfer checks.

All predictors use full class spaces. Reported macro accuracy averages the three concept-level accuracies; it is not a BANKING per-class macro accuracy. Oracle specialist accuracy is a diagnostic. Fixed deployment rules are last-active, uniform probability mixture and frozen-base centroid. A standardized linear gate trained on reservoir-text adapter ownership is a separately declared auxiliary development diagnostic. Both hard selection and probability mixture are retained; no best routing rule is selected from outcomes.

## 5. Findings supported by the completed primary study

Across all ten fresh BANKING seed/order trajectories, full-package and head-only CAU make identical allocation sequences, including spawn steps 18 and 50. This is a statement about this controlled stream and decision protocol. LoRA learning still improves prediction, so identical allocation does not imply that low-rank learning itself is useless.

With frozen-centroid routing, mean BANKING accuracy is 15.90% for private CAU and 16.44% for the private fixed single. The paired difference is -0.54 percentage points, with a descriptive seed-cluster interval [-3.99, 2.91]. On Amazon, corresponding means are 83.41% and 85.10%, with paired difference -1.69 points and interval [-4.05, 0.66]. Report all routing rules in the final tables; these intervals do not establish equivalence or a multiplicity-adjusted winner.

MultiNLI growing-pool predictors often perform near the balanced chance level, while fixed singles learn modestly above chance. Expansion alone is therefore insufficient evidence of adaptation success in this protocol. Longer learning regimes are required before a broad application claim.

All twelve frozen initial-loss ranking controls are complete: BANKING/Amazon, private/head-only, and canonical-order seeds 2026–2028. BANKING has zero allocation disagreements in all six comparisons. Amazon has zero in seeds 2026 and 2027, but 24 head-only and 30 private-package decision disagreements in seed 2028. Under last-active prediction, the seed-2028 head-only initial-loss and prospective-ranking accuracies are 77.34% and 79.95%; private-package accuracies are 84.11% and 83.33%. These are individual development-seed results, not seed-cluster significance claims. Prospective protected-memory checks remain in both conditions. The finding concerns ranking only and supports neither removal of all lookahead nor a runtime improvement claim.

| regime | architecture | seed | allocation_disagreements |
| --- | --- | --- | --- |
| amazon | head_only | 2026 | 0 |
| amazon | head_only | 2027 | 0 |
| amazon | head_only | 2028 | 24 |
| amazon | private | 2026 | 0 |
| amazon | private | 2027 | 0 |
| amazon | private | 2028 | 30 |
| banking | head_only | 2026 | 0 |
| banking | head_only | 2027 | 0 |
| banking | head_only | 2028 | 0 |
| banking | private | 2026 | 0 |
| banking | private | 2027 | 0 |
| banking | private | 2028 | 0 |

The auxiliary learned-router study is complete for all 110 checkpoints. Over five fresh BANKING seed clusters, private CAU minus private single is +5.95 percentage points under hard routing (descriptive interval [1.60, 10.30]) and +5.60 under probability mixture ([1.02, 10.18]). Corresponding Amazon differences are -1.98 ([-5.04, 1.08]) and -1.72 ([-4.14, 0.70]). These are auxiliary development outcomes introduced after the original deployment failure, not an untouched confirmation of a complete method. Both rules remain in the account.

All 44 fixed-memory trajectories, all 44 fixed-memory router reloads, and all 11 rank-96 capacity trajectories are complete. The 512-total-text budget controls retained training examples and caps pools at eight; it does not equalize model parameters, optimizer state or prediction compute. Fixed versus per-adapter memory changes the private BANKING centroid accuracy by +0.38 points (descriptive interval [0.12, 0.64]); Amazon changes are small and uncertain. With this fixed text budget, private learned hard routing exceeds the fixed rank-8 single by +5.35 points on BANKING ([0.82, 9.88]); probability mixture gives +5.40 ([0.67, 10.14]). Amazon differences are -2.24 ([-5.97, 1.49]) and -1.80 ([-4.40, 0.81]). All are development-stage descriptive five-seed comparisons, with orders averaged inside seeds. The routing extension was introduced after earlier deployment failure.

The larger static rank-96 baseline remains untuned: its final accuracy is lower than rank 8 by 9.46 points ([-14.06, -4.86]) under the fixed recipe. Rank 96 has 2,419,277 adaptation parameters, compared with 2,391,783 for three rank-8 private packages; this is a particular storage scale, not universal resource matching. Poor untuned performance cannot support superiority over a properly tuned static alternative. The subsequent equal-grid rate study below addresses this tuning gap within its declared development protocol. Broader hyperparameter choices and final complete-method confirmation remain untested.

## 6. Reproducibility and limitations

The original routing trajectories reproduce exactly. Tiny real PEFT/AdamW tests check transaction restoration, fresh/reuse equivalence, component inheritance, zero-LoRA head-only behavior, grouped data construction and fixed-memory budget invariants. Live records include source hashes, package versions, stream hashes, decisions, losses, reservoir sizes and final learner state. The older backbone-revision field was null, so its historical byte identity is not established. The restart pins an explicit backbone commit and file hashes and requires aggregate checkpoint accuracy/count equality and loss agreement within absolute 1e-5 before new outcomes. That numerical check is weaker than a historical backbone checksum or saved per-example predictions.

Five seed clusters remain small. Current development examples are repeatedly examined, class-group BANKING recurrence is artificial, short context constrains MultiNLI, and growing pools increase both classifier storage and reservoir size. The rank-96 static baseline controls a particular observed storage scale, not every possible pool or every resource. Aggregate checkpoint-reload accuracy agreement is weaker than saved per-example prediction agreement. Duplicate/truncation auditing does not prove absence of semantic near duplicates or pretrained exposure.

Earlier BANKING exploratory work used official test data before the clean development protocol. This history must be disclosed. No official test was used in the present live studies; MultiNLI official validation remains unused. A final protocol must freeze the complete learner, router and resource condition before confirmation evaluation.

The earlier strict Day-2 robustness gate failed, and the original v0 controller starved learning. These failures remain part of the account rather than being replaced by favorable checks. Modern source-faithful method baselines, larger natural same-label adaptation regimes and complete-method confirmation evaluation remain outstanding. Separate classifier weight/state attribution and BERT transfer are tracked below; coverage alone does not establish a general mechanism. The findings currently support a methodological audit of this allocator, not competitive superiority or guaranteed retention.

## 7. Preregistered development extensions

The separate weight/state audit has 10/20 verified trajectories. The BERT allocation transfer study has 20/20 completed trajectories. Every failed or incomplete attempt remains recorded. Empty comparisons are pending and unpaired orders are excluded from seed intervals.

The BERT check changes the backbone, tokenizer, representations, frozen pooler and classifier together. It uses a single linear classifier rather than the DistilBERT trainable pre-classifier/classifier stack, but is not a causal isolation of classifier design or a tuned BERT performance comparison.

All cross-backbone prediction differences are reported below. Negative values indicate lower BERT accuracy. The cross-backbone changes are joint changes in architecture and initialized packages, not an optimized performance comparison or a classifier-only causal attribution.

| architecture | rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| head_only | frozen_centroid | 5 | -0.0561 | -0.0930 | -0.0193 |
| head_only | last_active | 5 | -0.0287 | -0.0501 | -0.0073 |
| head_only | uniform_probability | 5 | -0.0400 | -0.0882 | 0.0081 |
| private | frozen_centroid | 5 | -0.1078 | -0.1257 | -0.0898 |
| private | last_active | 5 | -0.0706 | -0.0869 | -0.0543 |
| private | uniform_probability | 5 | -0.0912 | -0.1418 | -0.0405 |

| seed | order | allocation_disagreements | private_spawn_steps | head_only_spawn_steps | private_learning_updates | head_only_learning_updates |
| --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2027 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2030 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2030 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2031 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2031 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |

The following table retains all four marginal reset factors, both regimes, and each declared metric. Positive contrasts mean lower initial/post-update loss or greater local learning gain after reset. Conditional cells and interactions are in the full Day-15 report. These averages describe the actual active source, not a retrospectively chosen best feasible reuse candidate. The interval unit is a paired training seed; the fixed development examples do not supply population-sampling uncertainty.

The all-mature-batch marginal effects average all eight settings of the other three reset factors and all eligible batches. They are a different estimand from fresh-package versus best-feasible-reuse advantage at allocation windows. Their signs need not agree. These measurements do not imply that resetting a trained classifier generally improves prediction. Conditional contrasts retain the artificial inherited-state/reset-weight combinations; useful deployment recipes require separate closed-loop experiments.

| regime | factor | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | reset_head_optimizer | post_update_loss_decrease | 2 | 0.0017 | -0.0248 | 0.0283 |
| amazon | reset_head_optimizer | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_head_optimizer | local_improvement_increase | 2 | 0.0017 | -0.0248 | 0.0283 |
| amazon | reset_head_optimizer | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_head_optimizer | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_head_optimizer | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_head_optimizer | post_within_group_decrease | 2 | 0.0017 | -0.0248 | 0.0283 |
| amazon | reset_head_weights | post_update_loss_decrease | 2 | -0.1462 | -0.2975 | 0.0052 |
| amazon | reset_head_weights | initial_loss_decrease | 2 | -0.1499 | -0.3312 | 0.0313 |
| amazon | reset_head_weights | local_improvement_increase | 2 | 0.0038 | -0.0261 | 0.0336 |
| amazon | reset_head_weights | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_head_weights | initial_within_group_decrease | 2 | -0.1499 | -0.3312 | 0.0313 |
| amazon | reset_head_weights | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_head_weights | post_within_group_decrease | 2 | -0.1462 | -0.2975 | 0.0052 |
| amazon | reset_lora_optimizer | post_update_loss_decrease | 2 | 0.0001 | -0.0081 | 0.0083 |
| amazon | reset_lora_optimizer | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_lora_optimizer | local_improvement_increase | 2 | 0.0001 | -0.0081 | 0.0083 |
| amazon | reset_lora_optimizer | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_lora_optimizer | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_lora_optimizer | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_lora_optimizer | post_within_group_decrease | 2 | 0.0001 | -0.0081 | 0.0083 |
| amazon | reset_lora_weights | post_update_loss_decrease | 2 | -0.0585 | -0.0649 | -0.0522 |
| amazon | reset_lora_weights | initial_loss_decrease | 2 | -0.0552 | -0.0719 | -0.0384 |
| amazon | reset_lora_weights | local_improvement_increase | 2 | -0.0033 | -0.0137 | 0.0070 |
| amazon | reset_lora_weights | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_lora_weights | initial_within_group_decrease | 2 | -0.0552 | -0.0719 | -0.0384 |
| amazon | reset_lora_weights | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | reset_lora_weights | post_within_group_decrease | 2 | -0.0585 | -0.0649 | -0.0522 |
| banking | reset_head_optimizer | post_update_loss_decrease | 2 | -0.0032 | -0.0313 | 0.0250 |
| banking | reset_head_optimizer | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | reset_head_optimizer | local_improvement_increase | 2 | -0.0032 | -0.0313 | 0.0250 |
| banking | reset_head_optimizer | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | reset_head_optimizer | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | reset_head_optimizer | post_group_mass_decrease | 2 | -0.0010 | -0.0059 | 0.0039 |
| banking | reset_head_optimizer | post_within_group_decrease | 2 | -0.0021 | -0.0254 | 0.0211 |
| banking | reset_head_weights | post_update_loss_decrease | 2 | -0.8533 | -0.8825 | -0.8242 |
| banking | reset_head_weights | initial_loss_decrease | 2 | -0.8495 | -0.8897 | -0.8093 |
| banking | reset_head_weights | local_improvement_increase | 2 | -0.0038 | -0.0149 | 0.0072 |
| banking | reset_head_weights | initial_group_mass_decrease | 2 | -0.8213 | -0.8271 | -0.8156 |
| banking | reset_head_weights | initial_within_group_decrease | 2 | -0.0281 | -0.0741 | 0.0178 |
| banking | reset_head_weights | post_group_mass_decrease | 2 | -0.8251 | -0.8458 | -0.8045 |
| banking | reset_head_weights | post_within_group_decrease | 2 | -0.0282 | -0.0780 | 0.0216 |
| banking | reset_lora_optimizer | post_update_loss_decrease | 2 | 0.0022 | 0.0020 | 0.0024 |
| banking | reset_lora_optimizer | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | reset_lora_optimizer | local_improvement_increase | 2 | 0.0022 | 0.0020 | 0.0024 |
| banking | reset_lora_optimizer | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | reset_lora_optimizer | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | reset_lora_optimizer | post_group_mass_decrease | 2 | 0.0019 | 0.0019 | 0.0020 |
| banking | reset_lora_optimizer | post_within_group_decrease | 2 | 0.0002 | -0.0000 | 0.0005 |
| banking | reset_lora_weights | post_update_loss_decrease | 2 | -0.0869 | -0.1809 | 0.0071 |
| banking | reset_lora_weights | initial_loss_decrease | 2 | -0.0769 | -0.1521 | -0.0017 |
| banking | reset_lora_weights | local_improvement_increase | 2 | -0.0100 | -0.0288 | 0.0088 |
| banking | reset_lora_weights | initial_group_mass_decrease | 2 | -0.0710 | -0.1081 | -0.0338 |
| banking | reset_lora_weights | initial_within_group_decrease | 2 | -0.0059 | -0.0440 | 0.0321 |
| banking | reset_lora_weights | post_group_mass_decrease | 2 | -0.0804 | -0.1198 | -0.0411 |
| banking | reset_lora_weights | post_within_group_decrease | 2 | -0.0065 | -0.0611 | 0.0482 |

## 8. Related work and contribution boundary

Classifier recency bias is established in Supervised Contrastive Replay (Mai et al., 2021), which studies replacing softmax classifiers with nearest-class-mean prediction. Logit and parameter calibration are also established in NLP continual learning (Li et al., 2022, LPC). Kim et al. (2022) decompose class-incremental prediction into within-task and task-id prediction; Kim et al. (2023), Eq.1, restate that factorization. Neither recognizing classifier bias nor the label-group loss identity is our contribution.

Wang et al. (2026, Predicting Plasticity) already distinguish initial loss from normalized future optimization gain. Lyle et al. (2025) study multiple causes of plasticity loss; Hernandez-Garcia et al. (2026) compare weight and unit reinitialization. Prospective optimization consequences, factorial diagnosis, and reset benefits are established. The candidate contribution is an operational empirical audit of how classifier-bearing allocation packages select resources, with optimizer-state attribution, cross-backbone checks, deployment/resource controls, and explicit failure conditions. Novelty remains provisional without the comparator and stronger-regime evidence.

Primary source links and precise scope are in `notes/novelty_audit_20261006.md` and `notes/classifier_prior_audit_20261006.md`.

## 9. Equal-grid tuning of static baselines

The baseline repair has 24/24 pilot trajectories and 20/20 paired development confirmations. Ranks 8 and 96 receive the same six-rate, two-order pilot grid. Each rank's rate is selected using only seed 2026, then committed before seeds 2027–2031. The existing adaptive outcomes and fixed development examples had already been examined. This addresses learning-rate tuning within a declared grid, not an untouched final evaluation or exhaustive hyperparameter search.

| rank | adaptive_rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| 8 | frozen_centroid | 5 | -0.0016 | -0.0341 | 0.0308 |
| 8 | last_active | 5 | -0.0601 | -0.1060 | -0.0142 |
| 8 | linear_hard | 5 | 0.0535 | 0.0082 | 0.0988 |
| 8 | linear_probability_mixture | 5 | 0.0541 | 0.0067 | 0.1014 |
| 8 | uniform_probability | 5 | -0.0335 | -0.0835 | 0.0166 |
| 96 | frozen_centroid | 5 | 0.0812 | 0.0441 | 0.1184 |
| 96 | last_active | 5 | 0.0227 | -0.0116 | 0.0570 |
| 96 | linear_hard | 5 | 0.1363 | 0.0927 | 0.1800 |
| 96 | linear_probability_mixture | 5 | 0.1369 | 0.0907 | 0.1831 |
| 96 | uniform_probability | 5 | 0.0494 | -0.0274 | 0.1262 |

All static ranks and adaptive rules are retained, with both orders averaged within each seed. Actual parameter storage, optimizer state and prediction compute remain different resources. The full grid, every trajectory, selected rates and resource counts are in `notes/day17_static_tuning_results.md`.

## Independent saved-receipt quality control

A read-only check of 10 completed observer trajectories verified every eligible mature batch, the actual active source, all sixteen intervention cells and both query folds, weight/state receipt isolation, bitwise invariance of initial predictions to optimizer-state interventions, and query-loss/component identities. This additional quality-control check was added after the first observer outcomes. It changes neither the frozen experiments nor their contrast definitions and is not a new scientific replication. Earlier and final receipts are preserved.

## Secondary deployed-retention analysis

An analysis added after primary outcomes uses all five saved segment-end checkpoints and all three original deployment rules. It compares fixed-memory adaptive trajectories with the frozen static reference and every available pilot-selected static rank on exactly paired streams. For each concept, the observed checkpoint drop is its maximum accuracy after first exposure minus its final accuracy; the statistic is averaged over concepts. Positive adaptive-minus-static differences below indicate more drop for the adaptive predictor. These are descriptive five-seed development summaries, not retention guarantees or independently confirmed hypotheses.

| regime | comparison | rule | metric | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | adaptive_minus_static_rank8_frozen | frozen_centroid | maximum_seen_checkpoint_drop | 5 | 0.0094 | -0.0146 | 0.0333 |
| amazon | adaptive_minus_static_rank8_frozen | last_active | maximum_seen_checkpoint_drop | 5 | 0.0339 | -0.0576 | 0.1253 |
| amazon | adaptive_minus_static_rank8_frozen | uniform_probability | maximum_seen_checkpoint_drop | 5 | 0.0029 | -0.0047 | 0.0104 |
| banking | adaptive_minus_static_rank8_frozen | frozen_centroid | maximum_seen_checkpoint_drop | 5 | -0.0551 | -0.0957 | -0.0145 |
| banking | adaptive_minus_static_rank8_frozen | last_active | maximum_seen_checkpoint_drop | 5 | 0.0979 | 0.0416 | 0.1542 |
| banking | adaptive_minus_static_rank8_frozen | uniform_probability | maximum_seen_checkpoint_drop | 5 | -0.0403 | -0.0804 | -0.0001 |
| banking | adaptive_minus_static_rank8_tuned | frozen_centroid | maximum_seen_checkpoint_drop | 5 | -0.0551 | -0.0957 | -0.0145 |
| banking | adaptive_minus_static_rank8_tuned | last_active | maximum_seen_checkpoint_drop | 5 | 0.0979 | 0.0416 | 0.1542 |
| banking | adaptive_minus_static_rank8_tuned | uniform_probability | maximum_seen_checkpoint_drop | 5 | -0.0403 | -0.0804 | -0.0001 |
| banking | adaptive_minus_static_rank96_tuned | frozen_centroid | maximum_seen_checkpoint_drop | 5 | -0.0413 | -0.0659 | -0.0168 |
| banking | adaptive_minus_static_rank96_tuned | last_active | maximum_seen_checkpoint_drop | 5 | 0.1117 | 0.0623 | 0.1610 |
| banking | adaptive_minus_static_rank96_tuned | uniform_probability | maximum_seen_checkpoint_drop | 5 | -0.0265 | -0.0547 | 0.0016 |

The full report also retains final accuracy, the mean seen-concept checkpoint accuracy and final-minus-first-exposure accuracy. Recurrence contributes to the latter, so it is not standard backward transfer for a nonrecurring task sequence. Fixed-memory learned routers have only final reload measurements; their temporal retention is unavailable and is not imputed. Definitions, all comparisons and source hashes are in `notes/day18_deployment_retention_results.md`.

## Within-backbone output-classifier control

The original head-only DistilBERT control includes a learned hidden pre-classifier. A separately declared development extension freezes that layer in both LoRA-plus-output-classifier and output-classifier-only learning. It retains the DistilBERT backbone, initialization, stream, allocator, optimizer rate, clipping and memory condition. It removes hidden pre-classifier learning and its optimizer state together; it is not a weight-versus-state factorial for that layer. PEFT stores dormant pre-classifier copies, which remain counted in storage.

The extension completed 20/20 research trajectories and 10/10 allocation pairs. Its unchanged-wrapper replay and tiny CPU/CUDA intervention gates precede the research runs. The following tables retain every completed pair and every original prediction rule; these are repeatedly examined development streams, not untouched confirmation or tuned competitive performance.

| seed | order | allocation_disagreements | private_spawn_steps | head_only_spawn_steps | private_learning_updates | head_only_learning_updates |
| --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2027 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2030 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2030 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2031 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2031 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |

| rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- |
| frozen_centroid | 5 | -0.0010 | -0.0101 | 0.0081 |
| last_active | 5 | -0.0012 | -0.0096 | 0.0073 |
| uniform_probability | 5 | 0.0017 | -0.0067 | 0.0101 |

All deviations from the trainable-stack references, each trajectory and stored frozen versus output-classifier parameters are in `notes/day19_linear_classifier_results.md`.

## Figures and result sources

Use the generated PNG/PDF/SVG figures in `figures/research_audit`, with the explicit scope in `CAPTIONS.md`. All numeric tables are regenerated from the raw trajectories by the report modules. `notes/research_progress.md` gives current coverage and remaining research steps. `notes/day5_related_work_audit.md` and `notes/day11_baseline_port_matrix.md` provide primary-source links; complete bibliographic metadata and author-code reproductions before submission.

Day-5 tracker: causal audit complete; core LoRA-specific allocation interpretation unsupported by present controls; submission readiness pending the missing evidence above.
