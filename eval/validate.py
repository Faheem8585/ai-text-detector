#!/usr/bin/env python3
"""Evaluate the detector against the labelled corpus in eval/samples/.

Computes:
  - accuracy, precision, recall, F1 (at the 0.50 threshold)
  - confusion matrix
  - per-sample scores
  - ROC AUC across all thresholds

Run from the repo root:
    python -m eval.validate
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from app.engine.scorer import analyze  # noqa: E402


SAMPLES_DIR = ROOT / "samples"
THRESHOLD = 0.50


def load_corpus():
    items = []
    for label_name, label in (("human", 0), ("ai", 1)):
        for f in sorted((SAMPLES_DIR / label_name).glob("*.txt")):
            items.append({
                "name": f.name,
                "label": label,
                "label_name": label_name,
                "text": f.read_text(encoding="utf-8").strip(),
            })
    return items


def score_corpus(items):
    for item in items:
        result = analyze(item["text"])
        item["prob"] = result["ai_probability"]
        item["pred"] = 1 if result["ai_probability"] >= THRESHOLD else 0
        item["verdict"] = result["final_verdict"]
        item["layers"] = len(result["layers_triggered"])
    return items


def confusion_matrix(items):
    tp = sum(1 for x in items if x["label"] == 1 and x["pred"] == 1)
    tn = sum(1 for x in items if x["label"] == 0 and x["pred"] == 0)
    fp = sum(1 for x in items if x["label"] == 0 and x["pred"] == 1)
    fn = sum(1 for x in items if x["label"] == 1 and x["pred"] == 0)
    return tp, tn, fp, fn


def metrics(items):
    tp, tn, fp, fn = confusion_matrix(items)
    total = tp + tn + fp + fn
    acc = (tp + tn) / total if total else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return {
        "accuracy": acc, "precision": prec, "recall": rec, "f1": f1,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


def roc_auc(items):
    """Mann-Whitney U based AUC: probability that a random AI sample
    scores higher than a random human sample."""
    pos = [x["prob"] for x in items if x["label"] == 1]
    neg = [x["prob"] for x in items if x["label"] == 0]
    if not pos or not neg:
        return 0.0
    wins = ties = 0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1
            elif p == n:
                ties += 1
    return (wins + 0.5 * ties) / (len(pos) * len(neg))


def print_table(items):
    print(f"\n{'Sample':<25} {'Label':<7} {'Prob':>7} {'Pred':<5} {'Verdict':<24} {'Layers':>6}")
    print("-" * 80)
    for x in items:
        mark = "✓" if x["label"] == x["pred"] else "✗"
        print(f"{x['name']:<25} {x['label_name']:<7} {x['prob']:>7.3f} "
              f"{('AI' if x['pred'] else 'HUMAN'):<5} {x['verdict']:<24} "
              f"{x['layers']:>6} {mark}")


def main():
    items = load_corpus()
    if not items:
        print("No samples found in eval/samples/")
        sys.exit(1)

    print(f"Loaded {len(items)} samples "
          f"({sum(1 for x in items if x['label']==1)} AI, "
          f"{sum(1 for x in items if x['label']==0)} human)")
    print("Scoring...")
    items = score_corpus(items)

    print_table(items)

    m = metrics(items)
    auc = roc_auc(items)

    print()
    print("Metrics (threshold = {:.2f})".format(THRESHOLD))
    print("-" * 40)
    print(f"  Accuracy   : {m['accuracy']*100:5.1f}%")
    print(f"  Precision  : {m['precision']*100:5.1f}%")
    print(f"  Recall     : {m['recall']*100:5.1f}%")
    print(f"  F1 score   : {m['f1']*100:5.1f}%")
    print(f"  ROC AUC    : {auc*100:5.1f}%")
    print()
    print(f"  Confusion: TP={m['tp']}  TN={m['tn']}  FP={m['fp']}  FN={m['fn']}")

    out = ROOT / "results.json"
    out.write_text(json.dumps({
        "threshold": THRESHOLD,
        "metrics": m,
        "roc_auc": auc,
        "items": [{k: v for k, v in x.items() if k != "text"} for x in items],
    }, indent=2))
    print(f"\nResults written to {out}")


if __name__ == "__main__":
    main()
