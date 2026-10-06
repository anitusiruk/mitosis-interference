"""Observational factorial attribution on a frozen private-package trajectory."""
import copy
import inspect

import torch
import torch.nn.functional as F

from experiments.signal_scan import encode, trainable_params
from experiments.day2_predictor_scan_rngsafe import capture_rng_state, restore_rng_state


VARIANTS = {
    'reuse_lora_inherit_head': (False, False, False, False),
    'reuse_lora_fresh_head': (False, True, False, False),
    'fresh_lora_inherit_head': (True, False, False, False),
    'fresh_lora_fresh_head': (True, True, False, False),
    'reuse_lora_inherit_head_reset_optimizer': (False, False, True, False),
    'reuse_lora_common_frozen_head': (False, False, False, True),
    'fresh_lora_common_frozen_head': (True, False, False, True),
}


def component_parameters(model, adapter):
    result = {}
    for name, p in model.named_parameters():
        if f'.{adapter}.' not in name:
            continue
        if 'lora_' in name:
            kind = 'lora'
        elif '.modules_to_save.' in name and ('classifier' in name):
            kind = 'head'
        else:
            continue
        key = name.replace(f'.{adapter}.', '.__adapter__.')
        result[key] = (kind, p)
    return result


def component_trial(pool, source, support_texts, support_labels, query_texts,
                    query_labels, variant):
    fresh_lora, fresh_head, reset_optimizer, freeze_head = VARIANTS[variant]
    restore = pool.model.active_adapter
    rng = capture_rng_state()
    existing = [(p,p.requires_grad,None if p.grad is None else p.grad.detach().clone())
                for p in pool.model.parameters()]
    modes = [(m,m.training) for m in pool.model.modules()]
    source_params = component_parameters(pool.model, source)
    opt_source = pool.states[source].optimizer
    temp = '__day5_component__'
    opt = None
    try:
        if temp in pool.model.peft_config:
            raise RuntimeError('Temporary component adapter already exists')
        pool.model.add_adapter(temp, pool.cfg)
        pool.activate(temp)
        targets = component_parameters(pool.model, temp)
        if set(targets) != set(source_params):
            raise RuntimeError('Candidate/source parameter structures differ')
        for key, (kind, target) in targets.items():
            old_kind, old = source_params[key]
            assert kind == old_kind
            inherited = not (fresh_lora if kind == 'lora' else fresh_head)
            if inherited:
                with torch.no_grad():
                    target.copy_(old)
            if kind == 'head' and freeze_head:
                target.requires_grad_(False)
        params = trainable_params(pool.model)
        initial = {k:p.detach().clone() for k,(_,p) in targets.items()}
        accepted = set(inspect.signature(torch.optim.AdamW).parameters) - {'params'}
        defaults = copy.deepcopy(opt_source.defaults)
        extra = set(defaults) - accepted
        if extra - {'decoupled_weight_decay'} or defaults.get('decoupled_weight_decay', True) is not True:
            raise RuntimeError(f'Unsupported AdamW defaults: {extra}')
        opt = torch.optim.AdamW(params, **{k:v for k,v in defaults.items() if k in accepted})
        for key, (kind, target) in targets.items():
            inherited = not (fresh_lora if kind == 'lora' else fresh_head)
            old = source_params[key][1]
            if inherited and not reset_optimizer and target.requires_grad and old in opt_source.state:
                opt.state[target] = copy.deepcopy(opt_source.state[old])
        # Equal dropout randomness across the 2x2 cells. Counterfactual initialization
        # is restored afterward and never changes the frozen real trajectory.
        restore_rng_state(rng)
        sx = encode(pool.tok, support_texts, pool.device)
        sy = torch.tensor(support_labels,device=pool.device)
        qx = encode(pool.tok, query_texts, pool.device)
        qy = torch.tensor(query_labels,device=pool.device)
        pool.model.eval()
        with torch.no_grad():
            before = float(F.cross_entropy(pool.model(**qx).logits,qy))
        pool.model.train()
        opt.zero_grad(set_to_none=True)
        loss=pool.model(**sx,labels=sy).loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params,1.0)
        opt.step()
        pool.model.eval()
        with torch.no_grad():
            after=float(F.cross_entropy(pool.model(**qx).logits,qy))
        changes = {kind:sum(float((p.detach()-initial[k]).square().sum())
                   for k,(which,p) in targets.items() if which==kind)**0.5
                   for kind in ['head','lora']}
        return {'variant':variant, 'query_before':before, 'query_after':after,
                'local_trainability':before-after, 'support_loss':float(loss.detach()),
                'head_update_l2':changes['head'],'lora_update_l2':changes['lora'],
                'support_n':len(support_texts),'query_n':len(query_texts)}
    finally:
        if opt is not None:
            opt.zero_grad(set_to_none=True)
        if temp in pool.model.peft_config:
            pool.activate(restore)
            pool.model.delete_adapter(temp)
        pool.activate(restore)
        for p, req, grad in existing:
            p.requires_grad_(req)
            p.grad=grad
        for m, training in modes:
            m.training=training
        restore_rng_state(rng)


def crossfit_components(pool, texts, labels, source):
    if len(texts) < 2:
        return []
    records=[]
    for fold, support, query in [('A',range(0,len(texts),2),range(1,len(texts),2)),
                                  ('B',range(1,len(texts),2),range(0,len(texts),2))]:
        for variant in VARIANTS:
            result=component_trial(pool,source,[texts[i] for i in support],[labels[i] for i in support],
                                   [texts[i] for i in query],[labels[i] for i in query],variant)
            records.append({'source_adapter':source,'fold':fold,**result})
    return records
