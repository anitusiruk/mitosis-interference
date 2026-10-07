"""Scientific figures from complete saved contrast tables; no outcome selection."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FACTORS = ['reset_lora_weights', 'reset_head_weights', 'reset_lora_optimizer', 'reset_head_optimizer']
LABELS = ['LoRA weights', 'Classifier stack weights', 'LoRA AdamW state', 'Classifier stack AdamW state']
OUT = Path('figures/extended_audit')


def save(fig, stem):
    for extension in ['png', 'pdf', 'svg']:
        fig.savefig(OUT / (stem + '.' + extension), dpi=220, bbox_inches='tight')
    plt.close(fig)


def read(path):
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def contrasts(frame, metric):
    d = frame[frame.metric == metric].set_index('factor').reindex(FACTORS)
    if d['mean'].isna().any():
        raise RuntimeError('Cannot silently omit a reset factor')
    return d


def draw_points(ax, d, offset, label, color):
    y = np.arange(4) + offset
    ax.scatter(d['mean'], y, color=color, s=27, label=label, zorder=3)
    # Missing one-seed intervals remain visibly absent, never zero-width bars.
    for position, (_, row) in zip(y, d.iterrows()):
        if np.isfinite([row.ci_low, row.ci_high]).all():
            ax.plot([row.ci_low, row.ci_high], [position, position], color=color, lw=1.3)


def frozen_classifier_figure():
    d = read('results/day19_linear_classifier_prediction_differences.csv')
    if d.empty:
        return None
    rules = ['frozen_centroid', 'last_active', 'uniform_probability']
    assert len(d) == 3 and set(d.rule) == set(rules)
    d = d.set_index('rule').loc[rules]
    assert np.isfinite(d[['mean','ci_low','ci_high']].to_numpy()).all()
    fig, ax = plt.subplots(figsize=(8.1, 3.8))
    for i, (_, row) in enumerate(d.iterrows()):
        ax.scatter(100*row['mean'], i, s=36, color='#2468a2', zorder=3)
        ax.plot([100*row.ci_low,100*row.ci_high], [i,i], color='#2468a2', lw=1.7)
    ax.axvline(0, color='black', lw=.8)
    ax.set_yticks(range(3), ['Frozen centroid', 'Last active', 'Uniform mixture'])
    ax.invert_yaxis()
    ax.set_xlabel('LoRA plus output classifier minus output classifier only\nDevelopment accuracy difference (percentage points)')
    ax.set_title('Frozen hidden pre-classifier | '+str(int(d.seed_clusters.min()))+' paired training seeds')
    ax.grid(axis='x', alpha=.2)
    fig.tight_layout()
    save(fig, 'frozen_preclassifier_lora_comparison')
    return ('* `frozen_preclassifier_lora_comparison`: All three original prediction '
            'rules in the within-backbone control. The hidden pre-classifier and its '
            'private copies stay frozen. Positive differences favor LoRA learning; '
            'negative differences favor output-classifier-only learning. Both orders '
            'are averaged inside each training seed. The plot is a development '
            'diagnostic, not a tuned performance benchmark or untouched confirmation. '
            'Freezing the hidden layer also removes its optimizer state. No rule '
            'is selected by its observed outcome.')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    captions = ['# Extended development-audit figure captions', '',
        'All intervals are descriptive 95% Student intervals over paired training seeds. '
        'Both orders are averaged first. Fixed development examples have been repeatedly '
        'examined; no population-sampling or multiplicity-adjusted claim follows. '
        'No factor, regime or deployed rule is chosen by observed performance.', '']
    evidence = read('results/day15_seed_intervals.csv')
    if not evidence.empty:
        evidence = evidence[evidence.kind == 'marginal']
        available = [r for r in ['banking', 'amazon'] if r in set(evidence.regime)]
        fig, axes = plt.subplots(len(available), 1, figsize=(8.7, 3.9*len(available)), squeeze=False)
        for ax, regime in zip(axes[:,0], available):
            part = evidence[evidence.regime == regime]
            for metric, shift, label, color in [
                ('initial_loss_decrease', -.19, 'Initial predictor effect', '#2468a2'),
                ('local_improvement_increase', 0, 'Local learning effect', '#bd5f1b'),
                ('post_update_loss_decrease', .19, 'Post-update total', '#208047')]:
                draw_points(ax, contrasts(part, metric), shift, label, color)
            ax.axvline(0, color='black', lw=.7)
            ax.set_yticks(range(4), LABELS); ax.invert_yaxis()
            ax.set_title(f'{regime.upper()} | {int(part.n_seeds.min())} paired seeds')
            ax.set_xlabel('Loss effect of reset (positive = improvement)')
            ax.grid(axis='x', alpha=.2); ax.legend(fontsize=8, loc='best')
        fig.tight_layout(); save(fig, 'weight_state_attribution')
        captions += ['* `weight_state_attribution`: All four marginal reset effects, split into '
            'initial prediction and one-step local learning contributions, plus their post-update '
            'total. Artificial inherited optimizer states on reset weights are causal probes, '
            'not recommended deployment states. The classifier-stack factor includes '
            'both the hidden pre-classifier and output classifier. Effects average '
            'every eligible mature batch and all eight settings of the other factors; '
            'each verified observer reproduces the original '
            'real learner bitwise. The source is the actual active package, not retrospectively '
            'best feasible reuse.', '']
        fig, axes = plt.subplots(len(available), 2, figsize=(11, 3.8*len(available)), squeeze=False)
        for row, regime in enumerate(available):
            part = evidence[evidence.regime == regime]
            for col, phase in enumerate(['initial', 'post']):
                ax = axes[row,col]
                draw_points(ax, contrasts(part, phase+'_group_mass_decrease'), -.12,
                            'Group probability mass', '#2468a2')
                draw_points(ax, contrasts(part, phase+'_within_group_decrease'), .12,
                            'Within-group prediction', '#bd5f1b')
                ax.axvline(0, color='black', lw=.7)
                ax.set_yticks(range(4), LABELS); ax.invert_yaxis()
                ax.set_title(regime.upper() + ' | ' + ('Before update' if phase == 'initial' else 'After update'))
                ax.set_xlabel('Reset effect on cross-entropy component')
                ax.grid(axis='x', alpha=.2); ax.legend(fontsize=8)
        fig.tight_layout(); save(fig, 'label_group_attribution')
        captions += ['* `label_group_attribution`: All marginal reset contrasts in label-group '
            'probability loss and conditional within-group loss, before and after the matched '
            'update. Group metadata is evaluator-only and never enters allocation or deployed '
            'routing. BANKING has three disjoint observed label groups in a 77-output space; '
            'Amazon uses the full shared binary group, so its group-mass component is zero. '
            'The probability factorization is established prior work, not new theory.', '']
    grid = read('results/day17_static_pilot_grid.csv')
    if not grid.empty:
        fig, ax = plt.subplots(figsize=(7.5,4.6))
        for rank, color in [(8, '#2468a2'), (96, '#bd5f1b')]:
            d = grid[grid['rank'] == rank]
            means = d.groupby('learning_rate').final_macro_accuracy.mean().sort_index()
            ax.plot(means.index, means, marker='o', color=color, label=f'Rank {rank} paired-order mean')
            ax.scatter(d.learning_rate, d.final_macro_accuracy, color=color, alpha=.5, marker='x', s=30)
        ax.set_xscale('log'); ax.set_xlabel('AdamW learning rate')
        ax.set_ylabel('Final concept-macro development accuracy')
        ax.set_title('Seed 2026 tuning grid | both orders retained')
        ax.grid(alpha=.2); ax.legend(fontsize=8)
        fig.tight_layout(); save(fig, 'static_pilot_grid')
        captions += ['* `static_pilot_grid`: Every declared learning-rate candidate for both ranks '
            'and both pilot orders; crosses show individual orders and lines show their averages. '
            'The orders are not independent seed replicates. Rate selection uses only these '
            'pilot outcomes, before paired development confirmations.', '']
    comparison = read('results/day17_tuned_static_paired_differences.csv')
    if not comparison.empty:
        fig, ax = plt.subplots(figsize=(9,5.7))
        d = comparison.sort_values(['rank','adaptive_rule']).reset_index(drop=True)
        labels = [f'Rank {r["rank"]} | {r.adaptive_rule}' for _,r in d.iterrows()]
        for i, (_,r) in enumerate(d.iterrows()):
            color = '#2468a2' if r['rank'] == 8 else '#bd5f1b'
            ax.scatter(100*r['mean'], i, color=color, zorder=3)
            if np.isfinite([r.ci_low,r.ci_high]).all():
                ax.plot([100*r.ci_low,100*r.ci_high],[i,i],color=color,lw=1.5)
        ax.axvline(0,color='black',lw=.7);ax.set_yticks(range(len(d)),labels);ax.invert_yaxis()
        ax.set_xlabel('Fixed-memory adaptive minus tuned static accuracy (percentage points)')
        ax.set_title('Every frozen adaptive rule and both tuned static ranks')
        ax.grid(axis='x',alpha=.2);fig.tight_layout();save(fig,'tuned_static_development_comparison')
        captions += ['* `tuned_static_development_comparison`: Every adaptive routing rule versus '
            'both pilot-selected static ranks. Positive differences favor the adaptive reference. '
            'Actual head storage and compute differ even under the same retained-text budget. '
            'This repairs a learning-rate comparator gap; it does not establish final-test or '
            'named-method superiority.', '']
    classifier_caption = frozen_classifier_figure()
    if classifier_caption:
        captions += [classifier_caption, '']
    Path(OUT/'CAPTIONS.md').write_text('\n'.join(captions)+'\n')
    print('EXTENDED_EVIDENCE_FIGURES_SAVED', len(list(OUT.glob('*.png'))), flush=True)


if __name__ == '__main__':
    main()
