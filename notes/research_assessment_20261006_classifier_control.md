# Contribution boundary after the classifier control

Recorded UTC: 2026-10-07T02:40:00.796615+00:00
Verified static/classifier branch: adef3d8b56233396aeb07fb085fa3ba529dded57

BERT transfer: 20/20. Static pilots and confirmations: 44/44.
Frozen-pre-classifier controls: 20/20. Weight/state audits: 8/20 currently.
Remaining frozen audits are queued behind verified combined preservation and QC.

All ten frozen-pre-classifier pairs retain identical allocation sequences,
including spawn steps 18 and 50. These observed decisions require neither LoRA
updates nor hidden pre-classifier learning under this recipe. This does not
establish sufficient representation capacity generally or erase the storage
cost of multiple output classifiers. The centroid prediction difference is
negative; other rule intervals include zero. Do not generalize the original
trainable-stack LoRA benefit to this frozen-stack recipe.

Private LoRA-minus-output-classifier-only accuracy differences follow. Orders
are averaged within five training seeds; fixed development examples have been
repeatedly examined. These intervals are not population-sampling uncertainty.

```csv
rule,seed_clusters,mean,ci_low,ci_high
frozen_centroid,5,-0.0009856123258185,-0.0101155357106431,0.0081443110590061
last_active,5,-0.001152496027787,-0.0096391948653374,0.0073342028097634
uniform_probability,5,0.0016834792890662,-0.0067321820735988,0.0100991406517313
```

## Literature boundary

[LACE, arXiv:2603.28611v1](https://arxiv.org/html/2603.28611v1) already proposes
loss-driven expansion with a recent-loss baseline, spike threshold,
confirmation and cooldown. Its growing projection architecture differs from
the present private-classifier LoRA pool. Loss-driven expansion is not our
novelty. The current experiments neither reproduce LACE nor establish a defect
in it. A future comparison must preserve its complete detector and growth
semantics and clearly declare any text adaptation.

The candidate contribution is a controlled audit of classifier- and
optimizer-bearing allocation packages and their actual decisions. A factorial
design or probability factorization alone is insufficient novelty.
Source-faithful complete-method comparisons and a stronger natural same-label
learning regime remain outstanding.

## Submission assessment

[TMLR acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html) focus
on substantiated claims and useful findings communicated clearly. Benchmark
leadership and novel methods are not mandatory. Re-running a bespoke method
without generalizable lessons can still fail the interest criterion. The
criteria also caution about largely AI-produced papers with little human
involvement. The author needs to critically understand and review the
experiments and final arguments before submission.

Current readiness remains low. The audit route is plausible; adequate interest
and acceptance are not established. Complete the frozen seed coverage, inspect
regenerated figures and receipts, and address the complete-method and
natural-learning gaps before describing the paper as submission-ready.
