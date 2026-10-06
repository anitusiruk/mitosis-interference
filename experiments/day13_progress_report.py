"""Regenerate a concise research handoff from verified saved outputs."""
from datetime import datetime,timezone
import json
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table

def table(path,columns=None):
    p=Path(path)
    if not p.exists():return 'Pending; no saved completed-result table yet.'
    try:d=pd.read_csv(p)
    except pd.errors.EmptyDataError:return 'Pending; no complete fresh-seed comparison groups yet.'
    if d.empty:return 'Pending; no complete comparison groups yet.'
    if columns is not None:d=d[columns]
    return markdown_table(d)

counts=[]
for day,expected in [(5,6),(6,80),(7,24),(9,110),(8,44),(10,12),(12,11)]:
    path=Path(f'logs/day{day}_'+('routing_status.json' if day==9 else 'queue_status.json'))
    records=json.loads(path.read_text()) if path.exists() else []
    counts.append({'study':str(day),'completed':sum(x['status']=='completed' for x in records),
                   'planned':expected,'last_status':records[-1]['status'] if records else 'not launched'})
fixed_router=Path('logs/day14_fixed_memory_routing_status.json')
if fixed_router.exists():
    records=json.loads(fixed_router.read_text())
    counts.append({'study':'14 fixed-memory routing','completed':sum(x['status']=='completed' for x in records),
                   'planned':44,'last_status':records[-1]['status'] if records else 'not launched'})
diagnostics=Path('notes/day15_16_execution_status.json')
if diagnostics.exists():
    records=json.loads(diagnostics.read_text())['jobs']
    for study in [15,16]:
        part=[x for x in records if x['study']==study]
        counts.append({'study':str(study),'completed':sum(x['status']=='completed' for x in part),
                       'planned':20,'last_status':part[-1]['status'] if part else 'not launched'})
head=Path('logs/day5_head_only_queue_status.json')
if head.exists():counts.append({'study':'5 head-only','completed':sum(r['status']=='completed' for r in json.loads(head.read_text())),
                               'planned':2,'last_status':json.loads(head.read_text())[-1]['status']})
report=['# Research progress and evidence handoff','',
    'Generated '+datetime.now(timezone.utc).isoformat()+'. This is a development report, not a submission-ready paper.','',
    '## Decision','',
    'Carry forward the mechanistic audit and the original private-package implementation as a reference. '
    'The present results do not establish that the allocation policy identifies a need for new LoRA capacity, '
    'or that it improves deployable accuracy across these regimes. The useful candidate contribution is a '
    'controlled account of classifier resets, optimizer state, prospective learning gain, and inference routing. '
    'Modern source-faithful comparators and stronger same-label learning regimes are still required.','',
    '## Verified study coverage','',markdown_table(pd.DataFrame(counts)),'',
    'Complete trajectories alone enter summaries. A queue record is an execution status; the independent '
    'evidence audit also checks the saved trajectory summary, full step count and final metrics.','',
    '## Primary five-seed results','',
    'Seeds 2027–2031 each have canonical and B-first orders. Average both orders within a seed before '
    'descriptive 95% Student-t intervals. Fixed development examples define the scope; windows and orders '
    'are not independent replicates. All three fixed routing rules are reported. Macro accuracy averages '
    'three concept-level accuracies; it is not BANKING per-class macro accuracy.','',
    table('results/day6_seed_cluster_summary.csv',['regime','rule','architecture','policy','seed_clusters','mean','ci_low','ci_high']),'',
    table('results/day6_paired_differences.csv'),'','',
    '## Mechanism','',
    'On the original BANKING trajectory, fresh classifier reset with reused LoRA yielded substantially larger '
    'held-out one-step loss gains than replacing LoRA under a fresh classifier. The factorial changes both '
    'component weights and their corresponding AdamW moments, so it does not identify weights independently '
    'of moments. About 87% of fresh-versus-best-reuse utility at both spawn steps was an initial predictor '
    'gap, before the proposed update. Initial gap itself changes the whole package, not only the head.','',
    'The BANKING private and zero-LoRA head-only controllers made identical adapter/decision sequences '
    'across all ten fresh-seed/order trajectories. LoRA training improved classifier performance despite '
    'these identical structural decisions. Do not conflate prediction benefit with allocation necessity.','',
    table('results/day13_head_allocation_comparison.csv'),'','',
    'The closed-loop pre-update ranking sensitivity preserves prospective AdamW retention guards. '
    'Its original seed-2026 pilots made no allocation changes. This does not show that all lookahead '
    'computation is unnecessary: prospective protected-memory checks remain. Later pilot seeds are shown below.','',
    table('results/day10_initial_loss_comparison.csv'),'','',
    '## Third regime and deployment','',
    'MultiNLI uses only training data, with normalized-premise-grouped development holdout, genuine paired '
    'tokenization and sharp/blurry transitions that preserve examples. Three seeds and two boundary variants '
    'are descriptive transfer checks. The 64-token, 1440-example stress test produces low learning; allocation '
    'often performs near balanced chance (one third). It is not a competitive NLI benchmark.','',
    table('results/day7_multinli_comparison.csv',['seed','condition','architecture','policy','rule','macro_accuracy','updates','adapters']),'','',
    'A standard linear router was added after the initial routing failure, then frozen before its own outcomes. '
    'It learns past adapter ownership from training reservoir texts without true task IDs or class labels. '
    'Both hard routing and probability mixture are auxiliary development outcomes; their use is not a new '
    'routing contribution or a reproduction of L2R/HESTIA. Checkpoint reload checks compare nine aggregate '
    'sample counts and accuracies, not previously saved per-example prediction vectors.','',
    table('results/day9_routing_paired_differences.csv'),'','',
    '## Resource sensitivities','',
    'The fixed-memory extension limits total stored training examples to 512 and preserves 64-example probes. '
    'It also caps the pool at eight. The rank-96 single baseline was selected by parameter arithmetic near '
    'three rank-8 private packages; it is not universally parameter matched to an uncapped growing pool. '
    'Memory, head storage, optimizer state, active-update compute and inference compute remain separate resources. '
    'Poor rank-96 performance under the shared fixed recipe does not establish superiority over a tuned '
    'larger static baseline; baseline-specific tuning with pilot/confirmation separation remains necessary.','',
    table('results/day8_memory_paired_differences.csv'),'','',
    table('results/day12_capacity_paired_differences.csv'),'','',
    '## Fixed-memory learned routing and extended attribution','',
    table('results/day14_memory_routing_paired_differences.csv'),'','',
    'The Day-15 observer independently crosses LoRA/head weights with LoRA/head AdamW state. '
    'All mature batches and every cell are retained. Only verified bitwise paired trajectory/state '
    'reproductions enter its causal summaries. The Day-16 BERT check tests transfer beyond the '
    'DistilBERT classifier stack; multiple backbone components change together, so it does not '
    'isolate classifier architecture causally. Both studies are development extensions, not untouched '
    'test confirmations. Current novelty limits are in notes/novelty_audit_20261006.md.','',
    table('results/day15_seed_intervals.csv'),'','',
    table('results/day16_bert_allocation_pairs.csv'),'','',
    '## Methodological checks and limits','',
    'The shared-head, component, head-only, stream-order, MultiNLI data, fixed-memory and scoring integrity '
    'tests passed in the live environment. Original BANKING/Amazon Day-4 routing was reproduced with zero '
    'disagreements. Complete shadow transactions were checked against exact parameter, optimizer, RNG '
    'and reservoir restoration in their declared test scope. Legacy private probes clear stale gradients; '
    'the next real training update clears them anyway. Do not claim that all legacy probes restore gradient flags.','',
    'The frozen retention rule is harm_LCB <= 0 with z=1.96. It permits small positive mean harm on some '
    'Amazon probes and is not a 95% no-forgetting guarantee or an anytime-valid repeated-test procedure. '
    'No threshold has been retuned to fix that interpretation. Day-2 strict robustness failure and '
    'Day-4 v0 starvation remain recorded failures.','',
    'Official tests were not used in these live experiments. Earlier BANKING exploratory work did use '
    'official test data before the clean development protocol; disclose this history in the paper. '
    'Do not describe BANKING official test as never observed. MultiNLI official validation remains unused.','',
    'The normalized-text and token-truncation audit is an additional offline diagnostic of the existing '
    'split. If it finds overlap, retain these original results and declare a grouped split as a new protocol '
    'rather than silently filtering an outcome-selected subset.','',
    table('results/day13_split_audit.csv',['regime','seed','normalized_train_dev_unique_overlap',
          'truncated_token_train_dev_unique_overlap','training_fraction_over_64_tokens','development_fraction_over_64_tokens']),'','',
    '## Reproduction and preservation','',
    'The working branch is day5-causal-audit; master remains the restored Day-4 reference. All live trajectories '
    'record source hashes, package versions, stream hashes and saved final learner state. The older model-revision '
    'field is null; exact historical backbone identity was not recorded. The restart records an explicit '
    'Hugging Face commit and backbone file hashes, and verifies saved aggregate predictions and losses before '
    'new outcomes. This numerical reload check does not prove historical byte identity. '
    'The saved GitHub snapshot and all 738 checkpoint files were successfully restored on the new pod; '
    'notes/github_save_verification.json records the earlier authenticated save. Source-only archives and '
    'Git bundles omit LFS tensor content. New work requires its own successful GitHub save before pod shutdown.','',
    'To recover committed history from the final bundle:','',
    '```bash\ngit clone mitosis-research-final.bundle mitosis-interference\ncd mitosis-interference\n'
    'git checkout day5-causal-audit\nexport PYTHONPATH="$PWD"\n```','',
    'Regenerate analyses with the corresponding experiments.day5_report, day6_diagnostic_report, '
    'day7_multinli_report, day9_routing_report, day8_fixed_memory_report, day10_mechanism_report, '
    'day12_capacity_report, day13_evidence_audit and day13_progress_report modules. Scientific plots are '
    'generated by experiments.day13_evidence_figures. Do not rerun existing output directories.','',
    '## Remaining research schedule','',
    '1. Complete the frozen controls and independently inspect data/implementation audits.\n'
    '2. Reproduce the closest CABLE signal and at least one modern structural method from verified author code; '
    'keep task-boundary-informed conditions separate.\n'
    '3. Run longer same-label adaptation regimes with useful fixed-baseline learning; freeze router and resource '
    'protocol before new confirmation seeds.\n'
    '4. Separate head-weight reset from moment reset and test an intervention whose structural interpretation '
    'matches its claimed capacity resource.\n'
    '5. Only after complete-method freeze, run held-out evaluation with the earlier BANKING exposure disclosed, '
    'dedicated resource measurement and external baselines.\n'
    '6. Write a claim-supported paper and author verification record. The fifteen-day plan is a planning budget, '
    'not a reason to submit unsupported findings.','',
    '## Day-5 tracker','',
    'Causal audit: complete. Core LoRA-specific allocation claim: not established. Seed/order diagnosis: '
    'complete. Third-regime stress test: complete but low learning. Further controls: coverage table above. '
    'Modern baselines, complete-method confirmation and submission readiness: pending.']
Path('notes/research_progress.md').write_text('\n'.join(report)+'\n')
print('PROGRESS_REPORT_SAVED',flush=True)
