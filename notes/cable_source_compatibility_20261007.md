# CABLE source compatibility review

Inspected author repository `https://github.com/jjul482/CABLE` at commit
`c72b9cfeb345c8d517f1266ceb2b0ebf8a02430e`. All tracked files were downloaded
and matched a SHA-256 manifest. The author implementation was not executed.
This is a source inspection, not a reproduction, performance comparison, or
finding about the published method's experimental validity.

## Observed reproduction requirements

* The default entry point requests `exps/cable_cifar10_clip.json`; that file,
  an `exps` directory, dependency specification, and explicit license are
  absent from the inspected tracked tree. An original configuration and
  dependency versions are required before attempting reproduction.
* `Learner.incremental_train` uses task increments, known/total class counts,
  and current-task class-restricted training datasets. This is a different
  information condition from the present boundary-free recurrent stream.
  A text adaptation must disclose that change rather than quietly removing
  task and class information.
* `ClippedPPO.assign_class_to_adapter` calls `assign_batch` on an element of
  `backbone.cur_adapter`. The supplied `Adapter` class has no such method,
  and no `assign_batch` definition appears in the downloaded tree. Resolve
  this interface with the original implementation before calling a port
  source-faithful.
* The supplied learner averages image inputs over the batch dimension for
  the policy state and sets a linear policy input dimension of 224. Its
  intended state shape must be established from an original configuration
  and a small replay before using text features.
* The training loop selects one action, adds one reward, and immediately
  updates the policy. The provided episode update normalizes returns using
  the default sample standard deviation. With one return, that statistic
  is undefined. This is a static numerical concern to resolve in a real
  author-setting replay; no execution outcome has been inferred.

## Consequence for this project's claims

The existing equation-level loss-ratio comparator remains a signal ablation.
It is not full CABLE: the policy, adapter interfaces, task/class condition,
classifier construction, training schedule, and resource accounting have not
been reproduced. Preserve this boundary in the manuscript and result tables.
Do not replace these components with convenient defaults and report the
result as an official-method reproduction.

A reproduction gate needs an original configuration, a complete dependency
and interface record, a shape-valid state/action/reward trajectory, finite
policy updates, and an author-setting learning curve. Any necessary repair
must have its own patch, provenance, and explicit adapted-method label.

This review was added after development outcomes. It changes no training
recipe, completed checkpoint, or comparator outcome. Source files are kept
in a temporary inspection directory; no author code is redistributed here.

