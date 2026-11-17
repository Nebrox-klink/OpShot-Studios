"""Split ElevenLabs narration blocks (one mp3 per block of consecutive lines) into one wav per shot.

Each block was generated with the lines separated by blank lines, so the narrator pauses between them.
For a block of N lines we cut at the N-1 longest pauses (in time order), then trim silence at both ends.
Writes voiceover/verdict_v001/SH-xxx.wav (48 kHz mono) and verdict_v001_split_report.csv.

  python3 07_AUDIO/split_narration_blocks.py
"""
import csv
import pathlib
import subprocess

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLK = ROOT / "07_AUDIO/voiceover/verdict_v001_blocks"
OUT = ROOT / "07_AUDIO/voiceover/verdict_v001"
SR = 48000
BLOCKS = {
    "B0": ["SH-001", "SH-002", "SH-003", "SH-004", "SH-005", "SH-006", "SH-007"],
    "B1": [f"SH-{i:03d}" for i in range(8, 17)],
    "B2": [f"SH-{i:03d}" for i in range(17, 28)],
    "B3": ["SH-028", "SH-029", "SH-030", "SH-033", "SH-034"] + [f"SH-{i:03d}" for i in range(35, 42)],
    "B4": [f"SH-{i:03d}" for i in range(42, 50)] + ["SH-052"] + [f"SH-{i:03d}" for i in range(53, 60)],
    "B5": ["SH-060", "SH-061", "SH-062", "SH-063", "SH-068", "SH-069", "SH-070"],
    "B6": [f"SH-{i:03d}" for i in range(71, 83)] + ["SH-084", "SH-087", "SH-088"],
    "B7": [f"SH-{i:03d}" for i in range(89, 103)],
}
FR = 0.02  # analysis frame, s


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def write(p, x):
    import wave
    with wave.open(str(p), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


import json
TXT = {sid: t for v in json.load(open(ROOT / "07_AUDIO/voiceover/narration_chapters_v001.json", encoding="utf-8")).values() for sid, t in v}
OUT.mkdir(parents=True, exist_ok=True)
report = []
for b, shots in BLOCKS.items():
    src = BLK / f"{b}.mp3"
    if not src.exists():
        print("missing", src)
        continue
    x = load(src)
    hop = int(FR * SR)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
    db = 20 * np.log10(rms + 1e-9)
    thr = np.percentile(db, 90) - 32
    silent = db < thr
    gaps, i = [], 0
    while i < len(silent):
        if silent[i]:
            j = i
            while j < len(silent) and silent[j]:
                j += 1
            if i > 0 and j < len(silent):
                gaps.append((j - i, i, j))
            i = j
        else:
            i += 1
    need = len(shots) - 1
    # choose N-1 cut pauses that best match each line's expected length (characters), favouring long pauses
    chars = [len(TXT[sid]) for sid in shots]
    speech = float((~silent).sum()) * FR
    rate = speech / sum(chars)
    G = [g for g in gaps if g[0] * FR >= 0.12]
    pos = [(g[1] + g[2]) / 2 * FR for g in G]
    T = len(silent) * FR
    INF = 1e18
    # cost[k][j]: best cost with k-th cut at gap j
    import math
    cost = [[INF] * len(G) for _ in range(need)]
    back = [[-1] * len(G) for _ in range(need)]

    def seg_cost(a, b, k):
        sil = float(silent[int(a / FR):int(b / FR)].sum()) * FR
        exp = chars[k] * rate
        return ((b - a - sil) - exp) ** 2 / max(exp, 0.5)

    for j in range(len(G)):
        cost[0][j] = seg_cost(0, pos[j], 0) - 2.0 * G[j][0] * FR
    for k in range(1, need):
        for j in range(len(G)):
            best, arg = INF, -1
            for i in range(j):
                if cost[k - 1][i] < INF:
                    c = cost[k - 1][i] + seg_cost(pos[i], pos[j], k)
                    if c < best:
                        best, arg = c, i
            cost[k][j] = best - 2.0 * G[j][0] * FR if best < INF else INF
            back[k][j] = arg
    if need == 0:
        cuts = []
    else:
        endc = [cost[need - 1][j] + seg_cost(pos[j], T, need) for j in range(len(G))]
        j = int(np.argmin(endc)); sel = [j]
        for k in range(need - 1, 0, -1):
            j = back[k][j]; sel.append(j)
        cuts = [G[j] for j in reversed(sel)]
    ok = len(cuts) == need
    bounds = [0] + [int((g[1] + g[2]) / 2 * hop) for g in cuts] + [len(x)]
    for k, sid in enumerate(shots):
        seg = x[bounds[k]:bounds[k + 1]]
        sd = db[bounds[k] // hop: bounds[k + 1] // hop]
        on = np.where(sd >= thr)[0]
        if len(on):
            a, z = max(0, on[0] * hop - int(0.04 * SR)), min(len(seg), (on[-1] + 1) * hop + int(0.12 * SR))
            seg = seg[a:z]
        write(OUT / f"{sid}.wav", seg)
        report.append([b, sid, round(len(seg) / SR, 2), "ok" if ok else "CHECK"])
    shortest = min((g[0] * FR for g in cuts), default=0)
    print(b, "lines", len(shots), "cuts", len(cuts), "shortest cut pause %.2fs" % shortest)
with open(ROOT / "07_AUDIO/voiceover/verdict_v001_split_report.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["block", "shot_id", "seconds", "status"]); w.writerows(report)
print("wrote", len(report), "lines")
