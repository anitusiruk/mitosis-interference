"""Predeclared Day-5 physically shared-head CAU sensitivity architecture.

This is an architecture extension, not a replacement for frozen private CAU-v1.
The loss lower-bound gate is a heuristic harm filter, not a safety guarantee.
"""
import copy
import math

import torch
import torch.nn.functional as F

from experiments.signal_scan import encode, trainable_params
from experiments.day2_predictor_scan_rngsafe import capture_rng_state, restore_rng_state
from src.adapter_pool_cau_v1 import CAUV1AdapterPool


class SharedHeadCAUV1AdapterPool(CAUV1AdapterPool):
    def __init__(self, *args, **kwargs):
        self.shared_optimizer = None
        self.probe_events = []
        self.fresh_fold_profiles = []
        super().__init__(*args, **kwargs)
        if any('modules_to_save' in name for name, _ in self.model.named_parameters()):
            raise ValueError('Shared-head model must not contain private modules_to_save')
        if len(self.head_parameters()) != 4:
            raise ValueError('Expected DistilBERT pre_classifier/classifier weights and biases')

    def head_parameters(self):
        return [p for name, p in self.model.named_parameters()
                if '.pre_classifier.' in name or '.classifier.' in name]

    def activate(self, name):
        super().activate(name)
        for p in self.head_parameters():
            p.requires_grad_(True)

    def _new_optimizer(self):
        for p in self.head_parameters():
            p.requires_grad_(True)
        params = trainable_params(self.model)
        if self.shared_optimizer is None:
            self.shared_optimizer = torch.optim.AdamW(params, lr=self.lr)
        else:
            registered = {id(p) for g in self.shared_optimizer.param_groups for p in g['params']}
            new = [p for p in params if id(p) not in registered]
            if new:
                self.shared_optimizer.add_param_group({'params': new})
        return self.shared_optimizer

    def _fresh_optimizer(self):
        # A real spawn uses the SAME head moments and new LoRA moments. The
        # temporary optimizer reproduces that without changing real groups.
        opt = torch.optim.AdamW(trainable_params(self.model), lr=self.lr)
        for p in self.head_parameters():
            if p in self.shared_optimizer.state:
                opt.state[p] = copy.deepcopy(self.shared_optimizer.state[p])
        return opt

    @staticmethod
    def _stats(delta, z):
        mean = float(delta.mean())
        se = float(delta.std(unbiased=True) / math.sqrt(delta.numel())) if delta.numel() > 1 else 0.0
        return {'harm': mean, 'harm_se': se, 'harm_lcb': mean-z*se,
                'harm_ucb': mean+z*se, 'n': int(delta.numel())}

    def intervention(self, name, support_texts, support_labels, query_texts,
                     query_labels, restore_name, fresh=False):
        """One optimizer-faithful trial; restore every real learner component."""
        rng = capture_rng_state()
        existing = [(p, p.requires_grad, None if p.grad is None else p.grad.detach().clone())
                    for p in self.model.parameters()]
        modes = [(m, m.training) for m in self.model.modules()]
        memory_rngs = {n: s.memory.rng.getstate() for n, s in self.states.items()}
        real_opt_state = copy.deepcopy(self.shared_optimizer.state_dict())
        temp = '__day5_shared_fresh__'
        params, backups, optimizer = [], [], None
        try:
            if fresh:
                if temp in self.model.peft_config:
                    raise RuntimeError('Temporary adapter exists before trial')
                self.model.add_adapter(temp, self.cfg)
                name = temp
            self.activate(name)
            params = trainable_params(self.model)
            backups = [p.detach().clone() for p in params]
            optimizer = self._fresh_optimizer() if fresh else self.shared_optimizer
            sx = encode(self.tok, support_texts, self.device)
            sy = torch.tensor(support_labels, dtype=torch.long, device=self.device)
            qx = encode(self.tok, query_texts, self.device)
            qy = torch.tensor(query_labels, dtype=torch.long, device=self.device)
            self.model.eval()
            with torch.no_grad():
                query_before = float(F.cross_entropy(self.model(**qx).logits, qy))
            protected = {}
            for old_name, state in self.states.items():
                if len(state.memory.items) < self.memory_probe:
                    continue
                texts, labels = state.memory.sample(self.memory_probe)
                x = encode(self.tok, texts, self.device)
                y = torch.tensor(labels, dtype=torch.long, device=self.device)
                self.activate(old_name)
                with torch.no_grad():
                    before = F.cross_entropy(self.model(**x).logits, y, reduction='none')
                protected[old_name] = (x, y, before)
            self.activate(name)
            self.model.train()
            optimizer.zero_grad(set_to_none=True)
            loss = self.model(**sx, labels=sy).loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            optimizer.step()
            self.model.eval()
            with torch.no_grad():
                query_after = float(F.cross_entropy(self.model(**qx).logits, qy))
            harms, all_delta = {}, []
            for old_name, (x, y, before) in protected.items():
                self.activate(old_name)
                with torch.no_grad():
                    delta = F.cross_entropy(self.model(**x).logits, y, reduction='none') - before
                harms[old_name] = self._stats(delta, self.confidence_z)
                all_delta.append(delta)
            summary = self._stats(torch.cat(all_delta), self.confidence_z) if all_delta else {
                'harm': 0.0, 'harm_se': 0.0, 'harm_lcb': 0.0, 'harm_ucb': 0.0, 'n': 0}
            # The gate protects EACH adapter, not just a pooled average.
            summary['harm_lcb'] = max((h['harm_lcb'] for h in harms.values()), default=0.0)
            summary['harm_ucb'] = max((h['harm_ucb'] for h in harms.values()), default=0.0)
            result = {**summary, 'query_before': query_before, 'query_after': query_after,
                      'query_gain': query_before-query_after, 'support_loss': float(loss.detach()),
                      'protected_profiles': harms,
                      'feasible_all': all(h['harm_lcb'] <= self.threshold for h in harms.values())}
            self.probe_events.append({'candidate': name, 'fresh': fresh, **result})
            return result
        finally:
            with torch.no_grad():
                for p, old in zip(params, backups):
                    p.copy_(old)
            self.shared_optimizer.load_state_dict(real_opt_state)
            if optimizer is not None:
                optimizer.zero_grad(set_to_none=True)
            if fresh and temp in self.model.peft_config:
                self.activate(restore_name)
                self.model.delete_adapter(temp)
            self.activate(restore_name)
            for p, requires_grad, grad in existing:
                p.requires_grad_(requires_grad)
                p.grad = grad
            for module, mode in modes:
                module.training = mode
            for n, state in self.states.items():
                state.memory.rng.setstate(memory_rngs[n])
            restore_rng_state(rng)

    def shadow_reuse(self, name, support_texts, support_labels, query_texts,
                     query_labels, restore_name):
        return self.intervention(name, support_texts, support_labels, query_texts,
                                 query_labels, restore_name)

    def shadow_fresh(self, support_texts, support_labels, query_texts,
                     query_labels, restore_name):
        result = self.intervention(None, support_texts, support_labels, query_texts,
                                   query_labels, restore_name, fresh=True)
        self.fresh_fold_profiles.append(result)
        return result

    def profile(self, name, texts, labels):
        # Caller supplies a current real name; all internal calls restore it.
        restore = self.model.active_adapter
        result = self.intervention(name, texts, labels, texts, labels, restore)
        return {**result, 'gain': result['query_gain'],
                'cur_before': result['query_before'], 'cur_after': result['query_after']}

    def crossfit_action_utility(self, texts, labels, restore_name):
        self.fresh_fold_profiles = []
        utility = super().crossfit_action_utility(texts, labels, restore_name)
        if utility.get('status') == 'ok':
            if len(self.fresh_fold_profiles) != 2:
                raise RuntimeError('Expected exactly two fresh fold trials')
            utility['fresh_positive_unconstrained'] = utility['fresh_positive']
            utility['fresh_feasible_both'] = all(x['feasible_all'] for x in self.fresh_fold_profiles)
            utility['fresh_protected_profiles'] = [x['protected_profiles'] for x in self.fresh_fold_profiles]
            utility['fresh_positive'] = bool(utility['fresh_positive'] and utility['fresh_feasible_both'])
        return utility

    def select_action(self, texts, labels, restore_name):
        pending_before = self.pending_fresh
        self.probe_events = []
        info = {'policy_version': 'day5_shared_head', 'pending_before': pending_before,
                'full_batch_guards': {}}
        if self.warmup_name is not None:
            warm = self.warmup_name
            if len(self.states[warm].memory.items) < self.memory_probe:
                self.pending_fresh = False
                full = self.profile(warm, texts, labels)
                permitted = full['feasible_all']
                self.activate(warm if permitted else restore_name)
                return (warm if permitted else None), {**info,
                    'decision': 'warmup' if permitted else 'defer',
                    'reason': 'guarded_shared_warmup' if permitted else 'shared_warmup_rejected',
                    'pending_after': False, 'utility_status': 'warmup',
                    'warmup_guard': full, 'shared_probes': self.probe_events}
            self.warmup_name = None
        utility = self.crossfit_action_utility(texts, labels, restore_name)
        info.update(utility=utility, utility_status=utility.get('status'))
        if utility.get('status') != 'ok':
            self.pending_fresh = False
            self.activate(restore_name)
            return None, {**info, 'decision': 'defer', 'reason': 'utility_unavailable',
                          'pending_after': False, 'shared_probes': self.probe_events}
        fresh_positive = bool(utility['fresh_positive'])
        fresh_rejected = False
        if pending_before and fresh_positive:
            full = self.intervention(None, texts, labels, texts, labels, restore_name, fresh=True)
            info['full_batch_fresh_guard'] = full
            if full['feasible_all']:
                new = self.spawn()
                self.pending_fresh = False
                return new, {**info, 'decision': 'spawn', 'reason': 'confirmed_guarded_fresh',
                             'pending_after': False, 'shared_probes': self.probe_events}
            fresh_rejected = True
        best, guards = self._full_batch_guarded_reuse(texts, labels, restore_name, utility)
        self.pending_fresh = bool(fresh_positive and not fresh_rejected)
        info.update(full_batch_guards=guards, guarded_best_reuse=best,
                    pending_after=self.pending_fresh, fresh_positive=fresh_positive,
                    fresh_full_batch_rejected=fresh_rejected, shared_probes=self.probe_events)
        if best is None:
            self.activate(restore_name)
            return None, {**info, 'decision': 'defer', 'reason': 'no_retention_feasible_reuse'}
        self.activate(best)
        return best, {**info, 'decision': 'reuse', 'reason': 'guarded_shared_reuse'}
