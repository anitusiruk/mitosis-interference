"""Deadline-aware, sequential breadth-first dispatch of frozen diagnostics."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

os.environ['OMP_NUM_THREADS']='8'
os.environ['TOKENIZERS_PARALLELISM']='false'
CUTOFF=datetime.fromisoformat('2026-10-06T03:20:00+00:00')
DEADLINE='2026-10-06T03:25:00+00:00'

def launchable():return datetime.now(timezone.utc)<CUTOFF

def gate(module,log,extra=()):
    if not launchable():return False
    with open('logs/'+log,'w') as f:
        r=subprocess.run([sys.executable,'-u','-m',module,*extra],stdout=f,stderr=subprocess.STDOUT)
    if r.returncode:raise RuntimeError(f'Gate failed: {module}; inspect preserved log')
    print('GATE_PASS',module,flush=True)
    return True

def jobs(day,seed,order):
    if day==12:
        name=f'day12_banking_private_single_rank96_seed{seed}_{order}'
        return [(name,'experiments.day12_capacity_recurrence','banking','private','single')]
    suffix='fixed512' if day==8 else 'initial_loss'
    module=f'experiments.day{day}_'+('fixed_memory_recurrence' if day==8 else 'initial_loss_recurrence')
    return [(f'day{day}_{regime}_{arch}_cau_seed{seed}_{order}_{suffix}',module,regime,arch,'cau')
            for regime in ['banking','amazon'] for arch in ['private','head_only']]

def run(day,seed,order):
    path=Path(f'logs/day{day}_queue_status.json')
    records=json.loads(path.read_text()) if path.exists() else []
    for name,module,regime,arch,policy in jobs(day,seed,order):
        if not launchable():return False
        if (Path('results')/name).exists():raise RuntimeError('Refusing to overwrite '+name)
        cmd=[sys.executable,'-u','-m',module,'--regime',regime,'--architecture',arch,
             '--policy',policy,'--seed',str(seed),'--order',order,'--output',f'results/{name}',
             '--deadline-utc',DEADLINE]
        row=dict(name=name,command=cmd,status='running',start_utc=datetime.now(timezone.utc).isoformat(),
                 dispatcher='tonight_balanced_queue')
        records.append(row);path.write_text(json.dumps(records,indent=2))
        with open(f'logs/{name}.txt','w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
        status='failed'
        if r.returncode==0:
            summary=json.loads((Path('results')/name/'summary.json').read_text())
            status=summary['status']
        row.update(status=status,returncode=r.returncode,end_utc=datetime.now(timezone.utc).isoformat())
        path.write_text(json.dumps(records,indent=2))
        print('BALANCED',day,len(records),name,status,flush=True)
        if status=='failed':raise RuntimeError('Trajectory failed: '+name)
        if status!='completed':return False
    return True

def main():
    while launchable():
        path=Path('logs/day7_queue_status.json')
        if path.exists():
            r=json.loads(path.read_text())
            if r and r[-1]['status']=='failed':raise RuntimeError('MultiNLI failure requires inspection')
            if len(r)==24 and all(x['status']=='completed' for x in r):break
        time.sleep(15)
    else:return
    if not gate('experiments.day9_router_batch','day9_routing_pilot.txt',['--scope','pilot']):return
    for day,module,log in [(8,'experiments.day8_fixed_memory_integrity','day8_fixed_memory_integrity.txt'),
                           (10,'experiments.day10_initial_loss_integrity','day10_initial_loss_integrity.txt')]:
        if not gate(module,log):return
        if not run(day,2026,'canonical'):return
    if not run(12,2026,'canonical'):return
    if not gate('experiments.day9_router_batch','day9_routing_replication.txt',['--scope','replication']):return
    for seed in [2027,2028,2029,2030,2031]:
        if not run(8,seed,'canonical'):return
        if seed<=2028 and not run(10,seed,'canonical'):return
        if not run(12,seed,'canonical'):return
        if not run(8,seed,'b_first'):return
        if not run(12,seed,'b_first'):return
    print('BALANCED_QUEUE_COMPLETE',flush=True)

if __name__=='__main__':main()
