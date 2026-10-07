"""Known recurrence curve checks, including exclusion of unseen predictions."""
import json
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd
from experiments.day18_deployment_retention import summarize, RULES


def main():
    with tempfile.TemporaryDirectory(prefix='retention_curve_integrity_') as name:
        folder = Path(name)
        (folder/'summary.json').write_text(json.dumps({'status': 'completed', 'steps': 80}))
        (folder/'provenance.json').write_text('{}')
        route = pd.DataFrame([{'step': i+1, 'segment': ['A1','B1','A2','C1','B2'][i//16],
                               'concept': ['A','B','A','C','B'][i//16]} for i in range(80)])
        route.to_csv(folder/'routing.csv', index=False)
        accuracies = {'A': [.5,.4,.7,.6,.6], 'B': [.99,.6,.5,.5,.8], 'C': [.95,.95,.95,.7,.5]}
        rows = [{'step': 16*(j+1), 'checkpoint': ['A1','B1','A2','C1','B2'][j],
                 'rule': rule, 'concept': concept, 'accuracy': accuracies[concept][j], 'n': 12,
                 'seen_concept': concept in set(route.loc[route.step <= 16*(j+1), 'concept'])}
                for j in range(5) for rule in RULES for concept in ['A','B','C']]
        frame = pd.DataFrame(rows)
        frame.to_csv(folder/'label_free_eval.csv', index=False)
        _, metrics, concepts = summarize(folder)
        for row in metrics:
            assert abs(row['final_macro_accuracy'] - 1.9/3) < 1e-12
            assert abs(row['mean_seen_checkpoint_accuracy'] - (.5+.5+.6+.6+1.9/3)/5) < 1e-12
            assert abs(row['maximum_seen_checkpoint_drop'] - .1) < 1e-12
            assert abs(row['final_minus_first_exposure'] - .1/3) < 1e-12
        assert len(concepts) == 9
        for bad in [frame.iloc[:-1], frame.assign(seen_concept=True)]:
            bad.to_csv(folder/'label_free_eval.csv', index=False)
            try:
                summarize(folder)
            except AssertionError:
                pass
            else:
                raise AssertionError('Incomplete or future-contaminated curve was accepted')
    print('RETENTION_CURVE_ANALYTIC_GATE_PASS recurrence, unseen exclusion, missing-data rejection', flush=True)


if __name__ == '__main__':
    main()
