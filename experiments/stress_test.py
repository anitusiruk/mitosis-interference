import argparse
import copy
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

from signal_scan import (
    seed_all,
    encode,
    trainable_params,
    measure_signals,
    memory_loss,
)


@torch.no_grad()
def accuracy(model, tok, texts, labels, device):
    model.eval()

    correct = 0
    total = 0

    for start in range(0, len(texts), 32):
        t = texts[start:start + 32]
        y = labels[start:start + 32]

        x = encode(tok, t, device)
        logits = model(**x).logits
        pred = logits.argmax(-1).cpu().tolist()

        correct += sum(int(a == b) for a, b in zip(pred, y))
        total += len(y)

    return correct / max(1, total)


def snapshot_trainable(model):
    return {
        name: p.detach().cpu().clone()
        for name, p in model.named_parameters()
        if p.requires_grad
    }


def restore_trainable(model, state):
    with torch.no_grad():
        for name, p in model.named_parameters():
            if p.requires_grad:
                p.copy_(state[name].to(p.device))


def novelize(text):
    suffix = (
        " Additional unrelated context: this message was archived "
        "beside notes about galaxies, telescopes, mountains, "
        "classical music, botanical gardens, planets, and weather."
    )

    return text + suffix


def conflict_label(y):
    # Base experiment uses labels 0..10.
    return (int(y) + 1) % 11


def build_model(device):
    tok = AutoTokenizer.from_pretrained(
        "distilbert-base-uncased"
    )

    base = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=77,
    )

    cfg = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=8,
        lora_alpha=16,
        lora_dropout=0.0,
        target_modules=["q_lin", "v_lin"],
        bias="none",
    )

    model = get_peft_model(base, cfg).to(device)

    return tok, model


def train_baseline(
    model,
    tok,
    train_texts,
    train_labels,
    memory_texts,
    memory_labels,
    device,
    lr,
):
    optimizer = torch.optim.AdamW(
        trainable_params(model),
        lr=lr,
    )

    rng = np.random.default_rng(2026)

    for epoch in range(1, 13):
        order = rng.permutation(len(train_texts))

        model.train()

        for start in range(0, len(order), 16):
            ids = order[start:start + 16]

            texts = [train_texts[i] for i in ids]
            labels = [train_labels[i] for i in ids]

            x = encode(tok, texts, device)
            y = torch.tensor(labels, device=device)

            optimizer.zero_grad(set_to_none=True)

            loss = model(**x, labels=y).loss
            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                trainable_params(model),
                1.0,
            )

            optimizer.step()

        mem_acc = accuracy(
            model,
            tok,
            memory_texts,
            memory_labels,
            device,
        )

        mem_loss = memory_loss(
            model,
            tok,
            memory_texts,
            memory_labels,
            device,
        )

        print(
            f"baseline epoch={epoch} "
            f"memory_acc={mem_acc:.4f} "
            f"memory_loss={mem_loss:.4f}",
            flush=True,
        )

        if epoch >= 3 and mem_acc >= 0.95:
            break

    return optimizer


def adapt_and_measure(
    model,
    tok,
    baseline_state,
    optimizer_state,
    current_texts,
    current_labels,
    memory_texts,
    memory_labels,
    device,
    lr,
    adapt_steps,
):
    restore_trainable(model, baseline_state)

    optimizer = torch.optim.AdamW(
        trainable_params(model),
        lr=lr,
    )

    optimizer.load_state_dict(
        copy.deepcopy(optimizer_state)
    )

    before_loss = memory_loss(
        model,
        tok,
        memory_texts,
        memory_labels,
        device,
    )

    before_acc = accuracy(
        model,
        tok,
        memory_texts,
        memory_labels,
        device,
    )

    signals = measure_signals(
        model=model,
        optimizer=optimizer,
        tok=tok,
        cur_texts=current_texts,
        cur_labels=current_labels,
        mem_texts=memory_texts,
        mem_labels=memory_labels,
        device=device,
        virtual_lr=lr,
    )

    model.train()

    batch_size = 16

    for k in range(adapt_steps):
        start = (k * batch_size) % len(current_texts)

        texts = current_texts[start:start + batch_size]
        labels = current_labels[start:start + batch_size]

        x = encode(tok, texts, device)
        y = torch.tensor(labels, device=device)

        optimizer.zero_grad(set_to_none=True)

        loss = model(**x, labels=y).loss
        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            trainable_params(model),
            1.0,
        )

        optimizer.step()

    after_loss = memory_loss(
        model,
        tok,
        memory_texts,
        memory_labels,
        device,
    )

    after_acc = accuracy(
        model,
        tok,
        memory_texts,
        memory_labels,
        device,
    )

    return {
        **signals,
        "actual_harm": after_loss - before_loss,
        "accuracy_drop": before_acc - after_acc,
        "memory_acc_before": before_acc,
        "memory_acc_after": after_acc,
    }


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--trials", type=int, default=8)
    ap.add_argument("--window-size", type=int, default=64)
    ap.add_argument("--adapt-steps", type=int, default=5)
    ap.add_argument("--lr", type=float, default=2e-4)

    args = ap.parse_args()

    seed_all(args.seed)

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required")

    device = torch.device("cuda")

    print("GPU:", torch.cuda.get_device_name(0), flush=True)
    print("Loading BANKING77...", flush=True)

    ds = load_dataset(
        "PolyAI/banking77",
        trust_remote_code=True,
    )["train"]

    labels = np.asarray(ds["label"])

    # Use only the first 11 intents so label conflict
    # can be manipulated cleanly.
    ids = np.flatnonzero(labels < 11)

    rng = np.random.default_rng(args.seed)
    rng.shuffle(ids)

    memory_ids = ids[:128]
    candidate_ids = ids[128:640]
    train_ids = ids[640:]

    memory_texts = [ds[int(i)]["text"] for i in memory_ids]
    memory_labels = [int(ds[int(i)]["label"]) for i in memory_ids]

    train_texts = [ds[int(i)]["text"] for i in train_ids]
    train_labels = [int(ds[int(i)]["label"]) for i in train_ids]

    tok, model = build_model(device)

    optimizer = train_baseline(
        model,
        tok,
        train_texts,
        train_labels,
        memory_texts,
        memory_labels,
        device,
        args.lr,
    )

    baseline_state = snapshot_trainable(model)
    optimizer_state = copy.deepcopy(
        optimizer.state_dict()
    )

    baseline_acc = accuracy(
        model,
        tok,
        memory_texts,
        memory_labels,
        device,
    )

    print()
    print(
        f"FROZEN BASELINE memory accuracy = {baseline_acc:.4f}",
        flush=True,
    )

    conditions = [
        ("familiar_safe", False, False),
        ("novel_safe", True, False),
        ("familiar_conflict", False, True),
        ("novel_conflict", True, True),
    ]

    rows = []

    for trial in range(args.trials):
        selected = rng.choice(
            candidate_ids,
            size=args.window_size,
            replace=False,
        )

        original_texts = [
            ds[int(i)]["text"]
            for i in selected
        ]

        original_labels = [
            int(ds[int(i)]["label"])
            for i in selected
        ]

        for name, novel, conflict in conditions:
            texts = (
                [novelize(t) for t in original_texts]
                if novel
                else list(original_texts)
            )

            ys = (
                [conflict_label(y) for y in original_labels]
                if conflict
                else list(original_labels)
            )

            result = adapt_and_measure(
                model=model,
                tok=tok,
                baseline_state=baseline_state,
                optimizer_state=optimizer_state,
                current_texts=texts,
                current_labels=ys,
                memory_texts=memory_texts[:64],
                memory_labels=memory_labels[:64],
                device=device,
                lr=args.lr,
                adapt_steps=args.adapt_steps,
            )

            row = {
                "trial": trial,
                "condition": name,
                "novel_factor": int(novel),
                "conflict_factor": int(conflict),
                **result,
            }

            rows.append(row)

            print(
                f"trial={trial:02d} "
                f"{name:18s} "
                f"N={result['novelty']:+.4f} "
                f"G={result['grad_conflict']:+.4f} "
                f"VI={result['virtual_interference']:+.6f} "
                f"H={result['actual_harm']:+.4f} "
                f"dAcc={result['accuracy_drop']:+.4f}",
                flush=True,
            )

    out = Path(
        f"results/stress_seed{args.seed}"
    )

    out.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.DataFrame(rows)

    df.to_csv(
        out / "stress.csv",
        index=False,
    )

    summary = (
        df.groupby("condition")
        [
            [
                "novelty",
                "grad_conflict",
                "virtual_interference",
                "actual_harm",
                "accuracy_drop",
            ]
        ]
        .agg(["mean", "std"])
    )

    print()
    print("=" * 80)
    print("CONTROLLED 2x2 SUMMARY")
    print("=" * 80)
    print(summary.to_string())

    safe = df[df["conflict_factor"] == 0]
    conflict = df[df["conflict_factor"] == 1]

    familiar = df[df["novel_factor"] == 0]
    novel = df[df["novel_factor"] == 1]

    results = {
        "novelty_manipulation_effect_on_novelty": float(
            novel["novelty"].mean()
            - familiar["novelty"].mean()
        ),
        "conflict_effect_on_actual_harm": float(
            conflict["actual_harm"].mean()
            - safe["actual_harm"].mean()
        ),
        "novelty_effect_on_actual_harm": float(
            novel["actual_harm"].mean()
            - familiar["actual_harm"].mean()
        ),
        "conflict_effect_on_grad_conflict": float(
            conflict["grad_conflict"].mean()
            - safe["grad_conflict"].mean()
        ),
        "baseline_memory_accuracy": float(
            baseline_acc
        ),
    }

    print()
    print("=== FACTOR EFFECTS ===")
    print(json.dumps(results, indent=2))

    with open(out / "summary.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
