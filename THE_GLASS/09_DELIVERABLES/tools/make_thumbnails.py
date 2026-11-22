"""YouTube thumbnails (1280x720, JPEG < 2 MB) from approved stills: graded image + gradient + bold type.

Usage: python3 -I make_thumbnails.py THE_GLASS_ROOT OUT_DIR [NAME,NAME...]
All hooks are facts stated in the film. Keep the bottom-right corner clear (YouTube's duration badge).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
os.makedirs(OUT, exist_ok=True)
STILLS = os.path.join(ROOT, "02_VISUAL_DEVELOPMENT/shot_stills_v001/stills")
FONTS = "/usr/share/fonts/opentype/inter/"
BLACK = FONTS + "InterDisplay-Black.otf"
XBOLD = FONTS + "InterDisplay-ExtraBold.otf"
W, H = 1280, 720
AMBER, WHITE, RED = (242, 177, 52), (255, 255, 255), (214, 48, 39)

# name, still, crop focus (x, y as 0-1), zoom, kicker, headline lines [(text, colour)], text side, sub line
DESIGNS = [
    ("T1_113_shots", "SH_1302.png", (0.5, 0.5), 1.15, "THE NOKAS ROBBERY",
     [("113", AMBER, 1.55), ("SHOTS.", WHITE, 1.0), ("IT HELD.", WHITE, 1.0)], "left", None),
    ("T2_15_seconds", "SH_102.png", (0.36, 0.55), 1.38, "STAVANGER · 5 APRIL 2004",
     [("15", AMBER, 1.9), ("SECONDS", WHITE, 1.0), ("THAT WAS THE PLAN.", WHITE, 0.42)], "left", None),
    ("T3_never_locked", "SH_2002.png", (0.55, 0.5), 1.1, "THE NOKAS ROBBERY",
     [("IT WAS", WHITE, 1.0), ("NEVER", AMBER, 1.0), ("LOCKED", WHITE, 1.0)], "left", None),
    ("T4_title_square", "SH_1404.png", (0.6, 0.45), 1.0, "STAVANGER · 5 APRIL 2004",
     [("THE NOKAS", WHITE, 1.0), ("ROBBERY", AMBER, 1.0)], "bottom", "An animated documentary"),
    ("T5_wouldnt_break", "SH_2401.png", (0.62, 0.55), 1.25, "THE NOKAS ROBBERY",
     [("THE GLASS", WHITE, 1.0), ("THAT WOULDN'T", WHITE, 1.0), ("BREAK", AMBER, 1.45)], "left", None),
    # v002: chase thumbnails, to pair with the title "Police Slowed Logins Across Europe to Catch One Fugitive"
    ("T6_stayed_online", "SH_22042.png", (0.3, 0.5), 1.3, "THE NOKAS ROBBERY",
     [("HE STAYED", WHITE, 1.0), ("ONLINE", AMBER, 1.25), ("TOO LONG.", WHITE, 1.0)], "left", None),
    ("T6b_stayed_online_desk", "SH_2203.png", (0.3, 0.5), 1.2, "THE NOKAS ROBBERY",
     [("HE STAYED", WHITE, 1.0), ("ONLINE", AMBER, 1.25), ("TOO LONG.", WHITE, 1.0)], "left", None),
    # v003: robbery-focused (the morning itself, not the arrest)
    ("T7_11_men_1_window", "SH_1301.png", (0.2, 0.45), 1.4, "STAVANGER · 5 APRIL 2004",
     [("11 MEN.", WHITE, 1.0), ("1 WINDOW.", AMBER, 1.0), ("113 SHOTS.", WHITE, 1.0)], "left", None),
    ("T8_8_minutes", "SH_1503.png", (0.15, 0.5), 1.45, "THE NOKAS ROBBERY",
     [("THE PLAN:", WHITE, 0.6), ("8 MINUTES.", AMBER, 1.0), ("IT TOOK NEARLY 20.", WHITE, 0.55)], "left", None),
    ("T9_60_million_saved", "SH_1401.png", (0.25, 0.5), 1.25, "THE NOKAS ROBBERY",
     [("3 WOMEN", WHITE, 1.0), ("SAVED", WHITE, 1.0), ("60 MILLION", AMBER, 1.0)], "left", None),
]
FLIP = {"T9_60_million_saved"}  # mirrored so the trolleys sit clear of the text (image has no lettering)
ONLY = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None  # optional: comma-separated design names


def base(still, focus, zoom):
    im = Image.open(os.path.join(STILLS, still)).convert("RGB")
    sw, sh = im.size
    cw, ch = int(sw / zoom), int(sw / zoom * H / W)
    ch = min(ch, sh)
    cw = int(ch * W / H)
    x = int(max(0, min(sw - cw, focus[0] * sw - cw / 2)))
    y = int(max(0, min(sh - ch, focus[1] * sh - ch / 2)))
    im = im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(1.1)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def shade(im, side):
    """Dark gradient behind the text plus a soft vignette."""
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    if side == "left":
        for i in range(W):
            d.line([(i, 0), (i, H)], fill=int(max(0, 240 * (1 - i / (W * 0.72)))))
    else:
        for j in range(H):
            d.line([(0, j), (W, j)], fill=int(min(255, max(0, 255 * ((j - H * 0.30) / (H * 0.55))))))
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse((-W * 0.25, -H * 0.35, W * 1.25, H * 1.35), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGB", (W, H), (5, 6, 9))
    im = Image.composite(dark, im, g.point(lambda v: int(v * 0.92)))
    return Image.composite(im, dark, vig.point(lambda v: int(80 + v * 175 / 255)))


def text_block(im, kicker, lines, side, sub):
    d = ImageDraw.Draw(im)
    fk = ImageFont.truetype(XBOLD, 26)
    maxw = 700 if side == "left" else 1100
    size = 160

    def widest(sz):
        return max(d.textlength(t, font=ImageFont.truetype(BLACK, max(10, int(sz * k)))) for t, _, k in lines)
    while widest(size) > maxw and size > 60:
        size -= 4
    sizes = [max(10, int(size * k)) for _, _, k in lines]
    heights = [int(z * 0.98) for z in sizes]
    block = 46 + sum(heights) + (50 if sub else 0)
    x = 64
    y = (H - block) // 2 if side == "left" else H - block - 60
    d.text((x, y), " ".join(kicker), font=fk, fill=AMBER)  # tracked caps kicker
    y += 46
    for (t, col, _), z, h in zip(lines, sizes, heights):
        f = ImageFont.truetype(BLACK, z)
        sh = max(2, z // 30)
        d.text((x + sh, y + sh + 1), t, font=f, fill=(0, 0, 0))
        d.text((x, y), t, font=f, fill=col)
        y += h
    if sub:
        d.text((x + 2, y + 8), sub, font=ImageFont.truetype(XBOLD, 34), fill=(225, 225, 230))
    return im


for name, still, focus, zoom, kicker, lines, side, sub in DESIGNS:
    if ONLY and name not in ONLY:
        continue
    im = base(still, focus, zoom)
    if name in FLIP:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = shade(im, side)
    im = text_block(im, kicker, lines, side, sub)
    p = os.path.join(OUT, name + ".jpg")
    im.save(p, quality=90, optimize=True)
    print(p, os.path.getsize(p) // 1024, "KB")
