"""Paired seed-cluster summaries; orders/windows are never replicates."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
from experiments.day5_report import markdown_table


def interval(values):
    x=np.asarray(values,dtype=float)
    n=len(x)
    mean=float(x.mean()) if n else float('nan')
    if n<2:return {'seed_clusters':n,'mean':mean,'ci_low':float('nan'),'ci_high':float('nan')}
    half=float(t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n))
    return {'seed_clusters':n,'mean':mean,'ci_low':mean-half,'ci_high':mean+half}


def main():
    rows=[]
    incomplete=[]
    for folder in sorted(Path('results').glob('day6_*_seed*')):
        summary_path=folder/'summary.json'
        if not summary_path.exists():incomplete.append(folder.name);continue
        summary=json.loads(summary_path.read_text())
        if summary['status']!='completed':incomplete.append(folder.name);continue
        provenance=json.loads((folder/'provenance.json').read_text())
        args=provenance['args']
        df=pd.read_csv(folder/'label_free_eval.csv')
        last=df[df.step==df.step.max()]
        if not last.seen_concept.all():raise RuntimeError('Completed trajectory missing a seen concept')
        for rule,group in last.groupby('rule'):
            rows.append({'run':folder.name,'regime':args['regime'],'seed':args['seed'],'order':args['order'],
                         'architecture':args['architecture'],'policy':args['policy'],'rule':rule,
                         'macro_accuracy':group.accuracy.mean(),'updates':summary['learning_updates'],
                         'adapters':len(summary['final_adapters']),
                         'live_training_seconds':summary['timing']['live_training_seconds'],
                         'evaluation_seconds':summary['timing']['evaluation_seconds'],
                         'optimizer_state_bytes':summary['resources']['optimizer_state_bytes'],
                         'replay_items':summary['resources']['replay_items'],
                         'stored_private_head_parameters':summary['resources']['private_head_parameters'],
                         'stored_lora_parameters':summary['resources']['lora_parameters'],
                         'stream_sha256':provenance['stream_sha256']})
    report=['# Frozen seed and order diagnostic results','',
            'This batch evaluates the unchanged private-package CAU-v1 and a zero-LoRA head-only control, '
            'each against its fixed-single learner. Official tests remain unused. These are diagnostics '
            'conditional on fixed development data, not a submission-readiness or resource-matched superiority claim.','',
            f'Completed trajectories: {len(rows)//3}/80. Partial or unfinished folders: {incomplete}.','']
    if not rows:
        Path('notes/day6_diagnostic_results.md').write_text('\n'.join(report)+'\n');return
    df=pd.DataFrame(rows)
    df.to_csv('results/day6_individual_results.csv',index=False)
    # Every method on a given seed/order/regime must see identical stream data.
    for key,group in df.groupby(['regime','seed','order']):
        if group.stream_sha256.nunique()!=1:raise RuntimeError(f'Unpaired stream data {key}')
    summaries=[]
    differences=[]
    for (regime,rule),group in df.groupby(['regime','rule']):
        report+=['## '+regime+' / '+rule,'']
        for (arch,policy),part in group.groupby(['architecture','policy']):
            complete=part.groupby('seed').filter(lambda g:set(g.order)=={'canonical','b_first'})
            means=complete.groupby('seed').macro_accuracy.mean()
            summaries.append({'regime':regime,'rule':rule,'architecture':arch,'policy':policy,**interval(means)})
        pivot=group.pivot(index=['seed','order'],columns=['architecture','policy'],values='macro_accuracy')
        comparisons=[('LoRA minus head-only / CAU',('private','cau'),('head_only','cau')),
                     ('LoRA minus head-only / single',('private','single'),('head_only','single')),
                     ('CAU minus single / private',('private','cau'),('private','single')),
                     ('CAU minus single / head-only',('head_only','cau'),('head_only','single'))]
        here=[]
        for name,a,b in comparisons:
            if a not in pivot or b not in pivot:continue
            delta=(pivot[a]-pivot[b]).dropna().rename('difference').reset_index()
            complete=delta.groupby('seed').filter(lambda g:set(g.order)=={'canonical','b_first'})
            seed_means=complete.groupby('seed').difference.mean()
            result={'regime':regime,'rule':rule,'contrast':name,**interval(seed_means)}
            here.append(result);differences.append(result)
        report+=['Paired accuracy differences; both orders are averaged inside each seed before the interval.','',
                 markdown_table(pd.DataFrame(here)) if here else 'No complete paired seed clusters yet.','']
    pd.DataFrame(summaries).to_csv('results/day6_seed_cluster_summary.csv',index=False)
    pd.DataFrame(differences).to_csv('results/day6_paired_differences.csv',index=False)
    report+=['## Full run table','',markdown_table(df.drop(columns=['run','stream_sha256','optimizer_state_bytes',
              'stored_private_head_parameters','stored_lora_parameters','evaluation_seconds'])),'',
              '## Interpretation limits','',
              'Intervals are descriptive 95% Student-t intervals over independent seed clusters (maximum five), '
              'averaging the two paired orders within a seed. They condition on fixed evaluation examples and '
              'do not capture dataset sampling uncertainty. No window-level tests, oracle selection, '
              'post-outcome routing-rule choice, or multiplicity-adjusted winner claim is made.', '',
              'Pool growth increases total reservoir and private-head storage. Head-only stores unused zero-LoRA '
              'scaffolding; parameter columns report it explicitly. The primary experimental manipulation is '
              'training LoRA together with each classifier package versus training only classifier packages. '
              'Modern method baselines, fixed-total-resource runs and an untouched final evaluation are pending.']
    Path('notes/day6_diagnostic_results.md').write_text('\n'.join(report)+'\n')
    print('DAY6_REPORT_SAVED',len(rows)//3,flush=True)


if __name__=='__main__':main()
