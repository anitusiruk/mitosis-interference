---
name: project-audit-fixes
description: "session 4 (2026-10-12) — fixed external audit (\"astra\") of the TMLR paper; branch tmlr-audit-fixes, PR #8; extension 6 done and written up"
metadata:
  type: project
---

Repo at /workspace/tmlr-reframe (symlinked /workspace/mitosis-interference). Session-4 work on branch `tmlr-audit-fixes`, PR #8 to master (open, not merged).

Audit points (all addressed): Prop 1 zero-row scope; proto_ef vs proto_mean confounds; owned replay access; sign-flip overstatement; calibration wording; SEMA/NCM.

Extension 6 (prereg notes/tmlr_extension6_prereg.md, frozen 0771860) COMPLETE 2026-10-12 ~04:40 UTC: M1/M2/G1 supported on all 6 CIL streams; feature age = 75–98% of stored-vs-refreshed DiD (ImageNet-R ~half, sample support matters). FreshUtil cascades on shuffled CLINC/CIFAR/BANKING; exploratory X1 head inheritance kills it (41 -> 1.4). Paper section sec:res-controls + app:ext6 written; main text 12 pages, 18 total.

**Why:** user wants TMLR-ready + acceptance odds (last given ~80–85%).
**How to apply:** remaining risk is scale/length and author defence; next steps only if user asks (e.g. merge PR, anonymous build). Related: [[project-tmlr-goal]], [[feedback-stop-criterion]].
