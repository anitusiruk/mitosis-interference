"""Verify the restored immutable checkpoint snapshot and tiny observer gates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, time, shutil
ROOT=Path('/workspace/mitosis-interference')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
 return h.hexdigest()
def main():
 start=time.monotonic()
 r={'started_utc':datetime.now(timezone.utc).isoformat(),'status':'running',
    'restored_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()}
 out=ROOT/'notes/day21_restore_integrity.json'
 try:
  files=json.loads(subprocess.check_output(['git','lfs','ls-files','--json'],text=True))['files']
  objects={x['oid']:x['size'] for x in files}
  for oid,n in objects.items():
   p=ROOT/'.git/lfs/objects'/oid[:2]/oid[2:4]/oid
   assert p.stat().st_size==n and sha(p)==oid, str(p)
  for x in files:
   p=ROOT/x['name']
   assert p.stat().st_size==x['size'] and sha(p)==x['oid'], str(p)
  manifest=json.loads((ROOT/'results/checkpoint_preservation_manifest.json').read_text())
  for name,x in manifest.items():
   p=ROOT/name
   assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'], name
  r.update(lfs_unique_objects_verified=len(objects), lfs_working_files_verified=len(files),
    checkpoint_manifest_files_verified=len(manifest),all_sha256_verified=True,
    checkpoint_bytes=sum(x['bytes'] for x in manifest.values()))
  print('RESTORE_HASH_VERIFIED',len(objects),len(files),len(manifest),flush=True)
  r['integrity_gates']={}
  for device in ['cpu','cuda']:
   log=ROOT/('logs/day21_moment_integrity_'+device+'.txt')
   t=time.monotonic()
   with log.open('x') as f:
    c=subprocess.run([sys.executable,'-u','-m','experiments.day15_moment_integrity','--device',device],
      stdout=f,stderr=subprocess.STDOUT,timeout=180)
   r['integrity_gates'][device]={'returncode':c.returncode,'seconds':time.monotonic()-t,'log':str(log.relative_to(ROOT))}
   print('INTEGRITY_GATE',device,c.returncode,round(time.monotonic()-t,2),flush=True)
   assert c.returncode==0, 'Integrity gate failed: '+device
  r['status']='passed'
 except Exception as e:
  r.update(status='failed',error=type(e).__name__+': '+str(e))
  raise
 finally:
  r.update(finished_utc=datetime.now(timezone.utc).isoformat(),seconds=time.monotonic()-start,
    free_disk_bytes=shutil.disk_usage(ROOT).free)
  out.write_text(json.dumps(r,indent=2)+chr(10))
if __name__=='__main__':main()
