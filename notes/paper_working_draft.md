# When allocation selects a classifier reset: auditing prospective utility in continual adapter learning

**Working draft, October 2026. Development evidence only; incomplete comparator and final-evaluation sections.**

## Abstract

Continual adapter systems often create packages containing both a low-rank update and a trainable classifier. A successful fresh-package intervention can therefore reflect classifier initialization, optimizer state, or inference routing rather than a need for additional representation capacity. We study this distinction in a batch-level allocator that compares prospective, clipped AdamW updates against a common no-update state while separately checking protected-memory loss. Matched component interventions show substantial classifier-reset effects on a BANKING recurrence stream. Across five fresh seeds and two orders, a classifier-only allocator makes the same structural decisions as the full adapter allocator on BANKING, although training low-rank parameters improves prediction. Initial-loss ranking preserves the original pilot's decisions despite omitting the prospective learning-gain term from action ranking. We additionally evaluate label-free deployment, shared classifiers, fixed training-memory budgets and same-label MultiNLI genre shifts. These results delimit what prospective package utility establishes and motivate resource-specific controls. They do not establish competitive superiority or a new general-purpose continual-learning method.

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

The component factorial separately crosses inherited/fresh LoRA with inherited/fresh classifier stacks, preserves corresponding inherited AdamW moments, and empties moments for fresh components. Additional controls reset all moments and hold a common classifier fixed. Component weight and moment changes remain coupled in this factorial. A future weight-only/moment-only factorial is required for their separate attribution.

## 4. Experimental design

The reference backbone is DistilBERT with rank-8 Q/V LoRA, alpha 16, private pre-classifier/classifier stacks, one incoming-batch update, clipping, learning rate 0.0002, 64-token context, and 512-item reservoirs per package. The shared-head sensitivity uses one global classifier and optimizer with protection of all old adapters; this changes more than head sharing alone. The head-only control keeps all LoRA outputs exactly zero and trains only private classifiers. Fixed-single learners update each incoming batch without allocation probes.

BANKING uses a fixed train-derived development split, 33 observed classes within a full 77-way output space, and A1/B1/A2/C1/B2 recurrence with disjoint examples across repeated occurrences. Amazon uses train/validation sentiment recurrence over home, apparel and drugstore. Five fresh seeds 2027–2031 each have canonical and B-first orders. Both orders are averaged inside each seed before descriptive Student-t intervals. The evaluation examples are fixed, and interval scope does not include dataset-sampling uncertainty.

MultiNLI uses training-only fiction/government/telephone genres, three labels, a normalized-premise-grouped development holdout and genuine pair tokenization. Sharp/blurry variants preserve the same 1440 examples and labels. Its small short-context setting is a stress test, not a competitive NLI evaluation. Seed 2026 is a development pilot; 2027/2028 are descriptive transfer checks.

All predictors use full class spaces. Oracle specialist accuracy is a diagnostic. Fixed deployment rules are last-active, uniform probability mixture and frozen-base centroid. A standardized linear gate trained on reservoir-text adapter ownership is a separately declared auxiliary development diagnostic. Both hard selection and probability mixture are retained; no best routing rule is selected from outcomes.

## 5. Findings supported by the completed primary study

Across all ten fresh BANKING seed/order trajectories, full-package and head-only CAU make identical allocation sequences, including spawn steps 18 and 50. This is a statement about this controlled stream and decision protocol. LoRA learning still improves prediction, so identical allocation does not imply that low-rank learning itself is useless.

With frozen-centroid routing, mean BANKING accuracy is 15.90% for private CAU and 16.44% for the private fixed single. The paired difference is -0.54 percentage points, with a descriptive seed-cluster interval [-3.99, 2.91]. On Amazon, corresponding means are 83.41% and 85.10%, with paired difference -1.69 points and interval [-4.05, 0.66]. Report all routing rules in the final tables; these intervals do not establish equivalence or a multiplicity-adjusted winner.

MultiNLI growing-pool predictors often perform near the balanced chance level, while fixed singles learn modestly above chance. Expansion alone is therefore insufficient evidence of adaptation success in this protocol. Longer learning regimes are required before a broad application claim.

The four original pre-update-ranking pilots reproduce their original structural decisions. Prospective protected-memory checks remain in those pilots, so the finding concerns the action-ranking learning-gain term and does not demonstrate that all lookahead is unnecessary or that runtime improves.

Auxiliary learned routing, fixed-memory replications and the larger fixed-capacity baseline are **pending final analysis**. Insert their verified saved tables only after the relevant trajectories and consistency checks complete. The single learned-routing pilot already differs from the original deployment rules; do not promote that exploratory result to a confirmed end-to-end improvement.

## 6. Reproducibility and limitations

The original routing trajectories reproduce exactly. Tiny real PEFT/AdamW tests check transaction restoration, fresh/reuse equivalence, component inheritance, zero-LoRA head-only behavior, grouped data construction and fixed-memory budget invariants. Live records include source hashes, model revision, package versions, stream hashes, decisions, losses, reservoir sizes and final learner state.

Five seed clusters remain small. Current development examples are repeatedly examined, class-group BANKING recurrence is artificial, short context constrains MultiNLI, and growing pools increase both classifier storage and reservoir size. The rank-96 static baseline controls a particular observed storage scale, not every possible pool or every resource. Aggregate checkpoint-reload accuracy agreement is weaker than saved per-example prediction agreement. Duplicate/truncation auditing does not prove absence of semantic near duplicates or pretrained exposure.

Earlier BANKING exploratory work used official test data before the clean development protocol. This history must be disclosed. No official test was used in the present live studies; MultiNLI official validation remains unused. A final protocol must freeze the complete learner, router and resource condition before confirmation evaluation.

The earlier strict Day-2 robustness gate failed, and the original v0 controller starved learning. These failures remain part of the account rather than being replaced by favorable checks. Modern source-faithful method baselines, larger natural same-label adaptation regimes, separate classifier-weight/moment attribution and final evaluation are outstanding. The findings currently support a methodological audit of this allocator, not competitive superiority or guaranteed retention.

## Figures and result sources

Use the generated PNG/PDF/SVG figures in `figures/research_audit`, with the explicit scope in `CAPTIONS.md`. All numeric tables are regenerated from the raw trajectories by the report modules. `notes/research_progress.md` gives current coverage and remaining research steps. `notes/day5_related_work_audit.md` and `notes/day11_baseline_port_matrix.md` provide primary-source links; complete bibliographic metadata and author-code reproductions before submission.

Day-5 tracker: causal audit complete; core LoRA-specific allocation interpretation unsupported by present controls; submission readiness pending the missing evidence above.
