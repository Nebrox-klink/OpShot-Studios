"""English subtitles (.srt + Netflix-style .ass) for the narration, timed to the real audio.

Text comes from the Atlas narration prompts (exactly what the voice says; IPA spellings swapped back to names).
Timing: each chunk is placed on the timeline exactly as the mix places it (mix_sound_v008.py rule), then the
cues inside a chunk are spread over its detected speech (ffmpeg silencedetect) by character count, and their
edges snapped to the nearest pause. Rules (streaming-style): max 42 chars per line, max 2 lines, 0.83-7 s per cue,
<= 20 chars/s where possible, 2-frame gap between cues.

Usage: python3 -I make_subtitles.py THE_GLASS_ROOT CLIPS_DIR OUT_BASENAME
  CLIPS_DIR = a master's clips/ folder, used to find on-screen text at the bottom (lower-thirds, captions);
  cues that overlap it are raised above it.
Writes OUT_BASENAME.srt and OUT_BASENAME.ass.
"""
import json
import os
import re
import subprocess
import sys

ROOT, CLIPS, OUTB = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]
ATLAS = os.path.join(ROOT, "07_AUDIO/atlas_v008")
SCRIPT = os.path.join(ROOT, "01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v008.md")
MAXL, FPS = 42, 24
NAMES = {"/ˈɑːrnə ˈsɪɡvə ˈkluːŋlænd/": "Arne Sigve Klungland", "/ˈkluːŋlænd/": "Klungland", "/ˈʃuːmən/": "Schumann",
         "/stɑːˈvɑːŋər/": "Stavanger", "/ˈhɔːlɑːn/": "Håland", "/ˈneːdrə ˈdɑːlɡɑːtə/": "Nedre Dalgate",
         "/ˈnuːkɑːs/": "NOKAS", "/ˈsɑːnnəs/": "Sandnes", "/ˈsɜːrmɑːrkə/": "Sørmarka"}


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
    for a, b in NAMES.items():
        t = t.replace(a, b)
    t = re.sub(r"\[[^\]]+\]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def split_cues(text):
    """Sentences, then long sentences at commas/dashes, then at the middle word, until each fits 2x42."""
    out = []
    for s in re.split(r"(?<=[.!?…])\s+(?=[A-Z0-9\"“'‘])", text):
        todo = [s.strip()]
        while todo:
            c = todo.pop(0)
            if len(c) <= 2 * MAXL - 6 and fits(c):
                out.append(c)
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
             "would", "could", "should", "not", "very", "Arne", "Sigve", "Nedre", "Mr"}
BAD_BEFORE = {"it", "them", "him", "her", "me", "us", "kilos", "minutes", "seconds", "million", "kroner"}


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


# ---- timeline: shared with the mix and the picture (timing.py) ---------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timing  # noqa: E402

prompts = {x["id"]: x["text"] for x in json.load(open(os.path.join(ATLAS, "atlas_prompts_v008.json"), encoding="utf-8"))}
TL = timing.timeline(ROOT)
chunks = [(cid, v["start"] + off, p) for n, v in sorted(TL["scenes"].items()) for cid, off, p in v["chunks"]]

# ---- cues --------------------------------------------------------------------------------------------------------
cues = []
for cid, t0, path in chunks:
    segs = speech(path)
    total = sum(b - a for a, b in segs)
    texts = split_cues(clean(prompts[cid]))
    weights = [len(x) + 6 for x in texts]  # +6: each cue boundary costs a little time (breath)
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
    for i in range(1, len(edges) - 1):  # snap inner edges to a pause if one is near, never squeezing a cue
        near = min(pauses, key=lambda p: abs(p - edges[i]))
        floor_l = edges[i - 1] + max(0.6, len(texts[i - 1]) / 22)
        ceil_r = edges[i + 1] - max(0.6, len(texts[i]) / 22)
        if abs(near - edges[i]) < 0.6 and floor_l <= near <= ceil_r:
            edges[i] = near
    part = [[t0 + edges[i], t0 + edges[i + 1] + 0.25, x] for i, x in enumerate(texts)]
    i = 0
    while i < len(part):  # merge a cue shorter than 0.83 s with a neighbour in the same chunk when it fits
        a, b, x = part[i]
        avail = min(b, part[i + 1][0] - 2 / FPS) if i + 1 < len(part) else b
        if avail - a < 1.0 and len(part) > 1:
            j = i + 1 if i + 1 < len(part) else i - 1
            lo, hi = min(i, j), max(i, j)
            merged = part[lo][2] + " " + part[hi][2]
            if fits(merged) and part[hi][1] - part[lo][0] <= 7.0:
                part[lo:hi + 1] = [[part[lo][0], part[hi][1], merged]]
                continue
        i += 1
    if cid == "S17a":  # the white silence follows: the last line must leave with the voice, not hang on white
        part[-1][1] = min(part[-1][1], t0 + dur(path) - 1 / FPS)
    cues += part

gap = 2 / FPS
for i, c in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else 1e9
    c[1] = max(c[1], c[0] + 5 / 6)          # minimum 0.83 s
    c[1] = min(c[1], c[0] + 7.0, nxt - gap)  # maximum 7 s, keep a 2-frame gap

# ---- bottom-of-frame text in the picture (lower-thirds, captions): raise cues that overlap it --------------------
clips = [ln.split("'")[1] for ln in open(os.path.join(CLIPS, "list.txt"))]
starts, acc = {}, 0.0
for c in clips:
    k = int(os.path.basename(c)[1:4])
    starts[k] = (acc, acc + dur(c))
    acc = starts[k][1]
busy = []
for f in os.listdir(CLIPS):
    if m := re.match(r"t(\d{3})_\d+\.txt$", f):
        txt = open(os.path.join(CLIPS, f), encoding="utf-8").read()
        if re.search(r"to NRK|as recounted|^Arne Sigve Klungland$|In memory", txt):
            busy.append(starts[int(m.group(1))])

# ---- write -------------------------------------------------------------------------------------------------------
def ts(x, sep=","):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{int(round((s % 1) * 1000)) % 1000:03d}"


def ass_ts(x):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


with open(OUTB + ".srt", "w", encoding="utf-8") as fh:
    for i, (a, b, x) in enumerate(cues, 1):
        fh.write(f"{i}\n{ts(a)} --> {ts(b)}\n" + "\n".join(lines(x)) + "\n\n")

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Netflix,Inter Medium,50,&H00FFFFFF,&H00FFFFFF,&H00101010,&H8C000000,0,0,0,0,100,100,0,0,1,1.6,2.2,2,160,160,72,1
Style: Raised,Inter Medium,50,&H00FFFFFF,&H00FFFFFF,&H00101010,&H8C000000,0,0,0,0,100,100,0,0,1,1.6,2.2,2,160,160,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
raised = 0
with open(OUTB + ".ass", "w", encoding="utf-8") as fh:
    fh.write(ASS_HEAD)
    for a, b, x in cues:
        up = any(a < e and b > s for s, e in busy)
        raised += up
        body = "\\N".join(lines(x))
        fh.write(f"Dialogue: 0,{ass_ts(a)},{ass_ts(b)},{'Raised' if up else 'Netflix'},,0,0,0,,{body}\n")

cps = [len(x) / (b - a) for a, b, x in cues]
print(f"{len(cues)} cues; {sum(c > 20 for c in cps)} above 20 chars/s; max {max(cps):.1f} cps; "
      f"{raised} raised above on-screen text; last cue ends {ts(cues[-1][1])}")
print("WROTE", OUTB + ".srt", OUTB + ".ass")
