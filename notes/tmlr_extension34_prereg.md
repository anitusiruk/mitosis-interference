# Extensions 3 + 4 — ImageNet-R and exemplar-free prototype refresh (SDC)

Declared 2026-10-11 (session 3), before any run of these extensions with a confirmation seed.
At writing time: the primary study (q = 0.99) and extension-1 text results had been inspected;
extension 2 was running (about 5% of its runs complete; its results had NOT been analysed —
only the files of the development seed 2026 had been read). Development used seed 2026 only.
Frozen code of the primary study and of extensions 1-2 is unchanged; this adds new files only.

## Why (logic, not tuning)

Extension 2 tests whether expansion at classifier novelty helps when classifier statistics
cannot be refreshed (exemplar-free prototypes). Two threats remain:

1. **Refresh without exemplars.** If expansion helps exemplar-free learners because the
   prototypes of a package that keeps training go stale, then refreshing the prototypes
   without exemplars should recover part of the single package's accuracy and shrink the value
   of expansion. Semantic drift compensation (SDC; Yu et al., CVPR 2020) is the standard
   exemplar-free refresh, and continual adapter tuning with semantic-shift compensation (SSIAT;
   Tan et al., CVPR 2024) keeps a single shared adapter for this reason. We use SDC exactly as
   published (Gaussian-kernel interpolation of current-data drift at each prototype,
   L2-normalised embeddings, sigma = 0.3, the paper's default), applied after every update of
   the active package because a task-free stream has no tasks; sigma = 0.2 (the paper's
   CIFAR-100 value) and sigma = inf (uniform mean shift) are sensitivity rules.
   SDC changes no training computation, so it is a second inference rule on the same
   trajectory; its proto_ef equals extension 2's (verified bit-exactly in development).
2. **Canonical benchmark.** ImageNet-R (200 classes, ten groups of 20) is the standard
   class-incremental benchmark for pre-trained-model continual learning and is used by SEMA,
   EASE and Online-LoRA-type studies.

## Implementation (new files; sha256 at the end)

* src/tfcl/drift_comp.py — SDC mixin (rules proto_ef_sdc, proto_ef_sdc02, proto_ef_sdcinf).
* experiments/tfcl_run_x4.py — runner = tfcl_run_x3 (ImageNet-R stream) + --ef + SDC.
* experiments/tfcl_ext34.sh — the job lists below.
* experiments/tfcl_ext34_report.py — analysis.
ImageNet-R uses src/tfcl/vision_imnr.py / experiments/tfcl_run_x3.py (committed in session 2,
before this file), memory 512 as in every other stream (fixed global budget).

## Design

Part S (SDC; exemplar-free regime, --replay 0 --ef, runner tfcl_run_x4):
  streams banking_rec, banking_cil, clinc_cil, news_cil (seeds 2027-2031), cifar_cil
  (seeds 2027-2031); policies single, oracle, firstseg. Output results/tfcl/ext4_sdc.
  (Five seeds instead of ten: compute; development effects are 3-30 points.)
Part I (ImageNet-R imnr_cil, seeds 2027-2032):
  exemplar-based (replay 16; runner tfcl_run_x3): single, oracle, firstseg
      -> results/tfcl/ext3_imnr/exemplar
  exemplar-free (--replay 0 --ef; runner tfcl_run_x4): single, oracle, firstseg
      -> results/tfcl/ext3_imnr/ef
No triggers are run on ImageNet-R (compute; triggers are characterised on 15 other streams).

Decision rule (n = 5-6 seeds): a hypothesis is supported in a stream if the 95% paired
t-interval over seeds lies entirely on the predicted side of zero. Wilcoxon p is reported.
No multiplicity correction (each hypothesis is reported per stream, all streams shown).

## Hypotheses

* S1 (refresh). Single package: proto_ef_sdc > proto_ef, in each Part-S stream.
* S2 (refresh shrinks the value of expansion).
  (oracle - single | proto_ef_sdc) - (oracle - single | proto_ef) < 0, in each Part-S stream.
* I1. ImageNet-R, exemplar-based: oracle < single.
* I2. ImageNet-R, exemplar-based: oracle > firstseg.
* I3. ImageNet-R, exemplar-free: oracle > single (proto_ef).
* I4. ImageNet-R, within the exemplar-free runs:
  (oracle - single | proto_ef) - (oracle - single | proto_mean) > 0.
Descriptive: oracle - single under SDC (does refresh reverse the sign?), firstseg contrasts,
sigma sensitivity, all ImageNet-R contrasts.

## Development observations (seed 2026; recorded before freezing)

proto_ef -> proto_ef_sdc (sdcinf), --replay 0:
  banking_cil single .262 -> .420 (.412); oracle .566 -> .627; firstseg .606 -> .626
  banking_rec single .444 -> .728 (.685); oracle .738 -> .742; firstseg .675 -> .685
  clinc_cil   single .502 -> .473 (.553); firstseg .698 -> .716   (S1 AT RISK on clinc_cil)
Slow learner (lr 1e-4, banking_cil): single proto_ef .131, sdc .319; oracle .441; firstseg .607
  -> a lower learning rate did not reduce staleness; not part of the confirmation.
ImageNet-R (seed 2026): exemplar-based single .565, frozen .232 (memory prototypes; the
  full-stream frozen NCM is .463), firstseg .307; exemplar-free proto_ef single .365,
  oracle .397, random .304, firstseg .502. (Exemplar-based oracle: see below if completed.)
