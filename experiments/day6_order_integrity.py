"""Reordering changes only segment order and evaluation-only boundaries."""
from experiments.day6_frozen_diagnostics import reorder_stream

stream=[]
keys=[('A',1),('B',1),('A',2),('C',1),('B',2)]
for concept,occurrence in keys:
    for i in range(3):stream.append({'concept':concept,'occurrence':occurrence,'texts':[f'{concept}{occurrence}:{i}'],'labels':[i]})
canonical,boundaries=reorder_stream(stream,'canonical')
assert canonical==stream
assert boundaries==[4,7,10,13]
alternate,other_boundaries=reorder_stream(stream,'b_first')
assert [alternate[i]['concept'] for i in range(0,15,3)]==['B','A','B','C','A']
assert other_boundaries==boundaries
assert sorted(id(b) for b in alternate)==sorted(id(b) for b in stream)
for key in keys:
    assert [b['texts'] for b in alternate if (b['concept'],b['occurrence'])==key]==[b['texts'] for b in stream if (b['concept'],b['occurrence'])==key]
print('DAY6_ORDER_INTEGRITY_PASS: identical examples, labels and within-segment order',flush=True)
