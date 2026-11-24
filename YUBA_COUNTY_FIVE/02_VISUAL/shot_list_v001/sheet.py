"""Contact sheet: python3 -I sheet.py OUT.jpg SH_101 SH_102 ...  (3 columns, 640 px tiles)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
out, names = sys.argv[1], sys.argv[2:]
W, H, C = 640, 357, 3
f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 22)
rows = (len(names) + C - 1) // C
sh = Image.new("RGB", (C * (W + 10) + 10, rows * (H + 40) + 10), (240, 240, 240)); d = ImageDraw.Draw(sh)
for i, n in enumerate(names):
    im = Image.open(f"stills/{n}.png").convert("RGB").resize((W, H), Image.LANCZOS)
    x, y = 10 + (i % C) * (W + 10), 10 + (i // C) * (H + 40)
    sh.paste(im, (x, y)); d.text((x, y + H + 6), n, font=f, fill=(20, 20, 20))
sh.save(out, quality=86)
