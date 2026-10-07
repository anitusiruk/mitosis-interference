"""Retain every within-backbone linear-classifier control and original comparison."""
import json
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval


def main():
    rows, pairs, deployments, incomplete = [], [], [], []
    for seed in range(2027, 2032):
        for order in ['canonical', 'b_first']:
            routes = {}
            for architecture in ['private', 'head_only']:
                folder = Path(f'results/day19_banking_{architecture}_seed{seed}_{order}_frozen_preclassifier')
                if not folder.exists():
                    continue
                if not (folder/'summary.json').exists() or json.loads((folder/'summary.json').read_text())['status'] != 'completed':
                    incomplete.append(folder.name)
                    continue
                p = json.loads((folder/'provenance.json').read_text())
                s = json.loads((folder/'summary.json').read_text())
                assert p['preclassifier_mode'] == 'frozen'
                route = pd.read_csv(folder/'routing.csv')
                assert len(route) == 80
                reference = Path(f'results/day8_banking_{architecture}_cau_seed{seed}_{order}_fixed512')
                rp = json.loads((reference/'provenance.json').read_text())
                assert p['stream_sha256'] == rp['stream_sha256']
                old = pd.read_csv(reference/'routing.csv')
                changed = (route.decision != old.decision) | (route.adapter.fillna('DEFER') != old.adapter.fillna('DEFER'))
                rows.append({'seed':seed, 'order':order, 'architecture':architecture,
                    'allocation_disagreements_vs_trainable_stack':int(changed.sum()),
                    'spawn_steps':json.dumps(route.loc[route.decision=='spawn','step'].tolist()),
                    'learning_updates':s['learning_updates'], 'adapters':len(s['final_adapters']),
                    'stored_lora_parameters':s['resources']['lora_parameters'],
                    'stored_output_classifier_parameters':s['resources']['stored_output_classifier_parameters'],
                    'stored_frozen_preclassifier_parameters':s['resources']['frozen_private_preclassifier_parameters'],
                    'optimizer_bytes':s['resources']['optimizer_state_bytes'],
                    'maximum_training_texts':int(route.replay_items.max())})
                routes[architecture] = route
                final = pd.read_csv(folder/'label_free_eval.csv')
                final = final[final.step == 80]
                assert len(final) == 9
                for rule, group in final.groupby('rule'):
                    deployments.append({'seed':seed,'order':order,'architecture':architecture,
                                        'rule':rule,'final_macro_accuracy':group.accuracy.mean()})
            if set(routes) == {'private', 'head_only'}:
                a, b = routes['private'], routes['head_only']
                changed = (a.decision != b.decision) | (a.adapter.fillna('DEFER') != b.adapter.fillna('DEFER'))
                pairs.append({'seed':seed,'order':order,'allocation_disagreements':int(changed.sum()),
                    'private_spawn_steps':json.dumps(a.loc[a.decision=='spawn','step'].tolist()),
                    'head_only_spawn_steps':json.dumps(b.loc[b.decision=='spawn','step'].tolist()),
                    'private_learning_updates':int(a.train_executed.sum()),
                    'head_only_learning_updates':int(b.train_executed.sum())})
    report = ['# Frozen hidden pre-classifier allocation diagnostic', '',
        f'Completed trajectories {len(rows)}/20; paired controls {len(pairs)}/10. Incomplete attempts: {incomplete}.', '',
        'Both controls use the same DistilBERT backbone and fixed hidden pre-classifier. '
        'The private condition trains LoRA and the linear output classifier; the other '
        'trains only the output classifier, keeping LoRA output zero. This removes '
        'hidden pre-classifier learning, with its associated optimizer state, in both '
        'conditions. It is an allocation diagnostic, not a tuned competitive benchmark. '
        'The retained PEFT pre-classifier copies are dormant stored parameters.', '']
    pd.DataFrame(rows).to_csv('results/day19_linear_classifier_trajectories.csv', index=False)
    pd.DataFrame(pairs, columns=['seed','order','allocation_disagreements','private_spawn_steps',
        'head_only_spawn_steps','private_learning_updates','head_only_learning_updates']).to_csv(
            'results/day19_linear_classifier_allocation_pairs.csv', index=False)
    pd.DataFrame(deployments).to_csv('results/day19_linear_classifier_deployment.csv', index=False)
    summaries = []
    if deployments:
        frame = pd.DataFrame(deployments)
        paired = frame.pivot(index=['seed','order','rule'],columns='architecture',values='final_macro_accuracy').dropna()
        if not paired.empty and {'private','head_only'} <= set(paired.columns):
            paired['private_minus_head_only'] = paired.private-paired.head_only
            for rule, group in paired.reset_index().groupby('rule'):
                complete = group.groupby('seed').filter(lambda g:len(g)==2 and set(g.order)=={'canonical','b_first'})
                values = complete.groupby('seed').private_minus_head_only.mean()
                if len(values):summaries.append({'rule':rule,**interval(values)})
    summary = pd.DataFrame(summaries, columns=['rule','seed_clusters','mean','ci_low','ci_high'])
    summary.to_csv('results/day19_linear_classifier_prediction_differences.csv', index=False)
    report += ['## Every allocation pair','',markdown_table(pd.DataFrame(pairs)),'',
        '## All deviations from the trainable-stack reference and stored resources','',markdown_table(pd.DataFrame(rows)),'',
        '## All private-minus-output-classifier-only accuracy differences','',markdown_table(summary),'',
        '## Every deployment outcome','',markdown_table(pd.DataFrame(deployments)),'',
        'Intervals are descriptive over paired training seeds and fixed repeatedly examined '
        'development examples. Neither agreement nor disagreement establishes a universal '
        'capacity principle. Existing controls with trainable hidden classifiers must not '
        'be described as having no learned hidden representation capacity.']
    Path('notes/day19_linear_classifier_results.md').write_text('\n'.join(report)+'\n')
    print('LINEAR_CLASSIFIER_REPORT_SAVED', len(rows), 'trajectories', len(pairs), 'pairs', flush=True)


if __name__ == '__main__':
    main()
