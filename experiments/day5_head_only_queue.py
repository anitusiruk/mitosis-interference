"""Follow the main queue with the two predeclared head-only controls."""
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys
import time

cutoff=datetime.fromisoformat('2026-10-06T03:20:00+00:00')
while datetime.now(timezone.utc)<cutoff:
    main=json.loads(Path('logs/day5_queue_status.json').read_text())
    if main and main[-1]['status']=='failed':
        raise RuntimeError('Main queue failed; inspect it before running later controls')
    if len(main)==6 and all(r['status']=='completed' for r in main):break
    time.sleep(15)
else:
    raise RuntimeError('Head-only controls not launched before deadline cutoff')

records=[]
for regime in ['banking','amazon']:
    if datetime.now(timezone.utc)>=cutoff:break
    name=f'day5_{regime}_head_only_cau_seed2026'
    cmd=[sys.executable,'-u','-m','experiments.day5_head_only_recurrence','--regime',regime,
        '--architecture','head_only','--policy','cau','--seed','2026','--output',f'results/{name}',
        '--deadline-utc','2026-10-06T03:25:00+00:00']
    record={'name':name,'command':cmd,'status':'running','start_utc':datetime.now(timezone.utc).isoformat()}
    records.append(record)
    Path('logs/day5_head_only_queue_status.json').write_text(json.dumps(records,indent=2))
    with open(f'logs/{name}.txt','w') as log:
        result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
    record.update(returncode=result.returncode,status='completed' if result.returncode==0 else 'failed',
                  end_utc=datetime.now(timezone.utc).isoformat())
    Path('logs/day5_head_only_queue_status.json').write_text(json.dumps(records,indent=2))
    print('HEAD_ONLY_CONTROL',name,record['status'],flush=True)
    if result.returncode!=0:break
