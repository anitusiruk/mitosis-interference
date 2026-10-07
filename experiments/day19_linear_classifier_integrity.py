"""Tiny real PEFT/AdamW gates for frozen pre-classifier behavior."""
import argparse
import torch
from transformers import DistilBertConfig, DistilBertForSequenceClassification
from peft import LoraConfig, TaskType, get_peft_model
from experiments.signal_scan import seed_all, encode
from experiments.day3_action_utility_unit import nested_equal
from experiments.day5_shared_head_integrity import Tokenizer, snapshot, check
from src.adapter_pool_frozen_preclassifier import (
    FrozenPreClassifierCAUPool, FrozenPreClassifierHeadOnlyPool, assert_frozen_preclassifier)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', choices=['cpu', 'cuda'], required=True)
    args = parser.parse_args()
    device = torch.device(args.device)
    torch.set_num_threads(2)
    for architecture, kind in [('private', FrozenPreClassifierCAUPool), ('head_only', FrozenPreClassifierHeadOnlyPool)]:
        seed_all(2032)
        base = DistilBertForSequenceClassification(DistilBertConfig(vocab_size=64,dim=32,
            hidden_dim=64,n_heads=4,n_layers=2,num_labels=3,dropout=.1,attention_dropout=.1,seq_classif_dropout=.1))
        cfg = LoraConfig(task_type=TaskType.SEQ_CLS,r=2,lora_alpha=4,lora_dropout=0.,
                         target_modules=['q_lin','v_lin'],bias='none')
        model = get_peft_model(base,cfg).to(device)
        pool = kind(model=model,tokenizer=Tokenizer(),lora_config=cfg,device=device,lr=2e-4,
            memory_size=32,total_memory_budget=32,memory_probe=4,max_adapters=8,threshold=0.,seed=2032)
        texts,labels=['good item','bad item','new item','old item'],[0,1,2,0]
        for _ in range(3):pool.train_step('default',texts,labels)
        pool.warmup_name=None
        assert_frozen_preclassifier(model)
        allowed = [n for n,p in model.named_parameters() if p.requires_grad]
        check(architecture+' only declared parameters trainable',all('.classifier.modules_to_save.' in n or
              architecture=='private' and 'lora_' in n for n in allowed))
        check(architecture+' exactly one linear output classifier',sum('.classifier.modules_to_save.' in n for n in allowed)==2)
        before=snapshot(pool)
        pool.crossfit_action_utility(texts,labels,'default')
        check(architecture+' crossfit exact restoration',nested_equal(before,snapshot(pool)))
        trial=pool.shadow_reuse('default',texts,labels,texts,labels,'default')
        check(architecture+' inherited shadow exact restoration',nested_equal(before,snapshot(pool)))
        pool.train_step('default',texts,labels);model.eval()
        with torch.no_grad():actual=float(model(**encode(pool.tok,texts,device),labels=torch.tensor(labels,device=device)).loss)
        check(architecture+' inherited intervention equals real update',abs(actual-trial['query_after'])<1e-7)
        new=pool.spawn();pool.train_step(new,texts,labels);assert_frozen_preclassifier(model)
        pool.assert_memory_budget()
        check(architecture+' spawned preclassifier matches original',True)
        if architecture=='head_only':
            check('linear-head-only LoRA remains zero and frozen',all(not p.requires_grad for n,p in model.named_parameters() if 'lora_' in n)
                  and all(torch.count_nonzero(p)==0 for n,p in model.named_parameters() if 'lora_B' in n))
            check('linear-head-only optimizer has two parameters',all(len(s.optimizer.param_groups[0]['params'])==2 for s in pool.states.values()))
    print('LINEAR_CLASSIFIER_INTEGRITY_PASS',args.device,flush=True)


if __name__=='__main__':main()
