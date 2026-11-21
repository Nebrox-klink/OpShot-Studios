"""Mix Atlas narration + music + sound effects onto the v008 timeline and mux with the animatic slates.

Timeline is rebuilt exactly like build_animatic_audio.py (atlas mode): 4 s disclosure card, then per scene
LEAD 1 s + chunk(s), slot = max(script slot, used + 0.5). Scene 17 has 6 s of forced silence between S17a and S17b.

Usage: python -I mix_sound_v008.py THE_GLASS_ROOT
Writes 09_DELIVERABLES/animatic_atlas_v008/THE_GLASS_animatic_atlas_sound_v008.mp4 and a mix WAV next to it.
"""
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

ROOT = os.path.abspath(sys.argv[1])
SR = 44100
CARD, LEAD = 4.0, 1.0
SCRIPT = os.path.join(ROOT, "01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v008.md")
ATLAS = os.path.join(ROOT, "07_AUDIO/atlas_v008")
SFX = os.path.join(ROOT, "07_AUDIO/sfx_v008")
MUS = os.path.join(ROOT, "07_AUDIO/music_v008")
OUTDIR = os.path.join(ROOT, "07_AUDIO/mix_v008b")


def load(path):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).copy()
    return a


def norm(a, peak=0.9):
    m = float(np.max(np.abs(a))) or 1.0
    return a / m * peak


def db(x):
    return 10 ** (x / 20)


def fade(a, fin, fout):
    n = len(a)
    i, o = int(fin * SR), int(fout * SR)
    if i:
        a[:min(i, n)] *= np.linspace(0, 1, min(i, n))
    if o:
        a[max(0, n - o):] *= np.linspace(1, 0, min(o, n))
    return a


# ---- timeline -------------------------------------------------------------------------------------------
scene_re = re.compile(r"^#### Scene (\d+) · (.+?) \((\d+):(\d+)–(\d+):(\d+)\)")
slots = {}
for line in open(SCRIPT, encoding="utf-8"):
    if m := scene_re.match(line):
        n, _, a, b, c, d = m.groups()
        slots[int(n)] = (int(c) * 60 + int(d)) - (int(a) * 60 + int(b))
starts, lengths, narr_parts = {}, {}, []
t = CARD
for n in sorted(slots):
    one = os.path.join(ATLAS, f"S{n:02d}.mp3")
    if os.path.isfile(one):
        chunks = [(LEAD, load(one))]
        used = LEAD + len(chunks[0][1]) / SR
    else:
        a = load(os.path.join(ATLAS, f"S{n:02d}a.mp3"))
        b = load(os.path.join(ATLAS, f"S{n:02d}b.mp3"))
        chunks = [(LEAD, a), (LEAD + len(a) / SR + 6.0, b)]
        used = LEAD + len(a) / SR + 6.0 + len(b) / SR
    # v008b: halve the quiet tail after the narration; scenes whose sound design needs the full slot keep it.
    length = slots[n] if n in (1, 13, 17, 24) else max(used + 0.5, used + (slots[n] - used) * 0.5)
    starts[n], lengths[n] = t, length
    for off, au in chunks:
        narr_parts.append((t + off, au))
    t += length
TOTAL = t
N = int(TOTAL * SR) + SR
narr = np.zeros(N, np.float32)
for st, au in narr_parts:
    i = int(st * SR)
    narr[i:i + len(au)] += au
narr = norm(narr, 0.89)

# ---- cue sheet: (scene, file, start_in_scene, gain_db, kind, length_or_None, fade_in, fade_out) ------------
# kind: "once" plays the file once; "loop" repeats it for `length` seconds; "music" plays (optionally trimmed).
S17_SILENCE = None  # computed below
CUES = [
    # 1 Fifteen Seconds
    (1, "sfx/R03_city_morning_loop", 0, -24, "loop", 27, 2, 1),
    (1, "sfx/R01_hammer_thunk", 4.0, -4, "once", None, 0, 0),
    (1, "sfx/R02_ram_thud", 9.0, -3, "once", None, 0, 0),
    (1, "sfx/R01_hammer_thunk", 12.5, -6, "once", None, 0, 0),
    (1, "sfx/R04_rifle_bolt_shot", 24.0, -3, "once", None, 0, 0),
    (1, "mus/M3_title_end_notes", 30.5, -6, "music", 8, 0, 2),
    # 2 Counting Room
    (2, "mus/M5_city_dawn_pad", 0, -16, "music", None, 2, 3),
    (2, "sfx/X05_cathedral_bell", 1.5, -16, "once", None, 0, 0),
    (2, "sfx/R03_city_morning_loop", 0, -28, "loop", None, 1, 2),
    # 3 Player
    (3, "sfx/R06_clock_tick_loop", 0, -22, "loop", None, 1, 2),
    (3, "sfx/X07_chess_piece", 16.5, -8, "once", None, 0, 0),
    # 4 Guard
    (4, "sfx/R06_clock_tick_loop", 0, -30, "loop", None, 1, 2),
    # 5 Through the Glass
    (5, "sfx/R09_night_wind_loop", 0, -22, "loop", None, 2, 2),
    (5, "sfx/X10_muffled_trolley", 10, -14, "once", None, 0, 0),
    (5, "mus/M1_robbers_drone", 16, -26, "music", 14, 3, 3),
    # 6 Second of February
    (6, "sfx/R09_night_wind_loop", 0, -20, "loop", None, 1, 3),
    # 7 William
    (7, "sfx/R11_party_behind_door", 0.5, -16, "once", None, 0, 0),
    (7, "sfx/X12_church_organ", 15, -16, "once", None, 1, 2),
    # 8 Rehearsal
    (8, "sfx/R13_gravel_underpass", 1.5, -12, "once", None, 0, 0),
    (8, "mus/M1_robbers_drone", 10, -26, "music", None, 3, 3),
    # 9 Warning
    (9, "mus/M2_klungland_piano", 30, -16, "music", None, 3, 4),
    (9, "sfx/X17_bus_away", 39, -18, "once", 11, 0, 4),
    # 10 03:30
    (10, "sfx/R18_pine_wind_loop", 0, -20, "loop", None, 2, 2),
    (10, "sfx/R19_tape_tear", 9.5, -8, "once", None, 0, 0),
    (10, "mus/M1_robbers_drone", 0, -22, "music", None, 3, 3),
    # 11 Two Rooms
    (11, "sfx/R20_briefing_murmur_loop", 0, -26, "loop", None, 1, 3),
    (11, "mus/M2_klungland_piano", 0, -22, "music", 14, 2, 4),
    (11, "mus/M1_robbers_drone", 10, -24, "music", None, 4, 3),
    # 12 08:00
    (12, "sfx/R22_truck_fire", 6.5, -8, "once", None, 0, 1),
    (12, "sfx/R23_sirens_start", 10, -14, "once", None, 0, 1),
    # 13 113
    (13, "mus/M1_robbers_drone", 0, -22, "music", None, 1, 1),
    (13, "sfx/R24_rifle_bursts", 6.5, -8, "once", None, 0, 0),
    (13, "sfx/R25_glass_impacts", 8.0, -7, "once", None, 0, 0),
    (13, "sfx/R24_rifle_bursts", 12.0, -9, "once", None, 0, 0),
    (13, "sfx/R25_glass_impacts", 13.0, -8, "once", None, 0, 0),
    (13, "sfx/R26_glass_collapse", 21.5, -5, "once", None, 0, 0),
    # 14 Lift
    (14, "sfx/R27_lift", 1, -10, "once", None, 0, 0),
    (14, "sfx/R24_rifle_bursts", 8, -24, "once", None, 0, 0),
    (14, "mus/M1_robbers_drone", 12, -26, "music", None, 3, 3),
    # 15 Blue Notes
    (15, "sfx/X29_ram_gate", 10, -8, "once", None, 0, 0),
    (15, "sfx/R30_watch_tick_loop", 16, -18, "loop", None, 1, 1),
    # 16 Square
    (16, "sfx/R31_square_traffic_loop", 0, -20, "loop", None, 2, 2),
    (16, "sfx/R32_revolver_vs_rifle", 26.5, -8, "once", None, 0, 0),
    # 17 08:17 (silence window forced below)
    (17, "sfx/R34_aftermath_loop", 0, -30, "loop", 12, 2, 2),
    (17, "sfx/R33_engine_reverse", 11.0, -10, "once", None, 0, 0),
    (17, "sfx/R24_rifle_bursts", 13.0, -18, "once", None, 0, 0.5),
    (17, "mus/M2_klungland_piano", "after_silence", -20, "music", 6, 0.5, 3),
    # 18 Smoke
    (18, "sfx/R34_aftermath_loop", 0, -22, "loop", None, 2, 3),
    (18, "sfx/R22_truck_fire", 8, -20, "once", None, 0.5, 1),
    (18, "mus/M1_robbers_drone", 20, -28, "music", None, 3, 3),
    # 19 Six Hundred
    (19, "sfx/X05_cathedral_bell", 0, -12, "once", None, 0, 0),
    (19, "sfx/R37_helicopter", 6, -18, "once", None, 0.5, 1),
    (19, "mus/M2_klungland_piano", 0, -14, "music", None, 2, 4),
    # 20 Handle
    (20, "sfx/X38_camera_shutter", 0.5, -10, "once", None, 0, 0),
    (20, "sfx/X39_handle_click", 12.5, -6, "once", None, 0, 0),
    # 21 Chess Game
    (21, "sfx/R40_cicadas_loop", 0, -20, "loop", 8, 1, 2),
    (21, "sfx/X41_modem_keys", 9, -16, "once", None, 0, 1),
    (21, "mus/M4_hunt_pulse", 0, -16, "music", None, 2, 3),
    # 22 One Year
    (22, "mus/M4_hunt_pulse", 0, -20, "music", 14, 0, 4),
    (22, "sfx/X43_memorial", 17, -16, "once", None, 2, 2),
    # 24 Glass
    (24, "sfx/R45_morning_birds_loop", 0, -24, "loop", None, 2, 3),
    (24, "mus/M3_title_end_notes", 12, -8, "music", None, 0, 2),
]

bed = np.zeros(N, np.float32)      # music + ambience (ducked)
hits = np.zeros(N, np.float32)     # one-shot effects (lightly ducked)
cache = {}
s17_silence_start = starts[17] + LEAD + len(load(os.path.join(ATLAS, "S17a.mp3"))) / SR
s17_silence_end = s17_silence_start + 6.0
missing = []
for scene, name, off, gain, kind, length, fin, fout in CUES:
    folder, base = name.split("/")
    path = os.path.join(SFX if folder == "sfx" else MUS, base + ".mp3")
    if not os.path.isfile(path):
        missing.append(base)
        continue
    if path not in cache:
        cache[path] = norm(load(path))
    src = cache[path]
    if off == "after_silence":
        st = s17_silence_end + 0.3
    else:
        st = starts[scene] + off
    room = (starts[scene] + lengths[scene]) - st if length is None else length
    if kind == "loop":
        reps = int(np.ceil(room * SR / len(src))) + 1
        seg = np.tile(src, reps)[:int(room * SR)].copy()
    else:
        seg = src[:int(room * SR)].copy() if (length or kind == "music") else src.copy()
    seg = fade(seg, fin, fout) * db(gain)
    i = int(st * SR)
    target = hits if kind == "once" and folder == "sfx" else bed
    target[i:i + len(seg)] += seg[:max(0, N - i)]

# Ducking: lower the bed by up to 9 dB (hits by 4 dB) wherever the narrator speaks.
win = int(0.05 * SR)
env = np.sqrt(np.convolve(narr ** 2, np.ones(win) / win, mode="same"))
speech = (env > db(-40)).astype(np.float32)
k = int(0.35 * SR)
speech = np.convolve(speech, np.ones(k) / k, mode="same").clip(0, 1)
bed *= 1 - speech * (1 - db(-9))
hits *= 1 - speech * (1 - db(-4))

# 08:17: total silence over white.
a, b = int(s17_silence_start * SR), int(s17_silence_end * SR)
ramp = int(0.15 * SR)
mask = np.ones(N, np.float32)
mask[a:b] = 0
mask[a - ramp:a] = np.linspace(1, 0, ramp)
bed *= mask
hits *= mask

mix = narr + bed + hits
mix = mix[:int(TOTAL * SR)]
os.makedirs(OUTDIR, exist_ok=True)
raw = os.path.join(OUTDIR, "mix_raw.wav")
sf.write(raw, mix, SR, subtype="FLOAT")
wav = os.path.join(OUTDIR, "THE_GLASS_mix_v008b.wav")
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=14",
                "-ar", str(SR), wav], check=True)
os.remove(raw)
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", wav, "-c:a", "flac", wav[:-4] + ".flac"], check=True)
os.remove(wav)
print(f"total {TOTAL:.1f} s; 08:17 silence {s17_silence_start:.1f}-{s17_silence_end:.1f} s")
print("missing cues:", sorted(set(missing)) or "none")
print("WROTE", wav[:-4] + ".flac")
