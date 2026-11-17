"""Cycles quality test for the glass shots.

Opens a shot .blend built by tg3d_courtyard_shots.py (EEVEE preview set-up). Then it:
  - switches the render to Cycles on the GPU (OptiX, then CUDA; falls back to CPU),
  - replaces the alpha-faked laminated glass with real refractive glass
    (transmission, IOR 1.52, thin crazing bump),
  - turns the flat white impact "stars" into glossy, light-catching cracks,
  - renders the given frames at 1920x1080 and logs the seconds per frame to timing.json.

  blender -b -P cycles_glass_upgrade.py -- --blend out/SH-052_v001.blend --out results \
          --frames 1,60,120,180,240 --samples 128 [--res 1920x1080]
"""
import argparse
import json
import os
import sys
import time

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--blend", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--frames", default="1,60,120,180,240")
ap.add_argument("--samples", type=int, default=128)
ap.add_argument("--res", default="1920x1080")
a = ap.parse_args(argv)
os.makedirs(a.out, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.blend))
sc = bpy.context.scene

# ---------------------------------------------------------------- device
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
device = "CPU"
for t in ("OPTIX", "CUDA"):
    try:
        prefs.compute_device_type = t
        prefs.get_devices()
        gpus = [d for d in prefs.devices if d.type == t]
        if gpus:
            for d in prefs.devices:
                d.use = d.type == t
            device = t + ": " + ", ".join(d.name for d in gpus)
            sc.cycles.device = "GPU"
            break
    except Exception:
        pass
print("render device:", device)

cy = sc.cycles
cy.samples = a.samples
cy.use_adaptive_sampling = True
cy.use_denoising = True
try:
    cy.denoiser = "OPTIX" if device.startswith("OPTIX") else "OPENIMAGEDENOISE"
except Exception:
    pass
cy.max_bounces = 12
cy.transmission_bounces = 12
cy.glossy_bounces = 6
cy.caustics_reflective = False
cy.caustics_refractive = False
w, h = (int(v) for v in a.res.split("x"))
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
sc.render.image_settings.file_format = "PNG"


# ---------------------------------------------------------------- materials
def principled(m):
    return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")


def set_in(b, names, value):
    for n in names:
        if n in b.inputs:
            b.inputs[n].default_value = value
            return


g = bpy.data.materials.get("M02_glass_laminated")
if g:
    nt = g.node_tree
    b = principled(g)
    set_in(b, ["Base Color"], (0.86, 0.95, 0.92, 1))
    set_in(b, ["Alpha"], 1.0)
    set_in(b, ["Transmission Weight", "Transmission"], 1.0)
    set_in(b, ["Roughness"], 0.015)
    set_in(b, ["IOR"], 1.52)
    # fine crazing: voronoi cell edges -> thin lines -> bump
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 26.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp.color_ramp.elements[1].position = 0.02
    ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.25
    bump.inputs["Distance"].default_value = 0.002
    nt.links.new(vor.outputs["Distance"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    print("glass upgraded: refractive + crazing bump")

s = bpy.data.materials.get("FX02_star")
if s:
    b = principled(s)
    set_in(b, ["Emission Strength"], 0.0)
    set_in(b, ["Base Color"], (0.92, 0.95, 1.0, 1))
    set_in(b, ["Roughness"], 0.12)
    set_in(b, ["Transmission Weight", "Transmission"], 0.35)
    set_in(b, ["IOR"], 1.52)
    print("impact cracks: glossy, non-emissive")

# ---------------------------------------------------------------- render
frames = [int(f) for f in a.frames.split(",") if f.strip()]
times = []
for f in frames:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(os.path.abspath(a.out), f"{sc.get('shot_id', 'shot')}_cycles_f{f:04d}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t0
    times.append(round(dt, 1))
    print(f"frame {f}: {dt:.1f} s", flush=True)

rep = {"shot": sc.get("shot_id"), "device": device, "resolution": a.res, "samples": a.samples,
       "frames": frames, "seconds_per_frame": times,
       "average_s": round(sum(times) / len(times), 1) if times else None,
       "blender": bpy.app.version_string}
json.dump(rep, open(os.path.join(a.out, "timing.json"), "w"), indent=1)
print(json.dumps(rep))
