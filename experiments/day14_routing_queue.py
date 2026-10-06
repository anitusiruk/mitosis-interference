"""One sequential auxiliary routing extension after the frozen live studies."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

os.environ['OMP_NUM_THREADS']='8';os.environ['TOKENIZERS_PARALLELISM']='false'
cutoff=datetime.fromisoformat('2026-10-06T03:23:00+00:00')
while datetime.now(timezone.utc)<cutoff:
    ready=False
    running=False
    for day,expected in [(8,44),(10,12),(12,11)]:
        path=Path(f'logs/day{day}_queue_status.json')
        r=json.loads(path.read_text()) if path.exists() else []
        if r and r[-1]['status']=='failed':raise RuntimeError('Prior study failed; inspect before auxiliary inference')
        running=running or any(x['status']=='running' for x in r)
    pid=int(Path('logs/tonight_balanced_pid.txt').read_text())
    process=Path(f'/proc/{pid}')
    if not process.exists():ready=True
    elif (process/'stat').read_text().split()[2]=='Z':ready=True
    elif not (process/'cmdline').read_bytes():ready=True
    if ready and running:raise RuntimeError('Dispatcher exited with a running record; inspect before GPU inference')
    if ready:break
    time.sleep(15)
else:raise RuntimeError('Fixed-memory auxiliary scope not launched before cutoff')
with open('logs/day14_fixed_memory_routing.txt','w') as log:
    r=subprocess.run([sys.executable,'-u','-m','experiments.day14_fixed_memory_routing'],stdout=log,stderr=subprocess.STDOUT)
if r.returncode:raise RuntimeError('Fixed-memory auxiliary inference failed; preserve log and inspect')
print('FIXED_MEMORY_ROUTING_QUEUE_FINISHED',flush=True)
