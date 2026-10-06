"""Head-only negative control with identically zero-output LoRA branches."""
import torch

from experiments.signal_scan import trainable_params
from src.adapter_pool_cau_v1 import CAUV1AdapterPool


class HeadOnlyCAUV1AdapterPool(CAUV1AdapterPool):
    def freeze_lora(self):
        for name,p in self.model.named_parameters():
            if 'lora_' in name:
                p.requires_grad_(False)
            if 'lora_B' in name and torch.count_nonzero(p).item()!=0:
                raise RuntimeError('Head-only control has a nonzero LoRA output branch')

    def activate(self,name):
        super().activate(name)
        self.freeze_lora()

    def _new_optimizer(self):
        self.freeze_lora()
        return torch.optim.AdamW(trainable_params(self.model),lr=self.lr)
