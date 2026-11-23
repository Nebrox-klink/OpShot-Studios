"""D.B. Cooper thumbnails, style v003 ("case file"), built from a study of the niche's top outliers (23 Nov 2026).

What the high-performing D.B. Cooper / unsolved-mystery thumbnails share, and what this style takes from them:
  - the name "D.B. COOPER" (or "THE D.B. COOPER CASE") is on the thumbnail;
  - heavy condensed type (Anton, OFL), white with a thick black outline, readable at mobile size;
  - one key phrase on a solid highlight box (yellow with black text), plus a red tag/label;
  - a red arrow and/or red circle pointing at the clue in the picture;
  - punchy, high-contrast picture, darker edges.
Kept from our own rules: no faces, no fake "breaking news" banners, every claim is a fact from the film.

Usage: python3 -I make_thumbnails_v3.py DB_COOPER_ROOT OUT_DIR [NAME,NAME...]
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
ONLY = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
os.makedirs(OUT, exist_ok=True)
STILLS = os.path.join(ROOT, "02_VISUAL/shot_list_v001/stills")
REFS = os.path.join(ROOT, "02_VISUAL/style_refs_v001/png")
ANTON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts/Anton-Regular.ttf")
W, H = 1280, 720
WHITE, BLACK, RED, YELLOW = (255, 255, 255), (0, 0, 0), (214, 38, 32), (255, 212, 0)


def font(size):
    return ImageFont.truetype(ANTON, size)


def picture(name):
    p = os.path.join(STILLS, name)
    im = Image.open(p if os.path.isfile(p) else os.path.join(REFS, name)).convert("RGB")
    w, h = im.size
    ch = int(w * 9 / 16)
    if ch > h:
        cw = int(h * 16 / 9)
        im = im.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h))
    else:
        im = im.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch))
    im = im.resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.28)
    im = ImageEnhance.Color(im).enhance(1.22)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse((-W * 0.2, -H * 0.3, W * 1.2, H * 1.3), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(110))
    return Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), vig.point(lambda v: int(95 + v * 160 / 255)))


def shade(im, box, strength=170):
    """Soft dark patch behind a text area so white type always reads."""
    m = Image.new("L", (W, H), 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(m).rounded_rectangle((x0, y0, x1, y1), radius=60, fill=strength)
    m = m.filter(ImageFilter.GaussianBlur(60))
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, m)


def outlined(d, xy, text, size, fill=WHITE, stroke=None):
    f = font(size)
    sw = stroke if stroke is not None else max(6, size // 14)
    x, y = xy
    d.text((x + sw // 2 + 4, y + sw // 2 + 6), text, font=f, fill=(0, 0, 0), stroke_width=sw, stroke_fill=(0, 0, 0))
    d.text((x, y), text, font=f, fill=fill, stroke_width=sw, stroke_fill=BLACK)
    return d.textbbox((x, y), text, font=f, stroke_width=sw)


def boxed(d, xy, text, size, bg=YELLOW, fg=BLACK, pad=(18, 8), tilt=0):
    f = font(size)
    x, y = xy
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    w, h = r - l, b - t
    d.rectangle((x + 6, y + 8, x + w + 2 * pad[0] + 6, y + h + 2 * pad[1] + 8), fill=(0, 0, 0))  # hard shadow
    d.rectangle((x, y, x + w + 2 * pad[0], y + h + 2 * pad[1]), fill=bg)
    d.text((x + pad[0] - l, y + pad[1] - t), text, font=f, fill=fg)
    return (x, y, x + w + 2 * pad[0], y + h + 2 * pad[1])


def tag(d, xy, text, size=44):
    return boxed(d, xy, text, size, bg=RED, fg=WHITE, pad=(16, 8))


def arrow(d, start, end, width=22, head=62):
    (x0, y0), (x1, y1) = start, end
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - head * math.cos(ang), y1 - head * math.sin(ang)
    px, py = -math.sin(ang), math.cos(ang)
    shaft = [(x0 + px * width / 2, y0 + py * width / 2), (bx + px * width / 2, by + py * width / 2),
             (bx - px * width / 2, by - py * width / 2), (x0 - px * width / 2, y0 - py * width / 2)]
    tip = [(x1, y1), (bx + px * head * 0.62, by + py * head * 0.62), (bx - px * head * 0.62, by - py * head * 0.62)]
    for poly in (shaft, tip):
        d.polygon(poly, fill=RED, outline=BLACK, width=6)
    d.polygon(shaft, fill=RED)
    d.polygon(tip, fill=RED)


def ring(d, box, width=12):
    d.ellipse(box, outline=BLACK, width=width + 8)
    d.ellipse(box, outline=RED, width=width)


def t6(im):  # the open rear door: where he jumped
    im = shade(im, (0, 120, 640, 700))
    d = ImageDraw.Draw(im)
    tag(d, (44, 40), "THE D.B. COOPER CASE")
    outlined(d, (44, 150), "HE JUMPED", 136)
    boxed(d, (48, 345), "FROM HERE", 104)
    ring(d, (668, 255, 822, 505))
    arrow(d, (480, 560), (664, 455))
    return im


def t7(im):  # the money in the sand
    im = shade(im, (0, 0, 1280, 260), 150)
    im = shade(im, (0, 560, 900, 720), 170)
    d = ImageDraw.Draw(im)
    tag(d, (44, 34), "THE D.B. COOPER CASE")
    outlined(d, (44, 100), "$5,800 FOUND IN THE SAND", 104)
    ring(d, (120, 250, 1070, 640), width=12)
    boxed(d, (44, 588), "WHERE'S THE REST?", 82)
    return im


def t8(im):  # the empty outline on the case board
    im = shade(im, (620, 60, 1280, 640))
    d = ImageDraw.Draw(im)
    tag(d, (680, 60), "UNSOLVED SINCE 1971")
    outlined(d, (680, 160), "WHO WAS", 138)
    boxed(d, (684, 360), "D.B. COOPER?", 104)
    ring(d, (350, 225, 520, 410))
    arrow(d, (690, 540), (528, 370))
    return im


def t9(im):  # the 727 at night, stairs down
    im = shade(im, (0, 0, 700, 330), 160)
    im = shade(im, (0, 440, 860, 720), 190)
    d = ImageDraw.Draw(im)
    outlined(d, (40, 26), "D.B. COOPER", 170)
    outlined(d, (44, 470), "HE JUMPED.", 112)
    boxed(d, (48, 610), "NEVER FOUND.", 70)
    ring(d, (720, 330, 870, 470), width=10)
    arrow(d, (560, 520), (715, 430), width=18, head=54)
    return im


DESIGNS = [("T6_jumped_from_here", "SH_102.png", t6), ("T7_5800_in_the_sand", "SH_1303.png", t7),
           ("T8_who_was_db_cooper", "SH_2001.png", t8), ("T9_jumped_never_found", "BG3_727_night.png", t9)]

for name, still, fn in DESIGNS:
    if ONLY and name not in ONLY:
        continue
    im = fn(picture(still))
    p = os.path.join(OUT, name + ".jpg")
    im.save(p, quality=90, optimize=True)
    print(p, f"{os.path.getsize(p) // 1024} KB")
