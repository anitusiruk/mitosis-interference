"""Fixed-memory sensitivity follows training and checkpoint-router queues."""
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
    path=Path('logs/day9_routing_status.json')
    if path.exists() and len(json.loads(path.read_text()))==110:break
    pid=int(Path('logs/day9_routing_pid.txt').read_text())
    try:os.kill(pid,0)
    except ProcessLookupError:raise RuntimeError('Auxiliary routing exited before all checkpoints; inspect its log')
    time.sleep(15)
else:raise RuntimeError('Fixed-memory extension not launched before cutoff')

with open('logs/day8_fixed_memory_integrity.txt','w') as log:
    r=subprocess.run([sys.executable,'-u','-m','experiments.day8_fixed_memory_integrity'],stdout=log,stderr=subprocess.STDOUT)
if r.returncode:raise RuntimeError('Fixed-memory integrity failed; preserve log and inspect before live outcomes')
print('FIXED_MEMORY_INTEGRITY_PASS',flush=True)
records=[]
for seed in [2026,2027,2028,2029,2030,2031]:
    for order in ['canonical'] if seed==2026 else ['canonical','b_first']:
        for regime in ['banking','amazon']:
            for architecture in ['private','head_only']:
                if datetime.now(timezone.utc)>=cutoff:break
                name=f'day8_{regime}_{architecture}_cau_seed{seed}_{order}_fixed512'
                cmd=[sys.executable,'-u','-m','experiments.day8_fixed_memory_recurrence','--regime',regime,
                     '--architecture',architecture,'--policy','cau','--seed',str(seed),'--order',order,
                     '--output',f'results/{name}','--deadline-utc','2026-10-06T03:25:00+00:00']
                row={'name':name,'command':cmd,'status':'running','start_utc':datetime.now(timezone.utc).isoformat()}
                records.append(row);Path('logs/day8_queue_status.json').write_text(json.dumps(records,indent=2))
                with open(f'logs/{name}.txt','w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
                row.update(returncode=r.returncode,status='completed' if r.returncode==0 else 'failed',
                    end_utc=datetime.now(timezone.utc).isoformat())
                Path('logs/day8_queue_status.json').write_text(json.dumps(records,indent=2))
                print('FIXED_MEMORY',len(records),name,row['status'],flush=True)
                if r.returncode:raise RuntimeError(f'Fixed-memory job failed: {name}')
print('FIXED_MEMORY_QUEUE_FINISHED',len(records),flush=True)
