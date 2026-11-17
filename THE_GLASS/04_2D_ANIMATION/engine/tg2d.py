"""THE GLASS · 2D engine (tg2d)

A small, reusable 2.5D cutout-animation engine on Pillow + NumPy:
* Layers are RGBA images on a 1920x1080 "world". Each has a parallax factor p and an
  optional motion function m(t) -> (dx, dy, scale, alpha).
* A camera function cam(t) -> (zoom, cx, cy) frames the world. Layers with p<1 move less (depth).
* Overlays draw in screen space each frame (counters, strokes, flicker, text reveals).
* Global grade: palette tint, vignette, film grain.
* Frames are piped straight into ffmpeg (H.264, 1280x720, 24 fps).

Everything here is procedural, so it needs no external art. The fonts are the project's OFL/Apache files.
"""
import math
import os
import pathlib
import random
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
TYPO = ROOT / "03_2D_ASSETS/typography"
W, H, FPS = 1280, 720, 24
WW, WH = 1920, 1080                     # world size

NAVY = (23, 33, 43); SLATE = (85, 103, 116); IVORY = (233, 230, 222); AMBER = (199, 139, 85)
OXIDE = (169, 81, 73); INK = (38, 44, 52); GLASS = (120, 160, 140); CHAR = (14, 18, 23)
SUN = (232, 194, 122); STEEL = (60, 72, 84); FOG = (150, 162, 172)


def font(name, size):
    f = {"hand": "caveat-latin-600-normal.woff", "hand_l": "caveat-latin-400-normal.woff",
         "stamp": "special-elite-latin-400-normal.woff", "card": "oswald-latin-600-normal.woff",
         "card_l": "oswald-latin-400-normal.woff", "serif": "eb-garamond-latin-500-normal.woff",
         "serif_l": "eb-garamond-latin-400-normal.woff"}[name]
    return ImageFont.truetype(str(TYPO / f), int(size))


# ------------------------------------------------------------------ timing helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def lerp(a, b, x):
    return a + (b - a) * x


def mix(c1, c2, x):
    return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))


# ------------------------------------------------------------------ canvases & primitives
def rgba(size=(WW, WH), col=(0, 0, 0, 0)):
    return Image.new("RGBA", size, col)


def vgrad(size, top, bottom):
    w, h = size
    a = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - a) + np.array(bottom)[None, None, :] * a)
    arr = np.repeat(arr, w, axis=1)
    return Image.fromarray(arr.astype(np.uint8)).convert("RGBA")


def noise(size, scale, seed, lo, hi):
    r = np.random.default_rng(seed)
    w, h = size
    small = r.random((max(2, h // scale), max(2, w // scale)))
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return lo + np.asarray(im).astype(np.float32) / 255 * (hi - lo)


def textured(img, amt=6, seed=1, scale=3):
    a = np.asarray(img).astype(np.float32)
    n = noise(img.size, scale, seed, -amt, amt)
    a[..., :3] += n[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def radial(size, center, radius, color, strength=1.0, power=1.8):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2) / radius
    a = (np.clip(1 - d, 0, 1) ** power) * 255 * strength
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., :3] = color
    arr[..., 3] = np.clip(a, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def blur(img, r):
    return img.filter(ImageFilter.GaussianBlur(r))


def shadowed(layer, r=14, off=(10, 14), alpha=150):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(layer.split()[3].point(lambda v: v * alpha // 255))
    sh = blur(sh, r)
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    out.alpha_composite(sh, off)
    out.alpha_composite(layer)
    return out


def person(d, x, y, h, col=CHAR, pose="stand", hood=False, mask=False, facing=0):
    """Faceless silhouette, feet at (x, y), height h. pose: stand/seated/crouch/walk."""
    u = h / 10.0
    if pose == "seated":
        d.rounded_rectangle([x - 1.3 * u, y - 7.4 * u, x + 1.3 * u, y - 3.0 * u], radius=int(u), fill=col)
        d.rectangle([x - 1.3 * u, y - 3.2 * u, x + 2.6 * u, y - 2.2 * u], fill=col)
        d.rectangle([x + 1.8 * u, y - 3.0 * u, x + 2.6 * u, y], fill=col)
        hy = y - 8.4 * u
    elif pose == "crouch":
        d.rounded_rectangle([x - 1.4 * u, y - 5.6 * u, x + 1.4 * u, y - 1.6 * u], radius=int(1.2 * u), fill=col)
        d.rounded_rectangle([x - 1.2 * u, y - 2.2 * u, x + 1.6 * u, y], radius=int(0.6 * u), fill=col)
        hy = y - 6.4 * u
    else:
        sw = 0.5 * u if pose == "walk" else 0
        d.rounded_rectangle([x - 1.5 * u, y - 8.0 * u, x + 1.5 * u, y - 4.2 * u], radius=int(1.1 * u), fill=col)
        d.polygon([(x - 1.0 * u, y - 4.4 * u), (x - 0.15 * u, y - 4.4 * u), (x - 0.4 * u - sw, y), (x - 1.1 * u - sw, y)], fill=col)
        d.polygon([(x + 0.15 * u, y - 4.4 * u), (x + 1.0 * u, y - 4.4 * u), (x + 1.1 * u + sw, y), (x + 0.4 * u + sw, y)], fill=col)
        hy = y - 9.0 * u
    r = 0.95 * u
    d.ellipse([x - r, hy - r, x + r, hy + r], fill=col)
    if hood or mask:
        d.polygon([(x - 1.25 * u, hy + 0.4 * u), (x, hy - 1.45 * u), (x + 1.25 * u, hy + 0.4 * u)], fill=col)
    if mask:  # eye slit only, no face
        d.rectangle([x - 0.55 * u, hy - 0.15 * u, x + 0.55 * u, hy + 0.08 * u], fill=(40, 46, 52))


def house(d, x, y, w, h, col, roof, lit=0, rnd=None):
    d.rectangle([x, y - h, x + w, y], fill=col)
    d.polygon([(x - 6, y - h), (x + w / 2, y - h - w * 0.45), (x + w + 6, y - h)], fill=roof)
    rnd = rnd or random.Random(int(x))
    for i in range(int(w // 34)):
        for j in range(int(h // 40)):
            wx, wy = x + 12 + i * 34, y - h + 14 + j * 40
            if wx + 14 < x + w:
                c = AMBER if rnd.random() < lit else mix(col, NAVY, 0.55)
                d.rectangle([wx, wy, wx + 14, wy + 20], fill=c)


def cathedral(d, x, y, s, col):
    """Stylised Romanesque cathedral silhouette with twin east towers and a spire (not a survey drawing)."""
    d.rectangle([x, y - 140 * s, x + 380 * s, y], fill=col)                      # nave
    d.polygon([(x - 10 * s, y - 140 * s), (x + 190 * s, y - 215 * s), (x + 390 * s, y - 140 * s)], fill=col)
    for tx in (x + 300 * s, x + 350 * s):                                         # twin towers
        d.rectangle([tx, y - 300 * s, tx + 40 * s, y], fill=col)
        d.polygon([(tx - 4 * s, y - 300 * s), (tx + 20 * s, y - 380 * s), (tx + 44 * s, y - 300 * s)], fill=col)
    d.rectangle([x + 40 * s, y - 230 * s, x + 90 * s, y - 140 * s], fill=col)    # west tower
    d.polygon([(x + 34 * s, y - 230 * s), (x + 65 * s, y - 420 * s), (x + 96 * s, y - 230 * s)], fill=col)


def crack_lines(seed, cx, cy, n=9, length=(300, 700), scale=1.0):
    r = random.Random(seed)
    lines = []

    def branch(x, y, a, ln, depth):
        pts = [(x, y)]
        for _ in range(int(ln / 18)):
            a += r.uniform(-0.35, 0.35)
            x += math.cos(a) * 18 * scale; y += math.sin(a) * 18 * scale
            pts.append((x, y))
            if depth < 3 and r.random() < 0.08:
                branch(x, y, a + r.choice([-1, 1]) * r.uniform(0.5, 1.1), ln * 0.5, depth + 1)
        lines.append((depth, pts))
    for k in range(n):
        branch(cx, cy, k / n * 2 * math.pi + r.uniform(-0.2, 0.2), r.uniform(*length), 0)
    return lines


def draw_cracks(d, lines, p=1.0, col=(235, 245, 255), alpha=230, width=3):
    for depth, pts in lines:
        k = min(len(pts), max(2, int(len(pts) * ease_out(p * (1.0 + 0.4 * depth)))))
        d.line(pts[:k], fill=(*col, max(0, alpha - depth * 40)), width=max(1, width - depth))


def impact_star(d, cx, cy, size, seed, col=(240, 246, 255, 235)):
    r = random.Random(seed)
    for i in range(9):
        a = i / 9 * 2 * math.pi + r.uniform(-0.25, 0.25)
        ln = size * r.uniform(0.45, 1.0)
        d.line([(cx, cy), (cx + math.cos(a) * ln, cy + math.sin(a) * ln)], fill=col, width=2)
    d.ellipse([cx - size * 0.1, cy - size * 0.1, cx + size * 0.1, cy + size * 0.1], fill=col)


def card(w, h, title, body=None, top=NAVY, bg=IVORY, fs=54, bfs=118, tcol=IVORY, bcol=NAVY):
    c = rgba((w, h))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=10, fill=(*bg, 255), outline=(150, 145, 135, 255), width=2)
    d.rectangle([0, 0, w, int(h * 0.24)], fill=(*top, 255))
    d.text((w / 2, h * 0.12), title, font=font("card", fs), fill=tcol, anchor="mm")
    if body:
        d.text((w / 2, h * 0.6), body, font=font("card", bfs), fill=bcol, anchor="mm")
    return textured(c, 4, 7)


def stamp(text, col=OXIDE, size=64, rot=-8, seed=9):
    f = font("stamp", size)
    tw = int(f.getlength(text)) + 70
    th = int(size * 1.7)
    s = rgba((tw, th))
    d = ImageDraw.Draw(s)
    d.rounded_rectangle([6, 6, tw - 6, th - 6], radius=14, outline=(*col, 255), width=8)
    d.text((tw / 2, th / 2 + 4), text, font=f, fill=(*col, 255), anchor="mm")
    ink = (noise((tw, th), 2, seed, 0, 1) > 0.18).astype(np.uint16) * 255
    a = np.asarray(s.split()[3]).astype(np.uint16) * ink // 255
    s.putalpha(Image.fromarray(a.astype(np.uint8)))
    return s.rotate(rot, expand=True, resample=Image.BICUBIC)


def name_card(name, sub=None, accent=AMBER, w=760):
    h = 170 if sub else 120
    c = rgba((w, h))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, w, h], fill=(12, 16, 21, 225))
    d.rectangle([0, 0, 8, h], fill=(*accent, 255))
    d.text((34, 22), name, font=font("card", 64), fill=IVORY)
    if sub:
        d.text((36, 108), sub, font=font("serif", 34), fill=(190, 196, 200))
    return c


def text_layer(txt, fname, size, col, w=WW, h=None, anchor="mm", pos=None, spacing=10):
    f = font(fname, size)
    h = h or int(size * 2.2)
    c = rgba((w, h))
    d = ImageDraw.Draw(c)
    d.multiline_text(pos or (w / 2, h / 2), txt, font=f, fill=col, anchor=anchor, align="center", spacing=spacing)
    return c


# ------------------------------------------------------------------ stylised maps (NOT to scale)
NORWAY = [(560, 1000), (520, 930), (470, 880), (430, 840), (400, 790), (420, 740), (470, 700), (500, 640), (560, 600),
          (600, 540), (650, 480), (700, 420), (760, 360), (820, 300), (900, 230), (980, 170), (1060, 120), (1150, 90),
          (1240, 80), (1300, 110), (1250, 150), (1170, 190), (1100, 240), (1040, 300), (980, 360), (930, 430),
          (880, 500), (840, 560), (800, 640), (760, 720), (730, 800), (700, 880), (660, 960), (620, 1010)]
SPAIN = [(300, 300), (520, 260), (760, 250), (980, 280), (1160, 340), (1280, 420), (1240, 520), (1180, 640),
         (1100, 760), (980, 840), (820, 880), (650, 870), (520, 800), (420, 700), (330, 600), (280, 480)]


def map_base(poly, land=(48, 60, 70), sea=(16, 24, 32), seed=3, label=None):
    base = vgrad((WW, WH), mix(sea, NAVY, 0.3), sea)
    d = ImageDraw.Draw(base)
    for i in range(0, WW, 60):
        d.line([(i, 0), (i, WH)], fill=(30, 40, 52, 255), width=1)
    for j in range(0, WH, 60):
        d.line([(0, j), (WW, j)], fill=(30, 40, 52, 255), width=1)
    d.polygon(poly, fill=(*land, 255))
    d.line(poly + [poly[0]], fill=(110, 128, 140, 255), width=3)
    base = textured(base, 5, seed, 4)
    if label:
        ImageDraw.Draw(base).text((WW - 40, WH - 40), label, font=font("card_l", 26), fill=(120, 132, 140), anchor="rd")
    return base


def pin(d, x, y, col=AMBER, r=14, label=None, fs=36):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(*col, 255))
    d.ellipse([x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2], outline=(*col, 160), width=3)
    if label:
        d.text((x + r * 2.6, y), label, font=font("card", fs), fill=(*IVORY, 255), anchor="lm")


def route(d, pts, p, col=AMBER, width=6, dash=False):
    k = max(2, int(len(pts) * clamp(p)))
    if dash:
        for i in range(0, k - 1, 2):
            d.line([pts[i], pts[i + 1]], fill=(*col, 255), width=width)
    else:
        d.line(pts[:k], fill=(*col, 255), width=width, joint="curve")


def curve(a, b, bend=0.25, n=80):
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0) * bend, (x1 - x0) * bend
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * (mx + nx) + t * t * x1,
             (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (my + ny) + t * t * y1) for t in np.linspace(0, 1, n)]


# ------------------------------------------------------------------ shot / renderer
class Layer:
    def __init__(self, img, p=1.0, motion=None, blend=None):
        self.img, self.p, self.motion = img, p, motion


class Shot:
    def __init__(self, sid, dur):
        self.sid, self.dur = sid, dur
        self.layers = []
        self.overlays = []          # fn(t, img RGBA screen) -> None (draw in place)
        self.cam = lambda t: (1.0, WW / 2, WH / 2)
        self.tint = (1.0, 1.0, 1.0)
        self.vignette = 0.38
        self.fade_in = 0.0
        self.fade_out = 0.0
        self.white = None           # fn(t)->0..1 white-out amount

    def add(self, img, p=1.0, motion=None):
        self.layers.append(Layer(img, p, motion))
        return self

    def over(self, fn):
        self.overlays.append(fn)
        return self


_VIG = None
_GRAIN = None


def _grade_arrays():
    global _VIG, _GRAIN
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _VIG = (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        r = np.random.default_rng(5)
        _GRAIN = [r.normal(0, 1, (H, W)).astype(np.float32) for _ in range(6)]
    return _VIG, _GRAIN


def render_frame(shot, t, i):
    zoom, cx, cy = shot.cam(t)
    frame = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    for L in shot.layers:
        img = L.img
        dx = dy = 0.0; sc = 1.0; al = 1.0
        if L.motion:
            dx, dy, sc, al = L.motion(t)
        if al <= 0.003:
            continue
        z = 1 + (zoom - 1) * L.p
        lcx = WW / 2 + (cx - WW / 2) * L.p - dx
        lcy = WH / 2 + (cy - WH / 2) * L.p - dy
        z *= sc
        vw, vh = WW / z, WH / z
        ox = (img.width - WW) / 2
        oy = (img.height - WH) / 2
        box = (lcx - vw / 2 + ox, lcy - vh / 2 + oy, lcx + vw / 2 + ox, lcy + vh / 2 + oy)
        tile = img.transform((W, H), Image.EXTENT, box, resample=Image.BILINEAR)
        if al < 1:
            tile.putalpha(tile.split()[3].point(lambda v, a=al: int(v * a)))
        frame.alpha_composite(tile)
    for fn in shot.overlays:
        fn(t, frame)
    vig, grain = _grade_arrays()
    a = np.asarray(frame.convert("RGB")).astype(np.float32)
    a *= np.clip(1 - shot.vignette * vig, 0.4, 1)[..., None]
    a *= np.array(shot.tint, np.float32)[None, None, :]
    a += grain[i % len(grain)][..., None] * 4.0
    fade = 1.0
    if shot.fade_in:
        fade *= ease(seg(t, 0, shot.fade_in))
    if shot.fade_out:
        fade *= ease(1 - seg(t, shot.dur - shot.fade_out, shot.dur))
    a *= fade
    if shot.white:
        wv = shot.white(t)
        a = a * (1 - wv) + 245 * wv
    return np.clip(a, 0, 255).astype(np.uint8)


def render_shot(shot, out_path, preview_frames=None):
    n = int(round(shot.dur * FPS))
    if preview_frames:
        os.makedirs(out_path, exist_ok=True)
        for i in preview_frames:
            Image.fromarray(render_frame(shot, i / FPS, i)).save(os.path.join(out_path, f"{shot.sid}_f{i:04d}.png"))
        return
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", str(out_path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(render_frame(shot, i / FPS, i).tobytes())
    p.stdin.close()
    p.wait()
    return n
