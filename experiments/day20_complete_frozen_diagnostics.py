"""Resume only unlaunched frozen audits after the first verified editorial save.

Scheduling amendment only: the scientific trainer and original job definitions
remain byte-identical. No completed or failed attempt is overwritten.
"""
import ast
from datetime import datetime, timedelta, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('/workspace/mitosis-interference')
BRANCH = 'day5-causal-audit'
EXPECTED_WORKER = '11f7493d9003c65d307db1830c5ec76c591c9e137cdebbd9387e67a11a60e640'
BASELINE_DRAFT = '2a3158350c783920f36c217f738c8061796b78beecaab5115d7cec3a0d2306a6'
WAIT_DEADLINE = datetime.fromisoformat('2026-10-07T06:10:00+00:00')
ENV = os.environ.copy()
ENV.update(GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1')


def now():
    return datetime.now(timezone.utc).isoformat()


def read(args):
    return subprocess.check_output(args, cwd=ROOT, env=ENV, text=True, timeout=90).strip()


def run(args, log=None):
    print('RUN', ' '.join(args), flush=True)
    return subprocess.run(args, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                          stdout=log, stderr=subprocess.STDOUT if log else None).returncode


def write(path, value):
    p = ROOT / path
    p.write_text(json.dumps(value, indent=2) + '\n')


def push(message):
    assert run(['git', 'add', '-A']) == 0
    if read(['git', 'status', '--porcelain']):
        assert run(['git', 'commit', '-m', message]) == 0
    assert run(['git', 'push', 'origin', BRANCH]) == 0
    head = read(['git', 'rev-parse', 'HEAD'])
    assert read(['git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH]).split()[0] == head
    assert not read(['git', 'status', '--porcelain'])
    return head


def amend_schedule(source, cutoff, deadline):
    tree = ast.parse(source)
    changed = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        name = node.targets[0].id if isinstance(node.targets[0], ast.Name) else None
        if name == 'LAUNCH_CUTOFF':
            node.value = ast.parse('datetime.fromisoformat(' + repr(cutoff) + ')', mode='eval').body
            changed.add(name)
        elif name == 'TRAINING_DEADLINE':
            node.value = ast.Constant(deadline)
            changed.add(name)
    assert changed == {'LAUNCH_CUTOFF', 'TRAINING_DEADLINE'}
    # Explicitly verify that all other original statements remain identical.
    original = ast.parse(source)
    for a, b in zip(original.body, tree.body):
        if isinstance(a, ast.Assign) and len(a.targets) == 1 and isinstance(a.targets[0], ast.Name) and a.targets[0].id in changed:
            continue
        assert ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)
    return ast.fix_missing_locations(tree)


def main():
    os.chdir(ROOT)
    locks = [open('/workspace/mitosis-restart-worker.lock', 'a'),
             open('/workspace/mitosis-static-tuning-worker.lock', 'a')]
    while True:
        if datetime.now(timezone.utc) >= WAIT_DEADLINE:
            raise RuntimeError('Follow-on launch wait expired; saved experiments remain untouched')
        acquired, ready = [], False
        try:
            for lock in locks:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired.append(lock)
            p = ROOT / 'notes/final_evidence_quality_status.json'
            if p.exists():
                qc = json.loads(p.read_text())
                ready = all(qc.get(key) == 0 for key in [
                    'quality_control_returncode', 'editorial_returncode', 'secondary_retention_returncode'])
                ready = ready and not read(['git', 'status', '--porcelain'])
                ready = ready and read(['git', 'rev-parse', 'HEAD']) == read([
                    'git', 'ls-remote', 'origin', 'refs/heads/' + BRANCH]).split()[0]
            if ready:
                break
        except BlockingIOError:
            pass
        finally:
            if not ready:
                for lock in acquired:
                    fcntl.flock(lock, fcntl.LOCK_UN)
        print('FROZEN_CONTINUATION_WAITING_FOR_VERIFIED_EVIDENCE_SAVE', now(), flush=True)
        time.sleep(30)
    assert read(['git', 'branch', '--show-current']) == BRANCH
    assert read(['git', 'ls-files', '--error-unmatch', 'experiments/day20_complete_frozen_diagnostics.py'])
    assert read(['git', 'remote', 'get-url', 'origin']) == 'https://github.com/anitusiruk/mitosis-interference.git'
    status_path = ROOT / 'notes/day15_16_execution_status.json'
    previous = json.loads(status_path.read_text())
    assert previous.get('github_save_verified') and not previous.get('failed')
    assert all(r['status'] == 'completed' and not r.get('report_failed') and not r.get('progress_report_failed') for r in previous['jobs'])
    source_path = ROOT / 'experiments/day15_16_research_worker.py'
    source = source_path.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED_WORKER
    baseline = ROOT / 'notes/paper_working_draft_before_extended_audits.md'
    assert hashlib.sha256(baseline.read_bytes()).hexdigest() == BASELINE_DRAFT
    archive = ROOT / 'notes/day20_initial_verified_diagnostics_status.json'
    assert not archive.exists()
    archive.write_bytes(status_path.read_bytes())
    started = datetime.now(timezone.utc)
    cutoff, deadline = started + timedelta(hours=4), started + timedelta(hours=4, minutes=20)
    write('notes/day20_continuation_launch.json', {
        'utc': now(), 'original_worker_sha256': EXPECTED_WORKER,
        'scientific_job_definitions_unchanged': True,
        'only_ast_assignments_changed': ['LAUNCH_CUTOFF', 'TRAINING_DEADLINE'],
        'launch_cutoff_utc': cutoff.isoformat(), 'training_deadline_utc': deadline.isoformat(),
        'already_completed_jobs': len(previous['jobs']), 'planned_total_jobs': 40,
        'original_protocol_commit': 'dc45300d212e7ef52c77f4652bb64f9b5083945f',
        'reason': 'complete the originally declared five-seed factorial coverage; do not select a new protocol from partial results'})
    push('Declare scheduling-only continuation of unlaunched frozen factorial audits')
    # The original worker takes these same locks itself. Nobody else is queued
    # after the completed first editorial save; release before its acquisition.
    for lock in acquired:
        fcntl.flock(lock, fcntl.LOCK_UN)
    namespace = {'__name__': '__main__', '__file__': str(source_path)}
    print('FROZEN_CONTINUATION_LAUNCH', now(), 'REMAINING', 40-len(previous['jobs']), flush=True)
    exec(compile(amend_schedule(source.decode(), cutoff.isoformat(), deadline.isoformat()),
                 str(source_path), 'exec'), namespace)
    # Original worker retains its exclusive lock in this namespace through QC.
    current = json.loads(status_path.read_text())
    assert current['github_save_verified'] and not current['failed']
    receipt = json.loads((ROOT/'notes/github_save_verification.json').read_text())
    assert receipt['all_current_lfs_sha256_verified']
    earlier_qc = ROOT/'notes/factorial_receipt_integrity_final.json'
    archived_qc = ROOT/'notes/factorial_receipt_integrity_before_completion.json'
    assert not archived_qc.exists()
    archived_qc.write_bytes(earlier_qc.read_bytes())
    codes = {}
    with (ROOT/'logs/day20_factorial_receipt_integrity.txt').open('x') as log:
        codes['quality'] = run([sys.executable, '-u', '-m', 'experiments.day18_factorial_receipt_audit',
            '--root', str(ROOT), '--output', 'notes/factorial_receipt_integrity_final.json'], log)
    if codes['quality'] == 0:
        (ROOT/'notes/paper_working_draft_before_factorial_completion.md').write_bytes(
            (ROOT/'notes/paper_working_draft.md').read_bytes())
        (ROOT/'notes/paper_working_draft.md').write_bytes(baseline.read_bytes())
        for label, module in [('manuscript', 'experiments.day17_manuscript_refresh'),
                              ('figures', 'experiments.day17_evidence_figures'),
                              ('caveats', 'experiments.day18_evidence_caveats')]:
            with (ROOT/('logs/day20_'+label+'.txt')).open('x') as log:
                codes[label] = run([sys.executable, '-u', '-m', module], log)
            if codes[label]:
                break
    completed = sum(r['study'] == 15 and r['status'] == 'completed' for r in current['jobs'])
    qc = json.loads((ROOT/'notes/factorial_receipt_integrity_final.json').read_text())
    assert len(qc['passed']) == completed
    changed = read(['git', 'diff', '--name-only', receipt['preserved_snapshot_commit'], 'HEAD']).splitlines()
    changed += read(['git', 'diff', '--name-only']).splitlines()
    assert not any('checkpoint' in Path(p).parts or Path(p).suffix in {'.pt','.safetensors'} for p in changed)
    quality = json.loads((ROOT/'notes/final_evidence_quality_status.json').read_text())
    quality.update(utc=now(), quality_control_returncode=codes['quality'],
        editorial_returncode=(max(codes[k] for k in ['manuscript','figures','caveats']) if all(k in codes for k in ['manuscript','figures','caveats']) else None),
        finalization_returncodes=codes, figure_render_review_pending=True, verified_observers=len(qc['passed']),
        remaining_observers=20-len(qc['passed']),
        independently_remote_verified_checkpoint_snapshot=receipt['preserved_snapshot_commit'],
        checkpoint_verification_mode=receipt['verification_mode'],
        checkpoint_tree_unchanged_since_verified_snapshot=True)
    write('notes/final_evidence_quality_status.json', quality)
    write('notes/day20_completion_status.json', {'utc': now(), 'returncodes': codes,
        'completed_factorial_trajectories': completed, 'planned_factorial_trajectories': 20,
        'all_declared_diagnostics_completed': current['complete'],
        'training_sources_unchanged': True, 'independently_verified_checkpoint_snapshot': receipt['preserved_snapshot_commit'],
        'paper_remains_development_evidence': True})
    head = push('Refresh all factorial evidence and preserve independent final integrity receipts')
    print('FROZEN_DIAGNOSTIC_COMPLETION_AND_EVIDENCE_SAVED', head, 'OBSERVERS', completed,
          'COMPLETE', current['complete'], 'CODES', codes, flush=True)
    if any(codes.values()):
        raise RuntimeError('Post-completion editorial discrepancy preserved')


if __name__ == '__main__':
    main()
