"""Exercise receipt scope and fail-closed verification without invoking GitHub."""
import ast,hashlib,json,tempfile
from pathlib import Path
source=Path(__file__).with_name('remote-save-verifier-v2.py')
if not source.exists():source=Path('mitosis-interference/experiments/finalize_github_save.py')
nodes=[]
for node in ast.parse(source.read_text()).body:
 if isinstance(node,ast.Assert):break
 nodes.append(node)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
with tempfile.TemporaryDirectory() as temporary:
 root=Path(temporary); old=root/'mitosis-lfs-verify-prior'; fresh=root/'fresh'
 (root/'notes').mkdir()
 objects=[hashlib.sha256(v).hexdigest() for v in [b'old-a',b'old-b',b'not-covered']]
 for oid,data in zip(objects,[b'old-a',b'old-b',b'not-covered']):
  p=old/'objects'/oid[:2]/oid[2:4]/oid;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 receipt={'all_current_lfs_sha256_verified':True,'repository':'anitusiruk/mitosis-interference',
          'preserved_snapshot_commit':'fixture','unique_lfs_objects_verified':2}
 rp=root/'notes/github_save_verification.json';rp.write_text(json.dumps(receipt))
 ns['WORKSPACE']=root
 ns['lfs_map']=lambda commit: {'results/one/checkpoint/a.pt':objects[0], 'results/two/checkpoint/b.pt':objects[1]}
 import os
 original=Path.cwd();os.chdir(root)
 try:
  sources,seeded=ns['seed_verified_remote_objects'](fresh,set(objects))
  assert seeded==set(objects[:2]) and len(sources)==1
  assert not (fresh/'objects'/objects[2][:2]/objects[2][2:4]/objects[2]).exists()
  receipt['unique_lfs_objects_verified']=3;rp.write_text(json.dumps(receipt))
  try:ns['seed_verified_remote_objects'](root/'bad-count',set(objects))
  except AssertionError:pass
  else:raise AssertionError('Mismatched receipt scope accepted')
  receipt['unique_lfs_objects_verified']=2;rp.write_text(json.dumps(receipt))
  p=old/'objects'/objects[0][:2]/objects[0][2:4]/objects[0];p.write_bytes(b'corrupted')
  try:ns['seed_verified_remote_objects'](root/'bad-hash',set(objects))
  except AssertionError:pass
  else:raise AssertionError('Corrupted remote object accepted')
  p.unlink()
  try:ns['seed_verified_remote_objects'](root/'missing',set(objects))
  except AssertionError:pass
  else:raise AssertionError('Incomplete prior cache accepted')
 finally:os.chdir(original)
print('REMOTE_CACHE_REUSE_GATE_PASS: only receipt-covered objects reused; count mismatch, corrupted and missing objects rejected')

