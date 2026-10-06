"""Mechanistic ranking pilot after fixed-memory sensitivity."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

os.environ['OMP_NUM_THREADS']='8';os.environ['TOKENIZERS_PARALLELISM']='false'
cutoff=datetime.fromisoformat('2026-10-06T03:20:00+00:00')
while datetime.now(timezone.utc)<cutoff:
    path=Path('logs/day8_queue_status.json')
    if path.exists():
        r=json.loads(path.read_text())
        if r and r[-1]['status']=='failed':raise RuntimeError('Fixed-memory failure requires inspection')
        if len(r)==44 and all(x['status']=='completed' for x in r):break
    pid=int(Path('logs/day8_queue_pid.txt').read_text())
    try:os.kill(pid,0)
    except ProcessLookupError:raise RuntimeError('Fixed-memory queue exited before all jobs; inspect its log')
    time.sleep(15)
else:raise RuntimeError('Pre-update scoring pilot launch cutoff reached')
with open('logs/day10_initial_loss_integrity.txt','w') as log:
    r=subprocess.run([sys.executable,'-u','-m','experiments.day10_initial_loss_integrity'],stdout=log,stderr=subprocess.STDOUT)
if r.returncode:raise RuntimeError('Pre-update ranking integrity failed; preserve log and halt')
print('INITIAL_LOSS_INTEGRITY_PASS',flush=True)
records=[]
for seed in [2026,2027,2028]:
    for regime in ['banking','amazon']:
        for architecture in ['private','head_only']:
            if datetime.now(timezone.utc)>=cutoff:break
            name=f'day10_{regime}_{architecture}_cau_seed{seed}_canonical_initial_loss'
            cmd=[sys.executable,'-u','-m','experiments.day10_initial_loss_recurrence','--regime',regime,
                 '--architecture',architecture,'--policy','cau','--seed',str(seed),'--order','canonical',
                 '--output',f'results/{name}','--deadline-utc','2026-10-06T03:25:00+00:00']
            row={'name':name,'command':cmd,'status':'running','start_utc':datetime.now(timezone.utc).isoformat()}
            records.append(row);Path('logs/day10_queue_status.json').write_text(json.dumps(records,indent=2))
            with open(f'logs/{name}.txt','w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
            row.update(returncode=r.returncode,status='completed' if r.returncode==0 else 'failed',
                end_utc=datetime.now(timezone.utc).isoformat())
            Path('logs/day10_queue_status.json').write_text(json.dumps(records,indent=2))
            print('INITIAL_LOSS',len(records),name,row['status'],flush=True)
            if r.returncode:raise RuntimeError(f'Pre-update ranking job failed: {name}')
print('INITIAL_LOSS_QUEUE_FINISHED',len(records),flush=True)
