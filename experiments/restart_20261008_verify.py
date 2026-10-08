import hashlib,json,subprocess,time,os
from pathlib import Path
from datetime import datetime,timezone
os.chdir('/workspace/mitosis-interference')
out=Path('notes/restart_20261008_recovery.json')
assert not out.exists()
r={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),'restored_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'prior_pod_unsaved_outputs_available':False}
def save(): out.write_text(json.dumps(r,indent=2))
save()
try:
 for attempt in range(180):
  if 'RESTORE_DEPENDENCIES_COMPLETE' in Path('/workspace/restore-environment.log').read_text(): break
  time.sleep(5)
 else: raise RuntimeError('Dependency restoration did not complete within 15 minutes')
 manifest=json.loads(Path('results/checkpoint_preservation_manifest.json').read_text())
 actual={str(p) for p in Path('results').rglob('*') if p.is_file() and 'checkpoint' in p.parts}
 assert actual==set(manifest),'Checkpoint path set mismatch'
 total=0
 for name,expected in manifest.items():
  content=Path(name).read_bytes(); digest=hashlib.sha256(content).hexdigest()
  assert digest==(expected if isinstance(expected,str) else expected['sha256']),name
  total+=len(content)
 subprocess.run(['git','lfs','fsck'],check=True)
 r.update(checkpoint_files_verified=len(manifest),checkpoint_bytes=total,all_sha256_verified=True);save()
 from huggingface_hub import hf_hub_download
 model=json.loads(Path('notes/day22_pinned_model_file_integrity.json').read_text())
 for row in model['files']:
  p=Path(hf_hub_download(model['model'],row['filename'],revision=model['model_revision'],cache_dir=str(Path(model['model_snapshot_directory']).parents[2])))
  assert p==Path(row['cache_path'])
  assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
 r.update(status='passed',model_files_verified=len(model['files']),finished_utc=datetime.now(timezone.utc).isoformat())
 save();print('RECOVERY_VERIFIED',r,flush=True)
except Exception as e:
 r.update(status='failed',error=repr(e));save();raise
