"""Cross-architecture allocation diagnostic using the frozen Day-8 trainer."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from peft import LoraConfig
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from experiments import day8_fixed_memory_recurrence as trainer


MODEL = 'google-bert/bert-base-uncased'


class TokenizerFactory:
    @staticmethod
    def from_pretrained(_original, **kwargs):
        return AutoTokenizer.from_pretrained(MODEL, **kwargs)


class ModelFactory:
    @staticmethod
    def from_pretrained(_original, **kwargs):
        return AutoModelForSequenceClassification.from_pretrained(MODEL, **kwargs)


def bert_lora(**kwargs):
    if kwargs['target_modules'] != ['q_lin','v_lin']:
        raise RuntimeError('Unexpected reference LoRA targets')
    kwargs['target_modules'] = ['query','value']
    return LoraConfig(**kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--architecture', choices=['private','head_only'], required=True)
    parser.add_argument('--seed',type=int,required=True)
    parser.add_argument('--order',choices=['canonical','b_first'],required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--deadline-utc',required=True)
    args=parser.parse_args()
    pin=json.loads(Path('notes/day16_bert_backbone_pin.json').read_text())
    if pin['model_id'] != MODEL or len(pin['revision']) != 40:
        raise RuntimeError('Missing explicit BERT snapshot pin')
    os.environ['MITOSIS_MODEL_REVISION']=pin['revision']
    spec=Path('notes/day16_bert_allocation_spec.md')
    receipt={'model_id':MODEL,'backbone_manifest_sha256':hashlib.sha256(
        Path('notes/day16_bert_backbone_pin.json').read_bytes()).hexdigest(),
        'diagnostic_spec_sha256':hashlib.sha256(spec.read_bytes()).hexdigest(),
        'diagnostic_implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'architecture_scope':'BERT classifier-only output layer; frozen pooler',
        'lora_targets':['query','value'],'official_test_used':False}
    print('DAY16_FROZEN_DIAGNOSTIC',json.dumps(receipt,sort_keys=True),flush=True)
    trainer.AutoTokenizer=TokenizerFactory
    trainer.AutoModelForSequenceClassification=ModelFactory
    trainer.LoraConfig=bert_lora
    sys.argv=['day8_fixed_memory_recurrence','--regime','banking','--architecture',args.architecture,
        '--policy','cau','--seed',str(args.seed),'--order',args.order,'--output',args.output,
        '--deadline-utc',args.deadline_utc]
    trainer.main()
    folder=Path(args.output)
    provenance=json.loads((folder/'provenance.json').read_text());provenance.update(receipt)
    (folder/'provenance.json').write_text(json.dumps(provenance,indent=2))
    summary=json.loads((folder/'summary.json').read_text())
    routing=pd.read_csv(folder/'routing.csv')
    if summary['status']!='completed' or len(routing)!=80:
        raise RuntimeError('Incomplete architecture diagnostic preserved')
    if routing.replay_items.max()>512 or routing.num_adapters.max()>8:
        raise RuntimeError('Architecture diagnostic resource bound violated')
    if not np.isfinite(routing.loc[routing.train_executed,'loss']).all():
        raise RuntimeError('Nonfinite training losses')
    reference=Path(f'results/day8_banking_{args.architecture}_cau_seed{args.seed}_{args.order}_fixed512')
    rp=json.loads((reference/'provenance.json').read_text())
    if provenance['stream_sha256']!=rp['stream_sha256']:
        raise RuntimeError('BERT and DistilBERT streams differ')
    print('DAY16_BERT_DIAGNOSTIC_PASS',args.architecture,args.seed,args.order,flush=True)


if __name__=='__main__':
    main()
