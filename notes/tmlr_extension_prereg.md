# Extension study — declared 2026-10-10, before any extension confirmation run

Written in session 2 (Claude). Before this file was committed, NO result of the primary
confirmation study (results/tfcl/confirm*, seeds 2027–2036) had been inspected by the
author of this file (only completion counts were checked), and no extension run with a
seed other than 2026 had been executed. Development of the extension used seed 2026
only (results/tfcl/vision_dev, results/tfcl/recon_dev, results/tfcl/tweet_dev).

The frozen files of notes/tmlr_confirmation_prereg.md are unchanged (sha256 verified at
the start of session 2). The extension adds new files only:

    src/tfcl/vision.py           ViT-B/16 (google/vit-base-patch16-224-in21k) encoder + CIFAR-100 streams
    src/tfcl/data_x.py           tweet_conc natural concept-drift stream
    experiments/tfcl_run_x.py    wrapper around the frozen runner (+ policy firstseg)
    experiments/tfcl_grid_x.py   grid runner for tfcl_run_x
    experiments/tfcl_extension_report.py   analysis below (committed with this file)
    experiments/tfcl_lace_openloop.py      open-loop LACE-style rule (XL)

(sha256 of these files at freeze time are listed at the end of this file.)

## Motivation (why the extension exists)

1. Generality: the primary study is text-only with small encoders. Most expansion work
   (SEMA, EASE, Online-LoRA) uses ViT-B/16 on image benchmarks.
2. An apparent contradiction: SEMA's ablation reports that self-expansion improves on
   first-session adaptation in class-incremental learning, while our development data show
   expansion below a single continually trained package. Development (seed 2026, text)
   suggests both are true: oracle > firstseg but oracle < single in CIL. The extension tests
   whether the value of expansion is baseline-dependent.
3. Realism of the drift positive control: all primary drift streams use synthetic label
   flips. tweet_conc is a naturally occurring change of annotation concept (TweetEval
   offensive -> hate -> irony -> offensive, shared label ids). Development showed only a
   small oracle advantage (+1.8 points, seed 2026), so it is reported descriptively.
4. Faithfulness of triggers: LACE (Tathe, 2026) reports 100% boundary precision for a
   loss-ratio rule with a published threshold (tau = 2.5). We evaluate that rule open-loop.

## Design

Seeds: 2027–2036 for text extensions; 2027–2034 for vision (8 seeds: the smallest number
for which a two-sided Wilcoxon signed-rank test can reach p < 0.01; compute is one RTX 4090
shared with the primary pipeline). Vision forward passes use bf16 autocast (decided before
any vision result was seen; all vision runs, including the seed-2026 null calibration,
use it). Seed is the unit of analysis. proto_mean final mean dev
accuracy is the endpoint, as in the primary study.

* XV (vision replication). Streams cifar_cil (CIL), cifar_dil (DIL), cifar_conf (DRIFT).
  Policies: frozen, single, oracle, random, firstseg, trigger:{label_novel, loss_z, repr_z,
  fresh_util, label_surprise} at q = 0.99 (thresholds: i.i.d.-null shadow traces, seed 2026,
  results/tfcl/vision_dev/shadow/report_seed2026.json). interf_logit, interf_proto and
  conflict_z are omitted for compute (the last two are failed development candidates).
  Rehearsal-free variant (--replay 0): single and oracle.
* XR (baseline dependence of expansion). Text streams of the primary study plus
  tweet_conc: policy firstseg (seeds 2027–2036); single and oracle with --replay 0
  (seeds 2027–2036); tweet_conc also single, oracle, random, frozen and the five triggers
  above (thresholds results/tfcl/tweet_dev/shadow/report_seed2026.json).
* XL (open-loop LACE-style rule) and open-loop AUROCs: single-package shadow traces for
  every text stream (incl. tweet_conc) on seeds 2027–2031 and vision streams on seeds
  2027–2029.

## Hypotheses (directional; paired seed-level t-CI + Wilcoxon, Holm within family)

* XV1. In cifar_cil, >= 80% of loss_z and fresh_util spawns fall within 2 batches after a
  batch with a never-seen label (pooled over seeds).
* XV2. In cifar_cil: oracle < single; loss_z, fresh_util, label_novel pools < single.
* XV3. In cifar_conf: oracle > single and label_surprise > single.
* XV4. label_surprise is non-inferior to single (lower 95% bound > -1.0 point) in cifar_cil
  and cifar_dil. label_novel spawns nothing in cifar_dil / cifar_conf.
* XR1. In every CIL stream (banking_rec, banking_cil, clinc_cil, news_cil, cifar_cil):
  oracle > firstseg (expansion beats first-session adaptation).
* XR2. In every CIL stream, without training replay: oracle < single (the harm of
  expansion in CIL does not depend on rehearsal).

Descriptive only (no hypothesis): tweet_conc contrasts; difference-in-differences of the
expansion effect with vs. without replay; XL firing counts (fraction of firings within 2
batches of label novelty in CIL, firings within 2 batches of a segment change in DIL/DRIFT);
open-loop AUROCs on confirmation seeds; all other contrasts.

Deviations will be recorded in notes/tmlr_extension_results.md.
