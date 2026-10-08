"""Report every declared NLI pilot; select only after the entire grid completes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.day22_bounded_nli_pilot_v3 import RATES, pilot_name
from experiments.day5_report import markdown_table


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    observations, pending, failed, initial_hashes, sources = [], [], [], [], {}
    for rate in RATES:
        for order in ['canonical', 'b_first']:
            name = pilot_name(rate, order)
            folder = Path('results') / name
            receipt_path = Path('notes/' + name + '_execution.json')
            if not receipt_path.exists() or not (folder / 'summary.json').exists():
                pending.append(name)
                continue
            receipt, summary = [json.loads(path.read_text()) for path in [receipt_path, folder / 'summary.json']]
            if receipt['status'] != 'completed' or receipt['returncode'] != 0 or summary['status'] != 'completed':
                failed.append(name)
                continue
            assert summary['steps'] == summary['learning_updates'] == summary['expected_steps'] == 360
            assert summary['training_examples'] == 5760 and summary['adapters'] == ['default']
            provenance = json.loads((folder / 'provenance.json').read_text())
            assert provenance['actual_max_length'] == 256 and provenance['pair_tokenization_smoke_passed']
            assert provenance['training_seed'] == 2026 and provenance['rehearsal_updates'] == 0
            assert provenance['args']['learning_rate'] == rate and provenance['args']['order'] == order
            assert provenance['data_manifest']['dataset_payload_sha256'] == sha(Path('results/day22_multinli_pilot_data_v2/dataset.json.gz'))
            metrics = pd.read_csv(folder / 'eval_matrix.csv')
            assert len(metrics) == 18 and metrics.step.nunique() == 6
            assert sorted(metrics.step.unique()) == [0, 72, 144, 216, 288, 360]
            assert set(metrics.concept) == {'A', 'B', 'C'} and set(metrics.n) == {192}
            assert np.isfinite(metrics[['loss', 'accuracy', 'class_0_accuracy', 'class_1_accuracy', 'class_2_accuracy']]).all().all()
            assert np.allclose(metrics.accuracy, metrics[['class_0_accuracy', 'class_1_accuracy', 'class_2_accuracy']].mean(axis=1), atol=1e-12, rtol=0)
            for row in metrics.to_dict('records'):
                observations.append({'run': name, 'rate': rate, 'order': order, **row})
            predictions = [json.loads(line) for line in (folder / 'development_predictions.jsonl').read_text().splitlines()]
            assert len(predictions) == 6 * 576
            initial = [row for row in predictions if row['step'] == 0]
            assert len(initial) == 576
            initial_hashes.append(hashlib.sha256(json.dumps(initial, sort_keys=True).encode()).hexdigest())
            # Independently recompute every metric from all saved three-class logits.
            for step in [0, 72, 144, 216, 288, 360]:
                for concept in ['A', 'B', 'C']:
                    rows = [row for row in predictions if row['step'] == step and row['concept'] == concept]
                    assert len(rows) == len({row['source'] for row in rows}) == 192
                    labels = np.asarray([row['label'] for row in rows])
                    scores = np.asarray([row['logits'] for row in rows], dtype=float)
                    assert scores.shape == (192, 3) and np.isfinite(scores).all()
                    shifted = scores - scores.max(axis=1, keepdims=True)
                    losses = np.log(np.exp(shifted).sum(axis=1)) - shifted[np.arange(192), labels]
                    expected = metrics[(metrics.step == step) & (metrics.concept == concept)].iloc[0]
                    assert abs(float(losses.mean()) - expected.loss) <= 1e-6
                    correct = scores.argmax(axis=1) == labels
                    assert abs(float(correct.mean()) - expected.accuracy) <= 1e-12
                    for label in range(3):
                        assert int((labels == label).sum()) == 64
                        assert abs(float(correct[labels == label].mean()) - expected[f'class_{label}_accuracy']) <= 1e-12
            sources[name] = {'summary_sha256': sha(folder / 'summary.json'), 'metrics_sha256': sha(folder / 'eval_matrix.csv'),
                             'predictions_sha256': sha(folder / 'development_predictions.jsonl'), 'execution_sha256': sha(receipt_path)}
    assert not initial_hashes or len(set(initial_hashes)) == 1, 'Pilot candidates did not start with the same predictor'
    frame = pd.DataFrame(observations)
    if observations:
        frame.to_csv('results/day22_multinli_pilot_metrics.csv', index=False)
    complete = len(sources) == 6 and not pending and not failed
    rate_rows, selected = [], None
    if complete:
        for rate in RATES:
            part = frame[frame.rate == rate]
            final, initial = part[part.step == 360], part[part.step == 0]
            assert len(final) == len(initial) == 6
            by_genre = final.groupby('concept').accuracy.mean().to_dict()
            row = {'rate': rate, 'orders': 2, 'pilot_training_seeds': 1,
                   'final_macro_accuracy': float(final.accuracy.mean()),
                   'untrained_macro_accuracy': float(initial.accuracy.mean()),
                   'learning_gain': float(final.accuracy.mean() - initial.accuracy.mean()),
                   'A_accuracy': by_genre['A'], 'B_accuracy': by_genre['B'], 'C_accuracy': by_genre['C']}
            row['learnability_gate_passed'] = row['final_macro_accuracy'] >= .50 and row['learning_gain'] >= .10 and min(by_genre.values()) >= .40
            rate_rows.append(row)
        best = max(row['final_macro_accuracy'] for row in rate_rows)
        selected = min([row for row in rate_rows if abs(row['final_macro_accuracy'] - best) <= 1e-12], key=lambda row: row['rate'])
        pd.DataFrame(rate_rows).to_csv('results/day22_multinli_pilot_rate_selection.csv', index=False)
    payload = {'utc': datetime.now(timezone.utc).isoformat(), 'scope': 'one-seed repeatedly viewed development learnability pilot',
               'complete_candidates': len(sources), 'planned_candidates': 6, 'all_candidates_complete': complete,
               'pending': pending, 'failed': failed, 'rate_rows': rate_rows, 'selected': selected,
               'all_initial_per_example_logits_equal': bool(initial_hashes) and len(set(initial_hashes)) == 1,
               'all_completed_saved_logit_metrics_independently_recomputed': True,
               'confirmation_authorized_by_report': False, 'official_validation_or_test_evaluated': False,
               'no_training_outputs_modified': True, 'sources': sources, 'reporter_sha256': sha(Path(__file__))}
    Path('notes/day22_multinli_pilot_report.json').write_text(json.dumps(payload, indent=2) + '\n')
    text = '# Longer-context fixed-package NLI development pilot\n\n'
    text += f'Completed candidates: {len(sources)}/6. Pending: {pending}. Failed: {failed}.\n\n'
    if rate_rows:
        text += markdown_table(pd.DataFrame(rate_rows)) + '\n\n'
        text += f"Selected rate: {selected['rate']:g}; operational learnability gate passed: {selected['learnability_gate_passed']}.\n\n"
    text += ('All candidates use seed 2026 and the same 5760 fit examples and 576 development examples, '
             'with both orders paired before rate selection. These examples and this seed are development material. '
             'Orders, checkpoints and examples are not independent training replicates; no pilot significance interval is reported. '
             'The fixed learning-rate grid and thresholds were declared before pilot learning outcomes. '
             'A passing single learner would establish learnability of this development recipe, not an allocation benefit, '
             'a new mechanism or comparative superiority. A failed gate is retained without expanding the grid. '
             'Source-level preparation failures and amendments remain preserved. A separate fresh-seed comparison specification '
             'and complete published-method reproduction are still needed.\n')
    Path('notes/day22_multinli_pilot_results.md').write_text(text)
    print('NLI_PILOT_REPORT', len(sources), 'of 6', 'selected', selected, flush=True)


if __name__ == '__main__':
    main()
