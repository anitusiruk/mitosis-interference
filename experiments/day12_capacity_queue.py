"""Larger single-package baseline near three original packages in storage."""
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
    p=Path('logs/day10_queue_status.json')
    if p.exists():
        r=json.loads(p.read_text())
        if r and r[-1]['status']=='failed':raise RuntimeError('Scoring ablation failure requires inspection')
        if len(r)==12 and all(x['status']=='completed' for x in r):break
    pid=int(Path('logs/day10_queue_pid.txt').read_text())
    try:os.kill(pid,0)
    except ProcessLookupError:raise RuntimeError('Scoring queue exited before all jobs; inspect its log')
    time.sleep(15)
else:raise RuntimeError('Capacity baseline launch cutoff reached')
records=[]
for seed in [2026,2027,2028,2029,2030,2031]:
    for order in ['canonical'] if seed==2026 else ['canonical','b_first']:
        if datetime.now(timezone.utc)>=cutoff:break
        name=f'day12_banking_private_single_rank96_seed{seed}_{order}'
        cmd=[sys.executable,'-u','-m','experiments.day12_capacity_recurrence','--regime','banking',
             '--architecture','private','--policy','single','--seed',str(seed),'--order',order,
             '--output',f'results/{name}','--deadline-utc','2026-10-06T03:25:00+00:00']
        row={'name':name,'command':cmd,'status':'running','start_utc':datetime.now(timezone.utc).isoformat()}
        records.append(row);Path('logs/day12_queue_status.json').write_text(json.dumps(records,indent=2))
        with open(f'logs/{name}.txt','w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
        row.update(returncode=r.returncode,status='completed' if r.returncode==0 else 'failed',
            end_utc=datetime.now(timezone.utc).isoformat())
        Path('logs/day12_queue_status.json').write_text(json.dumps(records,indent=2))
        print('CAPACITY',len(records),name,row['status'],flush=True)
        if r.returncode:raise RuntimeError(f'Capacity job failed: {name}')
print('CAPACITY_QUEUE_FINISHED',len(records),flush=True)
