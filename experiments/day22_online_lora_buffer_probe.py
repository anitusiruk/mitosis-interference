"""Read-only instrumentation of a pinned author's loop in a synthetic enclosure."""
import argparse
import ast
from collections import defaultdict, deque
import datetime
import hashlib
import importlib.util
import json
import logging
import math
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace

import numpy as np
import torch
from torch.nn import functional as functional

from experiments.day21_online_lora_reset_probe import TinyBackbone, source_classes


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author-root', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    root, output = Path(args.author_root), Path(args.output)
    output.mkdir(exist_ok=False)
    receipt = json.loads(Path('notes/day21_online_lora_author_source_receipt.json').read_text())
    assert receipt['commit'] == '59b9fd42ea9ca701cb36978709d5bc0e25938d81'
    for name in ['Disjoint/engine.py', 'Disjoint/utils.py', 'Disjoint/lora.py', 'Disjoint/datasets.py']:
        assert digest(root / name) == receipt['all_source_sha256'][name]['sha256']
    engine = root / 'Disjoint/engine.py'
    tree = ast.parse(engine.read_text())
    node = next(item for item in tree.body if isinstance(item, ast.FunctionDef) and item.name == 'train_and_evaluate')
    points = [item.lineno for item in ast.walk(node) if isinstance(item, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == 'batch' for target in item.targets)
              and isinstance(item.value, ast.List) and not item.value.elts]
    buffer_point = max(points)
    utility_spec = importlib.util.spec_from_file_location('pinned_author_logging_utils', root / 'Disjoint/utils.py')
    utility = importlib.util.module_from_spec(utility_spec)
    utility_spec.loader.exec_module(utility)
    wrapper = source_classes(root / 'Disjoint/lora.py')
    torch.set_num_threads(2)
    started, cases = time.monotonic(), []
    for batch_size in [1, 8, 64]:
        for seed in [17, 31, 47]:
            torch.manual_seed(seed)
            folder = output / f'batch{batch_size}_seed{seed}'
            folder.mkdir()
            model = wrapper(TinyBackbone(), r=2, num_classes=3)
            optimizer = torch.optim.Adam(model.parameters(), lr=.0002)
            incoming = [(torch.randn(batch_size, 3, 8), torch.arange(batch_size) % 3) for _ in range(12)]
            buffer_rows, importance_shapes = [], []

            def nll_loss(scores, targets, **kwargs):
                importance_shapes.append({'input_shape': list(scores.shape), 'target_shape': list(targets.shape)})
                return functional.nll_loss(scores, targets, **kwargs)

            def trace(frame, event, argument):
                if event == 'line' and frame.f_code.co_filename == str(engine) and frame.f_code.co_name == 'train_and_evaluate' and frame.f_lineno == buffer_point:
                    buffer = frame.f_locals['hard_buffer']
                    buffer_rows.append({'completed_update': len(buffer_rows) + 1, 'entries': len(buffer),
                        'entry_shapes': [list(item['state'].shape) for item in buffer],
                        'retained_examples': sum(item['state'].shape[0] for item in buffer),
                        'input_tensor_bytes': sum(item['state'].numel() * item['state'].element_size() for item in buffer)})
                return trace

            utilities = SimpleNamespace(MetricLogger=utility.MetricLogger, SmoothedValue=utility.SmoothedValue,
                                        init_ckpt_path=lambda **kwargs: str(folder / 'unused_checkpoint.pt'))
            namespace = {'torch': torch, 'np': np, 'math': math, 'logging': logging, 'os': os,
                'datetime': datetime, 'json': json, 'utils': utilities,
                'F': SimpleNamespace(log_softmax=functional.log_softmax, nll_loss=nll_loss),
                'Iterable': list, 'evaluate_till_now': lambda **kwargs: {}}
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(engine), 'exec'), namespace)
            settings = SimpleNamespace(num_tasks=1, nb_batch=1, epochs=1, hard_loss=True,
                regularization=True, MAS_weight=2000., loss_window_length=5,
                loss_window_mean_threshold=10., loss_window_variance_threshold=1e6,
                new_lora=False, hard_buffer_size=4, output_dir=str(folder))
            old_trace = sys.gettrace()
            try:
                sys.settrace(trace)
                namespace['train_and_evaluate'](model=model, criterion=torch.nn.CrossEntropyLoss(),
                    data_loader=[{'train': incoming, 'val': []}], optimizer=optimizer,
                    device=torch.device('cpu'), args=settings, class_mask=None)
            finally:
                sys.settrace(old_trace)
            assert len(buffer_rows) == 12
            assert buffer_rows[-1]['entries'] == 4 and buffer_rows[-1]['retained_examples'] == 4 * batch_size
            assert importance_shapes and all(row['input_shape'] == [1, 3 * batch_size] and row['target_shape'] == [1] for row in importance_shapes)
            assert all(torch.isfinite(parameter).all() for parameter in model.parameters())
            item = {'batch_size': batch_size, 'seed': seed, 'status': 'passed', 'buffer_updates': buffer_rows,
                    'importance_call_shapes': importance_shapes,
                    'final_retained_examples': buffer_rows[-1]['retained_examples'],
                    'maximum_retained_examples': max(row['retained_examples'] for row in buffer_rows)}
            (folder / 'case.json').write_text(json.dumps(item, indent=2) + '\n')
            cases.append(item)
    result = {'status': 'passed', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'author_commit': receipt['commit'], 'source_sha256': {name: digest(root / name) for name in ['Disjoint/engine.py', 'Disjoint/utils.py', 'Disjoint/lora.py', 'Disjoint/datasets.py']},
        'script_sha256': digest(Path(__file__)), 'spec_sha256': digest(Path('notes/day22_online_lora_buffer_probe_spec.md')),
        'device': 'cpu', 'torch_version': torch.__version__, 'seconds': time.monotonic() - started,
        'unchanged_ast_extracted_function': 'train_and_evaluate', 'unchanged_author_forward_classes': True,
        'synthetic_network_inputs_and_labels': True, 'benchmark_evaluation_replaced_by_no_metric_callback': True,
        'fixture_new_lora_ablation': False, 'fixture_mean_threshold': 10., 'fixture_variance_threshold': 1e6,
        'author_benchmark_configuration_claimed': False, 'full_method_reproduction_claimed': False,
        'benchmark_accuracy_claim_permitted': False, 'cases': cases,
        'full_batch64_rgb224_float32_input_buffer_bytes_extrapolated': 4 * 64 * 3 * 224 * 224 * 4}
    (output / 'buffer_probe.json').write_text(json.dumps(result, indent=2) + '\n')
    print('AUTHOR_LOOP_BUFFER_UNIT_CPU_CHECK', len(cases), 'cases', round(result['seconds'], 3), 'seconds', flush=True)


if __name__ == '__main__':
    main()
