"""Independent read-only checks of saved real factorial intervention receipts.

Added as a quality-control check after the first observer outcomes. Does not
change experiments, contrast definitions, or inclusion criteria. Unverified
attempts are listed and never treated as valid causal observations.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

FACTORS = ('reset_lora_weights', 'reset_head_weights',
           'reset_lora_optimizer', 'reset_head_optimizer')
EMPTY_SHA = hashlib.sha256(b'').hexdigest()


def audit(folder, root):
    verification = json.loads((folder / 'observer_verification.json').read_text())
    assert verification['status'] == 'passed'
    assert verification['bitwise_learner_state_equal'] and verification['bitwise_adapter_tensors_equal']
    provenance = json.loads((folder / 'provenance.json').read_text())
    for name, expected in provenance['audit_implementation_sha256'].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
    route = pd.read_csv(folder / 'routing.csv')
    assert len(route) == 80 and list(route.step) == list(range(1, 81))
    assert json.loads((folder / 'summary.json').read_text())['status'] == 'completed'
    data = pd.read_csv(folder / 'component_trials.csv')
    # Frozen warmup behavior alone determines maturity; no effect-size filter.
    expected_steps = set(route.loc[route.decision != 'warmup', 'step'])
    assert set(data.step) == expected_steps, 'An eligible mature batch is missing or extra'
    sources = dict(zip(route.step, route.adapter.shift().fillna('default')))
    max_mean_error, max_decomposition_error = 0., 0.
    for step, batch in data.groupby('step'):
        assert len(batch) == 32
        assert set(batch.source_adapter) == {sources[step]}, 'Observer did not use the active source'
        for fold, part in batch.groupby('fold'):
            assert len(part) == 16 and set(map(tuple, part[list(FACTORS)].values)) == set(itertools.product([False, True], repeat=4))
            for kind in ['head', 'lora']:
                for reset, group in part.groupby('reset_' + kind + '_weights'):
                    assert group[kind + '_initial_weights_sha256'].nunique() == 1, 'Weight intervention leaked across factors'
                for reset, group in part.groupby('reset_' + kind + '_optimizer'):
                    assert group[kind + '_initial_optimizer_sha256'].nunique() == 1, 'State intervention leaked across factors'
                    counts = group[kind + '_inherited_state_parameters']
                    assert (counts == 0).all() if reset else (counts > 0).all()
                    if reset:
                        assert set(group[kind + '_initial_optimizer_sha256']) == {EMPTY_SHA}
            # Optimizer state may change learning, never the pre-update predictor.
            for _, same_weights in part.groupby(['reset_lora_weights', 'reset_head_weights']):
                arrays = [np.asarray(ast.literal_eval(x), dtype=float) for x in same_weights.query_before_each]
                assert all(np.array_equal(arrays[0], x) for x in arrays[1:]), 'Initial predictions depend on optimizer state'
        for _, cell in batch.groupby(list(FACTORS)):
            assert set(cell.fold) == {'A', 'B'} and len(cell) == 2
            indices = [i for x in cell.query_indices for i in ast.literal_eval(x)]
            assert sorted(indices) == list(range(int(cell.query_n.sum())))
        for row in batch.itertuples():
            before = np.asarray(ast.literal_eval(row.query_before_each), dtype=float)
            after = np.asarray(ast.literal_eval(row.query_after_each), dtype=float)
            assert len(before) == len(after) == row.query_n
            assert np.isfinite(before).all() and np.isfinite(after).all()
            error = max(abs(before.mean() - row.query_before), abs(after.mean() - row.query_after))
            max_mean_error = max(max_mean_error, error)
            assert error <= 1e-6
            assert abs(row.local_trainability - row.query_before + row.query_after) <= 1e-6
            error = max(abs(row.query_before - row.group_mass_loss_before - row.within_group_loss_before),
                        abs(row.query_after - row.group_mass_loss_after - row.within_group_loss_after))
            max_decomposition_error = max(max_decomposition_error, error)
            assert error <= 1e-5
            if provenance['args']['regime'] == 'amazon':
                assert row.group_mass_loss_before == row.group_mass_loss_after == 0.
            else:
                group = ast.literal_eval(row.label_group)
                concept = str(row.segment)[0]
                first = {'A': 0, 'B': 11, 'C': 22}[concept]
                assert group == list(range(first, first + 11))
    return {'run': folder.name, 'status': 'passed', 'mature_batches': len(expected_steps),
        'raw_cell_fold_rows': len(data), 'all_mature_batches_present': True,
        'actual_active_source_verified': True, 'weight_and_state_receipt_factor_independence': True,
        'initial_predictions_bitwise_invariant_to_optimizer_interventions': True,
        'each_example_queried_once_per_cell': True,
        'maximum_per_example_mean_error': max_mean_error,
        'maximum_label_mass_decomposition_error': max_decomposition_error,
        'component_trials_sha256': hashlib.sha256((folder / 'component_trials.csv').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    root = Path(args.root)
    rows, pending, failed = [], [], []
    for folder in sorted((root / 'results').glob('day15_*_weight_moments')):
        if not (folder / 'observer_verification.json').exists():
            pending.append(folder.name)
            continue
        try:
            rows.append(audit(folder, root))
        except Exception as error:
            failed.append({'run': folder.name, 'error': repr(error)})
    payload = {'utc': datetime.now(timezone.utc).isoformat(), 'scope': 'saved real observer receipt integrity',
        'check_added_after_first_observer_outcomes': True, 'training_outputs_modified': False,
        'passed': rows, 'pending_or_unverified': pending, 'failed': failed,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(args.output).write_text(json.dumps(payload, indent=2) + '\n')
    print('FACTORIAL_RECEIPT_INTEGRITY', len(rows), 'passed', len(pending), 'pending', len(failed), 'failed', flush=True)
    for row in rows:
        print(row['run'], row['mature_batches'], 'mature batches; all checks passed', flush=True)
    if failed:
        raise RuntimeError('Saved factorial receipt discrepancy: ' + repr(failed))


if __name__ == '__main__':
    main()

