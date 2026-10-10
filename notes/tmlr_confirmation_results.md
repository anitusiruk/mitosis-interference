# Confirmation study — results log (session 2)

Environment deviations (no effect on results; verified):
* New pod. Packages reinstalled at the pinned versions. Datasets re-downloaded; BANKING77 needs
  HF_DATASETS_TRUST_REMOTE_CODE=1 under datasets 3.6.0 (the loader is unchanged). A saved run
  (banking_rec single s2027) reproduced bit-for-bit (final proto_mean 0.8544746041297913),
  and the probe-restoration test passed. Frozen sha256 prefixes re-verified.
* Worker counts in experiments/tfcl_confirm.sh changed (6 -> 10 -> 8) for throughput; each
  run is an independent deterministic process, so this cannot change results. Some runs were
  restarted after interrupted grids; outputs are written only at completion.

## Interim (2026-10-10 ~03:00 UTC; development streams complete, held-out partial)

* H2 (expansion harms CIL): oracle - single = -8.2 (banking_rec), -11.4 (banking_cil),
  -10.0 (clinc_cil) points; 0 wins in every seed; loss_z / fresh_util / label_novel
  -4 to -10.5; all Holm-significant.
* H4: label_surprise never spawned in any CIL or DIL development stream -> identical to single
  (non-inferior).
* H3: amazon_dilconf oracle +1.9 [0.5, 3.3], label_surprise +2.1 [0.9, 3.3] (Holm-significant);
  amazon_conflict oracle +0.8 [-2.1, 3.8], label_surprise +1.0 [-1.9, 3.9] (NOT significant;
  development seed 2026 had shown +6). Random-timing expansion equals oracle on both drift
  streams (.615/.615, .582/.582).
* H1: fraction of loss_z / fresh_util spawns within 2 batches after a never-seen label:
  banking_cil 1.00/1.00, clinc_cil 1.00/1.00, but banking_rec 0.45/0.50 -> H1 FAILS on
  banking_rec as pre-registered.
* EXPLORATORY (post hoc, declared after seeing the H1 failure; experiments/tfcl_pkg_novelty.py):
  with *package-level* novelty (a label the newest package has never trained on; Proposition 1
  applies because its head row is zero), 100% of loss_z and fresh_util spawns fall within 2
  batches of package-level novelty in all CIL streams including banking_rec. Base rate of such
  batches among eligible batches: 0.27-0.30 (banking_rec), 0.25 (banking_cil), 0.15 (clinc_cil).
  Interpretation: in a recurrence stream, returning label groups are novel to the package
  spawned since they were last seen.
* Also notable: banking_rec random (.792) > oracle (.771): spawning exactly at label arrivals
  is worse than random timing.
