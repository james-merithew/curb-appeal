"""Per-door multi-view eval: ALL views of a door in ONE model call.

Attacks the adjudicated failure mode where majority voting over similar frames
amplifies a shared blind spot (a step riser visible only obliquely gets outvoted
by frontal frames shot from on top of the platform). One call sees every angle.

Usage:
    python eval/run_eval_door.py [--model claude-opus-5] [--doors door-01,door-08]
Writes eval/out/door_results.json and prints accuracy vs ground_truth.csv.
"""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from criteria import CRITERIA, CRITERIA_KEYS, allowed_verdicts
from run_eval import (
    IMAGE_EXTS, OUT_DIR, PHOTOS_DIR, load_env_key, parse_json_response,
    prep_image, validate_verdicts,
)

SYSTEM = """You are the vision engine for EntryMap, an ADA storefront screening app.
You assess ONLY what is visible in photos of a building entrance. You never guess
measurements: slope percentages and widths in inches are not assessable from a photo.
Presence/absence of visible features is your job. Be conservative: if no view shows
the relevant area, answer not_visible rather than absent.
Respond with ONLY a JSON object - no prose, no markdown fences."""


def build_door_prompt(n_views: int) -> str:
    lines = [
        f"The {n_views} photos above all show the SAME entrance from different "
        "angles and distances (head-on, obliques, near, far).",
        "Integrate ALL views before answering each criterion:",
        "- A feature clearly visible in ANY view is visible.",
        "- When views disagree, trust the view that actually shows the relevant "
        "area: a ground-level or oblique view showing a step riser or side ramp "
        "outweighs head-on views shot from on top of a platform.",
        "For each criterion return: verdict, confidence (0-100), evidence (one "
        "short phrase, naming which view showed it).",
        "Verdicts: 'present', 'absent', or 'not_visible' - except "
        "door_width_adequate, which uses 'appears_wide', 'appears_narrow', or "
        "'cannot_tell'.",
        "Criteria:",
    ]
    for key, desc in CRITERIA:
        lines.append(f"- {key}: {desc}")
    lines.append(
        'Return exactly this JSON shape: {"criteria": {"<key>": {"verdict": "...", '
        '"confidence": 0, "evidence": "..."}}, "overall_note": "one sentence a shop '
        'owner would understand"}'
    )
    return "\n".join(lines)


MAX_TOKENS = 4000


def assess_door(client, model: str, images_b64: list) -> tuple[dict, float]:
    content = [
        {"type": "image",
         "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}}
        for b64 in images_b64
    ]
    content.append({"type": "text", "text": build_door_prompt(len(images_b64))})
    t0 = time.perf_counter()
    response = client.messages.create(
        model=model, max_tokens=MAX_TOKENS, system=SYSTEM,
        messages=[{"role": "user", "content": content}],
    )
    latency = time.perf_counter() - t0
    if response.stop_reason == "refusal":
        raise RuntimeError("model refused the request")
    text = next((b.text for b in response.content if b.type == "text"), "")
    return parse_json_response(text), latency


def load_truth() -> dict:
    truth = {}
    with open(OUT_DIR / "ground_truth.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("truth", "").strip():
                truth[(r["door"], r["criterion"])] = r["truth"].strip().lower()
    return truth


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--doors", default="", help="comma-separated subset")
    ap.add_argument("--out", default="door_results.json",
                    help="results filename under eval/out")
    ap.add_argument("--max-tokens", type=int, default=4000,
                    help="sonnet truncates JSON under adaptive thinking at 2000")
    args = ap.parse_args()
    global MAX_TOKENS
    MAX_TOKENS = args.max_tokens
    load_env_key()
    client = anthropic.Anthropic()

    doors = sorted(d for d in PHOTOS_DIR.iterdir() if d.is_dir())
    if args.doors:
        wanted = set(args.doors.split(","))
        doors = [d for d in doors if d.name in wanted]

    results = {}
    for door in doors:
        files = sorted(p for p in door.iterdir()
                       if p.suffix.lower() in IMAGE_EXTS)
        images = [prep_image(p)[0] for p in files]
        try:
            parsed, latency = assess_door(client, args.model, images)
        except Exception as exc:  # one bad response must not lose the run
            for attempt in range(2):
                try:
                    parsed, latency = assess_door(client, args.model, images)
                    break
                except Exception as exc2:
                    exc = exc2
            else:
                print(f"{door.name}: FAILED after retries: {exc}")
                results[door.name] = {"views": len(images), "latency_s": None,
                                      "criteria": {k: {"verdict": "", "confidence": "", "evidence": f"error: {exc}"} for k in CRITERIA_KEYS},
                                      "overall_note": ""}
                continue
        results[door.name] = {
            "views": len(images),
            "latency_s": round(latency, 2),
            "criteria": validate_verdicts(parsed),
            "overall_note": str(parsed.get("overall_note", ""))[:300],
        }
        print(f"{door.name}: {len(images)} views in one call, {latency:.1f}s")

    (OUT_DIR / args.out).write_text(
        json.dumps(results, indent=1), encoding="utf-8")

    truth = load_truth()
    correct = wrong = abstain = 0
    misses = []
    for (door, crit), t in sorted(truth.items()):
        if door not in results or crit == "door_width_adequate":
            continue
        v = results[door]["criteria"][crit]["verdict"]
        if v == "not_visible":
            abstain += 1
        elif v == t:
            correct += 1
        else:
            wrong += 1
            misses.append((door, crit, v, t))
    committed = correct + wrong
    print(f"\nPER-DOOR SINGLE-CALL: {correct} correct, {wrong} wrong, "
          f"{abstain} abstained")
    if committed:
        print(f"accuracy of committed: {100 * correct / committed:.0f}% "
              f"({correct}/{committed})")
    for m in misses:
        print("  MISS:", *m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
