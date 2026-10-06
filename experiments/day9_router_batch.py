"""Train-assignment router diagnostic on verified frozen checkpoints."""
from datetime import datetime,timezone
import gc
import hashlib
import json
import os
from pathlib import Path
import time
from types import SimpleNamespace
import warnings

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from datasets import load_dataset
from peft import PeftModel
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from transformers import AutoTokenizer,AutoModelForSequenceClassification

from experiments.signal_scan import base_features,encode
from experiments.controller_recurrence_cau_v1 import make_dev_split
from experiments.domain_recurrence_data import build_domain_recurrence
from experiments.day5_causal_recurrence import evaluate_label_free
from experiments.day7_multinli_data import build_multinli,PairTokenizer


from experiments.day9_learned_routing import evaluation_sets, frozen_features, load_checkpoint, evaluate_learned

def main(scope):
    os.environ['OMP_NUM_THREADS']='8';os.environ['TOKENIZERS_PARALLELISM']='false';torch.set_num_threads(8)
    sets={};features={};all_rows=[]
    status_path=Path('logs/day9_routing_status.json')
    status=json.loads(status_path.read_text()) if status_path.exists() else []
    aggregate=Path('results/day9_learned_routing_comparison.csv')
    if aggregate.exists():all_rows=pd.read_csv(aggregate).to_dict('records')
    patterns=['day5_*_seed2026'] if scope=='pilot' else ['day6_*_seed*','day7_multinli_*_seed*']
    folders=sorted([p for pattern in patterns for p in Path('results').glob(pattern)])
    for folder in folders:
        if datetime.now(timezone.utc)>=datetime.fromisoformat('2026-10-06T03:25:00+00:00'):break
        summary_path=folder/'summary.json'
        if not summary_path.exists() or json.loads(summary_path.read_text())['status']!='completed':continue
        provenance=json.loads((folder/'provenance.json').read_text());args=provenance['args']
        if args['architecture'] not in ['private','head_only']:continue
        if (folder/'learned_routing.csv').exists():raise RuntimeError('Refusing to overwrite auxiliary routing outcomes')
        regime=args['regime']
        if regime not in sets:sets[regime]=evaluation_sets(regime)
        pool,last_name,provenance=load_checkpoint(folder)
        old=pd.read_csv(folder/'label_free_eval.csv');old=old[old.step==old.step.max()]
        repeated=pd.DataFrame(evaluate_label_free(pool,sets[regime],last_name))
        checked=old[['concept','rule','n','accuracy']].merge(repeated[['concept','rule','n','accuracy']],
            on=['concept','rule'],suffixes=('_stored','_reloaded'),validate='one_to_one')
        if len(checked)!=9 or not (checked.n_stored==checked.n_reloaded).all() or not np.allclose(
            checked.accuracy_stored,checked.accuracy_reloaded,atol=1e-12,rtol=0):
            checked.to_csv(folder/'checkpoint_reload_mismatch.csv',index=False)
            raise RuntimeError(f'Reloaded checkpoint fails original prediction agreement: {folder}')
        names=sorted(pool.states)
        started=time.monotonic();train_features=[];targets=[]
        for i,name in enumerate(names):
            texts=[x[0] for x in pool.states[name].memory.items]
            train_features.append(frozen_features(pool,texts));targets.extend([i]*len(texts))
        x=np.concatenate(train_features)
        gate=None
        if len(names)>1:
            gate=make_pipeline(StandardScaler(),LogisticRegression(C=1.,solver='lbfgs',max_iter=1000,tol=1e-6))
            with warnings.catch_warnings():
                warnings.simplefilter('error',ConvergenceWarning);gate.fit(x,np.asarray(targets))
            scale,lr=gate[0],gate[1]
            np.savez_compressed(folder/'learned_router.npz',mean=scale.mean_,scale=scale.scale_,
                coef=lr.coef_,intercept=lr.intercept_,classes=lr.classes_,adapter_names=np.asarray(names))
        fit_seconds=time.monotonic()-started
        if regime not in features:features[regime]={c:frozen_features(pool,e['texts']) for c,e in sets[regime].items()}
        started=time.monotonic()
        rows=evaluate_learned(pool,sets[regime],features[regime],gate,names)
        inference_seconds=time.monotonic()-started
        pd.DataFrame(rows).to_csv(folder/'learned_routing.csv',index=False)
        resource={'router_training_examples':len(targets),'fit_and_training_feature_seconds':fit_seconds,
                  'classifier_and_route_inference_seconds':inference_seconds,'adapters':names,
                  'learned_router_coefficients':int(gate[-1].coef_.size+gate[-1].intercept_.size) if gate else 0,
                  'normalization_statistics':int(2*x.shape[1]) if gate else 0,'original_prediction_agreement':True,
                  'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'frozen_algorithm_sha256':hashlib.sha256(Path('experiments/day9_learned_routing.py').read_bytes()).hexdigest(),
                  'execution_scope':scope,
                  'learner_state_sha256':hashlib.sha256((folder/'checkpoint/learner_state.pt').read_bytes()).hexdigest(),
                  'official_test_used':False}
        (folder/'learned_routing_provenance.json').write_text(json.dumps(resource,indent=2))
        for rule in ['linear_hard','linear_probability_mixture']:
            all_rows.append({'run':folder.name,'regime':regime,'seed':args['seed'],'architecture':args['architecture'],
                'policy':args['policy'],'order':args.get('order','canonical'),'condition':args.get('boundary_condition','sharp'),
                'rule':rule,'macro_accuracy':np.mean([r['accuracy'] for r in rows if r['rule']==rule]),**resource})
        pd.DataFrame(all_rows).to_csv('results/day9_learned_routing_comparison.csv',index=False)
        status.append({'run':folder.name,'status':'completed'})
        Path('logs/day9_routing_status.json').write_text(json.dumps(status,indent=2))
        print('LEARNED_ROUTING',len(status),folder.name,'checkpoint agreement PASS',flush=True)
        del pool;gc.collect();torch.cuda.empty_cache()
    print('LEARNED_ROUTING_SCOPE_FINISHED',scope,len(status),flush=True)
    expected=6 if scope=='pilot' else 110
    if len(status)!=expected:raise RuntimeError(f'Auxiliary router scope incomplete: {len(status)}/{expected}')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--scope',choices=['pilot','replication'],required=True)
    main(parser.parse_args().scope)
