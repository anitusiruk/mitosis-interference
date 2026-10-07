"""Analytic gate: pilot-only tie-breaking, complete grids and seed pairing."""
import os
from pathlib import Path
import tempfile

import pandas as pd

from experiments.day17_static_tuning_report import RATES, select_pilot_rates


def main():
    rows = []
    for rank in [8, 96]:
        for rate in RATES:
            for order in ['canonical', 'b_first']:
                good = (rank == 8 and rate in [1e-4, 2e-4]) or (rank == 96 and rate == 5e-5)
                rows.append({'rank': rank, 'learning_rate': rate, 'order': order, 'seed': 2026,
                             'updates': 80, 'final_macro_accuracy': .7 if good else .2})
    pilots = pd.DataFrame(rows)
    selected, grid = select_pilot_rates(pilots)
    assert selected == {'8': 1e-4, '96': 5e-5} and len(grid) == 12
    for bad in [pilots.iloc[:-1], pd.concat([pilots.iloc[:-1], pilots.iloc[:1]], ignore_index=True)]:
        try:
            select_pilot_rates(bad)
        except RuntimeError:
            pass
        else:
            raise AssertionError('An incomplete or duplicate grid was accepted')
    # Known paired differences and unpaired-order exclusion through the real report.
    import json
    from experiments.day17_static_tuning_report import main as report
    previous = Path.cwd()
    try:
        with tempfile.TemporaryDirectory(prefix='day17_analytic_') as directory:
            os.chdir(directory)
            Path('results').mkdir(); Path('notes').mkdir()
            Path('notes/day17_static_rate_selection.json').write_text(json.dumps({
                'selected_rates': selected, 'grid_summary': grid}))
            for seed in range(2027, 2032):
                for order in ['canonical', 'b_first']:
                    reference = Path(f'results/day8_banking_private_cau_seed{seed}_{order}_fixed512')
                    reference.mkdir()
                    resources = {'lora_parameters': 10, 'private_head_parameters': 20,
                                 'optimizer_state_bytes': 100, 'replay_items': 512,
                                 'gpu_peak_allocated_bytes': 1000}
                    summary = {'status': 'completed', 'steps': 80, 'learning_updates': 80,
                               'resources': resources, 'timing': {'live_training_seconds': 1, 'evaluation_seconds': 2}}
                    provenance = {'stream_sha256': f'paired:{seed}:{order}', 'args': {'seed': seed, 'order': order}}
                    (reference/'summary.json').write_text(json.dumps(summary))
                    (reference/'provenance.json').write_text(json.dumps(provenance))
                    original = [{'step': 80, 'concept': concept, 'rule': rule, 'accuracy': .6}
                                for concept in ['A', 'B', 'C']
                                for rule in ['last_active', 'uniform_probability', 'frozen_centroid']]
                    learned = [{'concept': concept, 'rule': rule, 'accuracy': .6}
                               for concept in ['A', 'B', 'C']
                               for rule in ['linear_hard', 'linear_probability_mixture']]
                    pd.DataFrame(original).to_csv(reference/'label_free_eval.csv', index=False)
                    pd.DataFrame(learned).to_csv(reference/'learned_routing.csv', index=False)
                    for rank in [8, 96]:
                        if rank == 96 and seed == 2031 and order == 'b_first':
                            continue
                        folder = Path(f'results/day17_confirm_rank{rank}_lr{int(selected[str(rank)]*1e6)}_seed{seed}_{order}')
                        folder.mkdir()
                        p = dict(provenance, lora_rank=rank, learning_rate=selected[str(rank)])
                        (folder/'provenance.json').write_text(json.dumps(p))
                        (folder/'summary.json').write_text(json.dumps(summary))
                        f = pd.DataFrame([{'step':80, 'rule':'last_active', 'concept':c, 'accuracy':.5}
                                          for c in ['A','B','C']])
                        f.to_csv(folder/'label_free_eval.csv', index=False)
            report()
            intervals = pd.read_csv('results/day17_tuned_static_paired_differences.csv')
            assert len(intervals) == 10
            assert set(intervals[intervals['rank']==8].seed_clusters) == {5}
            assert set(intervals[intervals['rank']==96].seed_clusters) == {4}
            assert abs(intervals['mean'] - .1).max() < 1e-12
            assert abs(intervals.ci_low - .1).max() < 1e-12
            assert abs(intervals.ci_high - .1).max() < 1e-12
    finally:
        os.chdir(previous)
    print('STATIC_REPORT_ANALYTIC_GATE_PASS pilot-only ties, missing grids, paired-seed exclusion', flush=True)


if __name__ == '__main__':
    main()
