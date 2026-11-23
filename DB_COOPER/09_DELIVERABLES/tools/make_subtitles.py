"""English subtitles (.srt + .ass) for the D.B. Cooper narration, timed to the real audio.

Text: the Brian prompts (exactly what the voice says, direction tags removed) and Cooper's line (in italics).
Timing: the same timeline as build_animatic.py / mix_sound_v001.py (LEAD 1.0 s + narration [+0.4 s + dialogue] + TAIL
0.5 s per scene, scene 2 = 6 s title). Inside a scene, cues are spread over the detected speech by character count and
their edges snapped to the nearest pause (logic reused from the NOKAS subtitle tool). Rules: max 42 chars per line,
max 2 lines, 0.83-7 s per cue, 2-frame gap.

Usage: python3 -I make_subtitles.py DB_COOPER_ROOT OUT_BASENAME
"""
import json
import os
import re
import subprocess
import sys

ROOT, OUTB = os.path.abspath(sys.argv[1]), sys.argv[2]
AUD = os.path.join(ROOT, "07_AUDIO/brian_v001")
COOPER = (4, os.path.join(ROOT, "07_AUDIO/cooper_v001/C04_miss_note_bomb.mp3"),
          "Miss, you'd better look at that note. I have a bomb.")
LEAD, TAIL, GAP = 1.0, 0.5, 0.4
MAXL, FPS = 42, 25


def decoded(p):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", p, "-f", "s16le", "-ac", "1", "-ar", "44100", "-"],
                         capture_output=True, check=True).stdout
    return len(raw) / 2 / 44100


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def speech(p):
    """Speech segments (start, end) inside one chunk, from silencedetect."""
    err = subprocess.run(["ffmpeg", "-nostdin", "-i", p, "-af", "silencedetect=noise=-38dB:d=0.22", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    D = dur(p)
    sil = [(float(a), float(b)) for a, b in re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", err)]
    segs, cur = [], 0.0
    for a, b in sil:
        if a > cur + 0.05:
            segs.append((cur, a))
        cur = max(cur, b)
    if D > cur + 0.05:
        segs.append((cur, D))
    return segs or [(0.0, D)]


def clean(t):
    t = re.sub(r"\[[^\]]+\]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def split_cues(text):
    """Sentences, then long sentences at commas/dashes, then at the middle word, until each fits 2x42."""
    out = []
    text = text.replace("D.B.", "D\u2024B\u2024")  # keep "D.B." from ending a sentence
    for s in re.split(r"(?:(?<=[.!?…])|(?<=[.!?…][\"”]))\s+(?=[A-Z0-9\"“'‘])", text):
        todo = [s.strip()]
        while todo:
            c = todo.pop(0)
            if len(c) <= 2 * MAXL - 6 and fits(c):
                out.append(c.replace("\u2024", "."))
                continue
            cut = None
            mid = len(c) / 2
            for m in re.finditer(r"[,;:—–] ", c):
                if 15 < m.end() < len(c) - 12 and (cut is None or abs(m.end() - mid) < abs(cut - mid)):
                    cut = m.end()
            if cut is None:
                sp = [m.start() for m in re.finditer(" ", c)]
                cut = min(sp, key=lambda i: abs(i - mid)) + 1
            todo[:0] = [c[:cut].strip(), c[cut:].strip()]
    return out


GOOD_BEFORE = {"and", "but", "or", "with", "to", "in", "on", "at", "of", "for", "from", "that", "who", "which",
               "when", "while", "because", "as", "into", "behind", "after", "before", "where", "than", "if"}
BAD_AFTER = {"a", "an", "the", "to", "of", "his", "her", "their", "its", "my", "had", "has", "was", "were", "is",
             "would", "could", "should", "not", "very", "Mr", "D.B."}
BAD_BEFORE = {"it", "them", "him", "her", "me", "us", "kilos", "minutes", "seconds", "dollars", "thousand"}


def lines(c):
    """Streaming-style line break: both lines <= 42, balanced, breaking at grammar boundaries."""
    if len(c) <= MAXL:
        return [c]
    sp = [m.start() for m in re.finditer(" ", c)]

    def score(i):
        prev, nxt = c[:i].split()[-1], c[i + 1:].split()[0]
        p = abs(i - len(c) / 2)
        if max(i, len(c) - i - 1) > MAXL:
            p += 1000
        if prev[-1] in ",;:—–.":
            p -= 12
        if nxt.lower().strip('"“') in GOOD_BEFORE:
            p -= 7
        if prev.endswith(("'s", "’s")):
            p += 14
        if prev.strip('"“') in BAD_AFTER or prev.lower() in BAD_AFTER:
            p += 14
        if nxt.lower().rstrip(".,;:") in BAD_BEFORE:
            p += 14
        return p
    best = min(sp, key=score)
    return [c[:best], c[best + 1:]]


def fits(c):
    return all(len(x) <= MAXL for x in lines(c)) and len(lines(c)) <= 2


# ---- timeline (same rule as the animatic and the mix) ---------------------------------------------------------
prompts = {x["id"]: x["text"] for x in json.load(open(os.path.join(AUD, "brian_prompts_v001.json"), encoding="utf-8"))}
chunks, t = [], 0.0  # (text, start, audio path, italic)
for sc in range(1, 24):
    p = os.path.join(AUD, f"S{sc:02d}.mp3")
    if not os.path.isfile(p):
        t += 6.0
        continue
    chunks.append((clean(prompts[f"S{sc:02d}"]), t + LEAD, p, False))
    if sc == COOPER[0]:
        n = decoded(p)
        chunks.append((COOPER[2], t + LEAD + n + GAP, COOPER[1], True))
        L = LEAD + n + GAP + decoded(COOPER[1]) + TAIL
    else:
        L = LEAD + dur(p) + TAIL
    t += L
TOTAL = t

# ---- cues --------------------------------------------------------------------------------------------------------
cues = []
for text, t0, path, ital in chunks:
    segs = speech(path)
    total = sum(b - a for a, b in segs)
    texts = split_cues(text)
    weights = [len(x) + 6 for x in texts]
    W = sum(weights)
    bounds_sp = [0.0]
    for w in weights:
        bounds_sp.append(bounds_sp[-1] + total * w / W)

    def sp2t(x):
        for a, b in segs:
            if x <= b - a + 1e-9:
                return a + x
            x -= b - a
        return segs[-1][1]
    edges = [sp2t(x) for x in bounds_sp]
    pauses = [b for a, b in segs] + [a for a, b in segs]
    for i in range(1, len(edges) - 1):
        near = min(pauses, key=lambda p: abs(p - edges[i]))
        floor_l = edges[i - 1] + max(0.6, len(texts[i - 1]) / 22)
        ceil_r = edges[i + 1] - max(0.6, len(texts[i]) / 22)
        if abs(near - edges[i]) < 0.6 and floor_l <= near <= ceil_r:
            edges[i] = near
    part = [[t0 + edges[i], t0 + edges[i + 1] + 0.25, x, ital] for i, x in enumerate(texts)]
    i = 0
    while i < len(part):
        a, b, x, it = part[i]
        avail = min(b, part[i + 1][0] - 2 / FPS) if i + 1 < len(part) else b
        if avail - a < 1.0 and len(part) > 1:
            j = i + 1 if i + 1 < len(part) else i - 1
            lo, hi = min(i, j), max(i, j)
            merged = part[lo][2] + " " + part[hi][2]
            if fits(merged) and part[hi][1] - part[lo][0] <= 7.0:
                part[lo:hi + 1] = [[part[lo][0], part[hi][1], merged, it]]
                continue
        i += 1
    cues += part

gap = 2 / FPS
for i, c in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else 1e9
    c[1] = max(c[1], c[0] + 5 / 6)
    c[1] = min(c[1], c[0] + 7.0, nxt - gap, TOTAL)


def ts(x, sep=","):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)) % 1000:03d}"


def ass_ts(x):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


with open(OUTB + ".srt", "w", encoding="utf-8") as fh:
    for i, (a, b, x, it) in enumerate(cues, 1):
        body = "\n".join(lines(x))
        fh.write(f"{i}\n{ts(a)} --> {ts(b)}\n" + (f"<i>{body}</i>" if it else body) + "\n\n")

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Netflix,Inter Medium,50,&H00FFFFFF,&H00FFFFFF,&H00101010,&H8C000000,0,0,0,0,100,100,0,0,1,1.6,2.2,2,160,160,72,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open(OUTB + ".ass", "w", encoding="utf-8") as fh:
    fh.write(ASS_HEAD)
    for a, b, x, it in cues:
        body = "\\N".join(lines(x))
        fh.write(f"Dialogue: 0,{ass_ts(a)},{ass_ts(b)},Netflix,,0,0,0,,{'{\\i1}' if it else ''}{body}\n")

cps = [len(x) / (b - a) for a, b, x, _ in cues]
print(f"{len(cues)} cues; {sum(c > 20 for c in cps)} above 20 chars/s; max {max(cps):.1f} cps; "
      f"timeline {TOTAL:.2f} s; last cue ends {ts(cues[-1][1])}")
print("WROTE", OUTB + ".srt", OUTB + ".ass")
