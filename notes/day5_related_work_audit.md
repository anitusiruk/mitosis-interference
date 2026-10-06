# Day-5 primary-source novelty and scope audit

Checked 2026-10-05. This is a focused audit, not proof that no equivalent method
exists. No numeric novelty score is assigned. Baseline source and official code
must be inspected before claiming an implementation is a faithful reproduction.

| Work | Relevant established idea | Consequence for our claim |
| --- | --- | --- |
| [SEMA, CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_Self-Expansion_of_Pre-trained_Models_with_Mixture_of_Adapters_for_Continual_CVPR_2025_paper.html) | Distribution descriptors trigger adapter reuse/expansion; a learned mixture router combines adapters. | Dynamic adapter creation and reuse are established. Compare allocation signals under matched training/data budgets. |
| [SAFM, EACL 2026](https://aclanthology.org/2026.eacl-long.37/) | Task-level architecture search selects reused, fresh, or empty adapters, then tunes with pseudo-replay. | Three-way structural choices and empty branches are established; its empty adapter is not our no-learning DEFER. Its supplied task episodes differ from our batch stream. |
| [CABLE, npj AI 2025](https://www.nature.com/articles/s44387-025-00028-4) | Eq. 10 combines actual pre/post-update loss ratios on incoming and remembered examples; a PPO policy learns adapter assignments. | Closest overlap: intervention-based forward/backward loss scoring and prospective forgetting are already present. Do not claim the first allocation method to evaluate actual learning consequences. Need CABLE-style loss-ratio and lookahead baselines; distinguish a port from official end-to-end CABLE. |
| [HESTIA, UAI 2026](https://proceedings.mlr.press/v337/le26a.html) | Order-invariant linearized adaptation and density-based label-free adapter retrieval. | Task-free adaptation and inference routing are established. Our oracle specialization scores cannot substantiate a deployable task-free learner. |
| [FiUni, August 2026 preprint](https://arxiv.org/html/2608.27070v1) | Fisher/K-FAC subspace similarity guides reuse, expansion, and construction of LoRA subspaces at batch level. | Task-free structural adaptation and model-based geometry signals are established. Prospective utility must improve on geometry/signals, rather than claim novelty for batch-level task detection. |
| [Online-LoRA, WACV 2025](https://arxiv.org/abs/2411.05663) | LoRA-based task-free online adaptation, online regularization, and loss-driven expansion. | Task-free online LoRA alone is not novel. Need a faithful port or clearly scoped comparable baseline. |
| [ODA, IEEE Access 2025](https://research-repository.st-andrews.ac.uk/handle/10023/32580) | Expert growth and opportunistic merging under class-incremental learning. | Flexible capacity and nonmonotone architecture management are established. |

The defensible candidate is an experimentally supported finding about absolute
action utility, protected-retention filtering, and learning continuity in a
learner-state-dependent allocation system. CABLE already measures actual loss
changes, so “intervention instead of similarity” alone is an inadequate novelty
argument. The common baseline cancels when ranking fresh against reuse; its
distinct role is the absolute positive-utility requirement for new capacity.
Explain this explicitly rather than presenting the baseline subtraction itself
as a new ranking principle. AdamW moment dependence is mathematically expected;
its scientific value requires a useful, controlled capacity-allocation finding.

Current scientific gaps: private-head confounding, narrow short development
streams, seed 2026 only, optimizer-state controls, fixed resource comparisons,
external baseline reproduction, and end-to-end label-free inference. Preserve
the Day-2 failed robustness gate and Day-4 v0 starvation failure.

[TMLR acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html) emphasize
convincing support for claims, clear communication, and findings of interest to
the audience. They do not require a new state-of-the-art or a novelty threshold.
This does not make an incomplete pilot ready to submit: evidence must support
the final stated scope and human authors must understand and verify the work.
