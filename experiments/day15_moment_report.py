"""All conditional and marginal contrasts, clustered by training seed."""
import ast
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t

from src.moment_component_audit import FACTORS
from experiments.day5_report import markdown_table


def interval(values):
    a = np.asarray(values, dtype=float)
    mean = float(a.mean())
    width = float(t.ppf(.975, len(a)-1) * a.std(ddof=1) / len(a)**.5) if len(a)>1 else float('nan')
    return {'n_seeds': len(a), 'mean': mean, 'ci_low': mean-width, 'ci_high': mean+width}


def main():
    observations, coverage, incomplete = [], [], []
    for folder in sorted(Path('results').glob('day15_*_weight_moments')):
        verification = folder / 'observer_verification.json'
        if not verification.exists():
            incomplete.append(folder.name)
            continue
        if json.loads(verification.read_text())['status'] != 'passed':
            raise RuntimeError('Invalid observer receipt ' + str(folder))
        provenance = json.loads((folder / 'provenance.json').read_text())
        args = provenance['args']
        if not args['component_audit'] or args['architecture'] != 'private' or args['policy'] != 'cau':
            raise RuntimeError('Incorrect audit information condition')
        data = pd.read_csv(folder / 'component_trials.csv')
        for factor in FACTORS:
            if data[factor].dtype != bool:
                raise RuntimeError('Factor coding must be Boolean')
        route = pd.read_csv(folder / 'routing.csv')
        if data.empty or len(route) != 80:
            raise RuntimeError('Empty or incomplete audit')
        # Per-example data provide coverage receipts, not independent replicates.
        for step, batch in data.groupby('step'):
            if len(batch) != 32 or len(set(batch.source_adapter)) != 1:
                raise RuntimeError('Missing factorial cell or inconsistent source')
            for key, cell in batch.groupby(list(FACTORS)):
                if set(cell.fold) != {'A', 'B'} or len(cell) != 2:
                    raise RuntimeError('Missing complementary folds')
                indices = [i for value in cell.query_indices for i in ast.literal_eval(value)]
                n = int(cell.query_n.sum())
                if sorted(indices) != list(range(n)):
                    raise RuntimeError('Crossfit does not query each batch example once')
                for row in cell.itertuples():
                    before, after = [ast.literal_eval(getattr(row, field))
                                     for field in ['query_before_each', 'query_after_each']]
                    if len(before) != row.query_n or len(after) != row.query_n:
                        raise RuntimeError('Per-example receipt has incorrect count')
                    if not np.isfinite(before + after).all():
                        raise RuntimeError('Nonfinite per-example loss')
        weighted = []
        for key, part in data.groupby(['step', *FACTORS]):
            row = dict(zip(['step', *FACTORS], key))
            row.update({metric: np.average(part[metric], weights=part.query_n)
                        for metric in ['query_before', 'query_after', 'local_trainability',
                                       'group_mass_loss_before','group_mass_loss_after',
                                       'within_group_loss_before','within_group_loss_after']})
            weighted.append(row)
        weighted = pd.DataFrame(weighted)
        for step, part in weighted.groupby('step'):
            cells = {tuple(row[f] for f in FACTORS): row for _, row in part.iterrows()}
            if len(cells) != 16:
                raise RuntimeError('Missing factorial cell')
            metadata = {'run': folder.name, 'regime': args['regime'], 'seed': args['seed'],
                        'order': args['order'], 'step': step}
            for j, factor in enumerate(FACTORS):
                other = [i for i in range(4) if i != j]
                for condition in itertools.product((False, True), repeat=3):
                    a = [False]*4
                    for i, value in zip(other, condition):
                        a[i] = value
                    b = a.copy()
                    b[j] = True
                    a, b = cells[tuple(a)], cells[tuple(b)]
                    initial = a.query_before - b.query_before
                    local = b.local_trainability - a.local_trainability
                    effect = a.query_after - b.query_after
                    if abs(effect-initial-local) > 1e-6:
                        raise RuntimeError('Effect decomposition failed')
                    extra = {'initial_group_mass_decrease': a.group_mass_loss_before-b.group_mass_loss_before,
                             'initial_within_group_decrease': a.within_group_loss_before-b.within_group_loss_before,
                             'post_group_mass_decrease': a.group_mass_loss_after-b.group_mass_loss_after,
                             'post_within_group_decrease': a.within_group_loss_after-b.within_group_loss_after}
                    if (abs(initial-extra['initial_group_mass_decrease']-extra['initial_within_group_decrease']) > 1e-5
                        or abs(effect-extra['post_group_mass_decrease']-extra['post_within_group_decrease']) > 1e-5):
                        raise RuntimeError('Label-mass decomposition failed')
                    observations.append({**metadata, 'kind': 'conditional', 'factor': factor,
                        'condition': json.dumps({FACTORS[i]: v for i, v in zip(other, condition)}, sort_keys=True),
                        'post_update_loss_decrease': effect, 'initial_loss_decrease': initial,
                        'local_improvement_increase': local, **extra})
            for j, k in itertools.combinations(range(4), 2):
                other = [i for i in range(4) if i not in [j, k]]
                values = []
                for condition in itertools.product((False, True), repeat=2):
                    base = [False]*4
                    for i, value in zip(other, condition):
                        base[i] = value
                    terms = {}
                    for x, y in itertools.product((False, True), repeat=2):
                        key = base.copy(); key[j], key[k] = x, y
                        terms[x,y] = cells[tuple(key)]
                    values.append({name: terms[True,False][metric]+terms[False,True][metric]
                                  -terms[True,True][metric]-terms[False,False][metric]
                        for name, metric in [('post_update_loss_decrease','query_after'),
                                             ('initial_loss_decrease','query_before'),
                                             ('initial_group_mass_decrease','group_mass_loss_before'),
                                             ('initial_within_group_decrease','within_group_loss_before'),
                                             ('post_group_mass_decrease','group_mass_loss_after'),
                                             ('post_within_group_decrease','within_group_loss_after')]})
                    values[-1]['local_improvement_increase'] = (terms[True,True].local_trainability
                        +terms[False,False].local_trainability-terms[True,False].local_trainability
                        -terms[False,True].local_trainability)
                averaged = {name: np.mean([v[name] for v in values]) for name in values[0]}
                if abs(averaged['post_update_loss_decrease']-averaged['initial_loss_decrease']
                       -averaged['local_improvement_increase']) > 1e-6:
                    raise RuntimeError('Interaction decomposition failed')
                observations.append({**metadata, 'kind':'interaction', 'factor': FACTORS[j]+' x '+FACTORS[k],
                                     'condition':'marginal_over_other_factors', **averaged})
        coverage.append({'run': folder.name, 'regime': args['regime'], 'seed': args['seed'],
                         'order': args['order'], 'mature_batches': data.step.nunique(), 'raw_cell_fold_rows': len(data)})
    report = ['# Separate weight and AdamW-state audit', '',
        'Development-stage matched interventions. Positive contrasts mean lower post-update query loss, '
        'lower initial query loss, or more local improvement when resetting the named factor. '
        'All conditional cells and interactions are retained. Intervals are descriptive and are not '
        'multiplicity-adjusted hypothesis tests.', '', f'Verified trajectories: {len(coverage)}/20. '
        f'Incomplete or unverified attempts: {incomplete}.', '']
    if observations:
        frame = pd.DataFrame(observations)
        metrics = ['post_update_loss_decrease','initial_loss_decrease','local_improvement_increase',
                   'initial_group_mass_decrease','initial_within_group_decrease',
                   'post_group_mass_decrease','post_within_group_decrease']
        group = ['run','regime','seed','order','kind','factor','condition']
        trajectory = frame.groupby(group, as_index=False)[metrics].mean()
        marginal = trajectory[trajectory.kind=='conditional'].groupby(
            ['run','regime','seed','order','factor'], as_index=False)[metrics].mean()
        marginal['kind'], marginal['condition'] = 'marginal', 'average_over_all_other_factors'
        trajectory = pd.concat([trajectory,marginal], ignore_index=True)
        frame.to_csv('results/day15_batch_contrasts.csv',index=False)
        trajectory.to_csv('results/day15_trajectory_contrasts.csv',index=False)
        pd.DataFrame(coverage).to_csv('results/day15_coverage.csv',index=False)
        summaries, seed_rows = [], []
        for key, part in trajectory.groupby(['regime','kind','factor','condition']):
            paired = part.groupby('seed').filter(lambda p: len(p)==2 and set(p.order)=={'canonical','b_first'})
            for seed, values in paired.groupby('seed'):
                seed_rows.append(dict(zip(['regime','kind','factor','condition'],key))|
                                 {'seed':seed}|{m: values[m].mean() for m in metrics})
            for metric in metrics:
                values = paired.groupby('seed')[metric].mean()
                if len(values):
                    summaries.append(dict(zip(['regime','kind','factor','condition'],key))|
                                     {'metric':metric}|interval(values))
        summary = pd.DataFrame(summaries, columns=['regime','kind','factor','condition','metric',
                                                  'n_seeds','mean','ci_low','ci_high'])
        pd.DataFrame(seed_rows).to_csv('results/day15_seed_contrasts.csv',index=False)
        summary.to_csv('results/day15_seed_intervals.csv',index=False)
        report += ['## All marginal effects', '', markdown_table(summary[summary.kind=='marginal']), '',
                   '## All conditional post-update effects', '', markdown_table(summary[
                       (summary.kind=='conditional')&(summary.metric=='post_update_loss_decrease')]), '',
                   '## All marginal two-factor interactions', '', markdown_table(summary[summary.kind=='interaction']), '']
    report += ['## Interpretation limits', '',
        'The probe source is the actual active package, not the best feasible reuse selected retrospectively. '
        'This is one-step causal attribution of that probe, not a closed-loop effectiveness study or proof '
        'of future plasticity. Resetting a classifier can be a legitimate prediction objective. '
        'Five training seeds and fixed development examples do not establish population-level generalization. '
        'Broader architectures, source-faithful comparators and stronger natural same-label regimes remain open.']
    Path('notes/day15_weight_moment_results.md').write_text('\n'.join(report)+'\n')
    print('DAY15_REPORT_SAVED', len(coverage), 'verified trajectories', flush=True)


if __name__=='__main__':
    main()
