"""Consistency checks on complete saved trajectories; no model changes."""
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

rows=[];paired={};allocations=[];manifest={};partial=[]
for pattern in ['day5_*_seed2026','day6_*_seed*','day7_multinli_*_seed*','day8_*_fixed512',
                'day10_*_initial_loss','day12_banking_private_single_rank96_seed*']:
    for folder in sorted(Path('results').glob(pattern)):
        if not (folder/'summary.json').exists():partial.append(folder.name);continue
        summary=json.loads((folder/'summary.json').read_text())
        if summary['status']!='completed':partial.append(folder.name);continue
        p=json.loads((folder/'provenance.json').read_text());a=p['args']
        assert p['official_test_used'] is False and summary['official_test_used'] is False
        r=pd.read_csv(folder/'routing.csv');e=pd.read_csv(folder/'label_free_eval.csv')
        assert len(r)==summary['steps']==p['stream_steps'],folder
        assert list(r.step)==list(range(1,len(r)+1)),folder
        assert int(r.train_executed.sum())==summary['learning_updates'],folder
        assert dict(Counter(r.decision))==summary['decisions'],folder
        assert np.isfinite(r.loc[r.train_executed,'loss']).all(),folder
        assert np.isfinite(e[['loss','accuracy']].to_numpy()).all(),folder
        assert e.accuracy.between(0,1).all() and (e.n>0).all(),folder
        final=e[e.step==e.step.max()]
        assert final.step.max()==len(r) and len(final)==9,folder
        assert set(final.rule)=={'last_active','uniform_probability','frozen_centroid'},folder
        assert set(final.concept)=={'A','B','C'},folder
        assert not final.duplicated(['concept','rule']).any(),folder
        assert len(summary['final_adapters'])==r.num_adapters.iloc[-1],folder
        key=(a['regime'],a['seed'],a.get('order','canonical'),a.get('boundary_condition','sharp'))
        paired.setdefault(key,set()).add(p['stream_sha256'])
        assert len(paired[key])==1,('Unpaired streams',key)
        for file in folder.rglob('*'):
            if file.is_file() and 'checkpoint' not in file.parts:
                manifest[str(file)]=hashlib.sha256(file.read_bytes()).hexdigest()
        rows.append({'run':folder.name,'regime':a['regime'],'seed':a['seed'],
                     'steps':len(r),'updates':summary['learning_updates'],'adapters':len(summary['final_adapters']),
                     'checks':'PASS'})

for regime in ['banking','amazon']:
    for seed in range(2027,2032):
        for order in ['canonical','b_first']:
            paths=[Path(f'results/day6_{regime}_{arch}_cau_seed{seed}_{order}/routing.csv')
                   for arch in ['private','head_only']]
            if not all(p.exists() for p in paths):continue
            a,b=map(pd.read_csv,paths)
            assert list(a.step)==list(b.step)
            spawns=lambda x:json.dumps(x.loc[x.decision=='spawn','step'].tolist())
            allocations.append({'regime':regime,'seed':seed,'order':order,
                 'private_spawn_steps':spawns(a),'head_only_spawn_steps':spawns(b),
                 'allocation_disagreements':int(((a.decision!=b.decision)|(a.adapter!=b.adapter)).sum())})

Path('results/day13_evidence_checks.csv').write_text(pd.DataFrame(rows).to_csv(index=False))
Path('results/day13_head_allocation_comparison.csv').write_text(pd.DataFrame(allocations).to_csv(index=False))
Path('results/day13_artifact_sha256.json').write_text(json.dumps(manifest,indent=2,sort_keys=True))
audit={'generated_utc':datetime.now(timezone.utc).isoformat(),'completed_trajectories_checked':len(rows),
       'partial_folders':partial,'stream_pair_groups':len(paired),'checks':'PASS',
       'official_test_flag_check':'provenance assertion, not an independent access audit',
       'checkpoint_reload_limit':'Auxiliary router checks nine aggregate sample counts and accuracies; per-example predictions were not stored.',
       'statistical_unit':'Independent training seed; paired orders averaged within seed; fixed development examples.'}
Path('results/day13_evidence_audit.json').write_text(json.dumps(audit,indent=2))
print('EVIDENCE_AUDIT_PASS',len(rows),'complete trajectories',len(paired),'paired stream groups',flush=True)
