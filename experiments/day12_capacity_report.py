"""Actual capacity and paired development comparisons for rank-96 baseline."""
import json
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval

rows=[];incomplete=[]
for folder in sorted(Path('results').glob('day12_banking_private_single_rank96_seed*')):
    if not (folder/'summary.json').exists():incomplete.append(folder.name);continue
    summary=json.loads((folder/'summary.json').read_text())
    if summary['status']!='completed':incomplete.append(folder.name);continue
    p=json.loads((folder/'provenance.json').read_text());a=p['args']
    metrics=pd.read_csv(folder/'label_free_eval.csv');last=metrics[metrics.step==metrics.step.max()]
    adaptive=Path('results')/(f"day5_banking_private_cau_seed2026" if a['seed']==2026 else
        f"day6_banking_private_cau_seed{a['seed']}_{a['order']}")
    fixed=Path('results')/(f"day5_banking_private_single_seed2026" if a['seed']==2026 else
        f"day6_banking_private_single_seed{a['seed']}_{a['order']}")
    ap=json.loads((adaptive/'provenance.json').read_text());fp=json.loads((fixed/'provenance.json').read_text())
    if len({p['stream_sha256'],ap['stream_sha256'],fp['stream_sha256']})!=1:raise RuntimeError('Capacity baseline data mismatch')
    am=pd.read_csv(adaptive/'label_free_eval.csv');am=am[am.step==am.step.max()]
    fm=pd.read_csv(fixed/'label_free_eval.csv');fm=fm[fm.step==fm.step.max()]
    ar=json.loads((adaptive/'summary.json').read_text())['resources']
    adaptation=lambda r:r['private_head_parameters']+r['lora_parameters']
    for rule,group in last.groupby('rule'):
        rows.append({'seed':a['seed'],'order':a['order'],'rule':rule,'rank96_accuracy':group.accuracy.mean(),
            'rank8_single_accuracy':fm[fm.rule==rule].accuracy.mean(),'adaptive_accuracy':am[am.rule==rule].accuracy.mean(),
            'rank96_minus_rank8':group.accuracy.mean()-fm[fm.rule==rule].accuracy.mean(),
            'rank96_minus_adaptive':group.accuracy.mean()-am[am.rule==rule].accuracy.mean(),
            'rank96_adaptation_parameters':adaptation(summary['resources']),'adaptive_adaptation_parameters':adaptation(ar),
            'adaptive_larger_than_rank96':adaptation(ar)>adaptation(summary['resources']),
            'rank96_live_training_seconds':summary['timing']['live_training_seconds'],
            'rank96_optimizer_bytes':summary['resources']['optimizer_state_bytes']})
report=['# Larger fixed-capacity baseline','',
    'Rank 96 was selected by parameter arithmetic before outcomes, near the storage of three rank-8 packages. '
    'It is a standard fixed-capacity alternative, not a named modern-method reproduction or universally '
    'parameter-matched algorithm. All predictors use the full 77-class label space. Official tests remain unused.','',
    f'Completed trajectories {len(rows)//3}/11; incomplete folders: {incomplete}.','']
if rows:
    df=pd.DataFrame(rows);df.to_csv('results/day12_capacity_comparison.csv',index=False)
    differences=[]
    for rule,part in df[df.seed!=2026].groupby('rule'):
        complete=part.groupby('seed').filter(lambda g:set(g.order)=={'canonical','b_first'})
        for column in ['rank96_minus_rank8','rank96_minus_adaptive']:
            differences.append({'rule':rule,'contrast':column,**interval(complete.groupby('seed')[column].mean())})
    d=pd.DataFrame(differences);d.to_csv('results/day12_capacity_paired_differences.csv',index=False)
    report+=['## Seed-cluster paired differences','',markdown_table(d),'',
        'Both orders are averaged inside each fresh seed before descriptive Student-t intervals; seed 2026 '
        'is excluded. Fixed examples and this rank choice define the scope of these intervals.','',
        '## Actual resources and every run','',markdown_table(df),'']
report+=['Growing pools store multiple classifier heads; rank 96 spends that budget on LoRA while retaining one '
    'head. Stored parameters, active-update compute, inference compute, and optimizer state are different '
    'resources. Report these differences instead of equating all of them. Modern source-faithful baseline '
    'reproductions and untouched final evaluation remain required.']
Path('notes/day12_capacity_results.md').write_text('\n'.join(report)+'\n')
print('DAY12_CAPACITY_REPORT_SAVED',len(rows)//3,flush=True)
