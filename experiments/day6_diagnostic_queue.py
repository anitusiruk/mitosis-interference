"""Sequential frozen diagnostic batch; seed-level replication, no retuning."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

os.environ['OMP_NUM_THREADS']='8'
os.environ['TOKENIZERS_PARALLELISM']='false'
cutoff=datetime.fromisoformat('2026-10-06T03:20:00+00:00')
while datetime.now(timezone.utc)<cutoff:
    path=Path('logs/day5_head_only_queue_status.json')
    if path.exists():
        previous=json.loads(path.read_text())
        if previous and previous[-1]['status']=='failed':raise RuntimeError('Head-only queue failed; inspect before progressing')
        if len(previous)==2 and all(r['status']=='completed' for r in previous):break
    time.sleep(15)
else:raise RuntimeError('Diagnostic batch not launched before cutoff')

records=[]
for seed in [2027,2028,2029,2030,2031]:
    for order in ['canonical','b_first']:
        for regime in ['banking','amazon']:
            for architecture,policy in [('private','cau'),('head_only','cau'),('private','single'),('head_only','single')]:
                if datetime.now(timezone.utc)>=cutoff:break
                name=f'day6_{regime}_{architecture}_{policy}_seed{seed}_{order}'
                cmd=[sys.executable,'-u','-m','experiments.day6_frozen_diagnostics','--regime',regime,
                     '--architecture',architecture,'--policy',policy,'--seed',str(seed),'--order',order,
                     '--output',f'results/{name}','--deadline-utc','2026-10-06T03:25:00+00:00']
                row={'name':name,'command':cmd,'status':'running','start_utc':datetime.now(timezone.utc).isoformat()}
                records.append(row)
                Path('logs/day6_queue_status.json').write_text(json.dumps(records,indent=2))
                with open(f'logs/{name}.txt','w') as log:result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
                row.update(status='completed' if result.returncode==0 else 'failed',returncode=result.returncode,
                           end_utc=datetime.now(timezone.utc).isoformat())
                Path('logs/day6_queue_status.json').write_text(json.dumps(records,indent=2))
                print('DIAGNOSTIC',len(records),name,row['status'],flush=True)
                if result.returncode:raise RuntimeError(f'Diagnostic failed: {name}')
print('DIAGNOSTIC_QUEUE_FINISHED',len(records),flush=True)
