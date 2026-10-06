"""Third-regime batch after Day 6; no concurrent GPU timing contamination."""
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
    path=Path('logs/day6_queue_status.json')
    if path.exists():
        rows=json.loads(path.read_text())
        if rows and rows[-1]['status']=='failed':raise RuntimeError('Day-6 diagnostic failure requires inspection')
        if len(rows)==80 and all(r['status']=='completed' for r in rows):break
    time.sleep(15)
else:raise RuntimeError('MultiNLI queue did not start before cutoff')

with open('logs/day7_multinli_integrity.txt','w') as log:
    checked=subprocess.run([sys.executable,'-u','-m','experiments.day7_multinli_integrity'],stdout=log,stderr=subprocess.STDOUT)
if checked.returncode:raise RuntimeError('MultiNLI data integrity failed; preserve log and halt')
print('MULTINLI_DATA_VALIDATION_PASS',flush=True)

records=[]
for seed in [2026,2027,2028]:
    for condition in ['sharp','blurry']:
        for architecture,policy in [('private','cau'),('head_only','cau'),('private','single'),('head_only','single')]:
            if datetime.now(timezone.utc)>=cutoff:break
            name=f'day7_multinli_{architecture}_{policy}_seed{seed}_{condition}'
            cmd=[sys.executable,'-u','-m','experiments.day7_multinli_recurrence','--regime','multinli',
                '--architecture',architecture,'--policy',policy,'--seed',str(seed),'--boundary-condition',condition,
                '--output',f'results/{name}','--deadline-utc','2026-10-06T03:25:00+00:00']
            row={'name':name,'command':cmd,'status':'running','start_utc':datetime.now(timezone.utc).isoformat()}
            records.append(row)
            Path('logs/day7_queue_status.json').write_text(json.dumps(records,indent=2))
            with open(f'logs/{name}.txt','w') as log:result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
            row.update(status='completed' if result.returncode==0 else 'failed',returncode=result.returncode,
                end_utc=datetime.now(timezone.utc).isoformat())
            Path('logs/day7_queue_status.json').write_text(json.dumps(records,indent=2))
            print('MULTINLI',len(records),name,row['status'],flush=True)
            if result.returncode:raise RuntimeError(f'MultiNLI job failed: {name}')
print('MULTINLI_QUEUE_FINISHED',len(records),flush=True)
