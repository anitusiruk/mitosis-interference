"""Four-factor observational audit on a verified fixed-memory trajectory.

Reuse the frozen trainer unchanged. The observer replaces only its optional
component measurements and must reproduce the unaudited reference state.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import torch
from safetensors.torch import load_file

from experiments import day8_fixed_memory_recurrence as trainer
from experiments.day3_action_utility_unit import nested_equal
from src.moment_component_audit import crossfit_moments


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_replay(output, reference):
    old = json.loads((reference / 'provenance.json').read_text())
    new = json.loads((output / 'provenance.json').read_text())
    if new['stream_sha256'] != old['stream_sha256']:
        raise RuntimeError('Unpaired observer/reference data streams')
    left, right = [pd.read_csv(p / 'routing.csv') for p in [reference, output]]
    if len(left) != len(right) or len(right) != 80:
        raise RuntimeError('Incomplete observer or reference trajectory')
    columns = ['step', 'adapter', 'decision', 'train_executed', 'num_adapters', 'replay_items']
    if not left[columns].equals(right[columns]):
        raise RuntimeError('Observer changed the real action or memory trajectory')
    if not np.allclose(left.loss, right.loss, atol=1e-6, rtol=0, equal_nan=True):
        raise RuntimeError('Observer changed real training loss')
    a, b = [torch.load(p / 'checkpoint/learner_state.pt', map_location='cpu', weights_only=False)
            for p in [reference, output]]
    if not nested_equal(a, b):
        raise RuntimeError('Observer final learner state is not bitwise identical')
    paths = sorted((reference / 'checkpoint/adapters').rglob('*.safetensors'))
    if not paths:
        raise RuntimeError('Reference has no saved adapter tensors')
    for path in paths:
        other = output / path.relative_to(reference)
        if not other.exists() or not nested_equal(load_file(str(path)), load_file(str(other))):
            raise RuntimeError('Observer changed saved adapter weights: ' + str(path))
    return {'status': 'passed', 'reference': str(reference), 'reference_learner_sha256':
            sha(reference / 'checkpoint/learner_state.pt'), 'output_learner_sha256':
            sha(output / 'checkpoint/learner_state.pt'), 'bitwise_learner_state_equal': True,
            'bitwise_adapter_tensors_equal': True, 'adapter_files_checked': len(paths),
            'training_loss_absolute_tolerance': 1e-6,
            'maximum_training_loss_difference': float(np.nanmax(np.abs(left.loss - right.loss))),
            'stream_sha256': new['stream_sha256']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--regime', choices=['banking', 'amazon'], required=True)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--order', choices=['canonical', 'b_first'], required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--deadline-utc', required=True)
    args = parser.parse_args()
    reference = Path(f'results/day8_{args.regime}_private_cau_seed{args.seed}_{args.order}_fixed512')
    if json.loads((reference / 'summary.json').read_text())['status'] != 'completed':
        raise RuntimeError('A complete unaudited reference is required')
    spec = Path('notes/day15_weight_moment_spec.md')
    implementation = ['src/moment_component_audit.py', 'experiments/day15_weight_moment_recurrence.py',
                      'experiments/day8_fixed_memory_recurrence.py']
    receipt = {'audit_spec_sha256': sha(spec), 'audit_implementation_sha256': {p: sha(p) for p in implementation},
               'audit_kind': 'observational_four_factor_weight_optimizer_state', 'reference': str(reference),
               'all_mature_batches': True, 'official_test_used': False}
    print('DAY15_FROZEN_OBSERVER', json.dumps(receipt, sort_keys=True), flush=True)
    def observer(pool, texts, labels, source):
        # Evaluator-only label grouping decomposes already computed losses.
        # It is never supplied to allocation, training, or deployment routing.
        if args.regime == 'banking':
            index = labels[0] // 11
            group = list(range(11*index, 11*(index+1)))
        else:
            group = [0, 1]
        return crossfit_moments(pool, texts, labels, source, label_group=group)
    trainer.crossfit_components = observer
    sys.argv = ['day8_fixed_memory_recurrence', '--regime', args.regime, '--architecture', 'private',
                '--policy', 'cau', '--seed', str(args.seed), '--order', args.order, '--component-audit',
                '--output', args.output, '--deadline-utc', args.deadline_utc]
    trainer.main()
    output = Path(args.output)
    provenance = json.loads((output / 'provenance.json').read_text())
    provenance.update(receipt)
    (output / 'provenance.json').write_text(json.dumps(provenance, indent=2))
    if json.loads((output / 'summary.json').read_text())['status'] != 'completed':
        raise RuntimeError('Incomplete audit preserved; no replay/causal claim permitted')
    # Failed checks leave every measurement and attempt intact for inspection.
    verification = verify_replay(output, reference)
    (output / 'observer_verification.json').write_text(json.dumps(verification, indent=2))
    print('DAY15_OBSERVER_REPLAY_PASS', args.regime, args.seed, args.order, flush=True)


if __name__ == '__main__':
    main()
