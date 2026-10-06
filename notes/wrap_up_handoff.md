# User-requested project wrap

Stopped 2026-10-06T05:43:12.745719+00:00. The active trajectory finished and saved its final checkpoint; the paused dispatcher was terminated before any further launch. The waiting bounded-memory routing driver was stopped. No ongoing GPU study is intended.

Primary seed/order study: 80/80. MultiNLI stress test: 24/24. Original learned-router study: 110/110 checkpoints. Later study coverage: [{"study": 8, "completed": 12, "planned": 44}, {"study": 10, "completed": 8, "planned": 12}, {"study": 12, "completed": 2, "planned": 11}].

Unlaunched frozen controls are listed in remaining_frozen_jobs.json. Their method/data protocols remain frozen. A subsequent session must supply a new deadline; the original dispatchers have expired hard-coded deadlines and refuse existing outputs. Never overwrite completed results or erase failed logs. The bounded-memory learned-router extension is implemented and declared but not executed.

All completed learner weights, optimizers, RNG and reservoirs are versioned through Git LFS. The complete offline archive contains the Git bundle and every local LFS object. A bundle alone does not contain model tensors. Preserve the complete archive before terminating the pod.

Current findings and limitations are in research_progress.md and paper_working_draft.md. Neither is a submission-ready paper. GitHub push status is recorded separately after the actual attempt.
