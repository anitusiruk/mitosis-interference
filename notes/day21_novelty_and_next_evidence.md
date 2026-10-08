# Day 21: contribution boundary and evidence priorities

Written 2026-10-08 UTC after inspecting primary papers and author code. This is a focused related-work check, not an exhaustive novelty or priority search. The two capped continuations complete already declared seed/order cells; they introduce no new scientific contrast and use no outcome-based scheduling.

## Candidate contribution

The defensible candidate is an operational audit of what a classifier-bearing, prospective adapter allocation decision actually selects. The package intervention crosses LoRA weights, classifier-stack weights, LoRA AdamW state and classifier-stack AdamW state; every mature batch, sixteen cells and both query folds remain visible. An independent observer reproduces the real learner bitwise. Allocation identity under zero-LoRA and frozen-hidden-pre-classifier controls separates observed allocation behavior from prediction benefits. Label-free deployment and distinct storage, optimizer, memory and inference costs constrain practical interpretation.

This combination may support a useful empirical contribution if the mechanism persists in a substantially learning same-label regime and in a complete relevant published system. The current synthetic CPU reset probe adds implementation evidence, not a competitive baseline. Acceptance and adequate novelty remain unestablished.

## Close primary work and its implications

| Primary source | Established or closely related idea | Boundary for this project |
| --- | --- | --- |
| [Online-LoRA, WACV 2025](https://arxiv.org/html/2411.05663v1), [official code](https://github.com/Christina200/Online-LoRA-official) | Online loss monitoring, plateau-triggered adaptation, low-rank consolidation and regularization with a small hard buffer. | Dynamic low-rank adaptation is existing work. Our source-path probe must not stand in for the complete image benchmark, MAS/hard-buffer loop or reported performance. |
| [SEMA, arXiv 2403.18886](https://arxiv.org/abs/2403.18886) | Demand-dependent adapter expansion and learned mixture routing. | Neither expansion nor learned routing is a standalone new contribution here. |
| [CABLE, npj Artificial Intelligence 2025](https://www.nature.com/articles/s44387-025-00028-4) | Counterfactual adaptation and predicted forgetting for reuse/allocation. | A claim that evaluating a learning consequence is new would be too broad. Equation-level ports remain distinct from full author-method reproduction. |
| [A Closer Look at Rehearsal-Free Continual Learning, CVPR Workshops 2023](https://openaccess.thecvf.com/content/CVPR2023W/CLVision/html/Smith_A_Closer_Look_at_Rehearsal-Free_Continual_Learning_CVPRW_2023_paper.html) | Classifier behavior and bias can materially affect continual-learning outcomes. | Classifier confounding is known; the narrower allocation intervention and its state controls need to carry the contribution. |
| [Local Classifier Alignment, arXiv 2603.09888](https://arxiv.org/abs/2603.09888) | Misalignment between task classifiers and a merged backbone, with classifier alignment for continual learning. | Classifier/backbone compatibility is also existing work; do not claim the general phenomenon as new. |
| [Predicting Plasticity in Deep Continual Learning, arXiv 2605.09044](https://arxiv.org/html/2605.09044v1) | Plasticity measures separate optimization gains from initial loss and inspect gradient quality. | Initial prediction quality versus subsequent optimization gain is not a new conceptual distinction. |
| [LoRA-the-Explorer, ICML 2024](https://arxiv.org/html/2402.16828v2), Section 3.4 and Appendix A.4 | Explicit LoRA factor and optimizer-reset ablations; retaining optimizer state can improve training. | The importance of optimizer retention is established. Our four-way attribution and the specific author reset path require their own evidence. |
| [Bilinear Optimization Divergence, arXiv 2609.23594v1](https://arxiv.org/html/2609.23594v1), Sections 3.2–3.5 and Appendix A.3 | Bilinear LoRA anchors, companion-factor residuals and realized optimizer displacements can invalidate gradient-level protection. | Cite this close September 2026 preprint. Bilinear cross terms, zero-output initialization and the difference between gradients and Adam displacement are not our new theory. Its main intervention concerns historical-subspace protection; ours currently concerns package-allocation attribution and classifier weights/state. That difference alone does not establish sufficient novelty. |

These sources narrow the claim. The source-level Online-LoRA observations in `day21_online_lora_source_review.md` are tied to one pinned public commit; they are not allegations about every implementation or the paper's reported experiments. No full author benchmark was executed in this session.

## Evidence needed before a serious submission

1. Finish the original twenty-cell seed/order factorial queue with the existing inclusion gates, retain all effects and paired-seed intervals, and publish every interrupted attempt. The current two additional cells increase paired seeds without choosing cells by effect size.
2. Establish meaningful learning in a natural same-label stream. The short MultiNLI stress run near chance cannot carry a broad plasticity claim. Freeze a separate pilot/confirmation recipe before examining fresh confirmation seeds.
3. Execute at least one complete close published method under its author configuration in an isolated environment. Add matched component controls only after reproducing the unmodified baseline, and report all deviations and measured resource budgets. Online-LoRA has a concrete official configuration; its complete source path is a feasible candidate, subject to a small timing gate rather than an hours-long launch.
4. Use a final held-out evaluation only after the method, scope, thresholds and comparison recipes are frozen. Repeatedly viewed development splits remain development evidence. Avoid counting orders, mature batches or examples as independent training replicates.
5. Test whether an attribution-based change produces a useful closed-loop outcome with matched controls. One-step causal probes, including artificial reset-weight/inherited-state cells, do not establish an effective deployment recipe or a retention guarantee.

The useful next experiment should address one of these gaps. More short weak-learning trajectories or algebra-only identities would increase file counts without resolving the submission risk.
