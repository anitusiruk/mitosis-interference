# Updated novelty assessment and contribution boundary

Checked 2026-10-06. This is a focused primary-source audit, not an exhaustive
priority search or a numerical probability of acceptance. Current readiness is
low: a plausible methodological-audit contribution remains, but the evidence
does not yet justify submission.

| Primary work | What it already establishes | Boundary for this project |
| --- | --- | --- |
| Wang et al., [Predicting Plasticity in Deep Continual Learning](https://arxiv.org/html/2605.09044v1), May 2026 | Defines trainability through normalized future optimization gain; explains why absolute gains across different initial losses can mislead; supplies theoretical counterexamples to structural diagnostics and an optimization-readiness measure. | Neither prospective gain as a diagnostic nor the distinction between initial quality and improvement is new. Our candidate finding is about actual reuse/expansion decisions in classifier-bearing packages under exact inherited AdamW state. No new trainability theorem is claimed. |
| Lyle et al., [Disentangling the Causes of Plasticity Loss](https://proceedings.mlr.press/v274/lyle25a.html), CoLLAs 2025 | Studies multiple mechanisms and combined interventions for preserving plasticity. | Multi-factor causal diagnosis of plasticity is established. A weight/state factorial needs an informative allocation finding; the factorial alone is insufficient novelty. |
| Hernandez-Garcia et al., [Reinitializing weights vs units](https://arxiv.org/html/2508.00212v1), 2025 | Compares selective weight reinitialization with unit reinitialization for maintaining plasticity. | Resetting weights or discovering a reset benefit is not a new contribution. Our one-step package result is not a proof of recovered future plasticity. |
| Julian et al., [CABLE](https://www.nature.com/articles/s44387-025-00028-4.pdf), npj AI 2025 | Eq.10 multiplies post/pre incoming and remembered loss ratios after an SGD lookahead; a reinforcement-learning policy assigns classes to adapters. | Evaluating actual update consequences for allocation is established. Our additive common-reference score and batch-level decision are specific design choices, not priority over CABLE. An equation-level signal study is distinct from reproducing its full PPO system. |
| Wei et al., [Online-LoRA](https://arxiv.org/html/2411.05663v1), 2024/2025 | Uses loss plateaus to expand LoRA, freezes/merges prior updates, and regularizes online parameter importance. | Task-free loss-triggered LoRA expansion is established. Its merged-backbone semantics differ from a selectable private-head package pool. No direct superiority claim follows without matched experiments. |
| Wang et al., [SEMA](https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_Self-Expansion_of_Pre-trained_Models_with_Mixture_of_Adapters_for_Continual_CVPR_2025_paper.pdf), CVPR 2025 | Uses representation descriptors for expansion and a learned adapter-mixture router. | Dynamic reuse/expansion and learned routing are established. Our linear ownership gate is an ordinary auxiliary control. |
| Yildirim et al., [Pruned Adaptation Modules](https://arxiv.org/html/2603.21170v1), March 2026 | Argues for rigorous lightweight baselines and introduces sparse task-specific ResNet modules for vision class-incremental learning. | Weak fixed-capacity controls cannot support broad resource-efficiency claims. Author vision numbers are not comparable with our short text streams. |

## Defensible question

When an allocator evaluates a fresh classifier-and-LoRA package, what exactly
does favorable prospective utility establish? The original predictor can lose
mass on a newly arriving label group, while an initializer restores that mass
before any update. A useful audit must identify this mechanism, distinguish
classifier weights from optimizer state, show its operational effect on actual
decisions, and delimit conditions where it disappears. It must also show that
LoRA can improve prediction even when the allocation sequence is unchanged.

Initial quality is a legitimate part of an immediate post-update prediction
objective. Calling it a bug or confound requires stating the stronger target
interpretation (need for more representation capacity or improved trainability).
The algebraic utility decomposition is elementary. Our study concerns CAU-v1;
it does not by itself establish a defect in any named published allocator.

The novelty claim should remain provisional until separate weight/state results,
a second classifier architecture, meaningful same-label learning, and a relevant
source-faithful signal/method comparison establish a useful scope. If these
controls show a narrow construction-specific effect, narrow the paper further
or change direction; do not manufacture a new method claim from that effect.

## Source-code audit caution

Read-only inspection of jjul482/CABLE at the GitHub API-reported commit
`c72b9cfeb345c8d517f1266ceb2b0ebf8a02430e` found an SGD virtual parameter
update and Fisher-weighted squared-change normalization in
`backbone/cable.py:compute_forgetting_score_adapters`. This inspected helper is
not Eq.10's direct loss-ratio expression. The top-level reinforcement module
must be traced before attributing full method semantics to that helper or
claiming a faithful reproduction. Preserve exact source hashes and distinguish
published equations, current author implementation, and any text adaptation.
Do not quietly replace the paper's signal with a convenient approximation.

## TMLR assessment

[TMLR's acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html)
emphasize substantiated claims and findings of interest; state-of-the-art results
are not required. Its [editorial policies](https://jmlr.org/tmlr/editorial-policies.html)
permit modest contributions but require correct attribution of prior work.
The current route is an empirical methodological audit with clear limits. It is
plausible, not established as sufficiently novel or ready, and no acceptance
guarantee or calibrated numerical probability is available.
