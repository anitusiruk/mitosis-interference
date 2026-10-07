EXPECTED = {'remote-save-verifier-v2.py': 'cb571bba6fa6b024130cfaa40ee679c7942c937b4f6ccb43f0c2ee151752c102', 'test-remote-cache-reuse.py': '27d5c89667a21727775cf7cdc8e24356daad0cc84eb8a801873cf8179b8996e8', 'integrate_saved_branches_v2.py': 'ff2f673b7a92027d1f20f4e321b09295bbebe3773505590802bfcd0a71346de8', 'finalize_evidence_quality_v3.py': '8213e4ceff19add493f4c252a046f822f54ac8897ccf4c5b76ca110d36bd660a'}

from pathlib import Path
import datetime,hashlib,json,os,py_compile,signal,subprocess,sys,time
STAGE=Path('/workspace/mitosis-day15-stage')
ROOT=Path('/workspace/mitosis-interference')
ENV=os.environ.copy();ENV.update(GIT_TERMINAL_PROMPT='0',GH_PROMPT_DISABLED='1')
def read(args):return subprocess.check_output(args,cwd=ROOT,env=ENV,text=True,timeout=90).strip()
for name,expected in EXPECTED.items():
 p=STAGE/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,(name,'staging checksum mismatch');py_compile.compile(str(p),doraise=True)
FILES={name:(STAGE/name).read_text() for name in EXPECTED}
with (STAGE/'remote_cache_reuse_gate.log').open('x') as log:
 code=subprocess.run([sys.executable,str(STAGE/'test-remote-cache-reuse.py')],cwd=STAGE,stdout=log,stderr=subprocess.STDOUT).returncode
assert code==0, 'Cache reuse gate failed; authoritative checkout unchanged'
assert read(['git','remote','get-url','origin'])=='https://github.com/anitusiruk/mitosis-interference.git'
assert read(['git','branch','--show-current'])=='day5-causal-audit'
assert not read(['git','status','--porcelain'])
assert not (ROOT/'.git/index.lock').exists()
target=ROOT/'experiments/finalize_github_save.py'
assert hashlib.sha256(target.read_bytes()).hexdigest()=='46d4bbe044e906485721cddf1c999f9465dd5dcbb95a2014f0ba474ab7dc5e21'
status=json.loads((ROOT/'notes/day15_16_execution_status.json').read_text())
assert status['jobs'][-1]['status']=='running'
trainers=[]
for proc in Path('/proc').iterdir():
 if not proc.name.isdigit():continue
 try:args=(proc/'cmdline').read_bytes().split(b'\0')
 except OSError:continue
 if b'experiments.day15_weight_moment_recurrence' in args:trainers.append(int(proc.name))
assert len(trainers)==1,'Only edit the administrative helper during a live scientific training job'
critical=['experiments/day15_weight_moment_recurrence.py','src/moment_component_audit.py','src/adapter_pool_fixed_memory.py']
before={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in critical}
old=(STAGE/'finalize_github_save_original.py');assert not old.exists();old.write_bytes(target.read_bytes())
temporary=target.with_suffix('.py.pending');temporary.write_text(FILES['remote-save-verifier-v2.py']);temporary.replace(target)
assert before=={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in critical}
(ROOT/'logs/github_remote_cache_reuse_integrity.txt').write_bytes((STAGE/'remote_cache_reuse_gate.log').read_bytes())
(ROOT/'notes/github_backup_verification_amendment.json').write_text(json.dumps({
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'administrative_only':True,
 'scientific_training_sources_sha256_unchanged':before,'live_training_process':trainers[0],
 'gate_returncode':code,'old_helper_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
 'new_helper_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
 'mode':'rehash receipt-covered immutable independent GitHub downloads; fetch every remaining current object; rehash the complete snapshot',
 'old_receipts_archived':True,'training_cutoffs_unchanged':True,
 'backup_only_cutoff_utc':'2026-10-07T06:00:00+00:00',
 'reason':'avoid redundant multi-gigabyte downloads while retaining independent remote-byte verification'},indent=2)+'\n')
print('ADMINISTRATIVE_BACKUP_HELPER_UPDATED',hashlib.sha256(target.read_bytes()).hexdigest(),flush=True)
# Replace only waiting coordinators; active trainers and save workers remain untouched.
for stem,expected,new,oldlog,newlog in [
 ('mitosis_day17_integration','experiments/day17_integrate_saved_branches.py','integrate_saved_branches_v2.py','mitosis_day17_integration.log','mitosis_day17_integration_v2.log'),
 ('mitosis_day18_quality','/workspace/mitosis-day15-stage/finalize_evidence_quality_v2.py','finalize_evidence_quality_v3.py','mitosis_day18_quality_v2.log','mitosis_day18_quality_v3.log')]:
 pidfile=Path('/workspace')/(stem+'_pid.txt');pid=int(pidfile.read_text())
 args=(Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0')
 assert any(expected.encode() in arg for arg in args),(stem,pid,args)
 lines=(Path('/workspace')/oldlog).read_text(errors='replace').splitlines()
 assert lines and 'WAITING_FOR_' in lines[-1], 'Coordinator is no longer waiting; leave it intact'
 os.kill(pid,signal.SIGTERM)
 for _ in range(30):
  proc=Path('/proc')/str(pid)
  if not proc.exists() or ') Z ' in (proc/'stat').read_text():break
  time.sleep(.1)
 else:raise RuntimeError('Waiting coordinator did not terminate')
 with (Path('/workspace')/newlog).open('x') as log:
  child=subprocess.Popen([sys.executable,'-u',str(STAGE/new)],cwd=ROOT,env=ENV,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  pidfile.write_text(str(child.pid)+'\n')
 print('COORDINATOR_REPLACED_WHILE_WAITING',stem,pid,'to',child.pid,flush=True)
print('BACKUP_AND_EVIDENCE_COORDINATORS_READY',flush=True)

