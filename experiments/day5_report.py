"""Descriptive Day-5 audit report; no window-level inferential claims."""
import argparse
from collections import Counter
import json
from pathlib import Path

import numpy as np
import pandas as pd


def markdown_table(df, index=False, digits=4):
    if index:df=df.reset_index()
    def cell(value):
        if isinstance(value,(float,np.floating)):
            return f'{value:.{digits}f}'
        return str(value).replace('|','\\|').replace('\n',' ')
    lines=['| '+' | '.join(map(str,df.columns))+' |',
           '| '+' | '.join(['---']*len(df.columns))+' |']
    lines += ['| '+' | '.join(cell(x) for x in row)+' |' for row in df.itertuples(index=False,name=None)]
    return '\n'.join(lines)


def components(folder):
    path=folder/'component_trials.csv'
    if not path.exists():return None,None
    df=pd.read_csv(path)
    df['weighted_after']=df.query_after*df.query_n
    df['weighted_before']=df.query_before*df.query_n
    grouped=df.groupby(['step','segment','source_adapter','variant'],sort=False).agg(
        after_sum=('weighted_after','sum'),before_sum=('weighted_before','sum'),n=('query_n','sum'))
    grouped['loss']=grouped.after_sum/grouped.n
    grouped['before']=grouped.before_sum/grouped.n
    values=grouped['loss'].unstack('variant')
    values=values.reset_index()
    ri=values['reuse_lora_inherit_head']
    rf=values['reuse_lora_fresh_head']
    fi=values['fresh_lora_inherit_head']
    ff=values['fresh_lora_fresh_head']
    values['new_lora_gain_inherited_head']=ri-fi
    values['fresh_head_gain_reused_lora']=ri-rf
    values['new_lora_gain_fresh_head']=rf-ff
    values['joint_package_gain']=ri-ff
    values['interaction_gain']=fi+rf-ri-ff
    values['new_lora_gain_common_frozen_head']=values['reuse_lora_common_frozen_head']-values['fresh_lora_common_frozen_head']
    values['retained_optimizer_gain']=values['reuse_lora_inherit_head_reset_optimizer']-ri
    metrics=['new_lora_gain_inherited_head','fresh_head_gain_reused_lora','new_lora_gain_fresh_head',
             'joint_package_gain','interaction_gain','new_lora_gain_common_frozen_head','retained_optimizer_gain']
    summary=values.groupby('segment',sort=False)[metrics].agg(['count','mean','median'])
    values.to_csv(folder/'component_contrasts.csv',index=False)
    summary.to_csv(folder/'component_segment_summary.csv')
    return values,summary


def guard_summary(routing):
    selected=[]
    probes=[]
    for row in routing.to_dict('records'):
        info=json.loads(row['info'])
        guards=info.get('full_batch_guards',{})
        for name,p in guards.items():
            probes.append({'step':row['step'],'adapter':name,'selected':name==row['adapter'],**p})
        if row['decision']=='reuse' and row['adapter'] in guards:
            p=guards[row['adapter']]
            selected.append({'step':row['step'],'segment':row['segment'],'adapter':row['adapter'],
                             'harm_mean':p['full_batch_harm'],'harm_lcb':p['full_batch_harm_lcb'],
                             'harm_ucb':p['full_batch_harm_ucb']})
    return pd.DataFrame(selected),pd.DataFrame(probes)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',default='results')
    parser.add_argument('--output',default='notes/day5_results_report.md')
    args=parser.parse_args()
    report=['# Day-5 development audit results','',
            'Seed 2026 only. Descriptive measurements, not independent replications. '
            'Oracle and restricted accuracies are diagnostic; label-free full-label-space '
            'metrics are reported separately. No official test data were used.','']
    aggregate=[]
    for folder in sorted(Path(args.root).glob('day5_*_seed2026*')):
        if not (folder/'routing.csv').exists():continue
        routing=pd.read_csv(folder/'routing.csv')
        complete=(folder/'summary.json').exists()
        report+=['## '+folder.name,'',f'Status: {"summary recorded" if complete else "partial run; no final summary"}.',
                 f'Completed steps: {len(routing)}. Learned batches: {int(routing.train_executed.sum())}. '
                 f'Decisions: {dict(Counter(routing.decision))}. Final pool: {int(routing.num_adapters.iloc[-1])}.','']
        spawns=routing[routing.decision=='spawn'][['step','segment','adapter']]
        report+=['Spawns: '+(spawns.to_json(orient='records') if len(spawns) else 'none')+'.','']
        selected,probes=guard_summary(routing)
        if len(selected):
            selected.to_csv(folder/'selected_guard_harm.csv',index=False)
            report+=[f'Selected guarded reuse updates: {len(selected)}; positive measured mean protected '
                     f'loss increase admitted: {int((selected.harm_mean>0).sum())}. '
                     f'Maximum measured mean harm: {selected.harm_mean.max():.6g}. '
                     'This is an empirical probe statistic, not a formal retention guarantee.','']
        if len(probes):probes.to_csv(folder/'all_guard_probes.csv',index=False)
        values,summary=components(folder)
        if values is not None:
            metrics=['new_lora_gain_inherited_head','fresh_head_gain_reused_lora',
                     'new_lora_gain_fresh_head','joint_package_gain','new_lora_gain_common_frozen_head','retained_optimizer_gain']
            means=values.groupby('segment',sort=False)[metrics].mean().reset_index()
            report+=['Factorial contrasts: positive values favor the named intervention. '
                     'These are means over dependent development windows; no confidence intervals are attached.','',
                     markdown_table(means,digits=6),'']
            spawn_steps=set(spawns.step)
            if spawn_steps:
                selected=values[values.step.isin(spawn_steps)][['step','segment','source_adapter',*metrics]]
                report+=['Matched active-source contrasts at the actual spawn windows (not a best-adapter attribution):','',
                         markdown_table(selected,digits=6),'',
                         'A fresh LoRA factor also resets its optimizer moments; a fresh head factor resets its head moments. '
                         'These contrasts attribute component interventions under that exact optimizer convention. '
                         'They do not isolate weight initialization from moment initialization.','']
            baseline=pd.read_csv(folder/'component_trials.csv')
            original=baseline[baseline.variant=='reuse_lora_inherit_head'].copy()
            original['x']=original.query_before*original.query_n
            before=original.groupby('step').agg(x=('x','sum'),n=('query_n','sum'))
            before=before.x/before.n
            original_util=values.step.map(before)-values['reuse_lora_inherit_head']
            reset_util=values.step.map(before)-values['reuse_lora_inherit_head_reset_optimizer']
            flips=int(((original_util>0)!=(reset_util>0)).sum())
            report+=[f'Active-source one-step utility sign changed by resetting all optimizer state: '
                     f'{flips}/{len(values)} windows. This is not a count of full-policy allocation reversals.','']
        router_file=folder/'label_free_eval.csv'
        if router_file.exists():
            labels=pd.read_csv(router_file)
            latest=labels[labels.step==labels.step.max()]
            report+=['Final recorded label-free full-space development accuracy:','',
                     markdown_table(latest.pivot(index='concept',columns='rule',values='accuracy'),index=True),'']
            macro=latest[latest.seen_concept].groupby('rule').accuracy.mean()
            report+=['Macro accuracy over already observed concepts: '+
                     ', '.join(f'{k}={v:.4f}' for k,v in macro.items())+'.','']
            aggregate.append({'run':folder.name,'steps':len(routing),'updates':int(routing.train_executed.sum()),
                              'adapters':int(routing.num_adapters.iloc[-1]),**macro.to_dict()})
        summary_file=folder/'summary.json'
        if summary_file.exists():
            result=json.loads(summary_file.read_text())
            report+=['Timings separate method execution from the extra attribution and evaluation probes:','',
                     '```json',json.dumps(result.get('timing',{}),indent=2),'```','']
        # Validate the claim that extra observational probes did not alter the
        # frozen Day-4 private CAU trajectory. Save disagreements rather than
        # silently declaring a new result equivalent to an old one.
        if folder.name in ['day5_banking_private_cau_seed2026','day5_amazon_private_cau_seed2026']:
            old_name='controller_recurrence_cau_v1_seed2026' if 'banking' in folder.name else 'controller_domain_recurrence_cau_v1_seed2026'
            old_path=Path(args.root)/old_name/'routing.csv'
            if old_path.exists():
                old=pd.read_csv(old_path)
                keys=['step','adapter','decision']
                joined=routing[keys].merge(old[keys],on='step',suffixes=('_new','_old'))
                disagreements=joined[(joined.adapter_new!=joined.adapter_old)|(joined.decision_new!=joined.decision_old)]
                disagreements.to_csv(folder/'day4_routing_disagreements.csv',index=False)
                report+=[f'Paired frozen Day-4 routing reproduction check: {len(disagreements)} '
                         f'disagreements over {len(joined)} comparable steps.','']
    if aggregate:
        report+=['## Development comparison','',markdown_table(pd.DataFrame(aggregate)),'']
        pd.DataFrame(aggregate).to_csv(Path(args.root)/'day5_run_comparison.csv',index=False)
    report+=['## Interpretation limits','',
        'The shared-head architecture adds all-adapter guards, including fresh and post-spawn warmup guards. '
        'It is a predeclared sensitivity extension. It differs from the private-package architecture in head '
        'sharing, moment sharing and protection scope; its between-run difference cannot isolate just one '
        'cause. The matched-state component contrasts provide more specific one-step attribution.', '',
        'Centroids use stored training texts with gold labels ignored. No rule is selected by development '
        'accuracy. Replay capacity in these runs is per adapter and grows with the pool; fixed-total-resource '
        'comparisons and unseen seed/order confirmation remain required.', '',
        'The runs do not establish TMLR readiness, a 95% retention guarantee, or LoRA-specific causal benefit '
        'without the corresponding positive matched-head evidence.']
    Path(args.output).write_text('\n'.join(report)+'\n')
    print('SAVED',args.output,flush=True)


if __name__=='__main__':main()
