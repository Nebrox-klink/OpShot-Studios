"""Spectare YouTube banner v002: an animation channel. Film-strip frames from our own film, logo L2, subscribe button.
Drawn in code, no AI generation. 2560x1440; logo, name, tagline and button sit in the 1546x423 safe area.
Usage: python3 -I make_banner.py OUT_DIR"""
import os, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "../..")
ANTON = os.path.join(ROOT, "DB_COOPER/09_DELIVERABLES/tools/fonts/Anton-Regular.ttf")
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
STILLS = os.path.join(ROOT, "DB_COOPER/02_VISUAL/shot_list_v001/stills")
LOGO = os.path.join(ROOT, "BRANDING/logo_v001/L2_spectare_monogram.png")
W, H = 2560, 1440
SX0, SY0, SX1, SY1 = (W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2
INK, RED, YEL, CREAM, FILM = (12, 14, 20), (214, 38, 32), (255, 212, 0), (240, 232, 214), (24, 24, 26)
FRAMES = ["SH_102.png", "SH_1303.png", "SH_1902.png", "SH_601.png", "SH_2001.png", "SH_1601.png", "SH_401.png", "SH_1101.png"]

# background: dark with a warm yellow glow behind the centre
im = Image.new("RGB", (W, H), INK)
glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse((W * .28, H * .30, W * .72, H * .70), fill=255)
glow = glow.filter(ImageFilter.GaussianBlur(220)).point(lambda v: int(v * .30))
im = Image.composite(Image.new("RGB", (W, H), (70, 56, 10)), im, glow)

def frame(name, fw, fh):
    p = Image.open(os.path.join(STILLS, name)).convert("RGB")
    w, h = p.size; ch = int(w * fh / fw)
    p = p.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch)) if ch <= h else p.crop(((w - int(h * fw / fh)) // 2, 0, (w + int(h * fw / fh)) // 2, h))
    p = ImageEnhance.Contrast(p.resize((fw, fh), Image.LANCZOS)).enhance(1.15)
    return ImageEnhance.Color(p).enhance(1.15)

def strip(names, fw=300, fh=200, gap=26, holes=True):
    """A horizontal film strip with sprocket holes and the given frames."""
    pad = 46; sw = len(names) * (fw + gap) + gap; sh = fh + 2 * pad
    s = Image.new("RGBA", (sw, sh), FILM + (255,)); d = ImageDraw.Draw(s)
    for i, n in enumerate(names):
        x = gap + i * (fw + gap); s.paste(frame(n, fw, fh), (x, pad))
    for x in range(14, sw - 20, 40):
        for y in (14, sh - 32):
            d.rounded_rectangle((x, y, x + 22, y + 18), radius=4, fill=(235, 230, 215, 255))
    return s

def place(base, s, angle, cx, cy):
    s = s.rotate(angle, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", s.size, (0, 0, 0, 0)); sh.putalpha(s.getchannel("A").point(lambda v: int(v * .6)))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    x, y = int(cx - s.width / 2), int(cy - s.height / 2)
    base.alpha_composite(sh, (x + 16, y + 22)); base.alpha_composite(s, (x, y))

base = im.convert("RGBA")
# left and right strips run diagonally through the sides (seen on desktop and TV), clear of the safe area
place(base, strip(FRAMES[:4]), 14, 260, 560)
place(base, strip(FRAMES[4:]), -14, W - 260, 560)
place(base, strip(FRAMES[2:6]), -8, 380, 1220)
place(base, strip(FRAMES[1:5][::-1]), 8, W - 380, 1220)
place(base, strip(FRAMES[5:] + FRAMES[:1]), 4, 520, 150)
place(base, strip(FRAMES[3:7]), -4, W - 520, 150)
im = base.convert("RGB")
# fade the strips toward the centre so the safe area stays calm
m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((SX0 - 10, SY0 - 120, SX1 + 10, SY1 + 120), radius=200, fill=255)
m = m.filter(ImageFilter.GaussianBlur(90))
centre = Image.new("RGB", (W, H), INK); centre = Image.composite(Image.new("RGB", (W, H), (70, 56, 10)), centre, glow)
im = Image.composite(centre, im, m)
d = ImageDraw.Draw(im)

# logo + wordmark + tagline + subscribe button
LS = 270
logo = Image.open(LOGO).resize((LS, LS), Image.LANCZOS)
mask = Image.new("L", (LS, LS), 0); ImageDraw.Draw(mask).ellipse((0, 0, LS - 1, LS - 1), fill=255)
f_big, f_tag, f_btn = ImageFont.truetype(ANTON, 200), ImageFont.truetype(INTER_B, 44), ImageFont.truetype(INTER_B, 48)
word, tag = "SPECTARE", "TRUE STORIES, ANIMATED"
track, gap = 14, 54
ww = sum(d.textlength(c, font=f_big) for c in word) + track * (len(word) - 1)
total = LS + gap + ww
lx = int((W - total) / 2); ly = (H - LS) // 2
ring = 12; d.ellipse((lx - ring, ly - ring, lx + LS + ring, ly + LS + ring), fill=CREAM)
im.paste(logo, (lx, ly), mask); d = ImageDraw.Draw(im)
tx = lx + LS + gap
l, t, r, b = d.textbbox((0, 0), word, font=f_big)
ty = SY0 + 14 - t; x = tx
for c in word:
    d.text((x + 6, ty + 8), c, font=f_big, fill=(0, 0, 0)); d.text((x, ty), c, font=f_big, fill=CREAM)
    x += d.textlength(c, font=f_big) + track
row = ty + b + 26
d.text((tx, row), tag, font=f_tag, fill=YEL)
# subscribe button, right-aligned under the wordmark
bt = "SUBSCRIBE"; bw = d.textlength(bt, font=f_btn) + 64 + 48; bh = 82
bx0 = tx; bx1 = bx0 + bw; by0 = row + 64
d.rounded_rectangle((bx0 + 5, by0 + 7, bx1 + 5, by0 + bh + 7), radius=bh // 2, fill=(0, 0, 0))
d.rounded_rectangle((bx0, by0, bx1, by0 + bh), radius=bh // 2, fill=RED)
# small bell
cx, cy = bx0 + 48, by0 + bh // 2
d.pieslice((cx - 17, cy - 22, cx + 17, cy + 18), 180, 360, fill=(255, 255, 255))
d.rectangle((cx - 17, cy - 2, cx + 17, cy + 10), fill=(255, 255, 255))
d.polygon([(cx - 23, cy + 12), (cx + 23, cy + 12), (cx + 17, cy + 4), (cx - 17, cy + 4)], fill=(255, 255, 255))
d.ellipse((cx - 6, cy + 13, cx + 6, cy + 23), fill=(255, 255, 255))
bl, btop, br, bb = d.textbbox((0, 0), bt, font=f_btn)
d.text((cx + 34, by0 + (bh - (bb - btop)) / 2 - btop), bt, font=f_btn, fill=(255, 255, 255))

assert lx - ring >= SX0 and bx1 + 5 <= SX1 and by0 + bh + 7 <= SY1, (lx, bx1, by0 + bh, (SX0, SX1, SY1))

im.save(os.path.join(OUT, "spectare_banner_v002.png"), optimize=True)
im.save(os.path.join(OUT, "spectare_banner_v002.jpg"), quality=92)

def crop(w, h): return im.crop(((W - w) // 2, (H - h) // 2, (W + w) // 2, (H + h) // 2))
views = [("TV (full image)", im), ("Desktop (2560x423)", crop(2560, 423)), ("Tablet (1855x423)", crop(1855, 423)), ("Mobile (1546x423)", crop(1546, 423))]
PW = 1280; f = ImageFont.truetype(INTER_B, 26)
rows = [(lab, v.resize((int(PW * v.width / W), int(v.height * PW / W)), Image.LANCZOS)) for lab, v in views]
sheet = Image.new("RGB", (PW + 80, sum(r.height + 70 for _, r in rows) + 30), (245, 245, 245)); sd = ImageDraw.Draw(sheet); y = 30
for lab, r in rows:
    sd.text((40, y), lab, font=f, fill=(20, 20, 20)); sheet.paste(r, (40, y + 38)); y += r.height + 70
sheet.save(os.path.join(OUT, "banner_device_check.jpg"), quality=88)
print("ok", os.path.getsize(os.path.join(OUT, "spectare_banner_v002.png")) // 1024, "KB")
