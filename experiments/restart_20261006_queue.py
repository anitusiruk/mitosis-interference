"""Continue only the saved, unlaunched controls; preserve every attempt."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2))
    temporary.replace(path)


def run(module, arguments, log_name):
    path = Path('logs') / log_name
    with path.open('x') as log:
        result = subprocess.run([sys.executable, '-u', '-m', module, *arguments],
                                stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    if result.returncode:
        raise RuntimeError(f'{module} failed; inspect preserved log {path}')


def verify_job(job):
    folder = Path('results') / job['name']
    summary = json.loads((folder / 'summary.json').read_text())
    provenance = json.loads((folder / 'provenance.json').read_text())
    assert summary['status'] == 'completed', folder
    expected = json.loads(Path('notes/restart_20261006_preflight.json').read_text())
    reference = next(x for x in expected['stream_checks'] if x['run'] == job['name'])
    assert provenance['stream_sha256'] == reference['stream_sha256'], folder
    assert provenance['model_revision'] == expected['backbone_revision'], folder
    assert provenance['official_test_used'] is False and summary['official_test_used'] is False
    routing = pd.read_csv(folder / 'routing.csv')
    assert len(routing) == provenance['stream_steps'] == summary['steps'] == 80, folder
    assert list(routing.step) == list(range(1, 81)), folder
    assert np.isfinite(routing.loc[routing.train_executed, 'loss']).all(), folder
    if job['study'] == 8:
        assert routing.replay_items.max() <= 512 and routing.num_adapters.max() <= 8, folder
    assert (folder / 'checkpoint/learner_state.pt').stat().st_size > 1000, folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--launch-cutoff-utc', required=True)
    parser.add_argument('--training-deadline-utc', required=True)
    parser.add_argument('--routing-deadline-utc', required=True)
    args = parser.parse_args()
    cutoff, training_deadline, routing_deadline = [datetime.fromisoformat(value) for value in
        [args.launch_cutoff_utc, args.training_deadline_utc, args.routing_deadline_utc]]
    assert all(value.tzinfo is not None for value in [cutoff, training_deadline, routing_deadline])
    assert cutoff < training_deadline < routing_deadline
    gate = json.loads(Path('notes/restart_20261006_preflight.json').read_text())
    assert gate['status'] == 'passed'
    os.environ['MITOSIS_MODEL_REVISION'] = gate['backbone_revision']
    os.environ['OMP_NUM_THREADS'] = '8'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    jobs = json.loads(Path('notes/remaining_frozen_jobs.json').read_text())
    assert len(jobs) == 45 and len({job['name'] for job in jobs}) == 45
    for job in jobs:
        status_path = Path(f"logs/day{job['study']}_queue_status.json")
        records = json.loads(status_path.read_text())
        existing = [row for row in records if row['name'] == job['name']]
        if existing:
            assert len(existing) == 1 and existing[0]['status'] == 'completed', existing
            verify_job(job)
            print('SKIP_COMPLETED', job['name'], flush=True)
            continue
        if datetime.now(timezone.utc) >= cutoff:
            print('NEW_LAUNCH_CUTOFF_REACHED', now(), flush=True)
            break
        output = Path('results') / job['name']
        assert not output.exists(), f'Refusing to overwrite preserved attempt: {output}'
        command = [sys.executable, '-u', '-m', job['module'], '--regime', job['regime'],
                   '--architecture', job['architecture'], '--policy', job['policy'],
                   '--seed', str(job['seed']), '--order', job['order'], '--output', str(output),
                   '--deadline-utc', args.training_deadline_utc]
        row = {'name': job['name'], 'command': command, 'status': 'running',
               'start_utc': now(), 'dispatcher': 'restart_20261006_queue'}
        records.append(row)
        write_json(status_path, records)
        with Path(f"logs/{job['name']}.txt").open('x') as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        row.update(returncode=result.returncode, end_utc=now(), status='failed')
        if result.returncode == 0 and (output / 'summary.json').exists():
            row['status'] = json.loads((output / 'summary.json').read_text())['status']
        write_json(status_path, records)
        print('FROZEN_JOB', job['name'], row['status'], flush=True)
        if row['status'] == 'failed':
            raise RuntimeError('Failed trajectory; preserved outputs require inspection')
        if row['status'] != 'completed':
            break
        verify_job(job)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for module in ['day8_fixed_memory_report', 'day10_mechanism_report', 'day12_capacity_report',
                   'day13_evidence_audit', 'day13_progress_report']:
        run('experiments.' + module, [], f'restart_{stamp}_{module}.txt')
    if datetime.now(timezone.utc) < routing_deadline:
        run('experiments.day14_fixed_memory_routing', ['--deadline-utc', args.routing_deadline_utc],
            f'restart_{stamp}_fixed_memory_routing.txt')
    run('experiments.day14_routing_report', [], f'restart_{stamp}_routing_report.txt')
    manifest = {}
    for path in sorted(Path('results').rglob('*')):
        if path.is_file() and 'checkpoint' in path.parts:
            h = hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                    h.update(block)
            manifest[str(path)] = {'bytes': path.stat().st_size, 'sha256': h.hexdigest()}
    write_json(Path('results/checkpoint_preservation_manifest.json'), manifest)
    print('RESTART_QUEUE_FINISHED', now(), 'CHECKPOINT_FILES', len(manifest), flush=True)


if __name__ == '__main__':
    main()
