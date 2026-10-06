"""Real PEFT/AdamW transaction tests using a tiny local DistilBERT model."""
import copy
import json

import torch
from transformers import DistilBertConfig, DistilBertForSequenceClassification
from peft import LoraConfig, TaskType, get_peft_model

from experiments.signal_scan import seed_all, encode
from experiments.day2_predictor_scan_rngsafe import capture_rng_state
from experiments.day3_action_utility_unit import nested_equal, snapshot_pool
from src.adapter_pool_shared_head import SharedHeadCAUV1AdapterPool


class Batch(dict):
    def to(self, device):
        return Batch({k: v.to(device) for k, v in self.items()})


class Tokenizer:
    def __call__(self, texts, **kwargs):
        ids = [[1]+[2+ord(c)%61 for c in t[:12]]+[2] for t in texts]
        size = max(map(len, ids))
        return Batch(input_ids=torch.tensor([r+[0]*(size-len(r)) for r in ids]),
                     attention_mask=torch.tensor([[1]*len(r)+[0]*(size-len(r)) for r in ids]))


def snapshot(pool):
    result = snapshot_pool(pool)
    result['parameters'] = [(n, p.requires_grad, None if p.grad is None else p.grad.clone())
                            for n, p in pool.model.named_parameters()]
    result['modes'] = [(n, m.training) for n, m in pool.model.named_modules()]
    result['pending_fresh'] = pool.pending_fresh
    return result


def check(name, value):
    print(name, 'PASS' if value else 'FAIL', flush=True)
    assert value, name


def main():
    seed_all(2026)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    base = DistilBertForSequenceClassification(DistilBertConfig(vocab_size=64, dim=32,
        hidden_dim=64, n_heads=4, n_layers=2, num_labels=3,
        dropout=0.1, attention_dropout=0.1, seq_classif_dropout=0.1))
    cfg = LoraConfig(task_type=TaskType.FEATURE_EXTRACTION, r=2, lora_alpha=4,
                     lora_dropout=0.0, target_modules=['q_lin', 'v_lin'], bias='none')
    model = get_peft_model(base, cfg).to(device)
    pool = SharedHeadCAUV1AdapterPool(model=model, tokenizer=Tokenizer(), lora_config=cfg,
        device=device, lr=2e-4, memory_size=16, memory_probe=4, threshold=0., seed=2026)
    texts, labels = ['good item', 'bad item', 'new item', 'old item'], [0,1,2,0]
    pool.train_step('default', texts, labels)
    pool.warmup_name = None
    check('one physical head stack, not private saved modules',
          len(pool.head_parameters()) == 4 and not any('modules_to_save' in n for n,_ in model.named_parameters()))
    check('shared head moments exist', all(p in pool.shared_optimizer.state for p in pool.head_parameters()))
    before = snapshot(pool)
    trial = pool.intervention('default', texts, labels, texts, labels, 'default')
    check('reuse restores params/opt/RNG/memory/gradients/trainability/modes', nested_equal(before, snapshot(pool)))
    before = snapshot(pool)
    fresh = pool.intervention(None, texts, labels, texts, labels, 'default', fresh=True)
    check('fresh restores full real state and registry', nested_equal(before, snapshot(pool)))
    check('fresh head intervention checks old default memory', 'default' in fresh['protected_profiles'])
    # Repeat the exact real update after the virtual trial: RNG and AdamW states
    # should make the post-update loss agree numerically.
    pool.train_step('default', texts, labels)
    pool.model.eval()
    with torch.no_grad():
        actual = float(pool.model(**encode(pool.tok,texts,device),
                       labels=torch.tensor(labels,device=device)).loss)
    check('virtual reuse equals exact subsequent real update', abs(actual-trial['query_after']) < 1e-7)
    new = pool.spawn()
    check('all adapter records share the same physical optimizer',
          all(s.optimizer is pool.shared_optimizer for s in pool.states.values()))
    ids = [id(p) for g in pool.shared_optimizer.param_groups for p in g['params']]
    check('optimizer parameters are unique', len(ids)==len(set(ids)))
    new_lora = [p for n,p in model.named_parameters() if f'.{new}.' in n and 'lora_' in n]
    check('real fresh LoRA has empty moments before first update', all(p not in pool.shared_optimizer.state for p in new_lora))
    pool.train_step(new, texts, labels)
    pool.warmup_name = None
    pool.activate('default')
    before = snapshot(pool)
    trial = pool.intervention(new, texts, labels, texts, labels, 'default')
    check('nonselected old adapter also protected', set(trial['protected_profiles'])=={'default',new})
    check('multi-adapter trial restores all shared state', nested_equal(before,snapshot(pool)))
    utility = pool.crossfit_action_utility(texts, labels, 'default')
    check('fresh feasibility requires both folds', utility.get('fresh_feasible_both') is not None)
    check('all crossfit probes restore full state', nested_equal(before,snapshot(pool)))
    # Fresh full-batch profile must equal the first real step after a real spawn.
    before = snapshot(pool)
    trial = pool.intervention(None,texts,labels,texts,labels,'default',fresh=True)
    check('new fresh probe is non-invasive',nested_equal(before,snapshot(pool)))
    next_name=pool.spawn()
    pool.train_step(next_name,texts,labels)
    pool.model.eval()
    with torch.no_grad():
        actual=float(pool.model(**encode(pool.tok,texts,device),labels=torch.tensor(labels,device=device)).loss)
    check('virtual fresh equals real spawn/update with inherited head moments',abs(actual-trial['query_after'])<1e-7)
    # The global-head architecture cannot inherit the private-package exemption.
    pool.warmup_name=next_name
    pool.states[next_name].memory.items=[]
    original_profile=pool.profile
    pool.profile=lambda *args: {'feasible_all':False,'protected_profiles':{'default':{'harm_lcb':1.}}}
    name,info=pool.select_action(texts,labels,next_name)
    check('post-spawn shared warmup rejects harm instead of unguarded training',name is None and info['decision']=='defer')
    pool.profile=original_profile
    print('DAY5_SHARED_HEAD_INTEGRITY_PASS',flush=True)


if __name__ == '__main__':
    main()
