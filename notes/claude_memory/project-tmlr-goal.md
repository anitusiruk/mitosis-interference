---
name: project-tmlr-goal
description: mitosis-interference repo goal = TMLR paper on what adapter-expansion triggers detect; work autonomously until told to stop
metadata:
  type: project
---
Goal: TMLR submission "Capacity or Classifier? What Expansion Triggers Detect in Task-Free Continual Adapter Learning" (branch tmlr-reframe; handoff.txt has full history). User wants continuous autonomous grinding until they say stop, periodic methodology/novelty audits with literature search, decently novel + methodologically robust, hardware-aware (single RTX 4090, 96 CPU, 251GB RAM, ~19GB free disk).

**Why:** user said "grind hard ... we go until i tell you to stop".
**How to apply:** keep pre-registration discipline (frozen hashed code in notes/tmlr_confirmation_prereg.md; extensions go in new files like src/tfcl/vision.py, experiments/tfcl_run_x.py, declared before confirmation seeds). Commit+push results periodically; GitHub is the only persistent storage. Datasets need HF_DATASETS_TRUST_REMOTE_CODE=1 (banking77). GPU OOM if >~12 concurrent jobs. See [[user-profile]].
