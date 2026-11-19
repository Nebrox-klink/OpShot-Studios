"""Render 3D 2 "113" v002 (SH-050, SH-051, SH-052) and export the improved 30 s reference video.

Run with Blender in the background (Windows PowerShell, from Documents\\THE_GLASS_repo):
  & "C:\\Program Files\\Blender Foundation\\Blender 5.3\\blender.exe" -b -P THE_GLASS\\05_BLENDER\\scripts\\render_seq2_v002.py

Uses EEVEE at 1280x720, 24 fps, every frame (tuned for integrated Intel graphics: 16 samples,
no raytracing, soft shadows on). Needs ffmpeg on PATH for the final MP4.
Writes 06_AI_VIDEO/references/SEQ2_113_REFVIDEO_30s_v002.mp4 (720 frames = 30.0 s).
"""
import os
import shutil
import subprocess
import time

import bpy

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEQ = os.path.join(ROOT, "05_BLENDER", "sequences", "SEQ2_v002")
FRAMES = os.path.join(ROOT, "05_BLENDER", "renders", "SEQ2_v002")
OUT = os.path.join(ROOT, "06_AI_VIDEO", "references", "SEQ2_113_REFVIDEO_30s_v002.mp4")
SHOTS = ("SH-050", "SH-051", "SH-052")

t0 = time.time()
for shot in SHOTS:
    bpy.ops.wm.open_mainfile(filepath=os.path.join(SEQ, f"{shot}_v002.blend"))
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
    sc.frame_step = 1
    sc.eevee.taa_render_samples = 16
    for attr, val in (("use_raytracing", False), ("use_shadows", True), ("shadow_ray_count", 1), ("shadow_step_count", 4)):
        try:
            setattr(sc.eevee, attr, val)
        except Exception:
            pass
    sc.render.image_settings.file_format = "PNG"
    d = os.path.join(FRAMES, shot)
    os.makedirs(d, exist_ok=True)
    sc.render.filepath = os.path.join(d, "f_")
    print(f"[{shot}] rendering {sc.frame_end} frames", flush=True)
    bpy.ops.render.render(animation=True)
    print(f"[{shot}] done after {time.time() - t0:.0f} s", flush=True)

ff = shutil.which("ffmpeg") or "ffmpeg"
parts = []
for shot in SHOTS:
    part = os.path.join(FRAMES, f"{shot}.mp4")
    subprocess.run([ff, "-y", "-v", "error", "-framerate", "24", "-i", os.path.join(FRAMES, shot, "f_%04d.png"),
                    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", part], check=True)
    parts.append(part)
lst = os.path.join(FRAMES, "concat.txt")
with open(lst, "w", encoding="utf-8") as fh:
    fh.writelines(f"file '{p.replace(os.sep, '/')}'\n" for p in parts)
subprocess.run([ff, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "24", "-movflags", "+faststart", OUT], check=True)
print("WROTE", OUT, f"total {time.time() - t0:.0f} s", flush=True)
