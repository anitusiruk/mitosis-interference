"""Check known factor/interaction effects and partial-pair handling on synthetic data."""
import importlib
import itertools
import json
import os
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd

from src.moment_component_audit import FACTORS
from experiments import day15_moment_report as report


def main():
    original = Path.cwd()
    with tempfile.TemporaryDirectory(prefix='day15_synthetic_',dir=original.parent) as temporary:
        os.chdir(temporary)
        try:
            Path('notes').mkdir();Path('results').mkdir()
            created=[]
            for seed in range(2027,2032):
                for order in ['canonical','b_first']:
                    for regime in ['banking','amazon']:
                        folder=Path('results')/f'day15_{regime}_{seed}_{order}_weight_moments'
                        folder.mkdir();created.append(folder)
                        (folder/'observer_verification.json').write_text(json.dumps({'status':'passed'}))
                        (folder/'provenance.json').write_text(json.dumps({'args':{
                            'seed':seed,'order':order,'regime':regime,'component_audit':True,
                            'architecture':'private','policy':'cau'}}))
                        pd.DataFrame({'step':range(1,81)}).to_csv(folder/'routing.csv',index=False)
                        rows=[]
                        for cell in itertools.product([False,True],repeat=4):
                            initial=10-sum((i+1)*v for i,v in enumerate(cell))*.1
                            gain=.02*sum(cell)+.08*cell[0]*cell[1]
                            for fold,indices in [('A',[1]),('B',[0,2])]:
                                rows.append(dict(zip(FACTORS,cell))|{'step':7,'source_adapter':'default',
                                    'fold':fold,'query_n':len(indices),'query_indices':str(indices),
                                    'query_before':initial,'query_after':initial-gain,'local_trainability':gain,
                                    'group_mass_loss_before':.3*initial,'within_group_loss_before':.7*initial,
                                    'group_mass_loss_after':.3*(initial-gain),'within_group_loss_after':.7*(initial-gain),
                                    'query_before_each':str([initial]*len(indices)),
                                    'query_after_each':str([initial-gain]*len(indices))})
                        pd.DataFrame(rows).to_csv(folder/'component_trials.csv',index=False)
            report.main();data=pd.read_csv('results/day15_seed_intervals.csv')
            assert set(data.n_seeds)=={5}
            for factor,expected in zip(FACTORS,[.16,.26,.32,.42]):
                values=data[(data.kind=='marginal')&(data.factor==factor)&
                            (data.metric=='post_update_loss_decrease')]
                assert np.allclose(values['mean'],expected,atol=1e-12),factor
            values=data[(data.kind=='interaction')&(data.factor==FACTORS[0]+' x '+FACTORS[1])&
                        (data.metric=='post_update_loss_decrease')]
            assert np.allclose(values['mean'],.08,atol=1e-12)
            mass=data[data.metric=='post_group_mass_decrease'].set_index(['regime','kind','factor','condition'])['mean']
            full=data[data.metric=='post_update_loss_decrease'].set_index(['regime','kind','factor','condition'])['mean']
            assert np.allclose(mass,.3*full,atol=1e-12),'Known label-mass contributions must recover analytically'
            # Hide all but one synthetic trajectory without deleting any evidence.
            for folder in created[1:]: folder.rename(folder.with_name('hidden_'+folder.name))
            report.main();partial=pd.read_csv('results/day15_seed_intervals.csv')
            assert partial.empty,'An unpaired order must not form an independent seed cluster'
            print('DAY15_ANALYTIC_REPORT_INTEGRITY_PASS',len(data),'balanced intervals; unpaired order excluded',flush=True)
        finally:
            os.chdir(original)


if __name__=='__main__':
    main()
