FILES = {'experiments/day18_evidence_caveats.py': '"""Add estimator and cross-backbone disclosure to the evidence-refreshed draft."""\nimport hashlib\nimport json\nfrom pathlib import Path\n\nimport pandas as pd\nfrom experiments.day5_report import markdown_table\n\n\ndef replace_once(text, old, new):\n    assert text.count(old) == 1, \'Inspect an independently changed draft before editing\'\n    return text.replace(old, new, 1)\n\n\ndef main():\n    paper = Path(\'notes/paper_working_draft.md\')\n    previous = hashlib.sha256(paper.read_bytes()).hexdigest()\n    receipt = json.loads(Path(\'notes/manuscript_refresh_receipt.json\').read_text())\n    assert receipt[\'new_manuscript_sha256\'] == previous\n    text = paper.read_text()\n    text = replace_once(text,\n        \'Matched component interventions show substantial classifier-reset effects on a BANKING recurrence stream.\',\n        \'Matched component interventions show classifier-reset effects at the original BANKING \'\n        \'allocation windows; the broader all-mature-batch audit separately measures effects \'\n        \'across the continuing trajectory.\')\n    text = replace_once(text,\n        \'Across five fresh seeds and two orders, a classifier-only allocator makes the same structural decisions as the full adapter allocator on BANKING, although training low-rank parameters improves prediction.\',\n        \'Across five development training seeds and two orders, a classifier-only allocator \'\n        \'makes the same structural decisions as the full adapter allocator on BANKING, \'\n        \'although training low-rank parameters improves prediction. The BERT transfer \'\n        \'diagnostic also preserves allocation decisions under its declared recipe.\')\n    anchor = (\'The interval unit is a paired training seed; \'\n              \'the fixed development examples do not supply population-sampling uncertainty.\')\n    text = replace_once(text, anchor, anchor + \'\\n\\n\'\n        \'The all-mature-batch marginal effects average all eight settings of the other \'\n        \'three reset factors and all eligible batches. They are a different estimand \'\n        \'from fresh-package versus best-feasible-reuse advantage at allocation windows. \'\n        \'Their signs need not agree. These measurements do not imply that resetting \'\n        \'a trained classifier generally improves prediction. Conditional contrasts \'\n        \'retain the artificial inherited-state/reset-weight combinations; useful \'\n        \'deployment recipes require separate closed-loop experiments.\')\n    anchor = (\'classifier together. It uses a single linear classifier rather than the DistilBERT \'\n              \'trainable pre-classifier/classifier stack, but is not a causal isolation of classifier \'\n              \'design or a tuned BERT performance comparison.\')\n    differences = pd.read_csv(\'results/day16_bert_paired_differences.csv\')\n    assert len(differences) == 6 and set(differences.seed_clusters) == {5}\n    text = replace_once(text, anchor, anchor + \'\\n\\n\'\n        \'All cross-backbone prediction differences are reported below. Negative \'\n        \'values indicate lower BERT accuracy. The cross-backbone changes are joint \'\n        \'changes in architecture and initialized packages, not an optimized \'\n        \'performance comparison or a classifier-only causal attribution.\\n\\n\'\n        + markdown_table(differences))\n    qc = json.loads(Path(\'notes/factorial_receipt_integrity_final.json\').read_text())\n    assert not qc[\'failed\']\n    anchor = \'## Figures and result sources\'\n    text = replace_once(text, anchor,\n        \'## Independent saved-receipt quality control\\n\\n\'\n        f\'A read-only check of {len(qc["passed"])} completed observer trajectories \'\n        \'verified every eligible mature batch, the actual active source, all sixteen \'\n        \'intervention cells and both query folds, weight/state receipt isolation, \'\n        \'bitwise invariance of initial predictions to optimizer-state interventions, \'\n        \'and query-loss/component identities. This additional quality-control check \'\n        \'was added after the first observer outcomes. It changes neither the frozen \'\n        \'experiments nor their contrast definitions and is not a new scientific \'\n        \'replication. Earlier and final receipts are preserved.\\n\\n\' + anchor)\n    paper.write_text(text)\n    Path(\'notes/manuscript_evidence_caveats_receipt.json\').write_text(json.dumps({\n        \'previous_manuscript_sha256\': previous,\n        \'new_manuscript_sha256\': hashlib.sha256(paper.read_bytes()).hexdigest(),\n        \'saved_observers_independently_checked\': len(qc[\'passed\']),\n        \'scope\': \'estimator distinction, full cross-backbone results, post-outcome quality-control disclosure\',\n        \'training_outputs_modified\': False}, indent=2) + \'\\n\')\n    print(\'EVIDENCE_ESTIMATOR_AND_TRANSFER_CAVEATS_SAVED\', flush=True)\n\n\nif __name__ == \'__main__\':\n    main()\n'}

from datetime import datetime,timezone
import fcntl,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path('/workspace/mitosis-interference')
STAGE=Path('/workspace/mitosis-day15-stage')
ENV=os.environ.copy();ENV.update(GIT_TERMINAL_PROMPT='0',GH_PROMPT_DISABLED='1')
BRANCH='day5-causal-audit'
def read(args):return subprocess.check_output(args,cwd=ROOT,env=ENV,text=True,timeout=90).strip()
def run(args,log=None):
 print('RUN',' '.join(args),flush=True)
 return subprocess.run(args,cwd=ROOT,env=ENV,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT if log else None).returncode
os.chdir(ROOT)
locks=[open('/workspace/mitosis-restart-worker.lock','a'),open('/workspace/mitosis-static-tuning-worker.lock','a')]
while True:
 if datetime.now(timezone.utc)>=datetime.fromisoformat('2026-10-07T03:29:00+00:00'):raise RuntimeError('Evidence QC cutoff; staged source remains for the next session')
 acquired=[];ready=False
 try:
  for lock in locks:
   fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);acquired.append(lock)
  p=Path('notes/day17_branch_integration.json')
  if p.exists():
   integration=json.loads(p.read_text())
   ready=integration.get('combined_remote_checkpoints_verified') and not integration.get('combined_save_pending') and not any(integration['editorial_returncodes'].values())
  if ready:break
 except BlockingIOError:pass
 finally:
  if not ready:
   for lock in acquired:fcntl.flock(lock,fcntl.LOCK_UN)
 print('EVIDENCE_QC_WAITING_FOR_VERIFIED_INTEGRATION',datetime.now(timezone.utc).isoformat(),flush=True)
 time.sleep(30)
assert read(['git','branch','--show-current'])==BRANCH
assert read(['git','remote','get-url','origin'])=='https://github.com/anitusiruk/mitosis-interference.git'
assert not read(['git','status','--porcelain'])
assert read(['git','rev-parse','HEAD'])==read(['git','ls-remote','origin','refs/heads/'+BRANCH]).split()[0]
checker=STAGE/'factorial_receipt_audit.py'
assert hashlib.sha256(checker.read_bytes()).hexdigest()=='be2bc41fe2af7f81792bb240037dd1abc8259b966d076a7d0d5e08d14d338521'
assert not Path('experiments/day18_factorial_receipt_audit.py').exists()
Path('experiments/day18_factorial_receipt_audit.py').write_bytes(checker.read_bytes())
for name,text in FILES.items():
 p=Path(name);assert not p.exists();p.write_text(text)
Path('experiments/day18_finalize_evidence_quality.py').write_bytes(Path(__file__).read_bytes())
for source,target in [('factorial_receipt_audit_first.json','notes/factorial_receipt_integrity_first.json'),('factorial_receipt_audit_first.log','logs/factorial_receipt_integrity_first.txt')]:
 assert not Path(target).exists();Path(target).write_bytes((STAGE/source).read_bytes())
with Path('logs/factorial_receipt_integrity_final.txt').open('x') as log:
 code=run([sys.executable,'-u','-m','experiments.day18_factorial_receipt_audit','--root',str(ROOT),'--output','notes/factorial_receipt_integrity_final.json'],log)
editorial=None
if code==0:
 with Path('logs/day18_evidence_caveats.txt').open('x') as log:
  editorial=run([sys.executable,'-u','-m','experiments.day18_evidence_caveats'],log)
qc=json.loads(Path('notes/factorial_receipt_integrity_final.json').read_text())
receipt=json.loads(Path('notes/github_save_verification.json').read_text())
assert receipt['all_current_lfs_sha256_verified']
# Plain-text/figure edits do not change the checkpoint tree already freshly fetched.
changed=read(['git','diff','--name-only',receipt['preserved_snapshot_commit'],'HEAD']).splitlines()
assert not any('checkpoint' in Path(p).parts or Path(p).suffix in {'.pt','.safetensors'} for p in changed)
assert not any('checkpoint' in Path(p).parts or Path(p).suffix in {'.pt','.safetensors'} for p in read(['git','diff','--name-only']).splitlines())
status={'utc':datetime.now(timezone.utc).isoformat(),'quality_control_returncode':code,'editorial_returncode':editorial,
 'verified_observers':len(qc['passed']),'planned_observers':20,'remaining_observers':20-len(qc['passed']),
 'fresh_remote_checkpoint_snapshot':receipt['preserved_snapshot_commit'],
 'checkpoint_tree_unchanged_since_verified_snapshot':True,'training_outputs_modified':False,
 'scope':'independent saved-receipt integrity and transparent manuscript estimands; scientific confirmation remains incomplete'}
Path('notes/final_evidence_quality_status.json').write_text(json.dumps(status,indent=2)+'\n')
assert run(['git','add','-A'])==0
assert run(['git','commit','-m','Verify every mature-batch factorial receipt and clarify evidence estimands'])==0
assert run(['git','push','origin',BRANCH])==0
head=read(['git','rev-parse','HEAD'])
assert read(['git','ls-remote','origin','refs/heads/'+BRANCH]).split()[0]==head
assert not read(['git','status','--porcelain'])
changed=read(['git','diff','--name-only',receipt['preserved_snapshot_commit'],head]).splitlines()
assert not any('checkpoint' in Path(p).parts or Path(p).suffix in {'.pt','.safetensors'} for p in changed)
print('POST_INTEGRATION_EVIDENCE_QC_AND_SAVE_COMPLETE',head,'QUALITY',code,'EDITORIAL',editorial,'OBSERVERS',len(qc['passed']),flush=True)
if code or editorial:raise RuntimeError('Evidence discrepancy preserved for inspection')

