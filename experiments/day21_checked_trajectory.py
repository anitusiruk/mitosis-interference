"""Run the frozen trainer with a before-training saved-stream identity gate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

from huggingface_hub import HfApi
from experiments import day8_fixed_memory_recurrence as trainer
from experiments import day15_weight_moment_recurrence as observer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--deadline-utc', required=True)
    parser.add_argument('--factorial', action='store_true')
    args = parser.parse_args()
    reference = Path('results/day8_banking_private_cau_seed2029_b_first_fixed512')
    old = json.loads((reference / 'provenance.json').read_text())
    revision = json.loads(Path('notes/restart_20261006_preflight.json').read_text())['backbone_revision']
    assert old['model_revision'] == revision
    os.environ['MITOSIS_MODEL_REVISION'] = revision
    dataset_revision = HfApi().dataset_info('PolyAI/banking77').sha
    assert dataset_revision
    load_dataset = trainer.load_dataset

    def pinned_dataset(name, *positional, **keywords):
        assert name == 'PolyAI/banking77'
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
                   'stream_check_before_any_training_update': True,
                   'dataset_revision_recovered_at_restore': True,
                   'historical_full_dataset_revision_not_recorded': True}
        (Path(args.output) / 'restore_stream_identity.json').write_text(json.dumps(receipt, indent=2) + '\n')
        assert receipt['status'] == 'passed', 'Restored stream differs from saved reference'
        print('RESTORED_STREAM_IDENTITY_PASS', digest, dataset_revision, flush=True)
        return result, boundaries

    trainer.load_dataset = pinned_dataset
    trainer.reorder_stream = checked_stream
    common = ['--regime', 'banking', '--seed', '2029', '--order', 'b_first',
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
