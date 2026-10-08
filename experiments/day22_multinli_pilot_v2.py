"""Declared data preparation and one bounded, fixed-package NLI pilot cell."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import gzip
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import time

import numpy as np

DATA = Path('results/day22_multinli_pilot_data_v2')
SPEC = Path('notes/day22_multinli_learnability_pilot_v2_spec.md')
GENRES = {'A': 'fiction', 'B': 'government', 'C': 'telephone'}
RATES = [5e-5, 2e-4, 8e-4]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def prepare():
    from datasets import load_dataset
    from huggingface_hub import HfApi, hf_hub_download
    from transformers import AutoTokenizer
    from experiments.day7_multinli_data import premise_key
    assert not DATA.exists(), 'Refusing to overwrite prepared data'
    DATA.mkdir()
    revision = HfApi().dataset_info('nyu-mll/multi_nli').sha
    model_revision = json.loads(Path('notes/restart_20261006_preflight.json').read_text())['backbone_revision']
    api = HfApi()
    train_files = [name for name in api.list_repo_files('nyu-mll/multi_nli', repo_type='dataset', revision=revision)
                   if name.startswith('data/train-') and name.endswith('.parquet')]
    assert train_files
    train_paths = [hf_hub_download('nyu-mll/multi_nli', filename=name, repo_type='dataset', revision=revision)
                   for name in train_files]
    dataset = load_dataset('parquet', data_files={'train': train_paths}, split='train')
    pools, pairs, duplicates, ambiguous = defaultdict(list), {}, Counter(), []
    for source_index, row in enumerate(dataset):
        genre, label = row['genre'], int(row['label'])
        if genre not in GENRES.values() or label not in [0, 1, 2]:
            continue
        key = premise_key(row['premise'])
        pair = (key, ' '.join(str(row['hypothesis']).lower().split()))
        item = {'text': [row['premise'], row['hypothesis']], 'label': label,
                'source': row['pairID'], 'source_index': source_index, 'premise_key': key, 'genre': genre}
        if pair not in pairs:
            pairs[pair] = {'first': item, 'labels': {label}, 'sources': [row['pairID']]}
        else:
            pairs[pair]['labels'].add(label)
            pairs[pair]['sources'].append(row['pairID'])
            duplicates[genre] += 1
    removed_ambiguous_rows = 0
    for pair, value in pairs.items():
        if len(value['labels']) > 1:
            ambiguous.append({'normalized_pair_sha256': hashlib.sha256(json.dumps(pair).encode()).hexdigest(),
                              'labels': sorted(value['labels']), 'source_ids': value['sources']})
            removed_ambiguous_rows += len(value['sources'])
            continue
        item = value['first']
        partition = 'dev' if int(item['premise_key'], 16) % 10 == 0 else 'train'
        pools[item['genre'], item['label'], partition].append(item)
    write(DATA / 'ambiguous_pairs_excluded.json', ambiguous)
    rng, dev_rng = np.random.default_rng(2026 + 9000), np.random.default_rng(424242)
    selections, eval_sets = {}, {}
    for concept, genre in GENRES.items():
        dev_rows = []
        for label in range(3):
            rows = pools[genre, label, 'train']
            ids = np.arange(len(rows)); rng.shuffle(ids)
            need = 768 if concept in ['A', 'B'] else 384
            assert len(ids) >= need
            chosen = [rows[int(i)] for i in ids[:need]]
            selections[concept, 1, label] = chosen[:384]
            if concept in ['A', 'B']:
                selections[concept, 2, label] = chosen[384:768]
            rows = pools[genre, label, 'dev']
            ids = np.arange(len(rows)); dev_rng.shuffle(ids)
            assert len(ids) >= 64
            dev_rows.extend(rows[int(i)] for i in ids[:64])
        eval_sets[concept] = dev_rows
    stream = []
    for concept, occurrence in [('A', 1), ('B', 1), ('A', 2), ('C', 1), ('B', 2)]:
        rows = [row for label in range(3) for row in selections[concept, occurrence, label]]
        rng.shuffle(rows)
        for start in range(0, len(rows), 16):
            stream.append({'concept': concept, 'occurrence': occurrence, 'rows': rows[start:start+16]})
    train_rows = [row for batch in stream for row in batch['rows']]
    dev_rows = [row for rows in eval_sets.values() for row in rows]
    assert len(stream) == 360 and len(train_rows) == 5760 and len(dev_rows) == 576
    assert len({row['source'] for row in train_rows}) == 5760
    assert len({row['source'] for row in dev_rows}) == 576
    train_groups, dev_groups = [{row['premise_key'] for row in rows} for rows in [train_rows, dev_rows]]
    assert not train_groups & dev_groups
    assert not {row['source'] for row in train_rows} & {row['source'] for row in dev_rows}
    for concept, occurrence in [('A', 1), ('B', 1), ('A', 2), ('C', 1), ('B', 2)]:
        rows = [row for batch in stream if (batch['concept'], batch['occurrence']) == (concept, occurrence) for row in batch['rows']]
        assert Counter(row['label'] for row in rows) == {0: 384, 1: 384, 2: 384}
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased', revision=model_revision)
    length_summary, length_rows = {}, []
    for partition, rows in [('train', train_rows), ('dev', dev_rows)]:
        lengths = []
        for start in range(0, len(rows), 128):
            part = rows[start:start+128]
            encoded = tokenizer([row['text'][0] for row in part], text_pair=[row['text'][1] for row in part],
                                truncation=False, add_special_tokens=True)
            values = [len(ids) for ids in encoded['input_ids']]
            lengths.extend(values)
            length_rows.extend({'partition': partition, 'source': row['source'], 'tokens': n}
                               for row, n in zip(part, values))
        length_summary[partition] = {'n': len(lengths), 'maximum': max(lengths),
            'quantiles_0_25_50_75_100': np.quantile(lengths, [0, .25, .5, .75, 1]).tolist(),
            'fractions_exceeding': {str(limit): float(np.mean(np.asarray(lengths) > limit)) for limit in [64, 128, 256]}}
    assert length_summary['train']['fractions_exceeding']['64'] > 0
    payload = {'stream': stream, 'eval_sets': eval_sets}
    with gzip.open(DATA / 'dataset.json.gz', 'wt') as output:
        json.dump(payload, output, sort_keys=True)
    write(DATA / 'token_lengths.json', length_rows)
    manifest = {'status': 'passed', 'dataset': 'nyu-mll/multi_nli', 'split': 'train',
        'dataset_revision': revision, 'dataset_fingerprint': dataset._fingerprint,
        'model_revision': model_revision, 'official_validation_or_test_loaded': False,
        'development_previously_viewed': True, 'pilot_seed': 2026,
        'train_examples': 5760, 'development_examples': 576, 'train_dev_premise_overlap': 0,
        'train_dev_source_overlap': 0, 'training_unique_source_ids': 5760,
        'duplicate_normalized_pairs_beyond_first_by_genre': dict(duplicates),
        'ambiguous_normalized_pairs_excluded': len(ambiguous), 'ambiguous_rows_excluded': removed_ambiguous_rows,
        'ambiguous_pairs_receipt_sha256': sha(DATA / 'ambiguous_pairs_excluded.json'),
        'train_only_parquet_sources': [{'filename': name, 'sha256': sha(Path(path))} for name, path in zip(train_files, train_paths)],
        'earlier_failed_preparation': 'results/day22_multinli_pilot_data/failed_preparation.json',
        'max_length': 256, 'length_summary': length_summary, 'source_sha256': sha(Path(__file__)),
        'spec_sha256': sha(SPEC), 'dataset_payload_sha256': sha(DATA / 'dataset.json.gz'),
        'token_lengths_sha256': sha(DATA / 'token_lengths.json'),
        'stream_sha256': hashlib.sha256(json.dumps(stream, sort_keys=True).encode()).hexdigest(),
        'development_sha256': hashlib.sha256(json.dumps(eval_sets, sort_keys=True).encode()).hexdigest()}
    write(DATA / 'manifest.json', manifest)
    print('NLI_PILOT_DATA_PREPARED', json.dumps(manifest), flush=True)


def run(args):
    import pandas as pd
    import torch
    import torch.nn.functional as functional
    from peft import LoraConfig, TaskType, get_peft_model
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from experiments.day2_predictor_scan_rngsafe import capture_rng_state, restore_rng_state
    from experiments.day7_multinli_data import PairTokenizer
    from experiments.day7_multinli_recurrence import checkpoint
    from experiments.signal_scan import seed_all
    from src.adapter_pool_cau_v1 import CAUV1AdapterPool

    torch.set_num_threads(8)
    seed_all(2026)
    manifest = json.loads((DATA / 'manifest.json').read_text())
    assert manifest['status'] == 'passed' and manifest['source_sha256'] == sha(Path(__file__))
    assert manifest['spec_sha256'] == sha(SPEC) and manifest['dataset_payload_sha256'] == sha(DATA / 'dataset.json.gz')
    with gzip.open(DATA / 'dataset.json.gz', 'rt') as source:
        payload = json.load(source)
    keys = [('A', 1), ('B', 1), ('A', 2), ('C', 1), ('B', 2)] if args.order == 'canonical' else [('B', 1), ('A', 1), ('B', 2), ('C', 1), ('A', 2)]
    stream = [batch for key in keys for batch in payload['stream'] if (batch['concept'], batch['occurrence']) == key]
    assert len(stream) == 360
    if args.mode == 'timing':
        assert args.order == 'canonical' and args.learning_rate == 2e-4
        stream = stream[:32]
    output = Path(args.output)
    output.mkdir(exist_ok=False)
    started = time.monotonic()
    deadline = datetime.now(timezone.utc) + timedelta(seconds=1380)
    assert torch.cuda.is_available()
    torch.cuda.reset_peak_memory_stats()
    revision = manifest['model_revision']
    raw_tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased', revision=revision)

    class LongPairTokenizer(PairTokenizer):
        def __call__(self, texts, **kwargs):
            if kwargs.get('truncation'):
                kwargs['max_length'] = 256
            return super().__call__(texts, **kwargs)

    tokenizer = LongPairTokenizer(raw_tokenizer)
    texts = [row['text'] for row in stream[0]['rows']]
    actual = tokenizer(texts, padding=True, truncation=True, max_length=64, return_tensors='pt')
    expected = raw_tokenizer([text[0] for text in texts], text_pair=[text[1] for text in texts],
                            padding=True, truncation=True, max_length=256, return_tensors='pt')
    assert set(actual) == set(expected) and all(torch.equal(actual[key], expected[key]) for key in actual)
    assert actual['input_ids'].shape[1] > 64, 'Context override smoke check needs a long first batch'
    base = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=3, revision=revision)
    assert getattr(base.config, '_commit_hash', None) == revision
    config = LoraConfig(task_type=TaskType.SEQ_CLS, r=8, lora_alpha=16, lora_dropout=0.,
                        target_modules=['q_lin', 'v_lin'], bias='none')
    model = get_peft_model(base, config).to('cuda')
    pool = CAUV1AdapterPool(model=model, tokenizer=tokenizer, lora_config=config, device=torch.device('cuda'),
        lr=args.learning_rate, memory_size=512, memory_probe=64, threshold=0., confidence_z=1.96, seed=2026)
    optimizer = pool.states['default'].optimizer
    assert len(optimizer.param_groups) == 1
    group = optimizer.param_groups[0]
    assert group['lr'] == args.learning_rate and group['betas'] == (.9, .999) and group['eps'] == 1e-8 and group['weight_decay'] == .01
    provenance = {'args': vars(args), 'data_manifest': manifest, 'pair_tokenization_smoke_passed': True,
        'actual_max_length': 256, 'three_class_full_space': True, 'single_fixed_package': True,
        'rehearsal_updates': 0, 'source_sha256': sha(Path(__file__)), 'spec_sha256': sha(SPEC),
        'packages': {p: metadata.version(p) for p in ['torch', 'transformers', 'peft', 'datasets', 'numpy', 'pandas']},
        'optimizer': {'lr': group['lr'], 'betas': group['betas'], 'eps': group['eps'], 'weight_decay': group['weight_decay']},
        'gpu': torch.cuda.get_device_name(0), 'training_seed': 2026}
    write(output / 'provenance.json', provenance)
    evaluation, events = [], []
    train_seconds, evaluation_seconds = 0., 0.

    def evaluate(label, step):
        nonlocal evaluation_seconds
        phase = time.monotonic()
        rng = capture_rng_state()
        modes = [(module, module.training) for module in model.modules()]
        try:
            model.eval()
            with (output / 'development_predictions.jsonl').open('a') as predictions:
                for concept, rows in payload['eval_sets'].items():
                    losses, correct, counts = [], Counter(), Counter()
                    for start in range(0, len(rows), 32):
                        part = rows[start:start+32]
                        x = tokenizer([row['text'] for row in part], padding=True, truncation=True, max_length=256, return_tensors='pt').to('cuda')
                        y = torch.tensor([row['label'] for row in part], device='cuda')
                        with torch.no_grad():
                            logits = model(**x).logits
                            loss = functional.cross_entropy(logits, y, reduction='none')
                        assert logits.shape[1] == 3 and torch.isfinite(logits).all() and torch.isfinite(loss).all()
                        losses.extend(loss.cpu().tolist())
                        for row, scores, prediction in zip(part, logits.cpu().tolist(), logits.argmax(-1).cpu().tolist()):
                            counts[row['label']] += 1
                            correct[row['label']] += int(prediction == row['label'])
                            predictions.write(json.dumps({'checkpoint': label, 'step': step, 'concept': concept,
                                'source': row['source'], 'premise_key': row['premise_key'], 'label': row['label'], 'logits': scores}) + '\n')
                    assert counts == {0: 64, 1: 64, 2: 64}
                    evaluation.append({'checkpoint': label, 'step': step, 'concept': concept, 'n': len(rows),
                        'loss': float(np.mean(losses)), 'accuracy': sum(correct.values()) / len(rows),
                        **{f'class_{c}_accuracy': correct[c] / counts[c] for c in range(3)}})
            pd.DataFrame(evaluation).to_csv(output / 'eval_matrix.csv', index=False)
        finally:
            for module, mode in modes:
                module.training = mode
            restore_rng_state(rng)
        evaluation_seconds += time.monotonic() - phase

    evaluate('initial', 0)
    status = 'completed'
    with (output / 'events.jsonl').open('x') as event_log:
        for step, batch in enumerate(stream, 1):
            if datetime.now(timezone.utc) >= deadline:
                status = 'deadline_stopped'
                break
            phase = time.monotonic()
            loss = pool.train_step('default', [row['text'] for row in batch['rows']], [row['label'] for row in batch['rows']])
            torch.cuda.synchronize()
            train_seconds += time.monotonic() - phase
            assert np.isfinite(loss)
            row = {'step': step, 'concept': batch['concept'], 'occurrence': batch['occurrence'], 'loss': loss,
                   'elapsed_seconds': time.monotonic() - started, 'gpu_peak_allocated_bytes': torch.cuda.max_memory_allocated()}
            events.append(row); event_log.write(json.dumps(row) + '\n'); event_log.flush()
            if step % 16 == 0:
                print('PILOT_STEP', step, 'elapsed', round(row['elapsed_seconds'], 2), flush=True)
            end = step == len(stream) or (batch['concept'], batch['occurrence']) != (stream[step]['concept'], stream[step]['occurrence'])
            if end:
                evaluate('prefix_end' if args.mode == 'timing' else f"{batch['concept']}{batch['occurrence']}", step)
    pd.DataFrame(events).to_csv(output / 'training.csv', index=False)
    checkpoint(pool, output, 'default', len(events))
    elapsed = time.monotonic() - started
    summary = {'status': status, 'steps': len(events), 'expected_steps': len(stream), 'learning_updates': pool.states['default'].updates,
        'training_examples': len(events) * 16, 'train_seconds': train_seconds, 'evaluation_seconds': evaluation_seconds,
        'elapsed_seconds': elapsed, 'gpu_peak_allocated_bytes': torch.cuda.max_memory_allocated(),
        'adapters': sorted(pool.states), 'official_validation_or_test_loaded': False, 'pilot_not_confirmation': True,
        'predictions_sha256': sha(output / 'development_predictions.jsonl')}
    if args.mode == 'timing':
        other = max(0., elapsed - train_seconds - evaluation_seconds)
        projection = 1.5 * (360 / 32 * train_seconds + 3 * evaluation_seconds + other)
        summary.update(projected_full_seconds_with_margin=projection,
                       compute_admitted=status == 'completed' and len(events) == 32 and projection < 600 and summary['gpu_peak_allocated_bytes'] < 4 * 1024**3,
                       admission_uses_learning_outcomes=False)
    write(output / 'summary.json', summary)
    assert status == 'completed' and len(events) == len(stream), 'Incomplete pilot is retained and cannot enter selection'
    print('NLI_SINGLE_PILOT_COMPLETE', json.dumps(summary), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['prepare', 'timing', 'pilot'], required=True)
    parser.add_argument('--output')
    parser.add_argument('--learning-rate', type=float, choices=RATES, default=2e-4)
    parser.add_argument('--order', choices=['canonical', 'b_first'], default='canonical')
    args = parser.parse_args()
    if args.mode == 'prepare':
        prepare()
    else:
        assert args.output
        run(args)


if __name__ == '__main__':
    main()
