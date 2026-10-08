"""Verify public model bytes against one immutable author's Hub commit."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download

OUTPUT = Path('notes/day22_pinned_model_file_integrity.json')
FILES = ['config.json', 'model.safetensors', 'tokenizer.json', 'tokenizer_config.json', 'vocab.txt']


def main():
    assert not OUTPUT.exists(), 'Refusing to overwrite a model verification attempt'
    revision = json.loads(Path('notes/restart_20261006_preflight.json').read_text())['backbone_revision']
    info = HfApi().model_info('distilbert-base-uncased', revision=revision, files_metadata=True)
    assert info.sha == revision
    siblings = {item.rfilename: item for item in info.siblings}
    rows, parents = [], set()
    for name in FILES:
        item = siblings[name]
        path = Path(hf_hub_download('distilbert-base-uncased', filename=name, revision=revision))
        assert path.parent.name == revision
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if item.lfs is not None:
            assert digest == item.lfs.sha256 and len(content) == item.lfs.size
            mode = 'sha256_matches_pinned_author_lfs_metadata'
        else:
            blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
            assert blob == item.blob_id
            mode = 'git_blob_sha1_matches_pinned_author_commit'
        parents.add(str(path.parent))
        rows.append({'filename': name, 'cache_path': str(path), 'bytes': len(content), 'sha256': digest,
                     'author_git_blob_id': item.blob_id, 'verification_mode': mode, 'status': 'passed'})
    assert len(parents) == 1
    payload = {'status': 'passed', 'utc': datetime.now(timezone.utc).isoformat(),
        'model': 'distilbert-base-uncased', 'model_revision': revision,
        'author_commit_verified': True, 'model_snapshot_directory': parents.pop(), 'files': rows,
        'historical_unpinned_backbone_identity_claimed': False,
        'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUTPUT.write_text(json.dumps(payload, indent=2) + '\n')
    print('PINNED_MODEL_BYTES_VERIFIED', revision, len(rows), 'files', flush=True)


if __name__ == '__main__':
    main()
