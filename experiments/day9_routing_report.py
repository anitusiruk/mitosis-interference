"""Auxiliary routing results, kept distinct from earlier primary diagnostics."""
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table
from experiments.day6_diagnostic_report import interval

path=Path('results/day9_learned_routing_comparison.csv')
report=['# Auxiliary learned routing diagnostic','',
    'Introduced after the Day-5 routing failure and frozen before these outcomes. '
    'A standardized linear gate learns past adapter assignments from reservoir texts only. '
    'Neither gold class labels nor true genre/concept identities are router fitting targets. '
    'Both hard selection and probability mixture are reported; no development winner is selected. '
    'Every included checkpoint first passed original prediction agreement. Official tests remain unused.','']
if path.exists():
    df=pd.read_csv(path)
    report+=[f'Completed learner checkpoints: {df.run.nunique()}.','']
    day5=df[df.run.str.startswith('day5_')]
    if len(day5):report+=['## Day-5 development checkpoints','',markdown_table(day5[['run','rule','macro_accuracy']]),'']
    day6=df[df.run.str.startswith('day6_')]
    differences=[]
    for (regime,rule),group in day6.groupby(['regime','rule']):
        pivot=group.pivot(index=['seed','order'],columns=['architecture','policy'],values='macro_accuracy')
        for name,a,b in [('LoRA minus head-only / CAU',('private','cau'),('head_only','cau')),
                         ('CAU minus single / private',('private','cau'),('private','single')),
                         ('CAU minus single / head-only',('head_only','cau'),('head_only','single'))]:
            if a not in pivot or b not in pivot:continue
            delta=(pivot[a]-pivot[b]).dropna().rename('difference').reset_index()
            complete=delta.groupby('seed').filter(lambda g:set(g.order)=={'canonical','b_first'})
            differences.append({'regime':regime,'rule':rule,'contrast':name,
                **interval(complete.groupby('seed').difference.mean())})
    if differences:
        d=pd.DataFrame(differences);d.to_csv('results/day9_routing_paired_differences.csv',index=False)
        report+=['## Auxiliary seed-cluster differences','',markdown_table(d),'',
            'Descriptive intervals average both paired orders within each seed, with maximum five independent '
            'seed clusters. This added routing rule was not a primary outcome of the earlier frozen seed batch.','']
    selected=['run','rule','macro_accuracy','router_training_examples','fit_and_training_feature_seconds',
              'classifier_and_route_inference_seconds','learned_router_coefficients','normalization_statistics']
    report+=['## Full results and added resources','',markdown_table(df[selected]),'']
report+=['## Limitations','',
    'This standard learned gate does not establish novel task-free routing, reproduce L2R or HESTIA, '
    'or eliminate growth in total training memory. Router labels inherit the learner\'s own allocation errors. '
    'Development improvements require later untouched confirmation of the complete learner-plus-router.']
Path('notes/day9_learned_routing_results.md').write_text('\n'.join(report)+'\n')
print('DAY9_ROUTING_REPORT_SAVED',flush=True)
