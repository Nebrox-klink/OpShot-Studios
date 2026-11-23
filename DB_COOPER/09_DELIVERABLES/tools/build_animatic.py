"""D.B. Cooper rough animatic: approved stills + slow push/pan + cards, timed to the recorded Brian narration.

Usage: python3 -I build_animatic.py DB_COOPER_ROOT OUT.mp4 [SCENES]
  SCENES: comma list (default 1-10). A scene with no narration file gets a placeholder length and a
  small "narration pending" note. Timing rule (tight, as NOKAS v009): 1.0 s lead-in + narration + 0.5 s tail.
Shots and their relative lengths come from 02_VISUAL/shot_list_v001/make_shot_list.py.
"""
import os
import subprocess
import sys

ROOT = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])
SCENES = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "1,2,3,4,5,6,7,8,9,10").split(",")]
W, H, FPS = 1280, 720, 25
LEAD, TAIL = 1.0, 0.5
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT2 = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
SL = os.path.join(ROOT, "02_VISUAL/shot_list_v001")
REF = os.path.join(ROOT, "02_VISUAL/style_refs_v001/png")
AUD = os.path.join(ROOT, "07_AUDIO/brian_v001")
TMP = os.path.join(os.path.dirname(OUT), "_animatic_tmp")
os.makedirs(TMP, exist_ok=True)

sys.path.insert(0, SL)
import make_shot_list as msl  # noqa: E402

REUSE = {"BG1": os.path.join(REF, "BG1_portland_airport_clean.png"), "BG3": os.path.join(REF, "BG3_727_night.png"),
         "BG4": os.path.join(REF, "BG4_forest_night.png"), "BG5": os.path.join(REF, "BG5_river_sandbar.png"),
         "BG6": os.path.join(REF, "BG6_case_board.png")}
CARDS = {2: ("D.B. COOPER", "THE CASE THAT WON'T CLOSE"), 9: ("CLUE 1", "THE NAME"), 10: ("CLUE 2", "WHAT HE KNEW"),
         11: ("CLUE 3", "THE NIGHT"), 12: ("CLUE 4", "THE MONEY"), 13: ("CLUE 5", "THE RIVER"), 14: ("CLUE 6", "THE TIE")}
PLACEHOLDER = {2: 6.0, 7: 14.0}
KCLIPS = os.path.join(ROOT, "06_AI_VIDEO/kling_pack_v001/clips")
MOTION = {"102": "K01.mp4", "BG4": "K03.mp4", "401": "K04.mp4", "502": "K05.mp4", "BG6": "K06.mp4",
          "1101": "K07.mp4", "BG5": "K08.mp4"}  # still id -> approved motion clip; shots that reuse the still (REUSE:102) get it too


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def src(sid, source):
    if source.startswith("REUSE:"):
        r = source.split(":")[1]
        return REUSE[r] if r in REUSE else os.path.join(SL, "stills", f"SH_{r}.png")
    return os.path.join(SL, "stills", f"SH_{sid}.png")


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")


def overlays(seconds, card, note):
    vf = []
    if card and card[0] == "D.B. COOPER":  # the film title: big title, small subtitle under it, whole shot
        al = f"if(lt(t,0.6),t/0.6,if(lt(t,{seconds - 0.6:.2f}),1,max(0,({seconds:.2f}-t)/0.6)))"
        vf.append(f"drawtext=fontfile={FONT}:text='{esc(card[0])}':fontsize=110:fontcolor=white:x=(w-tw)/2:y=h/2-80"
                  f":alpha='{al}'")
        vf.append(f"drawtext=fontfile={FONT2}:text='{esc(card[1])}':fontsize=30:fontcolor=0xF2B134:x=(w-tw)/2"
                  f":y=h/2+50:alpha='{al}'")
    elif card:
        big, small = card
        vf.append(f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.35:t=fill:enable='lt(t,3.2)'")
        vf.append(f"drawtext=fontfile={FONT2}:text='{esc(big)}':fontsize=34:fontcolor=0xF2B134:x=(w-tw)/2:y=h/2-70"
                  f":alpha='if(lt(t,0.4),t/0.4,if(lt(t,2.8),1,max(0,(3.2-t)/0.4)))':enable='lt(t,3.2)'")
        vf.append(f"drawtext=fontfile={FONT}:text='{esc(small)}':fontsize=72:fontcolor=white:x=(w-tw)/2:y=h/2-20"
                  f":alpha='if(lt(t,0.4),t/0.4,if(lt(t,2.8),1,max(0,(3.2-t)/0.4)))':enable='lt(t,3.2)'")
    if note:
        vf.append(f"drawtext=fontfile={FONT2}:text='{esc(note)}':fontsize=22:fontcolor=white@0.8:x=24:y=h-44"
                  f":box=1:boxcolor=black@0.5:boxborderw=8")
    return vf


def shot_clip(i, path, seconds, move, card=None, note=None, motion=None):
    n = max(1, round(seconds * FPS))
    fade = f"fade=in:st=0:d=0.35,fade=out:st={max(0, seconds - 0.35):.2f}:d=0.35"
    out = os.path.join(TMP, f"v{i:03d}.mp4")
    if motion:  # approved motion clip: fit to frame, slow down (at most 2x) to fill the shot, then hold the last frame
        md = dur(motion)
        k = min(2.0, max(1.0, seconds / md))
        vf = [f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS}",
              f"setpts={k:.4f}*PTS", f"tpad=stop_mode=clone:stop_duration={seconds:.2f}", f"trim=0:{seconds:.3f}",
              "setpts=PTS-STARTPTS", fade] + overlays(seconds, card, note)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", motion, "-an", "-vf", ",".join(vf), "-r", str(FPS),
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], check=True)
        return out
    pre = f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},setsar=1"
    if move == "push":
        zp = f"zoompan=z='1+0.10*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}"
    elif move == "pull":
        zp = f"zoompan=z='1.10-0.10*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}"
    else:  # pan left->right (or right->left)
        a, b = ("0", "1") if move == "panr" else ("1", "0")
        zp = (f"zoompan=z=1.12:x='(iw-iw/zoom)*({a}+({b}-{a})*on/{n})':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}"
              f":fps={FPS}")
    vf = [pre, zp, fade] + overlays(seconds, card, note)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", path, "-t", f"{seconds:.3f}", "-vf", ",".join(vf),
                    "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", out],
                   check=True)
    return out


def main():
    moves = ["push", "panr", "pull", "panl"]
    clips, auds, t, k, log = [], [], 0.0, 0, []
    for sc in SCENES:
        shots = [s for s in msl.S if s[1] == sc]
        a = os.path.join(AUD, f"S{sc:02d}.mp3")
        has_audio = os.path.isfile(a)
        length = (LEAD + dur(a) + TAIL) if has_audio else PLACEHOLDER.get(sc, 10.0)
        wsum = sum(s[2] for s in shots)
        # audio for this scene: lead silence + voice + tail, padded/trimmed to the exact scene length
        aout = os.path.join(TMP, f"a{sc:02d}.wav")
        if has_audio:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af",
                            f"adelay={int(LEAD * 1000)}:all=1,apad,atrim=0:{length:.3f},aformat=sample_rates=44100:"
                            f"channel_layouts=stereo", aout], check=True)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t",
                            f"{length:.3f}", aout], check=True)
        auds.append(aout)
        acc = 0.0
        for j, (sid, _, sec, _, _, source, _) in enumerate(shots):
            # frame-exact split of the scene length by shot weight
            end = length * (sum(s[2] for s in shots[:j + 1]) / wsum)
            seconds = round(end * FPS) / FPS - round(acc * FPS) / FPS
            start = t + acc
            acc = end
            card = CARDS.get(sc) if j == 0 else None
            note = None if has_audio or sc == 2 else f"Scene {sc}: narration not yet recorded"
            key = source.split(":")[1] if source.startswith("REUSE:") else str(sid)
            mo = os.path.join(KCLIPS, MOTION[key]) if key in MOTION and os.path.isfile(os.path.join(KCLIPS, MOTION[key])) else None
            clips.append(shot_clip(k, src(sid, source), seconds, moves[k % 4], card, note, mo))
            log.append(f"{start:7.2f}  scene {sc:2d}  shot {sid}  {seconds:5.2f}s")
            k += 1
        t += length
    with open(os.path.join(TMP, "v.txt"), "w") as fh:
        fh.writelines(f"file '{c}'\n" for c in clips)
    with open(os.path.join(TMP, "a.txt"), "w") as fh:
        fh.writelines(f"file '{a}'\n" for a in auds)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "v.txt"),
                    "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "a.txt"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", OUT], check=True)
    open(OUT[:-4] + "_shots.txt", "w").write("\n".join(log) + "\n")
    print(f"{len(clips)} shots, {t:.1f} s -> {OUT}")


if __name__ == "__main__":
    main()
