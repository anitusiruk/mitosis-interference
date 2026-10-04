# Day 3 Cross-Regime Counterfactual Action-Utility Result

Date: 2026-10-04

Status:
DEVELOPMENT RESULT.

All action-utility definitions and the two-window diagnostic were
committed before observing these results.

The scorer remained observational and did not alter the real V3
training trajectory.

# 1. Research question

Can system-level prospective action utility distinguish:

1. a distribution/domain shift that should be handled through
   shared adaptation;

from

2. a shift for which isolated fresh capacity is genuinely useful?

The two development regimes are intentionally contrasting:

Amazon:
- same binary labels across natural product domains
- shared default adapter learned all domains strongly

BANKING77:
- disjoint label groups
- earlier counterfactual experiments showed benefits from
  specialized B and C capacity

# 2. Amazon result

Schedule:
A1 -> B1 -> A2 -> C1 -> B2

Domains:
A = home
B = apparel
C = drugstore

Shared labels:
negative / positive

Eligible windows:
73

Fresh-positive:
4 / 73

Two-window confirmed:
0

By segment:

A1:
- eligible 12
- fresh-positive 3
- confirmed 0
- mean fresh utility -0.02635

B1:
- eligible 16
- fresh-positive 0
- confirmed 0
- mean fresh utility -0.10876

A2:
- eligible 16
- fresh-positive 0
- confirmed 0
- mean fresh utility -0.31424

C1:
- eligible 16
- fresh-positive 1
- confirmed 0
- mean fresh utility -0.27700

B2:
- eligible 13
- fresh-positive 0
- confirmed 0
- mean fresh utility -0.20188

Important event:

At B2 step 71 V3 had no safe reuse and therefore spawned.

However:

fresh utility = -0.42014

Therefore:

no safe reuse != fresh capacity is useful.

The appropriate action under the common-baseline formulation is
DEFER / leave the current learner unchanged.

# 3. BANKING77 result

Schedule:
A1 -> B1 -> A2 -> C1 -> B2

Eligible windows:
73

Fresh-positive:
25 / 73

Two-window confirmed:
23

By segment:

A1:
- eligible 12
- fresh-positive 0
- confirmed 0
- mean fresh utility -0.49870

B1:
- eligible 16
- fresh-positive 9
- confirmed 8
- mean fresh utility +0.11571
- mean fresh advantage +0.06749

A2:
- eligible 16
- fresh-positive 0
- confirmed 0
- mean fresh utility -1.37203

C1:
- eligible 16
- fresh-positive 16
- confirmed 15
- mean fresh utility +1.55461
- mean fresh advantage +1.42324

B2:
- eligible 13
- fresh-positive 0
- confirmed 0
- mean fresh utility -0.51626

Fresh-positive BANKING windows are therefore concentrated exactly in:

- early B1
- all C1

There are no fresh-positive windows in:

- A1
- A2 recurrence
- B2 recurrence

# 4. Cross-regime contrast

Amazon:
- fresh-positive 4 / 73
- confirmed 0

BANKING77:
- fresh-positive 25 / 73
- confirmed 23

BANKING confirmation localization:

B1:
8 confirmed

C1:
15 confirmed

A1/A2/B2:
0 confirmed

This is the primary Day-3 mechanistic result.

# 5. Interpretation

The result supports the hypothesis that:

distribution shift,
prospective interference,
and need for new parameter capacity

are distinct quantities.

Amazon contains natural domain shifts but strong positive shared
transfer. Fresh-capacity evidence is sparse and transient.

BANKING77 contains shifts for which prior experiments showed
specialized capacity to be beneficial. Fresh-capacity evidence is
sustained specifically in B1 and C1 and disappears on recurrence.

The action-utility diagnostic does not use concept or segment IDs.

Those labels are evaluation metadata only.

# 6. Important limitations

This remains development evidence.

Seed 2026 has been repeatedly inspected.

No statistical independence is claimed across batch-level windows.

The run/seed is the future inferential unit.

BANKING77 fresh capacity currently includes:

- fresh LoRA
- fresh pre-classifier
- fresh classifier

Therefore this result does NOT yet establish that fresh LoRA
representation capacity alone is required.

A shared-head causal audit remains mandatory.

Two-window confirmation is stabilization machinery, not claimed
novelty or a formal sequential guarantee.

No magnitude threshold was tuned.

# 7. Current conclusion

The diagnostic is strong enough to justify testing one live
action-utility controller.

It is NOT sufficient to freeze the final method.

Before final claims the method still requires:

- shared-head / LoRA-only isolation
- fresh-seed replication
- fixed-total-memory comparison
- blurry/interleaved streams
- task-free inference
- modern baselines
- compute/resource accounting
- untouched confirmatory evaluation
