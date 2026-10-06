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


def evaluation_sets(regime):
    if regime=='amazon':return build_domain_recurrence(2026)[2]
    if regime=='multinli':return build_multinli(2026)[2]
    ds=load_dataset('PolyAI/banking77',split='train',trust_remote_code=True)
    _,dev=make_dev_split(ds)
    labels=np.asarray(dev['label'])
    result={}
    for concept,low in [('A',0),('B',11),('C',22)]:
        ids=np.flatnonzero((labels>=low)&(labels<low+11))
        result[concept]={'texts':[dev[int(i)]['text'] for i in ids],
                         'labels':[int(dev[int(i)]['label']) for i in ids]}
    return result


@torch.no_grad()
def frozen_features(pool,texts):
    return torch.cat([base_features(pool.model,pool.tok,texts[i:i+64],pool.device).cpu()
                      for i in range(0,len(texts),64)]).numpy()


def load_checkpoint(folder):
    provenance=json.loads((folder/'provenance.json').read_text())
    args=provenance['args'];regime=args['regime']
    count={'banking':77,'amazon':2,'multinli':3}[regime]
    revision=provenance['model_revision']
    tok=AutoTokenizer.from_pretrained('distilbert-base-uncased',revision=revision)
    if regime=='multinli':tok=PairTokenizer(tok)
    base=AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased',revision=revision,num_labels=count)
    state=torch.load(folder/'checkpoint/learner_state.pt',map_location='cpu',weights_only=False)
    model=PeftModel.from_pretrained(base,folder/'checkpoint/adapters',adapter_name='default')
    names=sorted(state['states'])
    for name in names:
        if name!='default':model.load_adapter(folder/'checkpoint/adapters'/name,adapter_name=name)
    parameters=dict(model.named_parameters())
    for name,value in state['heads'].items():
        if name not in parameters or parameters[name].shape!=value.shape:raise RuntimeError(f'Checkpoint head mismatch {name}')
        parameters[name].data.copy_(value)
    if args['architecture']=='head_only':
        if any(torch.count_nonzero(p).item() for n,p in parameters.items() if 'lora_B' in n):
            raise RuntimeError('Reloaded head-only checkpoint has nonzero LoRA')
    model=model.to('cuda').eval()
    pool=SimpleNamespace(model=model,tok=tok,device=torch.device('cuda'),
        states={n:SimpleNamespace(memory=SimpleNamespace(items=state['states'][n]['items'])) for n in names},
        activate=model.set_adapter)
    pool.activate(state['last_real_name'])
    return pool,state['last_real_name'],provenance


@torch.no_grad()
def evaluate_learned(pool,eval_sets,feature_sets,gate,names):
    rows=[]
    for concept,eval_set in eval_sets.items():
        features=feature_sets[concept]
        weights=gate.predict_proba(features) if gate is not None else np.ones((len(features),1))
        if gate is not None and list(gate[-1].classes_)!=list(range(len(names))):raise RuntimeError('Router class order mismatch')
        totals={r:{'correct':0,'loss':0.,'n':0} for r in ['linear_hard','linear_probability_mixture']}
        for start in range(0,len(features),64):
            texts=eval_set['texts'][start:start+64]
            x=encode(pool.tok,texts,pool.device)
            logits=[]
            for name in names:
                pool.activate(name);pool.model.eval()
                logits.append(pool.model(**x).logits)
            logits=torch.stack(logits,dim=1)
            w=torch.tensor(weights[start:start+64],device=pool.device,dtype=logits.dtype)
            chosen=w.argmax(-1)
            scores={'linear_hard':logits[torch.arange(len(texts),device=pool.device),chosen],
                    'linear_probability_mixture':(w.unsqueeze(-1)*logits.softmax(-1)).sum(1).clamp_min(1e-30).log()}
            # Labels are introduced only after all route decisions and class scores.
            labels=torch.tensor(eval_set['labels'][start:start+64],device=pool.device)
            for rule,value in scores.items():
                totals[rule]['correct']+=int((value.argmax(-1)==labels).sum())
                totals[rule]['loss']+=float(F.cross_entropy(value,labels,reduction='sum'))
                totals[rule]['n']+=len(texts)
        for rule,m in totals.items():rows.append({'concept':concept,'rule':rule,'n':m['n'],
             'accuracy':m['correct']/m['n'],'loss':m['loss']/m['n']})
    return rows


def main():
    os.environ['OMP_NUM_THREADS']='8';os.environ['TOKENIZERS_PARALLELISM']='false';torch.set_num_threads(8)
    cutoff=datetime.fromisoformat('2026-10-06T03:20:00+00:00')
    for status_file,expected in [('day6_queue_status.json',80),('day7_queue_status.json',24)]:
        while datetime.now(timezone.utc)<cutoff:
            path=Path('logs')/status_file
            if path.exists():
                records=json.loads(path.read_text())
                if records and records[-1]['status']=='failed':raise RuntimeError(f'Prior queue failed: {status_file}')
                if len(records)==expected and all(r['status']=='completed' for r in records):break
            time.sleep(15)
        else:raise RuntimeError('Router diagnostic launch cutoff reached')
    sets={};features={};all_rows=[];status=[]
    folders=sorted([p for pattern in ['day5_*_seed2026','day6_*_seed*','day7_multinli_*_seed*']
                    for p in Path('results').glob(pattern)])
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
    print('LEARNED_ROUTING_FINISHED',len(status),flush=True)


if __name__=='__main__':main()
