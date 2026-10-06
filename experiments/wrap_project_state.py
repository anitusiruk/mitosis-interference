"""Finish the paused trajectory and preserve the complete Git/LFS project."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import zipfile

def command(args,**kwargs):return subprocess.run(args,check=True,**kwargs)
def now():return datetime.now(timezone.utc).isoformat()
def file_hash(path):
    digest=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):digest.update(block)
    return digest.hexdigest()

root=Path.cwd()
assert (root/'.git').is_dir(),'Run from the authoritative RunPod checkout'
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='day5-causal-audit'
driver=int(Path('logs/tonight_balanced_pid.txt').read_text())
proc=Path(f'/proc/{driver}')
if proc.exists() and (proc/'cmdline').read_bytes():
    assert b'experiments/tonight_balanced_queue.py' in (proc/'cmdline').read_bytes().split(b'\0')
    assert (proc/'stat').read_text().split()[2]=='T','Dispatcher must be paused before wrapping'
    until=time.monotonic()+180
    while time.monotonic()<until:
        children=(proc/'task'/str(driver)/'children').read_text().split()
        active=[pid for pid in children if Path(f'/proc/{pid}/stat').exists()
                and Path(f'/proc/{pid}/stat').read_text().split()[2]!='Z']
        if not active:break
        print('WAIT_CURRENT_TRAJECTORY',active,flush=True);time.sleep(5)
    else:raise RuntimeError('Active learner did not finish; preserve state and inspect')
    os.kill(driver,signal.SIGTERM)
    try:os.kill(driver,signal.SIGCONT)
    except ProcessLookupError:pass

for day in [8,10,12]:
    path=Path(f'logs/day{day}_queue_status.json')
    records=json.loads(path.read_text())
    for row in records:
        if row['status']=='running':
            saved=Path('results')/row['name']/'summary.json'
            assert saved.exists(),f'Missing active-trajectory summary: {row["name"]}'
            summary=json.loads(saved.read_text())
            assert summary['status']=='completed',summary
            row.update(status='completed',returncode=0,end_utc=now(),
                       finalized_by='user_requested_wrap_after_child_exit')
    path.write_text(json.dumps(records,indent=2))

from experiments.tonight_balanced_queue import jobs
remaining=[]
coverage=[]
for day,expected in [(8,44),(10,12),(12,11)]:
    records=json.loads(Path(f'logs/day{day}_queue_status.json').read_text())
    completed={r['name'] for r in records if r['status']=='completed'}
    coverage.append({'study':day,'completed':len(completed),'planned':expected})
    for seed in ([2026,2027,2028] if day==10 else range(2026,2032)):
        for order in (['canonical'] if seed==2026 or day==10 else ['canonical','b_first']):
            for name,module,regime,architecture,policy in jobs(day,seed,order):
                if name not in completed:
                    remaining.append(dict(study=day,name=name,module=module,regime=regime,
                        architecture=architecture,policy=policy,seed=seed,order=order))
Path('notes/remaining_frozen_jobs.json').write_text(json.dumps(remaining,indent=2))
Path('notes/wrap_up_handoff.md').write_text(
    '# User-requested project wrap\n\nStopped '+now()+'. The active trajectory finished and saved its final checkpoint; '
    'the paused dispatcher was terminated before any further launch. The waiting bounded-memory routing '
    'driver was stopped. No ongoing GPU study is intended.\n\n'
    'Primary seed/order study: 80/80. MultiNLI stress test: 24/24. Original learned-router study: 110/110 '
    'checkpoints. Later study coverage: '+json.dumps(coverage)+'.\n\n'
    'Unlaunched frozen controls are listed in remaining_frozen_jobs.json. Their method/data protocols remain '
    'frozen. A subsequent session must supply a new deadline; the original dispatchers have expired '
    'hard-coded deadlines and refuse existing outputs. Never overwrite completed results or erase failed '
    'logs. The bounded-memory learned-router extension is implemented and declared but not executed.\n\n'
    'All completed learner weights, optimizers, RNG and reservoirs are versioned through Git LFS. '
    'The complete offline archive contains the Git bundle and every local LFS object. A bundle alone '
    'does not contain model tensors. Preserve the complete archive before terminating the pod.\n\n'
    'Current findings and limitations are in research_progress.md and paper_working_draft.md. Neither '
    'is a submission-ready paper. GitHub push status is recorded separately after the actual attempt.\n')

for module in ['day5_report','day6_diagnostic_report','day7_multinli_report','day9_routing_report',
               'day8_fixed_memory_report','day10_mechanism_report','day12_capacity_report',
               'day13_evidence_audit','day13_progress_report','day14_routing_report']:
    command([sys.executable,'-m','experiments.'+module])

with open('environment/wrap_pip_freeze.txt','w') as f:command([sys.executable,'-m','pip','freeze'],stdout=f)
Path('environment/wrap_runtime.txt').write_text(sys.version+'\n'+
    subprocess.check_output(['git','lfs','version'],text=True)+'\nUTC '+now()+'\n')
checkpoints=[p for p in Path('results').rglob('*') if p.is_file() and 'checkpoint' in p.parts]
manifest={str(p):{'bytes':p.stat().st_size,'sha256':file_hash(p)} for p in checkpoints}
Path('results/checkpoint_preservation_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True))

command(['git','lfs','install','--local'])
command(['git','lfs','track','*.pt','*.safetensors'])
ignore=Path('.gitignore')
ignore.write_text('\n'.join(line for line in ignore.read_text().splitlines()
    if line not in ['results/day*/checkpoint/','data/day7_cache/'])+'\n')
command(['git','add','-A'])
command(['git','commit','-m','Preserve completed research evidence and full learner state with Git LFS'])
command(['git','lfs','fsck'])
snapshot=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
env=os.environ.copy();env['GIT_TERMINAL_PROMPT']='0';env['GCM_INTERACTIVE']='never'
with open('logs/wrap_github_push.txt','w') as f:
    try:
        pushed=subprocess.run(['git','push','--set-upstream','origin','day5-causal-audit'],env=env,
            stdout=f,stderr=subprocess.STDOUT,timeout=600)
        push_code=pushed.returncode
    except subprocess.TimeoutExpired:
        push_code=124;f.write('\nPush timed out; remote success is not established.\n')
status={'timestamp_utc':now(),'snapshot_commit':snapshot,'github_push_returncode':push_code,
        'branch':'day5-causal-audit','checkpoint_files':len(checkpoints),
        'checkpoint_bytes':sum(p.stat().st_size for p in checkpoints),
        'full_state_storage':'Git LFS tensors plus ordinary Git source/results/cache',
        'study_coverage':coverage,'unlaunched_live_jobs':len(remaining)}
Path('notes/preservation_status.json').write_text(json.dumps(status,indent=2))
command(['git','add','logs/wrap_github_push.txt','notes/preservation_status.json'])
command(['git','commit','-m','Record verified full-state preservation and GitHub push outcome'])
if push_code==0:
    with open('/workspace/mitosis_final_push_status.txt','w') as f:
        final_push=subprocess.run(['git','push','origin','day5-causal-audit'],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
    print('FINAL_STATUS_COMMIT_PUSH',final_push.returncode,flush=True)
else:
    print('GITHUB_PUSH_BLOCKED',push_code,flush=True)
    print(Path('logs/wrap_github_push.txt').read_text()[-2500:],flush=True)

bundle=Path('/workspace/mitosis-research-final.bundle')
command(['git','bundle','create',str(bundle),'day5-causal-audit'])
command(['git','bundle','verify',str(bundle)])
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
paths=subprocess.check_output(['git','ls-files','-z']).decode().split('\0')
with zipfile.ZipFile('/workspace/mitosis-source-results-final.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in paths:
        if name and 'checkpoint' not in Path(name).parts:z.write(name,name)

recovery='''Complete research state: Git history plus Git LFS tensors.
Unzip this archive into a new directory. Install Git and Git LFS from standard packages.
Run:
  GIT_LFS_SKIP_SMUDGE=1 git clone -b day5-causal-audit mitosis-research-final.bundle mitosis-interference
  cd mitosis-interference
  git lfs install --local
  cp -a ../git-lfs-objects/. .git/lfs/objects/
  git lfs checkout
  git lfs fsck
  git status --short
The Git bundle alone contains LFS pointers, not the actual learner tensors.
Authenticate GitHub in your own terminal if the saved push was blocked, then run:
  git remote set-url origin https://github.com/anitusiruk/mitosis-interference.git
  git push --set-upstream origin day5-causal-audit
The remote-setting command is for the offline bundle clone, whose origin initially points at the bundle.
'''
archive=Path('/workspace/mitosis-research-complete.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
    z.write(bundle,bundle.name);z.writestr('RECOVERY.txt',recovery)
    for p in Path('.git/lfs/objects').rglob('*'):
        if p.is_file():z.write(p,'git-lfs-objects/'+str(p.relative_to('.git/lfs/objects')))
checks={p.name:{'bytes':p.stat().st_size,'sha256':file_hash(p)}
        for p in [bundle,archive,Path('/workspace/mitosis-source-results-final.zip')]}
github_head=None
if push_code==0:
    remote=subprocess.run(['git','ls-remote','origin','refs/heads/day5-causal-audit'],env=env,capture_output=True,text=True,timeout=90)
    if remote.returncode==0 and remote.stdout.strip():github_head=remote.stdout.split()[0]
Path('/workspace/mitosis-preservation-checksums.json').write_text(json.dumps({'final_commit':head,
    'github_push_returncode':push_code,'github_ref_verified':github_head==head,'files':checks},indent=2))
assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip(),'Uncommitted project changes remain'
print('WRAP_COMPLETE',head,'FULL_ARCHIVE_BYTES',archive.stat().st_size,'PUSH_RETURN_CODE',push_code,
      'GITHUB_HEAD_VERIFIED',github_head==head,flush=True)
