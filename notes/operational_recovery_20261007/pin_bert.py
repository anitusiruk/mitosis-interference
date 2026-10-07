from pathlib import Path
from huggingface_hub import HfApi,snapshot_download
from datetime import datetime,timezone
import json,hashlib
model='google-bert/bert-base-uncased'
revision=HfApi(token=False).model_info(model).sha
path=Path(snapshot_download(model,revision=revision,token=False,allow_patterns=['config.json','tokenizer_config.json','tokenizer.json','vocab.txt','model.safetensors','special_tokens_map.json']))
files={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in path.iterdir() if p.is_file()}
assert 'model.safetensors' in files and 'config.json' in files
manifest={'model_id':model,'revision':revision,'resolved_utc':datetime.now(timezone.utc).isoformat(),'files':files,'download_only_no_research_evaluation':True}
Path('/workspace/mitosis-day15-stage/day16_bert_backbone_pin.json').write_text(json.dumps(manifest,indent=2))
print('BERT_BACKBONE_PINNED',revision,len(files),sum(x['bytes'] for x in files.values()),flush=True)
