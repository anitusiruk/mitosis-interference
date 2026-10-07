"""Refresh the working draft from saved diagnostic evidence, never training data."""
import hashlib
import json
from pathlib import Path

import pandas as pd

from experiments.day5_report import markdown_table


EXPECTED_DRAFT = '2a3158350c783920f36c217f738c8061796b78beecaab5115d7cec3a0d2306a6'


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError('Working draft changed; inspect before applying the editorial update')
    return text.replace(old, new, 1)


def table(path, condition=None, columns=None):
    p = Path(path)
    if not p.exists():
        return 'Pending: no saved verified comparison.'
    try:
        frame = pd.read_csv(p)
    except pd.errors.EmptyDataError:
        return 'Pending: no complete comparison group.'
    if condition is not None:
        frame = frame.loc[condition(frame)]
    if frame.empty:
        return 'Pending: no complete paired-seed comparison.'
    return markdown_table(frame if columns is None else frame[columns])


def main():
    paper = Path('notes/paper_working_draft.md')
    if hashlib.sha256(paper.read_bytes()).hexdigest() != EXPECTED_DRAFT:
        raise RuntimeError('Refusing to overwrite an independently edited manuscript')
    evidence = pd.read_csv('results/day10_initial_loss_comparison.csv')
    unique = evidence.drop_duplicates(['regime', 'architecture', 'seed'])
    if len(unique) != 12 or set(unique.seed) != {2026, 2027, 2028}:
        raise RuntimeError('All twelve frozen ranking controls are required')
    for name, expected in [('day8', 44), ('day12', 11)]:
        records = json.loads(Path('logs', name + '_queue_status.json').read_text())
        if sum(r['status'] == 'completed' for r in records) != expected:
            raise RuntimeError('Frozen control coverage changed: ' + name)
    records = json.loads(Path('logs/day14_fixed_memory_routing_status.json').read_text())
    if len(records) != 44 or any(r['status'] != 'completed' for r in records):
        raise RuntimeError('All fixed-memory routing reloads are required')
    new_status = json.loads(Path('notes/day15_16_execution_status.json').read_text())
    coverage = {day: sum(r['status'] == 'completed' for r in new_status['jobs'] if r['study'] == day)
                for day in [15, 16]}
    verified = len(list(Path('results').glob('day15_*_weight_moments/observer_verification.json')))
    if verified != coverage[15]:
        raise RuntimeError('Execution and verified-observer coverage disagree')
    text = paper.read_text()
    text = replace_once(text,
        "Initial-loss ranking preserves the original pilot's decisions despite omitting the prospective learning-gain term from action ranking.",
        'Initial-loss ranking preserves BANKING decisions across three canonical-order development seeds, '
        'but changes decisions on the third Amazon seed. Learning-gain relevance is therefore regime-dependent.')
    text = replace_once(text,
        'A future weight-only/moment-only factorial is required for their separate attribution.',
        'The separately preregistered four-factor extension crosses LoRA weights, classifier weights, '
        'LoRA AdamW state and classifier AdamW state in all sixteen cells. Every mature incoming batch '
        'and both complementary query folds are retained. It additionally decomposes full-space '
        'cross entropy into label-group probability loss and conditional within-group loss, using '
        'evaluator-only group metadata. These are known probability identities, consistent with the '
        'WP/TP factorization in Kim et al. (2022, 2023), not new theory. Only observers that reproduce '
        'their full reference learner state and adapter tensors bitwise enter the analysis.')
    text = replace_once(text,
        'The four original pre-update-ranking pilots reproduce their original structural decisions. Prospective protected-memory checks remain in those pilots, so the finding concerns the action-ranking learning-gain term and does not demonstrate that all lookahead is unnecessary or that runtime improves.',
        'All twelve frozen initial-loss ranking controls are complete: BANKING/Amazon, private/head-only, '
        'and canonical-order seeds 2026–2028. BANKING has zero allocation disagreements in all six '
        'comparisons. Amazon has zero in seeds 2026 and 2027, but 24 head-only and 30 private-package '
        'decision disagreements in seed 2028. Under last-active prediction, the seed-2028 head-only '
        'initial-loss and prospective-ranking accuracies are 77.34% and 79.95%; private-package '
        'accuracies are 84.11% and 83.33%. These are individual development-seed results, not '
        'seed-cluster significance claims. Prospective protected-memory checks remain in both '
        'conditions. The finding concerns ranking only and supports neither removal of all lookahead '
        'nor a runtime improvement claim.\n\n' + markdown_table(unique[
            ['regime', 'architecture', 'seed', 'allocation_disagreements']]))
    text = replace_once(text,
        'Fixed-memory replications and the larger fixed-capacity baseline remain **pending final analysis**. The rank-96 original pilot under the fixed training recipe performs poorly. This is a parameter sensitivity, not evidence that a properly tuned larger static alternative is inferior. Its training hyperparameters need a baseline tuning study with pilot/confirmation separation; no outcome-selected favorable rank or final-data tuning is justified.',
        'All 44 fixed-memory trajectories, all 44 fixed-memory router reloads, and all 11 rank-96 '
        'capacity trajectories are complete. The 512-total-text budget controls retained training '
        'examples and caps pools at eight; it does not equalize model parameters, optimizer state '
        'or prediction compute. Fixed versus per-adapter memory changes the private BANKING '
        'centroid accuracy by +0.38 points (descriptive interval [0.12, 0.64]); Amazon changes are '
        'small and uncertain. With this fixed text budget, private learned hard routing exceeds '
        'the fixed rank-8 single by +5.35 points on BANKING ([0.82, 9.88]); probability mixture '
        'gives +5.40 ([0.67, 10.14]). Amazon differences are -2.24 ([-5.97, 1.49]) and '
        '-1.80 ([-4.40, 0.81]). All are development-stage descriptive five-seed comparisons, '
        'with orders averaged inside seeds. The routing extension was introduced after earlier '
        'deployment failure.\n\nThe larger static rank-96 baseline remains untuned: its final accuracy '
        'is lower than rank 8 by 9.46 points ([-14.06, -4.86]) under the fixed recipe. Rank 96 '
        'has 2,419,277 adaptation parameters, compared with 2,391,783 for three rank-8 private '
        'packages; this is a particular storage scale, not universal resource matching. Poor '
        'untuned performance cannot support superiority over a properly tuned static alternative. '
        'A matched baseline tuning study with pilot/confirmation separation remains necessary.')
    text = replace_once(text,
        'Modern source-faithful method baselines, larger natural same-label adaptation regimes, separate classifier-weight/moment attribution and final evaluation are outstanding.',
        'Modern source-faithful method baselines, larger natural same-label adaptation regimes '
        'and complete-method confirmation evaluation remain outstanding. Separate classifier '
        'weight/state attribution and BERT transfer are tracked below; coverage alone does not '
        'establish a general mechanism.')
    text = replace_once(text,
        '## Figures and result sources',
        '## 7. Preregistered development extensions\n\n'
        f'The separate weight/state audit has {coverage[15]}/20 verified trajectories. '
        f'The BERT allocation transfer study has {coverage[16]}/20 completed trajectories. '
        'Every failed or incomplete attempt remains recorded. Empty comparisons are pending '
        'and unpaired orders are excluded from seed intervals.\n\n'
        'The BERT check changes the backbone, tokenizer, representations, frozen pooler and '
        'classifier together. It uses a single linear classifier rather than the DistilBERT '
        'trainable pre-classifier/classifier stack, but is not a causal isolation of classifier '
        'design or a tuned BERT performance comparison.\n\n'
        + table('results/day16_bert_allocation_pairs.csv') + '\n\n'
        'The following table retains all four marginal reset factors, both regimes, and each '
        'declared metric. Positive contrasts mean lower initial/post-update loss or greater '
        'local learning gain after reset. Conditional cells and interactions are in the full '
        'Day-15 report. These averages describe the actual active source, not a retrospectively '
        'chosen best feasible reuse candidate. The interval unit is a paired training seed; '
        'the fixed development examples do not supply population-sampling uncertainty.\n\n'
        + table('results/day15_seed_intervals.csv', lambda d: d.kind == 'marginal',
                ['regime', 'factor', 'metric', 'n_seeds', 'mean', 'ci_low', 'ci_high']) + '\n\n'
        '## 8. Related work and contribution boundary\n\n'
        'Classifier recency bias is established in Supervised Contrastive Replay (Mai et al., '
        '2021), which studies replacing softmax classifiers with nearest-class-mean prediction. '
        'Logit and parameter calibration are also established in NLP continual learning '
        '(Li et al., 2022, LPC). Kim et al. (2022) decompose class-incremental prediction into '
        'within-task and task-id prediction; Kim et al. (2023), Eq.1, restate that factorization. '
        'Neither recognizing classifier bias nor the label-group loss identity is our contribution.\n\n'
        'Wang et al. (2026, Predicting Plasticity) already distinguish initial loss from normalized '
        'future optimization gain. Lyle et al. (2025) study multiple causes of plasticity loss; '
        'Hernandez-Garcia et al. (2026) compare weight and unit reinitialization. Prospective '
        'optimization consequences, factorial diagnosis, and reset benefits are established. '
        'The candidate contribution is an operational empirical audit of how classifier-bearing '
        'allocation packages select resources, with optimizer-state attribution, cross-backbone '
        'checks, deployment/resource controls, and explicit failure conditions. Novelty remains '
        'provisional without the comparator and stronger-regime evidence.\n\n'
        'Primary source links and precise scope are in `notes/novelty_audit_20261006.md` and '
        '`notes/classifier_prior_audit_20261006.md`.\n\n'
        '## Figures and result sources')
    tuning_status = Path('notes/day17_static_tuning_execution.json')
    if tuning_status.exists():
        state = json.loads(tuning_status.read_text())
        pilots = sum(r['phase'] == 'pilot' and r['status'] == 'completed' for r in state['jobs'])
        confirmations = sum(r['phase'] == 'confirmation' and r['status'] == 'completed' for r in state['jobs'])
        addition = ('## 9. Equal-grid tuning of static baselines\n\n'
            f'The baseline repair has {pilots}/24 pilot trajectories and '
            f'{confirmations}/20 paired development confirmations. '
            'Ranks 8 and 96 receive the same six-rate, two-order pilot grid. Each rank\'s rate '
            'is selected using only seed 2026, then committed before seeds 2027–2031. '
            'The existing adaptive outcomes and fixed development examples had already been '
            'examined. This addresses learning-rate tuning within a declared grid, not an '
            'untouched final evaluation or exhaustive hyperparameter search.\n\n'
            + table('results/day17_tuned_static_paired_differences.csv') + '\n\n'
            'All static ranks and adaptive rules are retained, with both orders averaged within '
            'each seed. Actual parameter storage, optimizer state and prediction compute remain '
            'different resources. The full grid, every trajectory, selected rates and resource '
            'counts are in `notes/day17_static_tuning_results.md`.\n\n')
        text = replace_once(text, '## Figures and result sources', addition + '## Figures and result sources')
        if state.get('complete'):
            text = replace_once(text,
                'A matched baseline tuning study with pilot/confirmation separation remains necessary.',
                'The subsequent equal-grid rate study below addresses this tuning gap within '
                'its declared development protocol. Broader hyperparameter choices and final '
                'complete-method confirmation remain untested.')
    # Cross-check rounded editorial figures against the complete tables.
    memory = pd.read_csv('results/day8_memory_paired_differences.csv')
    row = memory[(memory.regime == 'banking') & (memory.architecture == 'private')
                 & (memory.rule == 'frozen_centroid')].iloc[0]
    if abs(row['mean'] - .00377) > .00001:
        raise RuntimeError('Fixed-memory editorial values no longer match saved evidence')
    comparisons = pd.read_csv('results/day14_memory_routing_paired_differences.csv')
    row = comparisons[(comparisons.regime == 'banking') & (comparisons.architecture == 'private')
                      & (comparisons.rule == 'linear_hard') & (comparisons.contrast == 'fixed_minus_single')].iloc[0]
    if abs(row['mean'] - .053512) > .000001:
        raise RuntimeError('Router editorial values no longer match saved evidence')
    paper.write_text(text)
    Path('notes/manuscript_refresh_receipt.json').write_text(json.dumps({
        'previous_manuscript_sha256': EXPECTED_DRAFT,
        'new_manuscript_sha256': hashlib.sha256(paper.read_bytes()).hexdigest(),
        'diagnostic_coverage': coverage,
        'training_or_test_data_accessed': False,
        'scope': 'editorial refresh from existing saved development evidence'}, indent=2) + '\n')
    print('MANUSCRIPT_EVIDENCE_REFRESH_SAVED', coverage, flush=True)


if __name__ == '__main__':
    main()
