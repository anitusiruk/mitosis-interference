"""Run a preregistered equal-grid baseline repair and preserve every attempt."""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path('/workspace/mitosis-interference')
BRANCH = 'day5-causal-audit'
RATES = [2e-5, 5e-5, 1e-4, 2e-4, 4e-4, 8e-4]
LAUNCH_CUTOFF = datetime.fromisoformat('2026-10-07T03:00:00+00:00')
DEADLINE = '2026-10-07T03:15:00+00:00'
STATUS = Path('notes/day17_static_tuning_execution.json')
ENV = os.environ.copy()
ENV.update(OMP_NUM_THREADS='8', TOKENIZERS_PARALLELISM='false',
           GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1')


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, data):
    p = Path(path)
    temporary = p.with_suffix(p.suffix + '.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(p)


def read(args):
    return subprocess.check_output(args, env=ENV, text=True, timeout=90).strip()


def command(args, log=None):
    print('RUN', ' '.join(args), flush=True)
    return subprocess.run(args, env=ENV, stdin=subprocess.DEVNULL, stdout=log,
                          stderr=subprocess.STDOUT if log else None).returncode


def preserve():
    manifest = {}
    for p in sorted(Path('results').rglob('*')):
        if p.is_file() and 'checkpoint' in p.parts:
            digest = hashlib.sha256()
            with p.open('rb') as stream:
                for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                    digest.update(block)
            manifest[str(p)] = {'bytes': p.stat().st_size, 'sha256': digest.hexdigest()}
    write('results/checkpoint_preservation_manifest.json', manifest)
    p = json.loads(Path('notes/preservation_status.json').read_text())
    p.update(checkpoint_files=len(manifest), checkpoint_bytes=sum(r['bytes'] for r in manifest.values()),
             new_snapshot_push_pending=True, github_ref_verified=False, remote_checkpoints_sha256_verified=False)
    write('notes/preservation_status.json', p)
    if command(['git', 'add', '-A']):
        raise RuntimeError('Staging failed')
    if read(['git', 'status', '--porcelain']):
        if command(['git', 'commit', '-m', 'Preserve pilot-selected fixed-capacity baseline progress']):
            raise RuntimeError('Progress commit failed')
    if command(['git', 'push', 'origin', BRANCH]):
        raise RuntimeError('Progress push failed; preserve local state')
    head = read(['git', 'rev-parse', 'HEAD'])
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH]).split()[0] == head
    assert not read(['git', 'status', '--porcelain'])
    print('STATIC_BASELINE_PROGRESS_PUSHED', head, flush=True)


def run_job(records, name, rank, rate, seed, order, phase):
    folder = Path('results', name)
    assert not folder.exists(), 'Refusing to overwrite ' + str(folder)
    args = [sys.executable, '-u', '-m', 'experiments.day17_static_tuning', '--rank', str(rank),
            '--learning-rate', str(rate), '--seed', str(seed), '--order', order,
            '--output', str(folder), '--deadline-utc', DEADLINE]
    row = {'name': name, 'phase': phase, 'status': 'running', 'started_utc': now(), 'command': args}
    records.append(row)
    write(STATUS, {'jobs': records, 'planned_research_jobs': 44, 'github_save_pending': True})
    with Path('logs', name + '.txt').open('x') as log:
        code = command(args, log)
    row.update(status='completed' if code == 0 else 'failed', returncode=code, finished_utc=now())
    if phase == 'replay_gate' and code == 0:
        with Path('logs', name + '_verify.txt').open('x') as log:
            code = command([sys.executable, '-u', '-m', 'experiments.day17_static_replay_gate',
                            '--output', str(folder)], log)
        row.update(replay_verification_returncode=code, status='completed' if code == 0 else 'failed')
    if phase != 'replay_gate':
        with Path('logs', name + '_report.txt').open('x') as log:
            report_code = command([sys.executable, '-u', '-m', 'experiments.day17_static_tuning_report'], log)
        if report_code:
            row['report_failed'] = True
            code = report_code
    write(STATUS, {'jobs': records, 'planned_research_jobs': 44, 'github_save_pending': True})
    preserve()
    print('STATIC_BASELINE_JOB', name, row['status'], flush=True)
    if code:
        raise RuntimeError('Baseline discrepancy preserved: ' + name)


def main():
    os.chdir(ROOT)
    ENV['MITOSIS_MODEL_REVISION'] = json.loads(Path('notes/restart_20261006_preflight.json').read_text())['backbone_revision']
    lock = open('/workspace/mitosis-restart-worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert read(['git', 'branch', '--show-current']) == BRANCH
    assert read(['git', 'remote', 'get-url', 'origin']) == 'https://github.com/anitusiruk/mitosis-interference.git'
    assert not read(['git', 'status', '--porcelain'])
    assert not STATUS.exists(), 'An existing preserved attempt requires inspection'
    records, failed, stopped = [], False, False
    try:
        if datetime.now(timezone.utc) >= LAUNCH_CUTOFF:
            stopped = True
        else:
            run_job(records, 'day17_rank96_reference_replay', 96, 2e-4, 2031, 'b_first', 'replay_gate')
        for rank in [8, 96]:
            for rate in RATES:
                for order in ['canonical', 'b_first']:
                    if stopped or datetime.now(timezone.utc) >= LAUNCH_CUTOFF:
                        stopped = True
                        break
                    tag = int(round(rate * 1e6))
                    run_job(records, f'day17_pilot_rank{rank}_lr{tag}_seed2026_{order}',
                            rank, rate, 2026, order, 'pilot')
        pilots = [r for r in records if r['phase'] == 'pilot' and r['status'] == 'completed']
        if len(pilots) == 24:
            from experiments.day17_static_tuning_report import pilot_table, select_pilot_rates
            data = pilot_table()
            selected, grid = select_pilot_rates(data)
            receipt = {'selected_rates': selected, 'grid_summary': grid, 'selected_utc': now(),
                'pilot_seed': 2026, 'selection_metric': 'final concept-macro accuracy, averaged paired pilot orders',
                'tie_break': 'smaller learning rate', 'confirmation_outcomes_used': False,
                'spec_sha256': hashlib.sha256(Path('notes/day17_static_tuning_spec.md').read_bytes()).hexdigest(),
                'pilot_grid_sha256': hashlib.sha256(Path('results/day17_static_pilot_grid.csv').read_bytes()).hexdigest()}
            assert not Path('notes/day17_static_rate_selection.json').exists()
            write('notes/day17_static_rate_selection.json', receipt)
            preserve()  # Freeze the pilot-only choice on GitHub before confirmation.
            for seed in range(2027, 2032):
                for order in ['canonical', 'b_first']:
                    for rank in [8, 96]:
                        if datetime.now(timezone.utc) >= LAUNCH_CUTOFF:
                            stopped = True
                            break
                        rate = selected[str(rank)]
                        tag = int(round(rate * 1e6))
                        run_job(records, f'day17_confirm_rank{rank}_lr{tag}_seed{seed}_{order}',
                                rank, rate, seed, order, 'confirmation')
    except Exception as error:
        failed = True
        write('notes/day17_static_tuning_failure.json', {'error': repr(error), 'utc': now()})
        print('STATIC_BASELINE_HALTED', repr(error), flush=True)
    write(STATUS, {'jobs': records, 'planned_research_jobs': 44, 'github_save_pending': True,
                   'failed': failed, 'administratively_stopped': stopped})
    preserve()
    if command([sys.executable, '-u', '-m', 'experiments.finalize_github_save']):
        raise RuntimeError('Baseline remote checkpoint roundtrip failed')
    receipt = json.loads(Path('notes/github_save_verification.json').read_text())
    assert receipt['all_current_lfs_sha256_verified']
    p = json.loads(Path('notes/preservation_status.json').read_text())
    p.update(github_push_returncode=0, github_ref_verified=True, new_snapshot_push_pending=False,
             remote_checkpoints_sha256_verified=True,
             last_successful_github_snapshot_commit=receipt['preserved_snapshot_commit'],
             last_successful_github_save_verified_utc=receipt['verified_utc'])
    write('notes/preservation_status.json', p)
    complete = sum(r['phase'] != 'replay_gate' and r['status'] == 'completed' for r in records) == 44 and not failed
    write(STATUS, {'jobs': records, 'planned_research_jobs': 44, 'github_save_pending': False,
                   'github_save_verified': True, 'failed': failed, 'complete': complete,
                   'administratively_stopped': stopped})
    if command(['git', 'add', 'notes/preservation_status.json', str(STATUS)]):
        raise RuntimeError('Final baseline receipt staging failed')
    if command(['git', 'commit', '-m', 'Record verified checkpoint preservation for tuned static baselines']):
        raise RuntimeError('Final baseline receipt commit failed')
    if command(['git', 'push', 'origin', BRANCH]):
        raise RuntimeError('Final baseline receipt push failed')
    head = read(['git', 'rev-parse', 'HEAD'])
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH]).split()[0] == head
    assert not read(['git', 'status', '--porcelain'])
    print('STATIC_BASELINE_AND_GITHUB_SAVE_COMPLETE', head, 'COMPLETE', complete, 'FAILED', failed, flush=True)


if __name__ == '__main__':
    main()
