"""Execute frozen transfer/causal diagnostics and push every preserved attempt."""
from datetime import datetime,timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT=Path('/workspace/mitosis-interference')
os.chdir(ROOT)
ENV=os.environ.copy()
ENV.update(OMP_NUM_THREADS='8',TOKENIZERS_PARALLELISM='false',GIT_TERMINAL_PROMPT='0',GH_PROMPT_DISABLED='1')
ENV['MITOSIS_MODEL_REVISION']=json.loads(Path('notes/restart_20261006_preflight.json').read_text())['backbone_revision']
BRANCH='day5-causal-audit'
LAUNCH_CUTOFF=datetime.fromisoformat('2026-10-07T03:00:00+00:00')
TRAINING_DEADLINE='2026-10-07T03:15:00+00:00'


def now():return datetime.now(timezone.utc).isoformat()


def read(command):return subprocess.check_output(command,env=ENV,text=True,timeout=90).strip()


def command(arguments,log=None):
    print('RUN',' '.join(arguments),flush=True)
    return subprocess.run(arguments,env=ENV,stdin=subprocess.DEVNULL,
                          stdout=log,stderr=subprocess.STDOUT if log else None).returncode


def write(path,data):
    p=Path(path);temporary=p.with_suffix(p.suffix+'.tmp')
    temporary.write_text(json.dumps(data,indent=2)+'\n');temporary.replace(p)


def preserve():
    manifest={}
    for path in sorted(Path('results').rglob('*')):
        if path.is_file() and 'checkpoint' in path.parts:
            digest=hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda:stream.read(8*1024*1024),b''):digest.update(block)
            manifest[str(path)]={'bytes':path.stat().st_size,'sha256':digest.hexdigest()}
    write('results/checkpoint_preservation_manifest.json',manifest)
    preservation=json.loads(Path('notes/preservation_status.json').read_text())
    preservation.update(checkpoint_files=len(manifest),checkpoint_bytes=sum(x['bytes'] for x in manifest.values()),
                        new_snapshot_push_pending=True,github_ref_verified=False,
                        remote_checkpoints_sha256_verified=False)
    write('notes/preservation_status.json',preservation)
    if command(['git','add','-A']):raise RuntimeError('Git staging failed')
    if read(['git','status','--porcelain']):
        if command(['git','commit','-m','Preserve frozen architecture and weight-state audit progress']):
            raise RuntimeError('Git progress commit failed')
    if command(['git','push','origin',BRANCH]):raise RuntimeError('GitHub progress push failed; local state preserved')
    head=read(['git','rev-parse','HEAD'])
    if read(['git','ls-remote','origin','refs/heads/'+BRANCH]).split()[0]!=head:
        raise RuntimeError('GitHub progress ref does not match')
    if read(['git','status','--porcelain']):raise RuntimeError('Unexpected uncommitted state')
    print('DIAGNOSTIC_PROGRESS_PUSHED',head,flush=True)


lock=open('/workspace/mitosis-restart-worker.lock','a')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert read(['git','branch','--show-current'])==BRANCH
assert read(['git','remote','get-url','origin'])=='https://github.com/anitusiruk/mitosis-interference.git'
assert not read(['git','status','--porcelain'])
assert read(['gh','api','repos/anitusiruk/mitosis-interference','--jq','.permissions.push'])=='true'
records=[];failed=False
jobs=[]
for seed in range(2027,2032):
    for order in ['canonical','b_first']:
        for architecture in ['private','head_only']:
            name=f'day16_banking_{architecture}_seed{seed}_{order}_bert'
            jobs.append((name,'experiments.day16_bert_allocation',
                         ['--architecture',architecture,'--seed',str(seed),'--order',order],16))
for seed in range(2027,2032):
    for order in ['canonical','b_first']:
        for regime in ['banking','amazon']:
            name=f'day15_{regime}_private_cau_seed{seed}_{order}_weight_moments'
            jobs.append((name,'experiments.day15_weight_moment_recurrence',
                         ['--regime',regime,'--seed',str(seed),'--order',order],15))
status=Path('notes/day15_16_execution_status.json')
if status.exists():
    records=json.loads(status.read_text())['jobs']
    if any(r['status']!='completed' for r in records):
        raise RuntimeError('Preserved incomplete/failed diagnostic attempt requires inspection')
for name,module,args,study in jobs:
    old=[r for r in records if r['name']==name]
    if old:
        assert len(old)==1 and old[0]['status']=='completed'
        assert json.loads(Path('results',name,'summary.json').read_text())['status']=='completed'
        if study==15:assert json.loads(Path('results',name,'observer_verification.json').read_text())['status']=='passed'
        continue
    if datetime.now(timezone.utc)>=LAUNCH_CUTOFF:
        print('DIAGNOSTIC_LAUNCH_CUTOFF',now(),flush=True);break
    output=Path('results')/name
    assert not output.exists(),'Refusing to overwrite '+str(output)
    arguments=[sys.executable,'-u','-m',module,*args,'--output',str(output),'--deadline-utc',TRAINING_DEADLINE]
    row={'name':name,'study':study,'status':'running','started_utc':now(),'command':arguments}
    records.append(row);write(status,{'jobs':records,'planned_jobs':40,'generated_utc':now(),'github_save_pending':True})
    with Path('logs',name+'.txt').open('x') as log:code=command(arguments,log)
    row.update(returncode=code,finished_utc=now(),status='completed' if code==0 else 'failed')
    write(status,{'jobs':records,'planned_jobs':40,'generated_utc':now(),'github_save_pending':True})
    print('DIAGNOSTIC_JOB',name,row['status'],flush=True)
    report='experiments.day16_bert_report' if study==16 else 'experiments.day15_moment_report'
    report_log=Path('logs',name+'_report.txt')
    with report_log.open('x') as log:report_code=command([sys.executable,'-u','-m',report],log)
    if report_code:row['report_failed']=True
    write(status,{'jobs':records,'planned_jobs':40,'generated_utc':now(),'github_save_pending':True})
    with Path('logs',name+'_progress.txt').open('x') as log:
        progress_code=command([sys.executable,'-u','-m','experiments.day13_progress_report'],log)
    if progress_code:row['progress_report_failed']=True
    write(status,{'jobs':records,'planned_jobs':40,'generated_utc':now(),'github_save_pending':True})
    preserve()
    if code or report_code or progress_code:failed=True;break
preserve()
if command([sys.executable,'-u','-m','experiments.finalize_github_save']):
    raise RuntimeError('Diagnostic remote checkpoint roundtrip failed')
receipt=json.loads(Path('notes/github_save_verification.json').read_text())
assert receipt['all_current_lfs_sha256_verified']
preservation=json.loads(Path('notes/preservation_status.json').read_text())
preservation.update(github_push_returncode=0,github_ref_verified=True,new_snapshot_push_pending=False,
    remote_checkpoints_sha256_verified=True,last_successful_github_snapshot_commit=receipt['preserved_snapshot_commit'],
    last_successful_github_save_verified_utc=receipt['verified_utc'])
write('notes/preservation_status.json',preservation)
write(status,{'jobs':records,'planned_jobs':40,'generated_utc':now(),'github_save_pending':False,
              'github_save_verified':True,'failed':failed,'complete':len(records)==40 and not failed})
if command(['git','add','notes/preservation_status.json',str(status)]):raise RuntimeError('Final Git stage failed')
if command(['git','commit','-m','Record verified GitHub checkpoint preservation for frozen diagnostics']):
    raise RuntimeError('Final Git commit failed')
if command(['git','push','origin',BRANCH]):raise RuntimeError('Final Git push failed')
head=read(['git','rev-parse','HEAD'])
assert read(['git','ls-remote','origin','refs/heads/'+BRANCH]).split()[0]==head
assert not read(['git','status','--porcelain'])
print('DIAGNOSTIC_QUEUE_AND_GITHUB_SAVE_COMPLETE',head,'JOBS',len(records),'FAILED',failed,flush=True)
if failed:raise RuntimeError('Research discrepancy preserved; inspect before continuing')
