"""Paired fixed-memory routing comparisons with actual stored resources."""
import json
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval

path=Path('results/day14_fixed_memory_routing_comparison.csv');rows=[]
report=['# Learned routing with fixed total training memory','',
    'Auxiliary development sensitivity with at most 512 total retained training texts. Both fixed learned rules '
    'are reported; no accuracy-selected rule or novel-router claim follows. Reload verification compares nine '
    'aggregate sample counts, accuracies and losses, not previously saved per-example prediction vectors.','']
if path.exists():
    df=pd.read_csv(path);original=pd.read_csv('results/day9_learned_routing_comparison.csv')
    for a in df.to_dict('records'):
        folder=Path('results')/a['run'];p=json.loads((folder/'provenance.json').read_text())
        s=json.loads((folder/'summary.json').read_text())
        assert a['router_training_examples']<=512
        reference=(f"day5_{a['regime']}_{a['architecture']}_cau_seed2026" if a['seed']==2026 else
            f"day6_{a['regime']}_{a['architecture']}_cau_seed{a['seed']}_{a['order']}")
        rp=json.loads((Path('results')/reference/'provenance.json').read_text())
        assert rp['stream_sha256']==p['stream_sha256']
        old=original[(original.run==reference)&(original.rule==a['rule'])]
        assert len(old)==1
        fixed=(f"day5_{a['regime']}_{a['architecture']}_single_seed2026" if a['seed']==2026 else
            f"day6_{a['regime']}_{a['architecture']}_single_seed{a['seed']}_{a['order']}")
        # Day 5 has no head-only fixed-single run; pilot comparison stays absent.
        fixed_accuracy=float('nan')
        if (Path('results')/fixed/'label_free_eval.csv').exists():
            f=pd.read_csv(Path('results')/fixed/'label_free_eval.csv');f=f[f.step==f.step.max()]
            fixed_accuracy=f[f.rule=='last_active'].accuracy.mean()
        rank_accuracy=float('nan');rank_parameters=float('nan')
        if a['regime']=='banking' and a['architecture']=='private':
            rank=Path(f"results/day12_banking_private_single_rank96_seed{a['seed']}_{a['order']}")
            if (rank/'summary.json').exists() and json.loads((rank/'summary.json').read_text())['status']=='completed':
                r=pd.read_csv(rank/'label_free_eval.csv');r=r[r.step==r.step.max()]
                rank_accuracy=r[r.rule=='last_active'].accuracy.mean()
                resources=json.loads((rank/'summary.json').read_text())['resources']
                rank_parameters=resources['private_head_parameters']+resources['lora_parameters']
        resources=s['resources'];parameters=resources['private_head_parameters']+resources['lora_parameters']
        rows.append({k:a[k] for k in ['run','regime','architecture','seed','order','rule']}|
            {'fixed_memory_accuracy':a['macro_accuracy'],'per_adapter_memory_accuracy':old.macro_accuracy.iloc[0],
             'fixed_minus_per_adapter':a['macro_accuracy']-old.macro_accuracy.iloc[0],
             'fixed_single_accuracy':fixed_accuracy,'fixed_minus_single':a['macro_accuracy']-fixed_accuracy,
             'rank96_accuracy':rank_accuracy,'fixed_minus_rank96':a['macro_accuracy']-rank_accuracy,
             'adaptation_parameters':parameters,'rank96_parameters':rank_parameters,
             'router_training_examples':a['router_training_examples'],'router_coefficients':a['learned_router_coefficients'],
             'normalization_statistics':a['normalization_statistics'],'optimizer_state_bytes':resources['optimizer_state_bytes']})
    comparisons=pd.DataFrame(rows);comparisons.to_csv('results/day14_memory_routing_comparisons.csv',index=False)
    differences=[]
    for key,group in comparisons[comparisons.seed!=2026].groupby(['regime','architecture','rule']):
        for contrast in ['fixed_minus_per_adapter','fixed_minus_single','fixed_minus_rank96']:
            part=group.dropna(subset=[contrast]).groupby('seed').filter(lambda g:set(g.order)=={'canonical','b_first'})
            differences.append(dict(zip(['regime','architecture','rule'],key))|
                {'contrast':contrast,**interval(part.groupby('seed')[contrast].mean())})
    d=pd.DataFrame(differences);d.to_csv('results/day14_memory_routing_paired_differences.csv',index=False)
    report+=[f'Completed checkpoints {df.run.nunique()}/44.','',markdown_table(d),'',markdown_table(comparisons),'']
report+=['Stored model parameters, optimizer state and router coefficients are reported separately from the '
    '512-text budget. Rank 96 controls a declared three-package storage scale; different package counts '
    'and classifier multiplicity limit parameter-match claims. All intervals are descriptive over at most '
    'five seeds, with paired orders averaged first and fixed development examples. The extension was added '
    'after original routing outcomes and requires later frozen complete-method confirmation.']
Path('notes/day14_fixed_memory_routing_results.md').write_text('\n'.join(report)+'\n')
print('FIXED_MEMORY_ROUTING_REPORT_SAVED',len(rows)//2,flush=True)
