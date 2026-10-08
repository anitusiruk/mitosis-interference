"""Small CPU probe of unchanged author Q/V forward and reset methods.

The enclosing network and data are synthetic. This is not a timm/ViT benchmark
reproduction and does not measure the published method's accuracy.
"""
import argparse
import ast
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import time

import torch
from torch import nn, Tensor
from torch.nn.parameter import Parameter


class TinyBackbone(nn.Module):
    def __init__(self):
        super().__init__()
        block = nn.Module()
        block.attn = nn.Module()
        block.attn.qkv = nn.Linear(8, 24)
        self.blocks = nn.ModuleList([block])
        self.head = nn.Linear(8, 3)

    def reset_classifier(self, num_classes):
        self.head = nn.Linear(8, num_classes)

    def forward(self, inputs):
        qkv = self.blocks[0].attn.qkv(inputs)
        return self.head((qkv[:, :, :8] + qkv[:, :, -8:]).mean(1))


def norm(tensors):
    return float(sum(x.detach().double().square().sum() for x in tensors).sqrt())


def source_classes(path):
    tree = ast.parse(path.read_text())
    wanted = ['_LoRA_qkv_timm', 'LoRA_ViT_timm']
    nodes = [x for x in tree.body if isinstance(x, ast.ClassDef) and x.name in wanted]
    assert [x.name for x in nodes] == wanted
    namespace = {'torch': torch, 'nn': nn, 'Tensor': Tensor, 'Parameter': Parameter,
                 'math': math, 'timm_ViT': nn.Module}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace['LoRA_ViT_timm']


def new_factors(model):
    return [x.weight for x in model.wnew_As + model.wnew_Bs]


def new_residual(model, inputs):
    q = model.lora_vit.blocks[0].attn.qkv
    return torch.cat([q.linear_new_b_q(q.linear_new_a_q(inputs)),
                      q.linear_new_b_v(q.linear_new_a_v(inputs))], dim=-1)


def run_probe(wrapper, seed, dtype):
    torch.manual_seed(seed)
    model = wrapper(TinyBackbone(), r=2, num_classes=3)
    optimizer = torch.optim.Adam(model.parameters(), lr=.0002)
    inputs = torch.randn(7, 3, 8)
    labels = torch.tensor([0, 1, 2, 0, 1, 2, 1])

    def train(m, opt):
        opt.zero_grad()
        loss = nn.functional.cross_entropy(m(inputs), labels)
        loss.backward()
        assert torch.isfinite(loss)
        opt.step()

    for _ in range(8):
        train(model, optimizer)
    before_first = model.lora_vit.blocks[0].attn.qkv(inputs).detach().clone()
    model.update_and_reset_lora_parameters()
    after_first = model.lora_vit.blocks[0].attn.qkv(inputs).detach().clone()
    tolerance = 1e-6 if dtype == torch.float32 else 1e-12
    assert torch.allclose(before_first, after_first, atol=tolerance, rtol=0)
    assert norm(new_factors(model)) == 0
    models = {kind: copy.deepcopy(model) for kind in ['inherited_adam', 'fresh_adam']}
    assert all(torch.equal(models['inherited_adam'].state_dict()[k], v)
               for k, v in models['fresh_adam'].state_dict().items())
    states = copy.deepcopy(optimizer.state_dict())
    arms = {}
    optimizers = {}
    for kind, m in models.items():
        opt = torch.optim.Adam(m.parameters(), lr=.0002)
        if kind == 'inherited_adam':
            opt.load_state_dict(copy.deepcopy(states))
        optimizers[kind] = opt
        opt.zero_grad()
        nn.functional.cross_entropy(m(inputs), labels).backward()
        gradient_norm = norm([p.grad for p in new_factors(m) if p.grad is not None])
        assert gradient_norm == 0
        count = sum(p in opt.state for p in new_factors(m))
        opt.step()
        arms[kind] = {'initial_new_factor_gradient_norm': gradient_norm,
                      'inherited_state_parameter_count': count,
                      'new_factor_norm_after_step': norm(new_factors(m)),
                      'new_residual_norm_after_step': norm([new_residual(m, inputs)])}
    assert arms['fresh_adam']['new_factor_norm_after_step'] == 0
    assert arms['inherited_adam']['new_factor_norm_after_step'] > 0
    assert arms['inherited_adam']['new_residual_norm_after_step'] > 0

    # Check a second consolidation with the same source path; retain full terms.
    m, opt = models['inherited_adam'], optimizers['inherited_adam']
    for _ in range(3):
        train(m, opt)
    q = m.lora_vit.blocks[0].attn.qkv
    before = q(inputs).detach().clone()
    cross_q = q.linear_b_q(q.linear_new_a_q(inputs)) + q.linear_new_b_q(q.linear_a_q(inputs))
    cross_v = q.linear_b_v(q.linear_new_a_v(inputs)) + q.linear_new_b_v(q.linear_a_v(inputs))
    predicted = torch.zeros_like(before)
    predicted[:, :, :8] = cross_q
    predicted[:, :, -8:] = cross_v
    m.update_and_reset_lora_parameters()
    delta = q(inputs).detach() - before
    assert torch.allclose(delta, predicted, atol=tolerance, rtol=0)
    assert norm([predicted]) > 0
    return {'seed': seed, 'dtype': str(dtype), 'arms': arms,
            'first_consolidation_qkv_max_difference': float((after_first-before_first).abs().max()),
            'second_consolidation_qkv_change_norm': norm([delta]),
            'second_consolidation_cross_term_norm': norm([predicted]),
            'second_consolidation_identity_max_error': float((delta-predicted).abs().max()),
            'equality_tolerance': tolerance}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author-root', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    receipt = json.loads(Path('notes/day21_online_lora_author_source_receipt.json').read_text())
    source = Path(args.author_root) / 'Disjoint/lora.py'
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == receipt['all_source_sha256']['Disjoint/lora.py']['sha256']
    assert receipt['commit'] == '59b9fd42ea9ca701cb36978709d5bc0e25938d81'
    wrapper = source_classes(source)
    started = time.monotonic()
    torch.set_num_threads(2)
    original_dtype = torch.get_default_dtype()
    rows = []
    try:
        for dtype in [torch.float32, torch.float64]:
            torch.set_default_dtype(dtype)
            for seed in [17, 31, 47, 61, 79]:
                rows.append(run_probe(wrapper, seed, dtype))
    finally:
        torch.set_default_dtype(original_dtype)
    result = {'status': 'passed', 'utc': datetime.now(timezone.utc).isoformat(),
              'author_commit': receipt['commit'], 'author_lora_source_sha256': digest,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'torch_version': torch.__version__, 'device': 'cpu',
              'synthetic_network_and_inputs': True, 'unchanged_author_forward_reset_construction': True,
              'ast_extracted_classes': ['_LoRA_qkv_timm', 'LoRA_ViT_timm'],
              'published_training_loop_executed': False, 'full_method_reproduced': False,
              'accuracy_claim_permitted': False, 'seeds_are_toy_checks_not_benchmark_replicates': True,
              'seconds': time.monotonic()-started, 'checks': rows}
    (out / 'reset_probe.json').write_text(json.dumps(result, indent=2) + '\n')
    print('AUTHOR_RESET_CPU_PROBE_PASS', len(rows), 'seed/dtype checks', flush=True)


if __name__ == '__main__':
    main()
