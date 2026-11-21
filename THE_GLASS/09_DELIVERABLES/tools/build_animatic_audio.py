"""Build the free audio-only screening animatic from a script .md.

Placeholder voice: Kokoro-82M via kokoro-onnx (offline, Apache-2.0 weights). Not the final narrator.
Output: a narration WAV laid out on the scene slots, plus an MP4 with black scene slates.

Usage:
  python -I build_animatic_audio.py SCRIPT.md MODELS_DIR OUT_DIR [voice] [speed]
Needs: kokoro-onnx, soundfile, pillow, numpy; ffmpeg on PATH.
"""
import os
import re
import subprocess
import sys
import textwrap

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from PIL import Image, ImageDraw, ImageFont

src, models, out = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
voice = sys.argv[4] if len(sys.argv) > 4 else "am_michael"
speed = float(sys.argv[5]) if len(sys.argv) > 5 else 0.9
os.makedirs(os.path.join(out, "slates"), exist_ok=True)

# Placeholder pronunciation respellings (see the script's pronunciation guide).
SAY = [("Arne Sigve Klungland", "Arneh Sigveh Kloongland"), ("Klungland", "Kloongland"),
       ("Kjell Alrich Schumann", "Shell Ahlrick Shooman"), ("Schumann", "Shooman"), ("Håland", "Hawlan"),
       ("Sørmarka", "Surmarka"), ("Nedre Dalgate", "Nehdreh Dahlgahteh"), ("NOKAS", "Nookahs"),
       ("Stavanger", "Stavahnger"), ("Sandnes", "Sahnness"), ("Toska", "Toskah")]
GAP, LEAD, CARD = 0.45, 1.0, 4.0

scene_re = re.compile(r"^#### Scene (\d+) · (.+?) \((\d+):(\d+)–(\d+):(\d+)\)")
act_re = re.compile(r"^### (COLD OPEN|ACT .+)")
scenes, cur, act, section = [], None, "", None
for line in open(src, encoding="utf-8"):
    line = line.rstrip("\n")
    if m := act_re.match(line):
        act = m.group(1)
        continue
    if m := scene_re.match(line):
        n, title, a, b, c, d = m.groups()
        cur = dict(n=int(n), title=title, act=act, start=int(a) * 60 + int(b), end=int(c) * 60 + int(d),
                   items=[], shots=[], sound="")
        scenes.append(cur)
        continue
    if cur is None:
        continue
    if line.startswith("**VISUAL**"):
        section = "v"
    elif line.startswith("**NARRATION**"):
        section = "n"
    elif line.startswith("**SOUND:**"):
        cur["sound"], section = line.replace("**SOUND:**", "").strip(), None
    elif line.startswith("**DIALOGUE"):
        section = None
    elif section == "v" and re.match(r"^\d+\. ", line):
        shot = re.sub(r"\*\*\[[^]]*\]\*\*|\*\*|`[^`]*`|\*\([^)]*\)\*", "", line).strip()
        cur["shots"].append(shot)
    elif section == "n" and line.startswith("> "):
        body = line[2:].strip()
        if body.startswith("*("):
            cur["items"].append(("pause", 6.0 if "white" in body else 3.0 if "hold" in body else 1.0))
        else:
            cur["items"].append(("say", re.sub(r"\s*`[^`]*`", "", body).strip()))

k = Kokoro(os.path.join(models, "kokoro-v1.0.onnx"), os.path.join(models, "voices-v1.0.bin"))
SR = 24000
lang = "en-us" if voice.startswith("a") else "en-gb"
track, report, t = [], [], 0.0
sil = lambda s: np.zeros(int(round(s * SR)), dtype=np.float32)

# Disclosure card (silent) before the film.
track.append(sil(CARD))
t = CARD
timeline = []
for s in scenes:
    slot = s["end"] - s["start"]
    parts = [sil(LEAD)]
    for kind, val in s["items"]:
        if kind == "pause":
            parts.append(sil(val))
            continue
        text = val
        for a, b in SAY:
            text = text.replace(a, b)
        audio, sr = k.create(text, voice=voice, speed=speed, lang=lang)
        assert sr == SR
        parts += [audio.astype(np.float32), sil(GAP)]
    used = sum(len(p) for p in parts) / SR
    length = max(slot, used + 0.5)
    parts.append(sil(length - used))
    seg = np.concatenate(parts)
    timeline.append((s, t, length))
    report.append((s["n"], s["title"], slot, used, length))
    track.append(seg)
    t += length
audio = np.concatenate(track)
peak = float(np.max(np.abs(audio))) or 1.0
audio = audio / peak * 0.89
wav = os.path.join(out, "narration_placeholder.wav")
sf.write(wav, audio, SR)

# Slates.
W, H = 1280, 720
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 44)
fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)


def slate(path, head, sub, lines, foot=""):
    im = Image.new("RGB", (W, H), (8, 8, 10))
    d = ImageDraw.Draw(im)
    d.text((80, 70), sub, font=fs, fill=(140, 140, 150))
    d.text((80, 105), head, font=fb, fill=(230, 230, 230))
    y = 200
    for ln in lines:
        for w in textwrap.wrap(ln, 95)[:2]:
            d.text((80, y), w, font=ft, fill=(170, 170, 175))
            y += 26
        y += 8
        if y > H - 120:
            break
    if foot:
        for i, w in enumerate(textwrap.wrap(foot, 110)[:2]):
            d.text((80, H - 90 + i * 24), w, font=ft, fill=(110, 110, 120))
    d.text((W - 360, H - 40), "AUDIO ANIMATIC · placeholder voice", font=ft, fill=(90, 90, 100))
    im.save(path)


lst = os.path.join(out, "slates", "list.txt")
with open(lst, "w") as fh:
    p = os.path.join(out, "slates", "s00.png")
    slate(p, "", "", ["A dramatised reconstruction of real events. Illustrations are AI-assisted and the narration "
                      "voice is synthetic. Quotes are from published interviews."])
    fh.write(f"file '{p}'\nduration {CARD}\n")
    for s, start, length in timeline:
        p = os.path.join(out, "slates", f"s{s['n']:02d}.png")
        mm, ss = divmod(int(start), 60)
        slate(p, f"{s['n']} · {s['title']}", f"{s['act']}  ·  {mm}:{ss:02d}", s["shots"], "SOUND: " + s["sound"])
        fh.write(f"file '{p}'\nduration {length:.3f}\n")
    fh.write(f"file '{p}'\n")
mp4 = os.path.join(out, "THE_GLASS_animatic_audio_v008.mp4")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                "-vf", "fps=6,format=yuv420p", "-c:v", "libx264", "-tune", "stillimage", "-crf", "28",
                "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4], check=True)

print(f"voice {voice} speed {speed} total {t:.1f} s")
for n, title, slot, used, length in report:
    flag = "  <- extended" if length > slot else ""
    print(f"{n:2d} {title:24s} slot {slot:3d}s  speech+pauses {used:5.1f}s{flag}")
print("WROTE", mp4)
