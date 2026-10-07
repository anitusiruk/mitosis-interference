"""Within-DistilBERT pre-classifier freeze using the unmodified frozen trainer."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import pandas as pd
import torch
from experiments import day8_fixed_memory_recurrence as trainer
from src.adapter_pool_frozen_preclassifier import (
    FrozenPreClassifierCAUPool, FrozenPreClassifierHeadOnlyPool)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--architecture', choices=['private', 'head_only'], required=True)
    parser.add_argument('--preclassifier-mode', choices=['frozen', 'inherited'], default='frozen')
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--order', choices=['canonical', 'b_first'], required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--deadline-utc', required=True)
    args = parser.parse_args()
    if args.preclassifier_mode == 'frozen':
        trainer.FixedMemoryCAUV1AdapterPool = FrozenPreClassifierCAUPool
        trainer.FixedMemoryHeadOnlyCAUV1AdapterPool = FrozenPreClassifierHeadOnlyPool
    sys.argv = ['day8_fixed_memory_recurrence', '--regime', 'banking', '--architecture', args.architecture,
        '--policy', 'cau', '--seed', str(args.seed), '--order', args.order,
        '--output', args.output, '--deadline-utc', args.deadline_utc]
    trainer.main()
    folder = Path(args.output)
    provenance = json.loads((folder/'provenance.json').read_text())
    provenance.update(preclassifier_mode=args.preclassifier_mode,
        diagnostic_spec_sha256=hashlib.sha256(Path('notes/day19_linear_classifier_spec.md').read_bytes()).hexdigest(),
        wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        freeze_implementation_sha256=hashlib.sha256(Path('src/adapter_pool_frozen_preclassifier.py').read_bytes()).hexdigest(),
        override_scope='pre-classifier trainability and its optimizer inclusion only')
    (folder/'provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')
    summary = json.loads((folder/'summary.json').read_text())
    route = pd.read_csv(folder/'routing.csv')
    assert summary['status'] == 'completed' and len(route) == 80
    assert route.replay_items.max() <= 512 and route.num_adapters.max() <= 8
    reference = Path(f'results/day8_banking_{args.architecture}_cau_seed{args.seed}_{args.order}_fixed512')
    rp = json.loads((reference/'provenance.json').read_text())
    assert provenance['stream_sha256'] == rp['stream_sha256']
    state = torch.load(folder/'checkpoint/learner_state.pt', map_location='cpu', weights_only=False)
    if args.preclassifier_mode == 'frozen':
        originals = {name.rsplit('.', 1)[-1]: value for name, value in state['heads'].items()
                     if '.pre_classifier.original_module.' in name}
        assert set(originals) == {'weight', 'bias'}
        for name, value in state['heads'].items():
            if '.pre_classifier.' in name:
                assert torch.equal(value, originals[name.rsplit('.', 1)[-1]])
        # Dormant PEFT copies remain stored; count them explicitly, not as trained capacity.
        summary['resources']['frozen_private_preclassifier_parameters'] = sum(
            value.numel() for name, value in state['heads'].items()
            if '.pre_classifier.modules_to_save.' in name)
        summary['resources']['stored_output_classifier_parameters'] = sum(
            value.numel() for name, value in state['heads'].items()
            if '.classifier.modules_to_save.' in name)
        (folder/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    else:
        from experiments.day15_weight_moment_recurrence import verify_replay
        receipt = verify_replay(folder, reference)
        (folder/'reference_replay_verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
        print('LINEAR_CONTROL_UNCHANGED_WRAPPER_BITWISE_REPLAY_PASS', flush=True)
    print('LINEAR_CLASSIFIER_CONTROL_TRAJECTORY_PASS', args.preclassifier_mode, args.architecture, args.seed, args.order, flush=True)


if __name__ == '__main__':
    main()
