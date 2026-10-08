"""Launch one declared NLI timing/pilot job; never queue another automatically."""
import argparse
from datetime import datetime, timezone
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
TIMING = Path('results/day22_multinli_timing_v4')
RATES = [5e-5, 2e-4, 8e-4]


def write(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def pilot_name(rate, order):
    return f'day22_multinli_v4_single_seed2026_lr{rate:g}_{order}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['timing', 'pilot'], required=True)
    parser.add_argument('--learning-rate', type=float, choices=RATES, default=2e-4)
    parser.add_argument('--order', choices=['canonical', 'b_first'], default='canonical')
    args = parser.parse_args()
    os.chdir(ROOT)
    lock = open('/workspace/mitosis-restart-worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip() == 'https://github.com/anitusiruk/mitosis-interference.git'
    for name in ['experiments/day22_multinli_pilot_v4.py', 'experiments/day22_bounded_nli_pilot_v4.py',
                 'notes/day22_multinli_learnability_pilot_v4_spec.md']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + name]) == Path(name).read_bytes(), name
    for name in ['src/adapter_pool.py', 'src/adapter_pool_cau_v0.py', 'src/adapter_pool_cau_v1.py',
                 'experiments/day7_multinli_recurrence.py']:
        assert subprocess.check_output(['git', 'show', 'b13105d211c013120784e79c38e3e77849e4ccbf:' + name]) == Path(name).read_bytes(), name
    previous = json.loads(Path('notes/day15_16_execution_status.json').read_text())
    assert not previous.get('failed') and all(row['status'] == 'completed' for row in previous['jobs'])
    if args.mode == 'timing':
        assert args.learning_rate == 2e-4 and args.order == 'canonical'
        name = TIMING.name
    else:
        timing = json.loads((TIMING / 'summary.json').read_text())
        receipt = json.loads(Path('notes/day22_multinli_timing_v4_execution.json').read_text())
        assert timing['status'] == 'completed' and timing['compute_admitted']
        assert receipt['status'] == 'completed' and receipt['returncode'] == 0
        planned = [pilot_name(rate, order) for rate in RATES for order in ['canonical', 'b_first']]
        remaining = []
        for candidate in planned:
            candidate_receipt = Path('notes/' + candidate + '_execution.json')
            if candidate_receipt.exists():
                row = json.loads(candidate_receipt.read_text())
                assert row['status'] == 'completed' and row['returncode'] == 0, 'Inspect preserved pilot discrepancy'
            else:
                remaining.append(candidate)
        name = pilot_name(args.learning_rate, args.order)
        assert remaining and name == remaining[0], 'Only the next declared pilot is eligible'
    output = Path('results') / name
    receipt_path = Path('notes/' + name + '_execution.json')
    assert not output.exists() and not receipt_path.exists(), 'Refusing to overwrite an attempt'
    gpu = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.total,memory.used', '--format=csv,noheader,nounits'], text=True).strip().splitlines()
    assert len(gpu) == 1
    total, used = [int(value.strip()) for value in gpu[0].split(',')]
    assert total >= 8192 and used < 256
    command = [sys.executable, '-u', '-m', 'experiments.day22_multinli_pilot_v4', '--mode', args.mode,
               '--learning-rate', str(args.learning_rate), '--order', args.order, '--output', str(output)]
    env = os.environ.copy()
    env.update(OMP_NUM_THREADS='8', TOKENIZERS_PARALLELISM='false')
    row = {'name': name, 'status': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(),
           'command': command, 'external_process_group_limit_seconds': 1500,
           'spec_sha256': hashlib.sha256(Path('notes/day22_multinli_learnability_pilot_v4_spec.md').read_bytes()).hexdigest(),
           'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
           'gpu_memory_total_mib': total, 'gpu_memory_used_before_mib': used}
    write(receipt_path, row)
    started = time.monotonic()
    with Path('logs/' + name + '.txt').open('x') as log:
        process = subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        row['pid'] = process.pid
        write(receipt_path, row)
        try:
            code = process.wait(timeout=1500)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 124
    row.update(returncode=code, seconds=time.monotonic() - started,
               finished_utc=datetime.now(timezone.utc).isoformat(), status='completed' if code == 0 else 'failed')
    write(receipt_path, row)
    print('BOUNDED_NLI', name, row['status'], round(row['seconds'], 2), flush=True)
    if code:
        raise RuntimeError('Preserved pilot failed; inspect before continuing')


if __name__ == '__main__':
    main()
