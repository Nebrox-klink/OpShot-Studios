"""D.B. Cooper sound mix v001: Brian narration + Cooper line + music + sound effects on the animatic timeline.

The timeline is rebuilt exactly like build_animatic.py: per scene LEAD 1.0 s + narration (+0.4 s + dialogue) + TAIL
0.5 s; scene 2 (title) is a 6 s placeholder. Scene starts are checked against the animatic's _shots.txt.

Usage: python3 -I mix_sound_v001.py DB_COOPER_ROOT ANIMATIC.mp4 OUT.mp4
Writes OUT.mp4 (animatic picture + new mix) and 07_AUDIO/mix_v001/DB_COOPER_mix_v001.flac.
"""
import os
import subprocess
import sys

import numpy as np

ROOT, VID, OUT = (os.path.abspath(a) for a in sys.argv[1:4])
SR = 44100
LEAD, TAIL, GAP = 1.0, 0.5, 0.4
AUD = os.path.join(ROOT, "07_AUDIO/brian_v001")
DIALOGUE = {4: os.path.join(ROOT, "07_AUDIO/cooper_v001/C04_miss_note_bomb.mp3")}
SFX = os.path.join(ROOT, "07_AUDIO/sfx_v001")
MUS = os.path.join(ROOT, "07_AUDIO/music_v001")
OUTDIR = os.path.join(ROOT, "07_AUDIO/mix_v001")


def load(path):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def norm(a, peak=0.9):
    m = float(np.max(np.abs(a))) or 1.0
    return a / m * peak


def db(x):
    return 10 ** (x / 20)


def fade(a, fin, fout):
    n = len(a)
    i, o = min(int(fin * SR), n), min(int(fout * SR), n)
    if i:
        a[:i] *= np.linspace(0, 1, i)
    if o:
        a[n - o:] *= np.linspace(1, 0, o)
    return a


# ---- narration timeline --------------------------------------------------------------------------------
starts, lengths, parts, t = {}, {}, [], 0.0
for sc in range(1, 24):
    p = os.path.join(AUD, f"S{sc:02d}.mp3")
    if os.path.isfile(p):
        au = load(p)
        if sc in DIALOGUE:
            au = np.concatenate([au, np.zeros(int(GAP * SR), np.float32), load(DIALOGUE[sc])])
        # same scene length rule as build_animatic.py: ffprobe duration (decoded length for the combined scene)
        L = LEAD + (len(au) / SR if sc in DIALOGUE else dur(p)) + TAIL
        parts.append((t + LEAD, au))
    else:
        L = 6.0  # scene 2: the title card
    starts[sc], lengths[sc] = t, L
    t += L
TOTAL = t
shots = os.path.splitext(VID)[0] + "_shots.txt"
first = {}
for line in open(shots):
    f = line.split()
    first.setdefault(int(f[2]), float(f[0]))
drift = max(abs(first[s] - starts[s]) for s in first)
assert drift < 0.06, f"timeline drift {drift:.3f} s vs the animatic"

N = int(TOTAL * SR) + SR
narr = np.zeros(N, np.float32)
for st, au in parts:
    i = int(st * SR)
    narr[i:i + len(au)] += au
narr = norm(narr, 0.89)

# ---- cue sheet: (scene, file, offset_in_scene, gain_db, kind, length_or_None, fade_in, fade_out) ---------------
# kind "loop" repeats for length (None = to the end of the scene), "once" plays once, "music" plays trimmed to length.
CUES = [
    # 1 cold open: cabin, the jolt, the open stairs in the rain
    (1, "sfx/D01_cabin_hum_loop", 0, -24, "loop", 12, 2, 3),
    (1, "mus/M2_hijack_tension", 0, -22, "music", 27, 3, 3),
    (1, "sfx/D03_airframe_jolt", 9.6, -4, "once", None, 0, 0),
    (1, "sfx/D02_open_door_wind_rain_loop", 10.5, -18, "loop", None, 2, 2),
    # 2 title
    (2, "mus/M1_title_theme", -0.5, -6, "music", 13, 0.3, 4),
    # 3 Portland
    (3, "sfx/D04_terminal_ambience_loop", 0, -22, "loop", None, 2, 2),
    (3, "sfx/D10_jet_flyover", 11, -20, "once", None, 0.5, 1),
    # 4 the note
    (4, "sfx/D01_cabin_hum_loop", 0, -26, "loop", None, 1, 1),
    (4, "sfx/D05_ice_glass", 1.9, -12, "once", None, 0, 0),
    (4, "sfx/D06_lighter", 3.4, -12, "once", None, 0, 0),
    (4, "sfx/D07_paper_note", 6.4, -10, "once", None, 0, 0),
    # 5-7 the hijacking
    (5, "mus/M2_hijack_tension", 0, -20, "music", 83.8, 3, 4),
    (5, "sfx/D01_cabin_hum_loop", 0, -26, "loop", None, 0, 1),
    (5, "sfx/D08_briefcase_latches", 0.6, -6, "once", None, 0, 0),
    (5, "sfx/D10_jet_flyover", 7.5, -18, "once", None, 0.5, 1),
    (6, "sfx/D01_cabin_hum_loop", 0, -26, "loop", None, 1, 1),
    (7, "sfx/D01_cabin_hum_loop", 0, -26, "loop", 11, 1, 2),
    (7, "sfx/D09_cabin_chime", 11.3, -10, "once", None, 0, 0),
    (7, "sfx/D02_open_door_wind_rain_loop", 11.0, -18, "loop", 8, 1.5, 1.5),
    (7, "sfx/D03_airframe_jolt", 17.4, -3, "once", None, 0, 0),
    (7, "sfx/D01_cabin_hum_loop", 19.5, -32, "loop", None, 2, 2),
    # 8-14 the case board and the clues
    (8, "mus/M3_investigation", 0, -20, "music", 90, 3, 5),
    (8, "sfx/D13_office_night_loop", 0, -26, "loop", None, 2, 1),
    (8, "sfx/D14_typewriter", 2.0, -16, "once", None, 0, 0.5),
    (9, "sfx/D15_pin_cork", 0.3, -8, "once", None, 0, 0),
    (9, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 1),
    (10, "sfx/D15_pin_cork", 0.3, -8, "once", None, 0, 0),
    (10, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 1),
    (11, "sfx/D15_pin_cork", 0.3, -8, "once", None, 0, 0),
    (11, "sfx/D11_forest_storm_loop", 0.5, -18, "loop", None, 2, 3),
    (12, "sfx/D15_pin_cork", 0.3, -8, "once", None, 0, 0),
    (12, "mus/M3_investigation", 0, -21, "music", 90, 3, 5),
    (12, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 1),
    (13, "sfx/D15_pin_cork", 0.3, -8, "once", None, 0, 0),
    (13, "sfx/D12_river_loop", 0.5, -20, "loop", None, 2, 2),
    (13, "sfx/D16_sand_digging", 4.0, -14, "once", None, 0.2, 0.5),
    (14, "sfx/D15_pin_cork", 0.3, -8, "once", None, 0, 0),
    (14, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 2),
    # 15-20 the suspects
    (15, "mus/M4_suspects", 0, -20, "music", 75, 3, 5),
    (15, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 0),
    (16, "sfx/D15_pin_cork", 0.3, -10, "once", None, 0, 0),
    (16, "sfx/D13_office_night_loop", 0, -30, "loop", 11.5, 0, 1),
    (16, "sfx/D10_jet_flyover", 12.5, -20, "once", None, 0.5, 1),
    (17, "sfx/D15_pin_cork", 0.3, -10, "once", None, 0, 0),
    (17, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 1),
    (18, "sfx/D15_pin_cork", 0.3, -10, "once", None, 0, 0),
    (19, "sfx/D15_pin_cork", 0.3, -10, "once", None, 0, 0),
    (19, "mus/M4_suspects", 0, -21, "music", 40, 3, 4),
    (19, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 1),
    (20, "sfx/D15_pin_cork", 0.3, -10, "once", None, 0, 0),
    (20, "sfx/D13_office_night_loop", 0, -30, "loop", None, 1, 2),
    # 21-23 endings, closed, last question
    (21, "mus/M5_closing", 0, -18, "music", None, 3, 0),
    (21, "sfx/D11_forest_storm_loop", 0, -26, "loop", 11.2, 1.5, 2),
    (21, "sfx/D12_river_loop", 22.3, -24, "loop", None, 2, 2),
    (22, "mus/M5_closing", "cont", -18, "music", None, 0, 0),
    (22, "sfx/D13_office_night_loop", 0, -28, "loop", 10.2, 2, 0.3),
    (22, "sfx/D17_lamp_switch_off", 10.2, -10, "once", None, 0, 0),
    (22, "sfx/D14_typewriter", 14.5, -20, "once", None, 0, 0.5),
    (23, "mus/M5_closing", "cont", -18, "music", None, 0, 4),
    (23, "sfx/D02_open_door_wind_rain_loop", 0, -30, "loop", 6.8, 2, 2),
    (23, "sfx/D01_cabin_hum_loop", 6.0, -32, "loop", None, 2, 4),
]

bed = np.zeros(N, np.float32)
hits = np.zeros(N, np.float32)
cache, missing = {}, []
m5_start = starts[21]
for scene, name, off, gain, kind, length, fin, fout in CUES:
    folder, base = name.split("/")
    path = os.path.join(SFX if folder == "sfx" else MUS, base + ".mp3")
    if not os.path.isfile(path):
        missing.append(base)
        continue
    if path not in cache:
        cache[path] = norm(load(path))
    src = cache[path]
    scene_end = starts[scene] + lengths[scene]
    if off == "cont":  # the closing music runs on through scenes 21-23: take the matching slice
        st = starts[scene]
        src = src[int((st - m5_start) * SR):]
    else:
        st = starts[scene] + off
    room = scene_end - st if length is None else length
    if kind == "loop":
        reps = int(np.ceil(room * SR / len(src))) + 1
        seg = np.tile(src, reps)[:int(room * SR)].copy()
    elif kind == "music":
        seg = src[:int(room * SR)].copy()
    else:
        seg = src.copy()
    seg = fade(seg, fin, fout) * db(gain)
    i = int(st * SR)
    target = hits if kind == "once" else bed
    target[i:i + len(seg)] += seg[:max(0, N - i)]

# Ducking: bed down up to 9 dB, hits 4 dB, wherever the narrator speaks.
win = int(0.05 * SR)
env = np.sqrt(np.convolve(narr ** 2, np.ones(win) / win, mode="same"))
speech = (env > db(-40)).astype(np.float32)
k = int(0.35 * SR)
speech = np.convolve(speech, np.ones(k) / k, mode="same").clip(0, 1)
bed *= 1 - speech * (1 - db(-9))
hits *= 1 - speech * (1 - db(-4))

mix = (narr + bed + hits)[:int(TOTAL * SR)]
os.makedirs(OUTDIR, exist_ok=True)
raw = os.path.join(OUTDIR, "_raw.f32")
mix.astype(np.float32).tofile(raw)
flac = os.path.join(OUTDIR, "DB_COOPER_mix_v001.flac")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw, "-af",
                "loudnorm=I=-16:TP=-1.5:LRA=14", "-ar", str(SR), "-ac", "2", flac], check=True)
os.remove(raw)
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", VID, "-i", flac, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-shortest", OUT], check=True)
print(f"total {TOTAL:.2f} s, drift {drift * 1000:.0f} ms, missing: {missing or 'none'}")
print("WROTE", flac, OUT)
