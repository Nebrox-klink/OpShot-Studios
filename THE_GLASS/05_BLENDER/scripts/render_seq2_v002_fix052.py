"""Re-render SH-052 frames 106-240 of 3D 2 v002 and rebuild the 30 s reference video.

Why: in the first laptop render the PC slept for ~4 h at frame 106; after waking, Blender kept
rendering but the camera dolly-back stopped updating, so frames 106-240 stayed in close-up.
The bad frames are moved (not deleted) to renders/SEQ2_v002/SH-052_bad_after_sleep/.
This process asks Windows to stay awake while it runs (released automatically when it exits).

  & "C:\\Program Files\\Blender Foundation\\Blender 5.3\\blender.exe" -b -P THE_GLASS\\05_BLENDER\\scripts\\render_seq2_v002_fix052.py
"""
import ctypes
import os
import shutil
import subprocess
import time

import bpy

FIRST, LAST = 106, 240
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEQ = os.path.join(ROOT, "05_BLENDER", "sequences", "SEQ2_v002")
FRAMES = os.path.join(ROOT, "05_BLENDER", "renders", "SEQ2_v002")
OUT = os.path.join(ROOT, "06_AI_VIDEO", "references", "SEQ2_113_REFVIDEO_30s_v002.mp4")
SHOTS = ("SH-050", "SH-051", "SH-052")

try:  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED: no sleep while this process runs
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
except Exception:
    pass

t0 = time.time()
d = os.path.join(FRAMES, "SH-052")
bad = os.path.join(FRAMES, "SH-052_bad_after_sleep")
os.makedirs(bad, exist_ok=True)
for f in range(FIRST, LAST + 1):
    src = os.path.join(d, f"f_{f:04d}.png")
    if os.path.isfile(src) and not os.path.isfile(os.path.join(bad, os.path.basename(src))):
        shutil.move(src, bad)

bpy.ops.wm.open_mainfile(filepath=os.path.join(SEQ, "SH-052_v002.blend"))
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
sc.eevee.taa_render_samples = 16
for attr, val in (("use_raytracing", False), ("use_shadows", True), ("shadow_ray_count", 1), ("shadow_step_count", 4)):
    try:
        setattr(sc.eevee, attr, val)
    except Exception:
        pass
sc.render.image_settings.file_format = "PNG"
for f in range(FIRST, LAST + 1):
    out = os.path.join(d, f"f_{f:04d}.png")
    if os.path.isfile(out):
        continue
    sc.frame_set(f)
    cam = sc.camera.matrix_world.translation
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print(f"[SH-052] f{f} cam y={cam.y:.3f} done {time.time() - t0:.0f} s", flush=True)

ff = shutil.which("ffmpeg") or "ffmpeg"
parts = []
for shot in SHOTS:
    part = os.path.join(FRAMES, f"{shot}.mp4")
    subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-framerate", "24", "-i", os.path.join(FRAMES, shot, "f_%04d.png"),
                    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", part], check=True)
    parts.append(part)
lst = os.path.join(FRAMES, "concat.txt")
with open(lst, "w", encoding="utf-8") as fh:
    fh.writelines(f"file '{p.replace(os.sep, '/')}'\n" for p in parts)
subprocess.run([ff, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "24", "-movflags", "+faststart", OUT], check=True)
print("WROTE", OUT, f"total {time.time() - t0:.0f} s", flush=True)
