"""Manually launch one original cell, with preserved attempts and short job caps."""
import argparse
from datetime import datetime, timedelta, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
RESTORED_COMMIT = 'b13105d211c013120784e79c38e3e77849e4ccbf'
SPEC = Path('notes/day22_original_queue_continuation_spec.md')


def write(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['replay', 'audit'], required=True)
    parser.add_argument('--regime', choices=['banking', 'amazon'], required=True)
    parser.add_argument('--seed', type=int, choices=[2030, 2031], required=True)
    parser.add_argument('--order', choices=['canonical', 'b_first'], required=True)
    args = parser.parse_args()
    os.chdir(ROOT)
    lock = open('/workspace/mitosis-restart-worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip() == 'https://github.com/anitusiruk/mitosis-interference.git'
    assert subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip() == 'day5-causal-audit'
    restore = json.loads(Path('notes/day21_restore_integrity.json').read_text())
    assert restore['status'] == 'passed' and restore['all_sha256_verified']
    for filename in ['src/moment_component_audit.py', 'experiments/day8_fixed_memory_recurrence.py',
                     'experiments/day15_weight_moment_recurrence.py', 'notes/day15_weight_moment_spec.md']:
        original = subprocess.check_output(['git', 'show', RESTORED_COMMIT + ':' + filename])
        assert original == Path(filename).read_bytes(), filename
    for filename in [str(SPEC), 'experiments/day22_checked_trajectory.py', 'experiments/day22_bounded_continuation.py']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + filename]) == Path(filename).read_bytes(), filename
    previous = json.loads(Path('notes/day15_16_execution_status.json').read_text())
    assert not previous.get('failed')
    assert all(x['status'] == 'completed' for x in previous['jobs'])
    names = [x['name'] for x in previous['jobs']]
    assert len(set(names)) == len(names)
    planned = [f'day15_{regime}_private_cau_seed{seed}_{order}_weight_moments'
               for seed in range(2027, 2032) for order in ['canonical', 'b_first']
               for regime in ['banking', 'amazon']]
    audit_name = f'day15_{args.regime}_private_cau_seed{args.seed}_{args.order}_weight_moments'
    remaining = [name for name in planned if name not in names]
    assert remaining and audit_name == remaining[0], 'Only the next original queue cell is eligible'
    stem = f'day22_{args.regime}_seed{args.seed}_{args.order}'
    replay_name = stem + '_replay'
    if args.phase == 'audit':
        replay = Path('results') / replay_name
        assert json.loads((replay / 'observer_verification.json').read_text())['status'] == 'passed'
        calibration = json.loads(Path('notes/' + stem + '_replay_execution.json').read_text())
        assert calibration['status'] == 'completed' and calibration['returncode'] == 0
        assert calibration['seconds'] < 240, 'Replayed trainer too slow for the bounded audit budget'
    name = replay_name if args.phase == 'replay' else audit_name
    output = Path('results') / name
    receipt_path = Path('notes/' + stem + '_' + args.phase + '_execution.json')
    assert not output.exists() and not receipt_path.exists(), 'Refusing to overwrite an attempt'
    gpu = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.total,memory.used', '--format=csv,noheader,nounits'], text=True).strip().splitlines()
    assert len(gpu) == 1
    total, used = [int(value.strip()) for value in gpu[0].split(',')]
    assert total >= 8192 and used < 256, 'GPU unavailable or another GPU job is active'
    budget = 300 if args.phase == 'replay' else 1380
    external_limit = budget + 120
    deadline = datetime.now(timezone.utc) + timedelta(seconds=budget)
    command = [sys.executable, '-u', '-m', 'experiments.day22_checked_trajectory',
               '--output', str(output), '--deadline-utc', deadline.isoformat(), '--regime', args.regime,
               '--seed', str(args.seed), '--order', args.order]
    if args.phase == 'audit':
        command.append('--factorial')
    env = os.environ.copy()
    env.update(OMP_NUM_THREADS='8', TOKENIZERS_PARALLELISM='false')
    row = {'name': name, 'study': 15 if args.phase == 'audit' else 'restore_replay',
           'status': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(),
           'command': command, 'training_budget_seconds': budget,
           'external_process_group_limit_seconds': external_limit,
           'spec_sha256': hashlib.sha256(SPEC.read_bytes()).hexdigest(),
           'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
           'gpu_memory_total_mib': total, 'gpu_memory_used_before_mib': used}
    write(receipt_path, row)
    if args.phase == 'audit':
        previous['jobs'].append(row)
        previous.update(generated_utc=row['started_utc'], github_save_pending=True,
                        github_save_verified=False, failed=False, complete=False)
        write(Path('notes/day15_16_execution_status.json'), previous)
    started = time.monotonic()
    with Path('logs/' + name + '.txt').open('x') as log:
        process = subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        row['pid'] = process.pid
        write(receipt_path, row)
        try:
            code = process.wait(timeout=external_limit)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 124
    row.update(returncode=code, seconds=time.monotonic() - started,
               finished_utc=datetime.now(timezone.utc).isoformat(),
               status='completed' if code == 0 else 'failed')
    write(receipt_path, row)
    if args.phase == 'audit':
        previous.update(generated_utc=row['finished_utc'], failed=code != 0,
                        complete=len(previous['jobs']) == 40 and code == 0)
        write(Path('notes/day15_16_execution_status.json'), previous)
    print('BOUNDED_PHASE', args.phase, row['status'], round(row['seconds'], 2), flush=True)
    if code:
        raise RuntimeError('Preserved trajectory failed; inspect before continuing')


if __name__ == '__main__':
    main()
