# Implementation checks before research outcomes

The four-factor audit's first CPU gate failed the equality check against the
original coupled fresh-head cell. The original code computed mean cross entropy
directly, while the new audit averaged separately computed per-example losses.
These mathematically equivalent reductions can differ at float32 precision.
The audit now computes its aggregate loss using the original reduction and also
saves per-example losses. The repaired CPU gate passed all 16 restoration checks,
initializer/state transport checks, real-update equality, odd-batch coverage and
cell-order invariance. The failed and passing logs are retained.

The BERT gate's first attempt called the shared-head pool's `intervention` API on
the private pool, whose API is `shadow_reuse`. The test call was corrected; the
learner and allocation implementation did not change. Preserve both attempts.

The report is tested on synthetic known main effects and a known two-factor
interaction, with unequal fold sizes and five paired seed clusters. A single
unpaired order must not contribute a seed interval. Synthetic data are temporary
test fixtures and never enter the research result tables.

Research launch additionally requires passing CUDA gates and an explicit BERT
backbone revision/file-hash manifest. Passing tiny tests does not prove the full
scientific methodology. The Day-15 observer must reproduce the paired final
learner state and adapter tensors bitwise on the full real stream; discrepancies
halt execution and remain in the repository.
