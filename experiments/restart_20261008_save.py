"""Checkpoint the authorized project and verify new LFS objects from GitHub."""
import fcntl, hashlib, json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path('/workspace/mitosis-interference')
os.chdir(ROOT)
lock=open('/workspace/mitosis-restart-worker.lock','a')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
ENV=os.environ.copy(); ENV.update(GIT_TERMINAL_PROMPT='0',GH_PROMPT_DISABLED='1')
def read(args): return subprocess.check_output(args,text=True,env=ENV,timeout=180).strip()
def run(args): subprocess.run(args,check=True,env=ENV,timeout=600)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024**2),b''): h.update(b)
 return h.hexdigest()
def write(p,d): p.write_text(json.dumps(d,indent=2,sort_keys=True))
assert read(['git','remote','get-url','origin'])=='https://github.com/anitusiruk/mitosis-interference.git'
assert read(['git','branch','--show-current'])=='day5-causal-audit'
recovery=json.loads(Path('notes/restart_20261008_recovery.json').read_text());assert recovery['status']=='passed'
for p in Path('notes').glob('day22*execution.json'):
 assert json.loads(p.read_text()).get('status')!='running',str(p)
base=recovery['restored_commit']
old={line.split()[0] for line in read(['git','lfs','ls-files','--long',base]).splitlines()}
manifest_path=Path('results/checkpoint_preservation_manifest.json')
archive=Path('notes/restart_20261008_original_checkpoint_manifest.json')
if not archive.exists(): archive.write_bytes(manifest_path.read_bytes())
manifest={str(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(Path('results').rglob('*')) if p.is_file() and 'checkpoint' in p.parts}
write(manifest_path,manifest)
run(['git','add','--all'])
if read(['git','diff','--cached','--name-only']): run(['git','commit','-m','Preserve complete recovered research state and current checkpoints'])
snapshot=read(['git','rev-parse','HEAD'])
mapping={line.split(' ',2)[2]:line.split()[0] for line in read(['git','lfs','ls-files','--long']).splitlines()}
for name,oid in mapping.items(): assert sha(Path(name))==oid,name
run(['git','lfs','fsck'])
run(['git','push','origin','day5-causal-audit'])
assert read(['git','ls-remote','origin','refs/heads/day5-causal-audit']).split()[0]==snapshot
new={name:oid for name,oid in mapping.items() if oid not in old}
cache=ROOT.parent/('verified-lfs-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
assert not cache.exists()
if new:
 run(['git','-c','lfs.storage='+str(cache),'lfs','fetch','--include='+','.join(new),'--exclude=','origin','day5-causal-audit'])
 for oid in set(new.values()): assert sha(cache/'objects'/oid[:2]/oid[2:4]/oid)==oid
receipt={'status':'passed','utc':datetime.now(timezone.utc).isoformat(),'snapshot_commit':snapshot,'checkpoint_files':len(manifest),'checkpoint_bytes':sum(x['bytes'] for x in manifest.values()),'all_working_lfs_sha256_verified':True,'new_unique_lfs_objects_independently_downloaded':len(set(new.values())),'restored_old_objects_verified_by':'notes/restart_20261008_recovery.json','new_lfs_storage':str(cache),'scope':'Old objects verified on restoration; new object bytes independently downloaded from GitHub.'}
write(Path('notes/restart_20261008_github_save.json'),receipt)
run(['git','add','notes/restart_20261008_github_save.json'])
run(['git','commit','-m','Record verified GitHub checkpoint persistence'])
run(['git','push','origin','day5-causal-audit'])
final=read(['git','rev-parse','HEAD'])
assert read(['git','ls-remote','origin','refs/heads/day5-causal-audit']).split()[0]==final
assert not read(['git','status','--porcelain'])
write(Path('/workspace/restart_20261008_save_final.json'),{'status':'passed','final_commit':final,'clean':True,'receipt':receipt})
print('SAVE_VERIFIED',final,len(manifest),flush=True)
