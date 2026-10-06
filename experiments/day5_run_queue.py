"""One GPU job at a time, with explicit experiment/deadline/exit-code records."""
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys

jobs=[('banking','private','cau',True),('banking','shared','cau',False),
      ('amazon','private','cau',True),('amazon','shared','cau',False),
      ('banking','private','single',False),('amazon','private','single',False)]
launch_cutoff=datetime.fromisoformat('2026-10-06T03:20:00+00:00')
status_path=Path('logs/day5_queue_status.json')
statuses=[]
for regime,architecture,policy,audit in jobs:
    if datetime.now(timezone.utc)>=launch_cutoff:
        statuses.append({'regime':regime,'architecture':architecture,'policy':policy,'status':'not_launched_deadline'})
        status_path.write_text(json.dumps(statuses,indent=2))
        continue
    name=f'day5_{regime}_{architecture}_{policy}_seed2026'
    out=Path('results')/name
    if out.exists():
        raise RuntimeError(f'Refusing to overwrite {out}')
    cmd=[sys.executable,'-u','-m','experiments.day5_causal_recurrence','--regime',regime,
         '--architecture',architecture,'--policy',policy,'--seed','2026','--output',str(out),
         '--deadline-utc','2026-10-06T03:25:00+00:00']
    if audit:cmd.append('--component-audit')
    status={'name':name,'command':cmd,'start_utc':datetime.now(timezone.utc).isoformat(),'status':'running'}
    statuses.append(status)
    status_path.write_text(json.dumps(statuses,indent=2))
    print('START',name,flush=True)
    with (Path('logs')/(name+'.txt')).open('w') as log:
        result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
    status.update(returncode=result.returncode,end_utc=datetime.now(timezone.utc).isoformat(),
                  status='completed' if result.returncode==0 else 'failed')
    status_path.write_text(json.dumps(statuses,indent=2))
    print('END',name,'returncode',result.returncode,flush=True)
    if result.returncode!=0:
        print('STOPPING_QUEUE_AFTER_FAILURE',name,flush=True)
        break
