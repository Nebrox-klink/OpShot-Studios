"""Provisional audio for prototype v001 (03:30–03:57 · SH-028 → SH-031), 27.0 s, 48 kHz stereo.

* TEMP VO: offline Festival TTS (cmu_us_slt_arctic_hts). It is a TIMING GUIDE ONLY.
  It is not the narrator, and it must be replaced by a recorded human (or licensed) voice.
* SFX are synthesised procedurally with NumPy, so they carry no licensing questions:
  room tone, lamp hum, low pulse, pencil scratch, card slide, stamp, paper tear,
  glass ring and crack, wind, and a distant city.

Usage: python3 build_prototype_audio.py --out <dir>
Requires: festival + festvox-us-slt-hts (apt), ffmpeg, numpy.
"""
import argparse
import os
import subprocess
import wave

import numpy as np

SR = 48000
DUR = 27.0
N = int(SR * DUR)

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

# shot-relative cue sheet (seconds from 03:30:00)
VO = [  # (shot, start, text)
    ("SH-028", 0.7, "Here is the part most people don't know."),
    ("SH-029", 7.5, "The fifth of April was not the first time they came for NOKAS."),
    ("SH-030", 14.3, "Two months earlier, Toska was already inside the courtyard."),
]


def tts(text, path):
    wav_tmp = path + ".raw.wav"
    subprocess.run(["text2wave", "-eval", "(voice_cmu_us_slt_arctic_hts)",
                    "-eval", "(Parameter.set 'Duration_Stretch 1.22)", "-o", wav_tmp],
                   input=text.encode(), check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_tmp, "-ar", str(SR), "-ac", "1",
                    "-af", "atempo=0.84,highpass=f=90,lowpass=f=9000,acompressor=threshold=-18dB:ratio=3", path], check=True)
    os.remove(wav_tmp)
    with wave.open(path) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x


def lp(x, a):  # one-pole low-pass, a in (0,1): higher = darker
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = a * acc + (1 - a) * x[i]
        y[i] = acc
    return y


def lp_fast(x, cutoff):
    # FFT brick-ish low-pass (fast, fine for noise beds)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x)).astype(np.float32)


def bp_fast(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / (1 + (f / hi) ** 4)) * (1 - 1 / (1 + (f / lo) ** 4))
    return np.fft.irfft(X, len(x)).astype(np.float32)


def env(n, a, r):
    e = np.ones(n, np.float32)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def place(bus, x, t, gain=1.0):
    i = int(t * SR)
    j = min(len(bus), i + len(x))
    bus[i:j] += x[: j - i] * gain


t = np.arange(N) / SR
L = np.zeros(N, np.float32)
R = np.zeros(N, np.float32)
vo_bus = np.zeros(N, np.float32)

# ---------------- VO
for shot, start, text in VO:
    x = tts(text, os.path.join(OUT, f"TEMP_VO_{shot}.wav"))
    place(vo_bus, x / (np.abs(x).max() + 1e-9) * 0.55, start)
    print(f"{shot}: VO {len(x) / SR:.2f}s starting {start:.2f}s")

# ---------------- 2D section 0-20 s
two_d = (t < 20.0).astype(np.float32)
fade2d = np.clip((20.2 - t) / 0.6, 0, 1).astype(np.float32)
room = lp_fast(rng.standard_normal(N).astype(np.float32), 400) * 0.010
hum = (np.sin(2 * np.pi * 50 * t) * 0.006 + np.sin(2 * np.pi * 100 * t) * 0.003).astype(np.float32)
# heartbeat-like low pulse (continues from Ch.2), ~54 bpm
pulse = np.zeros(N, np.float32)
for k in np.arange(0.2, 19.5, 60 / 54):
    for off, g in ((0, 1.0), (0.24, 0.6)):
        n = int(0.35 * SR)
        tt = np.arange(n) / SR
        thump = np.sin(2 * np.pi * (52 - 20 * tt) * tt) * np.exp(-tt * 11) * g
        place(pulse, thump.astype(np.float32), k + off, 0.10)
bed2d = (room + hum + pulse) * fade2d

# pencil scratch during circle strokes 1.0-4.0, 4.4-6.6
scratch = np.zeros(N, np.float32)
for a, b in ((1.0, 4.0), (4.4, 6.6)):
    n = int((b - a) * SR)
    nz = bp_fast(rng.standard_normal(n).astype(np.float32), 1800, 7000)
    tt = np.arange(n) / SR
    mod = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 3.1 * tt)) * (0.7 + 0.3 * rng.random(n))
    place(scratch, (nz * mod * env(n, 0.05, 0.15)).astype(np.float32), a, 0.05)
# card slide 7.3
n = int(0.9 * SR)
sw = bp_fast(rng.standard_normal(n).astype(np.float32), 400, 3000) * np.hanning(n).astype(np.float32)
place(scratch, sw, 7.3, 0.10)
# stamp 10.0 (thump + click)
n = int(0.5 * SR)
tt = np.arange(n) / SR
st = (np.sin(2 * np.pi * (95 - 40 * tt) * tt) * np.exp(-tt * 18) + bp_fast(rng.standard_normal(n).astype(np.float32), 800, 5000) * np.exp(-tt * 60) * 0.5)
place(scratch, st.astype(np.float32), 10.0, 0.45)
# paper tear 17.2-18.4
n = int(1.25 * SR)
tt = np.arange(n) / SR
crackle = rng.standard_normal(n).astype(np.float32) * (rng.random(n) < 0.08)
tear = bp_fast(crackle + rng.standard_normal(n).astype(np.float32) * 0.3, 900, 8000) * (0.3 + 0.7 * tt / tt[-1])
place(scratch, (tear * env(n, 0.02, 0.1)).astype(np.float32), 17.2, 0.22)
# glass ring 18.4 + crack tinkle 19.0 + low glass tone
n = int(3.5 * SR)
tt = np.arange(n) / SR
ring = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) * g for f, d, g in ((1830, 2.2, 0.5), (2710, 3.0, 0.35), (4150, 4.5, 0.2), (620, 1.4, 0.25)))
place(scratch, ring.astype(np.float32), 18.4, 0.09)
n = int(1.2 * SR)
tt = np.arange(n) / SR
tink = bp_fast(rng.standard_normal(n).astype(np.float32) * (rng.random(n) < 0.02), 3000, 14000) * np.exp(-tt * 3)
place(scratch, tink.astype(np.float32), 19.0, 0.6)
# whoosh into 3D 19.0-20.2
n = int(1.4 * SR)
tt = np.arange(n) / SR
wh = lp_fast(rng.standard_normal(n).astype(np.float32), 1200) * np.sin(np.pi * tt / tt[-1]) ** 2
place(scratch, wh.astype(np.float32), 19.0, 0.25)

# ---------------- 3D section 20-27 s (SH-031): wind, distant city, lamp buzz, no music
fade3d = np.clip((t - 19.6) / 0.8, 0, 1).astype(np.float32)
wind_src = lp_fast(rng.standard_normal(N).astype(np.float32), 500)
lfo = (0.55 + 0.45 * np.sin(2 * np.pi * 0.13 * t + 1.0) * np.sin(2 * np.pi * 0.071 * t)).astype(np.float32)
wind = wind_src * lfo * 0.06
city = lp_fast(rng.standard_normal(N).astype(np.float32), 120) * 0.05
buzz = ((np.sign(np.sin(2 * np.pi * 100 * t)) * 0.004 + np.sin(2 * np.pi * 200 * t) * 0.002)).astype(np.float32)
buzz = lp_fast(buzz, 2500)
bed3d = (wind + city + buzz) * fade3d

# ---------------- mix to stereo (slight width on beds)
L = bed2d + bed3d + scratch * 0.9 + vo_bus
R = np.roll(bed2d, 240) + np.roll(bed3d, 480) * 0.95 + scratch + vo_bus
mix = np.stack([L, R], 1)
mix /= max(1e-9, np.abs(mix).max()) / 0.85
out = os.path.join(OUT, "prototype_v001_mix_TEMP.wav")
with wave.open(out, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("wrote", out)
