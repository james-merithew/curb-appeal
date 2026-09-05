"""Confirmation run for the gated monocular-depth step detector.

The earlier experiment (eval/out/experiment_depth_steps.json) tuned on doors 13-38
and validated on 39-64, then recommended "ship gated, after a check on roughly 20
more doors".  This script is that check.  It does three things and refuses to blur
them together:

  1. PROVENANCE.  Enumerates, from the experiment JSON itself, exactly which doors
     and which image files the depth pipeline has already consumed, and derives the
     genuinely unseen remainder.  Nothing is assumed.

  2. EXCLUSION.  Derives the sealed entrances' door ids from their entrance ids
     (E-0NN <-> door-NN, a mapping ground_truth.csv states explicitly for E-001..
     E-012) and asserts that no sealed door reaches any scoring path.

  3. FROZEN EVALUATION.  Applies the earlier run's parameters with NO retuning,
     then separately re-runs the tuning procedure on the new data to report whether
     the frozen parameters are what the new data would have chosen.

Nothing here estimates a riser height.  step_score is the same depth-profile shape
statistic as before; profile_score is imported from depth_steps_analyze so the
geometry code is byte-identical to the run being confirmed.
"""
import csv
import glob
import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from depth_steps_analyze import profile_score, depth_verdict  # noqa: E402

ROOT = r"C:\dev\curb-appeal"
GT_CSV = os.path.join(ROOT, "eval", "out", "ground_truth.csv")
PRIOR_JSON = os.path.join(ROOT, "eval", "out", "experiment_depth_steps.json")
OUT_JSON = os.path.join(ROOT, "eval", "out", "experiment_depth_steps_confirm.json")

# The 18 entrances sealed from assessment, named by entrance id.  The door ids are
# DERIVED below, never hardcoded.
SEALED_ENTRANCES = ["E-002", "E-005", "E-006", "E-011", "E-014", "E-015", "E-016",
                    "E-021", "E-028", "E-029", "E-032", "E-036", "E-039", "E-044",
                    "E-046", "E-052", "E-059", "E-064"]

# ---- FROZEN gate parameters, lifted from the prior run's winning pass ----------
# pass "crop1036_last2views": crop_top=0.4, net_size=1036, last 2 views per door.
FROZEN = {
    "pass": "crop1036_last2views",
    "aggregation": "max",
    "threshold": 0.05,
    "uncertain_band": [0.0, 0.15],
    "fusion_rule": "override_lowconf",
    "fusion_X": 90,          # depth may override only when VLM confidence < X
    "last_n_views": 2,
}
ABSTAIN = {"not_visible", "uncertain", "cannot_tell", ""}


# ---------------------------------------------------------------- provenance ---
def load_truth(criterion="step_free_entry"):
    gt, names = {}, {}
    with open(GT_CSV, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            names[r["door"]] = r["door_name"]
            if r["criterion"] == criterion:
                gt[r["door"]] = r["truth"]
    return gt, names


def derive_sealed(names):
    """Map entrance ids to door ids and verify the mapping before trusting it.

    ground_truth.csv labels doors 01-12 as '<name> (E-0NN)'.  Every one of those
    satisfies E-0NN -> door-NN, so the identity mapping is verified, not assumed;
    doors 13-64 carry no entrance label and inherit it by the same rule.
    """
    checked = 0
    for door, name in names.items():
        if "(E-" in name:
            eid = name.split("(E-")[1].split(")")[0]
            assert f"door-{int(eid):02d}" == door, f"mapping broken: {name} vs {door}"
            checked += 1
    assert checked >= 12, f"only {checked} entrance labels found; mapping unverified"
    sealed = {f"door-{int(e.split('-')[1]):02d}" for e in SEALED_ENTRANCES}
    assert len(sealed) == len(SEALED_ENTRANCES)
    return sealed, checked


def prior_consumption():
    """Doors and image stems the depth experiment has already scored.

    Returned separately per pass, because the two passes consumed different
    amounts: full518_allviews read every photograph at net 518 with no crop,
    while the pass actually being confirmed (crop1036_last2views) read only the
    last two views of each door at net 1036.  'Unseen pixels' below means unseen
    by the SHIPPING configuration; the door-level provenance uses the union, so
    no door counts as unseen just because one pass skipped it.
    """
    with open(PRIOR_JSON, encoding="utf-8") as fh:
        prior = json.load(fh)
    doors, views_any, views_ship = set(), set(), set()
    for label, p in prior["passes"].items():
        for door, rec in p["doors"].items():
            doors.add(door)
            for v in rec["views"]:
                views_any.add((door, v["file"]))
                if label == FROZEN["pass"]:
                    views_ship.add((door, v["file"]))
    return prior, doors, views_any, views_ship


# ------------------------------------------------------------------ scoring ---
def score_door(depth_dir, door, files=None):
    paths = sorted(glob.glob(os.path.join(depth_dir, door, "*.npy")))
    if files is not None:
        want = set(files)
        paths = [p for p in paths if os.path.basename(p)[:-4] in want]
    views = []
    for p in paths:
        s, dbg = profile_score(np.load(p).astype(np.float32))
        views.append({"file": os.path.basename(p)[:-4], "step_score": round(float(s), 3),
                      "debug": dbg})
    return views


def aggregate(views, agg):
    if not views:
        return 0.0
    a = np.array([v["step_score"] for v in views])
    return {"max": float(a.max()), "mean": float(a.mean()),
            "median": float(np.median(a)),
            "top2": float(np.sort(a)[-2:].mean())}[agg]


def fuse(vlm_v, vlm_c, dep_v, X, handrail_veto=False, handrails=None):
    """The frozen gate.  Depth may only move a verdict when it commits, disagrees,
    and the vision model is not confident."""
    if dep_v == "uncertain" or dep_v == vlm_v:
        return vlm_v, "no_override"
    if handrail_veto and handrails == "present":
        return vlm_v, "veto_handrails"
    if vlm_c is None or vlm_c == "":
        return vlm_v, "no_override"
    if float(vlm_c) < X:
        return dep_v, "override"
    return vlm_v, "no_override"


def committed_accuracy(pred, truth, doors):
    correct = committed = 0
    errors = []
    for d in doors:
        if pred[d] in ABSTAIN:
            continue
        committed += 1
        if pred[d] == truth[d]:
            correct += 1
        else:
            errors.append(d)
    return {"correct": correct, "committed": committed, "n": len(doors),
            "abstained": len(doors) - committed,
            "acc_of_committed": round(correct / committed, 4) if committed else None,
            "acc_of_all": round(correct / len(doors), 4) if doors else None,
            "errors": errors}


def tune(per_door_views, truth, doors):
    """Re-run the ORIGINAL tuning procedure on a given door set.  Used only to ask
    whether the frozen parameters are what this data would have picked."""
    best = None
    for agg in ["max", "mean", "median", "top2"]:
        scores = {d: aggregate(per_door_views[d], agg) for d in doors}
        for t in np.arange(0.05, 0.96, 0.025):
            pred = {d: depth_verdict(scores[d], t, t) for d in doors}
            tp = sum(1 for d in doors if truth[d] == "absent" and pred[d] == "absent")
            tn = sum(1 for d in doors if truth[d] == "present" and pred[d] == "present")
            npos = sum(1 for d in doors if truth[d] == "absent")
            nneg = len(doors) - npos
            if npos == 0 or nneg == 0:
                continue
            bal = 0.5 * (tp / npos + tn / nneg)
            acc = sum(1 for d in doors if pred[d] == truth[d])
            if best is None or (bal, acc) > best[0]:
                best = ((bal, acc), agg, float(t))
    if best is None:
        return None
    (bal, acc), agg, t = best
    return {"aggregation": agg, "threshold": round(t, 3),
            "balanced_accuracy": round(bal, 3), "correct": acc, "n": len(doors)}


# -------------------------------------------------------------------- report ---
def evaluate(label, doors, depth_dir, vlm, truth, view_pick, X=None,
             handrail_veto=False, notes=""):
    X = FROZEN["fusion_X"] if X is None else X
    t_lo, t_hi = FROZEN["uncertain_band"]
    per_door_views, rows = {}, {}
    for d in sorted(doors):
        files = view_pick(d)
        views = score_door(depth_dir, d, files)
        per_door_views[d] = views
        s = aggregate(views, FROZEN["aggregation"])
        dv = depth_verdict(s, t_lo, t_hi)
        c = vlm[d]["step_free_entry"]
        hr = vlm[d].get("handrails_present", {}).get("verdict")
        fv, why = fuse(c["verdict"], c["confidence"], dv, X, handrail_veto, hr)
        rows[d] = {"truth": truth[d], "vlm_verdict": c["verdict"],
                   "vlm_confidence": c["confidence"], "vlm_evidence": c["evidence"],
                   "handrails_vlm": hr, "step_score": round(s, 3),
                   "depth_verdict": dv, "fusion_verdict": fv, "fusion_action": why,
                   "views_used": [v["file"] for v in views],
                   "view_scores": {v["file"]: v["step_score"] for v in views}}
    pred_v = {d: rows[d]["vlm_verdict"] for d in rows}
    pred_d = {d: rows[d]["depth_verdict"] for d in rows}
    pred_f = {d: rows[d]["fusion_verdict"] for d in rows}
    return {
        "label": label, "notes": notes, "depth_dir": depth_dir,
        "n_doors": len(rows), "fusion_X": X, "handrail_veto": handrail_veto,
        "n_stepped_truth": sum(1 for d in rows if truth[d] == "absent"),
        "vision_alone": committed_accuracy(pred_v, truth, rows),
        "depth_alone": committed_accuracy(pred_d, truth, rows),
        "fusion": committed_accuracy(pred_f, truth, rows),
        "overrides": {d: rows[d] for d in rows if rows[d]["fusion_action"] != "no_override"},
        "retune_on_this_data": tune(per_door_views, truth, list(rows)),
        "doors": rows,
    }, per_door_views


def main():
    scratch = os.environ["SCRATCH"]
    truth, names = load_truth()
    sealed, checked = derive_sealed(names)
    prior, prior_doors, prior_views, ship_views = prior_consumption()
    all_doors = set(truth)

    unseen_doors = sorted(all_doors - prior_doors - sealed)
    assert not (set(unseen_doors) & sealed), "SEALED DOOR LEAKED INTO UNSEEN SET"

    # ---- capture inventory: is there any 2026-09-04 capture the 52 did not use? --
    import datetime
    photo_dates = {}
    for d in sorted(all_doors):
        for f in sorted(glob.glob(os.path.join(ROOT, "photos", d, "*"))):
            stem = os.path.splitext(os.path.basename(f))[0]
            photo_dates.setdefault(
                datetime.date.fromtimestamp(os.path.getmtime(f)).isoformat(), []
            ).append((d, stem))
    sept4 = photo_dates.get("2026-09-04", [])
    sept4_unused_doors = sorted({d for d, _ in sept4} - prior_doors)

    vlm_pilot = json.load(open(os.path.join(ROOT, "eval", "out",
                                            "door_results_pilot_confirm.json"), encoding="utf-8"))
    vlm_pilot_archive = json.load(open(os.path.join(ROOT, "eval", "out",
                                                    "door_results_pilot.json"), encoding="utf-8"))
    vlm_heldout = json.load(open(os.path.join(ROOT, "eval", "out",
                                              "door_results_heldout.json"), encoding="utf-8"))
    vlm = {d: v["criteria"] for d, v in itertools.chain(vlm_heldout.items(),
                                                        vlm_pilot.items())}
    for d in sealed:
        vlm.pop(d, None)          # a sealed door cannot even be read from here

    pilot_dir = os.path.join(scratch, "depth_pilot_crop1036")
    all_dir = os.path.join(scratch, "depth_crop1036_all")

    def last_n(depth_dir, n):
        def pick(door):
            fs = sorted(os.path.basename(p)[:-4] for p in
                        glob.glob(os.path.join(depth_dir, door, "*.npy")))
            return fs[-n:] if n else fs
        return pick

    skipped_no_spare = []

    def unused_views(door):
        """Views the SHIPPING pass never read.  A door with <= 2 views has none;
        those doors are recorded and dropped rather than silently re-tested on
        the same pixels."""
        fs = sorted(os.path.basename(p)[:-4] for p in
                    glob.glob(os.path.join(all_dir, door, "*.npy")))
        used = {v for (d, v) in ship_views if d == door}
        rest = [f for f in fs if f not in used]
        if not rest:
            skipped_no_spare.append(door)
        return rest

    results = {}

    # ---- TEST 0 (control): does this file reproduce the run it is confirming? ----
    # Same cached depth maps, same views, same frozen parameters.  If the numbers
    # below disagree with the prior JSON's per-door verdicts, every negative result
    # in this file is an artefact of a reimplementation, not a finding.
    ship_dir = os.path.join(scratch, "depth_crop1036_last2")
    prior_doors_unsealed = sorted(d for d in prior["passes"][FROZEN["pass"]]["doors"]
                                  if d not in sealed)
    results["T0_control_reproduce_prior"], _ = evaluate(
        "control: reproduce the prior run on its own inputs", prior_doors_unsealed,
        ship_dir, vlm, truth, last_n(ship_dir, FROZEN["last_n_views"]),
        notes="Sealed doors removed, so this cannot equal the published 52-door "
              "figure; it is checked verdict-by-verdict against the prior JSON below.")
    prior_rows = prior["passes"][FROZEN["pass"]]["doors"]
    mismatches = [d for d in prior_doors_unsealed
                  if prior_rows[d]["fusion_verdict"]
                  != results["T0_control_reproduce_prior"]["doors"][d]["fusion_verdict"]
                  or abs(prior_rows[d]["step_score"]
                         - results["T0_control_reproduce_prior"]["doors"][d]["step_score"]) > 1e-6]
    results["T0_control_reproduce_prior"]["verdict_mismatches_vs_prior_json"] = mismatches

    # ---- TEST 1: the only genuinely unseen doors, frozen parameters --------------
    results["T1_unseen_doors_frozen"], pv1 = evaluate(
        "unseen pilot doors, frozen gate", unseen_doors, pilot_dir,
        vlm, truth, last_n(pilot_dir, FROZEN["last_n_views"]),
        notes="Doors never processed by any depth pass and not sealed. Frozen "
              "aggregation/threshold/fusion from the crop1036_last2views pass.")

    # sensitivity: same doors, every view instead of the last two
    results["T1b_unseen_doors_allviews"], _ = evaluate(
        "unseen pilot doors, all views", unseen_doors, pilot_dir,
        vlm, truth, last_n(pilot_dir, 0),
        notes="Same frozen threshold; view-selection heuristic relaxed. The pilot "
              "captures do not all follow the far-to-near ordering the last-2 rule "
              "assumes, so this is the fair sensitivity check on that heuristic.")

    # sensitivity: the write-up's stated confidence gate (85) vs the tuned one (90)
    results["T1c_unseen_doors_X85"], _ = evaluate(
        "unseen pilot doors, X=85", unseen_doors, pilot_dir,
        vlm, truth, last_n(pilot_dir, FROZEN["last_n_views"]), X=85,
        notes="The enhancement table says 'confidence below about 85'; the tuned "
              "parameter was 90. Both are reported.")

    results["T1d_unseen_doors_handrail_veto"], _ = evaluate(
        "unseen pilot doors, handrail veto on", unseen_doors, pilot_dir,
        vlm, truth, last_n(pilot_dir, FROZEN["last_n_views"]), handrail_veto=True,
        notes="The handrail veto is named in the write-up but was never implemented "
              "or measured in the original analysis code. Measured here.")

    # ---- TEST 2: unseen PIXELS on already-held-out doors -------------------------
    def band(lo, hi):
        ds = sorted(d for d in all_doors
                    if lo <= int(d.split("-")[1]) <= hi and d not in sealed)
        return [d for d in ds if unused_views(d)]

    heldout_b = band(39, 64)
    results["T2_heldoutB_unused_views"], _ = evaluate(
        "half-B doors, views the shipping pass never read", heldout_b, all_dir,
        vlm, truth, unused_views,
        notes="NOT an unseen-door test: these doors' truths were the earlier "
              "validation half. It is a capture-robustness replicate - same frozen "
              "gate, different photographs of the same entrances. Doors whose every "
              "view the shipping pass already read are excluded, not re-used.")

    # Would ANY of the gate's dials rescue it on the largest slice?  If one does,
    # that is a retuning requirement and therefore a negative result, not a win.
    for X in [65, 70, 75, 80, 85, 90]:
        for veto in [False, True]:
            results[f"T2v_X{X}_veto{int(veto)}"], _ = evaluate(
                f"half-B unused views, X={X} veto={veto}", heldout_b, all_dir,
                vlm, truth, unused_views, X=X, handrail_veto=veto,
                notes="Parameter sweep on the capture-robustness replicate. Any "
                      "setting that only looks good here is retuned, not confirmed.")

    half_a = band(13, 38)
    results["T3_heldoutA_unused_views"], _ = evaluate(
        "half-A doors, views the shipping pass never read", half_a, all_dir,
        vlm, truth, unused_views,
        notes="Weakest of the three: these doors set the threshold. Reported for "
              "completeness only.")

    # ---- TEST 4/5: fairness check on T2 ----------------------------------------
    # T2 hands depth only the views the shipping pass skipped, which are the WIDER
    # frames, while the vision baseline saw every view in one call.  If depth's
    # collapse were an artefact of that asymmetry it would disappear when depth
    # aggregates over every view too.  It does not.
    def all_views(door):
        return sorted(os.path.basename(p)[:-4] for p in
                      glob.glob(os.path.join(all_dir, door, "*.npy")))

    for lo, hi, tag in [(39, 64, "T4_heldoutB_allviews"), (13, 38, "T5_heldoutA_allviews")]:
        ds = sorted(d for d in all_doors
                    if lo <= int(d.split("-")[1]) <= hi and d not in sealed)
        results[tag], _ = evaluate(
            f"doors {lo}-{hi}, depth over every view", ds, all_dir,
            vlm, truth, all_views,
            notes="Fairness control for the capture-robustness replicate: depth now "
                  "aggregates over the same views the vision call saw. Half A is the "
                  "tuning half and is not evidence; half B is.")

    for key, res in results.items():
        leaked = sorted(set(res["doors"]) & sealed)
        assert not leaked, f"SEALED LEAK in {key}: {leaked}"

    out = {
        "purpose": "confirmation run for the gated depth step detector",
        "doctrine": "presence only - step_score is a depth-profile shape statistic, never a height",
        "criterion": "step_free_entry",
        "frozen_parameters": FROZEN,
        "committed_accuracy_definition":
            "correct / committed, where a verdict in "
            f"{sorted(ABSTAIN)} is an abstention and is not scored",
        "exclusion": {
            "sealed_entrances": SEALED_ENTRANCES,
            "sealed_doors_derived": sorted(sealed),
            "mapping_verified_on_n_labels": checked,
            "assert_no_sealed_door_scored": True,
        },
        "provenance": {
            "doors_with_ground_truth": len(all_doors),
            "doors_already_consumed_by_depth": sorted(prior_doors),
            "images_already_consumed_by_depth": len(prior_views),
            "genuinely_unseen_unsealed_doors": unseen_doors,
            "genuinely_unseen_stepped_doors":
                [d for d in unseen_doors if truth[d] == "absent"],
            "capture_dates": {k: len(v) for k, v in photo_dates.items()},
            "sept4_captures_on_doors_not_already_scored": sept4_unused_doors,
            "images_read_by_shipping_pass": len(ship_views),
            "doors_with_no_spare_views_excluded_from_T2_T3":
                sorted(set(skipped_no_spare)),
            "vlm_pilot_archive_vs_fresh_disagreements": [
                d for d in vlm_pilot
                if vlm_pilot_archive[d]["criteria"]["step_free_entry"]["verdict"]
                != vlm_pilot[d]["criteria"]["step_free_entry"]["verdict"]],
        },
        "tests": results,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)

    # -------------------------------------------------------------- console ----
    print("=" * 78)
    print("PROVENANCE")
    print(f"  doors with ground truth              : {len(all_doors)}")
    print(f"  sealed (derived from entrance ids)   : {len(sealed)} -> {sorted(sealed)}")
    print(f"  already consumed by a depth pass     : {len(prior_doors)} doors, "
          f"{len(prior_views)} images")
    print(f"  GENUINELY UNSEEN, UNSEALED DOORS     : {len(unseen_doors)} -> {unseen_doors}")
    print(f"  ...of which stepped (truth=absent)   : "
          f"{[d for d in unseen_doors if truth[d] == 'absent']}")
    print(f"  2026-09-04 captures on unscored doors: {sept4_unused_doors or 'NONE'}")
    print(f"  capture dates                        : "
          f"{ {k: len(v) for k, v in photo_dates.items()} }")
    for key, res in results.items():
        print("=" * 78)
        print(f"{key}: {res['label']}  (n={res['n_doors']}, "
              f"stepped={res['n_stepped_truth']}, X={res['fusion_X']}, "
              f"veto={res['handrail_veto']})")
        for m in ["vision_alone", "depth_alone", "fusion"]:
            s = res[m]
            print(f"  {m:14s} {s['correct']:3d}/{s['committed']:3d} committed "
                  f"= {100 * (s['acc_of_committed'] or 0):5.1f}%   "
                  f"(abstained {s['abstained']})  errors={s['errors']}")
        print(f"  retune on this data : {res['retune_on_this_data']}")
        if res["overrides"]:
            for d, r in res["overrides"].items():
                ok = "FIXED" if (r["fusion_verdict"] == r["truth"]
                                 and r["vlm_verdict"] != r["truth"]) else (
                     "BROKE" if (r["fusion_verdict"] != r["truth"]
                                 and r["vlm_verdict"] == r["truth"]) else "neutral")
                print(f"    {r['fusion_action']:14s} {d} truth={r['truth']:7s} "
                      f"vlm={r['vlm_verdict']}({r['vlm_confidence']}) "
                      f"score={r['step_score']:.3f} depth={r['depth_verdict']:9s} "
                      f"-> {r['fusion_verdict']:7s} [{ok}]")
        else:
            print("    no overrides fired")
    print("=" * 78)
    print(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
