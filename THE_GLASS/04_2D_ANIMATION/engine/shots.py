"""THE GLASS · 2D shot library: one builder per 2D shot (SH-001 … SH-102), rough-cut v001.

Each builder returns a tg2d.Shot. Durations come from 00_PROJECT_MANAGEMENT/shot_tracker.csv.
SH-028–030 are NOT rebuilt here: the cut reuses the approved prototype notebook sequence.
Shared sets are cached in SETS so every shot that shows the NOKAS façade, the police station,
the notebook and so on uses the same artwork.

Run:  python3 shots.py --out <dir> [--only SH-001,SH-005] [--preview] [--jobs 3]
"""
import argparse
import csv
import functools
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from tg2d import *  # noqa: E402,F401,F403

TRACKER = ROOT / "00_PROJECT_MANAGEMENT/shot_tracker.csv"
DUR = {r["shot_id"]: float(r["duration_s"]) for r in csv.DictReader(open(TRACKER, encoding="utf-8"))}
TYPE = {r["shot_id"]: r["type"] for r in csv.DictReader(open(TRACKER, encoding="utf-8"))}
SETS = {}


def cached(fn):
    @functools.wraps(fn)
    def w():
        if fn.__name__ not in SETS:
            SETS[fn.__name__] = fn()
        return SETS[fn.__name__]
    return w


# ===================================================================== shared sets
@cached
def set_night_sky():
    sky = vgrad((WW, WH), (10, 15, 22), (28, 40, 54))
    d = ImageDraw.Draw(sky)
    r = random.Random(2)
    for _ in range(160):
        x, y = r.randrange(WW), r.randrange(int(WH * 0.55))
        v = r.randrange(90, 190)
        d.point((x, y), fill=(v, v, v + 10, 255))
    return sky


@cached
def set_dawn_sky():
    return textured(vgrad((WW, WH), (32, 44, 60), (120, 108, 104)), 3, 4)


@cached
def set_stavanger_far():
    L = rgba((2400, WH))
    d = ImageDraw.Draw(L)
    r = random.Random(11)
    x = 0
    while x < 2400:
        w = r.randint(70, 150); h = r.randint(90, 200)
        house(d, x, 760, w, h, (64, 74, 86), (44, 52, 62), lit=0.12, rnd=r)
        x += w + r.randint(4, 18)
    cathedral(d, 1180, 770, 0.9, (40, 48, 58))
    return L


@cached
def set_stavanger_near():
    L = rgba((2600, WH))
    d = ImageDraw.Draw(L)
    r = random.Random(12)
    x = -40
    while x < 2600:
        w = r.randint(130, 220); h = r.randint(150, 280)
        col = mix((210, 208, 200), (150, 156, 160), r.random() * 0.6)
        house(d, x, 900, w, h, col, mix(col, NAVY, 0.6), lit=0.25, rnd=r)
        x += w + r.randint(6, 20)
    d.rectangle([0, 900, 2600, WH], fill=(20, 28, 36, 255))
    return L


@cached
def set_harbour():
    L = rgba((2600, WH))
    d = ImageDraw.Draw(L)
    for i in range(0, 200, 6):
        y = 880 + i
        d.line([(0, y), (2600, y)], fill=(24 + i // 10, 36 + i // 10, 50 + i // 8, 255), width=6)
    r = random.Random(3)
    for _ in range(140):
        x, y = r.randrange(2600), r.randrange(890, WH)
        d.line([(x, y), (x + r.randint(20, 80), y)], fill=(*AMBER, r.randrange(30, 120)), width=2)
    for bx in (300, 900, 1600, 2100):  # moored supply boats
        d.polygon([(bx, 900), (bx + 220, 900), (bx + 190, 940), (bx + 20, 940)], fill=(30, 36, 44, 255))
        d.rectangle([bx + 120, 850, bx + 190, 900], fill=(36, 44, 52, 255))
    return L


@cached
def set_nokas_facade():
    """Stylised NOKAS cash-centre façade (generic, NOT a survey of the real building)."""
    L = rgba((WW, WH))
    d = ImageDraw.Draw(L)
    d.rectangle([380, 160, 1540, 940], fill=(88, 96, 102, 255))
    for i in range(5):
        for j in range(4):
            x, y = 450 + i * 210, 230 + j * 160
            d.rectangle([x, y, x + 120, y + 100], fill=(40, 48, 56, 255))
            d.rectangle([x, y + 96, x + 120, y + 104], fill=(120, 128, 132, 255))
    d.rectangle([860, 760, 1060, 940], fill=(30, 36, 42, 255))
    d.rectangle([700, 690, 1220, 740], fill=(24, 30, 36, 255))
    d.text((960, 715), "NOKAS · Norsk Kontantservice", font=font("card_l", 34), fill=IVORY, anchor="mm")
    return textured(L, 5, 21)


@cached
def set_police_station():
    L = rgba((WW, WH))
    d = ImageDraw.Draw(L)
    d.rectangle([300, 220, 1650, 860], fill=(70, 80, 92, 255))
    for i in range(7):
        for j in range(3):
            x, y = 360 + i * 180, 270 + j * 130
            d.rectangle([x, y, x + 110, y + 80], fill=(34, 44, 56, 255))
    d.polygon([(900, 860), (1500, 860), (1500, 1080), (760, 1080)], fill=(40, 44, 50, 255))  # ramp
    d.rectangle([1040, 640, 1460, 860], fill=(22, 26, 30, 255))                                  # garage door
    d.text((560, 690), "POLICE", font=font("card", 48), fill=(170, 180, 190), anchor="mm")
    return textured(L, 5, 22)


def truck(w=520):
    t = rgba((w, int(w * 0.48)))
    d = ImageDraw.Draw(t)
    h = t.height
    d.rectangle([0, 0, int(w * 0.68), int(h * 0.78)], fill=(205, 205, 200, 255))
    d.polygon([(int(w * 0.70), int(h * 0.2)), (int(w * 0.92), int(h * 0.2)), (w, int(h * 0.5)), (w, int(h * 0.78)), (int(w * 0.70), int(h * 0.78))], fill=(190, 192, 190, 255))
    d.rectangle([int(w * 0.78), int(h * 0.27), int(w * 0.92), int(h * 0.48)], fill=(50, 60, 70, 255))
    for x in (0.16, 0.5, 0.84):
        d.ellipse([int(w * x) - 34, int(h * 0.7), int(w * x) + 34, int(h * 0.7) + 68], fill=(20, 20, 22, 255))
    return t


def car(w=360, col=(40, 46, 54)):
    c = rgba((w, int(w * 0.42)))
    d = ImageDraw.Draw(c)
    h = c.height
    d.rounded_rectangle([0, int(h * 0.35), w, int(h * 0.8)], radius=20, fill=(*col, 255))
    d.polygon([(int(w * 0.2), int(h * 0.38)), (int(w * 0.32), int(h * 0.05)), (int(w * 0.72), int(h * 0.05)), (int(w * 0.85), int(h * 0.38))], fill=(*col, 255))
    for x in (0.22, 0.78):
        d.ellipse([int(w * x) - 30, int(h * 0.62), int(w * x) + 30, int(h * 0.62) + 60], fill=(15, 15, 16, 255))
    return c


@cached
def set_desk():
    base = vgrad((WW, WH), mix(NAVY, CHAR, 0.4), CHAR)
    base = textured(base, 4, 30, 3)
    base.alpha_composite(radial((WW, WH), (WW * 0.36, WH * 0.28), 1200, (70, 46, 22), 0.9))
    return base


def notebook(lines=(), w=1500, h=1000, seed=4):
    pg = textured(Image.new("RGBA", (w, h), (*IVORY, 255)), 6, seed, 2)
    d = ImageDraw.Draw(pg)
    for x in range(130, w, 44):
        d.line([(x, 0), (x, h)], fill=(214, 214, 210, 255))
    for y in range(60, h, 44):
        d.line([(0, y), (w, y)], fill=(214, 214, 210, 255))
    d.line([(110, 0), (110, h)], fill=(196, 150, 140, 255), width=2)
    for y in range(70, h, 90):
        d.ellipse([32, y - 13, 58, y + 13], fill=tuple(int(c * 0.55) for c in NAVY))
    for (x, y, txt, size, col) in lines:
        d.text((x, y), txt, font=font("hand", size), fill=col)
    return shadowed(pg, 24, (16, 22), 170)


@cached
def set_board():
    b = textured(vgrad((WW + 400, WH + 200), (46, 40, 34), (30, 26, 22)), 8, 40, 3)
    return b


@cached
def set_courtroom():
    c = textured(vgrad((WW, WH), (40, 44, 48), (22, 24, 28)), 5, 50)
    d = ImageDraw.Draw(c)
    d.rectangle([260, 260, 1660, 520], fill=(58, 46, 36, 255))           # judges' bench
    d.rectangle([260, 250, 1660, 270], fill=(80, 64, 50, 255))
    for i in range(5):
        person(d, 520 + i * 220, 330, 150, (30, 30, 34), "seated")
    d.rectangle([0, 760, WW, 790], fill=(58, 46, 36, 255))               # dock rail
    return c


def courtroom_defendants(n=13, highlight=None, dim=False):
    L = rgba((WW, WH))
    d = ImageDraw.Draw(L)
    for i in range(n):
        x = 180 + i * 120
        col = (24, 26, 30) if not dim else (46, 48, 52)
        if highlight is not None and i == highlight:
            col = (14, 16, 18)
        person(d, x, 1000, 300, col, "stand")
    return L


@cached
def set_counting_room():
    c = textured(vgrad((WW, WH), (92, 70, 50), (44, 34, 26)), 5, 60)
    d = ImageDraw.Draw(c)
    d.rectangle([0, 740, WW, WH], fill=(38, 30, 24, 255))
    for x in (260, 860, 1460):
        d.rectangle([x, 640, x + 420, 690], fill=(70, 54, 40, 255))
        d.rectangle([x + 20, 690, x + 40, 840], fill=(50, 40, 30, 255))
        d.rectangle([x + 380, 690, x + 400, 840], fill=(50, 40, 30, 255))
        d.rectangle([x + 60, 560, x + 220, 640], fill=(56, 60, 62, 255))  # counting machine
    c.alpha_composite(radial((WW, WH), (WW / 2, 120), 900, (255, 200, 140), 0.35))
    return c


@cached
def set_glass_window():
    """Frontal laminated window (matches M02 proportions 2.2 x 1.6 m)."""
    L = rgba((WW, WH))
    d = ImageDraw.Draw(L)
    d.rectangle([0, 0, WW, WH], fill=(54, 62, 66, 255))
    x0, y0, x1, y1 = 360, 190, 1560, 1063
    d.rectangle([x0 - 30, y0 - 30, x1 + 30, y1 + 30], fill=(20, 24, 28, 255))
    gl = vgrad((x1 - x0, y1 - y0), (108, 140, 128), (64, 92, 84))
    L.alpha_composite(gl, (x0, y0))
    d.rectangle([958, y0, 962 + 18, y1], fill=(20, 24, 28, 255))
    for i in range(6):
        d.line([(x0 + 80 + i * 60, y0), (x0 + 380 + i * 60, y1)], fill=(170, 200, 190, 40), width=24)
    return textured(L, 4, 61)


@cached
def set_forest():
    L = rgba((2600, WH))
    d = ImageDraw.Draw(L)
    r = random.Random(70)
    for layer, (col, base) in enumerate((((26, 40, 36), 760), ((18, 30, 26), 860), ((10, 18, 16), 980))):
        for _ in range(70):
            x = r.randrange(-100, 2700); h = r.randint(220, 420) * (1 + layer * 0.3)
            d.polygon([(x, base - h), (x - h * 0.28, base), (x + h * 0.28, base)], fill=(*col, 255))
    return L


def flower():
    f = rgba((220, 360))
    d = ImageDraw.Draw(f)
    d.line([(110, 120), (118, 360)], fill=(60, 90, 60, 255), width=8)
    for a in range(6):
        ang = a / 6 * 2 * math.pi
        d.ellipse([110 + math.cos(ang) * 38 - 30, 110 + math.sin(ang) * 38 - 30, 110 + math.cos(ang) * 38 + 30, 110 + math.sin(ang) * 38 + 30], fill=(228, 226, 220, 255))
    d.ellipse([92, 92, 128, 128], fill=(*AMBER, 255))
    return f


# ===================================================================== helpers for builders
def push(z0, z1, cx0=WW / 2, cy0=WH / 2, cx1=None, cy1=None, dur=1.0, e=ease):
    cx1 = cx0 if cx1 is None else cx1
    cy1 = cy0 if cy1 is None else cy1
    return lambda t: (lerp(z0, z1, e(t / dur)), lerp(cx0, cx1, e(t / dur)), lerp(cy0, cy1, e(t / dur)))


def fade(a, b, slide=(0, 0)):
    return lambda t: (slide[0] * (1 - ease(seg(t, a, b))), slide[1] * (1 - ease(seg(t, a, b))), 1.0, ease(seg(t, a, b)))


def place(img, x, y, size=(WW, WH)):
    L = rgba(size)
    L.alpha_composite(img, (int(x), int(y)))
    return L


def flicker_glow(center, radius, col, base=0.6, amp=0.35, seed=1):
    r = random.Random(seed)
    phases = [r.random() * 6 for _ in range(3)]

    def fn(t, frame):
        k = base + amp * (math.sin(t * 9 + phases[0]) * 0.5 + math.sin(t * 23 + phases[1]) * 0.3 + math.sin(t * 5 + phases[2]) * 0.2)
        g = radial((W, H), center, radius, col, clamp(k))
        frame.alpha_composite(g)
    return fn


def smoke(seed, area, n=14, col=(120, 126, 132), speed=18):
    r = random.Random(seed)
    puffs = [(r.uniform(area[0], area[2]), r.uniform(area[1], area[3]), r.uniform(60, 160), r.uniform(0.3, 1.0)) for _ in range(n)]

    def fn(t, frame):
        L = rgba((W, H))
        d = ImageDraw.Draw(L)
        for (x, y, s, sp) in puffs:
            yy = y - t * speed * sp
            xx = x + math.sin(t * 0.6 + s) * 20
            ss = s * (1 + t * 0.05)
            d.ellipse([xx - ss, yy - ss * 0.7, xx + ss, yy + ss * 0.7], fill=(*col, 70))
        frame.alpha_composite(blur(L, 22))
    return fn


def screen_text(txt, fname, size, col, xy, a=0, b=0.6, anchor="mm", end=None):
    f = font(fname, size)

    def fn(t, frame):
        al = ease(seg(t, a, b))
        if end:
            al *= 1 - ease(seg(t, end[0], end[1]))
        if al <= 0:
            return
        L = rgba((W, H))
        ImageDraw.Draw(L).multiline_text(xy, txt, font=f, fill=(*col, int(255 * al)), anchor=anchor, align="center", spacing=8)
        frame.alpha_composite(L)
    return fn


def paste_fn(img, xy_fn):
    def fn(t, frame):
        x, y, al = xy_fn(t)
        if al <= 0:
            return
        im = img
        if al < 1:
            im = img.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * al)))
        frame.alpha_composite(im, (int(x), int(y)))
    return fn


def counter(start, end, a, b, fmt, xy, size=110, col=IVORY):
    f = font("card", size)

    def fn(t, frame):
        v = lerp(start, end, ease_out(seg(t, a, b)))
        if t < a:
            return
        L = rgba((W, H))
        ImageDraw.Draw(L).text(xy, fmt(v), font=f, fill=(*col, 255), anchor="mm")
        frame.alpha_composite(L)
    return fn


def S(sid):
    return Shot(sid, DUR[sid])


# ===================================================================== COLD OPEN
def SH_001():
    s = S("SH-001")
    s.add(rgba((WW, WH), (6, 8, 10, 255)))
    lines = crack_lines(1, 640, 360, n=2, length=(700, 900), scale=1.2)

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        draw_cracks(d, lines, seg(t, 0.3, 3.0), width=2)
    s.over(fn)
    s.vignette = 0.6
    return s


def SH_002():
    s = S("SH-002")
    s.add(set_night_sky(), 0.2).add(set_police_station(), 0.8)
    tr = truck()
    s.add(place(tr, 0, 0, (WW, WH)), 0.9, lambda t: (lerp(1500, 920, ease_out(seg(t, 0, 2.4))), 780, 1.0, 1.0))
    s.over(flicker_glow((780, 560), 380, (255, 120, 40), 0.0, 0.0))
    s.overlays[-1] = (lambda g: (lambda t, fr: (fr.alpha_composite(radial((W, H), (780, 560), 420, (255, 120, 40), clamp(seg(t, 2.4, 4.0) * (0.7 + 0.25 * math.sin(t * 13))))))))(None)
    s.over(smoke(2, (600, 420, 980, 600)))
    s.cam = push(1.0, 1.12, WW / 2, WH / 2 + 40, dur=s.dur)
    return s


def SH_003():
    s = S("SH-003")
    s.add(rgba((WW, WH), (8, 10, 12, 255)))
    panels = []
    ps = set_police_station().crop((900, 520, 1600, 1080)).resize((400, 320))
    p1 = ps.copy(); p1.alpha_composite(radial(p1.size, (200, 200), 260, (255, 120, 40), 0.8))
    p2 = rgba((400, 320), (30, 34, 38, 255)); d2 = ImageDraw.Draw(p2)
    d2.rectangle([0, 200, 400, 320], fill=(36, 40, 44, 255))
    for i in range(14):
        x = 20 + i * 27
        d2.polygon([(x, 236), (x + 10, 214), (x + 20, 236)], fill=(170, 176, 180, 255))
    d2.rectangle([10, 236, 390, 244], fill=(90, 96, 100, 255))
    p3 = set_police_station().crop((300, 520, 900, 1000)).resize((400, 320))
    panels = [p1, p2, p3]
    for k, p in enumerate(panels):
        s.over(paste_fn(p, (lambda k: lambda t: (60 + k * 410, 200, ease(seg(t, k * 2.0, k * 2.0 + 0.4))))(k)))
    s.over(smoke(3, (860, 220, 1240, 480), n=10, speed=12))
    return s


def SH_004():
    s = S("SH-004")
    s.add(set_dawn_sky(), 0.1).add(set_stavanger_far(), 0.35).add(set_nokas_facade(), 0.8)
    near = rgba((WW, WH)); cathedral(ImageDraw.Draw(near), 60, 1100, 1.6, (12, 16, 20)); s.add(near, 1.3)
    s.cam = push(1.0, 1.7, WW / 2, WH / 2, 980, 560, dur=s.dur)

    def pulses(t, frame):
        if 4.0 < t:
            k = (math.sin(t * 31) > 0.6) * 0.5
            frame.alpha_composite(radial((W, H), (650, 420), 160, (255, 230, 190), k))
    s.over(pulses)
    return s


def SH_005():
    s = S("SH-005")
    s.add(set_glass_window(), 1.0)
    r = random.Random(5)
    stars = [(r.uniform(260, 1020), r.uniform(150, 640), r.uniform(26, 60), k, r.uniform(0, 4.6)) for k in range(70)]

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        for (x, y, sz, k, t0) in stars:
            if t >= t0:
                impact_star(d, x, y, sz, k)
    s.over(fn)
    s.over(screen_text("113", "card", 64, IVORY, (1180, 660), 3.6, 4.4, anchor="rd"))
    s.cam = push(1.0, 1.08, dur=s.dur)
    return s


def SH_006():
    s = S("SH-006")
    s.add(rgba((WW, WH), (8, 10, 13, 255)))
    tiles = []
    t1 = rgba((300, 380), (30, 36, 42, 255)); person(ImageDraw.Draw(t1), 150, 360, 300, (8, 9, 11), mask=True)
    t2 = rgba((300, 380), (36, 40, 44, 255)); d2 = ImageDraw.Draw(t2); d2.rectangle([140, 60, 160, 340], fill=(10, 10, 12, 255)); d2.rectangle([90, 40, 210, 100], fill=(10, 10, 12, 255))
    t3 = rgba((300, 380), (40, 46, 52, 255)); person(ImageDraw.Draw(t3), 150, 360, 300, (12, 14, 18)); ImageDraw.Draw(t3).ellipse([130, 70, 170, 110], outline=(*AMBER, 255), width=3)
    t4 = rgba((300, 380), (120, 104, 80, 255)); d4 = ImageDraw.Draw(t4); d4.rectangle([40, 60, 260, 300], fill=(60, 54, 46, 255)); d4.rectangle([60, 80, 240, 200], fill=(150, 170, 180, 255))
    for k, tl in enumerate((t1, t2, t3, t4)):
        poly = rgba(tl.size); ImageDraw.Draw(poly).polygon([(20, 0), (300, 30), (280, 380), (0, 350)], fill=(255, 255, 255, 255))
        tl.putalpha(poly.split()[3])
        s.over(paste_fn(tl, (lambda k: lambda t: (100 + k * 280, 170 + math.sin(t * 0.8 + k) * 18 - t * 6, ease(seg(t, k * 0.6, k * 0.6 + 0.6))))(k)))
    return s


def SH_007():
    s = S("SH-007")
    s.add(rgba((WW, WH), (6, 8, 10, 255)))
    r = random.Random(7)
    shards = [(r.uniform(0, W), r.uniform(0, H), r.uniform(30, 90), r.uniform(-1, 1)) for _ in range(40)]

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        e = ease_out(seg(t, 0, 1.6))
        for (x, y, sz, a) in shards:
            cx, cy = W / 2 + (x - W / 2) * (1 + 2.5 * e), H / 2 + (y - H / 2) * (1 + 2.5 * e)
            s_ = sz * (1 + 2 * e)
            al = int(200 * (1 - e))
            if al > 0:
                d.polygon([(cx, cy - s_), (cx + s_ * 0.7, cy + s_ * a * 0.5), (cx - s_ * 0.5, cy + s_)], fill=(110, 150, 140, al))
    s.over(fn)
    s.over(screen_text("THE GLASS", "serif", 120, IVORY, (640, 330), 1.6, 2.6))
    s.over(screen_text("The NOKAS Robbery  ·  Stavanger, 5 April 2004", "card_l", 30, (180, 186, 190), (640, 430), 2.4, 3.2))
    s.fade_out = 1.2
    return s


# ===================================================================== CH 1 · THE CITY OF MONEY
def stavanger_wide(sid, z0=1.0, z1=1.15, panx=0):
    s = S(sid)
    s.add(set_dawn_sky(), 0.1).add(set_stavanger_far(), 0.4, lambda t: (-panx * t * 0.4, 0, 1, 1))
    s.add(set_harbour(), 1.0, lambda t: (-panx * t, 0, 1, 1)).add(set_stavanger_near(), 0.9, lambda t: (-panx * t, 120, 1, 1))
    s.cam = push(z0, z1, dur=s.dur)
    return s


def SH_008():
    s = stavanger_wide("SH-008", 1.0, 1.12, 8)
    s.fade_in = 1.0
    return s


def SH_009():
    s = S("SH-009")
    s.add(set_dawn_sky(), 0.1)
    sea = rgba((2600, WH)); d = ImageDraw.Draw(sea); d.rectangle([0, 700, 2600, WH], fill=(28, 40, 52, 255)); s.add(sea, 0.6)
    rig = rgba((WW, WH)); d = ImageDraw.Draw(rig)
    for rx in (1300, 1600):
        d.rectangle([rx, 600, rx + 110, 640], fill=(20, 24, 30, 255)); d.line([(rx + 20, 640), (rx + 10, 700)], fill=(20, 24, 30, 255), width=6)
        d.line([(rx + 90, 640), (rx + 100, 700)], fill=(20, 24, 30, 255), width=6); d.line([(rx + 80, 600), (rx + 70, 520)], fill=(20, 24, 30, 255), width=5)
    s.add(rig, 0.6, lambda t: (-12 * t, 0, 1, 1))
    s.over(lambda t, fr: fr.alpha_composite(radial((W, H), (900, 420), 120, (*AMBER,), ease(seg(t, 1, 3)) * 0.6)))

    def tl(t, frame):
        d = ImageDraw.Draw(frame)
        p = ease(seg(t, 2, 7))
        d.line([(160, 600), (160 + 960 * p, 600)], fill=(*IVORY, 200), width=3)
        f = font("card", 34)
        for k, (yr, x) in enumerate((("1969 · oil found", 160), ("1970s", 420), ("1990s", 760), ("2004", 1100))):
            if p * 960 + 160 >= x:
                d.text((x, 620), yr, font=f, fill=IVORY, anchor="la" if k == 0 else "ma")
    s.over(tl)
    return s


def SH_010():
    s = S("SH-010")
    s.add(textured(vgrad((WW, WH), (22, 30, 40), (14, 18, 24)), 4, 10))
    labels = ["OIL", "COMPANIES", "BANKS", "CASH", "DEPOT"]

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        for k, lab in enumerate(labels):
            x = 150 + k * 245
            a = ease(seg(t, k * 1.1, k * 1.1 + 0.5))
            if a <= 0:
                continue
            col = AMBER if k in (3, 4) else (180, 190, 196)
            d.rounded_rectangle([x - 90, 300, x + 90, 420], radius=16, outline=(*col, int(255 * a)), width=4)
            d.text((x, 360), lab, font=font("card", 34), fill=(*col, int(255 * a)), anchor="mm")
            if k < 4 and t > k * 1.1 + 0.5:
                p = ease(seg(t, k * 1.1 + 0.5, k * 1.1 + 1.1))
                d.line([(x + 95, 360), (x + 95 + 50 * p, 360)], fill=(*IVORY, 200), width=4)
    s.over(fn)
    return s


def SH_011():
    s = S("SH-011")
    s.add(map_base([(300, 900), (500, 500), (900, 300), (1500, 260), (1700, 700), (1400, 1000)], label="Stavanger · stylised map"), 1.0,
          lambda t: (0, 0, 1, 1 - ease(seg(t, 4.5, 6.5))))
    s.add(set_dawn_sky(), 0.3, lambda t: (0, 0, 1, ease(seg(t, 4.5, 6.5))))
    s.add(set_nokas_facade(), 0.9, lambda t: (0, 0, 0.8 + 0.2 * ease(seg(t, 4.5, 8)), ease(seg(t, 4.5, 6.5))))
    s.over(lambda t, fr: pin(ImageDraw.Draw(fr), 700, 380, label="NOKAS", fs=34) if t < 5.0 else None)
    s.cam = push(1.0, 1.25, WW / 2, WH / 2, 1050, 560, dur=4.5)
    return s


def SH_012():
    s = S("SH-012")
    s.add(set_counting_room(), 1.0)
    figs = rgba((WW, WH)); d = ImageDraw.Draw(figs)
    for x in (420, 1020, 1620):
        person(d, x, 900, 330, (40, 30, 24))
    s.add(figs, 1.0)

    def notes(t, frame):
        d = ImageDraw.Draw(frame)
        for k in range(12):
            x = (k * 140 + t * 90) % 1400 - 60
            d.rectangle([x, 405, x + 70, 432], fill=(*mix(AMBER, IVORY, 0.4), 220))
    s.over(notes)
    s.cam = push(1.12, 1.0, dur=s.dur)
    return s


def SH_013():
    s = S("SH-013")
    s.add(map_base([(200, 950), (300, 300), (1700, 200), (1800, 900)], land=(58, 68, 76), label="city centre · stylised, not to scale"))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        p = ease(seg(t, 0.5, 4))
        route(d, curve((300, 600), (900, 360), 0.2), p, (180, 190, 196), 5, dash=True)
        if t > 1:
            d.text((300, 640), "cathedral", font=font("card", 28), fill=IVORY)
            d.rectangle([280, 560, 320, 600], fill=(*IVORY, 255))
        if t > 2.5:
            d.text((560, 420), "pedestrian street", font=font("card_l", 26), fill=(200, 200, 196))
        if t > 3.6:
            pin(d, 900, 360, label="NOKAS", fs=32)
    s.over(fn)
    s.cam = push(1.0, 1.08, dur=s.dur)
    return s


def SH_014():
    s = S("SH-014")
    s.add(set_dawn_sky(), 0.1).add(set_nokas_facade(), 0.7)
    r = random.Random(14)
    walkers = [(r.uniform(-400, 1300), r.choice([-1, 1]), r.uniform(60, 120), r.uniform(240, 330)) for _ in range(7)]

    def fn(t, frame):
        L = rgba((W, H)); d = ImageDraw.Draw(L)
        for (x0, dirn, sp, hh) in walkers:
            x = x0 + dirn * sp * t
            person(d, x % 1600 - 160, 760, hh, (18, 22, 26), "walk" if int(t * 4 + x0) % 2 else "stand")
        frame.alpha_composite(blur(L, 2))
    s.over(fn)
    return s


def SH_015():
    s = S("SH-015")
    s.add(rgba((WW, WH), (14, 18, 22, 255)))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        sep = 60 * math.sin(clamp(t / s.dur) * math.pi)
        for k in range(5):
            x = 420 + k * (60 + sep) - 2 * (60 + sep)
            d.polygon([(x + 240, 140), (x + 520, 220), (x + 520, 620), (x + 240, 540)], fill=(110, 150, 136, 90), outline=(180, 220, 200, 200))
        d.text((640, 660), "laminated security glass (illustrative)", font=font("card_l", 24), fill=(140, 150, 156), anchor="mm")
    s.over(fn)
    return s


def SH_016():
    s = S("SH-016")
    s.add(set_glass_window())

    def glint(t, frame):
        x = lerp(-300, 1600, ease(seg(t, 1, 7)))
        L = rgba((W, H)); ImageDraw.Draw(L).polygon([(x, 0), (x + 120, 0), (x - 160, H), (x - 280, H)], fill=(255, 255, 255, 50))
        frame.alpha_composite(blur(L, 30))
    s.over(glint)
    s.cam = push(1.0, 1.1, dur=s.dur)
    s.fade_out = 0.6
    return s


# ===================================================================== CH 2 · THE ARCHITECT
def SH_017():
    s = S("SH-017")
    s.add(map_base(NORWAY, label="Norway · stylised, not to scale"))
    sv, osl = (480, 870), (840, 820)

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        sx = lambda p: (p[0] * W / WW, p[1] * H / WH)
        pin(d, *sx(sv), label="Stavanger", fs=28)
        route(d, [sx(p) for p in curve(sv, osl, -0.3)], ease(seg(t, 1, 5)))
        if t > 5:
            pin(d, *sx(osl), label="Oslo", fs=28)
    s.over(fn)
    s.tint = (0.9, 0.96, 1.08)
    s.cam = push(1.0, 1.3, WW / 2, WH / 2, 700, 820, dur=s.dur)
    return s


@cached
def set_kitchen():
    k = textured(vgrad((WW, WH), (30, 36, 44), (16, 20, 26)), 5, 80)
    d = ImageDraw.Draw(k)
    d.rectangle([0, 720, WW, WH], fill=(22, 24, 28, 255))
    d.rectangle([500, 640, 1500, 700], fill=(46, 40, 34, 255))
    d.rectangle([1340, 120, 1700, 520], fill=(40, 52, 66, 255))      # window to night
    person(d, 860, 900, 520, (10, 12, 14), "seated")
    d.polygon([(1180, 380), (1260, 380), (1300, 440), (1140, 440)], fill=(60, 50, 40, 255))  # lamp shade
    k.alpha_composite(radial((WW, WH), (1220, 560), 520, (210, 150, 80), 0.6))
    for i in range(4):
        d.rectangle([620 + i * 140, 630, 720 + i * 140, 646], fill=(*IVORY, 255))
    return k


def SH_018():
    s = S("SH-018")
    s.add(set_kitchen())
    s.over(paste_fn(name_card("DAVID TOSKA", "planner of the robbery"), lambda t: (60, 520, ease(seg(t, 1.5, 2.3)))))
    s.cam = push(1.0, 1.08, dur=s.dur)
    return s


def nb_shot(sid, lines, cam=(1.0, 1.1), extra=None):
    s = S(sid)
    s.add(set_desk(), 0.4).add(place(notebook(lines), 200, 40), 1.0)
    s.cam = push(cam[0], cam[1], dur=s.dur)
    if extra:
        s.over(extra)
    return s


def SH_019():
    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        p = ease(seg(t, 0.5, 6))
        for k in range(5):
            y = 260 + k * 70
            d.line([(360, y), (360 + 620 * clamp(p * 5 - k), y)], fill=(*INK, 255), width=3)
    return nb_shot("SH-019", [(200, 80, "the plan", 80, INK)], extra=fn)


def SH_020():
    s = S("SH-020")
    s.add(set_desk(), 0.4)

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        for k, cx in enumerate((260, 640, 1020)):
            d.ellipse([cx - 130, 230, cx + 130, 490], outline=(*IVORY, 230), width=5)
        ang = t * 2
        d.line([(260, 360), (260 + 100 * math.sin(ang), 360 - 100 * math.cos(ang))], fill=(*AMBER, 255), width=5)
        route(d, curve((540, 420), (740, 300), 0.4), ease(seg(t, 0.5, 6)), IVORY, 4)
        sw = min(t, 6.5)
        d.line([(1020, 360), (1020 + 100 * math.sin(sw), 360 - 100 * math.cos(sw))], fill=(*OXIDE, 255), width=5)
        for k, lab in enumerate(("TIMELINES", "ROUTES", "MINUTES")):
            d.text((260 + k * 380, 540), lab, font=font("card", 34), fill=IVORY, anchor="mm")
    s.over(fn)
    return s


def SH_021():
    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        p = ease(seg(t, 0.3, 5))
        box = [(460, 160), (1040, 160), (1040, 600), (460, 600), (460, 160)]
        route(d, box, p, INK, 4)
        if t > 3:
            d.rectangle([700, 300, 860, 400], outline=(*OXIDE, 255), width=4)
            d.text((780, 420), "WINDOW", font=font("hand", 44), fill=(*OXIDE, 255), anchor="ma")
    return nb_shot("SH-021", [(200, 80, "NOKAS — Stavanger", 70, INK)], extra=fn)


def SH_022():
    s = S("SH-022")
    s.add(rgba((WW, WH), (16, 20, 26, 255)))
    left = set_nokas_facade().resize((960, 540)); right = set_police_station().resize((960, 540))

    def fn(t, frame):
        frame.alpha_composite(left.resize((620, 349)), (10, 186))
        frame.alpha_composite(right.resize((620, 349)), (650, 186))
        d = ImageDraw.Draw(frame)
        if t > 3.5:
            x = lerp(1300, 645, ease_out(seg(t, 3.5, 5)))
            d.rectangle([x - 10, 150, x + 10, 570], fill=(*OXIDE, 255))
        d.text((320, 600), "the building", font=font("card", 34), fill=IVORY, anchor="mm")
        d.text((960, 600), "the police", font=font("card", 34), fill=IVORY, anchor="mm")
    s.over(fn)
    return s


def SH_023():
    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        p = ease(seg(t, 0.5, 2))
        d.line([(640, 160), (640, 160 + 460 * p)], fill=(*INK, 255), width=4)
        if t > 2:
            d.text((450, 220), "GET IN", font=font("hand", 70), fill=(*INK, 255), anchor="mm")
        if t > 5:
            d.text((830, 220), "KEEP THEM OUT", font=font("hand", 60), fill=(*INK, 120), anchor="mm")
    return nb_shot("SH-023", [], extra=fn)


def SH_024():
    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        d.text((450, 220), "GET IN", font=font("hand", 70), fill=(*INK, 120), anchor="mm")
        d.text((830, 220), "KEEP THEM OUT", font=font("hand", 60), fill=(*INK, 255), anchor="mm")
        d.line([(640, 160), (640, 620)], fill=(*INK, 255), width=4)
        d.ellipse([730, 330, 930, 530], outline=(*OXIDE, 255), width=5)
        ang = min(t, 5.2) * 1.2
        d.line([(830, 430), (830 + 80 * math.sin(ang), 430 - 80 * math.cos(ang))], fill=(*OXIDE, 255), width=4)
    return nb_shot("SH-024", [], extra=fn)


def crew_shot(sid, names, highlight=None, accent=AMBER):
    s = S(sid)
    s.add(textured(vgrad((WW, WH), (20, 24, 30), (8, 10, 12)), 4, 90))

    def fn(t, frame):
        L = rgba((W, H)); d = ImageDraw.Draw(L)
        for k in range(7):
            a = ease(seg(t, k * 0.35, k * 0.35 + 0.6))
            x = 120 + k * 170
            col = (16, 18, 22) if highlight is None or k == highlight else (34, 36, 40)
            if a > 0:
                person(d, x, 640, 420, (*col, int(255 * a)) if False else col, mask=True)
        frame.alpha_composite(L)
    s.over(fn)
    for i, (nm, sub) in enumerate(names):
        s.over(paste_fn(name_card(nm, sub, accent), (lambda i: lambda t: (60, 60 + i * 190, ease(seg(t, 2 + i, 2.6 + i))))(i)))
    return s


def SH_025():
    return crew_shot("SH-025", [("ERLING HAVNÅ", "«the sledgehammer man»")])


def SH_026():
    return crew_shot("SH-026", [("METKEL BETEW", "one of the central figures")], highlight=3)


def SH_027():
    s = crew_shot("SH-027", [("KJELL ALRICH SCHUMANN", None)], highlight=5, accent=OXIDE)
    s.vignette = 0.55
    return s


# ===================================================================== CH 3b · BACK TO THE DRAWING BOARD
def SH_035():
    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        frame.alpha_composite(card(300, 240, "2004", "FEB", fs=40, bfs=90), (250, 300))
        a = ease(seg(t, 0.3, 2.5))
        sm = rgba((W, H)); ImageDraw.Draw(sm).ellipse([230, 380, 590, 520], fill=(200, 196, 188, int(200 * a)))
        frame.alpha_composite(blur(sm, 18))
    return nb_shot("SH-035", [(200, 80, "NOKAS — courtyard", 70, INK)], extra=fn)


def SH_036():
    s = S("SH-036")
    s.add(set_courtroom(), 0.6)
    q = rgba((900, 200)); d = ImageDraw.Draw(q)
    d.rectangle([0, 0, 900, 200], fill=(233, 230, 222, 235))
    d.text((450, 70), "“never an attempt”", font=font("serif", 64), fill=NAVY, anchor="mm")
    d.text((450, 150), "Toska's position in court (paraphrased)", font=font("card_l", 28), fill=(90, 96, 100), anchor="mm")
    s.over(paste_fn(q, lambda t: (190, 470, ease(seg(t, 1.5, 2.5)))))
    s.cam = push(1.0, 1.1, dur=s.dur)
    return s


def SH_037():
    s = S("SH-037")
    s.add(set_kitchen())

    def fn(t, frame):
        L = rgba((W, H)); d = ImageDraw.Draw(L)
        for k in range(2):
            x = 300 + k * 160 - t * 90
            person(d, x, 640, 380, (8, 10, 12, int(200 * (1 - seg(t, 1, 5)))) if False else (8, 10, 12), "walk")
        L.putalpha(L.split()[3].point(lambda v: int(v * (1 - seg(t, 1.5, 5.5)))))
        frame.alpha_composite(L)
    s.over(fn)
    return s


def SH_038():
    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        d.rectangle([700, 260, 900, 390], outline=(*INK, 255), width=4)
        d.text((800, 400), "WINDOW", font=font("hand", 48), fill=(*INK, 255), anchor="ma")
        if t > 2:
            txt = "ordinary glass?"
            n = int(len(txt) * seg(t, 2, 4.5))
            d.text((620, 470), txt[:n], font=font("hand", 58), fill=(*OXIDE, 255))
        if t > 5.5:
            x = lerp(-200, 1400, seg(t, 5.5, 7.6))
            L = rgba((W, H)); ImageDraw.Draw(L).polygon([(x, 0), (x + 90, 0), (x - 150, H), (x - 240, H)], fill=(220, 240, 230, 70))
            frame.alpha_composite(blur(L, 20))
    return nb_shot("SH-038", [(200, 80, "NOKAS — Stavanger", 70, INK)], extra=fn)


def SH_039():
    s = S("SH-039")
    s.add(set_night_sky(), 0.1).add(set_forest(), 0.3, lambda t: (-40 * t, 0, 1, 1))

    def road(t, frame):
        d = ImageDraw.Draw(frame)
        d.polygon([(560, 380), (720, 380), (1280, 720), (0, 720)], fill=(24, 26, 30, 255))
        for k in range(8):
            z = ((k / 8 + t * 0.35) % 1.0)
            y = 380 + z ** 2 * 340
            w = 4 + z * 30
            d.rectangle([640 - w / 2, y, 640 + w / 2, y + 6 + z * 30], fill=(200, 196, 180, 255))
        frame.alpha_composite(radial((W, H), (640, 600), 520, (220, 210, 170), 0.35))
    s.over(road)
    return s


def SH_040():
    s = S("SH-040")
    s.add(map_base([(200, 900), (260, 260), (1700, 220), (1760, 960)], land=(52, 62, 70), label="stylised overview · route not shown"))
    fz = rgba((WW, WH)); ImageDraw.Draw(fz).ellipse([1250, 350, 1700, 720], fill=(30, 52, 40, 255)); s.add(fz, 1.0)

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        d.text((260, 470), "CITY CENTRE", font=font("card", 34), fill=IVORY)
        d.text((990, 440), "SØRMARKA", font=font("card", 34), fill=IVORY)
        route(d, curve((360, 520), (960, 380), -0.2), ease(seg(t, 0.5, 6)), (170, 180, 186), 14)
    s.over(fn)
    return s


def SH_041():
    s = S("SH-041")
    s.add(set_desk())

    def fn(t, frame):
        months = ["FEB", "MAR", "APR"]
        k = min(2, int(seg(t, 1, 6) * 3))
        frame.alpha_composite(card(380, 300, "2004", months[k], fs=50, bfs=120), (450, 200))
        if k == 2 and t > 6.5:
            ImageDraw.Draw(frame).text((640, 560), "5 APRIL", font=font("card", 60), fill=AMBER, anchor="mm")
    s.over(fn)
    return s


# ===================================================================== CH 4a · 5 APRIL 2004
def SH_042():
    s = S("SH-042")
    s.add(set_night_sky(), 0.1).add(set_stavanger_far(), 0.4)
    s.over(screen_text("MONDAY 5 APRIL 2004", "card", 74, IVORY, (640, 280), 0.3, 1.0))
    s.over(screen_text("03:00", "card_l", 54, AMBER, (640, 370), 0.8, 1.4))

    def vans(t, frame):
        L = rgba((W, H)); d = ImageDraw.Draw(L)
        for k in range(3):
            x = -300 + (t * 120 + k * 380) % 1700
            d.rounded_rectangle([x, 560, x + 220, 640], radius=10, fill=(10, 12, 14, 255))
        frame.alpha_composite(L)
    s.over(vans)
    return s


def SH_043():
    s = S("SH-043")
    s.add(set_board(), 0.5)
    items = ["VEHICLES", "SPIKE STRIPS", "SMOKE CANISTERS", "WEAPONS"]
    for k, it in enumerate(items):
        c = card(330, 190, "EVIDENCE", None, top=STEEL, fs=30)
        ImageDraw.Draw(c).text((165, 120), it, font=font("card", 36), fill=NAVY, anchor="mm")
        s.over(paste_fn(c, (lambda k: lambda t: (80 + k * 300, 250 + (k % 2) * 40, ease(seg(t, k * 1.3, k * 1.3 + 0.5))))(k)))
    s.over(screen_text("listed in the court record · not shown in use", "card_l", 24, (170, 170, 164), (640, 640), 5, 6))
    return s


def SH_044():
    s = stavanger_wide("SH-044", 1.0, 1.06, 4)
    s.layers[0] = Layer(set_dawn_sky(), 0.1)

    def fn(t, frame):
        L = rgba((W, H)); d = ImageDraw.Draw(L)
        x = lerp(-120, 1400, t / s.dur)
        d.ellipse([x - 26, 600, x + 26, 652], outline=(16, 18, 22, 255), width=6); d.ellipse([x + 54, 600, x + 106, 652], outline=(16, 18, 22, 255), width=6)
        person(d, x + 40, 620, 150, (16, 18, 22), "seated")
        person(d, 300, 660, 230, (20, 22, 26), "stand")
        frame.alpha_composite(L)
        ImageDraw.Draw(frame).text((1240, 40), "07:59", font=font("card", 54), fill=IVORY, anchor="ra")
    s.over(fn)
    return s


def SH_045():
    s = S("SH-045")
    s.add(set_night_sky(), 0.1, lambda t: (0, 0, 1, ease(seg(t, 2, 3)))).add(set_police_station(), 0.9, lambda t: (0, 0, 1, ease(seg(t, 2, 2.6))))
    s.add(rgba((WW, WH), (12, 14, 18, 255)), 1.0, lambda t: (0, 0, 1, 1 - ease(seg(t, 2, 2.6))))
    s.over(lambda t, fr: ImageDraw.Draw(fr).text((640, 360), "07:59" if t < 1.2 else "08:00", font=font("card", 160), fill=(*IVORY, int(255 * (1 - seg(t, 2, 2.6)))), anchor="mm"))
    s.cam = lambda t: (lerp(1.4, 1.0, ease_out(seg(t, 2, 3))), WW / 2, WH / 2)
    return s


def SH_046():
    s = SH_003()
    s.sid, s.dur = "SH-046", DUR["SH-046"]
    return s


def SH_047():
    s = S("SH-047")
    g = textured(vgrad((WW, WH), (14, 16, 20), (6, 8, 10)), 4, 47)
    d = ImageDraw.Draw(g)
    d.polygon([(600, 300), (1320, 300), (1700, 1080), (220, 1080)], fill=(24, 26, 30, 255))
    d.rectangle([660, 260, 1260, 560], fill=(40, 30, 24, 255))
    g.alpha_composite(truck(520), (700, 300))
    s.add(g)
    s.over(lambda t, fr: fr.alpha_composite(radial((W, H), (640, 260), 420, (255, 120, 40), 0.55 + 0.2 * math.sin(t * 11))))
    s.over(lambda t, fr: fr.alpha_composite(radial((W, H), (120, 120), 300, (60, 110, 255), 0.5 * (math.sin(t * 8) > 0))))
    s.over(smoke(47, (300, 120, 1000, 340), n=12, speed=10))
    s.cam = push(1.0, 1.1, dur=s.dur)
    return s


def SH_048():
    s = S("SH-048")
    s.add(map_base([(200, 900), (260, 260), (1700, 220), (1760, 960)], land=(52, 62, 70), label="stylised overview"))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        pin(d, 380, 420, (90, 130, 220), label="police station", fs=28)
        if t > 1.5:
            pin(d, 860, 300, OXIDE, label="NOKAS", fs=30)
    s.over(fn)
    s.cam = push(1.0, 1.9, WW / 2, WH / 2, 1290, 450, dur=s.dur)
    return s


def SH_049():
    s = S("SH-049")
    s.add(set_glass_window())
    fig = rgba((WW, WH)); person(ImageDraw.Draw(fig), 700, 1300, 900, (8, 9, 11), mask=True); s.add(fig, 1.2)
    lines = crack_lines(49, 640, 360, n=10)
    s.over(lambda t, fr: draw_cracks(ImageDraw.Draw(fr), lines, seg(t, 5.0, 7.0)))
    s.cam = push(1.0, 1.25, dur=s.dur)
    return s


# ===================================================================== CH 4b · INSIDE THE COUNTING ROOM
def room_shot(sid, figs=(), masked=(), cam=(1.0, 1.1)):
    s = S(sid)
    s.add(set_counting_room(), 0.8)
    L = rgba((WW, WH)); d = ImageDraw.Draw(L)
    for (x, h) in figs:
        person(d, x, 980, h, (44, 34, 26))
    for (x, h) in masked:
        person(d, x, 1060, h, (8, 9, 11), mask=True)
    s.add(L, 1.0)
    s.cam = push(cam[0], cam[1], dur=s.dur)
    return s


def SH_053():
    s = room_shot("SH-053", figs=[(1300, 520), (1560, 480)], masked=[(500, 700)])
    lines = crack_lines(53, 330, 300, n=8, length=(160, 300))
    s.over(lambda t, fr: draw_cracks(ImageDraw.Draw(fr), lines, 1.0, alpha=140))
    return s


def SH_054():
    s = room_shot("SH-054", figs=[(500, 560), (960, 600), (1400, 540)], cam=(1.05, 1.15))
    return s


def SH_055():
    s = room_shot("SH-055", figs=[(1400, 480)], masked=[(420, 900)])

    def bags(t, frame):
        d = ImageDraw.Draw(frame)
        for k in range(int(seg(t, 1, 7) * 6)):
            d.rounded_rectangle([600 + k * 80, 470, 670 + k * 80, 540], radius=14, fill=(110, 110, 106, 255))
    s.over(bags)
    return s


def SH_056():
    s = S("SH-056")
    s.add(textured(vgrad((WW, WH), (30, 26, 22), (14, 12, 10)), 4, 56))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        for k in range(10):
            x = lerp(-120, 1400, seg(t - k * 0.35, 0, 4))
            d.rounded_rectangle([x, 380 + (k % 3) * 40, x + 90, 450 + (k % 3) * 40], radius=16, fill=(120, 118, 112, 255))
    s.over(fn)
    s.over(counter(0, 57, 3.5, 7.5, lambda v: f"{int(v)} MILLION NOK+", (640, 220), 96, AMBER))
    return s


def SH_057():
    s = S("SH-057")
    s.add(textured(rgba((WW, WH), (12, 12, 14, 255)), 3, 57))
    s.over(screen_text("OVER 57 MILLION NOK", "card", 110, IVORY, (640, 330), 0.3, 1.2))
    s.over(screen_text("at the time, the largest robbery in Norwegian history", "serif", 38, (190, 192, 190), (640, 450), 1.5, 2.5))
    return s


def SH_058():
    s = S("SH-058")
    s.add(set_stavanger_far(), 0.4).add(set_glass_window(), 1.0, lambda t: (0, 0, 1, 0.55))
    s.over(smoke(58, (0, 200, 1280, 600), n=16, speed=14, col=(110, 112, 116)))
    s.cam = push(1.25, 1.0, dur=s.dur)
    return s


def SH_059():
    s = S("SH-059")
    s.add(map_base([(200, 900), (260, 260), (1700, 220), (1760, 960)], land=(52, 62, 70), label="stylised overview"))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        pts = curve((300, 520), (980, 300), 0.15)
        route(d, pts, 1 - seg(t, 4, 9), OXIDE, 6)
        pin(d, 380, 420, (90, 130, 220), label="police", fs=26)
    s.over(fn)
    s.tint = (0.92, 0.94, 0.98)
    return s


# ===================================================================== CH 5 · THE OFFICER
def SH_060():
    s = S("SH-060")
    s.add(set_dawn_sky(), 0.1).add(set_police_station(), 0.7)
    s.over(smoke(60, (500, 200, 900, 500), n=14, speed=12))
    s.over(paste_fn(car(320, (34, 44, 60)), lambda t: (lerp(1300, 900, ease(seg(t, 1, 7))), 540, 1)))
    return s


@cached
def medallion():
    m = rgba((520, 620))
    d = ImageDraw.Draw(m)
    d.ellipse([20, 20, 500, 500], fill=(70, 56, 44, 255))
    person(d, 260, 560, 520, (26, 30, 36))
    d.ellipse([20, 20, 500, 500], outline=(*AMBER, 255), width=6)
    return m


def SH_061():
    s = S("SH-061")
    s.add(textured(vgrad((WW, WH), (60, 46, 36), (20, 18, 16)), 4, 61))
    s.over(paste_fn(medallion().resize((390, 465)), lambda t: (445, 70, ease(seg(t, 0, 1.2)))))
    s.over(screen_text("ARNE SIGVE KLUNGLAND", "serif", 54, IVORY, (640, 590), 1.5, 2.5))
    s.over(screen_text("police lieutenant · Stavanger police", "card_l", 28, (200, 190, 176), (640, 650), 2.2, 3))
    return s


def SH_062():
    s = S("SH-062")
    g = textured(vgrad((WW, WH), (40, 44, 50), (18, 20, 24)), 4, 62)
    g.alpha_composite(car(1500, (40, 48, 60)), (200, 260))
    s.add(g)
    s.over(paste_fn(medallion().resize((240, 286)), lambda t: (560, 170, 0.25 * ease(seg(t, 0.5, 2)))))
    return s


def SH_063():
    s = SH_062()
    s.sid, s.dur = "SH-063", DUR["SH-063"]
    s.cam = push(1.0, 2.2, WW / 2, WH / 2, 1000, 450, dur=s.dur)
    return s


def mem_shot(sid, name=True, flower_=False, big=False):
    s = S(sid)
    s.add(textured(rgba((WW, WH), (18, 16, 14, 255)), 3, 68))
    if not big:
        s.over(paste_fn(medallion().resize((300, 358)), lambda t: (490, 70, ease(seg(t, 0, 1.5)))))
    if name:
        s.over(screen_text("ARNE SIGVE KLUNGLAND", "serif", 76 if big else 48, IVORY, (640, 360 if big else 500), 0.5, 1.8))
    if flower_:
        s.over(paste_fn(flower().resize((150, 245)), lambda t: (900, lerp(380, 420, ease(seg(t, 0.5, 3))), ease(seg(t, 0.5, 2)))))
        s.over(screen_text("5 APRIL 2004", "card_l", 34, (200, 196, 188), (640, 570), 1.5, 2.5))
    s.vignette = 0.5
    return s


def SH_068():
    return mem_shot("SH-068")


def SH_069():
    return mem_shot("SH-069", flower_=True)


def SH_070():
    s = mem_shot("SH-070", big=True)
    s.fade_out = 1.5
    return s


# ===================================================================== CH 6 · INTO THE WOODS
def SH_071():
    s = S("SH-071")
    s.add(set_night_sky(), 0.1).add(set_nokas_facade(), 0.8)
    s.tint = (1.05, 0.9, 0.88)

    def vans(t, frame):
        L = rgba((W, H)); d = ImageDraw.Draw(L)
        for k in range(2):
            x = lerp(500 + k * 240, 1500 + k * 240, ease(seg(t, 1 + k * 0.6, 6)))
            d.rounded_rectangle([x, 560, x + 230, 650], radius=12, fill=(8, 10, 12, 255))
        frame.alpha_composite(L)
    s.over(vans)
    return s


def SH_072():
    s = SH_040()
    s.sid, s.dur = "SH-072", DUR["SH-072"]
    return s


def SH_073():
    s = S("SH-073")
    s.add(set_night_sky(), 0.1).add(set_forest(), 0.6, lambda t: (-30 * t, 0, 1, 1))
    s.over(lambda t, fr: fr.alpha_composite(radial((W, H), (980, 560), 220, (255, 110, 40), 0.45 + 0.15 * math.sin(t * 9))))
    s.over(smoke(73, (880, 300, 1080, 520), n=10, speed=20))

    def fn(t, frame):
        L = rgba((W, H)); d = ImageDraw.Draw(L)
        d.rounded_rectangle([380, 560, 610, 640], radius=10, fill=(8, 10, 12, int(255 * (1 - seg(t, 2, 4)))))
        d.rounded_rectangle([640, 560, 840, 640], radius=10, fill=(8, 10, 12, int(255 * seg(t, 2, 4))))
        frame.alpha_composite(L)
    s.over(fn)
    return s


def SH_074():
    s = S("SH-074")
    s.add(textured(rgba((WW, WH), (16, 20, 26, 255)), 3, 74))
    icons = [set_glass_window().resize((300, 169)), set_police_station().resize((300, 169)),
             map_base(NORWAY).resize((300, 169))]
    for k, ic in enumerate(icons):
        s.over(paste_fn(ic, (lambda k: lambda t: (130 + k * 380, 240, ease(seg(t, k * 1.5, k * 1.5 + 0.6))))(k)))
    lines = crack_lines(74, 640, 330, n=6, length=(200, 500))
    s.over(lambda t, fr: draw_cracks(ImageDraw.Draw(fr), lines, seg(t, 5, 8), alpha=200))
    return s


def SH_075():
    s = S("SH-075")
    s.add(set_board(), 0.6)
    s.over(paste_fn(medallion().resize((220, 262)), lambda t: (530, 200, 1)))
    s.over(screen_text("ARNE SIGVE KLUNGLAND", "serif", 30, IVORY, (640, 490), 0, 0.5))
    s.cam = push(1.6, 1.0, dur=s.dur)
    return s


# ===================================================================== CH 7 · THE HUNT
def board_shot(sid, n_x=0, toska=True, extra=None, cam=(1.0, 1.08)):
    s = S(sid)
    s.add(set_board(), 0.6)
    r = random.Random(7)
    pos = [(r.uniform(60, 1080), r.uniform(60, 520)) for _ in range(10)]

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        for i in range(len(pos) - 1):
            d.line([(pos[i][0] + 60, pos[i][1] + 70), (pos[i + 1][0] + 60, pos[i + 1][1] + 70)], fill=(170, 40, 40, 200), width=3)
        for k, (x, y) in enumerate(pos):
            d.rectangle([x, y, x + 120, y + 150], fill=(200, 196, 188, 255))
            person(d, x + 60, y + 150, 140, (60, 62, 66))
            if k < n_x(t) if callable(n_x) else k < n_x:
                d.line([(x, y), (x + 120, y + 150)], fill=(*OXIDE, 255), width=6)
                d.line([(x + 120, y), (x, y + 150)], fill=(*OXIDE, 255), width=6)
        if toska:
            x, y = 560, 260
            d.rectangle([x, y, x + 150, y + 190], fill=(230, 226, 216, 255))
            person(d, x + 75, y + 190, 170, (30, 30, 34))
            d.text((x + 75, y + 200), "D. TOSKA", font=font("card", 26), fill=IVORY, anchor="ma")
    s.over(fn)
    if extra:
        s.over(extra)
    s.cam = push(cam[0], cam[1], dur=s.dur)
    return s


def SH_076():
    return board_shot("SH-076", n_x=0)


def SH_077():
    s = S("SH-077")
    s.add(map_base(NORWAY, label="stylised map · locations illustrative"))
    r = random.Random(77)
    dots = [(r.uniform(450, 900) * W / WW, r.uniform(500, 980) * H / WH) for _ in range(9)]

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        for k, (x, y) in enumerate(dots):
            if t > k * 0.6:
                d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(*OXIDE, 255))
        frame.alpha_composite(stamp("ARRESTS", size=50), (820, 120)) if t > 4 else None
    s.over(fn)
    return s


def SH_078():
    s = S("SH-078")
    wall = textured(vgrad((WW, WH), (70, 66, 60), (40, 38, 34)), 4, 78)
    d = ImageDraw.Draw(wall)
    d.rectangle([700, 220, 1220, 840], outline=(150, 120, 70, 255), width=26)
    s.add(wall)

    def fn(t, frame):
        a = 1 - ease(seg(t, 2, 4))
        L = rgba((W, H)); dd = ImageDraw.Draw(L)
        dd.rectangle([485, 165, 795, 545], fill=(120, 90, 60, int(255 * a)))   # original, abstract painted motif (not the artwork)
        dd.ellipse([600, 260, 680, 360], fill=(220, 190, 140, int(255 * a)))
        frame.alpha_composite(L)
        if t > 4.5:
            ImageDraw.Draw(frame).text((640, 360), "?", font=font("serif", 160), fill=(*IVORY, 200), anchor="mm")
    s.over(fn)
    s.over(screen_text("Oslo, August 2004", "card_l", 30, IVORY, (640, 650), 0.5, 1.2))
    return s


def SH_079():
    s = board_shot("SH-079", n_x=3)
    s.over(lambda t, fr: fr.alpha_composite(stamp("UNPROVEN THEORY", size=60, rot=-6), (300, 250)) if t > 1 else None)
    return s


def SH_080():
    return board_shot("SH-080", n_x=lambda t: int(seg(t, 0.5, 5) * 10), cam=(1.0, 1.35))


def SH_081():
    s = S("SH-081")
    poly = [(x * 0.55 + 900, y * 0.5 - 20) for (x, y) in NORWAY] + []
    base = map_base([(300, 700), (700, 640), (1000, 700), (1100, 950), (400, 1000)], label="stylised, not to scale")
    ImageDraw.Draw(base).polygon(poly, fill=(48, 60, 70, 255))
    s.add(base)

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        a, b = (1110 * W / WW, 420 * H / WH), (520 * W / WW, 880 * H / WH)
        route(d, curve(a, b, 0.25), ease(seg(t, 0.5, 5)), IVORY, 4, dash=True)
        pin(d, *a, label="Norway", fs=26)
        if t > 5:
            pin(d, *b, label="southern Spain", fs=26)
    s.over(fn)
    return s


def SH_082():
    s = S("SH-082")
    s.add(map_base(SPAIN, land=(78, 70, 58), sea=(26, 40, 52), label="Costa del Sol · stylised"))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        x, y = 700 * W / WW, 820 * H / WH
        pin(d, x, y, SUN, label="Málaga", fs=30)
        for k in range(3):
            tt = t - k * 2
            if tt > 0:
                r = 20 + tt * 60
                d.ellipse([x - r, y - r, x + r, y + r], outline=(*SUN, max(0, int(220 - tt * 60))), width=4)
        d.rectangle([x - 40, y - 140, x + 40, y - 90], outline=(*IVORY, 255), width=4)
        d.line([(x - 40, y - 140), (x, y - 112), (x + 40, y - 140)], fill=(*IVORY, 255), width=4)
    s.over(fn)
    s.tint = (1.05, 1.0, 0.92)
    return s


def SH_087():
    s = S("SH-087")
    s.add(textured(rgba((WW, WH), (14, 14, 16, 255)), 3, 87))
    c = rgba((760, 420)); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, 760, 420], fill=(225, 222, 214, 255))
    d.rectangle([30, 40, 280, 380], fill=(60, 62, 66, 255)); person(d, 155, 380, 330, (24, 26, 28))
    d.text((310, 60), "DAVID TOSKA", font=font("card", 54), fill=NAVY)
    d.text((310, 150), "ARRESTED — MÁLAGA", font=font("card_l", 36), fill=NAVY)
    d.text((310, 210), "5 APRIL 2005", font=font("card_l", 36), fill=OXIDE)
    d.text((310, 330), "illustrative card · not a police record", font=font("card_l", 22), fill=(110, 110, 106))
    s.over(paste_fn(c, lambda t: (260, 150, ease(seg(t, 0, 0.8)))))
    return s


def SH_088():
    s = S("SH-088")
    s.add(textured(rgba((WW, WH), (14, 14, 16, 255)), 3, 88))
    a = card(360, 280, "2004", "05 APR", fs=46, bfs=86); b = card(360, 280, "2005", "05 APR", fs=46, bfs=86)
    s.over(paste_fn(a, lambda t: (lerp(120, 270, ease(seg(t, 0.5, 3))), 200, 1)))
    s.over(paste_fn(b, lambda t: (lerp(800, 650, ease(seg(t, 0.5, 3))), 200, 1)))
    s.over(screen_text("one year to the day", "serif", 44, AMBER, (640, 560), 2.5, 3.5))
    return s


# ===================================================================== CH 8 · THE VERDICT
def court_shot(sid, highlight=None, dim=False, extra=None, cam=(1.0, 1.06)):
    s = S(sid)
    s.add(set_courtroom(), 0.6).add(courtroom_defendants(13, highlight, dim), 1.0)
    if extra:
        s.over(extra)
    s.cam = push(cam[0], cam[1], dur=s.dur)
    return s


def SH_089():
    return court_shot("SH-089", extra=screen_text("STAVANGER DISTRICT COURT · 10 MARCH 2006", "card", 40, IVORY, (640, 70), 1, 2))


def SH_090():
    s = court_shot("SH-090", dim=True)
    s.over(counter(0, 181, 0.5, 5, lambda v: f"{int(v)} YEARS", (640, 260), 140, IVORY))
    s.over(screen_text("13 men · combined sentences", "card_l", 34, (190, 190, 186), (640, 380), 3, 4))
    return s


def doc_shot(sid, lines):
    s = S(sid)
    s.add(set_desk(), 0.4)
    pg = textured(Image.new("RGBA", (1100, 900), (*IVORY, 255)), 5, 9, 2)
    d = ImageDraw.Draw(pg)
    for i in range(14):
        d.line([(90, 260 + i * 42), (1010, 260 + i * 42)], fill=(180, 178, 170, 255), width=8)
    s.add(place(shadowed(pg), 410, 120), 1.0)
    for k, (txt, a, col) in enumerate(lines):
        s.over(screen_text(txt, "card", 46, col, (640, 220 + k * 90), a, a + 0.6))
    s.cam = push(1.0, 1.12, dur=s.dur)
    return s


def SH_091():
    return doc_shot("SH-091", [("DAVID TOSKA", 0.3, NAVY), ("ADMITTED THE ROBBERY", 1.5, NAVY)])


def SH_092():
    return doc_shot("SH-092", [("DAVID TOSKA", 0, NAVY), ("ADMITTED THE ROBBERY", 0, NAVY), ("DENIED FIRING THE FATAL SHOT", 1.2, OXIDE)])


def SH_093():
    s = court_shot("SH-093", dim=True)
    s.over(lambda t, fr: fr.alpha_composite(card(300, 230, "2006", ["MAR", "MAY", "JUL", "SEP"][min(3, int(seg(t, 0.5, 5) * 4))], fs=40, bfs=96), (490, 160)))
    s.over(screen_text("GULATING COURT OF APPEAL", "card", 40, IVORY, (640, 440), 5, 6))
    return s


def SH_094():
    return court_shot("SH-094", highlight=6, dim=True, cam=(1.0, 1.3))


def SH_095():
    s = S("SH-095")
    s.add(textured(rgba((WW, WH), (14, 14, 16, 255)), 3, 95))
    s.over(paste_fn(name_card("KJELL ALRICH SCHUMANN", "admitted firing the fatal shots (appeal, 2006)", OXIDE, 820), lambda t: (60, 160, ease(seg(t, 0.3, 1.2)))))
    s.over(paste_fn(medallion().resize((220, 262)), lambda t: (980, 360, ease(seg(t, 2.5, 3.5)))))
    s.over(screen_text("ARNE SIGVE KLUNGLAND", "serif", 30, IVORY, (1090, 650), 3, 4))
    return s


# ===================================================================== EPILOGUE
def SH_096():
    s = S("SH-096")
    s.add(set_glass_window())
    s.over(screen_text("57 MILLION NOK", "card", 90, AMBER, (640, 330), 1.0, 2.0))
    s.cam = push(1.15, 1.0, dur=s.dur)
    return s


def SH_097():
    s = S("SH-097")
    s.add(set_glass_window(), 1.0, lambda t: (0, 0, 1, 0.5))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        p = ease(seg(t, 0.5, 3))
        d.rectangle([340, 240, 340 + 600 * 6 / 57, 320], fill=(*IVORY, 255))
        d.rectangle([340 + 600 * 6 / 57 + 8 * p, 240, 940 + 8 * p, 320], fill=(*AMBER, int(255 * (1 - 0.5 * p))))
        d.text((340, 340), "≈ 6 M accounted for", font=font("card", 34), fill=IVORY)
        d.text((940, 340), "≈ 50 M never found", font=font("card", 34), fill=AMBER, anchor="ra")
    s.over(fn)
    s.over(screen_text("figures as reported; status may change", "card_l", 22, (160, 160, 156), (640, 660), 2, 3))
    return s


def SH_098():
    s = S("SH-098")
    s.add(textured(rgba((WW, WH), (16, 18, 22, 255)), 3, 98))

    def fn(t, frame):
        d = ImageDraw.Draw(frame)
        d.line([(640, 120), (640, 600)], fill=(*IVORY, 120), width=2)
        d.text((330, 160), "the plan", font=font("card", 44), fill=IVORY, anchor="mm")
        d.text((950, 160), "the robbery", font=font("card", 44), fill=IVORY, anchor="mm")
        m = int(seg(t, 0.2, 4) * 14)
        d.text((330, 360), f"{m} months", font=font("card", 90), fill=AMBER, anchor="mm")
        d.text((950, 360), f"{int(seg(t, 0.2, 2) * 20)} minutes", font=font("card", 90), fill=OXIDE, anchor="mm")
        d.text((330, 450), "(more than a year – to be verified)", font=font("card_l", 22), fill=(150, 150, 146), anchor="mm")
    s.over(fn)
    return s


def SH_099():
    s = S("SH-099")
    s.add(set_glass_window())
    st31 = ROOT / "05_BLENDER/renders/SH-031_ref_frame_0168.png"
    if st31.exists():
        img = Image.open(st31).convert("RGBA").resize((560, 315))
        img.putalpha(110)
        s.over(paste_fn(img, lambda t: (100, 120, 1 - seg(t, 2.4, 2.8))))
    lines = crack_lines(99, 640, 360, n=9)
    s.over(lambda t, fr: draw_cracks(ImageDraw.Draw(fr), lines, seg(t, 2.6, 4.2), alpha=160))
    return s


def SH_100():
    s = room_shot("SH-100", cam=(1.0, 1.05))
    s.layers.append(Layer(rgba((WW, WH), (0, 0, 0, 255)), 1.0, lambda t: (0, 0, 1, ease(seg(t, 1, 5)))))
    return s


def SH_101():
    s = S("SH-101")
    s.add(set_glass_window())
    s.over(screen_text("50 M", "card", 120, AMBER, (640, 340), 0, 0.5, end=(2.5, 5.5)))
    return s


def SH_102():
    s = stavanger_wide("SH-102", 1.0, 1.08, 3)
    s.layers[0] = Layer(set_dawn_sky(), 0.1)
    s.over(screen_text("In memory of\nArne Sigve Klungland", "serif", 54, IVORY, (640, 330), 5.5, 7))
    s.add(rgba((WW, WH), (0, 0, 0, 255)), 1.0, lambda t: (0, 0, 1, ease(seg(t, 4.5, 6.5)) * 0.85))
    s.fade_out = 2.5
    return s


BUILDERS = {k.replace("_", "-"): v for k, v in dict(globals()).items() if k.startswith("SH_") and callable(v)}


def build(sid):
    return BUILDERS[sid]()


def _job(args):
    sid, out, preview = args
    s = build(sid)
    if preview:
        n = int(s.dur * FPS)
        render_shot(s, out, preview_frames=[0, n // 2, n - 1])
    else:
        render_shot(s, os.path.join(out, f"{sid}_2D_v001.mp4"))
    return sid


if __name__ == "__main__":
    from multiprocessing import Pool
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    ids = [x for x in a.only.split(",") if x] or sorted(BUILDERS)
    missing = [sid for sid in sorted(DUR) if TYPE[sid] == "2D" and sid not in BUILDERS and sid not in ("SH-028", "SH-029", "SH-030")]
    if missing:
        print("NO BUILDER:", missing)
    with Pool(a.jobs) as pool:
        for sid in pool.imap_unordered(_job, [(i, a.out, a.preview) for i in ids]):
            print("done", sid, flush=True)
