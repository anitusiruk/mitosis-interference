# Mitosis: Interference-Aware Adapter Expansion

Research question:

Can a task-free continual learner decide whether to reuse existing
LoRA capacity or allocate new capacity by estimating whether incoming
data can be safely absorbed?

Core distinction:

    novelty != interference

Initial project stages:

1. Measure distribution novelty.
2. Measure prospective interference.
3. Determine which signal predicts future forgetting.
4. Only then implement automatic adapter expansion.
