"""Integrate independent, verified branches without racing research workers."""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('/workspace/mitosis-interference')
AUXILIARY = Path('/workspace/mitosis-static-tuning')
MAIN_BRANCH = 'day5-causal-audit'
STATIC_BRANCH = 'day17-static-tuning-20261006'
DEADLINE = datetime.fromisoformat('2026-10-07T03:25:00+00:00')
ENV = os.environ.copy()
ENV.update(GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1', TOKENIZERS_PARALLELISM='false')


def now():
    return datetime.now(timezone.utc).isoformat()


def read(args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, env=ENV, text=True, timeout=90).strip()


def command(args, log=None):
    print('RUN', ' '.join(args), flush=True)
    return subprocess.run(args, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                          stdout=log, stderr=subprocess.STDOUT if log else None).returncode


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def push(message):
    assert command(['git', 'add', '-A']) == 0
    if read(['git', 'status', '--porcelain']):
        assert command(['git', 'commit', '-m', message]) == 0
    assert command(['git', 'push', 'origin', MAIN_BRANCH]) == 0
    head = read(['git', 'rev-parse', 'HEAD'])
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + MAIN_BRANCH]).split()[0] == head
    assert not read(['git', 'status', '--porcelain'])
    return head


def main():
    os.chdir(ROOT)
    main_lock = open('/workspace/mitosis-restart-worker.lock', 'a')
    static_lock = open('/workspace/mitosis-static-tuning-worker.lock', 'a')
    while True:
        if datetime.now(timezone.utc) >= DEADLINE:
            raise RuntimeError('Integration cutoff; retain both independently preserved branches')
        acquired = []
        try:
            for lock in [main_lock, static_lock]:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired.append(lock)
            paths = [ROOT / 'notes/day15_16_execution_status.json',
                     AUXILIARY / 'notes/day17_static_tuning_execution.json']
            if all(p.exists() for p in paths):
                diagnostic, static = [json.loads(p.read_text()) for p in paths]
                if diagnostic.get('github_save_verified') and static.get('github_save_verified'):
                    break
        except BlockingIOError:
            pass
        finally:
            if len(acquired) != 2 or not ('diagnostic' in locals() and 'static' in locals()
                    and diagnostic.get('github_save_verified') and static.get('github_save_verified')):
                for lock in acquired:
                    fcntl.flock(lock, fcntl.LOCK_UN)
        print('INTEGRATION_WAITING_FOR_BOTH_VERIFIED_SAVES', now(), flush=True)
        time.sleep(30)
    assert read(['git', 'branch', '--show-current']) == MAIN_BRANCH
    assert read(['git', 'remote', 'get-url', 'origin']) == 'https://github.com/anitusiruk/mitosis-interference.git'
    assert not read(['git', 'status', '--porcelain'])
    main_head = read(['git', 'rev-parse', 'HEAD'])
    static_head = read(['git', 'rev-parse', 'HEAD'], AUXILIARY)
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + MAIN_BRANCH]).split()[0] == main_head
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + STATIC_BRANCH]).split()[0] == static_head
    assert command(['git', 'merge', '--no-ff', '--no-edit', STATIC_BRANCH]) == 0
    assert not read(['git', 'status', '--porcelain'])
    codes = {}
    for label, module in [('manuscript', 'experiments.day17_manuscript_refresh'),
                          ('figures', 'experiments.day17_evidence_figures')]:
        with Path('logs', 'day17_integrated_' + label + '.txt').open('x') as log:
            codes[label] = command([sys.executable, '-u', '-m', module], log)
    manifest = {}
    for p in sorted(Path('results').rglob('*')):
        if p.is_file() and 'checkpoint' in p.parts:
            digest = hashlib.sha256()
            with p.open('rb') as stream:
                for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                    digest.update(block)
            manifest[str(p)] = {'bytes': p.stat().st_size, 'sha256': digest.hexdigest()}
    write('results/checkpoint_preservation_manifest.json', manifest)
    preservation = json.loads(Path('notes/preservation_status.json').read_text())
    preservation.update(checkpoint_files=len(manifest), checkpoint_bytes=sum(r['bytes'] for r in manifest.values()),
                        new_snapshot_push_pending=True, github_ref_verified=False,
                        remote_checkpoints_sha256_verified=False)
    write('notes/preservation_status.json', preservation)
    integration = {'utc': now(), 'diagnostic_branch_head': main_head, 'static_branch_head': static_head,
        'repository': 'anitusiruk/mitosis-interference', 'editorial_returncodes': codes,
        'diagnostic_complete': diagnostic.get('complete'), 'diagnostic_failed': diagnostic.get('failed'),
        'static_complete': static.get('complete'), 'static_failed': static.get('failed'),
        'combined_save_pending': True}
    write('notes/day17_branch_integration.json', integration)
    push('Integrate preserved static tuning and refresh all diagnostic evidence')
    if command([sys.executable, '-u', '-m', 'experiments.finalize_github_save']):
        raise RuntimeError('Combined remote checkpoint verification failed; retain local and branch saves')
    receipt = json.loads(Path('notes/github_save_verification.json').read_text())
    assert receipt['all_current_lfs_sha256_verified']
    preservation.update(github_push_returncode=0, github_ref_verified=True,
        new_snapshot_push_pending=False, remote_checkpoints_sha256_verified=True,
        last_successful_github_snapshot_commit=receipt['preserved_snapshot_commit'],
        last_successful_github_save_verified_utc=receipt['verified_utc'])
    write('notes/preservation_status.json', preservation)
    integration.update(combined_save_pending=False, combined_remote_checkpoints_verified=True,
                       verified_utc=now(), verified_snapshot=receipt['preserved_snapshot_commit'])
    write('notes/day17_branch_integration.json', integration)
    head = push('Record independently verified combined research checkpoint preservation')
    print('INTEGRATED_RESEARCH_AND_GITHUB_SAVE_COMPLETE', head, 'EDITORIAL', codes, flush=True)
    if any(codes.values()):
        raise RuntimeError('Editorial discrepancy preserved; inspect the corresponding log')


if __name__ == '__main__':
    main()
