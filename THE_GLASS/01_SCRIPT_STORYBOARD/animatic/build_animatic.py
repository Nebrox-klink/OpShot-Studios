"""Provisional 13:00 animatic: one slate per shot (102), a TEMP TTS voice-over on the
storyboard timecodes, and the playable prototype cut in at 03:30–03:57.

Outputs (in --out):
  THE_GLASS_animatic_v001.mp4       960x540, 24 fps, burnt-in timecode
  vo_timing_report.csv              each VO line measured against its shot length
  vo_temp/                          TEMP VO wavs (Festival TTS, a timing guide ONLY)

Usage: python3 build_animatic.py --out <dir> --prototype <prototype_v001.mp4> [--prototype-audio <wav>]
"""
import argparse
import csv
import os
import pathlib
import subprocess
import textwrap
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
TRACKER = ROOT / "00_PROJECT_MANAGEMENT/shot_tracker.csv"
TYPO = ROOT / "03_2D_ASSETS/typography"
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--prototype", required=True)
ap.add_argument("--proto-start", type=float, default=210.0)
ap.add_argument("--proto-dur", type=float, default=27.0)
args = ap.parse_args()
OUT = pathlib.Path(args.out)
(OUT / "slates").mkdir(parents=True, exist_ok=True)
(OUT / "vo_temp").mkdir(exist_ok=True)
W, H, SR, FPS = 960, 540, 48000, 24

f_id = ImageFont.truetype(str(TYPO / "oswald-latin-600-normal.woff"), 64)
f_lab = ImageFont.truetype(str(TYPO / "oswald-latin-400-normal.woff"), 22)
f_vo = ImageFont.truetype(str(TYPO / "eb-garamond-latin-500-normal.woff"), 30)
f_txt = ImageFont.truetype(str(TYPO / "eb-garamond-latin-400-normal.woff"), 22)
f_tag = ImageFont.truetype(str(TYPO / "special-elite-latin-400-normal.woff"), 20)

NAVY, IVORY, AMBER, OXIDE, SLATE = (23, 33, 43), (233, 230, 222), (199, 139, 85), (169, 81, 73), (85, 103, 116)
CLS_COL = {"DOCUMENTED": (110, 160, 110), "RECONSTRUCTED FROM EVIDENCE": (110, 140, 185),
           "DRAMATISED / ILLUSTRATIVE": (170, 160, 140), "UNVERIFIED — REQUIRES REVIEW": OXIDE}


def tc2s(tc):
    h, m, s = (int(x) for x in tc.split(":"))
    return h * 3600 + m * 60 + s


def tts(text, path):
    raw = str(path) + ".raw.wav"
    subprocess.run(["text2wave", "-eval", "(voice_cmu_us_slt_arctic_hts)", "-o", raw], input=text.encode(), check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-ar", str(SR), "-ac", "1",
                    "-af", "atempo=0.84,highpass=f=90,acompressor=threshold=-18dB:ratio=3", str(path)], check=True)
    os.remove(raw)
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


rows = list(csv.DictReader(open(TRACKER, encoding="utf-8")))
total = tc2s(rows[-1]["end"])
vo_bus = np.zeros(int(total * SR) + SR, np.float32)
report = []
concat = []
for r in rows:
    sid, start, end = r["shot_id"], tc2s(r["start"]), tc2s(r["end"])
    dur = end - start
    is3d = r["type"] == "3D"
    # ---- slate
    im = Image.new("RGB", (W, H), (14, 19, 25))
    d = ImageDraw.Draw(im)
    band = OXIDE if is3d else (40, 72, 110)
    d.rectangle([0, 0, W, 70], fill=band)
    d.text((24, 12), f"{'🟥 3D CINEMATIC' if False else ('3D CINEMATIC' if is3d else '2D ANIMATION')}", font=f_lab, fill=IVORY)
    d.text((24, 38), r["chapter"], font=f_lab, fill=IVORY)
    d.text((W - 24, 12), f"{r['start'][3:]} – {r['end'][3:]}  ({dur}s)", font=f_lab, fill=IVORY, anchor="ra")
    d.text((W - 24, 38), f"P: {r['priority']}   status: {r['production_status']}", font=f_lab, fill=IVORY, anchor="ra")
    d.text((24, 88), sid, font=f_id, fill=AMBER)
    vo = r["vo_exact"] if not r["vo_exact"].startswith("—") else "(no voice-over)"
    y = 210
    d.text((24, y - 26), "VO", font=f_lab, fill=SLATE)
    for line in textwrap.wrap(f"“{vo}”" if not vo.startswith("(") else vo, 58)[:4]:
        d.text((24, y), line, font=f_vo, fill=IVORY)
        y += 38
    y += 14
    d.text((24, y), "CAMERA", font=f_lab, fill=SLATE)
    y += 26
    for line in textwrap.wrap(r["camera"] or "", 80)[:2]:
        d.text((24, y), line, font=f_txt, fill=(190, 190, 185))
        y += 28
    cls = r["source_class"]
    d.rectangle([24, H - 62, 24 + 14, H - 48], fill=CLS_COL.get(cls, SLATE))
    d.text((46, H - 66), f"{cls}   ·   {r['source_ids']}"[:95], font=f_tag, fill=(200, 196, 188))
    d.text((24, H - 34), "TEMP ANIMATIC · TTS VOICE IS A TIMING GUIDE, NOT THE NARRATOR", font=f_tag, fill=(120, 126, 132))
    p = OUT / "slates" / f"{sid}.png"
    im.save(p)
    concat.append((p, dur))
    # ---- VO
    vo_dur = 0.0
    if not r["vo_exact"].startswith("—"):
        x = tts(r["vo_exact"], OUT / "vo_temp" / f"{sid}.wav")
        vo_dur = len(x) / SR
        i = int((start + 0.25) * SR)
        vo_bus[i:i + len(x)] += x / (np.abs(x).max() + 1e-9) * 0.5
    over = round(vo_dur + 0.25 - dur, 2)
    report.append([sid, r["chapter"], r["type"], dur, round(vo_dur, 2), over,
                   "OVERRUN" if over > 0.0 else ("TIGHT" if over > -0.6 else "OK"), r["vo_exact"]])

with open(OUT / "vo_timing_report.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["shot_id", "chapter", "type", "shot_s", "temp_vo_s", "overrun_s", "flag", "vo_exact"])
    w.writerows(report)

# ---- slates → video
lst = OUT / "concat.txt"
with open(lst, "w") as f:
    for p, dur in concat:
        f.write(f"file '{p}'\nduration {dur}\n")
    f.write(f"file '{concat[-1][0]}'\n")
base = OUT / "slates_only.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "26", "-preset", "veryfast", str(base)], check=True)

# ---- audio: VO bus, but the prototype's own mix replaces the bus inside its window
ps, pd_ = args.proto_start, args.proto_dur
vo_bus[int(ps * SR):int((ps + pd_) * SR)] = 0
vo_path = OUT / "vo_bus.wav"
with wave.open(str(vo_path), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(vo_bus, -1, 1) * 32767).astype(np.int16).tobytes())

font = str(ROOT / "03_2D_ASSETS/typography/oswald-latin-400-normal.woff")
dejavu = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
tcfont = dejavu if os.path.exists(dejavu) else font
final = OUT / "THE_GLASS_animatic_v001.mp4"
fc = (f"[1:v]scale={W}:{H},setpts=PTS-STARTPTS+{ps}/TB[pv];"
      f"[0:v][pv]overlay=enable='between(t,{ps},{ps + pd_})':eof_action=pass[v1];"
      f"[v1]drawtext=fontfile={tcfont}:text='%{{pts\\:hms}}':x=w-tw-14:y=h-th-12:fontsize=20:fontcolor=white@0.85:box=1:boxcolor=black@0.5[v];"
      f"[1:a]adelay={int(ps * 1000)}|{int(ps * 1000)}[pa];[2:a]aformat=channel_layouts=stereo[va];"
      f"[va][pa]amix=inputs=2:normalize=0:duration=first[a]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(base), "-i", args.prototype, "-i", str(vo_path),
                "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "27", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "128k", "-t", str(total), "-movflags", "+faststart", str(final)], check=True)
print("wrote", final)
n_over = sum(1 for r in report if r[6] == "OVERRUN")
print(f"VO overruns: {n_over} of {sum(1 for r in report if r[4] > 0)} voiced shots")
