"""Save only the authorized repository and verify all current LFS objects afresh.

Run after manual GitHub login. Authentication data is never read or serialized.
An independent empty LFS storage is used, because this pod lacks earlier caches.
"""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'anitusiruk/mitosis-interference'
BRANCH = 'day5-causal-audit'
ENV = os.environ.copy()
ENV.update(GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1', GCM_INTERACTIVE='never')


def read(args):
    return subprocess.check_output(args, env=ENV, text=True, timeout=90).strip()


def run(args, timeout=300):
    subprocess.run(args, env=ENV, check=True, timeout=timeout)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def remote_head():
    value = read(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH])
    assert value and len(value.splitlines()) == 1
    return value.split()[0]


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    os.chdir(ROOT)
    lock = open('/workspace/mitosis-restart-worker.lock', 'a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert read(['git', 'remote', 'get-url', 'origin']) == 'https://github.com/' + REPOSITORY + '.git'
    assert read(['git', 'branch', '--show-current']) == BRANCH
    assert not read(['git', 'status', '--porcelain']), 'Commit the complete state first'
    for prefix in ['day21_', 'day21_amazon_']:
        row = json.loads(Path('notes/' + prefix + 'audit_execution.json').read_text())
        assert row['status'] == 'completed' and row['returncode'] == 0
    repo = json.loads(read(['gh', 'api', 'repos/' + REPOSITORY]))
    assert repo['full_name'] == REPOSITORY and repo['permissions']['push']
    run(['gh', 'auth', 'setup-git'], timeout=90)
    snapshot = read(['git', 'rev-parse', 'HEAD'])
    manifest = json.loads(Path('results/checkpoint_preservation_manifest.json').read_text())
    current_checkpoints = {str(p) for p in Path('results').rglob('*') if p.is_file() and 'checkpoint' in p.parts}
    assert current_checkpoints == set(manifest), 'Manifest does not cover exactly every checkpoint file'
    mapping = {line.split(' ', 2)[2]: line.split()[0]
               for line in read(['git', 'lfs', 'ls-files', '--long']).splitlines()}
    for name, expected in manifest.items():
        p = Path(name)
        assert p.stat().st_size == expected['bytes'] and sha(p) == expected['sha256'], name
        if p.suffix in {'.pt', '.safetensors'}:
            assert mapping.get(name) == expected['sha256'], name
    for name, oid in mapping.items():
        assert sha(Path(name)) == oid, 'Working LFS file is a pointer or changed: ' + name
    run(['git', 'lfs', 'fsck'])
    run(['git', 'push', '--set-upstream', 'origin', BRANCH])
    assert remote_head() == snapshot
    run(['git', 'lfs', 'push', '--all', 'origin', BRANCH])
    unique = set(mapping.values())
    total = sum(Path(name).stat().st_size for name in mapping)
    assert shutil.disk_usage(ROOT).free > total + 1024**3, 'Insufficient space for independent verification'
    storage = ROOT.parent / ('mitosis-day21-lfs-verify-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    assert not storage.exists()
    run(['git', '-c', 'lfs.storage=' + str(storage), 'lfs', 'fetch', '--include=*', '--exclude=', 'origin', BRANCH])
    run(['git', '-c', 'lfs.storage=' + str(storage), 'lfs', 'fsck'])
    for oid in unique:
        obj = storage / 'objects' / oid[:2] / oid[2:4] / oid
        assert obj.is_file() and sha(obj) == oid, 'Remote object failed SHA256: ' + oid
    receipt = {'verified_utc': datetime.now(timezone.utc).isoformat(), 'repository': REPOSITORY,
        'branch': BRANCH, 'preserved_snapshot_commit': snapshot, 'github_snapshot_commit_verified': True,
        'verification_mode': 'independent_remote_download_into_new_empty_lfs_storage',
        'verification_storage': str(storage), 'historical_download_cache_reused': False,
        'all_current_lfs_sha256_verified': True, 'lfs_files': len(mapping),
        'unique_lfs_objects_verified': len(unique), 'checkpoint_files': len(manifest),
        'checkpoint_bytes': sum(x['bytes'] for x in manifest.values()),
        'checkpoint_manifest_sha256': sha(Path('results/checkpoint_preservation_manifest.json'))}
    write(Path('notes/day21_github_save_verification.json'), receipt)
    status = json.loads(Path('notes/preservation_status.json').read_text())
    status.update(snapshot_commit=snapshot, git_push_returncode=0,
        new_snapshot_push_pending=False, github_ref_verified=True,
        remote_checkpoints_sha256_verified=True, last_successful_github_snapshot_commit=snapshot,
        last_successful_github_snapshot_verified_utc=receipt['verified_utc'],
        github_verification_receipt='notes/day21_github_save_verification.json')
    write(Path('notes/preservation_status.json'), status)
    queue = json.loads(Path('notes/day15_16_execution_status.json').read_text())
    queue.update(github_save_pending=False, github_save_verified=True,
                 github_verification_receipt='notes/day21_github_save_verification.json')
    write(Path('notes/day15_16_execution_status.json'), queue)
    handoff = Path('notes/day21_session_handoff.md')
    handoff.write_text(handoff.read_text().replace(
        'GitHub save is pending until notes/day21_github_save_verification.json records a successful independent remote LFS round trip.',
        'The complete snapshot and independent remote LFS round trip are verified in notes/day21_github_save_verification.json.'))
    run(['git', 'add', 'notes/day21_github_save_verification.json', 'notes/preservation_status.json',
         'notes/day15_16_execution_status.json', 'notes/day21_session_handoff.md'])
    run(['git', 'commit', '-m', 'Verify full GitHub snapshot and independent round trip of every current checkpoint object'])
    run(['git', 'push', 'origin', BRANCH])
    final = read(['git', 'rev-parse', 'HEAD'])
    assert remote_head() == final and not read(['git', 'status', '--porcelain'])
    write(ROOT.parent / 'day21-final-save-status.json', {'status': 'passed', 'final_github_commit': final,
        'snapshot_commit': snapshot, 'all_current_lfs_sha256_verified': True,
        'repository': REPOSITORY, 'branch': BRANCH, 'utc': datetime.now(timezone.utc).isoformat()})
    print('GITHUB_SAVE_VERIFIED', final, 'CHECKPOINTS', len(manifest), 'LFS_OBJECTS', len(unique), flush=True)


if __name__ == '__main__':
    main()
