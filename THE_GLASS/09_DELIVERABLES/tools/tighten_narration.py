"""Tighten the narration: shorten every pause inside a chunk to at most MAXP seconds, trim the chunk edges.

Writes lossless FLAC copies plus a time map per chunk (old time -> new time), so sound cues placed against
the old audio can be moved to the same words in the new audio.

Usage: python -I tighten_narration.py SRC_DIR OUT_DIR [max_pause_s]
Needs numpy + soundfile (the mix venv) and ffmpeg.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

SRC, OUT = sys.argv[1], sys.argv[2]
MAXP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
SR, WIN, THR = 44100, 0.02, 10 ** (-38 / 20)
EDGE_IN, EDGE_OUT, XF = 0.05, 0.15, 0.02
os.makedirs(OUT, exist_ok=True)


def load(p):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


maps, report = {}, []
for f in sorted(os.listdir(SRC)):
    if not re.match(r"S\d\d[ab]?\.mp3$", f):
        continue
    x = load(os.path.join(SRC, f))
    w = int(WIN * SR)
    n = len(x) // w
    rms = np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1))
    loud = rms > THR
    idx = np.flatnonzero(loud)
    first, last = idx[0] * w, (idx[-1] + 1) * w
    # keep-segments in old samples: speech, with long silences cut down to MAXP
    keep, s = [], max(0, first - int(EDGE_IN * SR))
    run = None
    for i in range(idx[0], idx[-1] + 1):
        if not loud[i]:
            run = i if run is None else run
        elif run is not None:
            if (i - run) * WIN > MAXP:  # long pause: keep MAXP of it (half before, half after the cut)
                half = int(MAXP / 2 * SR)
                keep.append((s, run * w + half))
                s = i * w - half
            run = None
    keep.append((s, min(len(x), last + int(EDGE_OUT * SR))))
    out, knots, t_new = [], [], 0
    xf = int(XF * SR)
    for a, b in keep:
        seg = x[a:b].copy()
        if out:  # short crossfade at each cut
            seg[:xf] *= np.linspace(0, 1, xf)
            out[-1][-xf:] *= np.linspace(1, 0, xf)
        knots += [(a / SR, t_new / SR), (b / SR, (t_new + b - a) / SR)]
        out.append(seg)
        t_new += b - a
    y = np.concatenate(out)
    sf.write(os.path.join(OUT, f[:-4] + ".flac"), y, SR, subtype="PCM_24")
    maps[f[:-4]] = knots
    report.append((f[:-4], len(x) / SR, len(y) / SR))

json.dump(maps, open(os.path.join(OUT, "time_maps.json"), "w"), indent=0)
old, new = sum(r[1] for r in report), sum(r[2] for r in report)
for cid, a, b in report:
    print(f"{cid}: {a:6.2f} -> {b:6.2f} s")
print(f"total {old:.1f} -> {new:.1f} s (saved {old - new:.1f} s); max pause {MAXP} s")
