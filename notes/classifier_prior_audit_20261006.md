# Classifier and probability-factorization prior work

Focused primary-source check, 2026-10-06. This supplements the novelty audit;
it is not an exhaustive priority search. None of these papers has been reproduced
as a matched baseline in this repository yet.

* Mai, Li, Kim and Sanner, [Supervised Contrastive Replay: Revisiting the Nearest
  Class Mean Classifier in Online Class-Incremental Continual Learning](https://arxiv.org/abs/2103.13885),
  2021. The paper identifies softmax recency bias and studies replacing softmax
  classification with nearest-class-mean prediction across replay methods. It
  discusses probability mass favoring recent classes. Classifier bias and
  classifier-dependent continual-learning outcomes are established observations;
  they are not this project's novel claim.
* Li, Wang, Li, Khan and Thuraisingham, [LPC: A Logits and Parameter Calibration
  Framework for Continual Learning](https://aclanthology.org/2022.findings-emnlp.529/),
  Findings of EMNLP 2022, pp.7142–7155. It combines logit and parameter calibration
  without accessing previous task data and evaluates GLUE scenarios. NLP logit
  calibration and old/new-model alignment are established. This project does not
  claim to invent calibration or a stronger general-purpose NLP learner.
* Kim, Xiao, Konishi, Ke and Liu, [A Theoretical Study on Solving Continual
  Learning](https://arxiv.org/abs/2211.02633), NeurIPS 2022. It decomposes
  class-incremental prediction into within-task prediction and task-id prediction,
  and connects task identification with out-of-distribution detection.
* Kim, Xiao, Konishi and Liu, [Learnability and Algorithm for Continual
  Learning](https://proceedings.mlr.press/v202/kim23x.html), ICML 2023,
  pp.16877–16896. Section 3, Eq.1 explicitly restates the product factorization
  of within-task and task-id prediction, citing the 2022 work. Taking negative
  logarithms gives the same elementary decomposition used by our label-group
  audit. Our group-mass and conditional-loss measurements operationalize this
  established identity on the logits of the allocation intervention; they do
  not create a new theory, theorem or novel evaluation metric.
* Hernandez-Garcia, Dohare, Luo and Sutton, [Reinitializing weights vs units for
  maintaining plasticity in neural networks](https://proceedings.mlr.press/v330/hernandez-garcia26a.html),
  CoLLAs 2026, pp.776–806. This is the published version of the previously cited
  2025 preprint. Resetting parameters for plasticity and comparing reset resources
  are established. One-step classifier reset benefit is not evidence of sustained
  future plasticity.

## Consequence for the contribution

An empirical allocation audit needs evidence about actual structural choices:
the correspondence between full-package and zero-LoRA classifier-only decisions,
the independent role of optimizer state, pre-update versus local learning effects,
and conditions where these observations cease to hold. It must retain prediction
benefits of LoRA even when allocation is unchanged. Existing classifier-bias
literature explains why the mechanism is plausible; it does not by itself validate
this allocator's capacity interpretation or establish a defect in a named method.

The initial-loss ablation now supplies a boundary: all three BANKING canonical-order
development seeds preserve decisions, but the third Amazon seed changes 24 head-only
and 30 private-package decisions. The earlier all-zero pilot account cannot be
generalized to both regimes or used to claim that lookahead is always unnecessary.

## Author-source CABLE trace

Read-only inspection at author repository commit
`c72b9cfeb345c8d517f1266ceb2b0ebf8a02430e` found the top-level training calls in
`models/cable.py:352–369`: select a policy action, assign a batch to the selected
adapter, compute classifier cross entropy, use negative loss as reward, and update
the policy. `models/reinforcement.py:43–64` records categorical policy actions and
rewards; `finish_episode` contains the discounted-return/clipped PPO procedure.
The previously inspected virtual-step/Fisher-change helper and the paper's Eq.10
loss-ratio signal are distinct pieces. Merely transplanting one helper would not
reproduce the full author method. This trace is a source-faithfulness constraint,
not a performance result or an accusation that the published method is defective.
Exact downloaded source hashes are in the preserved author-source receipt; full
third-party source was neither executed nor copied into this repository.
