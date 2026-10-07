"""Isolated within-backbone frozen pre-classifier allocation controls.

Shares the GPU with diagnostics; timing is descriptive, not a compute benchmark.
Publishes only to a branch of the existing mitosis-interference repository.
"""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path('/workspace/mitosis-static-tuning')
BRANCH = 'day17-static-tuning-20261006'
LAUNCH_CUTOFF = datetime.fromisoformat('2026-10-07T03:00:00+00:00')
DEADLINE = '2026-10-07T03:15:00+00:00'
STATUS = Path('notes/day19_linear_classifier_execution.json')
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


def checkpoint_manifest():
    manifest = {}
    for folder in sorted(Path('results').glob('day19_*')):
        if not folder.is_dir():
            continue
        for p in sorted((folder / 'checkpoint').rglob('*')):
            if p.is_file():
                digest = hashlib.sha256()
                with p.open('rb') as stream:
                    for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                        digest.update(block)
                manifest[str(p)] = {'bytes': p.stat().st_size, 'sha256': digest.hexdigest()}
    return manifest


def preserve():
    write('results/day19_checkpoint_preservation_manifest.json', checkpoint_manifest())
    if command(['git', 'add', '-A']):
        raise RuntimeError('Staging failed')
    if read(['git', 'status', '--porcelain']):
        if command(['git', 'commit', '-m', 'Preserve frozen pre-classifier diagnostic progress']):
            raise RuntimeError('Progress commit failed')
    if command(['git', 'push', 'origin', BRANCH]):
        raise RuntimeError('Progress push failed; preserve local state')
    head = read(['git', 'rev-parse', 'HEAD'])
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH]).split()[0] == head
    assert not read(['git', 'status', '--porcelain'])
    print('LINEAR_CONTROL_PROGRESS_PUSHED', head, flush=True)


def verify_new_checkpoint_roundtrip():
    # This worktree intentionally retains pointers for unrelated old checkpoints.
    # Verify newly generated Day-19 checkpoints; do not replace the main manifest.
    snapshot = read(['git', 'rev-parse', 'HEAD'])
    manifest = json.loads(Path('results/day19_checkpoint_preservation_manifest.json').read_text())
    lines = read(['git', 'lfs', 'ls-files', '--long']).splitlines()
    by_path = {line.split(' ', 2)[2]: line.split()[0] for line in lines}
    tensors = {p for p in manifest if Path(p).suffix in {'.pt', '.safetensors'}}
    assert tensors <= set(by_path)
    for p, item in manifest.items():
        assert Path(p).stat().st_size == item['bytes']
        assert hashlib.sha256(Path(p).read_bytes()).hexdigest() == item['sha256']
        if p in tensors:
            assert item['sha256'] == by_path[p]
    fresh = Path('/workspace') / ('mitosis-day19-lfs-verify-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    assert not fresh.exists()
    if command(['git', '-c', 'lfs.storage=' + str(fresh), 'lfs', 'fetch',
                '--include=results/day19_*/checkpoint/**', '--exclude=', 'origin', BRANCH]):
        raise RuntimeError('Fresh static checkpoint download failed')
    oids = {by_path[p] for p in tensors}
    for oid in oids:
        p = fresh / 'objects' / oid[:2] / oid[2:4] / oid
        assert p.is_file(), 'Missing remotely downloaded static checkpoint'
        assert hashlib.sha256(p.read_bytes()).hexdigest() == oid
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH]).split()[0] == snapshot
    receipt = {'repository': 'anitusiruk/mitosis-interference', 'branch': BRANCH,
        'preserved_snapshot_commit': snapshot, 'verified_utc': now(),
        'scope': 'new Day-19 checkpoints only; unrelated checkpoints retain their main-branch receipts',
        'all_day19_lfs_sha256_verified': True, 'fresh_remote_lfs_fetch_returncode': 0,
        'checkpoint_files': len(manifest), 'tensor_files': len(tensors),
        'unique_lfs_objects_verified': len(oids),
        'checkpoint_bytes': sum(r['bytes'] for r in manifest.values())}
    write('notes/day19_github_save_verification.json', receipt)
    print('LINEAR_CONTROL_REMOTE_CHECKPOINT_ROUNDTRIP_PASS', len(oids), flush=True)
    return receipt


def run_job(records, architecture, seed, order, mode):
    name = ('day19_reference_replay_head_only_seed2031_b_first' if mode == 'inherited'
            else f'day19_banking_{architecture}_seed{seed}_{order}_frozen_preclassifier')
    folder = Path('results', name)
    assert not folder.exists()
    args = [sys.executable, '-u', '-m', 'experiments.day19_linear_classifier_control',
        '--architecture', architecture, '--preclassifier-mode', mode, '--seed', str(seed),
        '--order', order, '--output', str(folder), '--deadline-utc', DEADLINE]
    row = {'name': name, 'phase': 'replay_gate' if mode == 'inherited' else 'diagnostic',
           'status': 'running', 'started_utc': now(), 'command': args}
    records.append(row)
    write(STATUS, {'jobs': records, 'planned_research_jobs': 20, 'github_save_pending': True})
    with Path('logs', name + '.txt').open('x') as log:
        code = command(args, log)
    row.update(status='completed' if code == 0 else 'failed', returncode=code, finished_utc=now())
    if mode == 'frozen':
        with Path('logs', name + '_report.txt').open('x') as log:
            report_code = command([sys.executable, '-u', '-m', 'experiments.day19_linear_classifier_report'], log)
        if report_code:
            row['report_failed'] = True
            code = report_code
    write(STATUS, {'jobs': records, 'planned_research_jobs': 20, 'github_save_pending': True})
    preserve()
    print('LINEAR_CONTROL_JOB', name, row['status'], flush=True)
    if code:
        raise RuntimeError('Linear-classifier discrepancy preserved: ' + name)


def main():
    os.chdir(ROOT)
    ENV['MITOSIS_MODEL_REVISION'] = json.loads(Path('notes/restart_20261006_preflight.json').read_text())['backbone_revision']
    lock = open('/workspace/mitosis-static-tuning-worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert read(['git', 'branch', '--show-current']) == BRANCH
    assert read(['git', 'remote', 'get-url', 'origin']) == 'https://github.com/anitusiruk/mitosis-interference.git'
    assert not read(['git', 'status', '--porcelain'])
    assert json.loads(Path('notes/day17_static_tuning_execution.json').read_text())['github_save_verified']
    assert not STATUS.exists()
    records, failed, stopped = [], False, False
    try:
        if datetime.now(timezone.utc) >= LAUNCH_CUTOFF:
            stopped = True
        else:
            run_job(records, 'head_only', 2031, 'b_first', 'inherited')
        for seed in range(2027, 2032):
            for order in ['canonical', 'b_first']:
                for architecture in ['private', 'head_only']:
                    if stopped or datetime.now(timezone.utc) >= LAUNCH_CUTOFF:
                        stopped = True
                        break
                    run_job(records, architecture, seed, order, 'frozen')
    except Exception as error:
        failed = True
        write('notes/day19_linear_classifier_failure.json', {'error': repr(error), 'utc': now()})
        print('LINEAR_CONTROL_HALTED', repr(error), flush=True)
    write(STATUS, {'jobs': records, 'planned_research_jobs': 20, 'github_save_pending': True,
                   'failed': failed, 'administratively_stopped': stopped})
    preserve()
    verify_new_checkpoint_roundtrip()
    complete = sum(r['phase'] == 'diagnostic' and r['status'] == 'completed' for r in records) == 20 and not failed
    write(STATUS, {'jobs': records, 'planned_research_jobs': 20, 'github_save_pending': False,
                   'github_save_verified': True, 'failed': failed, 'complete': complete,
                   'administratively_stopped': stopped})
    assert command(['git', 'add', 'notes/day19_github_save_verification.json', str(STATUS)]) == 0
    assert command(['git', 'commit', '-m', 'Record verified frozen pre-classifier control preservation']) == 0
    assert command(['git', 'push', 'origin', BRANCH]) == 0
    head = read(['git', 'rev-parse', 'HEAD'])
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH]).split()[0] == head
    assert not read(['git', 'status', '--porcelain'])
    print('LINEAR_CLASSIFIER_AND_GITHUB_SAVE_COMPLETE', head, 'COMPLETE', complete, 'FAILED', failed, flush=True)


if __name__ == '__main__':
    main()
