"""Secondary development retention summaries from saved deployed predictions.

Added after primary development outcomes. No new training, final-test use, or
changes to the pilot-only learning-rate selection. Recurrence deltas are not
the standard backward-transfer statistic for a nonrecurring task sequence.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval

RULES = ['last_active', 'uniform_probability', 'frozen_centroid']
METRICS = ['final_macro_accuracy', 'mean_seen_checkpoint_accuracy',
           'maximum_seen_checkpoint_drop', 'final_minus_first_exposure']


def summarize(folder):
    p = json.loads((folder / 'provenance.json').read_text())
    s = json.loads((folder / 'summary.json').read_text())
    route = pd.read_csv(folder / 'routing.csv')
    d = pd.read_csv(folder / 'label_free_eval.csv')
    assert s['status'] == 'completed' and s['steps'] == 80 and len(route) == 80
    endpoints = set(route.groupby('segment').step.max())
    assert len(endpoints) == 5 and max(endpoints) == 80
    assert set(d.step) == endpoints and set(d.rule) == set(RULES)
    assert set(d.concept) == {'A', 'B', 'C'} and len(d) == 45
    assert np.isfinite(d.accuracy).all() and d.accuracy.between(0, 1).all()
    concepts, summaries = [], []
    for rule, predictions in d.groupby('rule'):
        for step, checkpoint in predictions.groupby('step'):
            assert len(checkpoint) == 3
            seen = set(route.loc[route.step <= step, 'concept'])
            assert set(checkpoint.loc[checkpoint.seen_concept, 'concept']) == seen
        first_steps = {}
        for concept, group in predictions.groupby('concept'):
            assert len(group) == 5 and group.n.nunique() == 1
            first = int(group.loc[group.checkpoint.str[0] == concept, 'step'].min())
            first_steps[concept] = first
            final = float(group.loc[group.step == 80, 'accuracy'].iloc[0])
            initial = float(group.loc[group.step == first, 'accuracy'].iloc[0])
            best = float(group.loc[group.step >= first, 'accuracy'].max())
            concepts.append({'rule': rule, 'concept': concept, 'first_exposure_checkpoint': first,
                'first_exposure_accuracy': initial, 'final_accuracy': final,
                'maximum_seen_accuracy': best, 'maximum_seen_checkpoint_drop': best-final,
                'final_minus_first_exposure': final-initial})
        part = pd.DataFrame([r for r in concepts if r['rule'] == rule])
        seen_curve = predictions[predictions.seen_concept].groupby('step').accuracy.mean()
        assert len(seen_curve) == 5
        summaries.append({'rule': rule, 'final_macro_accuracy': part.final_accuracy.mean(),
            'mean_seen_checkpoint_accuracy': seen_curve.mean(),
            'maximum_seen_checkpoint_drop': part.maximum_seen_checkpoint_drop.mean(),
            'final_minus_first_exposure': part.final_minus_first_exposure.mean()})
    return p, summaries, concepts


def main():
    rows, concept_rows, comparisons, coverage, hashes = [], [], [], [], {}
    selected_path = Path('notes/day17_static_rate_selection.json')
    selection = json.loads(selected_path.read_text()) if selected_path.exists() else None
    for regime in ['banking', 'amazon']:
        for seed in range(2027, 2032):
            for order in ['canonical', 'b_first']:
                names = {'adaptive': f'day8_{regime}_private_cau_seed{seed}_{order}_fixed512',
                         'static_rank8_frozen': f'day6_{regime}_private_single_seed{seed}_{order}'}
                if regime == 'banking' and selection:
                    for rank in [8, 96]:
                        rate = selection['selected_rates'][str(rank)]
                        names['static_rank' + str(rank) + '_tuned'] = (
                            f'day17_confirm_rank{rank}_lr{int(round(rate*1e6))}_seed{seed}_{order}')
                groups, streams = {}, {}
                for method, name in names.items():
                    folder = Path('results', name)
                    if not (folder / 'summary.json').exists() or json.loads((folder / 'summary.json').read_text())['status'] != 'completed':
                        coverage.append({'regime': regime, 'seed': seed, 'order': order,
                                         'method': method, 'status': 'missing_or_incomplete'})
                        continue
                    p, values, concepts = summarize(folder)
                    streams[method] = p['stream_sha256']
                    groups[method] = {r['rule']: r for r in values}
                    metadata = {'regime': regime, 'seed': seed, 'order': order, 'method': method, 'run': name}
                    rows.extend({**metadata, **r} for r in values)
                    concept_rows.extend({**metadata, **r} for r in concepts)
                    coverage.append({**metadata, 'status': 'completed'})
                    for name in ['provenance.json', 'routing.csv', 'label_free_eval.csv']:
                        hashes[str(folder / name)] = hashlib.sha256((folder / name).read_bytes()).hexdigest()
                assert len(set(streams.values())) <= 1, 'Unpaired deployed-retention streams'
                if 'adaptive' in groups:
                    for method in sorted(set(groups) - {'adaptive'}):
                        for rule in RULES:
                            for metric in METRICS:
                                comparisons.append({'regime': regime, 'seed': seed, 'order': order,
                                    'comparison': 'adaptive_minus_' + method, 'rule': rule, 'metric': metric,
                                    'difference': groups['adaptive'][rule][metric] - groups[method][rule][metric]})
    summary_rows, seed_rows = [], []
    if comparisons:
        frame = pd.DataFrame(comparisons)
        for key, group in frame.groupby(['regime', 'comparison', 'rule', 'metric']):
            complete = group.groupby('seed').filter(lambda g: len(g) == 2 and set(g.order) == {'canonical', 'b_first'})
            values = complete.groupby('seed').difference.mean()
            if len(values):
                summary_rows.append(dict(zip(['regime', 'comparison', 'rule', 'metric'], key)) | interval(values))
                seed_rows.extend(dict(zip(['regime', 'comparison', 'rule', 'metric'], key)) |
                                 {'seed': seed, 'difference': value} for seed, value in values.items())
        frame.to_csv('results/day18_retention_trajectory_comparisons.csv', index=False)
    summary = pd.DataFrame(summary_rows)
    pd.DataFrame(rows).to_csv('results/day18_retention_trajectory_metrics.csv', index=False)
    pd.DataFrame(concept_rows).to_csv('results/day18_retention_concept_metrics.csv', index=False)
    pd.DataFrame(coverage).to_csv('results/day18_retention_coverage.csv', index=False)
    pd.DataFrame(seed_rows).to_csv('results/day18_retention_seed_values.csv', index=False)
    summary.to_csv('results/day18_retention_paired_differences.csv', index=False)
    report = ['# Secondary deployed-retention development analysis', '',
        'Added after primary development outcomes. Uses saved full-output-space predictions, '
        'all three original deployment rules, both orders, both available regimes and both '
        'pilot-selected static ranks. No new training, rate selection, or official-test access. '
        'The learned routers have only final fixed-memory reload measurements; temporal '
        'retention is unavailable for those rules and is not imputed.', '',
        'Definitions: final concept-macro accuracy; the mean of five seen-concept checkpoint '
        'accuracies; the maximum accuracy at checkpoints after a concept first finishes '
        'training minus its final accuracy, averaged over concepts; and final minus '
        'first-exposure accuracy, averaged over concepts. The last statistic includes '
        'recurrence learning and is not standard nonrecurring-task backward transfer. '
        'Positive maximum-checkpoint drop means more loss from the observed peak; positive '
        'final-minus-first means improvement. The peak is a defined evaluation summary, '
        'not a selected predictor. Checkpoints do not constitute independent samples.', '',
        '## All paired comparisons', '', markdown_table(summary), '',
        'All intervals are descriptive over training seeds with orders averaged first. '
        'Fixed development examples were repeatedly examined. These secondary summaries '
        'neither establish a formal protected-memory guarantee nor change the primary '
        'final-accuracy selection objective.', '']
    Path('notes/day18_deployment_retention_results.md').write_text('\n'.join(report) + '\n')
    Path('notes/day18_retention_source_receipt.json').write_text(json.dumps({
        'source_files_sha256': hashes, 'analysis_added_after_primary_outcomes': True,
        'training_outputs_modified': False, 'official_test_accessed': False,
        'complete_trajectories': len(rows)//3}, indent=2) + '\n')
    print('SECONDARY_DEPLOYED_RETENTION_SAVED', len(rows)//3, 'trajectories', len(summary), 'comparisons', flush=True)


if __name__ == '__main__':
    main()
