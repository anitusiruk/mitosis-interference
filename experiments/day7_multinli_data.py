"""Train-only, premise-grouped, true-pair MultiNLI recurrence."""
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
from datasets import load_dataset

GENRES={'A':'fiction','B':'government','C':'telephone'}
SCHEDULE=[('A',1),('B',1),('A',2),('C',1),('B',2)]


def premise_key(text):
    return hashlib.sha256(' '.join(str(text).lower().split()).encode()).hexdigest()


class PairTokenizer:
    def __init__(self,tokenizer):self.tokenizer=tokenizer
    def __getattr__(self,name):return getattr(self.tokenizer,name)
    def __call__(self,texts,**kwargs):
        if not texts or not all(isinstance(x,(list,tuple)) and len(x)==2 for x in texts):
            raise TypeError('MultiNLI requires explicit premise/hypothesis input pairs')
        return self.tokenizer([x[0] for x in texts],text_pair=[x[1] for x in texts],**kwargs)


def blur_stream(stream,seed,batch_size=16):
    result=[dict(b) for b in stream]
    boundaries=[i for i in range(1,len(stream)) if (stream[i-1]['concept'],stream[i-1]['occurrence'])!=(stream[i]['concept'],stream[i]['occurrence'])]
    for j,boundary in enumerate(boundaries):
        if boundary<4 or boundary+4>len(stream):raise RuntimeError('Insufficient transition context')
        older=stream[boundary-4:boundary];newer=stream[boundary:boundary+4]
        def flatten(batches):
            return [(text,label,source,group) for b in batches for text,label,source,group in zip(b['texts'],b['labels'],b['source_ids'],b['premise_keys'])]
        old_rows=flatten(older);new_rows=flatten(newer)
        if len(old_rows)!=64 or len(new_rows)!=64:raise RuntimeError('Blurring requires full batches of 16')
        rng=np.random.default_rng(seed+800000+j)
        old_position=new_position=0
        for t,new_count in enumerate([1,3,5,7,9,11,13,15]):
            old_count=batch_size-new_count
            rows=old_rows[old_position:old_position+old_count]+new_rows[new_position:new_position+new_count]
            old_position+=old_count;new_position+=new_count
            rng.shuffle(rows)
            metadata=older[0] if t<4 else newer[0]
            result[boundary-4+t]={k:metadata[k] for k in ['concept','occurrence','domain']}
            result[boundary-4+t].update(texts=[r[0] for r in rows],labels=[r[1] for r in rows],
               source_ids=[r[2] for r in rows],premise_keys=[r[3] for r in rows],
               newer_count=new_count,transition_index=j)
        assert old_position==new_position==64
    assert sorted(x for b in stream for x in b['source_ids'])==sorted(x for b in result for x in b['source_ids'])
    return result


def build_multinli(seed,boundary_condition='sharp'):
    cache=Path('data/day7_cache')
    cache.mkdir(parents=True,exist_ok=True)
    cached=cache/f'premise_group_v1_seed{seed}.json.gz'
    if cached.exists():
        with gzip.open(cached,'rt') as f:payload=json.load(f)
        if payload['manifest']['source_file_sha256']!=hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
            raise RuntimeError('Cached data was built with a different data protocol source')
    else:
        ds=load_dataset('nyu-mll/multi_nli',split='train')
        pools=defaultdict(list)
        for row in ds:
            if row['genre'] not in GENRES.values() or int(row['label']) not in [0,1,2]:continue
            key=premise_key(row['premise'])
            partition='dev' if int(key,16)%10==0 else 'train'
            pools[(row['genre'],int(row['label']),partition)].append(
                {'text':[row['premise'],row['hypothesis']],'label':int(row['label']),
                 'source':row['pairID'],'premise_key':key})
        rng=np.random.default_rng(seed+9000)
        eval_rng=np.random.default_rng(424242)
        selections={};eval_sets={}
        for concept,genre in GENRES.items():
            dev_rows=[]
            for label in range(3):
                train_rows=pools[(genre,label,'train')]
                ids=np.arange(len(train_rows));rng.shuffle(ids)
                need=192 if concept in ['A','B'] else 96
                if len(ids)<need:raise RuntimeError('Insufficient training pool')
                chosen=[train_rows[int(i)] for i in ids[:need]]
                selections[(concept,1,label)]=chosen[:96]
                if concept in ['A','B']:selections[(concept,2,label)]=chosen[96:192]
                dev_pool=pools[(genre,label,'dev')]
                ids=np.arange(len(dev_pool));eval_rng.shuffle(ids)
                if len(ids)<64:raise RuntimeError('Insufficient development pool')
                dev_rows.extend(dev_pool[int(i)] for i in ids[:64])
            eval_sets[concept]={'domain':genre,'texts':[x['text'] for x in dev_rows],
                'labels':[x['label'] for x in dev_rows],'source_ids':[x['source'] for x in dev_rows],
                'premise_keys':[x['premise_key'] for x in dev_rows]}
        stream=[]
        for concept,occurrence in SCHEDULE:
            rows=[r for label in range(3) for r in selections[(concept,occurrence,label)]]
            rng.shuffle(rows)
            for start in range(0,len(rows),16):
                chunk=rows[start:start+16]
                stream.append({'concept':concept,'occurrence':occurrence,'domain':GENRES[concept],
                    'texts':[x['text'] for x in chunk],'labels':[x['label'] for x in chunk],
                    'source_ids':[x['source'] for x in chunk],'premise_keys':[x['premise_key'] for x in chunk]})
        train_groups={x for b in stream for x in b['premise_keys']}
        dev_groups={x for e in eval_sets.values() for x in e['premise_keys']}
        if train_groups & dev_groups:raise RuntimeError('Premise leakage')
        sources=[x for b in stream for x in b['source_ids']]
        if len(sources)!=len(set(sources)):raise RuntimeError('Duplicate training pair ID')
        manifest={'dataset':'nyu-mll/multi_nli','split':'train','dataset_fingerprint':ds._fingerprint,
            'development_rule':'normalized premise SHA256 modulo 10 == 0','official_validation_used':False,
            'training_examples':len(sources),'development_examples':sum(len(e['texts']) for e in eval_sets.values()),
            'train_dev_premise_overlap':0,'source_file_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        payload={'stream':stream,'eval_sets':eval_sets,'manifest':manifest}
        with gzip.open(cached,'wt') as f:json.dump(payload,f)
    stream=payload['stream']
    if boundary_condition=='blurry':stream=blur_stream(stream,seed)
    boundaries=[i+1 for i in range(1,len(stream)) if (stream[i-1]['concept'],stream[i-1]['occurrence'])!=(stream[i]['concept'],stream[i]['occurrence'])]
    return stream,boundaries,payload['eval_sets'],{**payload['manifest'],'boundary_condition':boundary_condition}
