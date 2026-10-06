"""Utility decomposition and matched-input scoring-ablation diagnostics."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from experiments.day5_report import markdown_table
from src.adapter_pool_initial_loss import initial_loss_scores

decomposition=[];comparisons=[]
for pattern in ['day5_*_private_cau_seed2026','day6_*_private_cau_seed*']:
    for folder in sorted(Path('results').glob(pattern)):
        if not (folder/'routing.csv').exists():continue
        routing=pd.read_csv(folder/'routing.csv')
        for row in routing.to_dict('records'):
            utility=json.loads(row['info']).get('utility',{})
            if utility.get('status')!='ok':continue
            before=initial_loss_scores(utility)
            best=utility['best_reuse']
            if best is None:continue
            reuse=utility['reuse_profiles'][best]
            gap=reuse['query_before']-utility['fresh_query_before']
            learned=utility['fresh_local_trainability']-reuse['local_trainability']
            if not np.isclose(gap+learned,utility['fresh_advantage'],atol=1e-6):raise RuntimeError('Utility decomposition mismatch')
            decomposition.append({'run':folder.name,'step':row['step'],'segment':row['segment'],
                'actual_decision':row['decision'],'best_post_update_reuse':best,'initial_loss_gap':gap,
                'learning_gain_difference':learned,'fresh_advantage':utility['fresh_advantage'],
                'initial_gap_share':gap/utility['fresh_advantage'] if abs(utility['fresh_advantage'])>1e-8 else np.nan,
                'post_update_fresh_positive':utility['fresh_positive'],'initial_loss_fresh_positive':before['fresh_positive'],
                'eligibility_changed':utility['fresh_positive']!=before['fresh_positive'],
                'best_reuse_changed':best!=before['best_reuse']})
for folder in sorted(Path('results').glob('day10_*_initial_loss')):
    if not (folder/'summary.json').exists():continue
    summary=json.loads((folder/'summary.json').read_text())
    if summary['status']!='completed':continue
    p=json.loads((folder/'provenance.json').read_text());a=p['args']
    reference=Path('results')/(f"day5_{a['regime']}_{a['architecture']}_cau_seed2026" if a['seed']==2026 else
        f"day6_{a['regime']}_{a['architecture']}_cau_seed{a['seed']}_canonical")
    rp=json.loads((reference/'provenance.json').read_text())
    if p['stream_sha256']!=rp['stream_sha256']:raise RuntimeError('Scoring ablation stream mismatch')
    new=pd.read_csv(folder/'routing.csv');old=pd.read_csv(reference/'routing.csv')
    aligned=new[['step','adapter','decision']].merge(old[['step','adapter','decision']],on='step',suffixes=('_initial','_post'))
    disagree=aligned[(aligned.adapter_initial!=aligned.adapter_post)|(aligned.decision_initial!=aligned.decision_post)]
    disagree.to_csv(folder/'allocation_disagreements.csv',index=False)
    new_metrics=pd.read_csv(folder/'label_free_eval.csv');new_metrics=new_metrics[new_metrics.step==new_metrics.step.max()]
    old_metrics=pd.read_csv(reference/'label_free_eval.csv');old_metrics=old_metrics[old_metrics.step==old_metrics.step.max()]
    for rule,group in new_metrics.groupby('rule'):
        comparisons.append({'regime':a['regime'],'architecture':a['architecture'],'seed':a['seed'],'rule':rule,
             'initial_loss_accuracy':group.accuracy.mean(),'post_update_accuracy':old_metrics[old_metrics.rule==rule].accuracy.mean(),
             'allocation_disagreements':len(disagree),'updates':summary['learning_updates'],
             'adapters':len(summary['final_adapters']),'spawns':new[new.decision=='spawn'][['step','segment']].to_json(orient='records')})
report=['# Action-utility mechanism audit','',
    'For a candidate a, U(a)=L(real,before)-L(a,before)+[L(a,before)-L(a,after)]. '
    'The common baseline cancels for fresh versus reuse; initial prediction changes and one-step learning '
    'are distinct contributions. All same-state windows are dependent development observations.','']
if decomposition:
    d=pd.DataFrame(decomposition);d.to_csv('results/day10_utility_decomposition.csv',index=False)
    original_spawns=d[(d.run=='day5_banking_private_cau_seed2026')&(d.actual_decision=='spawn')]
    report+=['## Original BANKING spawn windows','',markdown_table(original_spawns[['step','segment','initial_loss_gap',
        'learning_gain_difference','fresh_advantage','initial_gap_share']]),'',
        'The initial gap includes changing the complete classifier-and-LoRA package; it is not a pure classifier '
        'effect. The matched component factorial audit separately identifies substantial classifier-head effects.','',
        '## Same-state eligibility comparison','',
        markdown_table(d.groupby('run',sort=False).agg(windows=('step','count'),eligibility_changes=('eligibility_changed','sum'),
                         reuse_ranking_changes=('best_reuse_changed','sum')).reset_index()),'',
        'These disagreement counts rescore the same reference states. They are not a closed-loop ablation or '
        'independent-window significance test.','']
if comparisons:
    c=pd.DataFrame(comparisons);c.to_csv('results/day10_initial_loss_comparison.csv',index=False)
    report+=['## Closed-loop scoring pilot','',markdown_table(c),'',
        'Only ranking uses pre-update current-query loss. Exact AdamW protected-memory guards remain. '
        'No inference about the benefit of all lookahead computation or a runtime speedup follows. '
        'Three canonical-order development seeds require broader confirmation.']
Path('notes/day10_action_utility_mechanism.md').write_text('\n'.join(report)+'\n')
print('DAY10_MECHANISM_REPORT_SAVED',len(decomposition),len(comparisons)//3,flush=True)
