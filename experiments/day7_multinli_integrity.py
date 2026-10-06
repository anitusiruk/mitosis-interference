"""Data/group separation and pair-tokenization checks before live outcomes."""
from collections import Counter
from transformers import AutoTokenizer
from experiments.day7_multinli_data import build_multinli,PairTokenizer,premise_key

sharp,_,dev,manifest=build_multinli(2026,'sharp')
blurry,_,other_dev,_=build_multinli(2026,'blurry')
assert dev==other_dev
assert len(sharp)==len(blurry)==90
ids=lambda stream:[x for b in stream for x in b['source_ids']]
assert sorted(ids(sharp))==sorted(ids(blurry))
assert len(set(ids(sharp)))==1440
assert Counter(y for b in sharp for y in b['labels'])==Counter({0:480,1:480,2:480})
assert Counter(y for b in blurry for y in b['labels'])==Counter({0:480,1:480,2:480})
train_groups={x for b in sharp for x in b['premise_keys']}
dev_groups={x for e in dev.values() for x in e['premise_keys']}
assert not train_groups & dev_groups
assert premise_key('Some   Text')==premise_key('some text')
for j in range(4):
    assert [b['newer_count'] for b in blurry if b.get('transition_index')==j]==[1,3,5,7,9,11,13,15]
base=AutoTokenizer.from_pretrained('distilbert-base-uncased')
wrapped=PairTokenizer(base)
pairs=sharp[0]['texts'][:2]
args={'padding':True,'truncation':True,'max_length':64,'return_tensors':'pt'}
a=wrapped(pairs,**args);b=base([x[0] for x in pairs],text_pair=[x[1] for x in pairs],**args)
for k in a:assert (a[k]==b[k]).all()
assert ((a['input_ids']==base.sep_token_id).sum(1)==2).all()
print('DAY7_MULTINLI_DATA_INTEGRITY_PASS',manifest,flush=True)
