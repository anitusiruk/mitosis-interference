# Day 4 — CAU-v1 Cross-Regime Development Conclusion

Date: 2026-10-04

Status: DEVELOPMENT RESULT — SEED 2026 ONLY

Amazon same-label regime:
- 79 / 80 learning updates
- 1 DEFER
- 0 permanent spawns
- 1 final adapter
- preserved shared recurrence
- held-out trajectory approximately recovered to V3

BANKING77 disjoint-label regime:
- 80 / 80 batches learned
- 0 DEFER
- spawn B specialist at step 18
- spawn C specialist at step 50
- A1 and A2 use default capacity
- B1 uses adapter_1 after confirmation
- B2 reuses adapter_1 on recurrence
- C1 uses adapter_2 after confirmation
- 3 final adapters

Final BANKING held-out specialization:
- default on A: accuracy 0.2096
- adapter_1 on B: accuracy 0.3065
- adapter_2 on C: accuracy 0.2747

Interpretation:
The same frozen CAU-v1 policy avoids unnecessary expansion in the shared-transfer Amazon regime while creating and reusing specialized capacity in BANKING77.

Important limitations:
- seed 2026 is development-only
- BANKING fresh capacity includes fresh LoRA + fresh pre-classifier + fresh classifier
- two-window confirmation remains a heuristic persistence filter
- held-out oracle adapter evaluation is not task-free inference
- fresh-seed confirmation is required

No controller threshold or rule is changed after this result.
