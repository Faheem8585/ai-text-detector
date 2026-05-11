#!/usr/bin/env python3
"""Generate charts from eval/results.json.

Run AFTER validate.py. Outputs PNGs to eval/charts/.
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)
RESULTS = ROOT / "results.json"

if not RESULTS.exists():
    print("results.json not found. Run: python -m eval.validate first.")
    sys.exit(1)

data = json.loads(RESULTS.read_text())
items = data["items"]
metrics = data["metrics"]
auc = data["roc_auc"]
threshold = data["threshold"]

plt.style.use("dark_background")
BG = "#0a0e14"
PANEL = "#0f1620"


def save(fig, name):
    fig.patch.set_facecolor(BG)
    for ax in fig.axes:
        ax.set_facecolor(PANEL)
    out = CHARTS / name
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  {out.relative_to(ROOT.parent)}")


# 1. Per-sample scores ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
items_sorted = sorted(items, key=lambda x: x["prob"])
names = [x["name"] for x in items_sorted]
probs = [x["prob"] for x in items_sorted]
colors = ["#34d399" if x["label"] == 0 else "#f87171" for x in items_sorted]

y = np.arange(len(names))
ax.barh(y, probs, color=colors, edgecolor="#1e2a3a")
ax.axvline(threshold, color="#fbbf24", linestyle="--", linewidth=1, label=f"threshold = {threshold}")
ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=9, color="#94a3b8")
ax.set_xlabel("ai probability", color="#94a3b8")
ax.set_xlim(0, 1)
ax.set_title("per-sample scores", color="#22d3ee", fontsize=12, pad=12)
ax.legend(loc="lower right", framealpha=0.2)
ax.tick_params(colors="#64748b")
for spine in ax.spines.values():
    spine.set_color("#1e2a3a")

# legend for sample classes
from matplotlib.patches import Patch
legend = [
    Patch(facecolor="#34d399", label="human"),
    Patch(facecolor="#f87171", label="ai"),
]
ax.legend(handles=legend + [plt.Line2D([0], [0], color="#fbbf24",
          linestyle="--", label=f"threshold {threshold}")],
          loc="lower right", framealpha=0.2)
save(fig, "scores_by_sample.png")


# 2. Confusion matrix ----------------------------------------------------------
cm = np.array([[metrics["tn"], metrics["fp"]],
               [metrics["fn"], metrics["tp"]]])
fig, ax = plt.subplots(figsize=(5, 5))
im = ax.imshow(cm, cmap="cividis", vmin=0)
ax.set_xticks([0, 1], ["predicted human", "predicted ai"], color="#94a3b8")
ax.set_yticks([0, 1], ["actual human", "actual ai"], color="#94a3b8")
for i in range(2):
    for j in range(2):
        ax.text(j, i, str(cm[i][j]), ha="center", va="center",
                color="#0a0e14" if cm[i][j] > cm.max()/2 else "#e2e8f0",
                fontsize=24, weight="bold")
ax.set_title("confusion matrix", color="#22d3ee", fontsize=12, pad=12)
ax.tick_params(colors="#64748b")
for spine in ax.spines.values():
    spine.set_color("#1e2a3a")
save(fig, "confusion_matrix.png")


# 3. ROC curve -----------------------------------------------------------------
labels = [x["label"] for x in items]
scores = [x["prob"] for x in items]
thresholds = sorted(set(scores + [0, 1]), reverse=True)
tprs, fprs = [], []
P = sum(labels)
N = len(labels) - P
for t in thresholds:
    tp = sum(1 for s, l in zip(scores, labels) if s >= t and l == 1)
    fp = sum(1 for s, l in zip(scores, labels) if s >= t and l == 0)
    tprs.append(tp / P if P else 0)
    fprs.append(fp / N if N else 0)

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(fprs, tprs, color="#22d3ee", linewidth=2, marker="o", markersize=5)
ax.plot([0, 1], [0, 1], color="#64748b", linestyle="--", linewidth=1)
ax.fill_between(fprs, 0, tprs, color="#22d3ee", alpha=0.15)
ax.set_xlabel("false positive rate", color="#94a3b8")
ax.set_ylabel("true positive rate", color="#94a3b8")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.set_title(f"roc curve · auc = {auc:.3f}", color="#22d3ee", fontsize=12, pad=12)
ax.tick_params(colors="#64748b")
ax.grid(alpha=0.1)
for spine in ax.spines.values():
    spine.set_color("#1e2a3a")
save(fig, "roc_curve.png")


# 4. Metrics summary card ------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 4))
ax.axis("off")
ax.set_facecolor(PANEL)

rows = [
    ("accuracy",  metrics["accuracy"]),
    ("precision", metrics["precision"]),
    ("recall",    metrics["recall"]),
    ("f1 score",  metrics["f1"]),
    ("roc auc",   auc),
]
for i, (label, value) in enumerate(rows):
    y_pos = 0.85 - i * 0.16
    ax.text(0.05, y_pos, label, color="#94a3b8", fontsize=12,
            transform=ax.transAxes)
    ax.text(0.35, y_pos, f"{value*100:.1f}%", color="#22d3ee", fontsize=22,
            weight="bold", transform=ax.transAxes)
    bar_x = 0.55
    bar_w = 0.40 * value
    ax.add_patch(plt.Rectangle((bar_x, y_pos), 0.40, 0.06,
                               transform=ax.transAxes,
                               facecolor="#1e2a3a", edgecolor="none"))
    ax.add_patch(plt.Rectangle((bar_x, y_pos), bar_w, 0.06,
                               transform=ax.transAxes,
                               facecolor="#22d3ee", edgecolor="none"))

ax.text(0.05, 1.02, f"metrics · threshold = {threshold} · n = {len(items)}",
        color="#22d3ee", fontsize=12, transform=ax.transAxes)
save(fig, "metrics_summary.png")


print(f"\n{len(list(CHARTS.glob('*.png')))} charts written to {CHARTS.relative_to(ROOT.parent)}/")
