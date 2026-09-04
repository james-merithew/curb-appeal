"""Build the accuracy report from eval results + owner-filled ground truth.

Usage: python eval/report.py
Reads eval/out/results.csv and eval/out/ground_truth.csv.
Writes eval/out/report.md with four sections:
accuracy per criterion, cross-view consistency per door, device delta, latency.
"""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

from criteria import CRITERIA_KEYS

OUT_DIR = Path(__file__).resolve().parent / "out"
SCORED_KEYS = [k for k in CRITERIA_KEYS if k != "door_width_adequate"]


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct(n: int, d: int) -> str:
    return f"{100*n/d:.0f}%" if d else "n/a"


def main() -> int:
    results_path = OUT_DIR / "results.csv"
    if not results_path.exists():
        print(f"{results_path} not found - run eval/run_eval.py first.")
        return 1
    rows = [r for r in load_csv(results_path) if not r.get("error")]
    if not rows:
        print("results.csv has no successful rows.")
        return 1

    truth = {}
    gt_path = OUT_DIR / "ground_truth.csv"
    if gt_path.exists():
        for r in load_csv(gt_path):
            if r.get("truth", "").strip():
                truth[(r["door"], r["criterion"])] = r["truth"].strip().lower()

    lines = ["# EntryMap - Vision Accuracy Report", ""]
    lines.append(f"Model(s): {', '.join(sorted({r['model'] for r in rows}))} | "
                 f"images scored: {len(rows)} | "
                 f"doors: {len({r['door'] for r in rows})}")
    lines.append("")

    # --- 1. Accuracy vs ground truth (per criterion) ---
    lines.append("## 1. Accuracy vs ground truth")
    lines.append("")
    if truth:
        lines.append("`not_visible` counts as an abstention, not an error - "
                     "it is scored separately. door_width_adequate is excluded "
                     "(appearance-only vocabulary, no strict truth).")
        lines.append("")
        lines.append("| Criterion | Correct | Wrong | Abstained | Accuracy (of committed) |")
        lines.append("|---|---|---|---|---|")
        total_c = total_w = 0
        for key in SCORED_KEYS:
            c = w = a = 0
            for r in rows:
                t = truth.get((r["door"], key))
                if not t:
                    continue
                v = r.get(key, "")
                if v == "not_visible":
                    a += 1
                elif v == t:
                    c += 1
                else:
                    w += 1
            total_c += c
            total_w += w
            lines.append(f"| {key} | {c} | {w} | {a} | {pct(c, c+w)} |")
        lines.append(f"| **all criteria** | {total_c} | {total_w} | - | "
                     f"**{pct(total_c, total_c+total_w)}** |")
    else:
        lines.append("Ground truth not filled in yet - edit "
                     "eval/out/ground_truth.csv and re-run.")
    lines.append("")

    # --- 2. Cross-view consistency per door ---
    lines.append("## 2. Cross-view consistency (does the verdict flip with the angle?)")
    lines.append("")
    lines.append("Per door: share of views agreeing with the modal verdict, "
                 "averaged over criteria. 100% = rock solid across angles.")
    lines.append("")
    lines.append("| Door | Views | Consistency | Least stable criterion |")
    lines.append("|---|---|---|---|")
    by_door = defaultdict(list)
    for r in rows:
        by_door[r["door"]].append(r)
    for door in sorted(by_door):
        drows = by_door[door]
        per_crit = {}
        for key in CRITERIA_KEYS:
            verdicts = [r.get(key, "") for r in drows if r.get(key)]
            if len(verdicts) > 1:
                per_crit[key] = Counter(verdicts).most_common(1)[0][1] / len(verdicts)
        if not per_crit:
            continue
        avg = sum(per_crit.values()) / len(per_crit)
        worst = min(per_crit, key=per_crit.get)
        lines.append(f"| {door} | {len(drows)} | {avg*100:.0f}% | "
                     f"{worst} ({per_crit[worst]*100:.0f}%) |")
    lines.append("")

    # --- 3. Device delta ---
    lines.append("## 3. Device delta (iPhone 16 Pro vs iPhone 16)")
    lines.append("")
    by_device = defaultdict(list)
    for r in rows:
        by_device[r.get("device", "unknown")].append(r)
    lines.append("| Device | Images | Accuracy vs truth | Median latency |")
    lines.append("|---|---|---|---|")
    for device in sorted(by_device):
        drows = by_device[device]
        c = w = 0
        for r in drows:
            for key in SCORED_KEYS:
                t = truth.get((r["door"], key))
                v = r.get(key, "")
                if t and v != "not_visible":
                    if v == t:
                        c += 1
                    else:
                        w += 1
        lats = sorted(float(r["latency_s"]) for r in drows if r.get("latency_s"))
        med = f"{lats[len(lats)//2]:.1f}s" if lats else "n/a"
        lines.append(f"| {device} | {len(drows)} | {pct(c, c+w)} | {med} |")
    lines.append("")

    # --- 4. Latency vs the 15s budget ---
    lines.append("## 4. Latency vs the 15-second demo budget")
    lines.append("")
    lats = sorted(float(r["latency_s"]) for r in rows if r.get("latency_s"))
    if lats:
        p95 = lats[min(len(lats) - 1, int(len(lats) * 0.95))]
        over = sum(1 for x in lats if x > 15)
        lines.append(f"- min {lats[0]:.1f}s / median {lats[len(lats)//2]:.1f}s / "
                     f"p95 {p95:.1f}s / max {lats[-1]:.1f}s")
        lines.append(f"- over budget (>15s): {over}/{len(lats)} "
                     f"({pct(over, len(lats))})")
        lines.append("- note: this is model latency only; the production budget "
                     "must also cover upload (~2s) and geocode+render (~2s).")
    lines.append("")

    report_path = OUT_DIR / "report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {report_path}")
    print("\n".join(lines[:14]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
