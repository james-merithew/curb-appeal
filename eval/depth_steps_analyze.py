"""Phase 2 of the monocular-depth step experiment: turn cached relative-depth
maps into a per-door step_score (0-1), tune a threshold on doors 13-38, validate
on 39-64, fuse with the VLM verdict, and write experiment_depth_steps.json.

PRESENCE ONLY.  Nothing here estimates or reports a riser height; the score is a
shape statistic of the depth profile (does level ground recede, plateau, then
recede again?), not a measurement.

Geometry behind the score (relative inverse depth D, larger = closer):
  * on a ground plane D is affine in image row, so dD/dy is a positive constant
  * on a vertical face (riser, door leaf) D is constant, so dD/dy ~ 0
  * a flush entry therefore reads bottom-to-top as   slope -> plateau(door)
  * a stepped entry reads as                         slope -> plateau(riser) -> slope(tread) -> plateau(door)
  The score is the strength of an INTERIOR plateau that is followed above by
  ground that resumes receding.  The final plateau (the door) does not count.
"""
import csv
import glob
import json
import os
import sys

import numpy as np
from scipy.ndimage import gaussian_filter1d, uniform_filter1d

GT_CSV = r"C:\dev\curb-appeal\eval\out\ground_truth.csv"
VLM_JSON = r"C:\dev\curb-appeal\eval\out\door_results_heldout.json"
OUT_JSON = r"C:\dev\curb-appeal\eval\out\experiment_depth_steps.json"

HALF_A = [f"door-{i:02d}" for i in range(13, 39)]
HALF_B = [f"door-{i:02d}" for i in range(39, 65)]
KNOWN_MISSES = ["door-18", "door-21", "door-29", "door-35", "door-41", "door-44", "door-47"]

# ---- profile parameters (fixed a priori, not tuned per half) ----------------
BAND_TOP = 0.55       # ground band = lower 45% of the frame
COL_LO, COL_HI = 0.30, 0.70   # central columns (avoid side walls / planters)
SIGMA = 3.0           # vertical smoothing of the depth map (px @ 700 px tall)
T_LOW = 0.30          # normalised gradient below this = "vertical face"
T_HIGH = 0.55         # normalised gradient above this = "ground receding"
MIN_PLATEAU = 6       # px; ~a 15 cm riser at 5 m with a 700 px tall frame
MIN_RECOVERY = 10     # px of receding ground required above the plateau
GN_CAP = 2.5          # cap on normalised gradient (kills reflection jumps)
MAX_PLATEAU = 55      # px; taller "plateaus" are objects (planters, bins), not risers
JUMP = 1.8            # normalised gradient above this right over the plateau = occlusion edge
WIDE_LO, WIDE_HI = 0.15, 0.85  # window for horizontal-consistency check


def profile_score(depth):
    """Return (score, debug) for one depth map. score in [0,1]."""
    H, W = depth.shape
    y0 = int(H * BAND_TOP)
    x0, x1 = int(W * COL_LO), int(W * COL_HI)
    wide = gaussian_filter1d(depth[y0:, int(W * WIDE_LO):int(W * WIDE_HI)].astype(np.float32),
                             SIGMA, axis=0)
    band = depth[y0:, x0:x1].astype(np.float32)
    band = gaussian_filter1d(band, SIGMA, axis=0)
    g = np.diff(band, axis=0)                 # dD/dy, >0 where ground recedes upward
    g_wide = np.diff(wide, axis=0)
    G = np.median(g, axis=1)                  # column-median gradient profile (len = rows-1)
    ref = np.percentile(G, 80)                # reference "ground receding" slope
    if ref <= 1e-6:
        return 0.0, {"reason": "no receding ground in band"}
    Gn = np.clip(G / ref, -GN_CAP, GN_CAP)
    Gn = uniform_filter1d(Gn, 3)
    n = len(Gn)
    # per-column normalised gradient, for horizontal-consistency checks
    gn_cols = np.clip(g_wide / ref, -GN_CAP, GN_CAP)
    # cleanliness: a real slope/plateau/slope/plateau profile crosses T_LOW ~3 times;
    # clutter (signs, planters, bikes) crosses it many times
    crossings = int(np.sum(np.diff((Gn < T_LOW).astype(int)) != 0))
    clean = 1.0 if crossings <= 4 else float(np.clip(1.0 - (crossings - 4) / 6.0, 0.0, 1.0))
    # rows are indexed top(0) -> bottom(n-1) within the band
    low = Gn < T_LOW
    # runs of "vertical face"
    runs = []
    i = 0
    while i < n:
        if low[i]:
            j = i
            while j < n and low[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    best = 0.0
    best_dbg = None
    for (a, b) in runs:
        length = b - a
        if length < MIN_PLATEAU:
            continue
        if a < MIN_RECOVERY:                  # nothing above it inside the band
            continue
        above = Gn[max(0, a - 3 * MIN_RECOVERY):a]
        # recovery = how convincingly ground resumes above this plateau
        rec_rows = above[above > T_HIGH]
        if len(rec_rows) < MIN_RECOVERY:
            continue
        if np.max(above[-MIN_RECOVERY:]) > JUMP:
            continue                          # occlusion edge: an object, not a tread
        recovery = float(np.clip(np.median(above[-MIN_RECOVERY:]) / T_HIGH, 0, 1))
        dip = float(np.clip(1.0 - np.mean(Gn[a:b]) / T_LOW, 0, 1))
        span = float(np.clip(length / (2 * MIN_PLATEAU), 0, 1))
        if length > MAX_PLATEAU:              # soft cap: fades to 0 at ~2x MAX_PLATEAU
            span *= float(np.clip(1.0 - (length - MAX_PLATEAU) / MAX_PLATEAU, 0, 1))
        # fraction of central columns that individually see the plateau at these rows
        consist = float(np.mean(gn_cols[a:b].mean(axis=0) < T_HIGH))
        s = dip * recovery * (0.5 + 0.5 * span) * consist * clean
        if s > best:
            best = s
            best_dbg = {"plateau_rows": [int(y0 + a), int(y0 + b)], "dip": round(dip, 3),
                        "recovery": round(recovery, 3), "span": round(span, 3),
                        "consist": round(consist, 3), "clean": round(clean, 3), "crossings": crossings}
    return best, best_dbg or {"reason": "no interior plateau"}


def load_truth():
    gt = {}
    with open(GT_CSV, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["criterion"] == "step_free_entry":
                gt[r["door"]] = r["truth"]
    return gt


def load_vlm():
    with open(VLM_JSON) as fh:
        d = json.load(fh)
    return {k: v["criteria"]["step_free_entry"] for k, v in d.items()}


def score_doors(depth_dir, agg="max"):
    per_door = {}
    for door in HALF_A + HALF_B:
        files = sorted(glob.glob(os.path.join(depth_dir, door, "*.npy")))
        views = []
        for f in files:
            depth = np.load(f).astype(np.float32)
            s, dbg = profile_score(depth)
            views.append({"file": os.path.basename(f)[:-4], "step_score": round(s, 3), "debug": dbg})
        scores = np.array([v["step_score"] for v in views]) if views else np.array([0.0])
        agg_val = {
            "max": float(scores.max()),
            "mean": float(scores.mean()),
            "median": float(np.median(scores)),
            "top2": float(np.sort(scores)[-2:].mean()),
        }
        per_door[door] = {"views": views, "agg": agg_val, "step_score": agg_val[agg]}
    return per_door


def accuracy(pred, truth, doors):
    """pred: door -> present/absent/uncertain.  Returns (correct, committed, n)."""
    c = k = 0
    for d in doors:
        if pred[d] == "uncertain":
            continue
        k += 1
        c += pred[d] == truth[d]
    return c, k, len(doors)


def depth_verdict(score, t_lo, t_hi):
    # step_score is "a riser is here"; step_free_entry is the inverse
    if score >= t_hi:
        return "absent"
    if score <= t_lo:
        return "present"
    return "uncertain"


def evaluate(depth_dir, label):
    truth = load_truth()
    vlm = load_vlm()
    report = {"pass": label, "depth_dir": depth_dir, "model": None, "params": {
        "BAND_TOP": BAND_TOP, "COL": [COL_LO, COL_HI], "SIGMA": SIGMA, "T_LOW": T_LOW,
        "T_HIGH": T_HIGH, "MIN_PLATEAU": MIN_PLATEAU, "MIN_RECOVERY": MIN_RECOVERY}}
    logp = os.path.join(depth_dir, "extract_log.json")
    if os.path.exists(logp):
        with open(logp) as fh:
            lg = json.load(fh)
        report["model"] = lg["model"]
        report["crop_top"] = lg.get("crop_top", 0.0)
        report["net_size"] = lg.get("net_size", 518)
        secs = [x["seconds"] for x in lg["images"]]
        if secs:
            report["runtime_s_per_image"] = {"mean": round(float(np.mean(secs)), 2),
                                             "median": round(float(np.median(secs)), 2),
                                             "n_images": len(secs)}

    # ---- tune aggregation + single threshold on half A ------------------------
    best = None
    for agg in ["max", "mean", "median", "top2"]:
        per_door = score_doors(depth_dir, agg)
        for t in np.arange(0.05, 0.96, 0.025):
            pred = {d: depth_verdict(per_door[d]["step_score"], t, t) for d in HALF_A}
            c, k, n = accuracy(pred, truth, HALF_A)
            # balanced accuracy matters: 'present' is 85% of half A
            tp = sum(1 for d in HALF_A if truth[d] == "absent" and pred[d] == "absent")
            tn = sum(1 for d in HALF_A if truth[d] == "present" and pred[d] == "present")
            npos = sum(1 for d in HALF_A if truth[d] == "absent")
            nneg = len(HALF_A) - npos
            bal = 0.5 * (tp / npos + tn / nneg)
            key = (bal, c)
            if best is None or key > best[0]:
                best = (key, agg, float(t), c)
    (bal, c), agg, t_star, _ = best
    per_door = score_doors(depth_dir, agg)
    print(f"tuned on half A: agg={agg} t={t_star:.3f} acc={c}/26 balanced={bal:.3f}")
    # uncertain band: +/- 0.1 around the threshold (fixed, not tuned)
    t_lo, t_hi = max(0.0, t_star - 0.10), min(1.0, t_star + 0.10)

    depth_pred = {d: depth_verdict(per_door[d]["step_score"], t_lo, t_hi) for d in per_door}
    depth_pred_hard = {d: depth_verdict(per_door[d]["step_score"], t_star, t_star) for d in per_door}
    vlm_pred = {d: vlm[d]["verdict"] for d in per_door}

    # ---- fusion rules -----------------------------------------------------------
    def fuse(d, X, rule):
        v, vc = vlm[d]["verdict"], vlm[d]["confidence"]
        dp, ds = depth_pred[d], per_door[d]["step_score"]
        if rule == "vlm":
            return v
        if rule == "depth":
            return dp
        if rule == "control_flip_absent":
            # NO depth: just distrust a low-confidence VLM 'absent'.  If this scores
            # the same as the depth fusion, the gain is VLM calibration, not geometry.
            return "present" if (v == "absent" and vc < X) else v
        if dp == "uncertain" or dp == v:
            return v
        # conflict, depth committed
        if rule == "override_lowconf":
            return dp if vc < X else v
        if rule == "override_always":
            return dp
        if rule == "override_strong":
            # depth must be far from the threshold AND vlm not very sure
            strong = abs(ds - t_star) >= 0.25
            return dp if (strong and vc < X) else v
        raise ValueError(rule)

    fusion = {}
    best_f = None
    for rule in ["override_lowconf", "override_always", "override_strong", "control_flip_absent"]:
        for X in [65, 70, 75, 80, 85, 90, 101]:
            if rule == "override_always" and X != 101:
                continue
            pa = {d: fuse(d, X, rule) for d in HALF_A}
            ca, ka, _ = accuracy(pa, truth, HALF_A)
            pb = {d: fuse(d, X, rule) for d in HALF_B}
            cb, kb, _ = accuracy(pb, truth, HALF_B)
            fusion[f"{rule}_X{X}"] = {"halfA": f"{ca}/{ka}", "halfB": f"{cb}/{kb}"}
            if rule != "control_flip_absent" and (best_f is None or ca > best_f[0]):
                best_f = (ca, rule, X)
    _, rule_star, X_star = best_f

    def summarize(pred, doors):
        c, k, n = accuracy(pred, truth, doors)
        return {"correct": c, "committed": k, "n": n, "acc_of_committed": round(c / k, 3) if k else None,
                "acc_of_all": round(c / n, 3), "abstained": n - k}

    final_pred = {d: fuse(d, X_star, rule_star) for d in per_door}
    report.update({
        "tuned": {"aggregation": agg, "threshold": round(t_star, 3),
                  "uncertain_band": [round(t_lo, 3), round(t_hi, 3)],
                  "fusion_rule": rule_star, "fusion_X": X_star},
        "halfA": {
            "vlm": summarize(vlm_pred, HALF_A),
            "depth_hard": summarize(depth_pred_hard, HALF_A),
            "depth_with_uncertain": summarize(depth_pred, HALF_A),
            "fusion": summarize(final_pred, HALF_A),
        },
        "halfB": {
            "vlm": summarize(vlm_pred, HALF_B),
            "depth_hard": summarize(depth_pred_hard, HALF_B),
            "depth_with_uncertain": summarize(depth_pred, HALF_B),
            "fusion": summarize(final_pred, HALF_B),
        },
        "fusion_sweep": fusion,
        "known_misses": {d: {"truth": truth[d], "vlm": vlm_pred[d], "vlm_conf": vlm[d]["confidence"],
                             "depth_score": round(per_door[d]["step_score"], 3),
                             "depth": depth_pred[d], "fusion": final_pred[d]} for d in KNOWN_MISSES},
        "doors": {d: {"half": "A" if d in HALF_A else "B", "truth": truth[d],
                      "vlm_verdict": vlm_pred[d], "vlm_confidence": vlm[d]["confidence"],
                      "step_score": round(per_door[d]["step_score"], 3),
                      "step_score_by_agg": {k: round(v, 3) for k, v in per_door[d]["agg"].items()},
                      "depth_verdict": depth_pred[d], "fusion_verdict": final_pred[d],
                      "views": per_door[d]["views"]} for d in per_door},
    })
    print(f"\n=== pass {label} ({depth_dir}) ===")
    print(json.dumps({k: report[k] for k in ["tuned", "halfA", "halfB", "known_misses"]}, indent=1))
    print("fusion sweep:", json.dumps(fusion, indent=1))
    print("\nper-door:")
    for d in per_door:
        r = report["doors"][d]
        flag = "" if r["depth_verdict"] in (r["truth"], "uncertain") else "  <-- depth wrong"
        print(f"{d} {r['half']} truth={r['truth']:7s} vlm={r['vlm_verdict']:7s}({r['vlm_confidence']}) "
              f"score={r['step_score']:.3f} depth={r['depth_verdict']:9s} fusion={r['fusion_verdict']}{flag}")
    return report


def main():
    """Usage: depth_steps_analyze.py label=depth_dir [label=depth_dir ...]
    Each pass is tuned on half A and validated on half B independently; all go in one JSON."""
    passes = {}
    for arg in sys.argv[1:]:
        label, depth_dir = arg.split("=", 1)
        passes[label] = evaluate(depth_dir, label)
    out = {
        "doctrine": "presence only - step_score is a depth-profile shape statistic, never a height",
        "criterion": "step_free_entry",
        "tune_on": "doors 13-38 (half A)", "validate_on": "doors 39-64 (half B)",
        "passes": passes,
    }
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {OUT_JSON}")


if __name__ == "__main__":
    main()
