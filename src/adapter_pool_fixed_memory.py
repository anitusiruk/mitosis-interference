"""Budgeted extension preserving probe size and reservoir sampling semantics."""
from src.adapter_pool_cau_v1 import CAUV1AdapterPool
from src.adapter_pool_head_only import HeadOnlyCAUV1AdapterPool


class FixedMemoryMixin:
    def __init__(self,*args,total_memory_budget=512,max_adapters=8,**kwargs):
        self.total_memory_budget=total_memory_budget
        self.max_adapters=max_adapters
        super().__init__(*args,**kwargs)
        if total_memory_budget//max_adapters<self.memory_probe:
            raise ValueError('Maximum pool would violate frozen probe size')
        self.rebudget()

    def rebudget(self):
        quota=self.total_memory_budget//len(self.states)
        if quota<self.memory_probe:raise RuntimeError('Fixed probe requirement violated')
        for state in self.states.values():
            memory=state.memory
            memory.capacity=quota
            if len(memory.items)>quota:memory.items=memory.rng.sample(memory.items,quota)
        self.assert_memory_budget()

    def assert_memory_budget(self):
        if len(self.states)>self.max_adapters:raise RuntimeError('Adapter budget violated')
        if sum(s.memory.capacity for s in self.states.values())>self.total_memory_budget:
            raise RuntimeError('Allocated reservoir slots exceed total budget')
        if sum(len(s.memory.items) for s in self.states.values())>self.total_memory_budget:
            raise RuntimeError('Actual reservoir storage exceeds total budget')
        if any(len(s.memory.items)>s.memory.capacity for s in self.states.values()):
            raise RuntimeError('An individual reservoir exceeds its quota')

    def spawn(self):
        if len(self.states)>=self.max_adapters:raise RuntimeError('Hard adapter cap reached')
        name=super().spawn()
        self.rebudget()
        return name

    def crossfit_action_utility(self,*args,**kwargs):
        result=super().crossfit_action_utility(*args,**kwargs)
        blocked=len(self.states)>=self.max_adapters
        result['budget_blocked_fresh']=blocked and bool(result.get('fresh_positive'))
        if blocked:result['fresh_positive']=False
        result['total_memory_budget']=self.total_memory_budget
        result['max_adapters']=self.max_adapters
        return result

    def restored_call(self,method,*args,**kwargs):
        # Legacy probes clear stale gradients, which the next real update would
        # discard anyway. This extension restores those tensors and flags too,
        # so stricter snapshots can verify the complete transaction contract.
        parameters=[(p,p.requires_grad,None if p.grad is None else p.grad.clone())
                    for p in self.model.parameters()]
        modes=[(m,m.training) for m in self.model.modules()]
        try:return method(*args,**kwargs)
        finally:
            for p,flag,gradient in parameters:
                p.requires_grad_(flag);p.grad=gradient
            for module,training in modes:module.train(training)

    def shadow_reuse(self,*args,**kwargs):
        return self.restored_call(super().shadow_reuse,*args,**kwargs)

    def shadow_fresh(self,*args,**kwargs):
        return self.restored_call(super().shadow_fresh,*args,**kwargs)

    def profile(self,*args,**kwargs):
        return self.restored_call(super().profile,*args,**kwargs)

    def _statusquo_query_loss(self,*args,**kwargs):
        return self.restored_call(super()._statusquo_query_loss,*args,**kwargs)

    def train_step(self,*args,**kwargs):
        loss=super().train_step(*args,**kwargs)
        self.assert_memory_budget()
        return loss


class FixedMemoryCAUV1AdapterPool(FixedMemoryMixin,CAUV1AdapterPool):pass
class FixedMemoryHeadOnlyCAUV1AdapterPool(FixedMemoryMixin,HeadOnlyCAUV1AdapterPool):pass
