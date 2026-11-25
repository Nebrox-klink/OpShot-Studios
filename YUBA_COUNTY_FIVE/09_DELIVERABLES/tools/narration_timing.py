"""Sentence timing for Brian's narration without a speech model.

The text comes from brian_prompts_v001.json. Pauses come from ffmpeg silencedetect. Sentence boundaries are matched
to pauses by a monotonic DP that prefers long pauses near the time a character-proportional reading predicts.
phrase_time(scene_id, phrase) -> seconds from the start of the mp3 when that phrase begins (interpolated by characters
inside its sentence).
"""
import json
import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
AUD = os.path.join(ROOT, "07_AUDIO/brian_v001")
PROMPTS = {p["id"]: p["text"] for p in json.load(open(os.path.join(AUD, "brian_prompts_v001.json")))}


def clean(t):
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", " ", t)).strip()


def sentences(t):
    t = clean(t)
    parts = re.split(r'(?:(?<=[.?!])|(?<=[.?!][”"]))\s+', t)
    return [p for p in parts if p]


def speech_spans(path):
    out = subprocess.run(["ffmpeg", "-nostdin", "-i", path, "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                               capture_output=True, text=True).stdout)
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    sil = list(zip(st, en + [dur] * (len(st) - len(en))))
    return sil, dur


_cache = {}


def timing(sid):
    """[(sentence, start, end)] in mp3 seconds."""
    if sid in _cache:
        return _cache[sid]
    path = os.path.join(AUD, sid + ".mp3")
    sil, dur = speech_spans(path)
    sents = sentences(PROMPTS[sid])
    v0 = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0          # voice onset
    v1 = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur  # voice end
    gaps = [(a, b) for a, b in sil if a > v0 + 0.1 and b < v1 - 0.1]
    n = len(sents) - 1
    lens = [len(s) for s in sents]
    tot = sum(lens)
    exp, c = [], 0
    for L in lens[:-1]:
        c += L
        exp.append(v0 + (v1 - v0) * c / tot)
    # DP: choose n gaps in order; cost = |mid - expected| / span - 4 * gap length
    span = max(v1 - v0, 1)
    G = len(gaps)
    INF = 1e9
    if n == 0:
        res = [(sents[0], v0, v1)]
        _cache[sid] = res
        return res
    if G < n:
        raise SystemExit(f"{sid}: {G} pauses for {n} sentence boundaries")
    cost = [[INF] * G for _ in range(n)]
    back = [[-1] * G for _ in range(n)]
    for i in range(n):
        for j in range(G):
            a, b = gaps[j]
            local = abs((a + b) / 2 - exp[i]) / span * 10 - 4 * (b - a)
            if i == 0:
                cost[i][j] = local
            else:
                best = min(range(j), key=lambda k: cost[i - 1][k], default=None)
                if best is not None and cost[i - 1][best] < INF:
                    cost[i][j] = cost[i - 1][best] + local
                    back[i][j] = best
    j = min(range(G), key=lambda k: cost[n - 1][k])
    picks = []
    for i in range(n - 1, -1, -1):
        picks.append(j)
        j = back[i][j]
    picks.reverse()
    bounds = [v0] + [x for p in picks for x in gaps[p]] + [v1]
    res = [(sents[i], bounds[2 * i], bounds[2 * i + 1]) for i in range(len(sents))]
    _cache[sid] = res
    return res


def phrase_time(sid, phrase):
    for s, a, b in timing(sid):
        k = s.find(phrase)
        if k >= 0:
            return a + (b - a) * k / max(len(s), 1)
    raise KeyError(f"{sid}: phrase not found: {phrase!r}")


if __name__ == "__main__":
    import sys
    for sid in sys.argv[1:] or sorted(PROMPTS):
        print(f"== {sid}")
        for s, a, b in timing(sid):
            print(f"  {a:6.2f}-{b:6.2f}  {s[:70]}")
