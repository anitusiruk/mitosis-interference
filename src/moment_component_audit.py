"""Transactional 2^4 weight/state interventions; this is an audit, not a policy.

Fresh head means PEFT's original saved head initializer, not a new independent
draw. Inherited moments attached to reset weights are deliberate artificial
counterfactuals. They are not recommended optimizer states for deployment.
"""
import copy
import hashlib
import inspect
import itertools

import torch
import torch.nn.functional as F

from experiments.signal_scan import encode
from experiments.day2_predictor_scan_rngsafe import capture_rng_state, restore_rng_state
from src.component_intervention_audit import component_parameters


FACTORS = ('reset_lora_weights', 'reset_head_weights',
           'reset_lora_optimizer', 'reset_head_optimizer')
CELLS = tuple(dict(zip(FACTORS, values)) for values in itertools.product((False, True), repeat=4))


def tensor_digest(values):
    """Small receipt for exactly which weights/state each cell received."""
    digest = hashlib.sha256()
    for name, value in sorted(values.items()):
        digest.update(name.encode())
        if torch.is_tensor(value):
            tensor = value.detach().cpu().contiguous()
            digest.update(str((tensor.dtype, tuple(tensor.shape))).encode())
            digest.update(tensor.numpy().tobytes())
        else:
            digest.update(repr(value).encode())
    return digest.hexdigest()


def moment_trial(pool, source, support_texts, support_labels, query_texts,
                 query_labels, cell, label_group=None):
    if set(cell) != set(FACTORS) or any(type(v) is not bool for v in cell.values()):
        raise ValueError('A cell must specify all four Boolean interventions')
    if not support_texts or not query_texts:
        raise ValueError('Nonempty support and query are required')
    if len(support_texts) != len(support_labels) or len(query_texts) != len(query_labels):
        raise ValueError('Text/label lengths differ')
    active = pool.model.active_adapter
    rng = capture_rng_state()
    existing = [(p, p.requires_grad, None if p.grad is None else p.grad.detach().clone())
                for p in pool.model.parameters()]
    modes = [(m, m.training) for m in pool.model.modules()]
    source_params = component_parameters(pool.model, source)
    if {kind for kind, _ in source_params.values()} != {'head', 'lora'}:
        raise RuntimeError('Audit requires a private classifier and LoRA package')
    inherited_optimizer = pool.states[source].optimizer
    if type(inherited_optimizer) is not torch.optim.AdamW:
        raise RuntimeError('This audit is defined for ordinary torch AdamW')
    if len(inherited_optimizer.param_groups) != 1:
        raise RuntimeError('Multiple optimizer groups need an explicit matched port')
    temp, optimizer = '__weight_moment_audit__', None
    if temp in pool.model.peft_config:
        raise RuntimeError('A temporary audit adapter already exists')
    try:
        pool.model.add_adapter(temp, pool.cfg)
        pool.activate(temp)
        targets = component_parameters(pool.model, temp)
        if set(targets) != set(source_params):
            raise RuntimeError('Source and candidate parameter structures differ')
        for key, (kind, target) in targets.items():
            if kind != source_params[key][0]:
                raise RuntimeError('Component kind changed')
            old = source_params[key][1]
            if target.shape != old.shape or target.dtype != old.dtype:
                raise RuntimeError('Source/candidate component shape or dtype differs')
            if not cell[f'reset_{kind}_weights']:
                with torch.no_grad():
                    target.copy_(source_params[key][1])
        params = [p for _, p in targets.values()]
        if {id(p) for p in params} != {id(p) for p in pool.model.parameters() if p.requires_grad}:
            raise RuntimeError('Unexpected trainable parameters outside the private package')
        initial = {k: p.detach().clone() for k, (_, p) in targets.items()}
        accepted = set(inspect.signature(torch.optim.AdamW).parameters) - {'params'}
        # Read the actual group (which may differ from constructor defaults).
        group = copy.deepcopy({k: v for k, v in inherited_optimizer.param_groups[0].items() if k != 'params'})
        extra = set(group) - accepted
        if extra - {'decoupled_weight_decay', 'initial_lr'} or group.get('decoupled_weight_decay', True) is not True:
            raise RuntimeError(f'Unsupported AdamW group fields: {extra}')
        optimizer = torch.optim.AdamW(params, **{k: v for k, v in group.items() if k in accepted})
        copied = {'head': 0, 'lora': 0}
        for key, (kind, target) in targets.items():
            old = source_params[key][1]
            if not cell[f'reset_{kind}_optimizer'] and old in inherited_optimizer.state:
                for field in ['exp_avg','exp_avg_sq','max_exp_avg_sq']:
                    value = inherited_optimizer.state[old].get(field)
                    if value is not None and value.shape != target.shape:
                        raise RuntimeError('Transported moment shape differs: ' + key + ':' + field)
                optimizer.state[target] = copy.deepcopy(inherited_optimizer.state[old])
                copied[kind] += 1
        receipts = {}
        for kind in ['head', 'lora']:
            receipts[kind + '_initial_weights_sha256'] = tensor_digest(
                {k: initial[k] for k, (which, _) in targets.items() if which == kind})
            receipts[kind + '_initial_optimizer_sha256'] = tensor_digest(
                {k + ':' + field: value for k, (which, p) in targets.items() if which == kind
                 for field, value in optimizer.state.get(p, {}).items()})
            receipts[kind + '_inherited_state_parameters'] = copied[kind]
        # Every cell receives the same initialization and support dropout draw.
        # All initialization and training randomness is restored on exit.
        restore_rng_state(rng)
        sx, qx = encode(pool.tok, support_texts, pool.device), encode(pool.tok, query_texts, pool.device)
        sy = torch.tensor(support_labels, device=pool.device)
        qy = torch.tensor(query_labels, device=pool.device)
        pool.model.eval()
        with torch.no_grad():
            before_logits = pool.model(**qx).logits
            before = F.cross_entropy(before_logits, qy, reduction='none')
            before_mean = F.cross_entropy(before_logits, qy)
            group = list(range(before_logits.shape[-1])) if label_group is None else list(label_group)
            if len(set(group)) != len(group) or not set(query_labels + support_labels) <= set(group):
                raise ValueError('Audit label group must uniquely include every batch label')
            if not group or min(group) < 0 or max(group) >= before_logits.shape[-1]:
                raise ValueError('Audit label group lies outside the full output space')
            before_mass = before_logits.logsumexp(-1) - before_logits[:, group].logsumexp(-1)
            before_conditional = before - before_mass
        pool.model.train()
        optimizer.zero_grad(set_to_none=True)
        support_loss = pool.model(**sx, labels=sy).loss
        support_loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        optimizer.step()
        pool.model.eval()
        with torch.no_grad():
            after_logits = pool.model(**qx).logits
            after = F.cross_entropy(after_logits, qy, reduction='none')
            after_mean = F.cross_entropy(after_logits, qy)
            after_mass = after_logits.logsumexp(-1) - after_logits[:, group].logsumexp(-1)
            after_conditional = after - after_mass
        if not torch.isfinite(before).all() or not torch.isfinite(after).all() or not torch.isfinite(support_loss):
            raise RuntimeError('Nonfinite intervention loss')
        return {**cell, **receipts, 'query_before': float(before_mean),
                'query_after': float(after_mean), 'local_trainability': float(before_mean - after_mean),
                'label_group': group, 'group_mass_loss_before': float(before_mass.mean()),
                'group_mass_loss_after': float(after_mass.mean()),
                'within_group_loss_before': float(before_conditional.mean()),
                'within_group_loss_after': float(after_conditional.mean()),
                'query_before_each': before.cpu().tolist(), 'query_after_each': after.cpu().tolist(),
                'support_loss': float(support_loss.detach()), 'support_n': len(support_texts),
                'query_n': len(query_texts), **{kind + '_update_l2': sum(float((p.detach() - initial[k]).square().sum())
                    for k, (which, p) in targets.items() if which == kind) ** .5 for kind in ['head', 'lora']}}
    finally:
        if optimizer is not None:
            optimizer.zero_grad(set_to_none=True)
        if temp in pool.model.peft_config:
            pool.activate(active)
            pool.model.delete_adapter(temp)
        pool.activate(active)
        for parameter, requires_grad, grad in existing:
            parameter.requires_grad_(requires_grad)
            parameter.grad = grad
        for module, training in modes:
            module.training = training
        restore_rng_state(rng)


def crossfit_moments(pool, texts, labels, source, cells=CELLS, label_group=None):
    """Each example is queried once in each cell, including odd-sized batches."""
    if len(texts) < 2:
        return []
    if len(texts) != len(labels):
        raise ValueError('Text/label lengths differ')
    rows = []
    for fold, support, query in [('A', list(range(0, len(texts), 2)), list(range(1, len(texts), 2))),
                                 ('B', list(range(1, len(texts), 2)), list(range(0, len(texts), 2)))]:
        for cell in cells:
            result = moment_trial(pool, source, [texts[i] for i in support], [labels[i] for i in support],
                                  [texts[i] for i in query], [labels[i] for i in query], cell, label_group=label_group)
            rows.append({'source_adapter': source, 'fold': fold, 'query_indices': query, **result})
    return rows
