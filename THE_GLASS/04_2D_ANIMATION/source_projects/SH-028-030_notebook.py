"""SH-028 → SH-030 · Ch. 3a "The First Time" · 2D notebook sequence (20 s @ 24 fps)
plus SIGNATURE IN 1, a 2D tear → glass crack → shards transition into the first 3D frame.

Layered 2D cutout animation rendered with Pillow + NumPy. Every layer is generated
here, so the script has no external art dependencies:
  L0 desk (charcoal navy + lamp pool)    L1 notebook page (ivory, grid, binding)
  L2 handwriting (Caveat)                L3 pen (cutout, follows stroke tip)
  L4 calendar card "FEB 2004"            L5 stamp "CALLED OFF" (oxide red)
  L6 tear / crack overlay                L7 shards (Voronoi) over 3D frame 1
Camera: a 2.5D push-in on the notebook, then a push to the WINDOW rectangle.

Usage:
  python3 SH-028-030_notebook.py --out <frames_dir> --threed <SH-031 frame 1 png> [--res 1280x720]
"""
import argparse
import math
import os
import pathlib
import random

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
TYPO = ROOT / "03_2D_ASSETS/typography"
FONT_HAND = str(TYPO / "caveat-latin-600-normal.woff")
FONT_HAND_LIGHT = str(TYPO / "caveat-latin-400-normal.woff")
FONT_STAMP = str(TYPO / "special-elite-latin-400-normal.woff")
FONT_CARD = str(TYPO / "oswald-latin-600-normal.woff")

# Palette (style guide)
NAVY = (23, 33, 43)        # #17212B
SLATE = (85, 103, 116)     # #556774
AMBER = (199, 139, 85)     # #C78B55
IVORY = (233, 230, 222)    # #E9E6DE
OXIDE = (169, 81, 73)      # #A95149
INK = (38, 44, 52)
GLASS_GREEN = (120, 160, 140)

FPS = 24
DUR = 20.0
N = int(DUR * FPS)  # 480

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--threed", required=True, help="first frame of SH-031 render (match frame)")
ap.add_argument("--res", default="1280x720")
args, _unknown = ap.parse_known_args()
W, H = (int(v) for v in args.res.split("x"))
os.makedirs(args.out, exist_ok=True)
rng = random.Random(4)  # deterministic


def ease(t):  # smoothstep-ish ease in/out
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def seg(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


# ------------------------------------------------------------ world canvas
# The world canvas is 2x the output. The camera crops and resizes from it.
WW, WH = W * 2, H * 2
S = WW / 2560.0  # scale factor if res differs from 1280x720


def noise_img(w, h, scale, seed, lo=0, hi=255):
    r = np.random.default_rng(seed)
    small = r.random((max(2, h // scale), max(2, w // scale)))
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    a = np.asarray(im).astype(np.float32) / 255
    return lo + a * (hi - lo)


def build_desk():
    base = np.zeros((WH, WW, 3), np.float32)
    base[:] = np.array(NAVY, np.float32) * 0.62
    grain = noise_img(WW, WH, 3, 1, -4, 4)[..., None] + noise_img(WW, WH, 160, 2, -4, 4)[..., None]
    base += grain
    # long wood-ish streaks
    streak = noise_img(WW, WH // 40, 1, 3, -3, 3)
    streak = np.asarray(Image.fromarray(((streak + 5) * 25).astype(np.uint8)).resize((WW, WH), Image.BICUBIC)).astype(np.float32) / 25 - 5
    base += streak[..., None]
    # warm lamp pool, top-left
    yy, xx = np.mgrid[0:WH, 0:WW].astype(np.float32)
    cx, cy = WW * 0.38, WH * 0.30
    d = np.sqrt(((xx - cx) / (WW * 0.55)) ** 2 + ((yy - cy) / (WH * 0.65)) ** 2)
    pool = np.clip(1 - d, 0, 1) ** 1.8
    base += pool[..., None] * np.array([70, 46, 22], np.float32)
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


# notebook page geometry in world space
PW, PH = int(1700 * S), int(1180 * S)
PX, PY = int((WW - PW) / 2 + 40 * S), int((WH - PH) / 2 + 30 * S)
WINDOW_BOX = (int(980 * S), int(470 * S), int(1380 * S), int(720 * S))  # in page coords


def page_base():
    pg = np.zeros((PH, PW, 3), np.float32)
    pg[:] = IVORY
    pg += noise_img(PW, PH, 2, 5, -7, 7)[..., None]
    pg += noise_img(PW, PH, 220, 6, -6, 4)[..., None]
    img = Image.fromarray(np.clip(pg, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    # faint grid
    step = int(44 * S)
    for x in range(int(130 * S), PW, step):
        d.line([(x, 0), (x, PH)], fill=(214, 214, 210), width=1)
    for y in range(int(60 * S), PH, step):
        d.line([(0, y), (PW, y)], fill=(214, 214, 210), width=1)
    # margin line + binding holes
    d.line([(int(110 * S), 0), (int(110 * S), PH)], fill=(196, 150, 140), width=max(1, int(2 * S)))
    for y in range(int(70 * S), PH, int(90 * S)):
        r = int(13 * S)
        d.ellipse([int(45 * S) - r, y - r, int(45 * S) + r, y + r], fill=tuple(int(c * 0.55) for c in NAVY))
    # handwriting (static parts)
    fh = ImageFont.truetype(FONT_HAND, int(78 * S))
    fs = ImageFont.truetype(FONT_HAND_LIGHT, int(52 * S))
    d.text((int(180 * S), int(80 * S)), "NOKAS — Stavanger", font=fh, fill=INK)
    d.text((int(185 * S), int(175 * S)), "courtyard  /  counting room", font=fs, fill=(70, 78, 88))
    # building elevation sketch (wobbly lines)
    def wob(p0, p1, width=3, col=INK):
        pts = []
        for i in range(21):
            t = i / 20
            x = p0[0] + (p1[0] - p0[0]) * t + rng.uniform(-1.6, 1.6) * S
            y = p0[1] + (p1[1] - p0[1]) * t + rng.uniform(-1.6, 1.6) * S
            pts.append((x, y))
        d.line(pts, fill=col, width=max(1, int(width * S)), joint="curve")
    bx0, by0, bx1, by1 = int(700 * S), int(300 * S), int(1600 * S), int(1080 * S)
    wob((bx0, by1), (bx0, by0)); wob((bx0, by0), (bx1, by0)); wob((bx1, by0), (bx1, by1)); wob((bx0, by1), (bx1, by1))
    wob((bx0, int(400 * S)), (bx1, int(400 * S)), 2)
    # WINDOW rectangle + label
    vx0, vy0, vx1, vy1 = WINDOW_BOX
    wob((vx0, vy0), (vx1, vy0), 4); wob((vx1, vy0), (vx1, vy1), 4); wob((vx1, vy1), (vx0, vy1), 4); wob((vx0, vy1), (vx0, vy0), 4)
    wob(((vx0 + vx1) // 2, vy0), ((vx0 + vx1) // 2, vy1), 2)
    fl = ImageFont.truetype(FONT_HAND, int(70 * S))
    d.text(((vx0 + vx1) // 2, vy1 + int(20 * S)), "WINDOW", font=fl, fill=INK, anchor="ma")
    # door + arrows (abstract, no operational detail)
    wob((int(820 * S), by1), (int(820 * S), int(860 * S)), 2); wob((int(820 * S), int(860 * S)), (int(930 * S), int(860 * S)), 2); wob((int(930 * S), int(860 * S)), (int(930 * S), by1), 2)
    d.text((int(180 * S), int(420 * S)), "?", font=fh, fill=OXIDE)
    d.text((int(180 * S), int(980 * S)), "time:  —", font=fs, fill=(70, 78, 88))
    return img


def circle_path(cx, cy, rx, ry, turns=1.15, n=220, seed=0):
    r = random.Random(seed)
    pts = []
    a0 = r.uniform(-2.5, -1.5)
    for i in range(n):
        t = i / (n - 1)
        a = a0 + t * turns * 2 * math.pi
        k = 1 + 0.05 * math.sin(t * 7) + r.uniform(-0.004, 0.004)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


# ------------------------------------------------------------ assets
desk = build_desk()
page = page_base()
shadow = Image.new("L", (PW + 120, PH + 120), 0)
ImageDraw.Draw(shadow).rectangle([60, 60, PW + 60, PH + 60], fill=170)
shadow = shadow.filter(ImageFilter.GaussianBlur(int(28 * S)))

vcx, vcy = (WINDOW_BOX[0] + WINDOW_BOX[2]) / 2, (WINDOW_BOX[1] + WINDOW_BOX[3]) / 2 + 30 * S
circ1 = circle_path(vcx, vcy, 290 * S, 205 * S, 1.1, seed=1)
circ2 = circle_path(vcx + 6 * S, vcy - 4 * S, 310 * S, 222 * S, 1.05, seed=2)

# calendar card
CW, CH = int(380 * S), int(300 * S)
card = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle([0, 0, CW - 1, CH - 1], radius=int(10 * S), fill=(*IVORY, 255), outline=(150, 145, 135, 255), width=max(1, int(2 * S)))
cd.rectangle([0, 0, CW, int(70 * S)], fill=(*NAVY, 255))
fcard = ImageFont.truetype(FONT_CARD, int(54 * S))
fbig = ImageFont.truetype(FONT_CARD, int(118 * S))
cd.text((CW / 2, int(36 * S)), "2004", font=fcard, fill=IVORY, anchor="mm")
cd.text((CW / 2, int(185 * S)), "FEB", font=fbig, fill=NAVY, anchor="mm")
card_shadow = Image.new("L", (CW + 80, CH + 80), 0)
ImageDraw.Draw(card_shadow).rectangle([40, 40, CW + 40, CH + 40], fill=150)
card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(int(16 * S)))

# stamp (with ink texture)
fst = ImageFont.truetype(FONT_STAMP, int(64 * S))
tw = int(fst.getlength("CALLED OFF")) + int(70 * S)
th = int(112 * S)
stamp = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([6, 6, tw - 6, th - 6], radius=int(14 * S), outline=(*OXIDE, 255), width=max(2, int(9 * S)))
sd.text((tw / 2, th / 2 + int(4 * S)), "CALLED OFF", font=fst, fill=(*OXIDE, 255), anchor="mm")
ink = (noise_img(tw, th, 2, 9, 0, 1) > 0.18).astype(np.uint8) * 255
a = np.asarray(stamp.split()[3]).astype(np.uint16) * ink // 255
stamp.putalpha(Image.fromarray(a.astype(np.uint8)))
stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)

# pen cutout (top-down, simple)
PL = int(560 * S)
pen = Image.new("RGBA", (PL, int(60 * S)), (0, 0, 0, 0))
pd = ImageDraw.Draw(pen)
pd.rounded_rectangle([int(70 * S), int(14 * S), PL - 4, int(46 * S)], radius=int(14 * S), fill=(22, 26, 32, 255))
pd.rectangle([int(70 * S), int(14 * S), int(150 * S), int(46 * S)], fill=(150, 120, 80, 255))  # brass ring
pd.polygon([(0, int(30 * S)), (int(72 * S), int(16 * S)), (int(72 * S), int(44 * S))], fill=(36, 40, 46, 255))
pd.line([(int(160 * S), int(22 * S)), (PL - 30, int(22 * S))], fill=(70, 80, 92, 255), width=max(1, int(3 * S)))
PEN_ANGLE = 32  # degrees, lying from bottom-right
pen_rot = pen.rotate(PEN_ANGLE, expand=True, resample=Image.BICUBIC)
pen_tip_offset = None
# tip position inside rotated image: rotate the local tip (0, 30S) around the centre
cxp, cyp = pen.size[0] / 2, pen.size[1] / 2
ang = math.radians(PEN_ANGLE)
tx, ty = 0 - cxp, 30 * S - cyp
rx, ry = tx * math.cos(ang) + ty * math.sin(ang), -tx * math.sin(ang) + ty * math.cos(ang)
pen_tip_offset = (pen_rot.size[0] / 2 + rx, pen_rot.size[1] / 2 + ry)
pen_shadow = Image.new("L", pen_rot.size, 0)
pen_shadow.paste(pen_rot.split()[3], (0, 0))
pen_shadow = pen_shadow.filter(ImageFilter.GaussianBlur(int(10 * S)))

# tear path across the WINDOW rectangle (page coords) and crack network (screen coords, made later)
tear = []
x = WINDOW_BOX[0] - 120 * S
y = vcy - 60 * S
while x < WINDOW_BOX[2] + 140 * S:
    tear.append((x, y))
    x += rng.uniform(14, 30) * S
    y += rng.uniform(-16, 16) * S

# 3D match frame
three = Image.open(args.threed).convert("RGB").resize((W, H), Image.LANCZOS)


def crack_network(seed, cx, cy):
    r = random.Random(seed)
    lines = []
    def branch(x, y, a, length, depth):
        pts = [(x, y)]
        for _ in range(int(length / 18)):
            a += r.uniform(-0.35, 0.35)
            x += math.cos(a) * 18 * W / 1280
            y += math.sin(a) * 18 * W / 1280
            pts.append((x, y))
            if depth < 3 and r.random() < 0.08:
                branch(x, y, a + r.choice([-1, 1]) * r.uniform(0.5, 1.1), length * 0.5, depth + 1)
        lines.append((depth, pts))
    for k in range(9):
        branch(cx, cy, k / 9 * 2 * math.pi + r.uniform(-0.2, 0.2), r.uniform(380, 760), 0)
    return lines


def voronoi_labels(n, seed):
    r = np.random.default_rng(seed)
    sites = np.column_stack([r.uniform(0, W, n), r.uniform(0, H, n)])
    # bias some sites near the centre for small central shards
    sites[: n // 3] = np.column_stack([r.normal(W / 2, W / 9, n // 3), r.normal(H / 2, H / 9, n // 3)])
    yy, xx = np.mgrid[0:H:2, 0:W:2]
    d = (xx[..., None] - sites[:, 0]) ** 2 + (yy[..., None] - sites[:, 1]) ** 2
    lab = np.argmin(d, axis=2).astype(np.int16)
    lab = np.asarray(Image.fromarray(lab.astype(np.uint8)).resize((W, H), Image.NEAREST))
    return lab, sites


def camera_for(t):
    """returns (cx, cy, zoom) in world coords. zoom=1 shows whole world scaled to out res"""
    # phase 1 (0-14s): gentle push on the page, slight drift
    p1 = ease(seg(t, 0, 14))
    z = 1.02 + 0.16 * p1
    cx = WW / 2 + (60 * S) * p1
    cy = WH / 2 + (10 * S) * p1
    # phase 2 (14-19s): push to WINDOW
    p2 = ease(seg(t, 14.0, 18.6))
    vx = PX + vcx
    vy = PY + vcy
    z = z + (1.85 - z) * p2
    cx = cx + (vx - cx) * p2
    cy = cy + (vy - cy) * p2
    # handheld micro drift
    cx += math.sin(t * 0.7) * 3 * S
    cy += math.cos(t * 0.53) * 2 * S
    return cx, cy, z


def render_world(t):
    world = desk.copy()
    pg = page.copy()
    d = ImageDraw.Draw(pg)
    tip = None
    # SH-028: circles drawn 1.0-4.0 and 4.4-6.6
    for (a, b, pts, wdt) in ((1.0, 4.0, circ1, 5), (4.4, 6.6, circ2, 4)):
        p = seg(t, a, b)
        if p > 0:
            k = max(2, int(len(pts) * ease(p)))
            d.line(pts[:k], fill=INK, width=max(1, int(wdt * S)), joint="curve")
            if p < 1:
                tip = pts[k - 1]
    # tear (SH-030): 17.2-18.4
    pt = seg(t, 17.2, 18.4)
    if pt > 0:
        k = max(2, int(len(tear) * pt))
        # paper tear: dark gap with light fibre edge
        d.line(tear[:k], fill=(20, 24, 30), width=max(2, int(9 * S)), joint="curve")
        d.line([(x, y - 6 * S) for x, y in tear[:k]], fill=(250, 248, 240), width=max(1, int(3 * S)))
        if pt < 1:
            tip = tear[k - 1]
    # card + stamp (SH-029)
    pc = ease_out(seg(t, 7.3, 8.4))
    if pc > 0:
        cxw = int(320 * S + (1 - pc) * 1500 * S)
        cyw = int(560 * S)
        pg.paste(Image.new("RGB", card_shadow.size, (0, 0, 0)), (cxw - 30, cyw - 20), card_shadow.point(lambda v: v // 2))
        rot = card.rotate(3 - 5 * (1 - pc), expand=True, resample=Image.BICUBIC)
        pg.paste(rot, (cxw, cyw), rot)
        ps = seg(t, 9.9, 10.15)
        if ps > 0:
            sc = 1.7 - 0.7 * ease_out(ps)
            st = stamp.resize((int(stamp.width * sc), int(stamp.height * sc)), Image.BICUBIC)
            shake = int((1 - seg(t, 10.15, 10.45)) * 5 * S * math.sin(t * 90)) if t > 10.15 else 0
            sx = cxw + CW // 2 - st.width // 2 + int(40 * S) + shake
            sy = cyw + CH - int(40 * S)
            alpha = st.split()[3].point(lambda v: int(v * min(1, ps * 1.5)))
            pg.paste(st, (sx, sy), alpha)
    # page onto desk with shadow and slight rotation
    world.paste(Image.new("RGB", shadow.size, (5, 7, 10)), (PX - 40, PY - 30), shadow)
    world.paste(pg, (PX, PY))
    # pen (follows tip, otherwise rests bottom-right)
    rest = (PX + PW - 180 * S, PY + PH - 60 * S)
    if tip is not None:
        tw_ = (PX + tip[0], PY + tip[1])
    else:
        # glide to rest
        tw_ = rest
    world.paste(Image.new("RGB", pen_shadow.size, (0, 0, 0)),
                (int(tw_[0] - pen_tip_offset[0] + 26 * S), int(tw_[1] - pen_tip_offset[1] + 34 * S)),
                pen_shadow.point(lambda v: int(v * 0.55)))
    world.paste(pen_rot, (int(tw_[0] - pen_tip_offset[0]), int(tw_[1] - pen_tip_offset[1])), pen_rot)
    return world


def camera_crop(world, t):
    cx, cy, z = camera_for(t)
    vw, vh = WW / z / 1.0, WH / z / 1.0
    box = (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2)
    return world.transform((W, H), Image.EXTENT, box, resample=Image.BICUBIC)


def grade(img, t):
    a = np.asarray(img).astype(np.float32)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.38 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    a *= np.clip(v, 0.45, 1)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


cracks = crack_network(11, W / 2, H / 2)
labels, sites = voronoi_labels(42, 12)
shard_ids = np.unique(labels)
shard_dirs = {}
r2 = random.Random(21)
for sid in shard_ids:
    ys, xs = np.nonzero(labels == sid)
    cx, cy = xs.mean(), ys.mean()
    shard_dirs[sid] = (cx, cy, r2.uniform(-25, 25), r2.uniform(0.0, 0.12))


def render_frame(i):
    t = i / FPS
    img = grade(camera_crop(render_world(t), t), t)
    # crack overlay 18.4-19.0 (screen space), glass tint
    pc = seg(t, 18.35, 19.0)
    if pc > 0:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        tint = int(70 * ease(pc))
        od.rectangle([0, 0, W, H], fill=(*GLASS_GREEN, tint))
        for depth, pts in cracks:
            k = max(2, int(len(pts) * ease_out(pc * (1.0 + 0.4 * depth))))
            k = min(k, len(pts))
            od.line(pts[:k], fill=(235, 245, 255, 230 - depth * 40), width=max(1, 3 - depth))
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    # shards 19.0-20.0 over 3D frame 1
    ps = seg(t, 19.0, 20.0)
    if ps > 0:
        base = three.copy()
        lab_img = Image.fromarray(labels.astype(np.uint8))
        e = ps ** 1.6
        order = sorted(shard_ids, key=lambda s: -((shard_dirs[s][0] - W / 2) ** 2 + (shard_dirs[s][1] - H / 2) ** 2))
        for sid in order:
            cx, cy, rot, delay = shard_dirs[sid]
            q = min(1, max(0, (e - delay) / (1 - delay)))
            if q >= 1:
                continue
            mask = lab_img.point(lambda v, s=int(sid): 255 if v == s else 0)
            piece = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            piece.paste(img, (0, 0), mask)
            scale = 1 + 1.6 * q
            dx = (cx - W / 2) * (scale - 1) * 1.3
            dy = (cy - H / 2) * (scale - 1) * 1.3
            bb = mask.getbbox()
            if not bb:
                continue
            crop = piece.crop(bb)
            crop = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.BICUBIC)
            crop = crop.rotate(rot * q, expand=True, resample=Image.BICUBIC)
            alpha = crop.split()[3].point(lambda v: int(v * (1 - q ** 2)))
            # bright glass edge
            px = int(cx + dx - crop.width / 2)
            py = int(cy + dy - crop.height / 2)
            base.paste(crop, (px, py), alpha)
        img = base
    return img


if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[sys.argv.index("--only") + 1].split(",")] if "--only" in sys.argv else None
    frames = only if only else range(N)
    for i in frames:
        render_frame(i).save(os.path.join(args.out, f"SH-028-030_{i + 1:04d}.png"))
    print("frames:", len(list(frames)))
