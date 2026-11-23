"""Spectare YouTube banner v001, matching logo L2 (monogram). Drawn in code, no AI generation.
2560x1440. Everything important sits inside YouTube's safe area (1546x423, centred), which every device shows.
Usage: python3 -I make_banner.py OUT_DIR"""
import os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(HERE, "../../DB_COOPER/09_DELIVERABLES/tools/fonts/Anton-Regular.ttf")
INTER = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
LOGO = os.path.join(HERE, "../logo_v001/L2_spectare_monogram.png")
W, H = 2560, 1440
SAFE = ((W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2)
INK, RED, YEL, CREAM = (12, 14, 20), (214, 38, 32), (255, 212, 0), (236, 226, 204)

im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im)
random.seed(7)
for _ in range(60000):  # faint board texture
    x, y = random.randrange(W), random.randrange(H)
    d.point((x, y), fill=random.choice(((22, 25, 33), (18, 20, 27), (28, 31, 40))))
im = im.filter(ImageFilter.GaussianBlur(0.8)); d = ImageDraw.Draw(im)

def pin(x, y, r=20, c=RED):
    d.ellipse((x - r + 5, y - r + 7, x + r + 5, y + r + 7), fill=(0, 0, 0))
    d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    d.ellipse((x - r * .45, y - r * .55, x - r * .05, y - r * .15), fill=(255, 140, 130))

# red string web: decoration, runs out to the edges (TV/desktop) and stays clear of the text
pins = [(120, 380), (330, 610), (210, 900), (420, 1080), (2150, 470), (2420, 330), (2300, 820), (2460, 1060),
        (700, 260), (1880, 1180), (2050, 980)]
for a, b in [(0, 1), (1, 2), (2, 3), (1, 8), (4, 5), (4, 6), (6, 7), (6, 10), (10, 9), (3, 9)]:
    d.line([pins[a], pins[b]], fill=(150, 30, 26), width=6)
for i, p in enumerate(pins):
    pin(*p, 20, YEL if i in (2, 6) else RED)

# logo badge + wordmark + tagline, inside the safe area
x0, y0, x1, y1 = SAFE
logo = Image.open(LOGO).resize((280, 280), Image.LANCZOS)
mask = Image.new("L", (280, 280), 0); ImageDraw.Draw(mask).ellipse((0, 0, 279, 279), fill=255)
f_big, f_tag = ImageFont.truetype(ANTON, 212), ImageFont.truetype(INTER, 47)
word, tagline = "SPECTARE", "UNSOLVED MYSTERIES, ANIMATED"
gap, track = 52, 15
ww = sum(d.textlength(c, font=f_big) for c in word) + track * (len(word) - 1)
total = 280 + gap + ww
lx = int((W - total) // 2); ly = (H - 280) // 2
im.paste(logo, (lx, ly), mask); d = ImageDraw.Draw(im)
tx = lx + 280 + gap
l, t, r, b = d.textbbox((0, 0), word, font=f_big)
ty = (H - 423) // 2 + 58 - t
x = tx
for c in word:
    d.text((x, ty), c, font=f_big, fill=CREAM); x += d.textlength(c, font=f_big) + track
bar_y = ty + b + 26
d.rectangle((tx, bar_y, tx + ww, bar_y + 8), fill=RED)
d.text((tx, bar_y + 30), tagline, font=f_tag, fill=YEL)
assert lx >= x0 and tx + ww <= x1, (lx, tx + ww, SAFE)
im.save(os.path.join(OUT, "spectare_banner_v001.png"), optimize=True)
im.save(os.path.join(OUT, "spectare_banner_v001.jpg"), quality=92)

# preview: how each device crops it
def crop(w, h): return im.crop(((W - w) // 2, (H - h) // 2, (W + w) // 2, (H + h) // 2))
views = [("TV (full image)", im), ("Desktop (2560x423)", crop(2560, 423)), ("Tablet (1855x423)", crop(1855, 423)),
         ("Mobile (1546x423)", crop(1546, 423))]
PW = 1280; f = ImageFont.truetype(INTER, 26)
rows = [(lab, v.resize((PW if v.width == W else int(PW * v.width / W), int(v.height * PW / W)), Image.LANCZOS)) for lab, v in views]
sheet = Image.new("RGB", (PW + 80, sum(r.height + 70 for _, r in rows) + 30), (245, 245, 245)); sd = ImageDraw.Draw(sheet); y = 30
for lab, r in rows:
    sd.text((40, y), lab, font=f, fill=(20, 20, 20)); sheet.paste(r, (40, y + 38)); y += r.height + 70
sheet.save(os.path.join(OUT, "banner_device_check.jpg"), quality=88)
print("ok", os.path.getsize(os.path.join(OUT, "spectare_banner_v001.png")) // 1024, "KB png")
