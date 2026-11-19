"""THE GLASS · v002 builder (3D 2 "113" upgraded: stylised robbers, furnished counting room,
thick laminated glass with branching layered fractures). 3D 1 shots are unchanged from v001.
Camera paths and window layout are identical to v001.

Based on: THE GLASS · 3D 1 and 3D 2 courtyard shots built on the shared SH-031 set.

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


# ===================================================================== v002: 3D 2 "113" upgrade
# Stylised animated-documentary look (not photoreal), tuned for EEVEE on integrated graphics:
# low-poly smooth-shaded primitives, alpha-blended glass (no raytraced refraction), no volumetrics.
import bmesh


def pmat(name, base, rough=0.6, metal=0.0, alpha=1.0, emit=None, es=0.0, spec=0.5):
    m = mat(name, base, rough, emit=emit, es=es, alpha=alpha)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Metallic"].default_value = metal
    for n in ("Specular IOR Level", "Specular"):
        if n in b.inputs:
            b.inputs[n].default_value = spec
            break
    return m


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True


def ellip(name, loc, radii, m, parent=None, seg=20, rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = radii
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    smooth(o)
    o.data.materials.append(m)
    if parent:
        o.parent = parent
    return o


def limb(name, p1, p2, r1, r2, m, parent):
    """tapered capsule between two points, built at the origin-root (parent has identity transform)"""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=r1, radius2=r2, depth=d.length, location=(p1 + p2) / 2)
    o = bpy.context.object
    o.name = name
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    smooth(o)
    o.data.materials.append(m)
    o.parent = parent
    for k, (p, r) in enumerate(((p1, r1), (p2, r2))):
        ellip(f"{name}_j{k}", p, (r, r, r), m, parent, seg=12, rings=6)
    return o


def elbow(sh, hand, out):
    sh, hand = Vector(sh), Vector(hand)
    return (sh + hand) / 2 + Vector((out * 0.06, -0.02, -0.11))


def robber_v2(name, pose, mats):
    """stylised, faceless robber (dark overalls, vest, helmet, balaclava, gloves), ~1.80 m, facing +y.
    pose: 'ram_L' (ram on the figure's right), 'ram_R' (ram on its left), 'stand'."""
    m_suit, m_vest, m_helmet, m_mask, m_glove, m_boot = mats
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object
    root.name = name
    hipL, hipR = (-0.10, 0, 0.94), (0.10, 0, 0.94)
    if pose == "stand":
        kneeL, kneeR, ankL, ankR = (-0.11, 0.03, 0.50), (0.11, -0.01, 0.50), (-0.13, 0.0, 0.09), (0.13, -0.03, 0.09)
    else:  # braced stride behind the ram
        kneeL, kneeR, ankL, ankR = (-0.12, 0.16, 0.52), (0.12, -0.10, 0.49), (-0.13, 0.24, 0.09), (0.13, -0.26, 0.09)
    for s, hp, kn, an in (("L", hipL, kneeL, ankL), ("R", hipR, kneeR, ankR)):
        limb(f"{name}_thigh{s}", hp, kn, 0.085, 0.064, m_suit, root)
        limb(f"{name}_shin{s}", kn, an, 0.060, 0.046, m_suit, root)
        ellip(f"{name}_boot{s}", (an[0], an[1] + 0.05, 0.05), (0.056, 0.13, 0.05), m_boot, root)
    ellip(name + "_pelvis", (0, 0, 0.98), (0.17, 0.115, 0.12), m_suit, root)
    lean = 0.06 if pose != "stand" else 0.0
    ellip(name + "_torso", (0, 0.01 + lean / 2, 1.26), (0.19, 0.12, 0.29), m_suit, root)
    ellip(name + "_vest", (0, 0.02 + lean / 2, 1.30), (0.205, 0.138, 0.21), m_vest, root)
    limb(name + "_neck", (0, lean, 1.53), (0, 0.01 + lean, 1.62), 0.05, 0.048, m_mask, root)
    ellip(name + "_head", (0, 0.02 + lean, 1.715), (0.093, 0.108, 0.118), m_mask, root)
    ellip(name + "_helmet", (0, 0.01 + lean, 1.765), (0.113, 0.128, 0.088), m_helmet, root)
    shL, shR = (-0.215, lean, 1.49), (0.215, lean, 1.49)
    if pose == "ram_L":
        hands = {"L": (0.22, 0.20, 1.40), "R": (0.25, 0.48, 1.43)}
    elif pose == "ram_R":
        hands = {"L": (-0.25, 0.48, 1.43), "R": (-0.22, 0.20, 1.40)}
    else:
        hands = {"L": (-0.27, 0.10, 0.92), "R": (0.27, 0.08, 0.92)}
    for s, sh in (("L", shL), ("R", shR)):
        hd = hands[s]
        el = elbow(sh, hd, -1 if s == "L" else 1)
        limb(f"{name}_upperarm{s}", sh, el, 0.058, 0.048, m_suit, root)
        limb(f"{name}_forearm{s}", el, hd, 0.046, 0.04, m_suit, root)
        ellip(f"{name}_glove{s}", hd, (0.048, 0.06, 0.045), m_glove, root)
    return root


def glove_hand(name, m_glove, m_sleeve):
    """gloved hand + forearm reaching along +y (into the room); root at the wrist"""
    bpy.ops.object.empty_add(location=(0, 0, 0))
    root = bpy.context.object
    root.name = name
    limb(name + "_forearm", (0, -0.42, -0.02), (0, -0.02, 0), 0.05, 0.04, m_sleeve, root)
    ellip(name + "_palm", (0, 0.06, 0), (0.05, 0.075, 0.022), m_glove, root)
    for i, fx in enumerate((-0.033, -0.011, 0.011, 0.033)):
        ln = (0.075, 0.085, 0.082, 0.066)[i]
        limb(f"{name}_finger{i}", (fx, 0.12, 0.0), (fx * 1.15, 0.12 + ln, -0.025), 0.011, 0.009, m_glove, root)
    limb(name + "_thumb", (-0.045, 0.05, 0.0), (-0.085, 0.11, -0.01), 0.013, 0.01, m_glove, root)
    return root


def note_bundle(name, loc, m_note, m_band, parent=None):
    o = box(name, loc, (0.155, 0.072, 0.03), m_note, 0.004)
    b = box(name + "_band", loc, (0.03, 0.075, 0.032), m_band)
    return [o, b]


def desk(name, loc, size, m_top, m_leg):
    x, y = loc
    w, d = size
    parts = [box(name + "_top", (x, y, 0.74), (w, d, 0.04), m_top, 0.008)]
    for sx in (-1, 1):
        parts.append(box(f"{name}_side{sx}", (x + sx * (w / 2 - 0.03), y, 0.36), (0.035, d - 0.06, 0.72), m_leg, 0.004))
    parts.append(box(name + "_modesty", (x, y + d / 2 - 0.04, 0.45), (w - 0.1, 0.02, 0.45), m_leg))
    return parts


def cash_tray(name, loc, m_tray, m_note, m_band, rnd):
    x, y, z = loc
    parts = [box(name, (x, y, z + 0.02), (0.46, 0.32, 0.04), m_tray, 0.006)]
    for i in range(4):
        cx = x - 0.17 + i * 0.113
        parts.append(box(f"{name}_div{i}", (cx + 0.056, y, z + 0.035), (0.006, 0.3, 0.035), m_tray))
        for k in range(rnd.randint(1, 3)):
            parts += note_bundle(f"{name}_n{i}{k}", (cx, y, z + 0.045 + k * 0.031), m_note, m_band)
    return parts


def cassette(name, loc, m_box, m_handle):
    x, y, z = loc
    return [box(name, (x, y, z + 0.09), (0.30, 0.42, 0.18), m_box, 0.012),
            box(name + "_lid", (x, y, z + 0.145), (0.305, 0.425, 0.006), m_handle),
            box(name + "_handle", (x, y + 0.215, z + 0.11), (0.14, 0.02, 0.025), m_handle, 0.006),
            box(name + "_lock", (x + 0.1, y + 0.212, z + 0.07), (0.035, 0.012, 0.035), m_handle)]


def crack_paths(seed, size):
    """laminated-glass bullet impact: dense short jagged radials (layer 1), short side branches (layer 2),
    3-4 concentric ring cracks (layer 0). Radius R ~ 55 % of the old star size."""
    r = random.Random(seed)
    R = size * 0.55
    n = r.randint(12, 18)
    base = r.uniform(0, 2 * math.pi)
    radials, paths = [], []
    for i in range(n):
        ang = base + i / n * 2 * math.pi + r.uniform(-0.15, 0.15)
        L = R * r.uniform(0.45, 1.0)
        steps = 6
        seg = L / steps
        pts = [(math.cos(ang) * R * 0.08, math.sin(ang) * R * 0.08)]
        for s_ in range(steps):
            ang += r.uniform(-0.45, 0.45)
            x, z = pts[-1]
            pts.append((x + math.cos(ang) * seg, z + math.sin(ang) * seg))
            if s_ >= 2 and r.random() < 0.3:
                ba = ang + r.choice((-1, 1)) * r.uniform(0.5, 1.0)
                x2, z2 = pts[-1]
                bl = seg * r.uniform(0.8, 1.6)
                paths.append(([(x2, z2), (x2 + math.cos(ba) * bl, z2 + math.sin(ba) * bl)], 0.0013, 2))
        radials.append(pts)
        paths.append((pts, 0.0021, 1))
    for frac, prob in ((0.22, 0.95), (0.4, 0.85), (0.62, 0.6), (0.85, 0.35)):
        k = max(1, min(6, round(frac * 6)))
        for i in range(n):
            if r.random() < prob:
                p, q = radials[i][min(k, len(radials[i]) - 1)], radials[(i + 1) % n][min(k, len(radials[(i + 1) % n]) - 1)]
                mid = ((p[0] + q[0]) / 2 * 1.08 + r.uniform(-0.04, 0.04) * R, (p[1] + q[1]) / 2 * 1.08 + r.uniform(-0.04, 0.04) * R)
                paths.append(([p, mid, q], 0.0014, 0))
    return paths


def ribbon(bm, pts, width, yv, ox, oz, mi, scale):
    """thin tapered ribbon in the xz-plane at depth y; width tapers to 35 % at the tip"""
    n = len(pts)
    left, right = [], []
    for i, (x, z) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        tx, tz = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, tz) or 1.0
        nx, nz = -tz / ln, tx / ln
        w = width * scale * (1.0 - 0.65 * i / max(1, n - 1)) / 2
        left.append(bm.verts.new((ox + x + nx * w, yv, oz + z + nz * w)))
        right.append(bm.verts.new((ox + x - nx * w, yv, oz + z - nz * w)))
    for i in range(n - 1):
        f = bm.faces.new((left[i], left[i + 1], right[i + 1], right[i]))
        f.material_index = mi


def fracture(name, centre, size, seed, layer_y, crack_mats, parent):
    """one impact = two objects (core+radials, then rings+branches a few frames later) on the real glass plies"""
    ox, _, oz = centre
    scale = 1.0
    objs = []
    for part, layers in (("A", (1,)), ("B", (0, 2))):
        me = bpy.data.meshes.new(f"{name}_{part}")
        bm = bmesh.new()
        for pts, w, lay in crack_paths(seed, size):
            if lay in layers:
                ribbon(bm, pts, w, layer_y[lay], ox, oz, lay, scale)
        if part == "A":  # crushed crater + frosted halo on the outer ply
            for rad, mi, yv in ((size * 0.55 * 0.13, 3, layer_y[0]), (size * 0.55 * 0.32, 4, layer_y[1])):
                c = bm.verts.new((ox, yv, oz))
                ring = [bm.verts.new((ox + math.cos(t / 16 * 2 * math.pi) * rad * random.Random(seed + t).uniform(0.8, 1.15), yv,
                                       oz + math.sin(t / 16 * 2 * math.pi) * rad * random.Random(seed + 50 + t).uniform(0.8, 1.15)))
                        for t in range(16)]
                for t in range(16):
                    f = bm.faces.new((c, ring[t], ring[(t + 1) % 16]))
                    f.material_index = mi
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new(f"{name}_{part}", me)
        sc.collection.objects.link(o)
        for m in crack_mats:
            o.data.materials.append(m)
        o.parent = parent
        o.matrix_parent_inverse = parent.matrix_world.inverted()
        objs.append(o)
    return objs


def upgrade_glass():
    """laminated pane v002: thicker plies, faint green body, fresnel-driven opacity (reads as reflections at angle)."""
    g = bpy.data.materials["M02_glass_laminated"]
    nt = g.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.40, 0.56, 0.52, 1)
    b.inputs["Roughness"].default_value = 0.035
    for n in ("Specular IOR Level", "Specular"):
        if n in b.inputs:
            b.inputs[n].default_value = 0.45
            break
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.035
    mr.inputs["To Max"].default_value = 0.30
    nt.links.new(lw.outputs["Fresnel"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], b.inputs["Alpha"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 9.0
    mr2 = nt.nodes.new("ShaderNodeMapRange")
    mr2.inputs["To Min"].default_value = 0.02
    mr2.inputs["To Max"].default_value = 0.09
    nt.links.new(nz.outputs["Fac"], mr2.inputs["Value"])
    nt.links.new(mr2.outputs["Result"], b.inputs["Roughness"])
    for i in range(3):
        O[f"glass_layer_{i}"].scale[1] = 1.6  # 8 mm -> ~13 mm plies (~3.9 cm laminate overall)


def furnish_room():
    """cash-processing room v002 (replaces the block shelf/table)"""
    for nm in ("room_shelf", "room_table"):
        if nm in O:
            bpy.data.objects.remove(O[nm], do_unlink=True)
    rnd = random.Random(2004)
    m_top = pmat("M06v2_desk_laminate", (0.46, 0.46, 0.43), 0.45)
    m_leg = pmat("M06v2_desk_steel", (0.10, 0.105, 0.11), 0.45, metal=0.5)
    m_tray = pmat("M06v2_tray_plastic", (0.10, 0.11, 0.12), 0.5)
    m_note = pmat("M06v2_notes", (0.50, 0.55, 0.42), 0.8)
    m_band = pmat("M06v2_note_band", (0.80, 0.70, 0.45), 0.7)
    m_box = pmat("M06v2_cassette_metal", (0.11, 0.12, 0.13), 0.45, metal=0.55)
    m_handle = pmat("M06v2_black_plastic", (0.02, 0.02, 0.022), 0.4)
    m_safe = pmat("M06v2_safe_green", (0.06, 0.09, 0.085), 0.35, metal=0.5)
    m_mach = pmat("M06v2_counter_machine", (0.30, 0.29, 0.27), 0.5)
    m_bag = bpy.data.materials.get("M20_bag_grey")
    # two counting desks in the foreground (left/right of the window axis)
    for nm, x, y in (("desk_L", WX - 1.05, YB + 1.25), ("desk_R", WX + 1.15, YB + 1.25)):
        desk(nm, (x, y), (1.5, 0.72), m_top, m_leg)
    cash_tray("tray_L1", (WX - 1.35, YB + 1.20, 0.76), m_tray, m_note, m_band, rnd)
    cash_tray("tray_L2", (WX - 0.80, YB + 1.32, 0.76), m_tray, m_note, m_band, rnd)
    box("counter_machine", (WX - 0.55, YB + 1.05, 0.86), (0.30, 0.28, 0.20), m_mach, 0.02)
    box("counter_machine_slot", (WX - 0.55, YB + 0.92, 0.93), (0.22, 0.02, 0.03), m_handle)
    cassette("cassette_R1", (WX + 0.80, YB + 1.25, 0.76), m_box, m_handle)
    cassette("cassette_R2", (WX + 1.15, YB + 1.25, 0.76), m_box, m_handle)
    cassette("cassette_R3", (WX + 0.97, YB + 1.25, 0.94), m_box, m_handle)
    cash_tray("tray_R1", (WX + 1.55, YB + 1.25, 0.76), m_tray, m_note, m_band, rnd)
    # back desk (revealed by the SH-052 dolly back)
    desk("desk_back", (WX - 0.1, YB + 3.25), (2.0, 0.75), m_top, m_leg)
    cash_tray("tray_B1", (WX - 0.6, YB + 3.25, 0.76), m_tray, m_note, m_band, rnd)
    cassette("cassette_B1", (WX + 0.35, YB + 3.25, 0.76), m_box, m_handle)
    # secured containers: floor safe + wall cabinet of cassettes
    box("safe_body", (WX - 2.55, YB + 2.1, 0.75), (0.75, 0.75, 1.5), m_safe, 0.02)
    box("safe_door_line", (WX - 2.17, YB + 2.1, 0.75), (0.01, 0.66, 1.4), m_handle)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.03, location=(WX - 2.16, YB + 2.1, 0.95), rotation=(0, math.radians(90), 0))
    o = bpy.context.object; o.name = "safe_wheel"; o.data.materials.append(m_box)
    box("cabinet_R", (WX + 2.6, YB + 2.3, 0.95), (0.6, 1.4, 1.9), m_leg, 0.01)
    for i in range(3):
        for j in range(3):
            cassette(f"cabinet_cas{i}{j}", (WX + 2.42, YB + 1.85 + j * 0.45, 0.2 + i * 0.55), m_box, m_handle)
    # in frame for SH-050: open shelving either side of the window + a counter under the sill
    YI = YB + 0.45  # inside face of the facade wall
    for side, sx in (("L", -1), ("R", 1)):
        x0 = WX + sx * 1.40
        box(f"shelf_{side}_back", (x0, YI + 0.02, 1.15), (0.64, 0.03, 2.1), m_leg)
        for i in range(5):
            box(f"shelf_{side}_board{i}", (x0, YI + 0.2, 0.25 + i * 0.45), (0.64, 0.38, 0.025), m_leg)
            if i < 4:
                for j in range(2):
                    if rnd.random() < 0.8:
                        cassette(f"shelf_{side}_cas{i}{j}", (x0 - 0.15 + j * 0.3, YI + 0.22, 0.265 + i * 0.45), m_box, m_handle)
        for sx2 in (-1, 1):
            box(f"shelf_{side}_post{sx2}", (x0 + sx2 * 0.31, YI + 0.2, 1.15), (0.025, 0.38, 2.3), m_leg)
    box("window_counter", (WX, YI + 0.32, 0.84), (2.3, 0.6, 0.05), m_top, 0.006)
    box("window_counter_front", (WX, YI + 0.6, 0.42), (2.3, 0.03, 0.8), m_leg)
    cash_tray("tray_W1", (WX - 0.62, YI + 0.3, 0.865), m_tray, m_note, m_band, rnd)
    box("counter_machine_W", (WX + 0.05, YI + 0.3, 0.95), (0.32, 0.3, 0.18), m_mach, 0.02)
    hop = box("counter_machine_W_hopper", (WX + 0.05, YI + 0.25, 1.07), (0.24, 0.16, 0.05), m_mach, 0.01)
    hop.rotation_euler = (math.radians(-25), 0, 0)
    box("counter_machine_W_tray", (WX + 0.05, YI + 0.46, 0.89), (0.22, 0.06, 0.05), m_handle, 0.006)
    box("counter_machine_W_display", (WX + 0.05, YI + 0.452, 0.97), (0.12, 0.004, 0.035), m_handle)
    box("counter_machine_W_led", (WX + 0.15, YI + 0.453, 0.97), (0.012, 0.004, 0.012),
        pmat("M06v2_led_green", (0.1, 0.9, 0.3), 0.5, emit=(0.1, 1.0, 0.3), es=4.0))
    cassette("cassette_W1", (WX + 0.6, YI + 0.3, 0.865), m_box, m_handle)
    cassette("cassette_W2", (WX + 0.6, YI + 0.3, 1.045), m_box, m_handle)
    # sealed cash bags on the floor
    if m_bag:
        for i in range(4):
            box(f"cash_bag_{i}", (WX - 1.6 + i * 0.28, YB + 1.75 + (i % 2) * 0.12, 0.17), (0.26, 0.24, 0.34), m_bag, 0.06)


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
    upgrade_glass()
    furnish_room()
    rmats = (pmat("M03v2_overall", (0.0055, 0.0062, 0.0090), 0.95, spec=0.03), pmat("M03v2_vest", (0.0040, 0.0042, 0.0048), 0.9, spec=0.04),
             pmat("M03v2_helmet", (0.0045, 0.0048, 0.0052), 0.7, spec=0.08), pmat("M03v2_balaclava", (0.003, 0.003, 0.0034), 0.95, spec=0.02),
             m_glove, pmat("M03v2_boot", (0.003, 0.003, 0.003), 0.8, spec=0.05))
    if shot == "SH-050":
        robs = [robber_v2("M03_robber_A", "ram_L", rmats), robber_v2("M03_robber_B", "ram_R", rmats)]
    else:
        robs = [robber_v2("M03_robber_A", "stand", rmats), robber_v2("M03_robber_B", "stand", rmats)]
        robs[0].location = (WX - 0.55, YB - 1.1, 0); robs[1].location = (WX + 0.75, YB - 1.4, 0)
    ply_y = [O[f"glass_layer_{i}"].location.y + 0.012 for i in range(3)]  # inner faces of the three plies
    m_ck = [pmat("FX02v2_crack_ring", (0.88, 0.91, 0.92), 0.4, alpha=0.6),
            pmat("FX02v2_crack_radial", (0.94, 0.96, 0.97), 0.3, alpha=0.8),
            pmat("FX02v2_crack_branch", (0.90, 0.93, 0.94), 0.35, alpha=0.6),
            pmat("FX02v2_crater", (0.90, 0.92, 0.93), 0.8, alpha=0.95),
            pmat("FX02v2_frost_halo", (0.86, 0.89, 0.90), 0.85, alpha=0.42)]
    ply_parent = O["glass_layer_1"]

    def star(name, center, size, m, n=7, seed=0):  # v002: real branching fracture on the glass plies
        a, b = fracture(name, center, size, seed, ply_y, m_ck, ply_parent)
        b.parent = a; b.matrix_parent_inverse = a.matrix_world.inverted()
        return a
    glass = [O[f"glass_layer_{i}"] for i in range(3)]
    stars = []
    centres = [(WX + rng.uniform(-0.85, 0.85), YB - 0.04, WCZ + rng.uniform(-0.6, 0.6)) for _ in range(40)]
    haze = box("FX02_milky_haze", (WX, YB - 0.045, WCZ), (WIN_W - 0.14, 0.004, WIN_H - 0.14), m_haze)

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
        for fc in all_fcurves(ram):  # v002: the two robbers drive the ram (roots follow its y motion)
            if fc.data_path == "location" and fc.array_index == 1:
                for kp in fc.keyframe_points:
                    for rb, dx in ((robs[0], -0.30), (robs[1], 0.30)):
                        key(rb, "location", int(kp.co[0]), Vector((WX + dx, kp.co[1] - 0.30, 0)))
        for k in range(10):  # damage 0→1→2
            st = star(f"FX02_star_{k}", centres[k], rng.uniform(0.18, 0.32), m_star, seed=k)
            key_vis_target = 82 if k < 3 else 132
            key_vis(st, key_vis_target); key_vis(st.children[0], key_vis_target + 4)
    elif shot == "SH-051":
        cam, tgt = new_camera("CAM_SH051_locked", 40, 5.6, focus=1.7)
        key(cam, "location", 1, Vector((WX, YB + 1.7, WCZ)))
        key(tgt, "location", 1, Vector((WX, YB, WCZ)))
        for k in range(36):
            st = star(f"FX02_star_{k}", centres[k], rng.uniform(0.14, 0.34), m_star, seed=k)
            burst = (1, 70, 140, 210)[min(3, k // 9)]
            t_on = burst + rng.randint(0, 20)
            key_vis(st, t_on); key_vis(st.children[0], t_on + 4)
        bpy.ops.object.light_add(type="POINT", location=(WX + 0.3, YB - 1.6, 1.5))
        fl = bpy.context.object; fl.name = "FX05_flash"; fl.data.color = (1.0, 0.75, 0.45); fl.data.shadow_soft_size = 0.2
        pulses = sorted(rng.sample(range(10, 270), 14))
        fl.data.energy = 0; fl.data.keyframe_insert("energy", frame=1)
        for p in pulses:
            for f, e in ((p - 1, 0), (p, 2500), (p + 2, 0)):
                fl.data.energy = e; fl.data.keyframe_insert("energy", frame=f)
        fog_alpha_keys(m_haze, [(1, 0.0), (140, 0.05), (288, 0.14)])
    else:  # SH-052
        cam, tgt = new_camera("CAM_SH052_dollyback", 55, 4.0, focus=1.5)
        key(cam, "location", 1, Vector((WX + 0.1, YB + 1.7, 1.6))); key(cam, "location", N, Vector((WX + 0.35, YB + 3.6, 1.85)))
        key(tgt, "location", 1, Vector((WX, YB, 1.55))); key(tgt, "location", N, Vector((WX, YB, 1.5)))
        cam.data.dof.focus_distance = 1.7; cam.data.dof.keyframe_insert("focus_distance", frame=1)
        cam.data.dof.focus_distance = 3.62; cam.data.dof.keyframe_insert("focus_distance", frame=N)
        for k in range(36):
            st = star(f"FX02_star_{k}", centres[k], rng.uniform(0.14, 0.34), m_star, seed=k)
        fog_alpha_keys(m_haze, [(1, 0.14), (N, 0.17)])
        # the laminated pane sags inward (pivot at the bottom edge) – a controlled fold, not a shatter
        bpy.ops.object.empty_add(location=(WX, YB, SILL + 0.07))
        piv = bpy.context.object; piv.name = "M02_sag_pivot"
        movers = glass + [haze]
        for g in movers:
            if g.parent is None:
                g.parent = piv; g.matrix_parent_inverse = piv.matrix_world.inverted()
        key(piv, "rotation_euler", 1, 0.0, idx=0); key(piv, "rotation_euler", 30, 0.0, idx=0)
        key(piv, "rotation_euler", 150, math.radians(-14), idx=0)
        key(piv, "location", 150, piv.location + Vector((0, 0.18, 0)))
        # gloved hand reaches through f150–f200
        hand = glove_hand("M03_glove_hand", m_glove, bpy.data.materials["M03v2_overall"])
        key(hand, "location", 1, Vector((WX - 0.2, YB - 0.7, 1.15))); key(hand, "location", 150, Vector((WX - 0.2, YB - 0.7, 1.15)))
        key(hand, "location", 200, Vector((WX - 0.2, YB + 0.35, 1.2)))
        # v002: a ragged hole tears open in the laminate (f125-150) where the hand comes through
        bpy.ops.object.empty_add(type="SPHERE", location=(WX - 0.2, YB, 1.17))
        hole = bpy.context.object; hole.name = "FX02_hole"
        hole.parent = O["glass_layer_1"]; hole.matrix_parent_inverse = O["glass_layer_1"].matrix_world.inverted()
        for f_, sc_ in ((1, 0.001), (125, 0.001), (150, 0.2)):
            key(hole, "scale", f_, Vector((sc_, sc_, sc_)))

        def hole_mask(mt, base_alpha=None):
            nt = mt.node_tree
            bs = nt.nodes["Principled BSDF"]
            tc = nt.nodes.new("ShaderNodeTexCoord"); tc.object = hole
            ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
            mr = nt.nodes.new("ShaderNodeMapRange")
            mr.inputs["From Min"].default_value = 0.92; mr.inputs["From Max"].default_value = 1.0
            mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"
            nt.links.new(tc.outputs["Object"], ln.inputs[0]); nt.links.new(ln.outputs["Value"], mr.inputs["Value"])
            if bs.inputs["Alpha"].is_linked and base_alpha is None:
                nt.links.new(bs.inputs["Alpha"].links[0].from_socket, mu.inputs[0])
            else:
                mu.inputs[0].default_value = bs.inputs["Alpha"].default_value if base_alpha is None else base_alpha
            nt.links.new(mr.outputs["Result"], mu.inputs[1]); nt.links.new(mu.outputs[0], bs.inputs["Alpha"])
        hole_mask(bpy.data.materials["M02_glass_laminated"])
        hole_mask(m_haze, base_alpha=0.155)
        for mt in m_ck:
            hole_mask(mt)
        # torn, frosted rim (in hole-local units, so it grows with the hole)
        me = bpy.data.meshes.new("FX02_hole_rim"); bm = bmesh.new(); rr = random.Random(52)
        for i in range(56):
            a0, a1 = i / 56 * 2 * math.pi, (i + 1) / 56 * 2 * math.pi
            r_in, r_out = rr.uniform(0.93, 1.0), rr.uniform(1.04, 1.18)
            am = (a0 + a1) / 2 + rr.uniform(-0.05, 0.05)
            v = [bm.verts.new((math.cos(a0) * r_in, 0, math.sin(a0) * r_in)), bm.verts.new((math.cos(a1) * r_in, 0, math.sin(a1) * r_in)),
                 bm.verts.new((math.cos(am) * r_out, 0, math.sin(am) * r_out))]
            bm.faces.new(v)
        bm.to_mesh(me); bm.free()
        rim = bpy.data.objects.new("FX02_hole_rim", me); sc.collection.objects.link(rim)
        rim.data.materials.append(pmat("FX02v2_hole_edge", (0.84, 0.87, 0.88), 0.85, alpha=0.3)); rim.parent = hole
        key_vis(rim, 126)
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
blend = os.path.join(OUT, f"{shot}_v002.blend")
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
