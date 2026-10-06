# Pre-update action-ranking ablation, declared before closed-loop outcomes

For any candidate a, exact action utility decomposes as

U(a) = L(real active, before) - L(a, before) + [L(a, before) - L(a, after)].

The first term measures changing the current predictor before training, while the bracket measures the one-step held-out learning gain. The common real baseline cancels in a fresh-versus-reuse comparison. In the original BANKING development trajectory, the two spawn windows' initial fresh-versus-best-reuse loss gaps account for approximately 87% of their final utility advantages. The component audit attributes a substantial part of that gap to classifier-head initialization. This motivates an ablation rather than a claim that initialization alone explains all decisions.

Use the identical private-package and head-only CAU-v1 learners but rank actions by **pre-update** held-out query loss. Reuse utility becomes statusquo loss minus that adapter's pre-update query loss; fresh utility becomes statusquo loss minus the fresh package's pre-update query loss. Recompute the best cross-fold-feasible reuse using the exact frozen utility/harm/name tie-break, and apply the same positive absolute fresh criterion, two-window confirmation, warmup, full-batch reuse guard and literal DEFER. Preserve all exact AdamW retention probes. This tests whether the post-update current-query component adds value; it is not a no-lookahead retention method or a runtime speedup because existing prospective guard computations remain.

Run seeds 2026, 2027, 2028, canonical order, BANKING/Amazon, private/head-only: 12 trajectories. Compare to corresponding original frozen CAU inputs. This is a development mechanistic pilot; these selected early seeds do not establish statistical confirmation. Report allocation agreement/disagreement, spawn timing, updates and all three original label-free prediction rules. Do not pool windows as independent samples, choose a rule after outcomes, claim a full CABLE reproduction, or silently retune thresholds. Preserve original post-update utility values in the logs under explicit diagnostic names.

Before live runs, validate recomputed utility/ranking on synthetic profiles with ties, no feasible reuse, and empty/negative fresh eligibility. Verify that the wrapper changes no learned parameters, optimizer states, RNG or reservoirs around a real cross-fit probe. Queue after fixed-memory sensitivity; honor the existing 03:20/03:25 UTC cutoffs. If the user deadline limits completion, retain partial results separately.
