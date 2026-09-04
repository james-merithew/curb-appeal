"""Phase 1 of the monocular-depth step experiment: run a depth model over every
view of doors 13-64 and cache the relative-depth maps (float16 .npy) plus a small
RGB thumbnail in the scratch dir.  CPU only.  Nothing here outputs a measurement.

Usage: python depth_steps_extract.py <out_dir> [model_id] [crop_top] [net_size]
  crop_top: fraction of the frame height to drop before inference (0 = full frame).
            The crop's depth is padded back to full-frame coordinates (edge rows)
            so the analysis code is unchanged.
  net_size: image-processor target size (default 518).  Larger = finer risers, slower.
"""
import glob
import json
import os
import sys
import time

import numpy as np
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

PHOTOS = r"C:\dev\curb-appeal\photos"
LONG_SIDE = 700  # 4284x5712 HEIC -> 525x700; plenty for a ground-band profile


def load_rgb(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    s = LONG_SIDE / max(w, h)
    return im.resize((round(w * s), round(h * s)), Image.BILINEAR)


def main():
    out_dir = sys.argv[1]
    model_id = sys.argv[2] if len(sys.argv) > 2 else "depth-anything/Depth-Anything-V2-Small-hf"
    crop_top = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    net_size = int(sys.argv[4]) if len(sys.argv) > 4 else 518
    os.makedirs(out_dir, exist_ok=True)

    import torch
    from transformers import AutoImageProcessor, pipeline

    torch.set_num_threads(max(1, os.cpu_count() - 1))
    t0 = time.time()
    # AutoImageProcessor needs torchvision in transformers 5; the pipeline's own
    # (slow) processor loads fine, so override its target size in place instead.
    pipe = pipeline("depth-estimation", model=model_id, device="cpu")
    pipe.image_processor.size = {"height": net_size, "width": net_size}
    print(f"model loaded in {time.time()-t0:.1f}s: {model_id} crop_top={crop_top} net_size={net_size}",
          flush=True)

    log = {"model": model_id, "crop_top": crop_top, "net_size": net_size, "images": []}
    only = os.environ.get("DOORS")          # e.g. "20,29,37" for a targeted test
    doors = [int(x) for x in only.split(",")] if only else range(13, 65)
    for d in doors:
        door = f"door-{d:02d}"
        files = sorted(glob.glob(os.path.join(PHOTOS, door, "*")))
        last_n = int(os.environ.get("LAST_N", "0"))   # keep only the last N views (nearest)
        if last_n:
            files = files[-last_n:]
        dd = os.path.join(out_dir, door)
        os.makedirs(dd, exist_ok=True)
        for f in files:
            stem = os.path.splitext(os.path.basename(f))[0]
            npy = os.path.join(dd, stem + ".npy")
            if os.path.exists(npy):
                continue
            im = load_rgb(f)
            y_crop = int(im.height * crop_top)
            net_in = im.crop((0, y_crop, im.width, im.height)) if y_crop else im
            t1 = time.time()
            with torch.inference_mode():
                res = pipe(net_in)
            dt = time.time() - t1
            depth = res["predicted_depth"]
            if hasattr(depth, "numpy"):
                depth = depth.squeeze().float().numpy()
            depth = np.asarray(depth, dtype=np.float32)
            if depth.shape != (net_in.height, net_in.width):
                # pipeline normally resizes to input; be defensive
                depth = np.asarray(
                    Image.fromarray(depth).resize((net_in.width, net_in.height), Image.BILINEAR),
                    dtype=np.float32,
                )
            if y_crop:
                depth = np.pad(depth, ((y_crop, 0), (0, 0)), mode="edge")
            np.save(npy, depth.astype(np.float16))
            im.save(os.path.join(dd, stem + ".jpg"), quality=80)
            log["images"].append({"door": door, "file": stem, "seconds": round(dt, 2),
                                  "shape": list(depth.shape)})
            print(f"{door} {stem} {depth.shape} {dt:.2f}s", flush=True)
    with open(os.path.join(out_dir, "extract_log.json"), "w") as fh:
        json.dump(log, fh, indent=1)
    secs = [x["seconds"] for x in log["images"]]
    if secs:
        print(f"n={len(secs)} mean={np.mean(secs):.2f}s median={np.median(secs):.2f}s")


if __name__ == "__main__":
    main()
