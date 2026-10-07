"""Preserve the existing research state after the user's shutdown request."""
import ast
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path('/workspace/mitosis-interference')
AUX = Path('/workspace/mitosis-static-tuning')
STAGE = Path('/workspace/mitosis-day15-stage')
BRANCH = 'day5-causal-audit'
AUX_BRANCH = 'day17-static-tuning-20261006'
ENV = os.environ.copy()
ENV.update(GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1')
os.chdir(ROOT)

def now(): return datetime.now(timezone.utc).isoformat()
def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(8*1024*1024), b''): h.update(b)
    return h.hexdigest()
def read(args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, env=ENV, text=True, timeout=90).strip()
def run(args, cwd=ROOT, log=None):
    print('RUN', ' '.join(args), flush=True)
    return subprocess.run(args, cwd=cwd, env=ENV, stdin=subprocess.DEVNULL,
                          stdout=log, stderr=subprocess.STDOUT if log else None).returncode
def write(name, data):
    Path(name).write_text(json.dumps(data, indent=2)+chr(10))
def push(message, cwd=ROOT, branch=BRANCH):
    assert run(['git','add','-A'], cwd)==0
    if read(['git','status','--porcelain'], cwd):
        assert run(['git','commit','-m',message], cwd)==0
    assert run(['git','push','origin',branch], cwd)==0
    head=read(['git','rev-parse','HEAD'], cwd)
    assert read(['git','ls-remote','origin','refs/heads/'+branch], cwd).split()[0]==head
    assert not read(['git','status','--porcelain'], cwd)
    return head

# No scientific worker is relaunched. Acquire the existing worker locks.
locks=[]
for name in ['mitosis-restart-worker.lock','mitosis-static-tuning-worker.lock']:
    f=open(ROOT.parent/name,'a');fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);locks.append(f)
active=[]
for p in Path('/proc').iterdir():
    if not p.name.isdigit() or int(p.name)==os.getpid(): continue
    try: args=(p/'cmdline').read_bytes().replace(bytes([0]),b' ').decode()
    except (OSError,UnicodeError): continue
    if any(s in args for s in ['-m experiments.day','integrate_saved_branches_v2.py',
                              'finalize_evidence_quality_v3.py','day20_complete_frozen_diagnostics.py']):
        active.append({'pid':int(p.name),'command':args})
assert not active, active
gpu=read(['nvidia-smi','--query-compute-apps=pid,used_memory','--format=csv,noheader'])
assert not gpu, gpu
for cwd, branch in [(ROOT,BRANCH),(AUX,AUX_BRANCH)]:
    assert read(['git','remote','get-url','origin'],cwd)=='https://github.com/anitusiruk/mitosis-interference.git'
    assert read(['git','branch','--show-current'],cwd)==branch
    assert read(['git','rev-parse','HEAD'],cwd)==read(['git','ls-remote','origin','refs/heads/'+branch],cwd).split()[0]
assert not read(['git','status','--porcelain'])

# Preserve Jupyter's regenerated preview copy without discarding it.
aux_status=read(['git','status','--porcelain','--untracked-files=all'],AUX).splitlines()
for line in aux_status:
    assert line.startswith('?? figures/extended_audit/.ipynb_checkpoints/'), line
    p=AUX/line[3:];assert p.is_file()
    target=AUX/'notes/operational_recovery_20261007'/('jupyter_preview_'+p.name)
    target.parent.mkdir(exist_ok=True);assert not target.exists()
    digest=sha(p);p.rename(target);assert sha(target)==digest
aux_head=push('Preserve Jupyter preview state before requested pod shutdown',AUX,AUX_BRANCH)
assert run(['git','merge','--no-ff','--no-edit',AUX_BRANCH])==0
assert run(['git','lfs','checkout'])==0

worker=ROOT/'experiments/day15_16_research_worker.py'
assert sha(worker)=='11f7493d9003c65d307db1830c5ec76c591c9e137cdebbd9387e67a11a60e640'
helper=ROOT/'experiments/finalize_github_save.py'
source=helper.read_text()
old='run(["git", "config", "--local", "credential.https://github.com.helper", ""])'
new='run(["git", "config", "--local", "--replace-all", "credential.https://github.com.helper", ""])'
assert source.count(old)==1
helper.write_text(source.replace(old,new))

recovery=ROOT/'notes/operational_recovery_20261007';recovery.mkdir(exist_ok=True)
copied={}
for p in sorted(STAGE.iterdir()):
    if p.is_file() and p.suffix in {'.py','.log'} and not p.name.startswith('CABLE_'):
        target=recovery/p.name
        assert not target.exists();shutil.copyfile(p,target);copied[str(target.relative_to(ROOT))]=sha(target)
for p in sorted(ROOT.parent.glob('mitosis_day*.log')):
    target=recovery/p.name
    assert not target.exists();shutil.copyfile(p,target);copied[str(target.relative_to(ROOT))]=sha(target)
review=STAGE/'cable_source_compatibility_20261007.md'
if review.exists(): shutil.copyfile(review,ROOT/'notes'/review.name)
z=STAGE/'author_source_inspection_20261007.zip'
if z.exists():
    import zipfile
    with zipfile.ZipFile(z) as archive: provenance=json.loads(archive.read('source_manifest.json'))
    provenance.update(author_code_redistributed=False,review_added_after_development_outcomes=True)
    write('notes/cable_author_source_inspection_20261007.json',provenance)
shutil.copyfile(Path(__file__),ROOT/'experiments/wrap_stop_and_save_20261007.py')

status_path=ROOT/'notes/day15_16_execution_status.json'
state=json.loads(status_path.read_text())
assert all(r['status']=='completed' for r in state['jobs'])
completed={r['name'] for r in state['jobs']}
remaining=[f'day15_{regime}_private_cau_seed{seed}_{order}_weight_moments'
           for seed in range(2027,2032) for order in ['canonical','b_first']
           for regime in ['banking','amazon']
           if f'day15_{regime}_private_cau_seed{seed}_{order}_weight_moments' not in completed]
write('notes/pod_shutdown_request_20261007.json',{
    'utc':now(),'reason':'User requested immediate preservation and stopping long remaining jobs',
    'research_processes_running':False,'gpu_compute_processes_running':False,
    'follow_on_workers_expired_and_not_restarted':True,'remaining_frozen_jobs':remaining,
    'completed_bert_jobs':sum(r['study']==16 for r in state['jobs']),
    'completed_factorial_jobs':sum(r['study']==15 for r in state['jobs']),
    'original_scientific_worker_unchanged':True,'auxiliary_branch_head':aux_head,
    'backup_repair':'Use git config --replace-all for an existing multivalue credential helper',
    'operational_sources_and_logs_sha256':copied,'backup_verification_pending':True})

# Finish only the inexpensive, derived reports and audit checks.
qc_source=STAGE/'finalize_evidence_quality_v3.py'
assert sha(qc_source)=='8213e4ceff19add493f4c252a046f822f54ac8897ccf4c5b76ca110d36bd660a'
tree=ast.parse(qc_source.read_text())
payload=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
             and any(isinstance(t,ast.Name) and t.id=='FILES' for t in n.targets))
for name,text in payload.items():
    p=ROOT/name
    if p.exists(): assert p.read_text()==text,name
    else: p.write_text(text)
checker=STAGE/'factorial_receipt_audit.py'
assert sha(checker)=='be2bc41fe2af7f81792bb240037dd1abc8259b966d076a7d0d5e08d14d338521'
shutil.copyfile(checker,ROOT/'experiments/day18_factorial_receipt_audit.py')
codes={}
commands=[('factorial_report',[sys.executable,'-u','-m','experiments.day15_moment_report']),
          ('manuscript',[sys.executable,'-u','-m','experiments.day17_manuscript_refresh']),
          ('figures',[sys.executable,'-u','-m','experiments.day17_evidence_figures']),
          ('factorial_integrity',[sys.executable,'-u','-m','experiments.day18_factorial_receipt_audit',
             '--root',str(ROOT),'--output','notes/factorial_receipt_integrity_final.json']),
          ('retention_gate',[sys.executable,'-u','-m','experiments.day18_retention_integrity']),
          ('retention',[sys.executable,'-u','-m','experiments.day18_deployment_retention']),
          ('editorial',[sys.executable,'-u','-m','experiments.day18_evidence_caveats'])]
for label,args in commands:
    with (ROOT/'logs'/('shutdown_20261007_'+label+'.txt')).open('x') as log:
        codes[label]=run(args,log=log)
    print('DERIVED_FINISH',label,codes[label],flush=True)

manifest={}
for p in sorted((ROOT/'results').rglob('*')):
    if p.is_file() and 'checkpoint' in p.parts:
        manifest[str(p.relative_to(ROOT))]={'bytes':p.stat().st_size,'sha256':sha(p)}
write('results/checkpoint_preservation_manifest.json',manifest)
preservation=json.loads((ROOT/'notes/preservation_status.json').read_text())
preservation.update(checkpoint_files=len(manifest),checkpoint_bytes=sum(v['bytes'] for v in manifest.values()),
                    new_snapshot_push_pending=True,github_ref_verified=False,remote_checkpoints_sha256_verified=False)
write('notes/preservation_status.json',preservation)
write('notes/shutdown_evidence_finish_20261007.json',{
    'utc':now(),'derived_command_returncodes':codes,'new_scientific_training_launched':False,
    'complete_factorial_observers':sum(r['study']==15 for r in state['jobs']),
    'planned_factorial_observers':20,'remaining_jobs':remaining,'figure_visual_review_pending':True})
push('Preserve combined research state and finish derived evidence before pod shutdown')

backup_log=STAGE/'shutdown_remote_verification_20261007.log'
with backup_log.open('x') as log:
    code=run([sys.executable,'-u','-m','experiments.finalize_github_save'],log=log)
assert code==0,'Remote verification failed: '+str(backup_log)
receipt=json.loads((ROOT/'notes/github_save_verification.json').read_text())
assert receipt['all_current_lfs_sha256_verified']
snapshot=receipt['preserved_snapshot_commit']
preservation.update(new_snapshot_push_pending=False,github_ref_verified=True,
    remote_checkpoints_sha256_verified=True,github_push_returncode=0,
    last_successful_github_snapshot_commit=snapshot,last_successful_github_save_verified_utc=receipt['verified_utc'])
write('notes/preservation_status.json',preservation)
state.update(github_save_pending=False,github_save_verified=True,failed=False,
             complete=len(state['jobs'])==40,administratively_stopped=True,
             stopped_by_user=True,remaining_jobs=remaining,generated_utc=now())
write(status_path,state)
request=json.loads((ROOT/'notes/pod_shutdown_request_20261007.json').read_text())
request.update(backup_verification_pending=False,all_current_checkpoint_objects_remotely_verified=True,
               verified_snapshot_commit=snapshot,safe_to_stop_pod=True,verified_utc=now())
write('notes/pod_shutdown_request_20261007.json',request)
shutil.copyfile(backup_log,recovery/backup_log.name)
changed=read(['git','diff','--name-only',snapshot,'HEAD']).splitlines()
changed+=read(['git','diff','--name-only']).splitlines()
assert not any('checkpoint' in Path(p).parts or Path(p).suffix in {'.pt','.safetensors'} for p in changed)
final=push('Record verified complete project preservation and safe pod shutdown')
assert run(['git','merge-base','--is-ancestor',aux_head,final])==0
assert not read(['git','status','--porcelain'],AUX)
assert not read(['nvidia-smi','--query-compute-apps=pid,used_memory','--format=csv,noheader'])
print('POD_SAFE_TO_STOP',final,'CHECKPOINT_FILES',len(manifest),'REMOTE_OBJECTS',receipt['unique_lfs_objects_verified'],
      'FACTORIAL_COMPLETE',sum(r['study']==15 for r in state['jobs']),'REMAINING',len(remaining),'QC_CODES',codes,flush=True)

