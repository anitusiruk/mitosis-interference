"""Standalone scientific figures from saved CSVs; no learner modifications."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import t

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'savefig.bbox':'tight','pdf.fonttype':42,'ps.fonttype':42})
out=Path('figures/research_audit');out.mkdir(parents=True,exist_ok=True)

def save(fig,name):
    for suffix in ['png','pdf','svg']:fig.savefig(out/f'{name}.{suffix}',dpi=220)
    plt.close(fig)


bank=Path('results/day5_banking_private_cau_seed2026')
if (bank/'component_contrasts.csv').exists():
    routing=pd.read_csv(bank/'routing.csv');values=pd.read_csv(bank/'component_contrasts.csv')
    spawns=routing[routing.decision=='spawn']
    data=[]
    for row in spawns.to_dict('records'):
        u=json.loads(row['info'])['utility'];r=u['reuse_profiles'][u['best_reuse']]
        data.append((row['step'],r['query_before']-u['fresh_query_before'],
                     u['fresh_local_trainability']-r['local_trainability']))
    if data:
        fig,axes=plt.subplots(1,2,figsize=(11,4))
        x=np.arange(len(data));init=np.asarray([r[1] for r in data]);learn=np.asarray([r[2] for r in data])
        axes[0].bar(x,init,color='#4477AA',label='Initial predictor gap')
        axes[0].bar(x,learn,bottom=init,color='#EE7733',label='Difference in one-step gain')
        for i,(step,gap,gain) in enumerate(data):axes[0].text(i,gap+gain+.015,f'{gap/(gap+gain):.1%} initial',ha='center')
        axes[0].set_xticks(x,[f'Spawn step {r[0]}' for r in data]);axes[0].set_ylabel('Fresh versus best reuse loss advantage')
        axes[0].set_title('Action utility has two sources');axes[0].legend(frameon=False,fontsize=9)
        selected=values[values.step.isin([r[0] for r in data])]
        metrics=[('new_lora_gain_inherited_head','Fresh LoRA, inherited head','#4477AA'),
                 ('fresh_head_gain_reused_lora','Fresh head, reused LoRA','#EE7733'),
                 ('new_lora_gain_fresh_head','Fresh LoRA, fresh head','#228833')]
        for j,(column,label,color) in enumerate(metrics):axes[1].bar(x+(j-1)*.24,selected[column],width=.24,color=color,label=label)
        axes[1].axhline(0,color='#555555',lw=.8);axes[1].set_xticks(x,[f'Step {r[0]}' for r in data])
        axes[1].set_ylabel('Matched-component held-out loss gain');axes[1].set_title('Classifier reset is a substantial factor')
        axes[1].legend(frameon=False,fontsize=8)
        fig.suptitle('BANKING development seed 2026: dependent spawn-window diagnostics',fontsize=12)
        fig.tight_layout();save(fig,'day5_spawn_attribution')

styles=[('private_cau','Private package CAU','#4477AA'),('head_only_cau','Head-only CAU','#228833'),
        ('shared_cau','Shared-head sensitivity','#CC6677'),('private_single','Fixed single','#666666')]
fig,axes=plt.subplots(1,2,figsize=(11,4))
for suffix,label,color in styles:
    folder=Path(f'results/day5_banking_{suffix}_seed2026')
    if not (folder/'routing.csv').exists():continue
    d=pd.read_csv(folder/'routing.csv')
    axes[0].step(d.step,d.num_adapters,where='post',label=label,color=color)
    deferred=d[d.decision=='defer']
    if len(deferred):axes[0].scatter(deferred.step,np.full(len(deferred),.7),marker='x',s=15,color=color)
    e=pd.read_csv(folder/'label_free_eval.csv')
    # Show the three fixed label-free rules explicitly at the final checkpoint.
    latest=e[e.step==e.step.max()];means=latest.groupby('rule').accuracy.mean()
    for i,rule in enumerate(['last_active','uniform_probability','frozen_centroid']):
        axes[1].scatter(i,means[rule],s=40,color=color)
    axes[1].plot(range(3),[means[r] for r in ['last_active','uniform_probability','frozen_centroid']],color=color,label=label)
for boundary in [17,33,49,65]:axes[0].axvline(boundary,color='#AAAAAA',ls=':',lw=.8)
axes[0].set_xlabel('Incoming batch');axes[0].set_ylabel('Adapter packages');axes[0].set_ylim(.5,3.4)
axes[0].set_title('Capacity and skipped updates (× at bottom)');axes[0].legend(frameon=False,fontsize=8)
axes[1].set_xticks(range(3),['Last active','Uniform mixture','Frozen centroid'],rotation=12)
axes[1].set_ylabel('Final macro accuracy, full 77-way predictions');axes[1].set_ylim(0,.22)
axes[1].set_title('Oracle specialization does not ensure deployment gains')
fig.suptitle('BANKING development seed 2026; all fixed routers shown',fontsize=12)
fig.tight_layout();save(fig,'day5_allocation_and_inference')

path=Path('results/day6_individual_results.csv')
if path.exists():
    d=pd.read_csv(path)
    methods=[('private','cau','Package CAU'),('head_only','cau','Head-only CAU'),
             ('private','single','Package single'),('head_only','single','Head-only single')]
    rules=['last_active','uniform_probability','frozen_centroid']
    fig,axes=plt.subplots(2,3,figsize=(13,7),sharex=True)
    colors=['#4477AA','#228833','#999999','#CCBB44']
    for row,regime in enumerate(['banking','amazon']):
        for col,rule in enumerate(rules):
            ax=axes[row,col]
            for i,(arch,policy,label) in enumerate(methods):
                part=d[(d.regime==regime)&(d.rule==rule)&(d.architecture==arch)&(d.policy==policy)]
                part=part.groupby('seed').filter(lambda g:set(g.order)=={'canonical','b_first'})
                x=part.groupby('seed').macro_accuracy.mean().to_numpy()
                if not len(x):continue
                offsets=np.linspace(-.11,.11,len(x))
                ax.scatter(i+offsets,x,color=colors[i],s=22,alpha=.8)
                mean=x.mean()
                if len(x)>1:
                    half=t.ppf(.975,len(x)-1)*x.std(ddof=1)/np.sqrt(len(x))
                    ax.errorbar(i,mean,yerr=half,color='#222222',capsize=4,fmt='_',ms=15,lw=1.1)
                ax.text(i,mean+.005,f'n={len(x)}',ha='center',fontsize=7)
            ax.set_title(f'{regime.upper()} / {rule.replace("_"," ")}')
            ax.set_xticks(range(4),[m[2] for m in methods],rotation=25,ha='right',fontsize=8)
            ax.set_ylabel('Final macro accuracy')
    fig.suptitle('Two orders averaged inside each seed; dots=seeds, bars=descriptive 95% t intervals',fontsize=11)
    fig.tight_layout();save(fig,'day6_seed_cluster_accuracy')

captions='''# Figure scope and captions

- `day5_spawn_attribution`: original BANKING seed 2026 spawn windows. Left decomposes fresh-versus-best-feasible-reuse advantage into its initial predictor gap and difference in one-step learning gain. Right shows matched active-source component interventions, including their specified optimizer-moment resets. The two panels are different decompositions; initial gap is not itself a pure classifier effect. No uncertainty inference from these dependent windows.
- `day5_allocation_and_inference`: exact package counts and skipped batches for the Day-5 reference, head-only, shared-head sensitivity and fixed single. All three fixed label-free rules use full 77-class predictions. Boundaries in the plot are evaluator metadata only; never supplied to the learner. The shared-head extension also changes protection and moment sharing, so its curve is not a head-sharing-only causal estimate.
- `day6_seed_cluster_accuracy`: both paired orders are averaged within each seed. Dots represent independent seed clusters; intervals are descriptive Student-t intervals conditional on fixed development examples and the two orders. All fixed routing rules are displayed. Partial batches may show fewer than five complete clusters and must be labeled accordingly. No multiplicity-adjusted winner or official-test claim follows.

Macro accuracy averages the three concept-level accuracies; it is not BANKING per-class macro accuracy. All figures are generated deterministically from saved CSV/JSON values and supplied as PNG, SVG and PDF. No fabricated or illustrative measurements are used.
'''
(out/'CAPTIONS.md').write_text(captions)
print('EVIDENCE_FIGURES_SAVED',out,flush=True)
