import torch
from transformers import DistilBertConfig,DistilBertForSequenceClassification
from peft import LoraConfig,TaskType,get_peft_model

from experiments.signal_scan import seed_all,encode
from experiments.day5_shared_head_integrity import Tokenizer,check
from src.adapter_pool_head_only import HeadOnlyCAUV1AdapterPool


def main():
    seed_all(2026)
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    base=DistilBertForSequenceClassification(DistilBertConfig(vocab_size=64,dim=32,
        hidden_dim=64,n_heads=4,n_layers=2,num_labels=3))
    cfg=LoraConfig(task_type=TaskType.SEQ_CLS,r=2,lora_alpha=4,target_modules=['q_lin','v_lin'],bias='none')
    model=get_peft_model(base,cfg).to(device)
    pool=HeadOnlyCAUV1AdapterPool(model=model,tokenizer=Tokenizer(),lora_config=cfg,
        device=device,memory_probe=4,memory_size=16,seed=2026)
    texts,labels=['good item','bad item','new item','old item'],[0,1,2,0]
    before={n:p.detach().clone() for n,p in model.named_parameters() if 'lora_' in n}
    for _ in range(3):pool.train_step('default',texts,labels)
    check('all real LoRA tensors unchanged',all(torch.equal(before[n],p) for n,p in model.named_parameters() if n in before))
    check('all real LoRA B outputs exactly zero',all(torch.count_nonzero(p)==0 for n,p in model.named_parameters() if 'lora_B' in n))
    new=pool.spawn()
    for name in list(pool.states):
        pool.activate(name)
        check(name+' activation cannot unfreeze LoRA',all(not p.requires_grad for n,p in model.named_parameters() if 'lora_' in n))
    pool.train_step(new,texts,labels)
    for state in pool.states.values():
        registered={id(p) for g in state.optimizer.param_groups for p in g['params']}
        check(state.name+' optimizer contains no LoRA',all(id(p) not in registered for n,p in model.named_parameters() if 'lora_' in n))
    print('DAY5_HEAD_ONLY_INTEGRITY_PASS',flush=True)


if __name__=='__main__':main()
