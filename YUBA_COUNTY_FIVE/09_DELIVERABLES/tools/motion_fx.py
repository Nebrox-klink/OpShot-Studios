"""Local motion for still shots (free, no generation): slow camera push/pan + layered particle weather.

Usage: python3 -I motion_fx.py IN.png OUT.mp4 SECONDS [--snow N] [--push 1.08] [--pan dx,dy] [--fps 24]
Snow is drawn in three depth layers (far: small/slow/faint, near: big/fast/soft), so it reads as depth even though
the painting itself is flat. Output 1920x1080 H.264.
"""
import argparse, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("secs", type=float)
ap.add_argument("--snow", type=int, default=0); ap.add_argument("--push", type=float, default=1.08)
ap.add_argument("--pan", default="0,0"); ap.add_argument("--fps", type=int, default=24)
ap.add_argument("--crf", type=int, default=18)
a = ap.parse_args()
W, H = 1920, 1080
base = Image.open(a.src).convert("RGB")
# work canvas a bit larger than output so the push/pan never shows edges
cw = int(W * 1.25); ch = int(H * 1.25)
bw, bh = base.size; s = max(cw / bw, ch / bh)
base = base.resize((int(bw * s), int(bh * s)), Image.LANCZOS)
dx, dy = (float(v) for v in a.pan.split(","))
n = int(a.secs * a.fps)
rng = np.random.default_rng(7)
layers = []  # (count, size, speed px/s, drift, alpha, blur)
for cnt, size, spd, alpha, blur in [(a.snow, 2, 40, 140, 0), (a.snow // 2, 4, 90, 170, 0.6), (a.snow // 6, 9, 200, 150, 2.5)]:
    if cnt:
        layers.append(dict(x=rng.uniform(0, W, cnt), y=rng.uniform(0, H, cnt), ph=rng.uniform(0, 6.3, cnt),
                           size=size, spd=spd * rng.uniform(.7, 1.3, cnt), alpha=alpha, blur=blur))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(a.fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf),
                       "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / max(1, n - 1)
    e = t * t * (3 - 2 * t)  # ease in-out
    z = 1 + (a.push - 1) * e
    vw, vh = W * 1.2 / z, H * 1.2 / z
    cx = base.width / 2 + dx * e * base.width; cy = base.height / 2 + dy * e * base.height
    fr = base.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, H), Image.BICUBIC)
    for L in layers:
        L["y"] += L["spd"] / a.fps; L["x"] += np.sin(L["ph"] + i / a.fps * 1.3) * L["spd"] * 0.12 / a.fps
        L["y"] %= H + 20; L["x"] %= W
        ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov); r = L["size"]
        for x, y in zip(L["x"], L["y"]):
            d.ellipse((x - r, y - r, x + r, y + r), fill=L["alpha"])
        if L["blur"]: ov = ov.filter(ImageFilter.GaussianBlur(L["blur"]))
        fr = Image.composite(Image.new("RGB", (W, H), (235, 240, 250)), fr, ov)
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print(a.out)
