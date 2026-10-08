"""Run an original remaining trajectory with pinned data and exact replay gates."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

from experiments import day8_fixed_memory_recurrence as trainer
from experiments import day15_weight_moment_recurrence as observer
from experiments import domain_recurrence_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--deadline-utc', required=True)
    parser.add_argument('--factorial', action='store_true')
    parser.add_argument('--regime', choices=['banking', 'amazon'], required=True)
    parser.add_argument('--seed', type=int, choices=[2030, 2031], required=True)
    parser.add_argument('--order', choices=['canonical', 'b_first'], required=True)
    args = parser.parse_args()
    reference = Path(f'results/day8_{args.regime}_private_cau_seed{args.seed}_{args.order}_fixed512')
    old = json.loads((reference / 'provenance.json').read_text())
    revision = json.loads(Path('notes/restart_20261006_preflight.json').read_text())['backbone_revision']
    assert old['model_revision'] == revision
    os.environ['MITOSIS_MODEL_REVISION'] = revision
    prior_pin = Path(f'results/day21_{args.regime}_private_cau_seed2029_b_first_replay/restore_stream_identity.json')
    pin = json.loads(prior_pin.read_text())
    assert pin['status'] == 'passed' and pin['model_revision'] == revision
    dataset_revision = pin['dataset_revision']
    dataset_name = 'PolyAI/banking77' if args.regime == 'banking' else 'goosmanlei/amazon_reviews_multi'
    load_dataset = trainer.load_dataset if args.regime == 'banking' else domain_recurrence_data.load_dataset

    def pinned_dataset(name, *positional, **keywords):
        assert name == dataset_name
        assert 'revision' not in keywords or keywords['revision'] == dataset_revision
        keywords['revision'] = dataset_revision
        return load_dataset(name, *positional, **keywords)

    reorder = trainer.reorder_stream

    def checked_stream(stream, order):
        result, boundaries = reorder(stream, order)
        digest = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        receipt = {'status': 'passed' if digest == old['stream_sha256'] else 'failed',
                   'reference': str(reference), 'stream_sha256': digest,
                   'expected_stream_sha256': old['stream_sha256'],
                   'model_revision': revision, 'dataset_revision': dataset_revision,
                   'recovered_dataset_pin_receipt': str(prior_pin),
                   'stream_check_before_any_training_update': True,
                   'historical_full_dataset_revision_not_recorded': True}
        (Path(args.output) / 'restore_stream_identity.json').write_text(json.dumps(receipt, indent=2) + '\n')
        assert receipt['status'] == 'passed', 'Restored stream differs from saved reference'
        print('RESTORED_STREAM_IDENTITY_PASS', digest, dataset_revision, flush=True)
        return result, boundaries

    if args.regime == 'banking':
        trainer.load_dataset = pinned_dataset
    else:
        domain_recurrence_data.load_dataset = pinned_dataset
    trainer.reorder_stream = checked_stream
    common = ['--regime', args.regime, '--seed', str(args.seed), '--order', args.order,
              '--output', args.output, '--deadline-utc', args.deadline_utc]
    if args.factorial:
        sys.argv = ['day15_weight_moment_recurrence', *common]
        observer.main()
    else:
        sys.argv = ['day8_fixed_memory_recurrence', '--architecture', 'private', '--policy', 'cau', *common]
        trainer.main()
        assert json.loads((Path(args.output) / 'summary.json').read_text())['status'] == 'completed'
        receipt = observer.verify_replay(Path(args.output), reference)
        (Path(args.output) / 'observer_verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print('RESTORED_BASELINE_BITWISE_REPLAY_PASS', flush=True)


if __name__ == '__main__':
    main()
