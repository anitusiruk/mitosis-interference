"""Analyse shadow-mode statistic traces.

For each stream: AUROC of every statistic for detecting the first ``k`` batches
after a true segment change (among eligible batches), its Spearman correlation
with label novelty, the label-group share of the incoming loss at segment
changes, and null-calibrated thresholds (q-quantile over eligible batches of
the i.i.d.-shuffled version of the same stream and seed).
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score

STATS = ["label_novel", "loss_z", "repr_z", "interf_logit", "fresh_util", "interf_proto", "conflict_z"]


def load(path):
    return json.loads(Path(path).read_text())["trigger_records"]


def shift_labels(recs, k=2):
    lab, since = [], 10 ** 9
    for i, r in enumerate(recs):
        if i > 0 and r["seg"] != recs[i - 1]["seg"]:
            since = 0
        lab.append(since < k)
        since += 1
    return np.array(lab)


def thresholds(iid_recs, q):
    out = {}
    for s in STATS:
        v = np.array([r.get(s, np.nan) for r in iid_recs if r["eligible"]], float)
        v = v[~np.isnan(v)]
        out[s] = float(np.quantile(v, q)) if len(v) else float("nan")
    return out


def analyse(recs, k=2):
    y = shift_labels(recs, k)
    el = np.array([r["eligible"] for r in recs])
    res = {}
    for s in STATS:
        v = np.array([r.get(s, np.nan) for r in recs], float)
        v = np.where(np.isnan(v), -np.inf, v)  # undefined statistic = cannot fire
        v = np.where(np.isinf(v), np.nanmin(np.where(np.isinf(v), np.nan, v)) - 1, v) if np.isfinite(v).any() else v
        m = el
        auc = roc_auc_score(y[m], v[m]) if 0 < y[m].sum() < m.sum() else float("nan")
        nov = np.array([r["label_novel"] for r in recs], float)
        rho = spearmanr(v[m], nov[m]).statistic if nov[m].std() > 0 and v[m].std() > 0 else float("nan")
        res[s] = {"auroc_shift": auc, "spearman_with_label_novel": rho}
    b = np.flatnonzero(y & el)
    if len(b):
        g = np.array([recs[i]["loss_group_term"] for i in b])
        w = np.array([recs[i]["loss_within_term"] for i in b])
        res["boundary_loss_group_share"] = float(g.sum() / (g.sum() + w.sum()))
        res["boundary_loss_mean"] = float((g + w).mean())
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="results/tfcl/shadow")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--q", type=float, default=0.99)
    a = ap.parse_args()
    d = Path(a.dir)
    report = {}
    for f in sorted(d.glob(f"*_s{a.seed}.json")):
        if "_iid_" in f.name:
            continue
        name = f.name.replace(f"_s{a.seed}.json", "")
        recs = load(f)
        iid = d / f"{name}_iid_s{a.seed}.json"
        report[name] = analyse(recs)
        if iid.exists():
            report[name]["null_tau"] = thresholds(load(iid), a.q)
    print(json.dumps(report, indent=1))
    (d / f"report_seed{a.seed}.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
