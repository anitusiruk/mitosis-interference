"""Add estimator and cross-backbone disclosure to the evidence-refreshed draft."""
import hashlib
import json
from pathlib import Path

import pandas as pd
from experiments.day5_report import markdown_table


def replace_once(text, old, new):
    assert text.count(old) == 1, 'Inspect an independently changed draft before editing'
    return text.replace(old, new, 1)


def main():
    paper = Path('notes/paper_working_draft.md')
    previous = hashlib.sha256(paper.read_bytes()).hexdigest()
    receipt = json.loads(Path('notes/manuscript_refresh_receipt.json').read_text())
    assert receipt['new_manuscript_sha256'] == previous
    text = paper.read_text()
    text = replace_once(text,
        'rather than a need for additional representation capacity.',
        'rather than a need for additional low-rank adaptation capacity.')
    text = replace_once(text,
        'The head-only control keeps all LoRA outputs exactly zero and trains only private classifiers.',
        'The control named head-only keeps all LoRA outputs exactly zero and trains '
        'the private pre-classifier/classifier stack. Its hidden pre-classifier is '
        'a learned representation transform; this control rules out a need for '
        'LoRA in the observed allocation decisions, not all hidden representation learning.')
    text = replace_once(text,
        'Matched component interventions show substantial classifier-reset effects on a BANKING recurrence stream.',
        'Matched component interventions show classifier-reset effects at the original BANKING '
        'allocation windows; the broader all-mature-batch audit separately measures effects '
        'across the continuing trajectory.')
    text = replace_once(text,
        'Across five fresh seeds and two orders, a classifier-only allocator makes the same structural decisions as the full adapter allocator on BANKING, although training low-rank parameters improves prediction.',
        'Across five development training seeds and two orders, a classifier-only allocator '
        'makes the same structural decisions as the full adapter allocator on BANKING, '
        'although training low-rank parameters improves prediction. The BERT transfer '
        'diagnostic also preserves allocation decisions under its declared recipe.')
    anchor = ('The interval unit is a paired training seed; '
              'the fixed development examples do not supply population-sampling uncertainty.')
    text = replace_once(text, anchor, anchor + '\n\n'
        'The all-mature-batch marginal effects average all eight settings of the other '
        'three reset factors and all eligible batches. They are a different estimand '
        'from fresh-package versus best-feasible-reuse advantage at allocation windows. '
        'Their signs need not agree. These measurements do not imply that resetting '
        'a trained classifier generally improves prediction. Conditional contrasts '
        'retain the artificial inherited-state/reset-weight combinations; useful '
        'deployment recipes require separate closed-loop experiments.')
    anchor = ('classifier together. It uses a single linear classifier rather than the DistilBERT '
              'trainable pre-classifier/classifier stack, but is not a causal isolation of classifier '
              'design or a tuned BERT performance comparison.')
    differences = pd.read_csv('results/day16_bert_paired_differences.csv')
    assert len(differences) == 6 and set(differences.seed_clusters) == {5}
    text = replace_once(text, anchor, anchor + '\n\n'
        'All cross-backbone prediction differences are reported below. Negative '
        'values indicate lower BERT accuracy. The cross-backbone changes are joint '
        'changes in architecture and initialized packages, not an optimized '
        'performance comparison or a classifier-only causal attribution.\n\n'
        + markdown_table(differences))
    qc = json.loads(Path('notes/factorial_receipt_integrity_final.json').read_text())
    assert not qc['failed']
    anchor = '## Figures and result sources'
    text = replace_once(text, anchor,
        '## Independent saved-receipt quality control\n\n'
        f'A read-only check of {len(qc["passed"])} completed observer trajectories '
        'verified every eligible mature batch, the actual active source, all sixteen '
        'intervention cells and both query folds, weight/state receipt isolation, '
        'bitwise invariance of initial predictions to optimizer-state interventions, '
        'and query-loss/component identities. This additional quality-control check '
        'was added after the first observer outcomes. It changes neither the frozen '
        'experiments nor their contrast definitions and is not a new scientific '
        'replication. Earlier and final receipts are preserved.\n\n' + anchor)
    retention = pd.read_csv('results/day18_retention_paired_differences.csv')
    drops = retention[retention.metric == 'maximum_seen_checkpoint_drop']
    assert len(drops) >= 6
    text = replace_once(text, anchor,
        '## Secondary deployed-retention analysis\n\n'
        'An analysis added after primary outcomes uses all five saved segment-end '
        'checkpoints and all three original deployment rules. It compares fixed-memory '
        'adaptive trajectories with the frozen static reference and every available '
        'pilot-selected static rank on exactly paired streams. For each concept, the '
        'observed checkpoint drop is its maximum accuracy after first exposure minus '
        'its final accuracy; the statistic is averaged over concepts. Positive '
        'adaptive-minus-static differences below indicate more drop for the adaptive '
        'predictor. These are descriptive five-seed development summaries, not '
        'retention guarantees or independently confirmed hypotheses.\n\n'
        + markdown_table(drops) + '\n\n'
        'The full report also retains final accuracy, the mean seen-concept '
        'checkpoint accuracy and final-minus-first-exposure accuracy. Recurrence '
        'contributes to the latter, so it is not standard backward transfer for '
        'a nonrecurring task sequence. Fixed-memory learned routers have only final '
        'reload measurements; their temporal retention is unavailable and is not '
        'imputed. Definitions, all comparisons and source hashes are in '
        '`notes/day18_deployment_retention_results.md`.\n\n' + anchor)
    control_path = Path('notes/day19_linear_classifier_execution.json')
    if control_path.exists():
        control = json.loads(control_path.read_text())
        complete = sum(r['phase'] == 'diagnostic' and r['status'] == 'completed' for r in control['jobs'])
        pairs = pd.read_csv('results/day19_linear_classifier_allocation_pairs.csv') if complete else pd.DataFrame()
        differences = pd.read_csv('results/day19_linear_classifier_prediction_differences.csv') if complete else pd.DataFrame()
        text = replace_once(text, anchor,
            '## Within-backbone output-classifier control\n\n'
            'The original head-only DistilBERT control includes a learned hidden '
            'pre-classifier. A separately declared development extension freezes '
            'that layer in both LoRA-plus-output-classifier and output-classifier-only '
            'learning. It retains the DistilBERT backbone, initialization, stream, '
            'allocator, optimizer rate, clipping and memory condition. It removes '
            'hidden pre-classifier learning and its optimizer state together; it '
            'is not a weight-versus-state factorial for that layer. PEFT stores '
            'dormant pre-classifier copies, which remain counted in storage.\n\n'
            f'The extension completed {complete}/20 research trajectories and '
            f'{len(pairs)}/10 allocation pairs. Its unchanged-wrapper replay and '
            'tiny CPU/CUDA intervention gates precede the research runs. The '
            'following tables retain every completed pair and every original '
            'prediction rule; these are repeatedly examined development streams, '
            'not untouched confirmation or tuned competitive performance.\n\n'
            + markdown_table(pairs) + '\n\n' + markdown_table(differences) + '\n\n'
            'All deviations from the trainable-stack references, each trajectory '
            'and stored frozen versus output-classifier parameters are in '
            '`notes/day19_linear_classifier_results.md`.\n\n' + anchor)
    paper.write_text(text)
    Path('notes/manuscript_evidence_caveats_receipt.json').write_text(json.dumps({
        'previous_manuscript_sha256': previous,
        'new_manuscript_sha256': hashlib.sha256(paper.read_bytes()).hexdigest(),
        'saved_observers_independently_checked': len(qc['passed']),
        'scope': 'estimator distinction, full cross-backbone results, post-outcome quality-control disclosure',
        'training_outputs_modified': False}, indent=2) + '\n')
    print('EVIDENCE_ESTIMATOR_AND_TRANSFER_CAVEATS_SAVED', flush=True)


if __name__ == '__main__':
    main()
