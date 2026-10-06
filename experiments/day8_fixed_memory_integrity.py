"""Real tiny PEFT state and reservoir budget invariants."""
import copy
import torch
from transformers import DistilBertConfig,DistilBertForSequenceClassification
from peft import LoraConfig,TaskType,get_peft_model
from experiments.day5_shared_head_integrity import Tokenizer,snapshot
from experiments.day3_action_utility_unit import nested_equal
from src.adapter_pool_fixed_memory import FixedMemoryCAUV1AdapterPool,FixedMemoryHeadOnlyCAUV1AdapterPool
from src.adapter_pool_cau_v1 import CAUV1AdapterPool
from src.adapter_pool_head_only import HeadOnlyCAUV1AdapterPool

for cls in [FixedMemoryCAUV1AdapterPool,FixedMemoryHeadOnlyCAUV1AdapterPool]:
    torch.manual_seed(700)
    base=DistilBertForSequenceClassification(DistilBertConfig(vocab_size=100,dim=16,hidden_dim=32,n_layers=1,n_heads=2,num_labels=3,dropout=.1,seq_classif_dropout=.1))
    cfg=LoraConfig(task_type=TaskType.SEQ_CLS,r=2,lora_alpha=4,lora_dropout=0.,target_modules=['q_lin','v_lin'],bias='none')
    model=get_peft_model(base,cfg).to('cuda')
    pool=cls(model=model,tokenizer=Tokenizer(),lora_config=cfg,device=torch.device('cuda'),
        lr=2e-4,memory_size=16,memory_probe=4,total_memory_budget=16,max_adapters=4,seed=2026)
    for i in range(32):pool.states['default'].memory.add(str(i),i%3)
    pool.train_step('default',['one','two','three','four'],[0,1,2,0])
    pool.warmup_name=None
    reference_class=CAUV1AdapterPool if cls is FixedMemoryCAUV1AdapterPool else HeadOnlyCAUV1AdapterPool
    reference=reference_class(model=copy.deepcopy(pool.model),tokenizer=Tokenizer(),lora_config=cfg,
        device=torch.device('cuda'),lr=2e-4,memory_size=16,memory_probe=4,seed=2026)
    reference.states['default'].optimizer.load_state_dict(copy.deepcopy(pool.states['default'].optimizer.state_dict()))
    reference.states['default'].memory=copy.deepcopy(pool.states['default'].memory)
    reference.warmup_name=None
    a=pool.crossfit_action_utility(['one','two','three','four'],[0,1,2,0],'default')
    b=reference.crossfit_action_utility(['one','two','three','four'],[0,1,2,0],'default')
    for key in ['budget_blocked_fresh','total_memory_budget','max_adapters']:a.pop(key)
    assert nested_equal(a,b),'No-shrink state cleanup altered prospective action scores'
    original_seen=pool.states['default'].memory.seen
    name=pool.spawn()
    assert pool.states['default'].memory.seen==original_seen==36
    assert len(pool.states['default'].memory.items)==8
    assert all(s.memory.capacity==8 for s in pool.states.values())
    pool.train_step(name,['one','two','three','four'],[0,1,2,0])
    pool.train_step('default',['one','two','three','four'],[0,1,2,0])
    before=snapshot(pool)
    pool.shadow_reuse('default',['one','two'],[0,1],['three','four'],[2,0],'default')
    assert nested_equal(before,snapshot(pool))
    pool.spawn();pool.spawn()
    assert len(pool.states)==4
    assert all(s.memory.capacity==4 for s in pool.states.values())
    assert sum(len(s.memory.items) for s in pool.states.values())<=16
    for adapter in pool.states:
        if len(pool.states[adapter].memory.items)<4:
            pool.train_step(adapter,['one','two','three','four'],[0,1,2,0])
    pool.activate('default');pool.warmup_name=None
    before=snapshot(pool)
    result=pool.crossfit_action_utility(['one','two','three','four'],[0,1,2,0],'default')
    assert result['status']=='ok'
    assert nested_equal(before,snapshot(pool))
    assert not result['fresh_positive']
    assert result['max_adapters']==4
    try:pool.spawn()
    except RuntimeError as error:assert 'cap' in str(error)
    else:raise AssertionError('Hard cap allowed spawn')
    print(cls.__name__,'budget, historical seen, exact shadow restoration, cap PASS',flush=True)
print('DAY8_FIXED_MEMORY_INTEGRITY_PASS',flush=True)
