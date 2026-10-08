"""Refresh derived evidence after the two bounded original cells complete.

No training, new contrast, test access or outcome-selected inclusion occurs here.
Keep the current manuscript and old derived outputs before replacing tables.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pandas as pd
import numpy as np
from experiments.day5_report import markdown_table

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b13105d211c013120784e79c38e3e77849e4ccbf'


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    import os
    os.chdir(ROOT)
    for prefix in ['day21_', 'day21_amazon_']:
        receipt = json.loads(Path('notes/' + prefix + 'audit_execution.json').read_text())
        assert receipt['status'] == 'completed' and receipt['returncode'] == 0
        assert receipt['seconds'] < 1500
    scientific = ['src/moment_component_audit.py', 'experiments/day8_fixed_memory_recurrence.py',
                  'experiments/day15_weight_moment_recurrence.py', 'notes/day15_weight_moment_spec.md']
    for name in scientific:
        assert subprocess.check_output(['git', 'show', BASE + ':' + name]) == Path(name).read_bytes()
    # Additional post-outcome QC of saved aggregates, not a new replication or
    # a claim that historical per-example evaluation hashes were recorded.
    development_checks = []
    for regime in ['banking', 'amazon']:
        reference = Path(f'results/day8_{regime}_private_cau_seed2029_b_first_fixed512')
        outputs = [Path(f'results/day21_{regime}_private_cau_seed2029_b_first_replay'),
                   Path(f'results/day15_{regime}_private_cau_seed2029_b_first_weight_moments')]
        for output in outputs:
            for filename in ['eval_matrix.csv', 'label_free_eval.csv']:
                left, right = [pd.read_csv(p / filename) for p in [reference, output]]
                assert list(left.columns) == list(right.columns) and left.shape == right.shape
                assert left.checkpoint.nunique() == right.checkpoint.nunique() == 5
                errors = {}
                for column in left:
                    if column in {'loss', 'concept_prob_mass', 'concept_logit_margin'}:
                        a, b = left[column].to_numpy(), right[column].to_numpy()
                        assert np.isfinite(a).all() and np.isfinite(b).all()
                        errors[column] = float(np.max(np.abs(a-b)))
                        assert np.allclose(a, b, atol=1e-6, rtol=0), (str(output), filename, column)
                    else:
                        assert left[column].equals(right[column]), (str(output), filename, column)
                development_checks.append({'reference': str(reference), 'output': str(output),
                    'filename': filename, 'rows_checked': len(left), 'checkpoints_checked': 5,
                    'non_loss_metadata_and_accuracies_exactly_equal': True,
                    'continuous_loss_metric_absolute_tolerance': 1e-6, 'maximum_metric_errors': errors,
                    'reference_sha256': sha(reference / filename), 'output_sha256': sha(output / filename)})
    write(Path('notes/day21_development_replay_integrity.json'), {
        'utc': datetime.now(timezone.utc).isoformat(), 'status': 'passed',
        'scope': 'all saved segment-end aggregate development metrics',
        'historical_per_example_evaluation_hash_available': False,
        'per_example_identity_not_claimed': True, 'check_added_after_observer_outcomes': True,
        'training_outputs_modified': False, 'checks': development_checks})
    draft = Path('notes/paper_working_draft.md')
    original = draft.read_text()
    assert draft.read_bytes() == subprocess.check_output(['git', 'show', BASE + ':' + str(draft)])
    assert '## Within-backbone output-classifier control' in original
    assert original.count('10/20 verified trajectories') == 1
    archive = Path('notes/day21_before_bounded_refresh')
    archive.mkdir(exist_ok=False)
    preserved = [draft, Path('notes/day15_weight_moment_results.md'), Path('notes/research_progress.md')]
    preserved += sorted(Path('results').glob('day15_*.csv'))
    preserved += sorted(p for p in Path('figures/extended_audit').glob('*') if p.is_file())
    archived = {}
    for path in preserved:
        target = archive / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        archived[str(path)] = {'sha256': sha(path), 'bytes': path.stat().st_size,
                              'archived_as': str(target)}
    write(archive / 'manifest.json', archived)

    commands = [
        ('factorial_report', ['-m', 'experiments.day15_moment_report']),
        ('factorial_integrity', ['-m', 'experiments.day18_factorial_receipt_audit',
                                '--root', str(ROOT), '--output', 'notes/day21_factorial_integrity.json']),
        ('progress_report', ['-m', 'experiments.day13_progress_report']),
        ('figures', ['-m', 'experiments.day17_evidence_figures']),
    ]
    codes = {}
    for label, command in commands:
        with Path('logs/day21_refresh_' + label + '.txt').open('x') as log:
            result = subprocess.run([sys.executable, '-u', *command], stdout=log,
                                    stderr=subprocess.STDOUT, timeout=180)
        codes[label] = result.returncode
        assert result.returncode == 0, label
        print('DERIVED_PASS', label, flush=True)
    quality = json.loads(Path('notes/day21_factorial_integrity.json').read_text())
    assert len(quality['passed']) == 12 and not quality['pending_or_unverified'] and not quality['failed']
    coverage = pd.read_csv('results/day15_coverage.csv')
    assert len(coverage) == 12 and coverage.groupby('regime').size().to_dict() == {'amazon': 6, 'banking': 6}
    intervals = pd.read_csv('results/day15_seed_intervals.csv')
    marginal = intervals[intervals.kind == 'marginal']
    assert len(marginal) == 56 and set(marginal.n_seeds) == {3}
    columns = ['regime', 'factor', 'metric', 'n_seeds', 'mean', 'ci_low', 'ci_high']
    marker = '| regime | factor | metric | n_seeds | mean | ci_low | ci_high |'
    assert original.count(marker) == 1
    start = original.index(marker)
    end = original.index('\n\n## 8. Related work and contribution boundary', start)
    updated = original[:start] + markdown_table(marginal[columns]) + original[end:]
    updated = updated.replace('10/20 verified trajectories', '12/20 verified trajectories (three paired seeds per regime)')
    updated = updated.replace('A read-only check of 10 completed observer trajectories',
                              'A read-only check of 12 completed observer trajectories')
    updated = updated.replace('The larger static rank-96 baseline remains untuned: its final accuracy is lower',
                              'Under the original untuned fixed recipe, the larger static rank-96 baseline has final accuracy lower')
    anchor = 'Primary source links and precise scope are in `notes/novelty_audit_20261006.md` and `notes/classifier_prior_audit_20261006.md`.'
    assert updated.count(anchor) == 1
    new_prior = ('Huh et al. (2024, LoRA-the-Explorer) already ablate LoRA-factor and optimizer resets. '
        'Wang, Su and Ma (2026, Bilinear Optimization Divergence) analyze bilinear learned anchors '
        'and realized optimizer displacements. Neither the bilinear cross terms nor a general '
        'gradient-versus-momentum distinction is claimed here as new theory. The possible distinction '
        'is the controlled attribution of classifier-bearing package allocation; its generality '
        'and practical value still require the missing comparators and stronger learning regime.\n\n'
        + anchor + ' The focused October 8 update is `notes/day21_novelty_and_next_evidence.md`.')
    updated = updated.replace(anchor, new_prior)
    section = ('## Source-path implementation diagnostic\n\n'
        'An auxiliary CPU check uses unchanged forward and reset classes from the official Online-LoRA '
        'repository at commit `59b9fd42ea9ca701cb36978709d5bc0e25938d81`, inside a synthetic QKV/classifier '
        'enclosure. All ten declared seed/dtype checks were retained. After the inspected reset zeros '
        'both fresh factors, their gradients are zero while inherited Adam state can move them; '
        'an empty optimizer leaves them zero in the matched step. A later factorwise consolidation '
        'changes the local Q/V result by the expected bilinear cross terms. The classifier remains '
        'learnable. These are implementation diagnostics, not image-benchmark performance, a complete '
        'published-method reproduction, new algebra, or ten independent benchmark replicates. '
        'The complete training loop, plateau detector, MAS and hard-buffer logic were not executed. '
        'Scope, source hashes and full numeric checks are in `notes/day21_online_lora_source_review.md`.\n\n')
    anchor = '## Figures and result sources'
    assert updated.count(anchor) == 1
    updated = updated.replace(anchor, section + anchor)
    assert '## Within-backbone output-classifier control' in updated
    assert '## Secondary deployed-retention analysis' in updated
    draft.write_text(updated)
    progress = Path('notes/research_progress.md')
    progress_text = progress.read_text()
    progress_text = progress_text.replace(
        'baseline-specific tuning with pilot/confirmation separation remains necessary.',
        'the subsequent Day-17 equal-grid study completed 24/24 pilot and 20/20 confirmation trajectories '
        'with a rate selected per rank before fresh-seed outcomes. This addresses the declared rate grid; '
        'broader tuning and complete-method confirmation remain open.')
    progress_text = progress_text.replace(
        'The saved GitHub snapshot and all 738 checkpoint files were successfully restored on the new pod; '
        'notes/github_save_verification.json records the earlier authenticated save.',
        'The October 8 restart SHA256-verified 580 unique LFS objects, 783 LFS working files and '
        'all 1566 checkpoint-manifest files before the bounded continuation. '
        'notes/day21_restore_integrity.json records that restoration; '
        'the current snapshot requires its own day21_github_save_verification.json receipt.')
    progress_text = progress_text.replace(
        '4. Separate head-weight reset from moment reset and test an intervention whose structural interpretation ',
        '4. Finish the remaining eight original weight/state factorial cells and test an intervention whose structural interpretation ')
    progress.write_text(progress_text + '\n\n## October 8 bounded continuation\n\n'
        'The original factorial queue now has 12/20 independently verified trajectories and three '
        'paired training seeds in each regime. Two additional original seed-2029 B-first cells '
        'passed exact replay gates; no contrast was changed. `notes/day21_factorial_integrity.json` '
        'checks every mature batch and all cells. The auxiliary Online-LoRA CPU source diagnostic '
        'does not reproduce its image benchmark. Close 2026 prior work and remaining gaps are in '
        '`notes/day21_novelty_and_next_evidence.md`. Final test evaluation remains untouched.\n')
    receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'command_returncodes': codes,
        'complete_factorial_observers': len(coverage), 'planned_factorial_observers': 20,
        'paired_training_seeds_by_regime': {'banking': 3, 'amazon': 3},
        'independent_saved_receipt_check': 'notes/day21_factorial_integrity.json',
        'all_56_marginal_metric_rows_retained': True, 'original_scientific_source_unchanged': True,
        'prior_derived_archive': str(archive), 'manuscript_before_sha256': archived[str(draft)]['sha256'],
        'manuscript_after_sha256': sha(draft), 'new_test_access': False,
        'figure_visual_review_pending': True,
        'derived_sha256': {str(p): sha(p) for p in [draft, progress, Path('results/day15_seed_intervals.csv')]},
        'matplotlib_version': __import__('matplotlib').__version__}
    receipt['refresh_script_sha256'] = sha(Path(__file__))
    receipt['development_aggregate_replay_check'] = 'notes/day21_development_replay_integrity.json'
    write(Path('notes/day21_evidence_refresh.json'), receipt)
    print('SAVED_EVIDENCE_REFRESH_PASS', len(coverage), 'trajectories; 56 marginal rows; old outputs archived', flush=True)


if __name__ == '__main__':
    main()
