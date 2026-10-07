from pathlib import Path
from datetime import datetime,timezone
import importlib.metadata as metadata,json,subprocess,sys,os,fcntl,hashlib
root=Path('/workspace/mitosis-static-tuning');os.chdir(root)
lock=open('/workspace/mitosis-static-tuning-worker.lock','a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
critical=['numpy','pandas','torch','transformers','peft','datasets','accelerate','scipy']
def versions():
 result={}
 for name in critical:
  try:result[name]=metadata.version(name)
  except metadata.PackageNotFoundError:result[name]=None
 return result
before=versions()
constraints=Path('environment/plotting_constraints_20261007.txt');assert not constraints.exists()
constraints.write_text(''.join(name+'=='+version+'\n' for name,version in before.items() if version))
report=Path('notes/plotting_install_report_20261007.json');assert not report.exists()
args=[sys.executable,'-m','pip','install','--no-input','--disable-pip-version-check','--index-url','https://pypi.org/simple','--only-binary=:all:','--constraint',str(constraints),'--report',str(report),'matplotlib==3.10.7']
with Path('logs/plotting_install_20261007.txt').open('x') as log:
 code=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT).returncode
assert code==0,'Pinned plotting install failed; inspect preserved log'
assert versions()==before,'A training library version changed'
installed={item['metadata']['name'].lower() for item in json.loads(report.read_text())['install']}
assert not installed.intersection(set(critical)),installed
assert metadata.version('matplotlib')=='3.10.7'
Path('requirements-plotting.txt').write_text('matplotlib==3.10.7\n')
Path('notes/plotting_dependency_restore_20261007.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'before_training_versions':before,'after_training_versions':versions(),'training_packages_reinstalled':False,'matplotlib_version':'3.10.7','install_returncode':code,'official_index':'https://pypi.org/simple'},indent=2)+'\n')
sys.path.insert(0,str(root))
from experiments.day17_evidence_figures import OUT,frozen_classifier_figure
OUT.mkdir(parents=True,exist_ok=True);caption=frozen_classifier_figure();assert caption
Path('notes/day19_classifier_figure_caption.md').write_text(caption+'\n')
p=Path('experiments/day17_evidence_figures.py');assert hashlib.sha256(p.read_bytes()).hexdigest()=='8ae4b71c4dcc6cf9c5a9d2f7255a5634552d4372e5cb111f8467b77f52d2bb91'
Path('notes/figure_source_amendment_20261007.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'old_source_sha256':'4065f47a10793cc4b3e1643cd19d74fa93659921fd54637fafcaf7b34240c065','new_source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scientific_training_sources_modified':False,'added_after_control_outcomes':True,'reason':'clarify full classifier-stack interventions and show every original prediction rule','source_result_sha256':hashlib.sha256(Path('results/day19_linear_classifier_prediction_differences.csv').read_bytes()).hexdigest(),'visual_render_review_pending':True},indent=2)+'\n')
env=os.environ.copy();env.update(GIT_TERMINAL_PROMPT='0',GH_PROMPT_DISABLED='1')
for args in [['git','add','-A'],['git','commit','-m','Restore pinned plotting dependencies and clarify classifier evidence figures'],['git','push','origin','day17-static-tuning-20261006']]:
 assert subprocess.run(args,env=env).returncode==0
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','ls-remote','origin','refs/heads/day17-static-tuning-20261006'],text=True,env=env).split()[0]==head
assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip()
print('PINNED_PLOTTING_RESTORED_AND_CLASSIFIER_FIGURE_PUSHED',head,'TRAINING_PACKAGES_UNCHANGED',flush=True)
