"""Grounded re-ask experiment: zero-shot boxes -> evidence receipts + crops -> targeted VLM re-ask.

Hypothesis under test: crops of DETECTED regions (OWL-ViT zero-shot boxes for
"door handle" / "door") beat the earlier geometric band crops, which fixed the
hardware misses but hallucinated risers from close-up threshold crops.

Stages (default: all):
    detect  OWL-ViT on up to 4 views per door; writes
            eval/out/grounded/door-NN.jpg   (receipt: boxes + labels, all views)
            eval/out/grounded/crops/*.jpg   (handle crops + door crops)
            eval/out/grounded/detections.json
    ask     one claude call per door on <=4 crops, asking ONLY
            lever_or_pull_hardware and step_free_entry; fuses with the baseline
            (override only when the grounded verdict commits) and scores against
            ground_truth.csv; writes eval/out/experiment_grounded.json

Usage:
    python eval/experiment_grounded.py [--stage detect|ask|all] [--doors door-20,door-21]
Runs on CPU; the system python here already has torch+transformers.
"""

import argparse
import base64
import io
import json
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("WARNING: pillow-heif not installed - .HEIC files will fail to open")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from criteria import CRITERIA  # noqa: E402
from run_eval import IMAGE_EXTS, OUT_DIR, PHOTOS_DIR, load_env_key, parse_json_response  # noqa: E402
from run_eval_door import SYSTEM, load_truth  # noqa: E402

DETECTOR = "google/owlvit-base-patch32"
QUERIES = ["door handle", "door", "step", "ramp", "handrail", "wheelchair symbol sign"]
MIN_SCORE = {"door handle": 0.08, "door": 0.08, "step": 0.08, "ramp": 0.08,
             "handrail": 0.08, "wheelchair symbol sign": 0.08}
TOPK_PER_QUERY = 3
COLORS = {"door handle": (255, 60, 60), "door": (60, 140, 255), "step": (255, 170, 0),
          "ramp": (60, 200, 60), "handrail": (200, 60, 220), "wheelchair symbol sign": (0, 200, 200)}
MAX_VIEWS = 4
MAX_DIM = 1568
GROUNDED_DIR = OUT_DIR / "grounded"
CROPS_DIR = GROUNDED_DIR / "crops"
TARGET_KEYS = ["lever_or_pull_hardware", "step_free_entry"]
COMMITTED = {"present", "absent"}

HARDWARE_MISSES = {"door-20", "door-21", "door-22", "door-35"}
STEP_MISSES = {"door-18", "door-21", "door-29", "door-35", "door-41", "door-44", "door-47"}

HANDLE_GATE = 0.01  # min detector score for a handle box to license a hardware override

# USD per million tokens, first-party API rates.
PRICING = {"claude-sonnet-5": (2.00, 10.00), "claude-opus-5": (5.00, 25.00),
           "claude-haiku-4-5": (1.00, 5.00)}


# ---------------------------------------------------------------- detection

def pick_views(files: list, n: int = MAX_VIEWS) -> list:
    """Evenly spaced subset so near/far/oblique shots all get a chance."""
    if len(files) <= n:
        return files
    idx = [round(i * (len(files) - 1) / (n - 1)) for i in range(n)]
    return [files[i] for i in idx]


def load_view(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img.thumbnail((MAX_DIM, MAX_DIM))
    return img


DETECT_DIM = 1024  # OWL-ViT resizes to 768 internally; feeding 1568px only slows preprocessing


def run_detector(det, img: Image.Image) -> list:
    small = img.copy()
    small.thumbnail((DETECT_DIM, DETECT_DIM))
    sx, sy = img.width / small.width, img.height / small.height
    raw = det(small, candidate_labels=QUERIES, threshold=0.05)
    kept = []
    for label in QUERIES:
        cands = sorted((r for r in raw if r["label"] == label and r["score"] >= MIN_SCORE[label]),
                       key=lambda r: -r["score"])[:TOPK_PER_QUERY]
        for r in cands:
            b = r["box"]
            kept.append({"label": label, "score": round(float(r["score"]), 3),
                         "box": [int(b["xmin"] * sx), int(b["ymin"] * sy), int(b["xmax"] * sx), int(b["ymax"] * sy)]})
    return kept


def _font(size: int):
    for name in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_receipt(door: str, views: list, dets_per_view: list, out_path: Path) -> None:
    """Horizontal montage of the views with labelled boxes: the evidence receipt."""
    target_h = 900
    panels = []
    font = _font(22)
    for i, (img, dets) in enumerate(zip(views, dets_per_view)):
        panel = img.copy()
        draw = ImageDraw.Draw(panel)
        for d in dets:
            x0, y0, x1, y1 = d["box"]
            col = COLORS[d["label"]]
            draw.rectangle([x0, y0, x1, y1], outline=col, width=5)
            tag = f'{d["label"]} {d["score"]:.2f}'
            tw = draw.textlength(tag, font=font)
            ty = max(0, y0 - 28)
            draw.rectangle([x0, ty, x0 + tw + 8, ty + 26], fill=col)
            draw.text((x0 + 4, ty + 2), tag, fill=(0, 0, 0), font=font)
        draw.rectangle([0, 0, 120, 30], fill=(0, 0, 0))
        draw.text((6, 4), f"view {i + 1}", fill=(255, 255, 255), font=font)
        scale = target_h / panel.height
        panel = panel.resize((int(panel.width * scale), target_h))
        panels.append(panel)
    gap, header = 12, 44
    width = sum(p.width for p in panels) + gap * (len(panels) - 1)
    sheet = Image.new("RGB", (width, target_h + header), (24, 24, 24))
    hdraw = ImageDraw.Draw(sheet)
    hdraw.text((10, 10), f"{door}  -  {DETECTOR} zero-shot boxes (label score)", fill=(255, 255, 255), font=_font(26))
    x = 0
    for p in panels:
        sheet.paste(p, (x, header))
        x += p.width + gap
    sheet.save(out_path, format="JPEG", quality=82)


def _clip(box, w, h):
    x0, y0, x1, y1 = box
    return [max(0, int(x0)), max(0, int(y0)), min(w, int(x1)), min(h, int(y1))]


def handle_crop_box(box, w, h):
    """Handles are tiny; crop a square around them big enough to show context."""
    x0, y0, x1, y1 = box
    side = max(max(x1 - x0, y1 - y0) * 3, 420)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return _clip([cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2], w, h)


def door_crop_box(box, w, h):
    """Full door padded 15% each side, plus an extra 15% of height below so the
    threshold-to-sidewalk transition is in frame."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    return _clip([x0 - 0.15 * bw, y0 - 0.15 * bh, x1 + 0.15 * bw, y1 + 0.30 * bh], w, h)


def best_by_label(dets_per_view: list, label: str, n: int = 2) -> list:
    """Top-n boxes for a label across views, preferring distinct views."""
    cands = sorted(((d["score"], vi, d["box"]) for vi, dets in enumerate(dets_per_view)
                    for d in dets if d["label"] == label), key=lambda t: -t[0])
    picked, used_views = [], set()
    for s, vi, box in cands:
        if vi in used_views:
            continue
        picked.append((s, vi, box))
        used_views.add(vi)
        if len(picked) == n:
            break
    if len(picked) < n:  # fall back to same-view extras
        for s, vi, box in cands:
            if (s, vi, box) not in picked:
                picked.append((s, vi, box))
                if len(picked) == n:
                    break
    return picked


def make_crops(door: str, views: list, dets_per_view: list) -> list:
    crops = []
    for kind, label, boxer in (("handle", "door handle", handle_crop_box), ("door", "door", door_crop_box)):
        for k, (score, vi, box) in enumerate(best_by_label(dets_per_view, label)):
            img = views[vi]
            cb = boxer(box, img.width, img.height)
            crop = img.crop(cb)
            path = CROPS_DIR / f"{door}_{kind}{k + 1}_v{vi + 1}.jpg"
            crop.save(path, format="JPEG", quality=85)
            crops.append({"kind": kind, "label": label, "view": vi + 1, "score": score,
                          "det_box": box, "crop_box": cb, "size": list(crop.size), "path": str(path)})
    return crops


def stage_detect(doors: list) -> dict:
    from transformers import pipeline
    t0 = time.perf_counter()
    det = pipeline("zero-shot-object-detection", model=DETECTOR)
    print(f"detector loaded in {time.perf_counter() - t0:.1f}s")
    GROUNDED_DIR.mkdir(parents=True, exist_ok=True)
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    det_json = GROUNDED_DIR / "detections.json"
    out = json.loads(det_json.read_text(encoding="utf-8")) if det_json.exists() else {}
    for door in doors:
        files = pick_views(sorted(p for p in door.iterdir() if p.suffix.lower() in IMAGE_EXTS))
        t0 = time.perf_counter()
        views = [load_view(p) for p in files]
        dets_per_view = [run_detector(det, img) for img in views]
        draw_receipt(door.name, views, dets_per_view, GROUNDED_DIR / f"{door.name}.jpg")
        crops = make_crops(door.name, views, dets_per_view)
        dt = time.perf_counter() - t0
        out[door.name] = {
            "views": [p.name for p in files],
            "detections": [{"view": i + 1, "boxes": d} for i, d in enumerate(dets_per_view)],
            "crops": crops,
            "detect_s": round(dt, 1),
        }
        n_h = sum(1 for d in dets_per_view for b in d if b["label"] == "door handle")
        n_d = sum(1 for d in dets_per_view for b in d if b["label"] == "door")
        print(f"{door.name}: {len(views)} views, {dt:.1f}s, handle boxes={n_h}, door boxes={n_d}, crops={len(crops)}")
        det_json.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


# ---------------------------------------------------------------- re-ask

def build_reask_prompt() -> str:
    crit = dict(CRITERIA)
    return "\n".join([
        "The images above are CLOSE-UP CROPS of one building entrance, cut out by an "
        "object detector (each crop is preceded by its detector label, score and source view).",
        "'door handle' crops are zoomed on the detected hardware. 'door' crops show the "
        "detected door plus a strip of ground below it, i.e. the threshold.",
        "Assess ONLY these two criteria, using every crop:",
        f"- lever_or_pull_hardware: {crit['lever_or_pull_hardware']}",
        f"- step_free_entry: {crit['step_free_entry']}",
        "Crops are tight. For step_free_entry, answer present or absent only when a crop "
        "actually shows the ground plane from sidewalk to threshold; a door sill, mat, or "
        "a shadow line alone is NOT a riser. Otherwise answer not_visible.",
        "For each criterion return: verdict ('present', 'absent', or 'not_visible'), "
        "confidence (0-100), evidence (one short phrase naming which crop showed it).",
        'Return exactly this JSON shape: {"criteria": {"lever_or_pull_hardware": {"verdict": "...", '
        '"confidence": 0, "evidence": "..."}, "step_free_entry": {"verdict": "...", '
        '"confidence": 0, "evidence": "..."}}}',
    ])


def crop_b64(path: str) -> str:
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


def reask(client, model: str, crops: list) -> tuple[dict, float, dict]:
    content = []
    for i, c in enumerate(crops):
        content.append({"type": "text", "text": f"Crop {i + 1}: detector label '{c['label']}' "
                        f"(score {c['score']:.2f}), from view {c['view']}."})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                    "data": crop_b64(c["path"])}})
    content.append({"type": "text", "text": build_reask_prompt()})
    t0 = time.perf_counter()
    resp = client.messages.create(model=model, max_tokens=1500, system=SYSTEM,
                                  messages=[{"role": "user", "content": content}])
    latency = time.perf_counter() - t0
    if resp.stop_reason == "refusal":
        raise RuntimeError("model refused")
    text = next((b.text for b in resp.content if b.type == "text"), "")
    parsed = parse_json_response(text)
    usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    out = {}
    for key in TARGET_KEYS:
        e = parsed.get("criteria", {}).get(key, {})
        v = str(e.get("verdict", "")).strip().lower()
        out[key] = {"verdict": v if v in COMMITTED | {"not_visible"} else f"INVALID:{v or 'missing'}",
                    "confidence": e.get("confidence", ""), "evidence": str(e.get("evidence", ""))[:300]}
    return out, latency, usage


def half_b(door: str) -> bool:
    return int(door.split("-")[1]) >= 39


def score(verdict_of, doors: list, truth: dict, keys: list) -> dict:
    """verdict_of(door, crit) -> verdict string."""
    per = {}
    for key in keys:
        c = w = a = 0
        misses = []
        for door in doors:
            t = truth.get((door, key))
            if not t:
                continue
            v = verdict_of(door, key)
            if v == t:
                c += 1
            elif v in COMMITTED:
                w += 1
                misses.append(f"{door}: said {v}, truth {t}")
            else:
                a += 1
        per[key] = {"correct": c, "wrong": w, "abstain": a, "n": c + w + a,
                    "acc_of_committed": round(100 * c / (c + w), 1) if c + w else None,
                    "acc_of_all": round(100 * c / (c + w + a), 1) if c + w + a else None,
                    "misses": misses}
    tot_c = sum(p["correct"] for p in per.values())
    tot_w = sum(p["wrong"] for p in per.values())
    tot_a = sum(p["abstain"] for p in per.values())
    per["_total"] = {"correct": tot_c, "wrong": tot_w, "abstain": tot_a, "n": tot_c + tot_w + tot_a,
                     "acc_of_committed": round(100 * tot_c / (tot_c + tot_w), 1) if tot_c + tot_w else None,
                     "acc_of_all": round(100 * tot_c / (tot_c + tot_w + tot_a), 1) if tot_c + tot_w + tot_a else None}
    return per


def stage_ask(door_names: list, model: str) -> None:
    import anthropic
    load_env_key()
    client = anthropic.Anthropic()
    dets = json.loads((GROUNDED_DIR / "detections.json").read_text(encoding="utf-8"))
    baseline = json.loads((OUT_DIR / "door_results_heldout.json").read_text(encoding="utf-8"))
    truth = load_truth()
    out_path = OUT_DIR / "experiment_grounded.json"
    prev = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    per_door = prev.get("per_door", {})

    for door in door_names:
        if door in per_door and per_door[door].get("grounded"):
            continue  # resume
        crops = dets[door]["crops"]
        rec = {"crops": len(crops), "crop_kinds": [c["kind"] for c in crops],
               "detect_s": dets[door]["detect_s"], "vlm_s": None, "grounded": None, "usage": None}
        if crops:
            last = None
            for _ in range(3):
                try:
                    g, lat, usage = reask(client, model, crops)
                    rec.update(grounded=g, vlm_s=round(lat, 2), usage=usage)
                    break
                except Exception as exc:
                    last = exc
                    time.sleep(2)
            else:
                rec["error"] = str(last)
                print(f"{door}: FAILED {last}")
        else:
            rec["error"] = "no detections -> no crops -> no re-ask"
        per_door[door] = rec
        g = rec.get("grounded") or {}
        print(f"{door}: crops={len(crops)} vlm={rec['vlm_s']}s "
              f"hw={g.get('lever_or_pull_hardware', {}).get('verdict')} "
              f"step={g.get('step_free_entry', {}).get('verdict')}")
        out_path.write_text(json.dumps({"per_door": per_door}, indent=1), encoding="utf-8")

    # ---- fusion + scoring
    def base_v(door, key):
        return baseline[door]["criteria"][key]["verdict"]

    def fused_v(door, key):
        g = (per_door.get(door) or {}).get("grounded") or {}
        v = g.get(key, {}).get("verdict")
        return v if (key in TARGET_KEYS and v in COMMITTED) else base_v(door, key)

    def best_handle_score(door) -> float:
        ss = [c["score"] for c in dets[door]["crops"] if c["kind"] == "handle"]
        return max(ss) if ss else 0.0

    def fused_gated_v(door, key):
        """Coverage gate: only let the crop re-ask override the hardware verdict when the
        detector actually found a handle. Without it the model commits 'absent' from a
        whole-door crop where hardware is not resolvable - the dominant new-error mode."""
        if key == "lever_or_pull_hardware" and best_handle_score(door) < HANDLE_GATE:
            return base_v(door, key)
        return fused_v(door, key)

    doors_all = sorted(d for d in baseline if d in per_door)
    doors_a = [d for d in doors_all if not half_b(d)]
    doors_b = [d for d in doors_all if half_b(d)]
    all_keys = [k for k, _ in CRITERIA if k != "door_width_adequate"]

    def deltas(ds: list, verdict_of=None) -> dict:
        verdict_of = verdict_of or fused_v
        fixed, new_errors, still_missed = [], [], []
        for door in ds:
            for key in TARGET_KEYS:
                t = truth.get((door, key))
                if not t:
                    continue
                b, f = base_v(door, key), verdict_of(door, key)
                if b != t and f == t:
                    fixed.append(f"{door}/{key}")
                elif b == t and f != t:
                    new_errors.append(f"{door}/{key}: baseline {b} -> grounded {f} (truth {t})")
                elif b != t and f != t:
                    still_missed.append(f"{door}/{key}: baseline {b}, grounded {f} (truth {t})")
        return {"fixed": fixed, "new_errors": new_errors, "still_missed": still_missed}

    def det_stats_for(ds: list) -> dict:
        return {
            "doors": len(ds),
            "doors_with_handle_box": sum(1 for d in ds if any(c["kind"] == "handle" for c in dets[d]["crops"])),
            "doors_with_door_box": sum(1 for d in ds if any(c["kind"] == "door" for c in dets[d]["crops"])),
            "doors_with_no_crops": sum(1 for d in ds if not dets[d]["crops"]),
            "views_total": sum(len(dets[d]["views"]) for d in ds),
            "views_with_handle_box": sum(1 for d in ds for v in dets[d]["detections"]
                                         if any(b["label"] == "door handle" for b in v["boxes"])),
            "views_with_door_box": sum(1 for d in ds for v in dets[d]["detections"]
                                       if any(b["label"] == "door" for b in v["boxes"])),
            "label_box_counts": {q: sum(1 for d in ds for v in dets[d]["detections"]
                                        for b in v["boxes"] if b["label"] == q) for q in QUERIES},
        }

    in_price, out_price = PRICING.get(model, (None, None))

    def cost_runtime_for(ds: list) -> dict:
        vlm = [per_door[d]["vlm_s"] for d in ds if per_door[d].get("vlm_s")]
        dts = [per_door[d]["detect_s"] for d in ds]
        in_tok = sum((per_door[d].get("usage") or {}).get("input_tokens", 0) for d in ds)
        out_tok = sum((per_door[d].get("usage") or {}).get("output_tokens", 0) for d in ds)
        usd = (in_tok * in_price + out_tok * out_price) / 1e6 if in_price else None
        return {
            "doors": len(ds),
            "detect_s_mean": round(sum(dts) / len(dts), 1) if dts else None,
            "detect_s_max": max(dts) if dts else None,
            "vlm_s_mean": round(sum(vlm) / len(vlm), 1) if vlm else None,
            "vlm_s_max": max(vlm) if vlm else None,
            "per_door_total_s_mean": round((sum(dts) + sum(vlm)) / len(ds), 1) if ds else None,
            "tokens": {"input": in_tok, "output": out_tok},
            "usd_total": round(usd, 4) if usd is not None else None,
            "usd_per_door": round(usd / len(ds), 5) if usd is not None and ds else None,
        }

    halves = (("all_52", doors_all), ("half_A_13_38", doors_a), ("half_B_39_64", doors_b))
    tables, per_half = {}, {}
    for name, ds in halves:
        tables[name] = {
            "baseline_target": score(base_v, ds, truth, TARGET_KEYS),
            "grounded_target": score(fused_v, ds, truth, TARGET_KEYS),
            "baseline_all7": score(base_v, ds, truth, all_keys)["_total"],
            "grounded_all7": score(fused_v, ds, truth, all_keys)["_total"],
        }
        d = deltas(ds)
        dg = deltas(ds, fused_gated_v)
        per_half[name] = {
            "detection": det_stats_for(ds),
            "cost_runtime": cost_runtime_for(ds),
            "fixed": d["fixed"], "new_errors": d["new_errors"], "still_missed": d["still_missed"],
            "counts": {k: len(v) for k, v in d.items()},
            "gated": {
                "rule": f"override lever_or_pull_hardware only when a handle box scores >= {HANDLE_GATE}",
                "target": score(fused_gated_v, ds, truth, TARGET_KEYS)["_total"],
                "counts": {k: len(v) for k, v in dg.items()},
                "new_errors": dg["new_errors"],
            },
        }

    d_all = deltas(doors_all)
    fixed, new_errors, still_missed = d_all["fixed"], d_all["new_errors"], d_all["still_missed"]
    known = {f"{d}/lever_or_pull_hardware" for d in HARDWARE_MISSES} | {f"{d}/step_free_entry" for d in STEP_MISSES}

    summary = {
        "detector": DETECTOR, "queries": QUERIES, "min_score": MIN_SCORE, "topk_per_query": TOPK_PER_QUERY,
        "vlm_model": model, "price_per_mtok": {"input": in_price, "output": out_price},
        "doors": len(doors_all),
        "detection": det_stats_for(doors_all),
        "runtime": cost_runtime_for(doors_all),
        "tokens": cost_runtime_for(doors_all)["tokens"],
        "tables": tables,
        "per_half": per_half,
        "fixed": fixed,
        "known_misses_fixed": sorted(k for k in known if k in fixed),
        "known_misses_not_fixed": sorted(k for k in known if k not in fixed),
        "new_errors": new_errors,
        "still_missed": still_missed,
    }
    out_path.write_text(json.dumps({"summary": summary, "per_door": per_door}, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("tables", "per_half")}, indent=1))
    for name, t in tables.items():
        print(f"\n== {name} ==")
        for key in TARGET_KEYS + ["_total"]:
            b, g = t["baseline_target"][key], t["grounded_target"][key]
            print(f"{key:28s} baseline {b['correct']}/{b['wrong']}/{b['abstain']} (acc {b['acc_of_all']}%)   "
                  f"grounded {g['correct']}/{g['wrong']}/{g['abstain']} (acc {g['acc_of_all']}%)")
        b, g = t["baseline_all7"], t["grounded_all7"]
        print(f"{'all 7 criteria':28s} baseline {b['correct']}/{b['wrong']}/{b['abstain']} (acc {b['acc_of_all']}%)   "
              f"grounded {g['correct']}/{g['wrong']}/{g['abstain']} (acc {g['acc_of_all']}%)")
        h = per_half[name]
        print(f"{'deltas':28s} fixed {h['counts']['fixed']}  new_errors {h['counts']['new_errors']}  "
              f"still_missed {h['counts']['still_missed']}")
        dd, cr = h["detection"], h["cost_runtime"]
        print(f"{'detector coverage':28s} door {dd['doors_with_door_box']}/{dd['doors']}  "
              f"handle {dd['doors_with_handle_box']}/{dd['doors']}")
        print(f"{'cost / latency per door':28s} ${cr['usd_per_door']}  "
              f"{cr['per_door_total_s_mean']}s (detect {cr['detect_s_mean']}s + vlm {cr['vlm_s_mean']}s)")
        gc, gt = h["gated"]["counts"], h["gated"]["target"]
        print(f"{'gated (handle box required)':28s} fixed {gc['fixed']}  new_errors {gc['new_errors']}  "
              f"still_missed {gc['still_missed']}  (acc {gt['acc_of_all']}%)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["detect", "ask", "all"])
    ap.add_argument("--doors", default="", help="comma-separated subset")
    ap.add_argument("--model", default="claude-sonnet-5")
    args = ap.parse_args()
    doors = sorted(d for d in PHOTOS_DIR.iterdir() if d.is_dir() and 13 <= int(d.name.split("-")[1]) <= 64)
    if args.doors:
        wanted = set(args.doors.split(","))
        doors = [d for d in doors if d.name in wanted]
    if args.stage in ("detect", "all"):
        stage_detect(doors)
    if args.stage in ("ask", "all"):
        stage_ask([d.name for d in doors], args.model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
