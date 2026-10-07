"""Check the scoped rank/rate wrapper against a current exact reference."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from safetensors.torch import load_file

from experiments.day3_action_utility_unit import nested_equal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    original = Path('results/day12_banking_private_single_rank96_seed2031_b_first')
    candidate = Path(args.output)
    provenance = [json.loads((folder / 'provenance.json').read_text()) for folder in [original, candidate]]
    assert provenance[0]['stream_sha256'] == provenance[1]['stream_sha256']
    assert provenance[0]['model_revision'] == provenance[1]['model_revision']
    routes = [pd.read_csv(folder / 'routing.csv') for folder in [original, candidate]]
    columns = ['step', 'adapter', 'decision', 'train_executed', 'num_adapters', 'replay_items']
    assert len(routes[0]) == len(routes[1]) == 80
    assert routes[0][columns].equals(routes[1][columns])
    assert np.allclose(routes[0].loss, routes[1].loss, atol=1e-6, rtol=0)
    states = [torch.load(folder / 'checkpoint/learner_state.pt', map_location='cpu', weights_only=False)
              for folder in [original, candidate]]
    assert nested_equal(*states), 'Scoped baseline port changed the final real learner state'
    files = list((original / 'checkpoint/adapters').rglob('*.safetensors'))
    assert files
    for path in files:
        assert nested_equal(load_file(str(path)), load_file(str(candidate / path.relative_to(original))))
    receipt = {'status': 'passed', 'reference': str(original), 'candidate': str(candidate),
               'stream_sha256': provenance[0]['stream_sha256'], 'bitwise_final_state_equal': True,
               'bitwise_adapter_tensors_equal': True,
               'maximum_training_loss_difference': float(np.max(abs(routes[0].loss-routes[1].loss))),
               'reference_state_sha256': hashlib.sha256((original / 'checkpoint/learner_state.pt').read_bytes()).hexdigest()}
    (candidate / 'static_replay_verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('STATIC_TUNING_BITWISE_REPLAY_GATE_PASS', flush=True)


if __name__ == '__main__':
    main()
