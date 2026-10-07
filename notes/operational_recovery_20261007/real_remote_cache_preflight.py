from pathlib import Path
import ast,hashlib,json,datetime
source=Path('/workspace/mitosis-interference/experiments/finalize_github_save.py')
assert hashlib.sha256(source.read_bytes()).hexdigest()=='cb571bba6fa6b024130cfaa40ee679c7942c937b4f6ccb43f0c2ee151752c102'
nodes=[]
for node in ast.parse(source.read_text()).body:
 if isinstance(node,ast.Assert):break
 nodes.append(node)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
head=ns['read'](['git','rev-parse','HEAD'])
oids=set(ns['lfs_map'](head).values())
storage=Path('/workspace/mitosis-remote-cache-preflight-20261007')
assert not storage.exists()
sources,seeded=ns['seed_verified_remote_objects'](storage,oids)
value={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'snapshot_at_start':head,
 'helper_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'prior_remote_objects_rehashed':len(seeded),
 'current_snapshot_unique_objects':len(oids),'new_objects_not_yet_downloaded':len(oids-seeded),
 'sources':sources,'preflight_only':True,'all_current_objects_remotely_verified':False}
Path('/workspace/mitosis-interference/notes/github_remote_cache_preflight.json').write_text(json.dumps(value,indent=2)+'\n')
print('REAL_REMOTE_CACHE_PREFLIGHT_PASS',len(seeded),'prior verified objects;',len(oids-seeded),'new objects still require download',flush=True)
