"""Retain the complete baseline grid and all paired development rules."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval

RATES = [2e-5, 5e-5, 1e-4, 2e-4, 4e-4, 8e-4]


def select_pilot_rates(data):
    actual = set(zip(data['rank'], data.learning_rate, data.order))
    expected = {(rank, rate, order) for rank in [8, 96] for rate in RATES
                for order in ['canonical', 'b_first']}
    if (len(data) != 24 or actual != expected or set(data.seed) != {2026}
            or not (data.updates == 80).all() or not np.isfinite(data.final_macro_accuracy).all()
            or not data.final_macro_accuracy.between(0, 1).all()):
        raise RuntimeError('Pilot selection requires the complete exact 24-run grid')
    grid = [{'rank': int(rank), 'learning_rate': float(rate),
             'pilot_accuracy_mean': float(group.final_macro_accuracy.mean())}
            for (rank, rate), group in data.groupby(['rank', 'learning_rate'])]
    selected = {str(rank): sorted([r for r in grid if r['rank'] == rank],
                 key=lambda r: (-r['pilot_accuracy_mean'], r['learning_rate']))[0]['learning_rate']
                for rank in [8, 96]}
    return selected, grid


def final_accuracy(folder):
    p = json.loads((folder / 'provenance.json').read_text())
    s = json.loads((folder / 'summary.json').read_text())
    if s['status'] != 'completed' or s['steps'] != 80:
        raise RuntimeError('Incomplete baseline is not an observed outcome')
    f = pd.read_csv(folder / 'label_free_eval.csv')
    f = f[(f.step == 80) & (f.rule == 'last_active')]
    if len(f) != 3:
        raise RuntimeError('Missing full-space concept predictions')
    return p, s, float(f.accuracy.mean())


def pilot_table():
    rows = []
    for folder in sorted(Path('results').glob('day17_pilot_rank*_lr*_seed2026_*')):
        if not (folder / 'summary.json').exists():
            continue
        if json.loads((folder / 'summary.json').read_text())['status'] != 'completed':
            continue
        p, s, accuracy = final_accuracy(folder)
        rows.append({'run': folder.name, 'rank': p['lora_rank'], 'learning_rate': p['learning_rate'],
                     'seed': 2026, 'order': p['args']['order'], 'final_macro_accuracy': accuracy,
                     'updates': s['learning_updates']})
    return pd.DataFrame(rows)


def main():
    pilots = pilot_table()
    selection_path = Path('notes/day17_static_rate_selection.json')
    selection = json.loads(selection_path.read_text()) if selection_path.exists() else None
    report = ['# Tuned fixed-capacity development baselines', '',
              f'Completed pilot trajectories: {len(pilots)}/24.', '',
              'The full equal-budget learning-rate grid and its pilot-only selection rule were '
              'committed before tuning outcomes. Both ranks and all adaptive deployment rules '
              'are retained. Development examples and the adaptive reference outcomes were '
              'already examined; this is not untouched final evaluation.', '']
    if not pilots.empty:
        pilots.to_csv('results/day17_static_pilot_grid.csv', index=False)
        report += ['## Every pilot', '', markdown_table(pilots), '']
    comparisons, incomplete = [], []
    for folder in sorted(Path('results').glob('day17_confirm_rank*_lr*_seed*')):
        if not (folder / 'summary.json').exists() or json.loads((folder / 'summary.json').read_text())['status'] != 'completed':
            incomplete.append(folder.name)
            continue
        if selection is None:
            raise RuntimeError('Baseline confirmation has no frozen selection receipt')
        p, s, accuracy = final_accuracy(folder)
        rank, seed, order = p['lora_rank'], p['args']['seed'], p['args']['order']
        if p['learning_rate'] != selection['selected_rates'][str(rank)]:
            raise RuntimeError('Confirmation rate differs from the pilot-only selection')
        reference = Path(f'results/day8_banking_private_cau_seed{seed}_{order}_fixed512')
        rp = json.loads((reference / 'provenance.json').read_text())
        rs = json.loads((reference / 'summary.json').read_text())
        if p['stream_sha256'] != rp['stream_sha256'] or rs['status'] != 'completed':
            raise RuntimeError('Unpaired adaptive/static stream')
        f = pd.read_csv(reference / 'label_free_eval.csv')
        f = f[f.step == 80]
        learned = pd.read_csv(reference / 'learned_routing.csv')
        for rule, group in pd.concat([f, learned], ignore_index=True).groupby('rule'):
            if len(group) != 3:
                raise RuntimeError('Adaptive rule has incomplete concept coverage')
            adaptive = float(group.accuracy.mean())
            r = s['resources']
            comparisons.append({'rank': rank, 'learning_rate': p['learning_rate'], 'seed': seed,
                'order': order, 'adaptive_rule': rule, 'static_accuracy': accuracy,
                'adaptive_accuracy': adaptive, 'adaptive_minus_static': adaptive-accuracy,
                'static_adaptation_parameters': r['lora_parameters']+r['private_head_parameters'],
                'adaptive_adaptation_parameters': rs['resources']['lora_parameters']+rs['resources']['private_head_parameters'],
                'static_optimizer_bytes': r['optimizer_state_bytes'],
                'adaptive_optimizer_bytes': rs['resources']['optimizer_state_bytes'],
                'static_training_texts': r['replay_items'],
                'adaptive_training_texts': rs['resources']['replay_items'],
                'static_training_seconds': s['timing']['live_training_seconds'],
                'static_evaluation_seconds': s['timing']['evaluation_seconds'],
                'static_gpu_peak_allocated_bytes': r['gpu_peak_allocated_bytes']})
    if selection:
        report += ['## Frozen pilot selection', '', markdown_table(pd.DataFrame(selection['grid_summary'])), '',
                   'Selected rates: ' + json.dumps(selection['selected_rates'], sort_keys=True) + '.', '']
    report += [f'Completed paired-development static trajectories: {len(comparisons)//5}/20; '
               f'incomplete attempts: {incomplete}.', '']
    if comparisons:
        frame = pd.DataFrame(comparisons)
        frame.to_csv('results/day17_tuned_static_comparisons.csv', index=False)
        seed_rows, differences = [], []
        for (rank, rule), group in frame.groupby(['rank', 'adaptive_rule']):
            complete = group.groupby('seed').filter(lambda g: len(g) == 2 and set(g.order) == {'canonical', 'b_first'})
            for seed, pair in complete.groupby('seed'):
                seed_rows.append({'rank': rank, 'adaptive_rule': rule, 'seed': seed,
                                  'adaptive_minus_static': pair.adaptive_minus_static.mean(),
                                  'static_accuracy': pair.static_accuracy.mean(),
                                  'adaptive_accuracy': pair.adaptive_accuracy.mean()})
            values = complete.groupby('seed').adaptive_minus_static.mean()
            if len(values):
                differences.append({'rank': rank, 'adaptive_rule': rule, **interval(values)})
        pd.DataFrame(seed_rows).to_csv('results/day17_tuned_static_seed_values.csv', index=False)
        summary = pd.DataFrame(differences)
        summary.to_csv('results/day17_tuned_static_paired_differences.csv', index=False)
        report += ['## Every rule and rank', '', markdown_table(summary), '',
                   '## Every trajectory and actual resource count', '', markdown_table(frame), '']
    report += ['Intervals are descriptive over paired training seeds and fixed development examples. '
        'Repeatedly evaluated orders, batches, and classes are not independent replicates. '
        'This is a learning-rate study, not exhaustive hyperparameter optimization. Static and adaptive '
        'models differ in classifier multiplicity and update/inference compute. Equal retained-text '
        'budgets are not universal resource matching. No modern named-method or final-test claim follows.']
    Path('notes/day17_static_tuning_results.md').write_text('\n'.join(report) + '\n')
    print('STATIC_TUNING_REPORT_SAVED', len(pilots), 'pilots', len(comparisons)//5, 'confirmations', flush=True)


if __name__ == '__main__':
    main()
