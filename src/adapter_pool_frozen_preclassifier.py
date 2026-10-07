"""DistilBERT classifier-stack control with a frozen hidden pre-classifier."""
import torch
from src.adapter_pool_fixed_memory import FixedMemoryCAUV1AdapterPool, FixedMemoryHeadOnlyCAUV1AdapterPool


def assert_frozen_preclassifier(model):
    layer = model.base_model.model.pre_classifier
    originals = dict(layer.original_module.named_parameters())
    assert set(originals) == {'weight', 'bias'}
    for name, parameter in layer.named_parameters():
        assert not parameter.requires_grad
        assert torch.equal(parameter, originals[name.rsplit('.', 1)[-1]])
    return sum(p.numel() for n, p in model.named_parameters()
               if '.pre_classifier.modules_to_save.' in n)


class FrozenPreClassifierMixin:
    def freeze_preclassifier(self):
        for name, parameter in self.model.named_parameters():
            if '.pre_classifier.' in name:
                parameter.requires_grad_(False)

    def activate(self, name):
        super().activate(name)
        self.freeze_preclassifier()

    def _new_optimizer(self):
        self.freeze_preclassifier()
        return super()._new_optimizer()

    def train_step(self, *args, **kwargs):
        assert_frozen_preclassifier(self.model)
        result = super().train_step(*args, **kwargs)
        assert_frozen_preclassifier(self.model)
        return result


class FrozenPreClassifierCAUPool(FrozenPreClassifierMixin, FixedMemoryCAUV1AdapterPool):
    pass


class FrozenPreClassifierHeadOnlyPool(FrozenPreClassifierMixin, FixedMemoryHeadOnlyCAUV1AdapterPool):
    pass
