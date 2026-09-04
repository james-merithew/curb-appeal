"""Diagnostic sheet for the depth-step experiment: per view, RGB with the ground
band / column window / detected plateau overlaid, the depth map, and the
normalised gradient profile.  Usage: python depth_steps_diag.py <depth_dir> <out.png> door-18 door-21 ...
"""
import glob
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d, uniform_filter1d

sys.path.insert(0, os.path.dirname(__file__))
import depth_steps_analyze as A


def profile(depth):
    H, W = depth.shape
    y0 = int(H * A.BAND_TOP)
    x0, x1 = int(W * A.COL_LO), int(W * A.COL_HI)
    band = gaussian_filter1d(depth[y0:, x0:x1].astype(np.float32), A.SIGMA, axis=0)
    G = np.median(np.diff(band, axis=0), axis=1)
    ref = np.percentile(G, 80)
    Gn = uniform_filter1d(np.clip(G / max(ref, 1e-6), -A.GN_CAP, A.GN_CAP), 3)
    return y0, x0, x1, Gn


def main():
    depth_dir, out = sys.argv[1], sys.argv[2]
    doors = sys.argv[3:]
    rows = []
    for d in doors:
        for f in sorted(glob.glob(os.path.join(depth_dir, d, "*.npy")))[:4]:
            rows.append((d, f))
    fig, axes = plt.subplots(len(rows), 3, figsize=(11, 3.2 * len(rows)))
    if len(rows) == 1:
        axes = [axes]
    for (d, f), ax in zip(rows, axes):
        depth = np.load(f).astype(np.float32)
        rgb = Image.open(f[:-4] + ".jpg")
        s, dbg = A.profile_score(depth)
        y0, x0, x1, Gn = profile(depth)
        ax[0].imshow(rgb)
        ax[0].axhline(y0, color="y", lw=1)
        ax[0].axvline(x0, color="c", lw=1); ax[0].axvline(x1, color="c", lw=1)
        if "plateau_rows" in dbg:
            ax[0].axhspan(dbg["plateau_rows"][0], dbg["plateau_rows"][1], xmin=A.COL_LO, xmax=A.COL_HI,
                          color="r", alpha=0.35)
        ax[0].set_title(f"{d} {os.path.basename(f)[:-4]}  score={s:.2f}", fontsize=9)
        ax[0].axis("off")
        ax[1].imshow(depth, cmap="magma"); ax[1].axis("off")
        ys = np.arange(len(Gn)) + y0
        ax[2].plot(Gn, ys, lw=1)
        ax[2].axvline(A.T_LOW, color="r", ls="--", lw=0.8); ax[2].axvline(A.T_HIGH, color="g", ls="--", lw=0.8)
        ax[2].invert_yaxis(); ax[2].set_xlim(-0.5, 2.6)
        ax[2].set_title(str(dbg), fontsize=7)
    plt.tight_layout()
    plt.savefig(out, dpi=80)


if __name__ == "__main__":
    main()
