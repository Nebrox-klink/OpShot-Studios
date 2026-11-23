"""Channel logo options v001 (drawn in code, no AI generation). Usage: python3 -I make_logos.py OUT_DIR"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(HERE, "../../DB_COOPER/09_DELIVERABLES/tools/fonts/Anton-Regular.ttf")
INTER = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
S = 3; N = 800 * S  # supersample
NAVY, INK, RED, YEL, CREAM, CORK = (14, 20, 32), (8, 10, 14), (214, 38, 32), (255, 212, 0), (236, 226, 204), (150, 104, 62)
F = lambda p, s: ImageFont.truetype(p, s * S)

def canvas(bg):
    return Image.new("RGB", (N, N), bg)

def pin(d, x, y, r=46, c=RED):
    r *= S
    d.ellipse((x - r + 10 * S, y - r + 14 * S, x + r + 10 * S, y + r + 14 * S), fill=(0, 0, 0))
    d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    d.ellipse((x - r * .45, y - r * .55, x - r * .05, y - r * .15), fill=(255, 140, 130))

def ctext(d, y, text, f, fill, track=0):
    w = d.textlength(text, font=f) + track * (len(text) - 1)
    x = (N - w) / 2
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track

def eye(d, cx, cy, w, h, width, col):
    # almond eye from two arcs
    pts = []
    for sgn in (1, -1):
        for i in range(0, 101):
            t = -1 + 2 * i / 100
            pts.append((cx + t * w / 2, cy - sgn * h / 2 * (1 - t * t)))
    d.line(pts[:101] + pts[101:][::-1][1:] + [pts[0]], fill=col, width=width, joint="curve")

def a_spectare_eye():
    im = canvas(NAVY); d = ImageDraw.Draw(im); c = N // 2
    eye(d, c, c - 40 * S, 600 * S, 330 * S, 34 * S, CREAM)
    r = 120 * S; d.ellipse((c - r, c - 40 * S - r, c + r, c - 40 * S + r), outline=CREAM, width=30 * S)
    pin(d, c, c - 40 * S, 58)
    ctext(d, c + 170 * S, "SPECTARE", F(ANTON, 118), CREAM, track=10 * S)
    return im

def b_spectare_monogram():
    im = canvas(YEL); d = ImageDraw.Draw(im); c = N // 2
    f = F(ANTON, 640); l, t, r, b = d.textbbox((0, 0), "S", font=f)
    d.text((c - (l + r) / 2, c - (t + b) / 2), "S", font=f, fill=INK)
    pin(d, c + 150 * S, c - 210 * S, 54)
    return im

def c_red_string():
    im = canvas((22, 24, 28)); d = ImageDraw.Draw(im)
    pts = [(240, 190), (560, 250), (320, 500), (585, 480)]
    pts = [(x * S, y * S) for x, y in pts]
    for a, b in [(0, 1), (1, 2), (2, 3), (0, 2)]:
        d.line([pts[a], pts[b]], fill=RED, width=16 * S)
    for p in pts: pin(d, *p, 44, CREAM if p == pts[3] else RED)
    ctext(d, 565 * S, "RED STRING", F(ANTON, 84), CREAM, track=8 * S)
    return im

def d_case_board():
    im = canvas(CORK); d = ImageDraw.Draw(im)
    # subtle cork speckle
    import random; random.seed(4)
    for _ in range(9000):
        x, y = random.randrange(N), random.randrange(N); s = random.choice((2, 3, 4)) * S
        d.ellipse((x, y, x + s, y + s), fill=random.choice(((120, 80, 45), (175, 128, 82))))
    # manila folder
    x0, y0, x1, y1 = 150 * S, 250 * S, 650 * S, 600 * S
    d.rectangle((x0 + 14 * S, y0 + 18 * S, x1 + 14 * S, y1 + 18 * S), fill=(0, 0, 0))
    d.polygon([(x0, y0), (x0, y0 - 60 * S), (x0 + 200 * S, y0 - 60 * S), (x0 + 240 * S, y0)], fill=(222, 190, 120))
    d.rectangle((x0, y0, x1, y1), fill=(232, 204, 140))
    f = F(ANTON, 150); w = d.textlength("CASE", font=f)
    d.text(((N - w) / 2, y0 + 40 * S), "CASE", font=f, fill=INK)
    d.rectangle((x0 + 60 * S, y0 + 245 * S, x1 - 60 * S, y0 + 315 * S), fill=RED)
    ctext(d, y0 + 247 * S, "BOARD", F(ANTON, 54), (255, 255, 255), track=18 * S)
    pin(d, N // 2, y0 - 10 * S, 40)
    return im

DESIGNS = [("L1_spectare_eye", "Spectare", a_spectare_eye), ("L2_spectare_monogram", "Spectare (monogram)", b_spectare_monogram),
           ("L3_red_string", "Red String", c_red_string), ("L4_case_board", "The Case Board", d_case_board)]

tiles = []
for name, label, fn in DESIGNS:
    im = fn().resize((800, 800), Image.LANCZOS); im.save(os.path.join(OUT, name + ".png")); tiles.append((label, im))

# contact sheet: each logo as YouTube shows it (circle) at 400 px and at 48 px
sheet = Image.new("RGB", (len(tiles) * 440 + 40, 640), (245, 245, 245)); sd = ImageDraw.Draw(sheet)
mask = Image.new("L", (400, 400), 0); ImageDraw.Draw(mask).ellipse((0, 0, 399, 399), fill=255)
for i, (label, im) in enumerate(tiles):
    x = 40 + i * 440
    sheet.paste(im.resize((400, 400), Image.LANCZOS), (x, 40), mask)
    m48 = mask.resize((48, 48), Image.LANCZOS); sheet.paste(im.resize((48, 48), Image.LANCZOS), (x, 480), m48)
    sheet.paste(im.resize((88, 88), Image.LANCZOS), (x + 70, 460), mask.resize((88, 88), Image.LANCZOS))
    sd.text((x, 575), label, font=ImageFont.truetype(INTER, 30), fill=(20, 20, 20))
sheet.save(os.path.join(OUT, "logo_options_v001_sheet.jpg"), quality=90)
print("ok")
