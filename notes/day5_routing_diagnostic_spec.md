# Day-5 label-free routing feasibility diagnostic

Frozen before new Day-5 live outcomes. This is exploratory engineering evidence,
not an additional claimed contribution or a method tuned on held-out data.

At the end of each segment evaluate three fixed inference rules, always predicting
over the full classifier label space: (1) the last active adapter, (2) a uniform
average of adapter probabilities, (3) nearest cosine centroid using frozen-base
mean-token embeddings. The centroid of an adapter is the normalized average
embedding of its stored training texts; ignore their labels. No concept, segment,
domain identity, incoming gold label, evaluation example or evaluation accuracy
is used to fit/select a routing rule. Compute centroids solely from current
training reservoirs. Preserve state and RNG around diagnostic evaluation.

Report each rule separately; never choose the best rule per concept or per seed
as a deployable result. Oracle adapter and concept-restricted accuracy remain
separate diagnostics. Evaluate the original fixed development sets. Report both
per-concept scores and the macro average over concepts already observed, with
that aggregation used only offline. No calibration or threshold search.
