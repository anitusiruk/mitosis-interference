import argparse, json, random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def encode(tok, texts, device):
    return tok(
        texts,
        padding=True,
        truncation=True,
        max_length=64,
        return_tensors="pt",
    ).to(device)


def trainable_params(model):
    return [p for p in model.parameters() if p.requires_grad]


def grad_vector(model):
    parts = []
    for p in trainable_params(model):
        if p.grad is None:
            parts.append(torch.zeros_like(p).flatten())
        else:
            parts.append(p.grad.detach().flatten())
    return torch.cat(parts)


def masked_mean(hidden, mask):
    m = mask.unsqueeze(-1).float()
    return (hidden * m).sum(1) / m.sum(1).clamp_min(1.0)


@torch.no_grad()
def base_features(model, tok, texts, device):
    x = encode(tok, texts, device)

    model.eval()
    with model.disable_adapter():
        out = model(
            **x,
            output_hidden_states=True,
            return_dict=True,
        )

    z = masked_mean(out.hidden_states[-1], x["attention_mask"])
    return F.normalize(z, dim=1)


def memory_loss(model, tok, texts, labels, device):
    model.eval()
    x = encode(tok, texts, device)
    y = torch.tensor(labels, device=device)

    with torch.no_grad():
        return float(model(**x, labels=y).loss.item())


class Reservoir:
    def __init__(self, capacity, seed):
        self.capacity = capacity
        self.items = []
        self.seen = 0
        self.rng = random.Random(seed)

    def add(self, text, label):
        self.seen += 1
        item = (text, int(label))

        if len(self.items) < self.capacity:
            self.items.append(item)
            return

        j = self.rng.randrange(self.seen)
        if j < self.capacity:
            self.items[j] = item

    def sample(self, n):
        rows = self.rng.sample(self.items, min(n, len(self.items)))
        return (
            [x[0] for x in rows],
            [x[1] for x in rows],
        )


def measure_signals(
    model, optimizer, tok,
    cur_texts, cur_labels,
    mem_texts, mem_labels,
    device, virtual_lr,
):
    """
    Measures:
      novelty: frozen-base centroid distance
      grad_conflict: negative gradient cosine
      virtual_interference: memory loss increase after a
                            temporary SGD-style LoRA update
    """

    model.eval()

    cur_x = encode(tok, cur_texts, device)
    mem_x = encode(tok, mem_texts, device)

    cur_y = torch.tensor(cur_labels, device=device)
    mem_y = torch.tensor(mem_labels, device=device)

    # -------------------------
    # Current losses
    # -------------------------

    with torch.no_grad():
        cur_loss = float(
            model(**cur_x, labels=cur_y).loss.item()
        )

        mem_before = float(
            model(**mem_x, labels=mem_y).loss.item()
        )

    # -------------------------
    # Novelty
    # -------------------------

    z_cur = base_features(model, tok, cur_texts, device)
    z_mem = base_features(model, tok, mem_texts, device)

    c_cur = F.normalize(z_cur.mean(0), dim=0)
    c_mem = F.normalize(z_mem.mean(0), dim=0)

    novelty = float(
        1.0 - torch.dot(c_cur, c_mem).item()
    )

    # -------------------------
    # Incoming gradient
    # -------------------------

    optimizer.zero_grad(set_to_none=True)

    loss = model(**cur_x, labels=cur_y).loss
    loss.backward()

    g_cur = grad_vector(model).detach()

    # -------------------------
    # Memory gradient
    # -------------------------

    optimizer.zero_grad(set_to_none=True)

    loss = model(**mem_x, labels=mem_y).loss
    loss.backward()

    g_mem = grad_vector(model).detach()

    grad_cos = float(
        F.cosine_similarity(
            g_cur[None],
            g_mem[None],
            dim=1,
        ).item()
    )

    grad_conflict = -grad_cos

    # -------------------------
    # Virtual update
    # -------------------------

    params = trainable_params(model)
    backup = [p.detach().clone() for p in params]

    optimizer.zero_grad(set_to_none=True)

    loss = model(**cur_x, labels=cur_y).loss
    loss.backward()

    with torch.no_grad():
        for p in params:
            if p.grad is not None:
                p.add_(p.grad, alpha=-virtual_lr)

    mem_after = memory_loss(
        model, tok,
        mem_texts, mem_labels,
        device,
    )

    # Restore model exactly
    with torch.no_grad():
        for p, old in zip(params, backup):
            p.copy_(old)

    optimizer.zero_grad(set_to_none=True)
    model.train()

    return {
        "current_loss": cur_loss,
        "memory_loss_before": mem_before,
        "novelty": novelty,
        "grad_cos": grad_cos,
        "grad_conflict": grad_conflict,
        "virtual_interference": mem_after - mem_before,
    }


def make_stream(ds, batch_size, seed):
    rng = np.random.default_rng(seed)

    labels = np.asarray(ds["label"])
    groups = np.array_split(np.arange(77), 7)

    stream = []
    boundaries = []

    for phase, group in enumerate(groups):
        ids = np.flatnonzero(np.isin(labels, group))
        rng.shuffle(ids)

        if phase > 0:
            boundaries.append(len(stream))

        for start in range(0, len(ids), batch_size):
            chunk = ids[start:start + batch_size]

            stream.append({
                "phase": phase,
                "texts": [ds[int(i)]["text"] for i in chunk],
                "labels": [int(ds[int(i)]["label"]) for i in chunk],
            })

    return stream, boundaries


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--probe-every", type=int, default=10)
    ap.add_argument("--horizon", type=int, default=10)
    ap.add_argument("--memory-size", type=int, default=512)
    ap.add_argument("--memory-probe", type=int, default=64)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--virtual-lr", type=float, default=2e-4)
    ap.add_argument("--max-steps", type=int, default=0)
    ap.add_argument("--tag", type=str, default="full")

    args = ap.parse_args()

    seed_all(args.seed)

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available")

    device = torch.device("cuda")
    print("GPU:", torch.cuda.get_device_name(0), flush=True)

    print("Loading BANKING77...", flush=True)
    ds = load_dataset("PolyAI/banking77", trust_remote_code=True)["train"]

    stream, boundaries = make_stream(
        ds,
        args.batch_size,
        args.seed,
    )

    print("steps:", len(stream), flush=True)
    print("hidden boundaries:", boundaries, flush=True)

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

    optimizer = torch.optim.AdamW(
        trainable_params(model),
        lr=args.lr,
    )

    reservoir = Reservoir(
        args.memory_size,
        args.seed + 1,
    )

    rows = []
    pending = []

    for step, batch in enumerate(stream, start=1):

        # --------------------------------
        # Resolve actual future harm
        # --------------------------------

        keep = []

        for item in pending:
            if item["due"] == step:
                future = memory_loss(
                    model,
                    tok,
                    item["texts"],
                    item["labels"],
                    device,
                )

                rows[item["row"]]["future_harm"] = (
                    future - item["baseline"]
                )

            else:
                keep.append(item)

        pending = keep

        # --------------------------------
        # Signal probe BEFORE training
        # --------------------------------

        if (
            step % args.probe_every == 0
            and len(reservoir.items) >= args.memory_probe
        ):
            mt, ml = reservoir.sample(args.memory_probe)

            sig = measure_signals(
                model,
                optimizer,
                tok,
                batch["texts"],
                batch["labels"],
                mt,
                ml,
                device,
                args.virtual_lr,
            )

            boundary_dist = min(
                abs(step - b)
                for b in boundaries
            )

            row = {
                "step": step,
                "true_phase": batch["phase"],
                "distance_to_boundary": boundary_dist,
                **sig,
                "future_harm": np.nan,
            }

            rows.append(row)

            pending.append({
                "row": len(rows) - 1,
                "due": step + args.horizon,
                "texts": list(mt),
                "labels": list(ml),
                "baseline": sig["memory_loss_before"],
            })

            print(
                f"step={step:4d} "
                f"phase(eval)={batch['phase']} "
                f"novelty={sig['novelty']:+.4f} "
                f"conflict={sig['grad_conflict']:+.4f} "
                f"virtualI={sig['virtual_interference']:+.6f}",
                flush=True,
            )

        # --------------------------------
        # Real optimizer update
        # --------------------------------

        model.train()

        x = encode(tok, batch["texts"], device)
        y = torch.tensor(batch["labels"], device=device)

        optimizer.zero_grad(set_to_none=True)

        loss = model(**x, labels=y).loss
        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            trainable_params(model),
            1.0,
        )

        optimizer.step()

        # Diagnostic memory only
        for text, label in zip(
            batch["texts"],
            batch["labels"],
        ):
            reservoir.add(text, label)

        if args.max_steps and step >= args.max_steps:
            print("Reached max-steps.", flush=True)
            break

    out = Path(
        f"results/{args.tag}_seed{args.seed}"
    )

    out.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df.to_csv(out / "signals.csv", index=False)

    print()
    print("DONE")
    print("saved:", out / "signals.csv")


if __name__ == "__main__":
    main()
