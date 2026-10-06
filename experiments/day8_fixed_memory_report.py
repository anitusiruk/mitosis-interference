"""Paired sensitivity to a fixed total training reservoir."""
import json
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval

rows=[];incomplete=[]
for folder in sorted(Path('results').glob('day8_*_fixed512')):
    if not (folder/'summary.json').exists():incomplete.append(folder.name);continue
    summary=json.loads((folder/'summary.json').read_text())
    if summary['status']!='completed':incomplete.append(folder.name);continue
    prov=json.loads((folder/'provenance.json').read_text());a=prov['args']
    route=pd.read_csv(folder/'routing.csv')
    if route.replay_items.max()>512 or route.allocated_memory_slots.max()>512:raise RuntimeError('Stored memory budget violated')
    reference=Path('results')/(f"day5_{a['regime']}_{a['architecture']}_cau_seed2026" if a['seed']==2026 else
        f"day6_{a['regime']}_{a['architecture']}_cau_seed{a['seed']}_{a['order']}")
    rp=json.loads((reference/'provenance.json').read_text())
    if prov['stream_sha256']!=rp['stream_sha256']:raise RuntimeError('Memory sensitivity streams are unpaired')
    new=pd.read_csv(folder/'label_free_eval.csv');new=new[new.step==new.step.max()]
    old=pd.read_csv(reference/'label_free_eval.csv');old=old[old.step==old.step.max()]
    for rule,part in new.groupby('rule'):
        old_accuracy=old[old.rule==rule].accuracy.mean()
        rows.append({'run':folder.name,'regime':a['regime'],'architecture':a['architecture'],'seed':a['seed'],
            'order':a['order'],'rule':rule,'fixed_macro_accuracy':part.accuracy.mean(),
            'per_adapter_macro_accuracy':old_accuracy,'fixed_minus_per_adapter':part.accuracy.mean()-old_accuracy,
            'updates':summary['learning_updates'],'adapters':len(summary['final_adapters']),
            'maximum_stored_memory':int(route.replay_items.max()),'final_stored_memory':int(route.replay_items.iloc[-1]),
            'final_allocated_slots':int(route.allocated_memory_slots.iloc[-1]),
            'live_training_seconds':summary['timing']['live_training_seconds']})
report=['# Fixed-total-memory sensitivity results','',
    'Each growing pool is restricted to 512 total reservoir items, with fixed 64-item probes and at most eight adapters. '
    'Reservoirs still protect and route; training uses incoming batches only. This controls training-text memory, '
    'not model parameter storage or inference compute. All comparisons use identical seed/order streams.','',
    f'Completed trajectories {len(rows)//3}/44. Incomplete folders: {incomplete}.','']
if rows:
    df=pd.DataFrame(rows);df.to_csv('results/day8_memory_comparison.csv',index=False)
    summary_rows=[]
    for key,part in df[df.seed!=2026].groupby(['regime','architecture','rule']):
        complete=part.groupby('seed').filter(lambda g:set(g.order)=={'canonical','b_first'})
        summary_rows.append(dict(zip(['regime','architecture','rule'],key))|
            interval(complete.groupby('seed').fixed_minus_per_adapter.mean()))
    s=pd.DataFrame(summary_rows);s.to_csv('results/day8_memory_paired_differences.csv',index=False)
    report+=['## Fixed minus per-adapter accuracy','',markdown_table(s),'',
        'Descriptive intervals average both paired orders within a seed and use at most five independent seed clusters. '
        'Seed 2026 remains a development pilot.','',
        '## Every run','',markdown_table(df.drop(columns=['run'])),'']
report+=['## Limits','',
    'Equal reservoir capacity does not make different adapter pools parameter- or compute-matched. The extension '
    'also includes a hard eight-adapter cap and stricter restoration of stale gradients/flags/modes; the no-shrink '
    'numeric-equivalence test checks that cleanup leaves action scores unchanged. This sensitivity does not '
    'constitute an untouched final evaluation or modern-baseline comparison.']
Path('notes/day8_fixed_memory_results.md').write_text('\n'.join(report)+'\n')
print('DAY8_REPORT_SAVED',len(rows)//3,flush=True)
