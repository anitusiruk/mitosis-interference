"""All BERT allocation pairs and deployment rules, without winner selection."""
import json
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval


def main():
    rows, pairs, partial = [], [], []
    for seed in range(2027,2032):
        for order in ['canonical','b_first']:
            routes={}
            for architecture in ['private','head_only']:
                folder=Path(f'results/day16_banking_{architecture}_seed{seed}_{order}_bert')
                if not folder.exists():continue
                if not (folder/'summary.json').exists() or json.loads((folder/'summary.json').read_text())['status']!='completed':
                    partial.append(folder.name);continue
                provenance=json.loads((folder/'provenance.json').read_text())
                summary=json.loads((folder/'summary.json').read_text())
                route=pd.read_csv(folder/'routing.csv');routes[architecture]=(route,provenance)
                metrics=pd.read_csv(folder/'label_free_eval.csv');metrics=metrics[metrics.step==80]
                if len(route)!=80 or len(metrics)!=9:raise RuntimeError('Incomplete BERT evidence')
                reference=Path(f'results/day8_banking_{architecture}_cau_seed{seed}_{order}_fixed512')
                rp=json.loads((reference/'provenance.json').read_text())
                if provenance['stream_sha256']!=rp['stream_sha256']:raise RuntimeError('Unpaired cross-backbone stream')
                old=pd.read_csv(reference/'label_free_eval.csv');old=old[old.step==80]
                for rule,part in metrics.groupby('rule'):
                    rows.append({'seed':seed,'order':order,'architecture':architecture,'rule':rule,
                        'bert_macro_accuracy':part.accuracy.mean(),
                        'distilbert_macro_accuracy':old[old.rule==rule].accuracy.mean(),
                        'bert_minus_distilbert':part.accuracy.mean()-old[old.rule==rule].accuracy.mean(),
                        'updates':summary['learning_updates'],'adapters':len(summary['final_adapters']),
                        'adaptation_parameters':summary['resources']['private_head_parameters']+summary['resources']['lora_parameters'],
                        'maximum_training_texts':int(route.replay_items.max())})
            if set(routes)=={'private','head_only'}:
                a,ap=routes['private'];b,bp=routes['head_only']
                if ap['stream_sha256']!=bp['stream_sha256']:raise RuntimeError('Unpaired BERT architecture controls')
                disagreements=((a.decision!=b.decision)|(a.adapter.fillna('DEFER')!=b.adapter.fillna('DEFER')))
                pairs.append({'seed':seed,'order':order,'allocation_disagreements':int(disagreements.sum()),
                    'private_spawn_steps':json.dumps(a.loc[a.decision=='spawn','step'].tolist()),
                    'head_only_spawn_steps':json.dumps(b.loc[b.decision=='spawn','step'].tolist()),
                    'private_learning_updates':int(a.train_executed.sum()),
                    'head_only_learning_updates':int(b.train_executed.sum())})
    report=['# BERT allocation transfer diagnostic','',f'Complete trajectories {len(rows)//3}/20; '
        f'complete private/head-only pairs {len(pairs)}/10. Partial attempts: {partial}.','',
        'This transfer check replaces the backbone, representations, tokenizer, pooler and classifier. '
        'It does not isolate classifier design alone or compare against a tuned static BERT baseline. '
        'All deployment rules and both allocation controls are retained.','']
    if rows:
        frame=pd.DataFrame(rows);frame.to_csv('results/day16_bert_deployment.csv',index=False)
        pd.DataFrame(pairs).to_csv('results/day16_bert_allocation_pairs.csv',index=False)
        differences=[]
        for key,part in frame.groupby(['architecture','rule']):
            complete=part.groupby('seed').filter(lambda p:len(p)==2 and set(p.order)=={'canonical','b_first'})
            differences.append(dict(zip(['architecture','rule'],key))|interval(
                complete.groupby('seed').bert_minus_distilbert.mean()))
        summary=pd.DataFrame(differences);summary.to_csv('results/day16_bert_paired_differences.csv',index=False)
        report+=['## Every allocation pair','',markdown_table(pd.DataFrame(pairs)),'',
            '## Descriptive cross-backbone accuracy differences','',markdown_table(summary),'',
            '## Every trajectory and prediction rule','',markdown_table(frame),'']
    report+=['Intervals average both orders within each independent seed. The fixed development examples '
        'have been repeatedly examined; this is development evidence. Scope is the BANKING label-group '
        'stress test, the frozen training recipe and the declared memory budget. Neither allocation '
        'equivalence nor disagreement alone establishes competitive utility or a general capacity principle.']
    Path('notes/day16_bert_allocation_results.md').write_text('\n'.join(report)+'\n')
    print('DAY16_BERT_REPORT_SAVED',len(rows)//3,len(pairs),'pairs',flush=True)


if __name__=='__main__':main()
