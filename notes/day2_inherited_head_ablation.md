# Day 2 Inherited-Head Ablation

Seed 2026.

Full-fresh CF:
- 2 spawns
- 3 final adapters
- B1 accuracy 0.1226
- C1 accuracy 0.2637
- B2 accuracy 0.3290

Inherited-head CF:
- 5 spawns
- 6 final adapters
- B1 accuracy 0.1226
- C1 accuracy 0.2234
- B2 accuracy 0.2968

Inherited-head routing still learned useful B/C capacity, showing that
resetting the classifier/pre-classifier to original initialization is
not required for the learning benefit.

However, the zero-cost decision became unstable:

B1:
- initial spawn advantage +0.18098
- redundant later spawn advantages +0.00203 and +0.00353

C1:
- initial spawn advantage +0.02750
- redundant later spawn advantage +0.00580

Interpretation:
Fresh-head reset is not necessary for specialization, but zero-cost
mean query loss comparison is too sensitive to tiny improvements when
fresh capacity inherits the existing head.

Next step:
Use paired per-example query-loss uncertainty and require confident
evidence that fresh capacity improves query loss before spawning.

No fresh-advantage threshold will be tuned from this seed.
