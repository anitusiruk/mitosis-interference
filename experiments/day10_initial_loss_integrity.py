"""Ranking semantics and core state restoration for the scoring ablation."""
import copy
import torch
from transformers import DistilBertConfig,DistilBertForSequenceClassification
from peft import LoraConfig,TaskType,get_peft_model
from experiments.day5_shared_head_integrity import Tokenizer
from experiments.day3_action_utility_unit import snapshot_pool,nested_equal
from src.adapter_pool_initial_loss import initial_loss_scores,InitialLossCAUV1AdapterPool,InitialLossHeadOnlyCAUV1AdapterPool

def profile(before,after,feasible=True):
    return dict(query_before=before,query_after=after,system_utility=5-after,feasible_both=feasible,
                harm_lcb_max=-.01,harm_mean=-.02)
original=dict(status='ok',statusquo_loss=5.,fresh_query_before=3.,fresh_utility=.2,best_reuse='b',
    best_reuse_utility=1.,reuse_profiles={'b':profile(4.,2.),'a':profile(4.,3.),'c':profile(1.,1.,False)})
saved=copy.deepcopy(original);x=initial_loss_scores(original)
assert original==saved
assert x['best_reuse']=='a' and x['best_reuse_utility']==1. and x['fresh_utility']==2. and x['fresh_positive']
empty=copy.deepcopy(original)
for p in empty['reuse_profiles'].values():p['feasible_both']=False
assert initial_loss_scores(empty)['best_reuse'] is None
empty['fresh_query_before']=5.
assert not initial_loss_scores(empty)['fresh_positive']
assert initial_loss_scores({'status':'warmup'})=={'status':'warmup'}
for cls in [InitialLossCAUV1AdapterPool,InitialLossHeadOnlyCAUV1AdapterPool]:
    torch.manual_seed(900)
    base=DistilBertForSequenceClassification(DistilBertConfig(vocab_size=100,dim=16,hidden_dim=32,n_layers=1,n_heads=2,num_labels=3))
    cfg=LoraConfig(task_type=TaskType.SEQ_CLS,r=2,lora_alpha=4,lora_dropout=0.,target_modules=['q_lin','v_lin'],bias='none')
    pool=cls(model=get_peft_model(base,cfg).to('cuda'),tokenizer=Tokenizer(),lora_config=cfg,
        device=torch.device('cuda'),lr=2e-4,memory_size=16,memory_probe=4,seed=2026)
    pool.train_step('default',['one','two','three','four'],[0,1,2,0]);pool.warmup_name=None
    before=snapshot_pool(pool)
    result=pool.crossfit_action_utility(['one','two','three','four'],[0,1,2,0],'default')
    assert nested_equal(before,snapshot_pool(pool))
    assert result['scoring_policy']=='pre_update_query_loss_ablation'
    print(cls.__name__,'core learner state/RNG/optimizer/reservoir restoration PASS',flush=True)
print('DAY10_INITIAL_LOSS_INTEGRITY_PASS',flush=True)
