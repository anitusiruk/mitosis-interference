"""Meaningful CPU/GPU checks for the four-factor causal audit."""
import argparse
import torch
from transformers import DistilBertConfig, DistilBertForSequenceClassification
from peft import LoraConfig, TaskType, get_peft_model

from experiments.signal_scan import seed_all, encode
from experiments.day3_action_utility_unit import nested_equal
from experiments.day5_shared_head_integrity import Tokenizer, snapshot, check
from src.adapter_pool_cau_v1 import CAUV1AdapterPool
from src.component_intervention_audit import component_trial
from src.moment_component_audit import CELLS, FACTORS, moment_trial, crossfit_moments


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cpu')
    args = parser.parse_args()
    torch.set_num_threads(2)
    seed_all(2032)
    device = torch.device(args.device)
    model = DistilBertForSequenceClassification(DistilBertConfig(vocab_size=64, dim=32,
        hidden_dim=64, n_heads=4, n_layers=2, num_labels=3,
        dropout=.1, attention_dropout=.1, seq_classif_dropout=.1))
    cfg = LoraConfig(task_type=TaskType.SEQ_CLS, r=2, lora_alpha=4, lora_dropout=0.,
                     target_modules=['q_lin', 'v_lin'], bias='none')
    model = get_peft_model(model, cfg).to(device)
    pool = CAUV1AdapterPool(model=model, tokenizer=Tokenizer(), lora_config=cfg, device=device,
        lr=2e-4, memory_size=16, memory_probe=4, threshold=0., seed=2032)
    texts, labels = ['good item', 'bad item', 'new item', 'old item'], [0, 1, 2, 0]
    for _ in range(3):
        pool.train_step('default', texts, labels)
    pool.warmup_name = None
    # Deliberately preserve stale gradients, mixed module modes and inactive state.
    before = snapshot(pool)
    trials = []
    for cell in CELLS:
        trials.append(moment_trial(pool, 'default', texts, labels, texts, labels, cell))
        check(str(tuple(cell.values())) + ' restores complete live state', nested_equal(before, snapshot(pool)))
    check('all 16 cells exist exactly once', len({tuple(r[k] for k in FACTORS) for r in trials}) == 16)
    for kind in ['head', 'lora']:
        for reset in [False, True]:
            matching = [r for r in trials if r[f'reset_{kind}_weights'] == reset]
            check(kind + f' matched initializer {reset}', len({r[kind + '_initial_weights_sha256'] for r in matching}) == 1)
        check(kind + ' optimizer transport is independent of weights',
              len({r[kind + '_initial_optimizer_sha256'] for r in trials if not r[f'reset_{kind}_optimizer']}) == 1)
        check(kind + ' empty optimizer state is empty in every cell',
              all(r[kind + '_inherited_state_parameters'] == 0 for r in trials if r[f'reset_{kind}_optimizer']))
        check(kind + ' inherited state is present even with reset weights',
              all(r[kind + '_inherited_state_parameters'] > 0 for r in trials if not r[f'reset_{kind}_optimizer']))
    for lora in [False, True]:
        for head in [False, True]:
            matching = [r for r in trials if r['reset_lora_weights'] == lora and r['reset_head_weights'] == head]
            check('moments do not affect initial prediction', len({r['query_before'] for r in matching}) == 1)
            variant = ('fresh' if lora else 'reuse') + '_lora_' + ('fresh' if head else 'inherit') + '_head'
            old = component_trial(pool, 'default', texts, labels, texts, labels, variant)
            new = next(r for r in matching if r['reset_lora_optimizer'] == lora and r['reset_head_optimizer'] == head)
            check('old coupled cell matches ' + variant, abs(old['query_after'] - new['query_after']) < 1e-7)
    inherited = trials[0]
    group_trial = moment_trial(pool,'default',texts,[0,1,1,0],texts,[0,1,1,0],CELLS[0],label_group=[0,1])
    for phase in ['before','after']:
        check('full loss separates class-group mass and conditional loss '+phase,
              abs(group_trial['query_'+phase]-group_trial['group_mass_loss_'+phase]
                  -group_trial['within_group_loss_'+phase])<1e-6)
    check('label-group measurement is non-invasive',nested_equal(before,snapshot(pool)))
    pool.train_step('default', texts, labels)
    model.eval()
    with torch.no_grad():
        actual = float(model(**encode(pool.tok, texts, device), labels=torch.tensor(labels, device=device)).loss)
    check('fully inherited cell equals real optimizer update', abs(actual - inherited['query_after']) < 1e-7)
    before = snapshot(pool)
    records = crossfit_moments(pool, texts + ['fifth item'], labels + [1], 'default')
    for cell in CELLS:
        matching = [r for r in records if all(r[k] == cell[k] for k in FACTORS)]
        check('odd crossfit query partition', sorted(i for r in matching for i in r['query_indices']) == list(range(5)))
    check('crossfit is non-invasive', nested_equal(before, snapshot(pool)))
    backward = crossfit_moments(pool, texts + ['fifth item'], labels + [1], 'default', cells=tuple(reversed(CELLS)))
    key = lambda r: (r['fold'], tuple(r[k] for k in FACTORS))
    check('cell order does not change losses or receipts',
          sorted(records, key=key) == sorted(backward, key=key))
    check('reverse crossfit is non-invasive', nested_equal(before, snapshot(pool)))
    print('DAY15_WEIGHT_MOMENT_INTEGRITY_PASS', args.device, flush=True)


if __name__ == '__main__':
    main()
