"""Plot the entire one-seed NLI rate grid, including both orders and initial state."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    report = json.loads(Path('notes/day22_multinli_pilot_report.json').read_text())
    assert report['all_candidates_complete'] and report['complete_candidates'] == 6
    frame = pd.read_csv('results/day22_multinli_pilot_metrics.csv')
    rates = sorted(frame.rate.unique())
    assert rates == [5e-5, 2e-4, 8e-4]
    output = Path('figures/nli_learnability_pilot')
    output.mkdir(exist_ok=False)
    figure, axes = plt.subplots(1, 2, figsize=(11.3, 4.4), sharey=True)
    initial = frame[frame.step == 0].groupby('rate').accuracy.mean().reindex(rates)
    final = frame[frame.step == 360].groupby('rate').accuracy.mean().reindex(rates)
    axes[0].plot(rates, initial, color='#66717c', marker='s', label='Untrained mean')
    axes[0].plot(rates, final, color='#2468a2', marker='o', label='Final paired-order mean')
    per_order = frame[frame.step == 360].groupby(['rate', 'order']).accuracy.mean()
    for rate in rates:
        values = per_order.loc[rate].reindex(['canonical', 'b_first'])
        axes[0].scatter([rate * np.exp(-.045), rate * np.exp(.045)], values, marker='x', color='#2468a2', alpha=.65, zorder=4)
    axes[0].axhline(.5, color='#208047', ls=':', lw=1.1, label='Macro gate: 0.50')
    axes[0].set_title('Concept-macro accuracy | all three rates')
    colors = ['#2468a2', '#bd5f1b', '#7c4b96']
    for concept, genre, color in zip(['A', 'B', 'C'], ['Fiction', 'Government', 'Telephone'], colors):
        part = frame[(frame.step == 360) & (frame.concept == concept)]
        means = part.groupby('rate').accuracy.mean().reindex(rates)
        axes[1].plot(rates, means, color=color, marker='o', label=genre)
        for rate in rates:
            values = part[part.rate == rate].set_index('order').accuracy.reindex(['canonical', 'b_first'])
            axes[1].scatter([rate * np.exp(-.045), rate * np.exp(.045)], values, marker='x', color=color, alpha=.55, zorder=4)
    axes[1].axhline(.4, color='#208047', ls=':', lw=1.1, label='Every-genre gate: 0.40')
    axes[1].set_title('Final genre accuracy | both orders retained')
    for axis in axes:
        axis.set_xscale('log')
        axis.set_xticks(rates, [f'{rate:g}' for rate in rates])
        axis.minorticks_off()
        axis.set_xlabel('AdamW learning rate')
        axis.axhline(1 / 3, color='black', ls='--', lw=.75, label='Balanced chance')
        axis.grid(alpha=.15)
        axis.legend(fontsize=8, loc='upper left', bbox_to_anchor=(0, -.19), frameon=False, ncol=2)
    values = frame.accuracy.to_numpy()
    axes[0].set_ylim(max(0, min(values.min(), 1 / 3) - .055), min(1, max(values.max(), .5) + .045))
    axes[0].set_ylabel('Three-class development accuracy')
    figure.suptitle('MultiNLI fixed-package development pilot | seed 2026 | 5760 fit pairs | 256-token cap')
    figure.tight_layout(rect=(0, .12, 1, .94))
    for extension in ['png', 'pdf', 'svg']:
        figure.savefig(output / ('all_rates_and_orders.' + extension), dpi=220, bbox_inches='tight')
    plt.close(figure)
    caption = ('# One-seed learnability pilot figure\n\n'
        'Every declared rate and both orders are retained. Circles/lines average both orders; crosses show individual orders. '
        'The grey series is the untrained mean. The dashed line marks balanced chance, and dotted lines mark the predefined '
        'operational macro and every-genre gates. The separate learning-gain requirement is checked in the selection table. '
        'There is one pilot training seed, so no seed-confidence interval is shown. These repeatedly viewed development '
        'examples are not final confirmation. This combined context/exposure/data-cleaning recipe tests learnability, '
        'not the isolated effect of context length, an adaptive allocation benefit or named-method superiority.\n')
    (output / 'CAPTION.md').write_text(caption)
    print('FULL_NLI_PILOT_GRID_FIGURE_SAVED', flush=True)


if __name__ == '__main__':
    main()
