"""Architecture-port checks on tiny local BERT, without downloaded research data."""
import argparse
import torch
from transformers import BertConfig, BertForSequenceClassification
from peft import LoraConfig, TaskType, get_peft_model

from experiments.signal_scan import seed_all, encode
from experiments.day3_action_utility_unit import nested_equal
from experiments.day5_shared_head_integrity import Tokenizer, snapshot, check
from src.adapter_pool_fixed_memory import FixedMemoryCAUV1AdapterPool, FixedMemoryHeadOnlyCAUV1AdapterPool
from src.component_intervention_audit import component_parameters, component_trial


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--device',choices=['cpu','cuda'],default='cpu')
    args=parser.parse_args();device=torch.device(args.device);torch.set_num_threads(2)
    for architecture,kind in [('private',FixedMemoryCAUV1AdapterPool),('head_only',FixedMemoryHeadOnlyCAUV1AdapterPool)]:
        seed_all(2032)
        base=BertForSequenceClassification(BertConfig(vocab_size=64,hidden_size=32,
            intermediate_size=64,num_attention_heads=4,num_hidden_layers=2,num_labels=3,
            hidden_dropout_prob=.1,attention_probs_dropout_prob=.1,classifier_dropout=.1))
        cfg=LoraConfig(task_type=TaskType.SEQ_CLS,r=2,lora_alpha=4,lora_dropout=0.,
            target_modules=['query','value'],bias='none')
        model=get_peft_model(base,cfg).to(device)
        pool=kind(model=model,tokenizer=Tokenizer(),lora_config=cfg,device=device,lr=2e-4,
            memory_size=32,total_memory_budget=32,memory_probe=4,max_adapters=8,threshold=0.,seed=2032)
        texts,labels=['good item','bad item','new item','old item'],[0,1,2,0]
        for _ in range(3): pool.train_step('default',texts,labels)
        pool.warmup_name=None
        parameters=component_parameters(model,'default')
        check(architecture+' single private linear classifier',sum(k=='head' for k,p in parameters.values())==2)
        check(architecture+' frozen pooler',all(not p.requires_grad for n,p in model.named_parameters() if '.pooler.' in n))
        before=snapshot(pool)
        pool.crossfit_action_utility(texts,labels,'default')
        check(architecture+' exact crossfit state restoration',nested_equal(before,snapshot(pool)))
        trial=pool.shadow_reuse('default',texts,labels,texts,labels,'default')
        check(architecture+' inherited intervention restoration',nested_equal(before,snapshot(pool)))
        pool.train_step('default',texts,labels);model.eval()
        with torch.no_grad():actual=float(model(**encode(pool.tok,texts,device),labels=torch.tensor(labels,device=device)).loss)
        check(architecture+' intervention equals actual update',abs(actual-trial['query_after'])<1e-7)
        new=pool.spawn();pool.train_step(new,texts,labels);pool.assert_memory_budget()
        check(architecture+' multi-package allocation budget',sum(s.memory.capacity for s in pool.states.values())<=32)
        if architecture=='head_only':
            check('head-only LoRA is zero and frozen',all(not p.requires_grad for n,p in model.named_parameters() if 'lora_' in n)
                and all(torch.count_nonzero(p)==0 for n,p in model.named_parameters() if 'lora_B' in n))
        else:
            before=snapshot(pool)
            component_trial(pool,new,texts,labels,texts,labels,'reuse_lora_inherit_head')
            check('BERT component cloning is non-invasive',nested_equal(before,snapshot(pool)))
    print('DAY16_BERT_INTEGRITY_PASS',args.device,flush=True)


if __name__=='__main__':main()
