"""THE GLASS · 3D 1 and 3D 2 courtyard shots built on the shared SH-031 set.

Opens 05_BLENDER/sequences/SH-031_courtyard_v001.blend (M01 courtyard, M02 window,
M06 room, M03b figure) and builds one of these shots:
  SH-032, SH-033, SH-034  (3D 1 "Through the Glass", night, Feb 2004)
  SH-050, SH-051, SH-052  (3D 2 "113", morning, 5 Apr 2004)

Usage:
  python tg3d_courtyard_shots.py --shot SH-032 --out <dir> [--res 640x360] [--samples 6]
         [--step 2] [--render none|stills|anim]
  (or: blender -b -P tg3d_courtyard_shots.py -- --shot SH-032 ...)

--step 2 renders every second frame (12 fps), and the encoder doubles each frame
to 24 fps. That is a ROUGH-CUT preview economy for software EEVEE. Finals use --step 1.
"""
import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
ap = argparse.ArgumentParser()
ap.add_argument("--shot", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--res", default="640x360")
ap.add_argument("--samples", type=int, default=4)
ap.add_argument("--step", type=int, default=2)
ap.add_argument("--render", default="none", choices=["none", "stills", "anim"])
args = ap.parse_args(argv)
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "sequences", "SH-031_courtyard_v001.blend")
OUT = os.path.abspath(args.out)
os.makedirs(OUT, exist_ok=True)

LENGTH = {"SH-032": 192, "SH-033": 168, "SH-034": 192, "SH-050": 192, "SH-051": 288, "SH-052": 240}
WX, YB, SILL, WIN_W, WIN_H = 0.6, 4.5, 0.9, 2.2, 1.6
WCZ = SILL + WIN_H / 2          # window centre z = 1.7
RY = YB + 0.45 + 2.0            # room centre y = 6.95
AMBER = (1.0, 0.55, 0.25)

bpy.ops.wm.open_mainfile(filepath=os.path.abspath(BASE))
sc = bpy.context.scene
O = bpy.data.objects
rng = random.Random(113)


def mat(name, base, rough=0.8, emit=None, es=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = es
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    return m


def box(name, loc, size, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        md = o.modifiers.new("bev", "BEVEL"); md.width = bevel; md.segments = 2
    o.data.materials.append(m)
    return o


def key(ob, path, frame, value, idx=None):
    setattr(ob, path, value) if idx is None else getattr(ob, path).__setitem__(idx, value)
    ob.keyframe_insert(path, frame=frame, index=-1 if idx is None else idx)


def key_vis(ob, frame_on, frame_off=None):
    """hide_render keys: hidden before frame_on, (and after frame_off)."""
    ob.hide_render = True; ob.keyframe_insert("hide_render", frame=1)
    ob.hide_render = False; ob.keyframe_insert("hide_render", frame=frame_on)
    if frame_off:
        ob.hide_render = True; ob.keyframe_insert("hide_render", frame=frame_off)
    ob.hide_viewport = False


def all_fcurves(ob):
    ad = ob.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    curves = getattr(act, "fcurves", None)
    if curves is None:
        curves = [c for layer in act.layers for strip in layer.strips for cb in strip.channelbags for c in cb.fcurves]
    return list(curves)


def constant(ob):
    for fc in all_fcurves(ob):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


def new_camera(name, lens=50, fstop=2.8, focus=None):
    # remove SH-031 camera + its target animation
    for nm in ("CAM_SH031_crane",):
        if nm in O:
            bpy.data.objects.remove(O[nm], do_unlink=True)
    tgt = O.get("cam_target_window")
    if tgt:
        tgt.animation_data_clear()
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.name = name
    sc.camera = cam
    tc = cam.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    cam.data.lens = lens
    cam.data.sensor_width = 36
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = fstop
    if focus is not None:
        cam.data.dof.focus_distance = focus
    return cam, tgt


def staff_figure(name, m):
    """anonymous capsule figure (M21), root empty returned"""
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object; root.name = name
    parts = [box(name + "_body", (0, 0, 0.95), (0.42, 0.26, 1.15), m, 0.12),
             box(name + "_legs", (0, 0, 0.38), (0.34, 0.22, 0.76), m, 0.06)]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(0, 0, 1.68))
    hd = bpy.context.object; hd.name = name + "_head"; hd.data.materials.append(m); parts.append(hd)
    for p in parts:
        p.parent = root
    return root


def trolley(name, m, mbag):
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object; root.name = name
    parts = [box(name + "_frame", (0, 0, 0.45), (0.9, 0.55, 0.08), m), box(name + "_base", (0, 0, 0.12), (0.9, 0.55, 0.05), m),
             box(name + "_handle", (-0.45, 0, 0.8), (0.04, 0.55, 0.7), m)]
    for i in range(5):
        parts.append(box(f"{name}_bag{i}", (-0.25 + (i % 3) * 0.25, -0.12 + (i // 3) * 0.24, 0.62), (0.22, 0.2, 0.26), mbag, 0.05))
    for p in parts:
        p.parent = root
    return root


def star(name, center, size, m, n=7, seed=0):
    """white impact star (FX02) made of thin radial slivers; centre on the glass plane (x,z)"""
    r = random.Random(seed)
    bpy.ops.object.empty_add(location=center)
    root = bpy.context.object; root.name = name
    core = box(name + "_core", center, (size * 0.18, 0.004, size * 0.18), m)
    core.parent = root; core.matrix_parent_inverse = root.matrix_world.inverted()
    for i in range(n):
        a = i / n * 2 * math.pi + r.uniform(-0.25, 0.25)
        ln = size * r.uniform(0.5, 1.0)
        s = box(f"{name}_r{i}", (center[0] + math.cos(a) * ln / 2, center[1], center[2] + math.sin(a) * ln / 2), (ln, 0.003, size * 0.025), m)
        s.rotation_euler = (0, -a, 0)
        s.parent = root; s.matrix_parent_inverse = root.matrix_world.inverted()
    return root


def morning():
    """S2 relight: 08:00 overcast spring morning (LIGHTS_morning). Geometry untouched."""
    w = sc.world.node_tree.nodes["Background"]
    w.inputs["Color"].default_value = (0.45, 0.50, 0.56, 1); w.inputs["Strength"].default_value = 2.2
    sc.view_settings.exposure = -0.3
    bpy.data.materials["M02_glass_laminated"].node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.05
    rw = bpy.data.materials["M06_room_wall"].node_tree.nodes["Principled BSDF"]
    rw.inputs["Emission Strength"].default_value = 0.12
    rw.inputs["Base Color"].default_value = (0.28, 0.24, 0.20, 1)
    bpy.data.materials["M06_ceiling_light"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.0
    for nm in ("lamp_spot", "rim_figure_cold", "fill_back_cold"):
        if nm in O:
            O[nm].hide_render = True
    O["window_spill_light"].data.energy = 0
    for nm in ("room_light_0", "room_light_1"):
        O[nm].data.energy = 35
    sun = [o for o in O if o.type == "LIGHT" and o.data.type == "SUN"][0]
    sun.data.energy = 4.5; sun.data.color = (1.0, 0.93, 0.85)
    if "M03b_root" in O:  # Toska's Feb silhouette is not in the April scenes
        for ch in O["M03b_root"].children:
            ch.hide_render = True


def robber(name, loc, m):
    root = staff_figure(name, m)
    root.location = loc
    return root


m_fig = bpy.data.materials.get("M03b_silhouette_cloth")
m_staff = mat("M21_staff_warm", (0.10, 0.07, 0.05), 0.9)
m_bag = mat("M20_bag_grey", (0.22, 0.22, 0.21), 0.9)
m_star = mat("FX02_star", (0.95, 0.97, 1.0), 0.3, emit=(0.9, 0.95, 1.0), es=1.5)
m_fog = mat("FX01_breath_fog", (0.88, 0.93, 1.0), 0.4, emit=(0.7, 0.8, 0.9), es=0.35, alpha=0.0)
m_haze = mat("FX02_milky_haze", (0.85, 0.85, 0.80), 0.6, alpha=0.0)
m_glove = mat("M03_glove", (0.012, 0.012, 0.014), 0.7)
m_ram = mat("M05_ram_steel", (0.08, 0.085, 0.09), 0.45)
for nm in ("M21_staff_A", "M20_trolley_A"):  # replace static placeholders
    if nm in O:
        bpy.data.objects.remove(O[nm], do_unlink=True)

shot = args.shot
N = LENGTH[shot]
sc.frame_start, sc.frame_end = 1, N


def fog_alpha_keys(mat_, keys, radial=False):
    """Alpha keyframes. radial=True multiplies by a soft spherical falloff (round breath patch, no hard edges)."""
    nt = mat_.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    if radial:
        val = nt.nodes.new("ShaderNodeValue")
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Location"].default_value = (-0.5, -0.5, 0)
        mp.inputs["Scale"].default_value = (1, 1, 1)
        gr = nt.nodes.new("ShaderNodeTexGradient"); gr.gradient_type = "SPHERICAL"
        sq = nt.nodes.new("ShaderNodeMath"); sq.operation = "POWER"; sq.inputs[1].default_value = 1.6
        mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"
        nt.links.new(tc.outputs["UV"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], gr.inputs["Vector"])
        nt.links.new(gr.outputs["Fac"], sq.inputs[0]); nt.links.new(sq.outputs[0], mu.inputs[0])
        nt.links.new(val.outputs[0], mu.inputs[1]); nt.links.new(mu.outputs[0], bsdf.inputs["Alpha"])
        target = val.outputs[0]
    else:
        target = bsdf.inputs["Alpha"]
    for f, v in keys:
        target.default_value = v
        target.keyframe_insert("default_value", frame=f)


# ===================================================================== 3D 1
if shot == "SH-032":
    cam, tgt = new_camera("CAM_SH032_ots", 35, 2.8, focus=2.2)
    key(cam, "location", 1, Vector((-1.3, 2.85, 1.4))); key(cam, "location", N, Vector((-1.2, 2.95, 1.4)))
    key(tgt, "location", 1, Vector((0.45, YB, 1.5)))
    for i, (dx, delay) in enumerate(((0.0, 0), (0.7, 26))):
        s = staff_figure(f"M21_staff_{i}", m_staff)
        t = trolley(f"M20_trolley_{i}", m_staff, m_bag)
        y = RY - 1.3 + i * 0.6
        key(s, "location", 20 + delay, Vector((WX + 2.6 + dx, y, 0)))
        key(s, "location", 170 + delay // 2, Vector((WX - 2.9 + dx, y, 0)))
        key(t, "location", 20 + delay, Vector((WX + 1.9 + dx, y - 0.1, 0)))
        key(t, "location", 170 + delay // 2, Vector((WX - 3.6 + dx, y - 0.1, 0)))
    sc["shot_id"] = shot

elif shot == "SH-033":
    cam, tgt = new_camera("CAM_SH033_ecu", 50, 2.8, focus=1.0)
    key(cam, "location", 1, Vector((-0.55, 3.6, 1.3)))
    key(tgt, "location", 1, Vector((0.15, YB - 0.03, 1.36)))
    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0.08, YB - 0.045, 1.33), rotation=(math.radians(90), 0, 0))
    fog = bpy.context.object; fog.name = "FX01_breath_fog"; fog.data.materials.append(m_fog)
    fog_alpha_keys(m_fog, [(1, 0.0), (20, 0.0), (32, 0.6), (60, 0.12), (75, 0.0), (87, 0.7), (115, 0.15),
                           (130, 0.0), (142, 0.75), (168, 0.45)], radial=True)
    for f, s in ((1, 0.6), (32, 1.0), (75, 0.7), (87, 1.1), (130, 0.8), (142, 1.2), (168, 1.15)):
        key(fog, "scale", f, Vector((s, s, s)))
    glove = box("M03b_glove", (-0.32, YB - 0.28, 1.02), (0.13, 0.1, 0.17), m_glove, 0.04)
    for f, sz in ((1, 1.0), (90, 1.0), (150, 0.72), (168, 0.72)):
        key(glove, "scale", f, Vector((1.0, 1.0, sz)))
    sc["shot_id"] = shot

elif shot == "SH-034":
    cam, tgt = new_camera("CAM_SH034_static", 35, 4.0, focus=3.7)
    key(cam, "location", 1, Vector((-0.6, 0.95, 0.75)))
    key(tgt, "location", 1, Vector((0.1, YB, 1.25))); key(tgt, "location", 120, Vector((0.1, YB, 1.25)))
    key(tgt, "location", N, Vector((0.08, YB - 0.04, 1.33)))
    key(cam.data, "lens", 1, 35); key(cam.data, "lens", 120, 35); key(cam.data, "lens", N, 92)
    cam.data.dof.focus_distance = 3.7
    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0.08, YB - 0.045, 1.33), rotation=(math.radians(90), 0, 0))
    fog = bpy.context.object; fog.name = "FX01_breath_fog"; fog.data.materials.append(m_fog)
    fog_alpha_keys(m_fog, [(1, 0.7), (60, 0.6), (150, 0.4), (N, 0.25)], radial=True)
    root = O["M03b_root"]
    head = O["M03b_head_hood"]
    key(head, "location", 1, head.location.copy()); key(head, "location", 40, head.location + Vector((0, 0.02, -0.07)))
    key(root, "location", 1, root.location.copy()); key(root, "location", 90, root.location.copy())
    key(root, "location", 150, root.location + Vector((-3.2, -0.4, 0.0)))
    for f in range(96, 150, 12):  # walking bob
        key(root, "location", f + 6, 0.03, idx=2); key(root, "location", f + 12, 0.0, idx=2)
    sc["shot_id"] = shot

# ===================================================================== 3D 2
elif shot in ("SH-050", "SH-051", "SH-052"):
    morning()
    m_rob = m_fig
    robs = [robber("M03_robber_A", (WX - 0.55, YB - 1.1, 0), m_rob), robber("M03_robber_B", (WX + 0.75, YB - 1.4, 0), m_rob)]
    glass = [O[f"glass_layer_{i}"] for i in range(3)]
    stars = []
    centres = [(WX + rng.uniform(-0.85, 0.85), YB - 0.04, WCZ + rng.uniform(-0.6, 0.6)) for _ in range(40)]
    haze = box("FX02_milky_haze", (WX, YB + 0.05, WCZ), (WIN_W - 0.14, 0.004, WIN_H - 0.14), m_haze)

    if shot == "SH-050":
        cam, tgt = new_camera("CAM_SH050_inside", 28, 4.0, focus=2.6)
        key(cam, "location", 1, Vector((WX, YB + 2.6, 1.62)))
        key(tgt, "location", 1, Vector((WX, YB, 1.66)))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=1.1, location=(WX, YB - 0.9, 1.45), rotation=(math.radians(90), 0, 0))
        ram = bpy.context.object; ram.name = "M05_ram"; ram.data.materials.append(m_ram)
        hits = (30, 80, 130)
        key(ram, "location", 1, Vector((WX, YB - 1.2, 1.45)))
        for i, h in enumerate(hits):
            key(ram, "location", h - 8, Vector((WX, YB - 1.25, 1.45)))
            key(ram, "location", h, Vector((WX, YB - 0.62, 1.45)))
            key(ram, "location", h + 10, Vector((WX, YB - 1.15, 1.45)))
            for g in glass:
                key(g, "location", h - 1, g.location.copy())
                key(g, "location", h + 1, g.location + Vector((0, 0.035, 0)))
                key(g, "location", h + 6, g.location.copy())
            cam_shake = cam.location.copy()
            key(cam, "location", h, cam_shake); key(cam, "location", h + 1, cam_shake + Vector((0.006, 0, -0.004)))
            key(cam, "location", h + 3, cam_shake)
        for k in range(10):  # damage 0→1→2
            st = star(f"FX02_star_{k}", centres[k], rng.uniform(0.18, 0.32), m_star, seed=k)
            key_vis_target = 82 if k < 3 else 132
            for ch in [st] + list(st.children):
                key_vis(ch, key_vis_target)
    elif shot == "SH-051":
        cam, tgt = new_camera("CAM_SH051_locked", 40, 5.6, focus=1.7)
        key(cam, "location", 1, Vector((WX, YB + 1.7, WCZ)))
        key(tgt, "location", 1, Vector((WX, YB, WCZ)))
        for k in range(36):
            st = star(f"FX02_star_{k}", centres[k], rng.uniform(0.14, 0.34), m_star, seed=k)
            burst = (1, 70, 140, 210)[min(3, k // 9)]
            for ch in [st] + list(st.children):
                key_vis(ch, burst + rng.randint(0, 20))
        bpy.ops.object.light_add(type="POINT", location=(WX + 0.3, YB - 1.6, 1.5))
        fl = bpy.context.object; fl.name = "FX05_flash"; fl.data.color = (1.0, 0.75, 0.45); fl.data.shadow_soft_size = 0.2
        pulses = sorted(rng.sample(range(10, 270), 14))
        fl.data.energy = 0; fl.data.keyframe_insert("energy", frame=1)
        for p in pulses:
            for f, e in ((p - 1, 0), (p, 2500), (p + 2, 0)):
                fl.data.energy = e; fl.data.keyframe_insert("energy", frame=f)
        fog_alpha_keys(m_haze, [(1, 0.0), (140, 0.08), (288, 0.25)])
    else:  # SH-052
        cam, tgt = new_camera("CAM_SH052_dollyback", 55, 4.0, focus=1.5)
        key(cam, "location", 1, Vector((WX + 0.1, YB + 1.7, 1.6))); key(cam, "location", N, Vector((WX + 0.35, YB + 3.6, 1.85)))
        key(tgt, "location", 1, Vector((WX, YB, 1.55))); key(tgt, "location", N, Vector((WX, YB, 1.5)))
        for k in range(36):
            st = star(f"FX02_star_{k}", centres[k], rng.uniform(0.14, 0.34), m_star, seed=k)
        fog_alpha_keys(m_haze, [(1, 0.25), (N, 0.3)])
        # the laminated pane sags inward (pivot at the bottom edge) – a controlled fold, not a shatter
        bpy.ops.object.empty_add(location=(WX, YB, SILL + 0.07))
        piv = bpy.context.object; piv.name = "M02_sag_pivot"
        movers = glass + [haze] + [o for o in O if o.name.startswith("FX02_star_")]
        for g in movers:
            if g.parent is None:
                g.parent = piv; g.matrix_parent_inverse = piv.matrix_world.inverted()
        key(piv, "rotation_euler", 1, 0.0, idx=0); key(piv, "rotation_euler", 30, 0.0, idx=0)
        key(piv, "rotation_euler", 150, math.radians(-14), idx=0)
        key(piv, "location", 150, piv.location + Vector((0, 0.18, 0)))
        # gloved hand reaches through f150–f200
        hand = box("M03_glove_hand", (WX - 0.2, YB - 0.5, 1.15), (0.11, 0.42, 0.11), m_glove, 0.04)
        key(hand, "location", 1, Vector((WX - 0.2, YB - 0.7, 1.15))); key(hand, "location", 150, Vector((WX - 0.2, YB - 0.7, 1.15)))
        key(hand, "location", 200, Vector((WX - 0.2, YB + 0.35, 1.2)))
        # foreground shard (OUT 2 match frame)
        sh = box("FX02_fg_shard", (WX - 0.55, YB + 2.9, 1.55), (0.5, 0.01, 0.75), bpy.data.materials["M02_glass_laminated"])
        sh.rotation_euler = (0.1, 0.25, 0.6)
        key_vis(sh, 160)
    sc["shot_id"] = shot

sc["sequence"] = "3D 1 · Through the Glass" if shot < "SH-040" else "3D 2 · 113"
sc["source_class"] = "RECONSTRUCTED FROM EVIDENCE – staging dramatised"

# ---------------------------------------------------------------- render settings
w, h = (int(v) for v in args.res.split("x"))
sc.render.resolution_x, sc.render.resolution_y = w, h
sc.render.resolution_percentage = 100
sc.eevee.taa_render_samples = args.samples
sc.frame_step = args.step
if args.samples <= 8:  # LITE preview profile: ~5 s/frame on software EEVEE (benchmarked 17 Nov)
    for a_, v_ in (("shadow_resolution_scale", 0.25), ("use_gtao", False), ("use_fast_gi", False)):
        try:
            setattr(sc.eevee, a_, v_)
        except Exception:
            pass
    for o in bpy.data.objects:
        if o.type == "LIGHT" and o.data.type in ("POINT", "AREA") and o.name not in ("window_spill_light", "rim_figure_cold"):
            o.data.use_shadow = False
blend = os.path.join(OUT, f"{shot}_v001.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend)
print("saved", blend)
if args.render == "stills":
    for f in (1, N // 2, N):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(OUT, f"{shot}_still_f{f:04d}.png")
        bpy.ops.render.render(write_still=True)
elif args.render == "anim":
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.join(OUT, "frames", f"{shot}_")
    bpy.ops.render.render(animation=True)
print("done", shot)
