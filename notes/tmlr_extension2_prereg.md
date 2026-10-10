# Extension 2 — the exemplar-free regime (regime map). Draft; frozen when committed with hashes.

Written in session 2. At writing time the primary confirmation results for the development
streams had been inspected (interim log in notes/tmlr_confirmation_results.md); extension-1
first-segment and partial rehearsal-free results had been inspected. No extension-2 run with
a seed other than 2026 had been executed.

## Rationale (logic, not tuning)

Rehearsal-free pre-trained-model learners (APER/ADAM, EASE, SEMA) keep no exemplars, so a
class prototype is the mean of features computed when the class was observed and is never
recomputed. If the package that produced those features keeps training, the prototypes of
earlier classes become stale (feature drift); a frozen package's prototypes stay valid. Hence:

* In an exemplar-based learner, the classifier statistics can be refreshed under the current
  package, and the cost of continued training is small: expansion buys little and fragments
  training data (primary study: expansion hurts in CIL).
* In an exemplar-free learner, freezing a package when new classes arrive preserves the
  validity of the prototypes recorded so far: expansion at (package-level) label novelty
  should help, and a trigger that never spawns in CIL (LabelSurprise) should do badly.

The value of a trigger that detects label novelty is therefore regime-dependent. Proposition 1
says what loss-type triggers detect; this extension tests when that is the right moment to
expand.

## Implementation

src/tfcl/exemplar_free.py (mixin; records per-package running class sums of normalised
features at observation time; rule proto_ef), experiments/tfcl_run_x2.py (adds --ef to
tfcl_run_x; otherwise identical), experiments/run_jobs.py (job runner). Training uses
--replay 0 (no rehearsal in the loss). Endpoint: final mean dev accuracy under proto_ef.
Triggers are re-calibrated for this regime: thresholds are the q = 0.99 quantiles of each
statistic on i.i.d.-shuffled null shadow traces run with --replay 0, seed 2026
(results/tfcl/ef_dev/shadow/report_seed2026.json), because the statistics depend on the
training trajectory, which --replay 0 changes (--ef does not change training).

## Design

Streams: banking_rec, banking_cil, clinc_cil, news_cil (CIL); amazon_dil, senti_dil (DIL);
amazon_dilconf, senti_conf (DRIFT); cifar_cil, cifar_dil, cifar_conf (vision).
Seeds: 2027–2036 (text), 2027–2034 (vision).
Policies (all with --replay 0 --ef): single, oracle, random, firstseg,
trigger:{label_novel, loss_z, label_surprise} at q = 0.99.

## Hypotheses (paired seed-level t-CI + Wilcoxon; Holm within family)

* R1 (regime flip). In every CIL stream (4 text + cifar_cil), under proto_ef: oracle > single.
* R2 (interaction, isolating the refresh factor). Every extension-2 run also reports the
  exemplar-based rule proto_mean on the identical trajectory. In every CIL stream:
  (oracle - single | proto_ef) - (oracle - single | proto_mean) > 0 (paired by seed).
* R3 (triggers). In every CIL stream, under proto_ef: loss_z > label_surprise.
* R4 (timing). In every CIL stream, under proto_ef: oracle > random.

Descriptive: DIL and DRIFT streams; firstseg; label_novel; package counts.

[development observations and hashes appended at freeze]
