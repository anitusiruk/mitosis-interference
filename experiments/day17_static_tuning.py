"""Scoped static-rank/rate port of the unchanged Day-12 trainer."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from peft import LoraConfig

from experiments import day12_capacity_recurrence as trainer
from src.adapter_pool_cau_v1 import CAUV1AdapterPool


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank', type=int, choices=[8, 96], required=True)
    parser.add_argument('--learning-rate', type=float, required=True)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--order', choices=['canonical', 'b_first'], required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--deadline-utc', required=True)
    args = parser.parse_args()
    if not math.isfinite(args.learning_rate) or args.learning_rate <= 0:
        parser.error('A finite positive rate is required')
    supplied = {}

    def config(**kwargs):
        if kwargs['r'] != 96 or kwargs['lora_alpha'] != 192:
            raise RuntimeError('Unexpected reference rank configuration')
        kwargs.update(r=args.rank, lora_alpha=2 * args.rank)
        supplied['config'] = dict(kwargs)
        return LoraConfig(**kwargs)

    def pool(**kwargs):
        if kwargs['lr'] != 2e-4:
            raise RuntimeError('Unexpected reference optimizer rate')
        kwargs['lr'] = args.learning_rate
        answer = CAUV1AdapterPool(**kwargs)
        if any(g['lr'] != args.learning_rate for s in answer.states.values()
               for g in s.optimizer.param_groups):
            raise RuntimeError('The actual AdamW rate differs')
        return answer

    trainer.LoraConfig = config
    trainer.CAUV1AdapterPool = pool
    sys.argv = ['day12_capacity_recurrence', '--regime', 'banking', '--architecture', 'private',
                '--policy', 'single', '--seed', str(args.seed), '--order', args.order,
                '--output', args.output, '--deadline-utc', args.deadline_utc]
    trainer.main()
    folder = Path(args.output)
    p = json.loads((folder / 'provenance.json').read_text())
    p.update(lora_rank=args.rank, lora_alpha=2 * args.rank, learning_rate=args.learning_rate,
             tuning_spec_sha256=hashlib.sha256(Path('notes/day17_static_tuning_spec.md').read_bytes()).hexdigest(),
             tuning_wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             override_scope=['lora_rank', 'lora_alpha', 'adamw_learning_rate'],
             actual_lora_config=supplied['config'])
    (folder / 'provenance.json').write_text(json.dumps(p, indent=2) + '\n')
    summary = json.loads((folder / 'summary.json').read_text())
    route = pd.read_csv(folder / 'routing.csv')
    if (summary['status'] != 'completed' or len(route) != 80
            or summary['learning_updates'] != 80 or route.num_adapters.max() != 1
            or set(route.decision) != {'single_update'} or route.replay_items.max() > 512
            or not np.isfinite(route.loss).all()):
        raise RuntimeError('Incomplete or invalid static attempt preserved')
    state = trainer.torch.load(folder / 'checkpoint/learner_state.pt', map_location='cpu', weights_only=False)
    for opt in state['optimizers'].values():
        if any(g['lr'] != args.learning_rate for g in opt['param_groups']):
            raise RuntimeError('Saved optimizer rate differs')
    evaluation = pd.read_csv(folder / 'label_free_eval.csv')
    for _, batch in evaluation.groupby(['step', 'concept']):
        if len(batch) != 3 or batch.accuracy.nunique() != 1 or np.ptp(batch.loss) > 1e-5:
            raise RuntimeError('One-package predictor rules differ')
    print('STATIC_TUNING_TRAJECTORY_PASS', args.rank, args.learning_rate, args.seed, args.order, flush=True)


if __name__ == '__main__':
    main()
