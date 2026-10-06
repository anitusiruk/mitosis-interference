"""Component factorial trials: exact non-invasion and matched-update checks."""
import torch
from transformers import DistilBertConfig, DistilBertForSequenceClassification
from peft import LoraConfig, TaskType, get_peft_model

from experiments.signal_scan import seed_all,encode
from experiments.day3_action_utility_unit import nested_equal
from experiments.day5_shared_head_integrity import Tokenizer,snapshot,check
from src.adapter_pool_cau_v1 import CAUV1AdapterPool
from src.component_intervention_audit import VARIANTS,component_trial,crossfit_components


def main():
    seed_all(2026)
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    base=DistilBertForSequenceClassification(DistilBertConfig(vocab_size=64,dim=32,
        hidden_dim=64,n_heads=4,n_layers=2,num_labels=3,
        dropout=0.1,attention_dropout=0.1,seq_classif_dropout=0.1))
    cfg=LoraConfig(task_type=TaskType.SEQ_CLS,r=2,lora_alpha=4,lora_dropout=0.,
                   target_modules=['q_lin','v_lin'],bias='none')
    model=get_peft_model(base,cfg).to(device)
    pool=CAUV1AdapterPool(model=model,tokenizer=Tokenizer(),lora_config=cfg,device=device,
                         lr=2e-4,memory_size=16,memory_probe=4,threshold=0.,seed=2026)
    texts,labels=['good item','bad item','new item','old item'],[0,1,2,0]
    for _ in range(3):
        pool.train_step('default',texts,labels)
    pool.warmup_name=None
    before=snapshot(pool)
    trials={}
    for variant in VARIANTS:
        trials[variant]=component_trial(pool,'default',texts,labels,texts,labels,variant)
        check(variant+' restores all real state',nested_equal(before,snapshot(pool)))
    for variant in ['reuse_lora_common_frozen_head','fresh_lora_common_frozen_head']:
        check(variant+' changes no head parameters',trials[variant]['head_update_l2']==0.)
    pool.train_step('default',texts,labels)
    pool.model.eval()
    with torch.no_grad():
        actual=float(pool.model(**encode(pool.tok,texts,device),labels=torch.tensor(labels,device=device)).loss)
    check('cloned inherited-components trial matches exact real optimizer update',
          abs(actual-trials['reuse_lora_inherit_head']['query_after'])<1e-7)
    before=snapshot(pool)
    records=crossfit_components(pool,texts+['fifth item'],labels+[1],'default')
    check('odd batch queries each example once per variant',all(
        sum(r['query_n'] for r in records if r['variant']==v)==5 for v in VARIANTS))
    check('all factorial folds jointly remain non-invasive',nested_equal(before,snapshot(pool)))
    print('DAY5_COMPONENT_INTEGRITY_PASS',flush=True)


if __name__=='__main__':
    main()
