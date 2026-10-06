"""Run the frozen continuation and save only to the existing GitHub repo."""
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path('/workspace/mitosis-interference')
os.chdir(ROOT)
ENV = os.environ.copy()
ENV.update(OMP_NUM_THREADS='8', TOKENIZERS_PARALLELISM='false',
           GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1', GCM_INTERACTIVE='never')


def read(command):
    return subprocess.check_output(command, env=ENV, text=True, timeout=90).strip()


def run(command):
    print('RUN', ' '.join(command), flush=True)
    subprocess.run(command, env=ENV, check=True)


def save_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


lock = open('/workspace/mitosis-restart-worker.lock', 'a')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
assert read(['git', 'branch', '--show-current']) == 'day5-causal-audit'
assert read(['git', 'remote', 'get-url', 'origin']) == 'https://github.com/anitusiruk/mitosis-interference.git'
gate = json.loads(Path('notes/restart_20261006_preflight.json').read_text())
assert gate['status'] == 'passed'
ENV['MITOSIS_MODEL_REVISION'] = gate['backbone_revision']
run(['git', 'config', '--local', 'user.name', 'Codex'])
run(['git', 'config', '--local', 'user.email', 'codex@localhost'])
run(['git', 'add', '-A'])
if read(['git', 'status', '--porcelain']):
    run(['git', 'commit', '-m', 'Verify GitHub recovery and pin frozen experiment continuation'])
queue = [sys.executable, '-u', '-m', 'experiments.restart_20261006_queue',
         '--launch-cutoff-utc', '2026-10-07T03:00:00+00:00',
         '--training-deadline-utc', '2026-10-07T03:15:00+00:00',
         '--routing-deadline-utc', '2026-10-07T03:25:00+00:00']
started = datetime.now(timezone.utc).isoformat()
result = subprocess.run(queue, env=ENV)
save_json('notes/restart_execution_status.json', {
    'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
    'queue_returncode': result.returncode, 'successful_execution': result.returncode == 0,
    'github_save_pending': True, 'repository': 'anitusiruk/mitosis-interference'})
manifest = {}
for path in sorted(Path('results').rglob('*')):
    if path.is_file() and 'checkpoint' in path.parts:
        h = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                h.update(block)
        manifest[str(path)] = {'bytes': path.stat().st_size, 'sha256': h.hexdigest()}
save_json('results/checkpoint_preservation_manifest.json', manifest)
save_json('environment/restart_runtime.json', {
    'python': sys.version,
    'packages': {d.metadata['Name']: d.version for d in metadata.distributions() if d.metadata['Name']},
    'backbone_revision': gate['backbone_revision']})
preservation = json.loads(Path('notes/preservation_status.json').read_text())
preservation.update(checkpoint_files=len(manifest), checkpoint_bytes=sum(x['bytes'] for x in manifest.values()),
                    github_push_returncode=None, github_ref_verified=False, new_snapshot_push_pending=True)
save_json('notes/preservation_status.json', preservation)
run(['git', 'add', '-A'])
if read(['git', 'status', '--porcelain']):
    run(['git', 'commit', '-m', 'Preserve all frozen continuation outcomes and complete checkpoint state'])
deadline = datetime.fromisoformat('2026-10-07T03:29:00+00:00')
while datetime.now(timezone.utc) < deadline:
    auth = subprocess.run(['gh', 'api', 'user', '--jq', '.login'], env=ENV,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    if auth.returncode == 0:
        break
    print('GITHUB_CONNECTION_REQUIRED_FOR_SAVE', flush=True)
    time.sleep(15)
else:
    raise RuntimeError('GitHub authentication unavailable; local commits exist but new snapshot was not pushed')
run([sys.executable, '-u', '-m', 'experiments.finalize_github_save'])
receipt = json.loads(Path('notes/github_save_verification.json').read_text())
assert receipt['all_current_lfs_sha256_verified']
preservation.update(github_push_returncode=0, github_ref_verified=True, new_snapshot_push_pending=False,
                    remote_checkpoints_sha256_verified=True,
                    last_successful_github_snapshot_commit=receipt['preserved_snapshot_commit'],
                    last_successful_github_save_verified_utc=receipt['verified_utc'])
save_json('notes/preservation_status.json', preservation)
execution = json.loads(Path('notes/restart_execution_status.json').read_text())
execution.update(github_save_pending=False, github_save_verified=True)
save_json('notes/restart_execution_status.json', execution)
run(['git', 'add', 'notes/preservation_status.json', 'notes/restart_execution_status.json'])
run(['git', 'commit', '-m', 'Record verified GitHub preservation of resumed research'])
run(['git', 'push', 'origin', 'day5-causal-audit'])
head = read(['git', 'rev-parse', 'HEAD'])
assert read(['git', 'ls-remote', 'origin', 'refs/heads/day5-causal-audit']).split()[0] == head
assert not read(['git', 'status', '--porcelain'])
print('RESTART_AND_GITHUB_SAVE_COMPLETE', head, 'QUEUE_RETURN_CODE', result.returncode, flush=True)
if result.returncode:
    raise RuntimeError('Research queue failed; attempted state was saved and must be inspected')
