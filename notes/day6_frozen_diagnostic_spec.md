# Frozen seed and order diagnostics, declared before the new outcomes

This advances the Day-6 work without declaring the method ready. Day-5 seed 2026 is development. Its matched-state audit shows substantial head-reset effects and the shared-head sensitivity suffers deferral. The original private-package CAU-v1 is retained as a frozen reference, not relabeled a LoRA-only method. No threshold, optimizer, learning rate, architecture, or routing rule will be tuned using the following runs.

## Design

- Seeds: 2027, 2028, 2029, 2030, 2031. These are unused in the present Day-5 research branch.
- Regimes: BANKING77 disjoint-label recurrence and Amazon same-label domain recurrence, using precisely the existing train/development data builders. Official tests remain unused. Development evaluation sets remain fixed across seeds.
- Orders: canonical A1 B1 A2 C1 B2; alternate B1 A1 B2 C1 A2. Reorder the exact same generated batches, preserving each segment's within-segment order. Segment identities are supplied only to the evaluator, never the controller or prediction router.
- Four learners per seed/order/regime: private LoRA-and-head CAU-v1; head-only CAU-v1 with all LoRA branches identically zero; fixed single LoRA-and-head learner; fixed single head-only learner.
- Run all 80 combinations sequentially on the same GPU, with the same model and package environment, CPU thread budget 8, batch size 16, AdamW learning rate 0.0002, warmup and harm-LCB gate as frozen on Day 4. No component probes in these runs.
- A per-adapter reservoir of 512 remains the original protocol. Pool growth increases total memory and parameters. Thus these are architectural and controller diagnostics, not a fixed-total-resource superiority claim. Head-only carries unused zero-LoRA scaffolding for implementation comparability; active and stored parameter accounting must disclose it.
- Label-free predictions: last active, uniform probability mixture, frozen-feature nearest centroid, exactly as declared on Day 5. Report all three without choosing a winner after outcomes. Full 77-way BANKING accuracy is mandatory; concept-restricted/oracle scores remain diagnostics.

## Analysis and stopping

For each regime and fixed prediction rule, report final macro accuracy, learned-batch count, adapter count, and runtime for every seed/order. Compare private versus head-only with paired differences under each controller, and CAU versus fixed-single within each architecture. Average the two orders within each seed before estimating a seed-level mean and Student-t interval (five independent seed clusters); order-specific results remain visible. Such intervals quantify only the sampled training randomness conditional on these fixed datasets, two orders, and this development protocol. They do not establish significance across methods, datasets, or all possible streams; report no winner from multiple rule comparisons. Windows and paired orders are not independent replicates.

The queue stops launching at 03:20 UTC and every learner has a 03:25 UTC checkpoint cutoff on 2026-10-06, ahead of the user's 10:30 PM Dallas deadline. Preserve completed and partial runs separately. A failed job halts the batch for inspection; no failed result is silently replaced. No official-test access and no further model/controller tuning in this batch.

## Decision criterion

Carry CAU-v1 forward as a candidate only if it repeatedly preserves learning and its allocation benefits are useful under label-free evaluation. A near-equivalent head-only result undermines a LoRA-specific novelty claim. More adapters alone, restricted/oracle performance alone, or one seed's clean boundary alignment is insufficient. Shared-head deferral and optimizer-state sensitivity must remain explicit negative findings. Modern baseline implementations, a third natural regime, fixed-total-resource experiments, and untouched final evaluation are still required for a submission claim.
