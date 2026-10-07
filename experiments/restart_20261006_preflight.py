"""Verify restored data streams and old predictions before new outcomes."""
from datetime import datetime, timezone
import gc
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import load_dataset

from experiments.controller_recurrence_cau_v1 import make_dev_split, make_recurrence_stream
from experiments.domain_recurrence_data import build_domain_recurrence
from experiments.day8_fixed_memory_recurrence import reorder_stream
from experiments.day5_causal_recurrence import evaluate_label_free
from experiments.day9_learned_routing import evaluation_sets, load_checkpoint


def main():
    pin = json.loads(Path('notes/restart_backbone_pin.json').read_text())
    revision = pin['revision']
    assert len(revision) == 40 and all(c in '0123456789abcdef' for c in revision)
    os.environ['MITOSIS_MODEL_REVISION'] = revision
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    os.environ['OMP_NUM_THREADS'] = '8'
    torch.set_num_threads(8)
    jobs = json.loads(Path('notes/remaining_frozen_jobs.json').read_text())
    assert len(jobs) == 45
    train, _ = make_dev_split(load_dataset('PolyAI/banking77', split='train', trust_remote_code=True))
    stream_checks = []
    streams = {}
    for job in jobs:
        key = (job['regime'], job['seed'], job['order'])
        if key not in streams:
            if job['regime'] == 'banking':
                stream, _ = make_recurrence_stream(train, 16, job['seed'])
            else:
                stream, _, _ = build_domain_recurrence(job['seed'], batch_size=16)
            stream, _ = reorder_stream(stream, job['order'])
            streams[key] = hashlib.sha256(json.dumps(stream, sort_keys=True).encode()).hexdigest()
        reference = Path('results') / (
            f"day6_{job['regime']}_private_cau_seed{job['seed']}_{job['order']}"
        ) / 'provenance.json'
        expected = json.loads(reference.read_text())['stream_sha256']
        assert streams[key] == expected, (job['name'], streams[key], expected)
        stream_checks.append({'run': job['name'], 'stream_sha256': expected, 'matches_saved_reference': True})
    print('FROZEN_STREAM_HASHES_PASS', len(stream_checks), flush=True)
    reload_checks = []
    sets = {}
    for folder in sorted(Path('results').glob('day8_*_fixed512')):
        summary = json.loads((folder / 'summary.json').read_text())
        assert summary['status'] == 'completed', folder
        provenance = json.loads((folder / 'provenance.json').read_text())
        regime = provenance['args']['regime']
        if regime not in sets:
            sets[regime] = evaluation_sets(regime)
        pool, last_name, _ = load_checkpoint(folder)
        old = pd.read_csv(folder / 'label_free_eval.csv')
        old = old[old.step == old.step.max()]
        repeated = pd.DataFrame(evaluate_label_free(pool, sets[regime], last_name))
        joined = old[['concept', 'rule', 'n', 'accuracy', 'loss']].merge(
            repeated[['concept', 'rule', 'n', 'accuracy', 'loss']],
            on=['concept', 'rule'], suffixes=('_stored', '_reloaded'), validate='one_to_one')
        assert len(joined) == 9 and (joined.n_stored == joined.n_reloaded).all(), folder
        assert np.allclose(joined.accuracy_stored, joined.accuracy_reloaded, atol=1e-12, rtol=0), folder
        loss_delta = float(np.max(np.abs(joined.loss_stored - joined.loss_reloaded)))
        if not np.allclose(joined.loss_stored, joined.loss_reloaded, atol=1e-5, rtol=0):
            joined.to_csv('notes/restart_checkpoint_reload_mismatch.csv', index=False)
            raise RuntimeError(f'Preserved checkpoint loss mismatch: {folder}; max difference {loss_delta}')
        reload_checks.append({'run': folder.name, 'aggregate_counts_and_accuracies_equal': True,
                              'maximum_absolute_loss_difference': loss_delta})
        print('PINNED_RELOAD_PASS', folder.name, loss_delta, flush=True)
        del pool
        gc.collect()
        torch.cuda.empty_cache()
    assert len(reload_checks) == 12, len(reload_checks)
    receipt = {'verified_utc': datetime.now(timezone.utc).isoformat(), 'backbone_revision': revision,
               'historical_revision_field_was_null': True,
               'historical_exact_backbone_identity_proven': False,
               'validation_scope': 'nine aggregate counts, accuracies and losses per restored Day8 checkpoint; per-example predictions were not saved',
               'loss_absolute_tolerance': 1e-5, 'loss_relative_tolerance': 0,
               'stream_checks': stream_checks, 'checkpoint_reload_checks': reload_checks,
               'official_test_used': False, 'status': 'passed'}
    Path('notes/restart_20261006_preflight.json').write_text(json.dumps(receipt, indent=2))
    print('RESTART_PREFLIGHT_PASS', flush=True)


if __name__ == '__main__':
    main()
