"""EntryMap vision-accuracy eval.

Walks photos/<door-id>/*, runs each image through the Claude vision checklist,
records verdicts + confidence + latency, and emits a ground-truth template.

Usage:
    python eval/run_eval.py [--model claude-opus-5] [--limit N]
"""

import argparse
import base64
import csv
import io
import json
import sys
import time
from pathlib import Path

import anthropic
from PIL import Image

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("WARNING: pillow-heif not installed - .HEIC files will be skipped.")

from criteria import CRITERIA, CRITERIA_KEYS, allowed_verdicts

ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "photos"
OUT_DIR = Path(__file__).resolve().parent / "out"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
MAX_DIM = 1568  # matches planned production pipeline: resize before upload
EXIF_MODEL_TAG = 272

SYSTEM = """You are the vision engine for EntryMap, an ADA storefront screening app.
You assess ONLY what is visible in a photo of a building entrance. You never guess
measurements: slope percentages and widths in inches are not assessable from a photo.
Presence/absence of visible features is your job. Be conservative: if a feature is
not clearly visible in frame, answer not_visible rather than absent.
Respond with ONLY a JSON object - no prose, no markdown fences."""


def build_prompt() -> str:
    lines = [
        "Assess this entrance photo against the criteria below.",
        "For each criterion return: verdict, confidence (0-100), evidence "
        "(one short phrase describing what you see).",
        "Verdicts: 'present', 'absent', or 'not_visible' - except "
        "door_width_adequate, which uses 'appears_wide', 'appears_narrow', "
        "or 'cannot_tell'.",
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


def load_env_key() -> None:
    """Populate ANTHROPIC_API_KEY from .env if present and not already set."""
    import os
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY="):
                os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip()
                return


def prep_image(path: Path):
    """Return (jpeg_base64, device_model) for an image file."""
    img = Image.open(path)
    exif = img.getexif()
    device = str(exif.get(EXIF_MODEL_TAG, "")).strip() or "unknown"
    img = img.convert("RGB")
    img.thumbnail((MAX_DIM, MAX_DIM))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8"), device


def parse_json_response(text: str) -> dict:
    """Parse model output that should be bare JSON; tolerate stray fences."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object in response: {text[:200]}")
    return json.loads(text[start : end + 1])


def assess(client: anthropic.Anthropic, model: str, image_b64: str) -> tuple[dict, float]:
    """One API call. Returns (parsed_result, latency_seconds)."""
    t0 = time.perf_counter()
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image",
                 "source": {"type": "base64", "media_type": "image/jpeg",
                            "data": image_b64}},
                {"type": "text", "text": build_prompt()},
            ],
        }],
    )
    latency = time.perf_counter() - t0
    if response.stop_reason == "refusal":
        raise RuntimeError("model refused the request (recorded as failure)")
    text = next((b.text for b in response.content if b.type == "text"), "")
    return parse_json_response(text), latency


def validate_verdicts(parsed: dict) -> dict:
    """Normalize the criteria block; flag out-of-vocabulary verdicts."""
    out = {}
    crit = parsed.get("criteria", {})
    for key in CRITERIA_KEYS:
        entry = crit.get(key, {})
        verdict = str(entry.get("verdict", "")).strip().lower()
        if verdict not in allowed_verdicts(key):
            verdict = f"INVALID:{verdict or 'missing'}"
        out[key] = {
            "verdict": verdict,
            "confidence": entry.get("confidence", ""),
            "evidence": str(entry.get("evidence", ""))[:200],
        }
    return out


def discover_images() -> list[Path]:
    if not PHOTOS_DIR.exists():
        return []
    return sorted(
        p for p in PHOTOS_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )


def write_ground_truth_template(doors: list[str]) -> Path:
    """One row per door x criterion for the owner to fill; never overwrites."""
    path = OUT_DIR / "ground_truth.csv"
    if path.exists():
        return path
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["door", "criterion", "truth"])
        for door in doors:
            for key in CRITERIA_KEYS:
                w.writerow([door, key, ""])
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--limit", type=int, default=0,
                    help="only process the first N images (smoke test)")
    args = ap.parse_args()

    images = discover_images()
    if not images:
        print(f"No images found under {PHOTOS_DIR}.")
        print("Create photos/<door-id>/ folders and drop your door photos in.")
        return 1
    if args.limit:
        images = images[: args.limit]

    load_env_key()
    import os
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        print("No API key found. Create a .env file in the repo root containing:")
        print("  ANTHROPIC_API_KEY=sk-ant-...   (console.anthropic.com -> API keys)")
        return 1
    client = anthropic.Anthropic()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    print(f"Assessing {len(images)} images with {args.model}...\n")
    for i, path in enumerate(images, 1):
        door = path.parent.name
        row = {"door": door, "file": path.name, "model": args.model,
               "device": "", "latency_s": "", "overall_note": "", "error": ""}
        try:
            image_b64, device = prep_image(path)
            row["device"] = device
            parsed, latency = assess(client, args.model, image_b64)
            row["latency_s"] = round(latency, 2)
            row["overall_note"] = str(parsed.get("overall_note", ""))[:300]
            for key, entry in validate_verdicts(parsed).items():
                row[f"{key}"] = entry["verdict"]
                row[f"{key}_conf"] = entry["confidence"]
                row[f"{key}_evidence"] = entry["evidence"]
            flag = "" if latency <= 15 else "  << OVER 15s"
            print(f"[{i}/{len(images)}] {door}/{path.name}  "
                  f"{row['latency_s']}s  ({device}){flag}")
        except Exception as e:  # record and continue - one bad image must not kill the run
            row["error"] = f"{type(e).__name__}: {e}"
            print(f"[{i}/{len(images)}] {door}/{path.name}  FAILED: {row['error']}")
        rows.append(row)

    fieldnames = ["door", "file", "model", "device", "latency_s"]
    for key in CRITERIA_KEYS:
        fieldnames += [key, f"{key}_conf", f"{key}_evidence"]
    fieldnames += ["overall_note", "error"]

    csv_path = OUT_DIR / "results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    (OUT_DIR / "results.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8")

    doors = sorted({r["door"] for r in rows})
    gt_path = write_ground_truth_template(doors)

    ok = [r for r in rows if not r["error"]]
    lat = sorted(float(r["latency_s"]) for r in ok if r["latency_s"] != "")
    print(f"\nDone: {len(ok)}/{len(rows)} succeeded -> {csv_path}")
    if lat:
        p95 = lat[min(len(lat) - 1, int(len(lat) * 0.95))]
        print(f"Latency: median {lat[len(lat)//2]:.1f}s, p95 {p95:.1f}s, "
              f"over-15s: {sum(1 for x in lat if x > 15)}/{len(lat)}")
    print(f"Next: fill in the truth column of {gt_path}, "
          f"then run eval/report.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
