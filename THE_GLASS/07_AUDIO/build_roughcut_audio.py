"""Rough-cut v001 audio: 13:00, 48 kHz stereo, all procedural and licence-free.

Layers:
  A1 narration : TEMP TTS lines (01_SCRIPT_STORYBOARD/animatic vo_temp/SH-xxx.wav), placed at shot start + 0.25 s.
                 Lines never overlap: if a line would collide with the previous one it is delayed,
                 and the delay is logged (vo_drift.csv). Re-time with the real narrator.
  A2 atmos     : per-chapter beds (harbour wash, room tone, city morning, forest wind, café, courtroom).
  A3 SFX       : the recurring motifs: glass THUNK, clock tick, ram impacts, muffled gunfire pulses,
                 crack tinkle, door slam, paper.
  A4 music     : a restrained synthesised pad + single piano notes (Klungland, epilogue).
  03:30–03:57  : the prototype v001 mix is inserted as is.

Usage: python build_roughcut_audio.py --vo <vo_temp dir> --proto <prototype mix wav> --out <dir>
"""
import argparse
import csv
import os
import pathlib
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
SR = 48000
DUR = 780.0
N = int(SR * DUR)
ap = argparse.ArgumentParser()
ap.add_argument("--vo", required=True)
ap.add_argument("--proto", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
rng = np.random.default_rng(13)
t_all = np.arange(N) / SR


def tc(s):
    h, m, x = (int(v) for v in s.split(":"))
    return h * 3600 + m * 60 + x


def rd(path):
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2)
        return x, w.getframerate()


def lp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1 + (f / fc) ** 4), len(x)).astype(np.float32)


def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1 + (f / hi) ** 4) * (1 - 1 / (1 + (f / max(lo, 1)) ** 4)), len(x)).astype(np.float32)


def noise(sec):
    return rng.standard_normal(int(sec * SR)).astype(np.float32)


def env(n, at, rl):
    e = np.ones(n, np.float32)
    na, nr = int(at * SR), int(rl * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e


def place(bus, x, t, g=1.0):
    i = int(t * SR)
    if i >= len(bus): return
    j = min(len(bus), i + len(x))
    bus[i:j] += x[: j - i] * g


A1 = np.zeros(N, np.float32); A2 = np.zeros(N, np.float32); A3 = np.zeros(N, np.float32); A4 = np.zeros(N, np.float32)

# ---------------------------------------------------------------- A1 narration
rows = list(csv.DictReader(open(ROOT / "00_PROJECT_MANAGEMENT/shot_tracker.csv", encoding="utf-8")))
drift = []
prev_end = 0.0
for r in rows:
    sid = r["shot_id"]
    st = tc(r["start"])
    if 210 <= st < 237:          # prototype window has its own VO
        continue
    p = os.path.join(a.vo, f"{sid}.wav")
    if not os.path.exists(p):
        continue
    x, sr = rd(p)
    x = x / (np.abs(x).max() + 1e-9) * 0.55
    want = st + 0.25
    at = max(want, prev_end + 0.15)
    place(A1, x, at)
    prev_end = at + len(x) / SR
    drift.append((sid, round(want, 2), round(at, 2), round(at - want, 2), round(prev_end - (tc(r["end"])), 2)))
with open(os.path.join(a.out, "vo_drift.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["shot_id", "planned_start_s", "placed_start_s", "delay_s", "ends_after_shot_end_s"]); w.writerows(drift)

# ---------------------------------------------------------------- sound kit
def thunk(g=1.0):
    n = int(0.9 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (70 - 30 * t) * t) * np.exp(-t * 7) + bp(noise(0.9), 200, 1500) * np.exp(-t * 30) * 0.4
    return (x * g).astype(np.float32)


def glass_ring(g=1.0, dur=3.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) * k for f, d, k in ((1830, 2.2, .5), (2710, 3, .35), (4150, 4.5, .2), (620, 1.4, .25)))
    return (x * g).astype(np.float32)


def tick():
    n = int(0.05 * SR); t = np.arange(n) / SR
    return (bp(noise(0.05), 2000, 8000) * np.exp(-t * 120)).astype(np.float32)


def pulse(f0=52):
    n = int(0.35 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (f0 - 20 * t) * t) * np.exp(-t * 11)).astype(np.float32)


def muffled_shot():
    n = int(0.4 * SR); t = np.arange(n) / SR
    return (lp(noise(0.4), 600) * np.exp(-t * 25) * 3 + np.sin(2 * np.pi * 60 * t) * np.exp(-t * 20) * 0.6).astype(np.float32)


def piano(freq, dur=6.0, g=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * freq * k * t) * np.exp(-t * (0.6 + 0.5 * k)) / k ** 1.3 for k in range(1, 7))
    x *= np.minimum(1, t / 0.005)
    return (x * g).astype(np.float32)


def bed(kind, a0, a1, g):
    sec = a1 - a0
    n = int(sec * SR)
    t = np.arange(n) / SR
    if kind == "room":
        x = lp(noise(sec), 380) * 0.5 + np.sin(2 * np.pi * 50 * t) * 0.05
    elif kind == "harbour":
        x = lp(noise(sec), 700) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t)) + bp(noise(sec), 3000, 6000) * 0.04
    elif kind == "wind":
        x = lp(noise(sec), 500) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.13 * t + 1) * np.sin(2 * np.pi * 0.071 * t))
    elif kind == "city":
        x = lp(noise(sec), 250) * 0.8 + bp(noise(sec), 400, 2000) * 0.1
    elif kind == "drone":
        x = sum(np.sin(2 * np.pi * f * t + k) for k, f in enumerate((55, 82.4, 110.2))) * 0.25
        x += lp(noise(sec), 150) * 0.3
    elif kind == "cafe":
        x = lp(noise(sec), 900) * 0.4 + np.sin(2 * np.pi * 120 * t) * 0.03
        keys = np.zeros(n, np.float32)
        for k in np.cumsum(rng.uniform(0.08, 0.35, int(sec * 5))):
            if k < sec: place_local = int(k * SR); keys[place_local:place_local + 2400] += tick()[:len(keys[place_local:place_local + 2400])] * 0.5
        x = x + keys
    else:
        x = np.zeros(n)
    return (x * env(n, min(1.5, sec / 4), min(2.0, sec / 4)) * g).astype(np.float32)


def add_bed(kind, a0, a1, g):
    place(A2, bed(kind, a0, a1, g), a0)


def pad(a0, a1, root=55.0, g=0.05):
    sec = a1 - a0; n = int(sec * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * root * r * t + r) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t + r)) for r in (1, 1.5, 2, 3))
    place(A4, (lp(x.astype(np.float32), 900) * env(n, 4, 4) * g).astype(np.float32), a0)


# ---------------------------------------------------------------- cue sheet (timeline seconds)
# 00 cold open 0–45
place(A3, thunk(1.0), 0.05)
add_bed("drone", 0, 45, 0.10)
place(A3, lp(noise(3), 200) * env(int(3 * SR), 0.05, 2) * 0.5, 5.2)          # truck engine / fire whoomp
add_bed("wind", 6, 18, 0.08)
for k in range(28):                                                              # muffled continuous fire under SH-004/005
    place(A3, muffled_shot(), 18.5 + k * 0.62 + rng.uniform(-0.08, 0.08), 0.18)
place(A3, glass_ring(0.25), 37.2); place(A3, thunk(0.9), 37.3)
# 01 city of money 45–120
add_bed("harbour", 45, 120, 0.10); pad(46, 119, 55.0, 0.035)
# 02 the architect 120–210
add_bed("room", 120, 210, 0.08)
for k in np.arange(140, 210, 1.0):
    place(A3, tick(), k, 0.25)
for k in np.arange(200, 210, 60 / 54):
    place(A3, pulse(), k, 0.22)
# 03a/3D1/03b: prototype window 210–237 inserted later; 237–260 3D 1 rest; 260–315 notebook + road
add_bed("wind", 237, 260, 0.10)
place(A3, glass_ring(0.06, 4), 247)
place(A4, piano(65.4, 8, 0.10), 252)                                              # low cello-like note at "He called it off"
add_bed("room", 260, 290, 0.07)
add_bed("city", 290, 315, 0.07)
# 04a 315–375
add_bed("drone", 315, 330, 0.08)
for k in np.arange(320, 345, 1.0):
    place(A3, tick(), k, 0.3)
add_bed("city", 330, 345, 0.10)
place(A3, tick() * 3, 345.0); place(A3, lp(noise(4), 220) * env(int(4 * SR), 0.05, 3) * 0.5, 346)
add_bed("wind", 346, 368, 0.06)
place(A3, thunk(0.9), 374.6)
# 3D 2 "113" 375–405
add_bed("room", 375, 405, 0.05)
for k, tt in enumerate((376.25, 378.33, 380.42)):
    place(A3, thunk(1.0), tt)
for k in range(16):
    place(A3, muffled_shot(), 383.2 + k * 0.72 + rng.uniform(-0.1, 0.1), 0.22)
place(A3, (bp(noise(0.8), 800, 6000) * np.exp(-np.arange(int(0.8 * SR)) / SR * 6) * 0.6).astype(np.float32), 401.3)
# 04b 405–465
add_bed("room", 405, 465, 0.07); pad(406, 464, 49.0, 0.03)
# 05 the officer 465–545: piano, then 3D 3 (no music in the windshield), memorial
place(A4, piano(220, 9, 0.16), 465.2)
add_bed("city", 487, 495, 0.05)
add_bed("city", 495, 511, 0.07)                                                   # engine hum / radio
place(A2, (bp(noise(16), 900, 3500) * 0.03).astype(np.float32), 495)
for k, tt in enumerate((511.8, 512.05, 512.3)):
    place(A3, muffled_shot(), tt, 0.12)
n_ring = int(9 * SR); tt_ = np.arange(n_ring) / SR
place(A3, (np.sin(2 * np.pi * 6200 * tt_) * np.exp(-tt_ * 0.5) * 0.02).astype(np.float32), 513.5)
add_bed("wind", 516, 545, 0.07)
place(A4, piano(196, 8, 0.12), 520); place(A4, piano(220, 10, 0.12), 526)
# 06 into the woods 545–585
add_bed("wind", 545, 585, 0.10)
for k in np.arange(546, 584, 60 / 58):
    place(A3, pulse(48), k, 0.18)
# 07a the hunt 585–635
add_bed("room", 585, 635, 0.08)
for k in np.arange(600, 635, 1.0):
    place(A3, tick(), k, 0.22)
# 3D 4 635–665
add_bed("city", 635, 642.5, 0.12)
add_bed("cafe", 642, 657.5, 0.10)
place(A3, thunk(1.0), 660.0)
# 07b + 08 verdict 665–735
add_bed("room", 665, 735, 0.07); pad(676, 734, 41.2, 0.035)
# 09 epilogue 735–780
add_bed("drone", 735, 780, 0.06)
place(A3, thunk(0.35), 758.0)
place(A4, piano(220, 10, 0.14), 768.5)

# ---------------------------------------------------------------- mix
L = A1 * 1.0 + A2 * 1.0 + A3 * 0.9 + A4 * 1.0
R = A1 * 1.0 + np.roll(A2, 300) + A3 * 1.0 + np.roll(A4, 200)
mix = np.stack([L, R], 1)
# prototype window
px, psr = rd(a.proto)
if px.ndim == 1:
    px = np.stack([px, px], 1)
i0 = int(210 * SR)
mix[i0:i0 + len(px)] = px[: len(mix) - i0] * 0.9
mix /= max(1e-9, np.abs(mix).max()) / 0.89
out = os.path.join(a.out, "THE_GLASS_roughcut_v001_mix_TEMP.wav")
with wave.open(out, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
late = [d for d in drift if d[3] > 0.5]
print("wrote", out, "| VO lines delayed >0.5 s:", len(late), "| max delay:", max([d[3] for d in drift] or [0]))
