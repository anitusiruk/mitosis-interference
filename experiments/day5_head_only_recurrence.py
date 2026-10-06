"""Head-only control reusing the fixed Day-5 recurrence harness."""
import argparse
from collections import Counter
import hashlib
import importlib.metadata as metadata
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import LoraConfig, TaskType, get_peft_model

from experiments.signal_scan import seed_all, encode, base_features
from experiments.day2_predictor_scan_rngsafe import capture_rng_state, restore_rng_state
from experiments.controller_recurrence_cau_v1 import make_dev_split, make_recurrence_stream, evaluate_adapter_concept
from experiments.controller_domain_recurrence_cau_v1 import evaluate_adapter_domain
from experiments.domain_recurrence_data import build_domain_recurrence
from experiments.day3_action_utility_unit import nested_equal
from experiments.day5_shared_head_integrity import snapshot
from src.adapter_pool_cau_v1 import CAUV1AdapterPool
from src.adapter_pool_shared_head import SharedHeadCAUV1AdapterPool
from src.adapter_pool_head_only import HeadOnlyCAUV1AdapterPool
from src.component_intervention_audit import crossfit_components


def resources(pool, started):
    params=list(pool.model.named_parameters())
    optimizers={id(s.optimizer):s.optimizer for s in pool.states.values()}.values()
    opt_bytes=sum(t.numel()*t.element_size() for opt in optimizers for state in opt.state.values()
                  for t in state.values() if torch.is_tensor(t))
    return {'lora_parameters':sum(p.numel() for n,p in params if 'lora_' in n),
            'private_head_parameters':sum(p.numel() for n,p in params if '.modules_to_save.' in n),
            'unwrapped_shared_head_parameters':sum(p.numel() for n,p in params
                if ('.pre_classifier.' in n or '.classifier.' in n) and 'modules_to_save' not in n and 'original_module' not in n),
            'total_unique_parameters':sum(p.numel() for _,p in params),
            'currently_trainable_parameters':sum(p.numel() for _,p in params if p.requires_grad),
            'optimizer_state_bytes':opt_bytes,'replay_items':sum(len(s.memory.items) for s in pool.states.values()),
            'elapsed_seconds':time.monotonic()-started,
            'gpu_peak_allocated_bytes':torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0}


@torch.no_grad()
def evaluate_label_free(pool, eval_sets, restore_name):
    """No labels or concept identities enter centroid fitting or prediction."""
    rng=capture_rng_state()
    modes=[(m,m.training) for m in pool.model.modules()]
    flags=[(p,p.requires_grad) for p in pool.model.parameters()]
    names=sorted(pool.states)
    centers=[]
    try:
        for name in names:
            texts=[x[0] for x in pool.states[name].memory.items]
            if not texts:
                raise RuntimeError('Cannot fit centroid for empty reservoir')
            chunks=[base_features(pool.model,pool.tok,texts[i:i+64],pool.device) for i in range(0,len(texts),64)]
            centers.append(F.normalize(torch.cat(chunks).mean(0),dim=0))
        centers=torch.stack(centers)
        rows=[]
        for concept, eval_set in eval_sets.items():
            totals={rule:{'loss':0.,'correct':0,'n':0} for rule in ['last_active','uniform_probability','frozen_centroid']}
            counts=Counter()
            for start in range(0,len(eval_set['texts']),64):
                texts=eval_set['texts'][start:start+64]
                labels=torch.tensor(eval_set['labels'][start:start+64],device=pool.device)
                # Gold labels are used only AFTER prediction for metric evaluation.
                features=base_features(pool.model,pool.tok,texts,pool.device)
                chosen=(features@centers.T).argmax(1)
                counts.update(names[int(i)] for i in chosen.cpu())
                x=encode(pool.tok,texts,pool.device)
                logits=[]
                for name in names:
                    pool.activate(name)
                    pool.model.eval()
                    logits.append(pool.model(**x).logits)
                logits=torch.stack(logits)
                probabilities=logits.softmax(-1)
                selected=logits[chosen,torch.arange(len(texts),device=pool.device)]
                predictions={
                    'last_active':logits[names.index(restore_name)],
                    'uniform_probability':probabilities.mean(0).clamp_min(1e-30).log(),
                    'frozen_centroid':selected}
                for rule, scores in predictions.items():
                    totals[rule]['loss']+=float(F.cross_entropy(scores,labels,reduction='sum'))
                    totals[rule]['correct']+=int((scores.argmax(-1)==labels).sum())
                    totals[rule]['n']+=len(texts)
            for rule,m in totals.items():
                rows.append({'concept':concept,'rule':rule,'n':m['n'],
                             'loss':m['loss']/m['n'],'accuracy':m['correct']/m['n'],
                             'centroid_routing_counts':json.dumps(dict(counts),sort_keys=True)})
        return rows
    finally:
        pool.activate(restore_name)
        for p,flag in flags:p.requires_grad_(flag)
        for m,mode in modes:m.training=mode
        restore_rng_state(rng)


def checkpoint(pool, out, last_name, step):
    folder=out/'checkpoint'
    folder.mkdir(exist_ok=True)
    pool.model.save_pretrained(folder/'adapters', safe_serialization=True)
    # PEFT feature extraction deliberately excludes the common classifier from
    # adapter weights; save it explicitly alongside its single optimizer state.
    head={n:p.detach().cpu() for n,p in pool.model.named_parameters()
          if '.pre_classifier.' in n or '.classifier.' in n}
    optimizer_names={}
    optimizers={}
    for name,state in pool.states.items():
        key=optimizer_names.setdefault(id(state.optimizer),name)
        optimizers[key]=state.optimizer.state_dict()
    torch.save({'step':step,'last_real_name':last_name,'heads':head,'optimizers':optimizers,
        'optimizer_for_adapter':{n:optimizer_names[id(s.optimizer)] for n,s in pool.states.items()},
        'states':{n:{'updates':s.updates,'items':s.memory.items,'seen':s.memory.seen,
                     'memory_rng':s.memory.rng.getstate()} for n,s in pool.states.items()},
        'pending_fresh':pool.pending_fresh,'warmup_name':pool.warmup_name,'next_id':pool.next_id,
        'rng':capture_rng_state()},folder/'learner_state.pt')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--regime',choices=['banking','amazon'],required=True)
    parser.add_argument('--architecture',choices=['private','shared','head_only'],required=True)
    parser.add_argument('--seed',type=int,default=2026)
    parser.add_argument('--batch-size',type=int,default=16)
    parser.add_argument('--component-audit',action='store_true')
    parser.add_argument('--policy',choices=['cau','single'],default='cau')
    parser.add_argument('--output',required=True)
    parser.add_argument('--deadline-utc',default='2026-10-06T03:30:00+00:00')
    args=parser.parse_args()
    os.environ['TOKENIZERS_PARALLELISM']='false'
    os.environ['OMP_NUM_THREADS']='8'
    torch.set_num_threads(8)
    if args.component_audit and args.architecture!='private':
        parser.error('Factorial attribution is on the original private-package trajectory')
    out=Path(args.output)
    out.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    seed_all(args.seed)
    if not torch.cuda.is_available():raise RuntimeError('CUDA required')
    torch.cuda.reset_peak_memory_stats()
    device=torch.device('cuda')
    if args.regime=='banking':
        ds=load_dataset('PolyAI/banking77',split='train',trust_remote_code=True)
        train,dev=make_dev_split(ds)
        stream,boundaries=make_recurrence_stream(train,args.batch_size,args.seed)
        concept_labels={'A':list(range(0,11)),'B':list(range(11,22)),'C':list(range(22,33))}
        eval_sets={}
        dl=np.asarray(dev['label'])
        for concept,labels in concept_labels.items():
            ids=np.flatnonzero(np.isin(dl,labels))
            eval_sets[concept]={'texts':[dev[int(i)]['text'] for i in ids],
                                'labels':[int(dev[int(i)]['label']) for i in ids]}
        num_labels=77
    else:
        stream,boundaries,eval_sets=build_domain_recurrence(args.seed,batch_size=args.batch_size)
        num_labels=2
    tok=AutoTokenizer.from_pretrained('distilbert-base-uncased')
    base=AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased',num_labels=num_labels)
    cfg=LoraConfig(task_type=TaskType.FEATURE_EXTRACTION if args.architecture=='shared' else TaskType.SEQ_CLS,
        r=8,lora_alpha=16,lora_dropout=0.,target_modules=['q_lin','v_lin'],bias='none')
    model=get_peft_model(base,cfg).to(device)
    cls={'private':CAUV1AdapterPool,'shared':SharedHeadCAUV1AdapterPool,
         'head_only':HeadOnlyCAUV1AdapterPool}[args.architecture]
    pool=cls(model=model,tokenizer=tok,lora_config=cfg,device=device,lr=2e-4,
        memory_size=512,memory_probe=64,threshold=0.,confidence_z=1.96,seed=args.seed)
    pool.activate('default')
    provenance={'args':vars(args),'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'python':sys.version,'gpu':torch.cuda.get_device_name(0),
        'packages':{p:metadata.version(p) for p in ['torch','transformers','peft','datasets','numpy','pandas','scikit-learn']},
        'model_revision':getattr(base.config,'_commit_hash',None),
        'stream_sha256':hashlib.sha256(json.dumps(stream,sort_keys=True).encode()).hexdigest(),
        'stream_steps':len(stream),'boundaries_evaluation_only':boundaries,
        'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for pattern in ['src/*.py','experiments/day5*.py','notes/day5*spec.md'] for p in Path('.').glob(pattern)},
        'official_test_used':False}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2))
    rows,eval_rows,router_rows,component_rows=[],[],[],[]
    timing={'component_audit_seconds':0.,'live_training_seconds':0.,'evaluation_seconds':0.}
    last_name='default'
    seen=set()
    status='completed'
    deadline=datetime.fromisoformat(args.deadline_utc)
    event_path=out/'events.jsonl'
    with event_path.open('w') as events:
        for step,batch in enumerate(stream,1):
            if datetime.now(timezone.utc)>=deadline:
                status='deadline_stopped'
                break
            segment=f"{batch['concept']}{batch['occurrence']}"
            seen.add(batch['concept'])
            if args.component_audit and pool.warmup_name is not None and len(pool.states[pool.warmup_name].memory.items)>=pool.memory_probe:
                # Normalize lifecycle exactly as frozen select_action would.
                pool.warmup_name=None
            if args.component_audit and pool.warmup_name is None:
                phase_start=time.monotonic()
                before=snapshot(pool)
                audit=crossfit_components(pool,batch['texts'],batch['labels'],last_name)
                if not nested_equal(before,snapshot(pool)):
                    raise RuntimeError(f'Component audit mutated real learner at step {step}')
                component_rows.extend({'step':step,'segment':segment,**r} for r in audit)
                pd.DataFrame(component_rows).to_csv(out/'component_trials.csv',index=False)
                timing['component_audit_seconds']+=time.monotonic()-phase_start
            phase_start=time.monotonic()
            if args.policy=='single':
                name='default'
                loss=pool.train_step(name,batch['texts'],batch['labels'])
                info={'decision':'single_update','reason':'fixed_single_adapter'}
            else:
                name,info,loss=pool.live_step(batch['texts'],batch['labels'],last_name)
            timing['live_training_seconds']+=time.monotonic()-phase_start
            if loss is not None and not math.isfinite(loss):
                raise RuntimeError(f'Nonfinite real loss at step {step}')
            last_name=name
            row={'step':step,'segment':segment,'concept':batch['concept'],'occurrence':batch['occurrence'],
                'adapter':name,'decision':info['decision'],'reason':info.get('reason'),'loss':loss,
                'num_adapters':len(pool.states),'train_executed':loss is not None,
                **resources(pool,started),**timing}
            utility=info.get('utility',{})
            for key in ['statusquo_loss','fresh_utility','best_reuse_utility','fresh_advantage','fresh_positive','fresh_feasible_both']:
                row[key]=utility.get(key)
            row['info']=json.dumps(info,sort_keys=True,allow_nan=False)
            rows.append(row)
            events.write(json.dumps(row)+'\n')
            events.flush()
            pd.DataFrame(rows).to_csv(out/'routing.csv',index=False)
            if step%5==0 or info['decision']=='spawn':
                print(f"step={step} segment(eval)={segment} decision={info['decision']} adapter={name} pool={len(pool.states)} elapsed={row['elapsed_seconds']:.1f}",flush=True)
            segment_end=step==len(stream) or batch['concept']!=stream[step]['concept'] or batch['occurrence']!=stream[step]['occurrence']
            if segment_end:
                phase_start=time.monotonic()
                for adapter in list(pool.states):
                    for concept in eval_sets:
                        if args.regime=='banking':
                            metrics=evaluate_adapter_concept(pool,adapter,name,dev,concept_labels[concept])
                        else:
                            metrics=evaluate_adapter_domain(pool,adapter,name,eval_sets[concept])
                        eval_rows.append({'checkpoint':segment,'step':step,'adapter':adapter,'concept':concept,
                                          'seen_concept':concept in seen,**metrics})
                pd.DataFrame(eval_rows).to_csv(out/'eval_matrix.csv',index=False)
                routes=evaluate_label_free(pool,eval_sets,name)
                router_rows.extend({'checkpoint':segment,'step':step,'seen_concept':r['concept'] in seen,**r} for r in routes)
                pd.DataFrame(router_rows).to_csv(out/'label_free_eval.csv',index=False)
                print('CHECKPOINT',segment,'label-free full-space accuracy',
                      {r['rule']+':'+r['concept']:round(r['accuracy'],4) for r in routes},flush=True)
                timing['evaluation_seconds']+=time.monotonic()-phase_start
    checkpoint(pool,out,last_name,len(rows))
    summary={'status':status,'steps':len(rows),'learning_updates':sum(r['train_executed'] for r in rows),
        'decisions':dict(Counter(r['decision'] for r in rows)),'final_adapters':list(pool.states),
        'pool_summary':pool.summary(),'resources':resources(pool,started),
        'timing':timing,
        'component_trial_rows':len(component_rows),'official_test_used':False}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    print('FINAL_SUMMARY',json.dumps(summary),flush=True)


if __name__=='__main__':
    main()
