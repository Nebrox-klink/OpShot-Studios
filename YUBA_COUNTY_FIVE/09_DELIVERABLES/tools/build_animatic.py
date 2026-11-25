"""Yuba County Five animatic v001: every still becomes 2-3 cuts (wide / medium / close), every cut moves.

Usage: python3 -I build_animatic.py YUBA_ROOT OUT.mp4 [SCENES]
  env YCF_W/YCF_H (default 1280x720), YCF_CRF.
Timing per scene: 1.0 s lead + narration + 0.5 s tail (D.B. Cooper rule); scene 2 (title) is 6 s; the last scene
gets a 2.5 s tail. Shots, cut counts and motion types come from 02_VISUAL/shot_list_v001/make_shot_list.py.
Motion: KH/KU stills use their approved clip (all cuts of that still are re-framings of one continuous clip);
L stills get a still move + an effect (FX); G stills get a generated graphic. Text exists only as edit overlays.
"""
import math
import os
import random
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])
SCENES = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else list(range(1, 20))
W, H, FPS = int(os.environ.get("YCF_W", 1280)), int(os.environ.get("YCF_H", 720)), 25
K = H / 720
CRF = os.environ.get("YCF_CRF", "21")
LEAD, TAIL = 1.0, 0.5
SL = os.path.join(ROOT, "02_VISUAL/shot_list_v001")
ST = os.path.join(ROOT, "02_VISUAL/style_test_v001/png")
AUD = os.path.join(ROOT, "07_AUDIO/brian_v001")
HCL = os.path.join(ROOT, "06_AI_VIDEO/higgsfield_clips_v001/clips")
KCL = os.path.join(ROOT, "06_AI_VIDEO/kling_pack_v001/clips")
ANTON = os.path.join(ROOT, "../DB_COOPER/09_DELIVERABLES/tools/fonts/Anton-Regular.ttf")
INTER = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
TMP = os.path.join(os.path.dirname(OUT), "_animatic_tmp")
os.makedirs(TMP, exist_ok=True)
sys.path.insert(0, SL)
_cwd = os.getcwd(); os.chdir(SL)  # the shot-list module writes its request files next to itself
import make_shot_list as msl  # noqa: E402
os.chdir(_cwd)

YEL, RED, BLK, WHT = (255, 212, 0), (214, 38, 32), (0, 0, 0), (255, 255, 255)
AUDIO = {1: "S01", 3: "S03", 4: "S04", 5: "S05", 6: "S06", 7: "S07", 8: "S08", 9: "S09", 10: "S10", 11: "S11",
         12: "S12", 13: "S13", 14: "S13b", 15: "S14", 16: "S15", 17: "S16", 18: "S17", 19: "S18"}
REUSE = {"ST1": "ST1_car_in_snow.png", "ST2": "ST2_trailer_spring.png", "ST3": "ST3_case_board.png",
         "ST4": "ST4_jerseys.png", "ST5": "ST5_five_walking.png"}
CARDS = {2: ("THE YUBA COUNTY FIVE", "TRUE STORY · CALIFORNIA, 1978"), 6: ("CLUE 1", "THE WRONG ROAD"),
         7: ("CLUE 2", "THE CAR"), 9: ("CLUE 3", "THE VOICES"), 11: ("CLUE 4", "THE TRAILER"),
         12: ("CLUE 5", "WHAT WAS NEVER USED"), 13: ("CLUE 6", "THE SHOES"), 14: ("CLUE 7", "WHAT THE BODIES SHOWED"),
         16: ("THEORY A", "LOST"), 17: ("THEORY B", "SOMEONE ELSE"), 18: ("THEORY C", "GARY")}
# approved clips: still id -> (file, use-from, use-to seconds)
CLIPS = {101: ("H_101.mp4", 0, 5), 103: ("H_103.mp4", 0, 5), 104: ("H_104.mp4", 0, 5), 303: ("H_303.mp4", 0, 5),
         305: ("H_305.mp4", 0, 5), 603: ("H_603.mp4", 0, 5), 702: ("H_702.mp4", 0, 3.0), 703: ("H_703.mp4", 0, 3.1),
         706: ("H_706.mp4", 0, 5), 801: ("H_801.mp4", 0, 5), 902: ("H_902.mp4", 0, 5), 903: ("H_903.mp4", 0, 5),
         906: ("H_906.mp4", 0, 5), 908: ("H_908.mp4", 0, 5), 1002: ("H_1002.mp4", 0, 5), 1103: ("H_1103.mp4", 0, 5),
         1201: ("H_1201.mp4", 0, 5), 1203: ("H_1203.mp4", 0, 5), 1303: ("H_1303.mp4", 0, 5),
         1306: ("H_1306.mp4", 0, 5), 1354: ("H_1354.mp4", 0, 5), 1502: ("H_1502.mp4", 0, 5),
         1505: ("H_1505.mp4", 0, 5), 1801: ("H_1801.mp4", 0, 5), 1802: ("H_1802.mp4", 0, 5),
         1501: ("H_1501.mp4", 0, 5), 401: ("K_401.mp4", 0, 3), 904: ("K_904.mp4", 0, 3), 905: ("K_905.mp4", 0, 3),
         1101: ("K_1101.mp4", 0, 3), 1504: ("K_1504.mp4", 0, 3)}
REUSE_CLIP = {1601: 904}  # a reuse shot that plays another still's clip
# local effects for L/G stills: list of (kind, params)
FX = {102: [("squall", {})], 105: [("fog", {})], 201: [("lighton", {})], 301: [("glowon", {"x": .30, "y": .55})],
      302: [("lighton", {})], 304: [("glowon", {"x": .64, "y": .17})], 402: [("flash", {})],
      403: [("lightoff", {"depth": .22})], 404: [("flicker", {}), ("lightoff", {"at": .7})], 405: [("tick", {})],
      501: [("snow0", {})], 502: [("shake", {})], 602: [("snow", {})], 604: [("slide", {})], 605: [("snow", {})],
      701: [("squall", {})], 704: [("snow0", {})], 705: [("rings", {})], 901: [("glowon", {"x": .64, "y": .68})],
      907: [("snow", {})], 1001: [("slide", {})], 1003: [("snow", {"heavy": 1})], 1102: [("lighton", {})],
      1104: [("sweep", {})], 1105: [("toSpring", {})], 1202: [("flicker", {})], 1204: [("rings", {})],
      1205: [("fog", {}), ("rings", {})], 1206: [("squall", {})], 1301: [("rings", {})], 1302: [("rings", {})],
      1305: [("shake", {})], 1307: [("fog", {})], 1351: [("sweep", {})], 1352: [("rings", {})],
      1355: [("rings", {})], 1401: [("snow0", {})], 1503: [("snow", {})], 1506: [("rings", {})],
      1602: [("glowflicker", {"x": .20, "y": .45})], 1603: [("rings", {})], 1701: [("lighton", {}), ("flicker", {})],
      1702: [("fog", {})], 1803: [("lightoff", {"at": .55})]}
RINGS = {705: [(.43, .42, .09), (.42, .65, .09), (.60, .56, .07), (.71, .70, .07)],
         1204: [(.39, .48, .22)], 1205: [(.56, .33, .07)], 1301: [(.55, .76, .17)], 1302: [(.47, .72, .12)],
         1352: [(.33, .50, .09), (.51, .67, .05), (.72, .67, .09), (.66, .36, .08)], 1355: [(.50, .72, .20)],
         1506: [(.53, .33, .07)], 1603: [(.72, .67, .09)], 703: [(.41, .47, .13)]}
LABEL = {401: "FRIDAY · 24 FEBRUARY 1978", 403: "BEHR'S MARKET · CHICO", 405: "JUST BEFORE 10 PM",
         302: "THE GATEWAY GATORS", 602: "OVER 4,000 FT", 603: "SEEN THE DAY AFTER THE GAME", 703: "A QUARTER TANK",
         704: "NOT A SCRATCH", 702: "STUCK · BUT NOT BADLY", 801: "SEARCH CALLED OFF", 902: "A HEART ATTACK",
         906: "8 MILES TO THE LODGE", 1101: "4 JUNE 1978", 1105: "AROUND 3 MONTHS", 1201: "NEVER LIT",
         1202: "NEVER WORN", 1203: "ABOUT 3 DOZEN CANS EATEN", 1204: "FOOD FOR A YEAR · NEVER OPENED",
         1205: "VALVE NEVER TURNED", 1301: "GARY'S SHOES", 1306: "3 FOUND · 1 MISSING", 1354: "NOT TED'S",
         1502: "THE DAY BEFORE", 1506: "LOCKED", 1602: "THE LODGE", 1603: "WHOSE WATCH?", 1702: "NEVER FOUND",
         1001: "SIGHTINGS · NONE CONFIRMED", 1303: "11 MILES FROM THE CAR"}
QUOTE = {1401: "“THIS CASE IS BIZARRE AS HELL.”"}
FRAMES = [(1.00, 1.08, .5, .5), (1.30, 1.40, .5, .45), (1.70, 1.80, .5, .5)]  # wide, medium, close: z0, z1, cx, cy


def run(cmd):
    subprocess.run(cmd, check=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def font(path, size):
    return ImageFont.truetype(path, int(size * K))


def still_path(sid, source):
    if source.startswith("REUSE:"):
        r = source.split(":")[1]
        return os.path.join(ST, REUSE[r]) if r in REUSE else os.path.join(SL, "stills", f"SH_{r}.png")
    return os.path.join(SL, "stills", f"SH_{sid}.png")


def enc(out):
    return ["-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", CRF, "-pix_fmt", "yuv420p", "-an", out]


# ---------- generated assets ----------
def snow_layer(path, secs=8, heavy=False):
    if os.path.isfile(path):
        return path
    rng = random.Random(3)
    n = 360 if heavy else 200
    flakes = [(rng.uniform(0, W), rng.uniform(0, H), rng.choice((1, 1, 2, 3, 5)), rng.uniform(.6, 1.4),
               rng.uniform(0, 6.3)) for _ in range(n)]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-"] + enc(path), stdin=subprocess.PIPE)
    for f in range(int(secs * FPS)):
        im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
        for x, y, s, v, ph in flakes:
            sp = (30 + 40 * s) * v * K * (2.2 if heavy else 1)
            yy = (y + sp * f / FPS) % H
            xx = (x + math.sin(ph + f / FPS) * 12 * s * K + (60 * K * f / FPS if heavy else 0)) % W
            r = s * K
            c = int(120 + 25 * s)
            d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=(c, c, c + 10))
        p.stdin.write(im.filter(ImageFilter.GaussianBlur(.6)).tobytes())
    p.stdin.close(); p.wait()
    return path


def ring_png(path, rings, frame=(1, 1, .5, .5)):
    """Rings are given in still coordinates; map them through the cut's framing (mean zoom of the move)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    zm = (frame[0] + frame[1]) / 2
    for px, py, r in rings:
        cx, cy = px * zm - (zm - 1) * frame[2], py * zm - (zm - 1) * frame[3]
        rr = r * H * zm
        box = (cx * W - rr * 1.25, cy * H - rr, cx * W + rr * 1.25, cy * H + rr)
        d.ellipse(box, outline=(0, 0, 0, 200), width=int(11 * K))
        d.ellipse(box, outline=RED + (255,), width=int(6 * K))
    im.save(path)
    return path


def label_png(path, text, quote=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if quote:
        f = font(ANTON, 54)
        tw = d.textlength(text, font=f)
        x, y = (W - tw) / 2, H * .78
        d.text((x + 3 * K, y + 4 * K), text, font=f, fill=(0, 0, 0, 220))
        d.text((x, y), text, font=f, fill=WHT + (255,), stroke_width=int(3 * K), stroke_fill=BLK + (255,))
    else:
        f = font(ANTON, 40)
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        px, py = 16 * K, 8 * K
        x, y = 40 * K, H - 120 * K
        d.rectangle((x + 5 * K, y + 6 * K, x + r - l + 2 * px + 5 * K, y + b - t + 2 * py + 6 * K), fill=(0, 0, 0, 230))
        d.rectangle((x, y, x + r - l + 2 * px, y + b - t + 2 * py), fill=YEL + (255,))
        d.text((x + px - l, y + py - t), text, font=f, fill=BLK + (255,))
    im.save(path)
    return path


def glow_png(path, x, y):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).ellipse((x * W - 160 * K, y * H - 110 * K, x * W + 160 * K, y * H + 110 * K), fill=255)
    im = im.filter(ImageFilter.GaussianBlur(70 * K))
    rgba = Image.new("RGBA", (W, H), (255, 236, 190, 0)); rgba.putalpha(im.point(lambda v: int(v * .85)))
    rgba.save(path)
    return path


def map_video(path, base, secs, pins):
    """Animated route on the painted map (601): Chico -> south toward home (dashed), then the real route bending
    north-east into the mountains, pins and labels. pins=True adds the June discovery pins (scene 13)."""
    if os.path.isfile(path):
        return path
    bg = Image.open(base).convert("RGB")
    s = max(W / bg.width, H / bg.height); bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    P = {"CHICO": (.27, .30), "YUBA CITY": (.30, .80), "OROVILLE": (.40, .50), "CAR": (.60, .38),
         "TRAILER": (.75, .20)}
    home = [P["CHICO"], (.29, .55), P["YUBA CITY"]]
    real = [P["CHICO"], (.34, .40), P["OROVILLE"], (.48, .46), (.55, .40), P["CAR"]]
    fL, fS = font(ANTON, 30), font(ANTON, 44)
    n = int(secs * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-"] + enc(path), stdin=subprocess.PIPE)

    def pts(seq, frac):
        seg = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
        L = [math.dist(a, b) for a, b in seg]; tot = sum(L); want = tot * frac; out = [seq[0]]
        for (a, b), l in zip(seg, L):
            if want >= l:
                out.append(b); want -= l
            else:
                out.append((a[0] + (b[0] - a[0]) * want / l, a[1] + (b[1] - a[1]) * want / l)); break
        return [(x * W, y * H) for x, y in out]

    def pin(d, xy, c=RED):
        x, y = xy[0] * W, xy[1] * H; r = 12 * K
        d.ellipse((x - r + 3, y - r + 4, x + r + 3, y + r + 4), fill=(0, 0, 0))
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)

    def tag(d, xy, text, f=fL):
        x, y = xy[0] * W + 18 * K, xy[1] * H - 18 * K
        d.text((x, y), text, font=f, fill=WHT, stroke_width=int(3 * K), stroke_fill=BLK)
    for i in range(n):
        t = i / FPS
        im = bg.copy(); d = ImageDraw.Draw(im)
        zoom = 1 + 0.06 * t / secs
        if not pins:
            hf = min(1, max(0, (t - .6) / 1.6)); rf = min(1, max(0, (t - 2.6) / 2.4))
            if hf > 0:
                h = pts(home, hf)
                for a, b in zip(h, h[1:]):
                    seg = math.dist(a, b); k = int(seg // (14 * K)) or 1
                    for j in range(0, k, 2):
                        d.line([(a[0] + (b[0] - a[0]) * j / k, a[1] + (b[1] - a[1]) * j / k),
                                (a[0] + (b[0] - a[0]) * (j + 1) / k, a[1] + (b[1] - a[1]) * (j + 1) / k)],
                               fill=WHT, width=int(5 * K))
            if rf > 0:
                r = pts(real, rf)
                d.line(r, fill=BLK, width=int(11 * K), joint="curve"); d.line(r, fill=RED, width=int(6 * K), joint="curve")
            pin(d, P["CHICO"]); tag(d, P["CHICO"], "CHICO")
            pin(d, P["YUBA CITY"], WHT); tag(d, P["YUBA CITY"], "HOME · YUBA CITY")
            if rf >= 1:
                pin(d, P["CAR"]); tag(d, P["CAR"], "THE CAR", fS)
            if t > 5.6:
                tag(d, (.52, .62), "≈ 70 MILES", fS)
        else:
            d.line(pts(real, 1), fill=RED, width=int(6 * K)); pin(d, P["CAR"]); tag(d, P["CAR"], "THE CAR")
            tr = [P["CAR"], (.66, .30), P["TRAILER"]]
            tf = min(1, max(0, (t - .5) / 1.5))
            if tf > 0:
                d.line(pts(tr, tf), fill=YEL, width=int(6 * K))
            if t > 2.0:
                pin(d, P["TRAILER"], YEL); tag(d, P["TRAILER"], "TRAILER · ≈ 20 MI")
            if t > 3.0:
                pin(d, (.67, .30)); tag(d, (.67, .34), "MADRUGA · STERLING · 11 MI")
            if t > 4.2:
                pin(d, (.73, .13)); tag(d, (.36, .11), "HUETT · 2 MI FROM THE TRAILER")
        if zoom != 1:
            zw, zh = int(W / zoom), int(H / zoom)
            im = im.crop(((W - zw) // 2, (H - zh) // 2, (W - zw) // 2 + zw, (H - zh) // 2 + zh)).resize((W, H))
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    return path


def checklist_video(path, base, secs):
    if os.path.isfile(path):
        return path
    bg = Image.open(base).convert("RGB")
    s = max(W / bg.width, H / bg.height); bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = Image.blend(bg, Image.new("RGB", (W, H)), .62)
    lines = [("WOUNDS", "NONE"), ("WEAPON", "NONE"), ("WALLET & CASH", "STILL THERE"), ("CAUSE", "COLD AND HUNGER")]
    fT, f = font(ANTON, 46), font(INTER, 40)
    n = int(secs * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-"] + enc(path), stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS; im = bg.copy(); d = ImageDraw.Draw(im)
        d.text((W * .18, H * .18), "WHAT THE BODIES SHOWED", font=fT, fill=YEL)
        for k, (a, b) in enumerate(lines):
            t0 = .6 + k * 1.1
            if t < t0:
                continue
            txt = f"{a}:  {b}"; c = int(min(len(txt), (t - t0) * 28))
            d.text((W * .18, H * (.34 + k * .12)), txt[:c], font=f, fill=WHT)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    return path


# ---------- cut rendering ----------
def card_filters(card, secs):
    if not card:
        return []
    big, small = card
    fb, fs = os.path.join(os.path.dirname(ANTON), "Anton-Regular.ttf"), INTER
    if big == "THE YUBA COUNTY FIVE":
        al = f"if(lt(t,0.6),t/0.6,if(lt(t,{secs - 0.6:.2f}),1,max(0,({secs:.2f}-t)/0.6)))"
        return [f"drawtext=fontfile={fb}:text='{big}':fontsize={round(96 * K)}:fontcolor=white:borderw={round(4 * K)}"
                f":bordercolor=black:x=(w-tw)/2:y=h/2-{round(80 * K)}:alpha='{al}'",
                f"drawtext=fontfile={fs}:text='{small}':fontsize={round(28 * K)}:fontcolor=0xFFD400:x=(w-tw)/2"
                f":y=h/2+{round(40 * K)}:alpha='{al}'"]
    al = "if(lt(t,0.25),t/0.25,if(lt(t,2.6),1,max(0,(2.9-t)/0.3)))"
    return ["drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill:enable='lt(t,2.9)'",
            f"drawtext=fontfile={fb}:text='{big}':fontsize={round(40 * K)}:fontcolor=0xFFD400:x=(w-tw)/2"
            f":y=h/2-{round(78 * K)}:alpha='{al}':enable='lt(t,2.9)'",
            f"drawtext=fontfile={fb}:text='{small}':fontsize={round(84 * K)}:fontcolor=white:borderw={round(4 * K)}"
            f":bordercolor=black:x=(w-tw)/2:y=h/2-{round(28 * K)}:alpha='{al}':enable='lt(t,2.9)'"]


def render_cut(out, base, is_video, secs, frame, fx, overlays, card, v_offset=0.0, stretch=1.0):
    """base: still png or (master) video. frame = (z0, z1, cx, cy). fx: list of (kind, params).
    overlays: list of (png, t_in, t_out)."""
    z0, z1, cx, cy = frame
    n = max(1, round(secs * FPS))
    inputs, chains = [], []
    if is_video:
        inputs += ["-ss", f"{v_offset:.3f}", "-i", base]
        zm = (z0 + z1) / 2
        chains.append(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS},"
                      f"scale={int(W * zm)}:{int(H * zm)},crop={W}:{H}:{int((W * zm - W) * cx)}:{int((H * zm - H) * cy)},"
                      f"tpad=stop_mode=clone:stop_duration={secs:.2f},trim=0:{secs:.3f},setpts=PTS-STARTPTS[b0]")
    else:
        inputs += ["-loop", "1", "-i", base]
        zexpr = f"{z0}+({z1}-{z0})*on/{n}"
        if any(k == "shake" for k, _ in fx):
            xs, ys = f"+{6 * K:.1f}*sin(on*1.7)", f"+{4 * K:.1f}*cos(on*2.3)"
        else:
            xs = ys = ""
        chains.append(f"[0:v]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},setsar=1,"
                      f"zoompan=z='{zexpr}':x='(iw-iw/zoom)*{cx}{xs}':y='(ih-ih/zoom)*{cy}{ys}':d={n}:s={W}x{H}:fps={FPS},"
                      f"trim=0:{secs:.3f},setpts=PTS-STARTPTS[b0]")
    cur, idx, ni = "b0", 1, 1  # ni = next ffmpeg input index
    for kind, prm in fx:
        nx = f"b{idx}"
        if kind in ("snow", "snow0", "squall"):
            heavy = kind == "squall" or prm.get("heavy")
            lay = snow_layer(os.path.join(TMP, "snow_heavy.mp4" if heavy else "snow.mp4"), heavy=heavy)
            inputs += ["-stream_loop", "-1", "-i", lay]; ii = ni; ni += 1
            op = .55 if kind == "snow0" else .9
            chains.append(f"[{ii}:v]trim=0:{secs:.3f},setpts=PTS-STARTPTS,format=gbrp[s{idx}];"
                          f"[{cur}]format=gbrp[c{idx}];[c{idx}][s{idx}]blend=all_mode=screen:all_opacity={op}[{nx}]")
            if kind == "squall":  # a white gust wave sweeping through
                chains[-1] += (f";[{nx}]eq=brightness='0.18*exp(-pow((t-{secs * .45:.2f})/0.6,2))':eval=frame[{nx}w]")
                nx = f"{nx}w"
        elif kind == "lighton":
            chains.append(f"[{cur}]eq=brightness='-0.35*max(0,1-t/0.5)':eval=frame[{nx}]"); inputs += []
        elif kind == "lightoff":
            at = prm.get("at", .5) * secs
            dp = prm.get("depth", .42)
            chains.append(f"[{cur}]eq=brightness='if(gt(t,{at:.2f}),-{dp}*min(1,(t-{at:.2f})/0.15),0)':eval=frame[{nx}]")
        elif kind == "flicker":
            chains.append(f"[{cur}]eq=brightness='0.10*sin(t*37)*sin(t*11)*lt(t,1.6)':eval=frame[{nx}]")
        elif kind == "flash":
            chains.append(f"[{cur}]eq=brightness='0.35*(lt(mod(t,1.3),0.06))':eval=frame[{nx}]")
        elif kind == "tick":
            chains.append(f"[{cur}]eq=brightness='0.08*(lt(mod(t,1.0),0.05))':eval=frame[{nx}]")
        elif kind == "fog":
            chains.append(f"[{cur}]eq=brightness='0.10*t/{secs:.2f}':contrast='1-0.25*t/{secs:.2f}':eval=frame[{nx}]")
        elif kind == "sweep":
            chains.append(f"[{cur}]eq=brightness='0.16*exp(-pow((t-{secs * .35:.2f})/0.7,2))-0.10':eval=frame[{nx}]")
        elif kind in ("glowon", "glowflicker"):
            g = glow_png(os.path.join(TMP, f"glow_{prm['x']}_{prm['y']}.png"), prm["x"], prm["y"])
            inputs += ["-loop", "1", "-i", g]; ii = ni; ni += 1
            a = "min(1,t/0.25)" if kind == "glowon" else "0.6+0.4*sin(t*9)*sin(t*3)"
            chains.append(f"[{ii}:v]format=rgba,trim=0:{secs:.3f},setpts=PTS-STARTPTS,"
                          f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='alpha(X,Y)*({a.replace('t', 'T')})'[g{idx}];"
                          f"[{cur}][g{idx}]overlay=0:0:shortest=1[{nx}]")
        elif kind == "slide":
            chains.append(f"[{cur}]pad=iw:ih,eq=brightness='-0.2*max(0,1-t/0.4)':eval=frame[{nx}]")
        else:
            continue
        cur, idx = nx, idx + 1
    for png, t0, t1 in overlays:
        inputs += ["-loop", "1", "-i", png]; ii = ni; ni += 1
        chains.append(f"[{ii}:v]format=rgba,trim=0:{secs:.3f},setpts=PTS-STARTPTS,"
                      f"fade=in:st={t0:.2f}:d=0.2:alpha=1,fade=out:st={max(t0 + .3, t1 - .25):.2f}:d=0.25:alpha=1[o{idx}];"
                      f"[{cur}][o{idx}]overlay=0:0:shortest=1[b{idx}]")
        cur, idx = f"b{idx}", idx + 1
    post = card_filters(card, secs)
    chains.append(f"[{cur}]" + (",".join(post) + "," if post else "") + f"trim=0:{secs:.3f},format=yuv420p[vout]")
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(chains), "-map", "[vout]",
                                                    "-t", f"{secs:.3f}"] + enc(out))
    return out


def master_clip(sid, secs):
    """One continuous clip for all cuts of a moving still: trimmed, stretched (≤1.8x) to the still's screen time."""
    f, a, b = CLIPS[sid]
    src = os.path.join(HCL if f.startswith("H_") else KCL, f)
    out = os.path.join(TMP, f"m{sid}.mp4")
    k = min(1.8, max(1.0, secs / (b - a)))
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", src, "-vf",
         f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS},setpts={k:.4f}*PTS,"
         f"tpad=stop_mode=clone:stop_duration={secs:.2f},trim=0:{secs:.3f},setpts=PTS-STARTPTS"] + enc(out))
    return out


def main():
    clips, auds, log, t = [], [], [], 0.0
    for sc in SCENES:
        shots = [s for s in msl.S if s[1] == sc]
        a = os.path.join(AUD, AUDIO[sc] + ".mp3") if sc in AUDIO else None
        tail = 2.5 if sc == 19 else TAIL
        length = LEAD + dur(a) + tail if a else 6.0
        aout = os.path.join(TMP, f"a{sc:02d}.wav")
        if a:
            run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", f"adelay={int(LEAD * 1000)}:all=1,apad,atrim=0:{length:.3f},"
                 "aformat=sample_rates=44100:channel_layouts=stereo", aout])
        else:
            run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{length:.3f}", aout])
        auds.append(aout)
        total_cuts = sum(s[2] for s in shots)
        acc_cuts, acc_t, first = 0, 0.0, True
        for sid, _, cuts, _, motion, big, source in shots:
            s_start = round(length * acc_cuts / total_cuts * FPS) / FPS
            acc_cuts += cuts
            s_end = round(length * acc_cuts / total_cuts * FPS) / FPS
            s_len = s_end - s_start
            path = still_path(sid, source)
            base, is_video = path, False
            csid = REUSE_CLIP.get(sid, sid)
            if motion == "G" and sid in (601, 1304):
                base, is_video = map_video(os.path.join(TMP, f"map{sid}.mp4"), still_path(601, "NEW"), s_len + .1,
                                           sid == 1304), True
            elif motion == "G" and sid == 1353:
                base, is_video = checklist_video(os.path.join(TMP, "check1353.mp4"), path, s_len + .1), True
            elif csid in CLIPS:
                base, is_video = master_clip(csid, s_len), True
            if sid == 1105:  # winter -> spring: render winter cuts, last cut crossfades into the spring still
                pass
            for c in range(cuts):
                c0 = round(s_len * c / cuts * FPS) / FPS
                c1 = round(s_len * (c + 1) / cuts * FPS) / FPS
                secs = c1 - c0
                fr = FRAMES[c % 3] if not (is_video and sid in (601, 1304, 1353)) else FRAMES[0]
                if sid in RINGS and fr != FRAMES[0]:  # punch toward the first circled detail
                    rx, ry, _ = RINGS[sid][0]; fr = (fr[0], fr[1], rx, ry)
                fx = list(FX.get(sid, [])) if not is_video or sid in (601, 1304, 1353) else []
                if is_video and sid not in (601, 1304, 1353):
                    fx = []
                ovs = []
                if sid in RINGS and c == cuts - 1:
                    ovs.append((ring_png(os.path.join(TMP, f"ring{sid}_{c}.png"), RINGS[sid], fr), .3, secs))
                if sid in LABEL and c == min(1, cuts - 1):
                    ovs.append((label_png(os.path.join(TMP, f"lab{sid}.png"), LABEL[sid]), .25, secs))
                if sid in QUOTE:
                    ovs.append((label_png(os.path.join(TMP, f"q{sid}.png"), QUOTE[sid], True), .4, secs))
                rbase = base
                if sid == 1105 and c == cuts - 1:
                    rbase = os.path.join(ST, REUSE["ST2"]); fx = [("lighton", {})]
                card = CARDS.get(sc) if first else None
                out = os.path.join(TMP, f"c{len(clips):03d}.mp4")
                render_cut(out, rbase, is_video and rbase == base, secs, fr, fx, ovs, card, v_offset=c0)
                clips.append(out); first = False
                log.append(f"{t + s_start + c0:7.2f}  scene {sc:2d}  shot {sid}  cut {c + 1}/{cuts}  {secs:5.2f}s  {motion}  {big}")
        t += length
        print(f"scene {sc}: {length:.1f} s, {total_cuts} cuts", flush=True)
    with open(os.path.join(TMP, "v.txt"), "w") as fh:
        fh.writelines(f"file '{c}'\n" for c in clips)
    with open(os.path.join(TMP, "a.txt"), "w") as fh:
        fh.writelines(f"file '{a}'\n" for a in auds)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "v.txt"), "-f", "concat",
         "-safe", "0", "-i", os.path.join(TMP, "a.txt"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "160k", "-shortest", OUT])
    open(OUT[:-4] + "_cuts.txt", "w").write("\n".join(log) + "\n")
    print(f"{len(clips)} cuts, {t:.1f} s -> {OUT}")


if __name__ == "__main__":
    main()
