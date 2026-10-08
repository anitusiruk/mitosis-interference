"""Execute exactly one replay or originally unlaunched factorial trajectory."""
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
REPLAY = 'day21_banking_private_cau_seed2029_b_first_replay'
AUDIT = 'day15_banking_private_cau_seed2029_b_first_weight_moments'


def write(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['replay', 'audit'], required=True)
    parser.add_argument('--regime', choices=['banking', 'amazon'], default='banking')
    args = parser.parse_args()
    replay_name = REPLAY.replace('banking', args.regime)
    audit_name = AUDIT.replace('banking', args.regime)
    note_prefix = 'day21_' if args.regime == 'banking' else 'day21_amazon_'
    os.chdir(ROOT)
    lock = open('/workspace/mitosis-restart-worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    restore = json.loads(Path('notes/day21_restore_integrity.json').read_text())
    assert restore['status'] == 'passed' and restore['all_sha256_verified']
    for filename in ['src/moment_component_audit.py', 'experiments/day8_fixed_memory_recurrence.py',
                     'experiments/day15_weight_moment_recurrence.py', 'notes/day15_weight_moment_spec.md']:
        original = subprocess.check_output(['git', 'show', RESTORED_COMMIT + ':' + filename])
        assert original == Path(filename).read_bytes(), filename
    previous = json.loads(Path('notes/day15_16_execution_status.json').read_text())
    assert not previous.get('failed')
    assert all(x['status'] == 'completed' for x in previous['jobs'])
    if args.phase == 'audit':
        replay = Path('results') / replay_name
        assert json.loads((replay / 'observer_verification.json').read_text())['status'] == 'passed'
        calibration = json.loads(Path('notes/' + note_prefix + 'replay_execution.json').read_text())
        assert calibration['status'] == 'completed'
        assert calibration['seconds'] < 240, 'Replayed trainer too slow for the bounded audit budget'
        assert not any(x['name'] == audit_name for x in previous['jobs'])
    name = replay_name if args.phase == 'replay' else audit_name
    output = Path('results') / name
    assert not output.exists(), 'Refusing to overwrite an attempt'
    receipt_path = Path('notes/' + note_prefix + args.phase + '_execution.json')
    assert not receipt_path.exists()
    budget = 300 if args.phase == 'replay' else 1380
    external_limit = budget + 120
    deadline = datetime.now(timezone.utc) + timedelta(seconds=budget)
    command = [sys.executable, '-u', '-m', 'experiments.day21_checked_trajectory',
               '--output', str(output), '--deadline-utc', deadline.isoformat(), '--regime', args.regime]
    if args.phase == 'audit':
        command.append('--factorial')
    env = os.environ.copy()
    env.update(OMP_NUM_THREADS='8', TOKENIZERS_PARALLELISM='false')
    row = {'name': name, 'study': 15 if args.phase == 'audit' else 'restore_replay',
           'status': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(),
           'command': command, 'training_budget_seconds': budget,
           'external_process_group_limit_seconds': external_limit,
           'spec_sha256': hashlib.sha256(Path('notes/day21_bounded_continuation_spec.md' if args.regime == 'banking'
                                             else 'notes/day21_amazon_continuation_spec.md').read_bytes()).hexdigest(),
           'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()}
    write(receipt_path, row)
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
    row.update(returncode=code, seconds=time.monotonic()-started,
               finished_utc=datetime.now(timezone.utc).isoformat(),
               status='completed' if code == 0 else 'failed')
    write(receipt_path, row)
    if args.phase == 'audit':
        previous['jobs'].append(row)
        previous.update(generated_utc=row['finished_utc'], github_save_pending=True,
                        github_save_verified=False, failed=code != 0, complete=False)
        write(Path('notes/day15_16_execution_status.json'), previous)
    print('BOUNDED_PHASE', args.phase, row['status'], round(row['seconds'], 2), flush=True)
    if code:
        raise RuntimeError('Preserved trajectory failed; inspect before continuing')


if __name__ == '__main__':
    main()
