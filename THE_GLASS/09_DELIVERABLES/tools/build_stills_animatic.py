"""Stills animatic: lay the approved shot stills on the v008 timeline with slow camera moves, under the full sound mix.

Timeline = same as mix_sound_v008.py (4 s card, per-scene slots from Atlas chunk lengths).
Usage: python -I build_stills_animatic.py THE_GLASS_ROOT
Output: 09_DELIVERABLES/animatic_stills_v008/THE_GLASS_stills_animatic_v008.mp4
"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(sys.argv[1])
FPS, W, H = 24, 1280, 720
CARD, LEAD = 4.0, 1.0
SCRIPT = os.path.join(ROOT, "01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v008.md")
ATLAS = os.path.join(ROOT, "07_AUDIO/atlas_v008")
STILLS = os.path.join(ROOT, "02_VISUAL_DEVELOPMENT/shot_stills_v001/final_jpg")
MIX = os.path.join(ROOT, "07_AUDIO/mix_v008b/THE_GLASS_mix_v008b.flac")
MOTION_DIR = os.path.join(ROOT, "06_AI_VIDEO/motion_v001/clips")
MOTION = {"S02_01": 201, "S03_02": 302, "S05_01": 501, "S07_02": 702, "S08_03": 803, "S09_05": 905, "S10_01": 1001,
          "S12_02": 12022, "S13_04": 1304, "S14_02": 1402, "S14_04": 1404, "S17_04": 1704, "S18_02": 1802,
          "S18_04": 1804, "S19_02": 1902, "S21_01": 2101, "S22_02": 2202, "S24_01": 2401}
USE_MOTION = os.environ.get("USE_MOTION", "1") == "1"
OUT = os.path.join(ROOT, "09_DELIVERABLES/animatic_motion_v008d")
TMP = os.path.join(OUT, "clips")
os.makedirs(TMP, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


# ---- timeline (identical rule to the mix) -----------------------------------------------------------------------
scene_re = re.compile(r"^#### Scene (\d+) · (.+?) \((\d+):(\d+)–(\d+):(\d+)\)")
slots = {}
for line in open(SCRIPT, encoding="utf-8"):
    if m := scene_re.match(line):
        n, _, a, b, c, d = m.groups()
        slots[int(n)] = (int(c) * 60 + int(d)) - (int(a) * 60 + int(b))
length, s17_sil = {}, None
for n in sorted(slots):
    one = os.path.join(ATLAS, f"S{n:02d}.mp3")
    if os.path.isfile(one):
        used = LEAD + dur(one)
    else:
        a = dur(os.path.join(ATLAS, f"S{n:02d}a.mp3"))
        used = LEAD + a + 6.0 + dur(os.path.join(ATLAS, f"S{n:02d}b.mp3"))
        s17_sil = LEAD + a
    # v008b: halve the quiet tail after the narration; scenes whose sound design needs the full slot keep it.
    length[n] = slots[n] if n in (1, 13, 17, 24) else max(used + 0.5, used + (slots[n] - used) * 0.5)


def S(name):
    return ("img", os.path.join(STILLS, name + ".jpg"))


def card(text, big=False, color="black", fg="white"):
    return ("card", text, big, color, fg)


PORTRAIT = card("[ Portrait of Arne Sigve Klungland ]\\nwaiting for the family's answer", False, "0x1a1a1e", "0x9a9aa0")

# Each scene: list of (item, seconds or None=share the rest equally, extras)
PLAN = {
    1: [(card("Stavanger, Norway  ·  Monday 5 April 2004  ·  08:02"), 3.0), (S("S01_03"), 6.0), (S("S01_04"), 5.0),
        (S("S01_02"), 10.0), (S("S01_05"), 3.6), (card(""), 2.9), (card("THE GLASS", True), None)],
    2: [(S("S02_01"), None), (S("S02_03"), None)],
    3: [(S("S03_01"), None), (S("S03_02"), None)],
    4: [(S("S04_01"), None), (S("S04_02"), None)],
    5: [(S("S05_01"), 13.0), (S("S05_02"), None, "Kjell Alrich Schumann, to NRK (2024)")],
    6: [(S("S06_01"), None)],
    7: [(S("S07_01"), 11.0), (S("S07_02"), 12.0), (S("S07_31"), 6.0), (S("S07_32"), 6.0), (S("S07_33"), 6.0), (S("S07_04"), None)],
    8: [(S("S08_01"), None), (S("S08_02"), None), (S("S08_03"), None)],
    9: [(S("S09_01"), None), (S("S09_02"), None), (S("S09_03"), None), (S("S09_04"), None, "Arne Sigve Klungland"), (S("S09_05"), None)],
    10: [(S("S10_01"), None), (S("S10_02"), None), (S("S10_03"), None), (S("S10_04"), None)],
    11: [(S("S11_01"), 15.0, "Erik Håland, to NRK (2024)"), (S("S10_02"), None)],
    12: [(S("S12_01"), 6.5), (S("S12_02"), None)],
    13: [(S("S13_01"), 8.0), (S("S13_02"), 13.5, "COUNT113"), (card(""), 1.5), (S("S13_04"), None)],
    14: [(S("S14_01"), None), (S("S14_02"), None), (card("08:08"), 2.0), (S("S14_04"), None)],
    15: [(S("S15_01"), None), (S("S15_02"), None), (S("S15_03"), None)],
    16: [(S("S16_01"), 14.0), (S("S16_02"), 12.0), (S("S16_03"), None, "as recounted to NRK (2024)")],
    17: [(S("S17_01"), 8.0), (S("S17_02"), "SIL"), (card("", False, "white"), 6.0), (S("S17_04"), None)],
    18: [(S("S18_01"), None), (S("S18_02"), None), (S("S18_03"), None), (S("S18_04"), None)],
    19: [(S("S19_01"), None), (S("S19_02"), None), (S("S19_03"), None, "CAPTION:In memory of Arne Sigve Klungland  ·  1950 – 2004")],
    20: [(S("S20_01"), None), (S("S20_02"), None), (S("S14_02"), None)],
    21: [(S("S21_01"), None), (S("S21_02"), None), (card("Oslo  ·  Madrid  ·  Málaga"), 4.0)],
    22: [(card("5 April 2005"), 3.0), (S("S22_02"), None), (S("S22_03"), None), (S("S22_04"), None)],
    23: [(S("S23_01"), None)],
    24: [(S("S24_01"), None, "FADEOUT")],
}

clips = []
k = 0


def render(item, secs, extra, move):
    global k
    k += 1
    out = os.path.join(TMP, f"c{k:03d}.mp4")
    frames = max(1, round(secs * FPS))
    secs = frames / FPS
    mclip = None
    if item[0] == "img" and USE_MOTION:
        key = os.path.basename(item[1])[:-4]
        cand = os.path.join(MOTION_DIR, f"M_{MOTION.get(key, 0)}.mp4")
        if key in MOTION and os.path.isfile(cand):
            mclip = cand
    if mclip:
        mdur = dur(mclip)
        slow = min(2.0, max(1.0, secs / mdur))
        hold = max(0.0, secs - mdur * slow)
        vf = f"scale={W}:{H},setpts={slow:.4f}*PTS,fps={FPS},tpad=stop_mode=clone:stop_duration={hold + 0.5:.2f},setsar=1"
        inp = ["-i", mclip]
    elif item[0] == "img":
        if move % 3 == 0:
            z, x, y = "1+0.07*on/{d}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
        elif move % 3 == 1:
            z, x, y = "1.08", "(iw-iw/zoom)*on/{d}", "ih/2-(ih/zoom/2)"
        else:
            z, x, y = "1.08-0.06*on/{d}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
        z, x = z.format(d=frames), x.format(d=frames)
        vf = f"scale=2560:1440,zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},setsar=1"
        inp = ["-loop", "1", "-i", item[1]]
    else:
        _, text, big, color, fg = item
        vf = "setsar=1"
        if text:
            fs = 64 if big else 34
            ff = FONTB if big else FONT
            lines = text.split("\\n")
            for i, ln in enumerate(lines):
                yy = f"(h/2)-{(len(lines) - 1) * 26}+{i * 52}-text_h/2"
                vf += f",drawtext=fontfile={ff}:text='{ln.replace(':', chr(92) + ':')}':fontsize={fs}:fontcolor={fg}:x=(w-text_w)/2:y={yy}"
        inp = ["-f", "lavfi", "-i", f"color=c={color}:s={W}x{H}:r={FPS}"]
    if extra and extra.startswith("COUNT"):
        n = int(extra[5:])
        vf += (f",drawtext=fontfile={FONTB}:text='%{{eif\\:min({n}\\,floor(t*{n}/{secs - 1:.2f}))\\:d}}':"
               f"fontsize=46:fontcolor=white@0.85:x=w-text_w-40:y=36")
    elif extra and extra.startswith("CAPTION:"):
        txt = extra[8:]
        vf += (f",drawtext=fontfile={FONTB}:text='{txt}':fontsize=34:fontcolor=white:box=1:boxcolor=black@0.45:"
               f"boxborderw=16:x=(w-text_w)/2:y=h-110:alpha='min(1,t/1.5)'")
    elif extra == "FADEOUT":
        vf += f",fade=t=out:st={max(0, secs - 2.5):.2f}:d=2.5"
    elif extra:
        vf += (f",drawtext=fontfile={FONT}:text='{extra}':fontsize=24:"
               f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=10:x=50:y=h-80")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inp, "-vf", vf, "-frames:v", str(frames), "-r", str(FPS),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], check=True)
    clips.append(out)
    return secs


total = 0.0
total += render(card("A dramatised reconstruction of real events.\\nIllustrations are AI-assisted and the narration voice is synthetic.\\nQuotes are from published interviews."), CARD, None, 0)
move = 0
for n in sorted(PLAN):
    L = length[n]
    items = PLAN[n]
    fixed = 0.0
    for it in items:
        if isinstance(it[1], (int, float)):
            fixed += it[1]
        elif it[1] == "SIL":
            fixed += s17_sil - 8.0
    free = [it for it in items if it[1] is None]
    scale = 1.0
    if free and (L - fixed) / len(free) < 3.0 and n not in (1, 13, 17):
        scale = max(0.5, (L - 3.0 * len(free)) / fixed)
    share = (L - fixed * scale) / len(free) if free else 0
    scene_t = 0.0
    for idx, it in enumerate(items):
        secs = it[1] * scale if isinstance(it[1], (int, float)) else (s17_sil - 8.0 if it[1] == "SIL" else share)
        if idx == len(items) - 1:
            secs = L - scene_t  # absorb rounding
        extra = it[2] if len(it) > 2 else None
        got = render(it[0], secs, extra, move)
        scene_t += got
        move += 1
    total += scene_t
    print(f"scene {n:2d}: {len(items)} items, {scene_t:.2f}/{L:.2f} s", flush=True)

lst = os.path.join(TMP, "list.txt")
with open(lst, "w") as fh:
    fh.writelines(f"file '{c}'\n" for c in clips)
silent = os.path.join(OUT, "video_only.mp4")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
final = os.path.join(OUT, "THE_GLASS_motion_animatic_v008d.mp4")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", silent, "-i", MIX, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
print(f"video {total:.1f} s; WROTE {final}")
