"""Third-regime descriptive report; no inference from transition windows."""
import json
from pathlib import Path
import pandas as pd
from experiments.day5_report import markdown_table

rows=[];incomplete=[]
for folder in sorted(Path('results').glob('day7_multinli_*_seed*')):
    if not (folder/'summary.json').exists():incomplete.append(folder.name);continue
    result=json.loads((folder/'summary.json').read_text())
    if result['status']!='completed':incomplete.append(folder.name);continue
    provenance=json.loads((folder/'provenance.json').read_text());args=provenance['args']
    router=pd.read_csv(folder/'label_free_eval.csv');last=router[router.step==router.step.max()]
    routing=pd.read_csv(folder/'routing.csv')
    spawns=routing[routing.decision=='spawn'][['step','segment']].to_json(orient='records')
    for rule,group in last.groupby('rule'):
        rows.append({'regime':'multinli','seed':args['seed'],'condition':args['boundary_condition'],
            'architecture':args['architecture'],'policy':args['policy'],'rule':rule,
            'macro_accuracy':group.accuracy.mean(),'steps':result['steps'],'updates':result['learning_updates'],
            'adapters':len(result['final_adapters']),'spawns':spawns,
            'live_training_seconds':result['timing']['live_training_seconds'],
            'stream_sha256':provenance['stream_sha256']})
report=['# Train-only MultiNLI stress-test results','',
    'Fixed three-class genre recurrence, grouped premise holdout, with sharp and gradual boundaries. '
    'Official matched/mismatched validation and test data were not evaluated. '
    'The short-context, 1440-example protocol is a development stress test, not a competitive NLI benchmark.','',
    f'Completed trajectories {len(rows)//3}/24; incomplete folders: {incomplete}.','']
if rows:
    df=pd.DataFrame(rows)
    for key,group in df.groupby(['seed','condition']):
        if group.stream_sha256.nunique()!=1:raise RuntimeError(f'Methods saw different MultiNLI inputs: {key}')
    df.to_csv('results/day7_multinli_comparison.csv',index=False)
    report+=[markdown_table(df.drop(columns=['regime','stream_sha256'])),'',
        'Chance under these balanced development subsets is 1/3. Low accuracy must be interpreted with the '
        'fixed single baselines; expansion or retention by itself does not demonstrate useful learning. '
        'Seed 2026 is a development pilot; 2027/2028 are transfer checks. Two fresh seeds and one genre '
        'schedule do not establish statistical confirmation. No confidence intervals over dependent windows '
        'or sharp/blurry variants are reported.']
Path('notes/day7_multinli_results.md').write_text('\n'.join(report)+'\n')
print('DAY7_REPORT_SAVED',len(rows)//3,flush=True)
