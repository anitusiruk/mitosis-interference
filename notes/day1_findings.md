# Day 1 Findings

## Research question

Should task-free continual-learning capacity expansion be triggered by
distribution novelty, or by evidence that existing capacity cannot
safely absorb an incoming update?

Working principle:

    novelty != destructive interference

and therefore:

    novelty != automatic need for expansion


## Experiment 1: Natural BANKING77 stream

A continuous BANKING77 stream was trained without automatic expansion.

Every 10 steps, four candidate signals were measured before the real
training update:

1. current loss
2. frozen-representation novelty
3. gradient conflict
4. one-step virtual-update interference

The target was actual future damage to a protected memory set after
additional real training updates.


### Harm prediction results

Signal                  AUROC    AUPRC    Pearson r
---------------------------------------------------
Current loss            0.4651   0.5118   -0.3910
Novelty                 0.5697   0.5709   +0.0711
Gradient conflict       0.7462   0.7358   +0.5901
Virtual interference    0.7200   0.7264   +0.6073

Novelty was only weakly informative about future forgetting.

Gradient conflict and virtual-update interference contained
substantially more information about subsequent protected-memory harm.


## Experiment 2: Controlled 2x2 stress test

We independently manipulated:

1. representation/input novelty
2. label conflict

Conditions:

- familiar + safe
- novel + safe
- familiar + conflict
- novel + conflict

Two independent seeds were run with eight paired trials per seed.

Baseline protected-memory accuracy was approximately 95-96% before
stress adaptation.


### Paired effects across trials

Safe novelty effect:

    mean = +0.0246
    bootstrap 95% CI = [+0.0111, +0.0388]

Familiar conflict effect:

    mean = +0.9468
    bootstrap 95% CI = [+0.7493, +1.1427]

Novel conflict effect:

    mean = +0.1365
    bootstrap 95% CI = [+0.0980, +0.1737]

Average conflict effect:

    mean = +0.5417
    bootstrap 95% CI = [+0.4492, +0.6319]


## Interpretation

The novelty manipulation is not perfectly harmless: it produces a
small measurable increase in protected-memory loss.

However, the average conflict effect is roughly 22 times larger than
the safe novelty effect.

The controlled and observational experiments therefore support the
same qualitative conclusion:

    Distribution novelty is a weak proxy for destructive interference.

A continual learner should not allocate new capacity merely because
incoming inputs are distributionally different.

The more relevant question is whether the currently available
parameters can safely absorb the update.


## Important limitations

These are exploratory Day-1 experiments, not publication-level results.

Only BANKING77 has been tested.

Only two controlled random seeds have been run.

The controlled novelty manipulation appends unrelated semantic context
and may alter optimization in ways beyond pure distribution novelty.

Bootstrap intervals are over paired trials, not enough independent
dataset/model seeds to establish broad generalization.

The current one-step gradient-conflict and virtual-update measurements
are informative but not yet sufficiently reliable to directly control
adapter expansion.

The virtual step currently approximates adaptation using a simple
gradient step rather than an exact multi-step cloned AdamW trajectory.


## Day 1 conclusion

The core research hypothesis survives initial testing.

Proceed to Day 2.

The next problem is no longer whether novelty and interference are
different.

The next problem is:

    Can destructive interference be predicted reliably enough,
    before adaptation, to decide whether an existing LoRA adapter
    should absorb an incoming window or new capacity should be spawned?


## Day 2 candidates

Evaluate prospective interference estimators including:

- persistent / EMA gradient conflict
- multi-batch gradient conflict
- multi-step counterfactual adaptation
- optimizer-aware AdamW counterfactual adaptation
- interference measured over multiple protected subsets

Automatic adapter spawning should not be implemented until a predictor
is sufficiently reliable.
