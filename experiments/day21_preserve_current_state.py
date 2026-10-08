"""Hash every checkpoint and commit the complete bounded-session state."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main():
    import os
    os.chdir(ROOT)
    assert subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip() == 'https://github.com/anitusiruk/mitosis-interference.git'
    assert subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip() == 'day5-causal-audit'
    for name in ['day21_replay_execution', 'day21_audit_execution',
                 'day21_amazon_replay_execution', 'day21_amazon_audit_execution']:
        r = json.loads(Path('notes/' + name + '.json').read_text())
        assert r['status'] == 'completed' and r['returncode'] == 0, name
    refresh = json.loads(Path('notes/day21_evidence_refresh.json').read_text())
    assert not refresh['figure_visual_review_pending'], 'Inspect the refreshed figures before saving the final session'
    manifest = {}
    for path in sorted(Path('results').rglob('*')):
        if path.is_file() and 'checkpoint' in path.parts:
            manifest[str(path)] = {'bytes': path.stat().st_size, 'sha256': sha(path)}
    write(Path('results/checkpoint_preservation_manifest.json'), manifest)
    state = json.loads(Path('notes/preservation_status.json').read_text())
    state.update(timestamp_utc=datetime.now(timezone.utc).isoformat(),
        checkpoint_files=len(manifest), checkpoint_bytes=sum(x['bytes'] for x in manifest.values()),
        new_snapshot_push_pending=True, github_ref_verified=False,
        remote_checkpoints_sha256_verified=False, local_checkpoint_sha256_verified=True)
    write(Path('notes/preservation_status.json'), state)
    handoff = ('# October 8 bounded-session handoff\n\n'
        'Authoritative repository: anitusiruk/mitosis-interference, branch day5-causal-audit. '
        'The two original seed-2029 B-first factorial cells are complete. Their exact replay gates '
        'and final audited learners match the saved references bitwise. Coverage is 12/20, with '
        'three paired training seeds in each regime; the original scientific trainer and contrasts '
        'are unchanged. No automatic GPU queue remains.\n\n'
        'All prior checkpoint trees remain, and the complete preservation manifest was refreshed. '
        'The old draft, Day-15 tables and extended figures are archived under '
        'notes/day21_before_bounded_refresh. Fresh raw receipts, derived tables, independent QC, '
        'manuscript and visually checked figures are saved. GitHub save is pending until '
        'notes/day21_github_save_verification.json records a successful independent remote LFS round trip. '
        'Do not infer a new save from historical verification flags.\n\n'
        'The auxiliary Online-LoRA CPU probe keeps all ten seed/dtype checks, executes only two '
        'unchanged author classes in a synthetic enclosure, and makes no published benchmark claim. '
        'Close 2026 prior work narrows novelty. Complete comparator reproduction, stronger natural '
        'same-label learning, the remaining eight factorial cells and a frozen final evaluation '
        'remain outstanding. The next shared-label note is a proposal, not an executed confirmation.\n\n'
        'For restart, restore this exact branch and all Git LFS objects, then hash the manifest '
        'before computing. Do not run the old Day-20 driver with expired absolute deadlines. '
        'Launch any later original cell separately after a measured replay/timing gate, use fresh '
        'attempt names and a short hard process-group cap, and retain unsuccessful attempts.\n')
    Path('notes/day21_session_handoff.md').write_text(handoff)
    subprocess.run(['git', 'add', '-A'], check=True)
    # Preserve raw terminal progress and generated SVG whitespace byte-for-byte.
    subprocess.run(['git', 'diff', '--cached', '--check', '--', ':(top,glob)experiments/day21_*.py',
                    ':(top,glob)notes/day21_*.md', 'notes/paper_working_draft.md'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Preserve two exact original factorial continuations, full evidence refresh and source audit'], check=True)
    print('LOCAL_COMPLETE_SNAPSHOT', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
          'CHECKPOINTS', len(manifest), 'BYTES', sum(x['bytes'] for x in manifest.values()), flush=True)


if __name__ == '__main__':
    main()
