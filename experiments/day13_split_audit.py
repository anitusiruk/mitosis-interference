"""Offline duplicate/truncation audit of existing development inputs only."""
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import unicodedata
os.environ['OMP_NUM_THREADS']='1';os.environ['TOKENIZERS_PARALLELISM']='false'
import numpy as np
import pandas as pd
import torch
from datasets import load_dataset
from transformers import AutoTokenizer
from experiments.controller_recurrence_cau_v1 import make_dev_split,make_recurrence_stream
from experiments.domain_recurrence_data import build_domain_recurrence
from experiments.day7_multinli_data import build_multinli,PairTokenizer

torch.set_num_threads(1)
def normal(text):
    if isinstance(text,(tuple,list)):return tuple(normal(x) for x in text)
    return ' '.join(unicodedata.normalize('NFKC',str(text)).casefold().split())
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False).encode()).hexdigest()
def token_ids(tok,texts,truncation):
    result=[]
    for start in range(0,len(texts),128):
        batch=texts[start:start+128]
        args={'truncation':truncation,'padding':False}
        if truncation:args['max_length']=64
        result.extend(tok(batch,**args)['input_ids'])
    return result

started=datetime.now(timezone.utc).isoformat()
tok=AutoTokenizer.from_pretrained('distilbert-base-uncased')
bank=load_dataset('PolyAI/banking77',split='train',trust_remote_code=True)
train,dev=make_dev_split(bank)
labels=np.asarray(dev['label']);bank_dev=[dev[int(i)]['text'] for i in np.flatnonzero(labels<33)]
rows=[]
for regime,seeds in [('banking',range(2026,2032)),('amazon',range(2026,2032)),('multinli',range(2026,2029))]:
    for seed in seeds:
        if regime=='banking':
            stream,_=make_recurrence_stream(train,16,seed);evaluation=bank_dev;tokenizer=tok
        elif regime=='amazon':
            stream,_,sets=build_domain_recurrence(seed)
            evaluation=[t for s in sets.values() for t in s['texts']];tokenizer=tok
        else:
            stream,_,sets,manifest=build_multinli(seed)
            evaluation=[t for s in sets.values() for t in s['texts']];tokenizer=PairTokenizer(tok)
        incoming=[t for b in stream for t in b['texts']]
        train_hashes=[digest(normal(t)) for t in incoming];dev_hashes=[digest(normal(t)) for t in evaluation]
        train_tokens=token_ids(tokenizer,incoming,True);dev_tokens=token_ids(tokenizer,evaluation,True)
        train_token_hashes={digest(x) for x in train_tokens};dev_token_hashes={digest(x) for x in dev_tokens}
        lengths=[len(x) for x in token_ids(tokenizer,incoming,False)]
        dev_lengths=[len(x) for x in token_ids(tokenizer,evaluation,False)]
        shared=set(train_hashes)&set(dev_hashes)
        row={'regime':regime,'seed':seed,'training_examples':len(incoming),'development_examples':len(evaluation),
             'normalized_train_dev_unique_overlap':len(shared),
             'development_examples_with_normalized_overlap':sum(x in shared for x in dev_hashes),
             'training_duplicate_normalized_examples':len(incoming)-len(set(train_hashes)),
             'development_duplicate_normalized_examples':len(evaluation)-len(set(dev_hashes)),
             'truncated_token_train_dev_unique_overlap':len(train_token_hashes&dev_token_hashes),
             'training_fraction_over_64_tokens':np.mean(np.asarray(lengths)>64),
             'development_fraction_over_64_tokens':np.mean(np.asarray(dev_lengths)>64),
             'training_median_tokens':float(np.median(lengths)),'development_median_tokens':float(np.median(dev_lengths)),
             'stream_sha256':hashlib.sha256(json.dumps(stream,sort_keys=True).encode()).hexdigest()}
        rows.append(row);pd.DataFrame(rows).to_csv('results/day13_split_audit.csv',index=False)
        print('SPLIT_AUDIT',regime,seed,'overlap',len(shared),'truncated token overlap',row['truncated_token_train_dev_unique_overlap'],flush=True)
Path('results/day13_split_audit_provenance.json').write_text(json.dumps({'start_utc':started,
    'end_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'official_test_or_multinli_validation_used':False,'normalization':'Unicode NFKC, casefold, whitespace collapse',
    'timing_caveat':'Offline CPU-only data audit may overlap queued GPU runs; current wall-clock measurements are descriptive, not dedicated resource benchmarks.',
    'interpretation':'Exact-normalized/token-prefix overlap audit only; does not establish absence of near duplicates, pretrained exposure, or all provenance problems.'},indent=2))
print('SPLIT_AUDIT_COMPLETE',len(rows),flush=True)
