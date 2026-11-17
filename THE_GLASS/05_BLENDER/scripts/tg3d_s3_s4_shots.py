"""THE GLASS · 3D 3 "The Windshield" (SH-064–067) and 3D 4 "One Year to the Day" (SH-083–086).

Rough-cut v001 builders. These are low-poly, procedural, EEVEE sets, built from factory settings.
The ethics rules are hard-coded:
  3D 3: no face, no head, no blood, no impact on a person; the windshield crack is a graphic decal.
  3D 4: a generic Málaga street and internet café (not the real Chicoti façade), calm entry,
        the man stays seated, no weapons, no readable text.

Usage:
  python tg3d_s3_s4_shots.py --shot SH-064 --out <dir> [--res 640x360] [--samples 4] [--step 2]
         [--render none|stills|anim]
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
OUT = os.path.abspath(args.out)
os.makedirs(OUT, exist_ok=True)
SHOT = args.shot
LENGTH = {"SH-064": 192, "SH-065": 192, "SH-066": 96, "SH-067": 240,
          "SH-083": 168, "SH-084": 144, "SH-085": 216, "SH-086": 192}
N = LENGTH[SHOT]
rng = random.Random(64)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
sc.render.fps = 24
sc.frame_start, sc.frame_end = 1, N
sc.view_settings.view_transform = "AgX"
looks = [i.identifier for i in sc.view_settings.bl_rna.properties["look"].enum_items]
sc.view_settings.look = "AgX - Base Contrast" if "AgX - Base Contrast" in looks else "None"
for a, v in (("shadow_ray_count", 1), ("shadow_step_count", 2), ("use_raytracing", False)):
    if hasattr(sc.eevee, a):
        setattr(sc.eevee, a, v)
world = bpy.data.worlds.new("W")
sc.world = world
world.use_nodes = True
BG = world.node_tree.nodes["Background"]


# ------------------------------------------------------------------ helpers
def mat(name, base, rough=0.8, emit=None, es=0.0, alpha=1.0, metal=0.0, spec=0.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = spec
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


def box(name, loc, size, m, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        md = o.modifiers.new("bev", "BEVEL"); md.width = bevel; md.segments = 2
    o.data.materials.append(m)
    return o


def cyl(name, loc, r, d, m, rot=(0, 0, 0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(m)
    return o


def plane(name, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0] / 2, size[1] / 2, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(m)
    return o


def light(kind, loc, energy, col, rot=(0, 0, 0), size=0.5, name=None):
    bpy.ops.object.light_add(type=kind, location=loc, rotation=rot)
    l = bpy.context.object
    if name:
        l.name = name
    l.data.energy = energy
    l.data.color = col
    if kind == "AREA":
        l.data.size = size
    if hasattr(l.data, "shadow_soft_size") and kind != "AREA":
        l.data.shadow_soft_size = 0.05
    return l


def camera(lens, loc, target, fstop=2.8, focus_obj=None, name="CAM"):
    bpy.ops.object.empty_add(location=target)
    tgt = bpy.context.object
    tgt.name = name + "_target"
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = name
    cam.data.lens = lens
    tc = cam.constraints.new("TRACK_TO"); tc.target = tgt
    tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = fstop
    if focus_obj:
        cam.data.dof.focus_object = focus_obj
    sc.camera = cam
    return cam, tgt


def key(ob, path, frame, value):
    setattr(ob, path, value)
    ob.keyframe_insert(path, frame=frame)


def all_fcurves(idblock):
    ad = idblock.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    curves = getattr(act, "fcurves", None)
    if curves is None:
        curves = [c for layer in act.layers for strip in layer.strips for cb in strip.channelbags for c in cb.fcurves]
    return list(curves)


def interp(idblock, mode):
    for fc in all_fcurves(idblock):
        for kp in fc.keyframe_points:
            kp.interpolation = mode


def figure(name, loc, m, seated=False, scale=1.0, rot_z=0.0):
    """Faceless low-poly person from bevelled boxes; returns the root empty."""
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    root.name = name
    parts = []
    s = scale
    if seated:
        spec = [("torso", (0, 0, 0.78), (0.42, 0.26, 0.60), (math.radians(-8), 0, 0)),
                ("head", (0, -0.02, 1.22), (0.20, 0.22, 0.25), (0, 0, 0)),
                ("thigh_L", (-0.11, -0.26, 0.48), (0.15, 0.46, 0.15), (0, 0, 0)),
                ("thigh_R", (0.11, -0.26, 0.48), (0.15, 0.46, 0.15), (0, 0, 0)),
                ("shin_L", (-0.11, -0.48, 0.24), (0.13, 0.13, 0.46), (0, 0, 0)),
                ("shin_R", (0.11, -0.48, 0.24), (0.13, 0.13, 0.46), (0, 0, 0)),
                ("arm_L", (-0.26, -0.18, 0.86), (0.11, 0.40, 0.11), (math.radians(20), 0, 0)),
                ("arm_R", (0.26, -0.18, 0.86), (0.11, 0.40, 0.11), (math.radians(20), 0, 0))]
    else:
        spec = [("torso", (0, 0, 1.20), (0.44, 0.26, 0.66), (0, 0, 0)),
                ("head", (0, 0, 1.70), (0.20, 0.22, 0.26), (0, 0, 0)),
                ("leg_L", (-0.11, 0, 0.45), (0.16, 0.18, 0.90), (0, 0, 0)),
                ("leg_R", (0.11, 0, 0.45), (0.16, 0.18, 0.90), (0, 0, 0)),
                ("arm_L", (-0.28, 0, 1.12), (0.11, 0.12, 0.62), (0, 0, 0)),
                ("arm_R", (0.28, 0, 1.12), (0.11, 0.12, 0.62), (0, 0, 0))]
    for nm, l, sz, r in spec:
        o = box(f"{name}_{nm}", Vector(loc) + Vector(l) * s, tuple(x * s for x in sz), m, bevel=0.04 * s, rot=r)
        parts.append(o)
    for p in parts:
        p.parent = root
        p.matrix_parent_inverse = root.matrix_world.inverted()
    root.rotation_euler = (0, 0, rot_z)
    return root, {p.name.split("_", 1)[1]: p for p in parts}


# ================================================================== 3D 3 SET
def build_s3():
    BG.inputs["Color"].default_value = (0.42, 0.50, 0.60, 1)
    BG.inputs["Strength"].default_value = 0.35
    sc.view_settings.exposure = -0.4
    m_dash = mat("M07_dash", (0.03, 0.035, 0.04), 0.7)
    m_trim = mat("M07_trim", (0.06, 0.065, 0.07), 0.6)
    m_seat = mat("M07_seat", (0.02, 0.022, 0.026), 0.9)
    m_glass = mat("M07_windshield", (0.6, 0.7, 0.75), 0.05, alpha=0.08, spec=0.8)
    m_sleeve = mat("M08_uniform", (0.015, 0.02, 0.04), 0.85)
    m_glove = mat("M08_hand", (0.02, 0.02, 0.02), 0.8)
    m_asph = mat("M10_asphalt", (0.05, 0.05, 0.055), 0.45)
    m_walls = [mat(f"M10_facade_{i}", c, 0.9) for i, c in enumerate(((0.78, 0.76, 0.70), (0.62, 0.64, 0.62), (0.70, 0.66, 0.58), (0.55, 0.58, 0.60)))]
    m_win = mat("M10_window", (0.08, 0.1, 0.12), 0.2, emit=(0.9, 0.75, 0.5), es=0.05)
    m_spire = mat("M11_spire", (0.25, 0.28, 0.30), 0.9)
    m_smoke = mat("FX07_smoke", (0.40, 0.42, 0.45), 1.0, alpha=0.10)
    m_crack = mat("FX02_crack", (0.95, 0.97, 1.0), 0.3, emit=(1, 1, 1), es=2.5, alpha=0.0)
    # cabin: car faces +Y; driver on the left (x = -0.4), camera inside
    box("M07_dashboard", (0, 0.55, 0.85), (1.6, 0.5, 0.25), m_dash, bevel=0.05)
    box("M07_dash_top", (0, 0.72, 1.0), (1.6, 0.35, 0.06), m_trim)
    for sx in (-1, 1):
        box(f"M07_A_pillar_{sx}", (0.78 * sx, 0.8, 1.25), (0.08, 0.08, 0.6), m_trim, rot=(math.radians(-25), 0, 0))
        box(f"M07_side_{sx}", (0.82 * sx, -0.2, 0.75), (0.06, 1.8, 0.5), m_trim)
    box("M07_roof", (0, 0.0, 1.55), (1.7, 1.8, 0.06), m_dash)
    box("M07_seat_driver", (-0.4, -0.45, 0.55), (0.55, 0.55, 0.12), m_seat, bevel=0.05)
    box("M07_seatback_driver", (-0.4, -0.72, 0.95), (0.55, 0.12, 0.75), m_seat, bevel=0.05)
    ws = plane("M07_windshield", (0, 0.9, 1.22), (1.55, 0.62), m_glass, rot=(math.radians(65), 0, 0))
    crack = plane("FX02_crack_decal", (0.30, 0.875, 1.33), (0.42, 0.30), m_crack, rot=(math.radians(65), 0, 0))
    # procedural spider-web crack texture: thin radial lines via wave texture on polar coords (approximation)
    nt = m_crack.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["UV"], sep.inputs[0])
    cx = nt.nodes.new("ShaderNodeMath"); cx.operation = "SUBTRACT"; cx.inputs[1].default_value = 0.5
    cy = nt.nodes.new("ShaderNodeMath"); cy.operation = "SUBTRACT"; cy.inputs[1].default_value = 0.55
    nt.links.new(sep.outputs[0], cx.inputs[0]); nt.links.new(sep.outputs[1], cy.inputs[0])
    at = nt.nodes.new("ShaderNodeMath"); at.operation = "ARCTAN2"
    nt.links.new(cy.outputs[0], at.inputs[0]); nt.links.new(cx.outputs[0], at.inputs[1])
    jit = nt.nodes.new("ShaderNodeTexNoise"); jit.inputs["Scale"].default_value = 14.0
    nt.links.new(tc.outputs["UV"], jit.inputs["Vector"])
    jadd = nt.nodes.new("ShaderNodeMath"); jadd.operation = "MULTIPLY_ADD"; jadd.inputs[1].default_value = 0.35
    nt.links.new(jit.outputs["Fac"], jadd.inputs[0]); nt.links.new(at.outputs[0], jadd.inputs[2])
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 7.0
    nt.links.new(jadd.outputs[0], mul.inputs[0])
    sn = nt.nodes.new("ShaderNodeMath"); sn.operation = "SINE"
    nt.links.new(mul.outputs[0], sn.inputs[0])
    ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"
    nt.links.new(sn.outputs[0], ab.inputs[0])
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.03
    nt.links.new(ab.outputs[0], lt.inputs[0])
    # rings
    ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    cmb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(cx.outputs[0], cmb.inputs[0]); nt.links.new(cy.outputs[0], cmb.inputs[1])
    nt.links.new(cmb.outputs[0], ln.inputs[0])
    rmul = nt.nodes.new("ShaderNodeMath"); rmul.operation = "MULTIPLY"; rmul.inputs[1].default_value = 55.0
    nt.links.new(ln.outputs["Value"], rmul.inputs[0])
    rs = nt.nodes.new("ShaderNodeMath"); rs.operation = "SINE"
    nt.links.new(rmul.outputs[0], rs.inputs[0])
    rl = nt.nodes.new("ShaderNodeMath"); rl.operation = "GREATER_THAN"; rl.inputs[1].default_value = 0.9995
    nt.links.new(rs.outputs[0], rl.inputs[0])
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
    nt.links.new(lt.outputs[0], mx.inputs[0]); nt.links.new(rl.outputs[0], mx.inputs[1])
    # growth: radius mask driven by value node "crack"
    grow = nt.nodes.new("ShaderNodeValue"); grow.name = "crack"; grow.outputs[0].default_value = 0.0
    gm = nt.nodes.new("ShaderNodeMath"); gm.operation = "LESS_THAN"
    nt.links.new(ln.outputs["Value"], gm.inputs[0]); nt.links.new(grow.outputs[0], gm.inputs[1])
    fin = nt.nodes.new("ShaderNodeMath"); fin.operation = "MULTIPLY"
    nt.links.new(mx.outputs[0], fin.inputs[0]); nt.links.new(gm.outputs[0], fin.inputs[1])
    fa = nt.nodes.new("ShaderNodeMath"); fa.operation = "MULTIPLY"; fa.inputs[1].default_value = 1.0
    nt.links.new(fin.outputs[0], fa.inputs[0])
    nt.links.new(fa.outputs[0], b.inputs["Alpha"])
    # driver hands on wheel (no head, no face ever in frame)
    wheel_c = Vector((-0.4, 0.25, 1.0))
    bpy.ops.mesh.primitive_torus_add(location=wheel_c, rotation=(math.radians(65), 0, 0), major_radius=0.19, minor_radius=0.018)
    wheel = bpy.context.object; wheel.name = "M09_wheel"; wheel.data.materials.append(m_trim)
    cyl("M09_column", wheel_c + Vector((0, 0.2, -0.1)), 0.03, 0.4, m_trim, rot=(math.radians(65), 0, 0))
    for sx, nm in ((-1, "L"), (1, "R")):
        hand = box(f"M08_hand_{nm}", wheel_c + Vector((0.17 * sx, -0.02, 0.05)), (0.07, 0.09, 0.11), m_glove, bevel=0.02)
        box(f"M08_sleeve_{nm}", wheel_c + Vector((0.19 * sx, -0.30, -0.06)), (0.075, 0.5, 0.075), m_sleeve, bevel=0.02, rot=(math.radians(15), 0, 0))
    # street outside (+Y)
    plane("M10_road", (0, 30, 0.0), (9, 70), m_asph)
    for side in (-1, 1):
        y = 4
        i = 0
        while y < 62:
            w = rng.uniform(5, 9); h = rng.uniform(6, 11)
            fac = box(f"M10_house_{side}_{i}", (side * 9.5, y + w / 2, h / 2), (5, w, h), m_walls[rng.randrange(4)])
            for wy in range(int(w // 1.8)):
                for wz in range(int(h // 2.6)):
                    box(f"M10_win_{side}_{i}_{wy}_{wz}", (side * 6.98, y + 0.9 + wy * 1.8, 1.6 + wz * 2.6), (0.05, 0.8, 1.1), m_win)
            y += w + 0.3; i += 1
    sp = box("M11_spire_tower", (1.5, 70, 9), (4, 4, 18), m_spire)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=2.8, depth=9, location=(1.5, 70, 22.5))
    bpy.context.object.data.materials.append(m_spire)
    for k in range(3):
        s = plane(f"FX07_smoke_{k}", (rng.uniform(-3, 4), 38 + k * 4, 5 + k), (8, 7), m_smoke, rot=(math.radians(90), 0, 0))
        key(s, "location", 1, s.location.copy())
        key(s, "location", N, s.location + Vector((0.8, 0, 1.8)))
    # light: low warm sun from front-left through the windshield, cool sky fill
    sun = light("SUN", (0, 0, 10), 4.5, (1.0, 0.80, 0.55), rot=(math.radians(74), 0, math.radians(200)), name="sun")
    light("AREA", (0, 0.4, 1.45), 6, (0.7, 0.78, 0.9), rot=(0, 0, 0), size=1.2, name="cabin_fill")
    return dict(ws=ws, crack=crack, grow=grow, sun=sun, wheel=wheel)


# ================================================================== 3D 4 SET
def build_s4():
    BG.inputs["Color"].default_value = (0.50, 0.64, 0.85, 1)
    BG.inputs["Strength"].default_value = 0.45
    sc.view_settings.exposure = -0.5
    facades = [mat(f"M12_facade_{i}", c, 0.9) for i, c in enumerate(((0.86, 0.80, 0.66), (0.80, 0.68, 0.48), (0.88, 0.85, 0.78), (0.74, 0.62, 0.50)))]
    m_road = mat("M12_road", (0.09, 0.09, 0.095), 0.6)
    m_pave = mat("M12_pavement", (0.5, 0.47, 0.42), 0.9)
    m_shut = mat("M12_shutter", (0.35, 0.25, 0.18), 0.8)
    m_win = mat("M12_window", (0.05, 0.06, 0.07), 0.15, spec=0.8)
    m_sign = mat("M13_sign_generic", (0.12, 0.22, 0.32), 0.5, emit=(0.4, 0.7, 0.9), es=0.3)
    m_car = [mat(f"M14_car_{i}", c, 0.35, metal=0.3) for i, c in enumerate(((0.55, 0.08, 0.06), (0.62, 0.62, 0.64), (0.10, 0.18, 0.32)))]
    m_floor = mat("M13_floor", (0.55, 0.52, 0.46), 0.6)
    m_wall = mat("M13_wall", (0.80, 0.80, 0.76), 0.9)
    m_desk = mat("M13_desk", (0.40, 0.33, 0.25), 0.6)
    m_beige = mat("M19_beige_plastic", (0.72, 0.68, 0.58), 0.6)
    m_screen = mat("M19_crt_screen", (0.02, 0.025, 0.03), 0.05, emit=(0.55, 0.75, 0.95), es=1.2, spec=0.9)
    m_fluor = mat("M13_fluorescent", (1, 1, 1), 0.5, emit=(0.9, 0.97, 1.0), es=6)
    m_door = mat("M13_glass_door", (0.6, 0.7, 0.75), 0.05, alpha=0.18, spec=0.9)
    m_fig = mat("M03b_jacket_light", (0.30, 0.30, 0.28), 0.9)
    m_pol = [mat(f"M16_plainclothes_{i}", c, 0.9) for i, c in enumerate(((0.05, 0.06, 0.08), (0.12, 0.14, 0.18), (0.20, 0.17, 0.14), (0.08, 0.09, 0.07)))]
    # street along X; café on the north side (y = 6 façade line), interior y in [6, 14]
    plane("M12_road", (0, 0, 0), (80, 9), m_road)
    plane("M12_pave_N", (0, 5.25, 0.08), (80, 1.5), m_pave)
    plane("M12_pave_S", (0, -5.25, 0.08), (80, 1.5), m_pave)
    x = -40
    i = 0
    while x < 40:
        w = rng.uniform(7, 12); h = rng.uniform(14, 20)
        for side, y0 in ((1, 6.0), (-1, -6.0)):
            if side == 1 and -3.5 < x + w / 2 < 3.5:
                continue  # leave room for the café block
            box(f"M12_bld_{side}_{i}", (x + w / 2, y0 + side * 4, h / 2), (w - 0.2, 8, h), facades[rng.randrange(4)])
            for fx in range(int(w // 2.4)):
                for fz in range(1, int(h // 3.2)):
                    box(f"M12_win_{side}_{i}_{fx}_{fz}", (x + 1.2 + fx * 2.4, y0 - side * 0.02, fz * 3.2 + 0.8), (1.0, 0.05, 1.5), m_win)
                    if rng.random() < 0.6:
                        box(f"M12_shut_{side}_{i}_{fx}_{fz}", (x + 0.55 + fx * 2.4, y0 - side * 0.05, fz * 3.2 + 0.8), (0.3, 0.05, 1.5), m_shut)
        x += w; i += 1
    # café block x in [-3.5, 3.5]: ground floor shopfront + upper floors
    box("M13_upper", (0, 10, 10.5), (7, 8, 15), facades[2])
    box("M13_shop_L", (-3.2, 6.1, 1.6), (0.6, 0.3, 3.2), facades[1])
    box("M13_shop_R", (3.2, 6.1, 1.6), (0.6, 0.3, 3.2), facades[1])
    box("M13_sign", (0, 5.95, 2.9), (4.5, 0.12, 0.55), m_sign)  # generic sign: no letters
    plane("M13_window_L", (-1.9, 6.0, 1.45), (2.0, 2.5), m_door, rot=(math.radians(90), 0, 0))
    plane("M13_window_R", (1.9, 6.0, 1.45), (2.0, 2.5), m_door, rot=(math.radians(90), 0, 0))
    door = plane("M13_door", (0, 6.0, 1.15), (1.0, 2.3), m_door, rot=(math.radians(90), 0, 0))
    # interior
    plane("M13_floor", (0, 10, 0.02), (7, 8), m_floor)
    box("M13_back_wall", (0, 13.9, 1.6), (7, 0.2, 3.2), m_wall)
    box("M13_wall_L", (-3.4, 10, 1.6), (0.2, 8, 3.2), m_wall)
    box("M13_wall_R", (3.4, 10, 1.6), (0.2, 8, 3.2), m_wall)
    plane("M13_ceiling", (0, 10, 3.2), (7, 8), m_wall, rot=(math.radians(180), 0, 0))
    for k, (cx, cy) in enumerate(((-1.5, 8.5), (1.5, 8.5), (-1.5, 11.5), (1.5, 11.5))):
        box(f"M13_fluor_{k}", (cx, cy, 3.15), (1.2, 0.3, 0.04), m_fluor)
        light("AREA", (cx, cy, 3.1), 60, (0.88, 0.95, 1.0), rot=(0, 0, 0), size=1.2, name=f"fluor_light_{k}")
    screens = []
    hero = None
    for row in range(2):
        for col in range(3):
            dx, dy = -2.2 + col * 2.2, 8.4 + row * 2.6
            box(f"M13_desk_{row}_{col}", (dx, dy, 0.73), (1.6, 0.7, 0.05), m_desk)
            box(f"M19_crt_{row}_{col}", (dx, dy + 0.12, 1.0), (0.42, 0.42, 0.38), m_beige, bevel=0.04)
            scr = plane(f"M19_screen_{row}_{col}", (dx, dy - 0.095, 1.02), (0.33, 0.26), m_screen, rot=(math.radians(90), 0, 0))
            box(f"M19_tower_{row}_{col}", (dx + 0.55, dy + 0.1, 0.95), (0.2, 0.45, 0.42), m_beige)
            box(f"M19_kbd_{row}_{col}", (dx, dy - 0.25, 0.77), (0.45, 0.16, 0.025), m_beige)
            box(f"M13_chair_{row}_{col}", (dx, dy - 0.75, 0.45), (0.45, 0.45, 0.06), m_desk)
            screens.append(scr)
            if row == 0 and col == 1:
                hero = (dx, dy, scr)
    hx, hy, hscr = hero
    man, parts = figure("M03b_seated_man", (hx, hy - 0.72, 0.0), m_fig, seated=True, rot_z=math.radians(180))
    sun = light("SUN", (0, 0, 20), 5.5, (1.0, 0.80, 0.52), rot=(math.radians(38), 0, math.radians(150)), name="sun")
    return dict(door=door, man=man, parts=parts, hero=hero, screens=screens, m_screen=m_screen, m_pol=m_pol)


# ================================================================== SHOTS
if SHOT in ("SH-064", "SH-065", "SH-066", "SH-067"):
    S3 = build_s3()
    ws, crack, grow, sun = S3["ws"], S3["crack"], S3["grow"], S3["sun"]
    if SHOT == "SH-064":
        # fixed side profile from the passenger side: hands + sleeve only; sun streaks travel across
        cam, tgt = camera(35, (0.45, -0.55, 1.22), (-0.35, 0.45, 0.98), fstop=2.8, focus_obj=S3["wheel"])
        key(sun, "rotation_euler", 1, sun.rotation_euler.copy())
        key(sun, "rotation_euler", N, (sun.rotation_euler[0], sun.rotation_euler[1], sun.rotation_euler[2] + math.radians(28)))
        for o in [o for o in bpy.data.objects if o.name.startswith(("M07", "M08", "M09"))]:
            pass
        cab = [o for o in bpy.data.objects if o.name.startswith(("M07", "M08", "M09"))]
        bpy.ops.object.empty_add(location=(0, 0, 0)); rig = bpy.context.object; rig.name = "cabin_rig"
        for o in cab:
            o.parent = rig
        cam.parent = rig; tgt.parent = rig
        for f in range(1, N + 1, 6):
            key(rig, "location", f, (rng.uniform(-0.002, 0.002), 0, rng.uniform(-0.003, 0.003)))
    elif SHOT == "SH-065":
        # POV behind the windshield, slow turn + forward drift; smoke ahead; NO figure (smoke alone is enough)
        cam, tgt = camera(35, (-0.4, 0.15, 1.25), (-0.4, 30, 3.0), fstop=4.0)
        cam.data.dof.focus_distance = 0.8
        key(cam.data.dof, "focus_distance", 1, 0.8)
        key(cam.data.dof, "focus_distance", 100, 0.8)
        key(cam.data.dof, "focus_distance", 170, 30.0)
        bpy.ops.object.empty_add(location=(0, 0, 0)); rig = bpy.context.object; rig.name = "car_rig"
        for o in [o for o in bpy.data.objects if o.name.startswith(("M07", "M08", "M09", "FX02"))]:
            o.parent = rig
        cam.parent = rig; tgt.parent = rig
        key(rig, "location", 1, (0, 0, 0)); key(rig, "location", N, (0, 6, 0))
        key(rig, "rotation_euler", 1, (0, 0, math.radians(8))); key(rig, "rotation_euler", N, (0, 0, math.radians(-4)))
    elif SHOT == "SH-066":
        # locked ECU on the glass; crack decal grows in 3 steps; cut to white at f60
        cam, tgt = camera(50, (0.0, 0.05, 1.24), (0.25, 0.9, 1.32), fstop=8.0, focus_obj=crack)
        for f, v in ((1, 0.0), (19, 0.0), (20, 0.12), (25, 0.12), (26, 0.26), (31, 0.26), (32, 0.48)):
            grow.outputs[0].default_value = v
            grow.outputs[0].keyframe_insert("default_value", frame=f)
        interp(S3["crack"].data.materials[0].node_tree, "CONSTANT")
        key(sc.view_settings, "exposure", 1, -0.4)
        key(sc.view_settings, "exposure", 59, -0.4)
        key(sc.view_settings, "exposure", 60, 12.0)
        interp(sc, "CONSTANT")
    elif SHOT == "SH-067":
        # white → empty street through the symbolically cracked glass; extremely slow push
        grow.outputs[0].default_value = 0.48
        cam, tgt = camera(50, (-0.2, -0.35, 1.24), (0.4, 40, 4.5), fstop=5.6)
        cam.data.dof.focus_distance = 25
        key(cam, "location", 1, (-0.2, -0.35, 1.24)); key(cam, "location", N, (-0.2, -0.05, 1.24))
        key(sc.view_settings, "exposure", 1, 12.0); key(sc.view_settings, "exposure", 40, 12.0)
        key(sc.view_settings, "exposure", 140, -0.4)
        for o in bpy.data.objects:
            if o.name.startswith(("M08", "M09")):
                o.hide_render = True
    sc.view_settings.exposure = sc.view_settings.exposure

else:
    S4 = build_s4()
    hx, hy, hscr = S4["hero"]
    if SHOT == "SH-083":
        # 4A: street establishing shot, slow dolly toward the café entrance, starts overexposed (glare match)
        cam, tgt = camera(28, (-14, -4.2, 1.7), (0, 6, 3.2), fstop=8)
        key(cam, "location", 1, (-14, -4.2, 1.7)); key(cam, "location", N, (-9.5, -2.6, 1.7))
        key(sc.view_settings, "exposure", 1, 2.0); key(sc.view_settings, "exposure", 24, -0.5)
        mped = mat("ped", (0.25, 0.22, 0.2), 0.9)
        for k, (x0, y0, dx) in enumerate(((-14, -5.2, 1), (12, 5.0, -1), (-20, 5.2, 1))):
            p, _ = figure(f"pedestrian_{k}", (x0, y0, 0.08), mped, rot_z=math.radians(-90 * dx))
            key(p, "location", 1, (x0, y0, 0.08)); key(p, "location", N, (x0 + dx * 9, y0, 0.08))
    elif SHOT == "SH-084":
        # 4B: locked OTS on the seated man at a CRT; upper-right third kept calm for the 2D date graphic
        cam, tgt = camera(40, (hx + 1.0, hy - 2.7, 1.62), (hx - 0.1, hy, 1.0), fstop=2.8, focus_obj=hscr)
        ms = S4["m_screen"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        for f in range(1, N + 1, 7):
            ms.default_value = 1.2 * (1 + rng.uniform(-0.05, 0.05))
            ms.keyframe_insert("default_value", frame=f)
    elif SHOT == "SH-085":
        # 4C: rack focus screen → door; door opens; 4 plain-clothes officers walk in calmly; he turns, stays seated
        cam, tgt = camera(35, (hx + 2.4, hy + 0.9, 1.45), (hx - 0.9, 6.6, 1.1), fstop=2.8)
        key(cam.data.dof, "focus_distance", 1, 2.4); key(cam.data.dof, "focus_distance", 60, 2.4)
        key(cam.data.dof, "focus_distance", 100, 4.5)
        door = S4["door"]
        key(door, "location", 1, door.location.copy()); key(door, "location", 70, door.location.copy())
        key(door, "location", 84, door.location + Vector((-0.95, 0, 0)))
        for k in range(4):
            start = Vector((0.0 + (k - 1.5) * 0.25, 4.6, 0.02))
            end = Vector((hx - 1.9 + k * 0.5, hy - 1.3 - (k % 2) * 0.45, 0.02))
            p, pp = figure(f"M16_officer_{k}", tuple(start), S4["m_pol"][k], rot_z=0.0)
            f_in = 80 + k * 14
            for part in pp.values():
                part.hide_render = True; part.keyframe_insert("hide_render", frame=1)
                part.hide_render = False; part.keyframe_insert("hide_render", frame=f_in)
            key(p, "location", f_in, start + Vector((0, 1.6, 0)))
            key(p, "location", min(N, f_in + 70), end)
        man = S4["man"]
        key(man, "rotation_euler", 120, man.rotation_euler.copy())
        key(man, "rotation_euler", 150, (0, 0, man.rotation_euler[2] - math.radians(35)))
    elif SHOT == "SH-086":
        # 4D: locked ECU on the CRT; screen switches off; reflection of the man + officers in the dark glass
        cam, tgt = camera(50, (hx + 0.32, hy - 0.42, 1.08), (hx, hy - 0.09, 1.02), fstop=4, focus_obj=hscr)
        if hasattr(sc.eevee, "use_raytracing"):
            sc.eevee.use_raytracing = True
        ms = S4["m_screen"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        for f, v in ((1, 1.2), (30, 1.2), (36, 0.0)):
            ms.default_value = v; ms.keyframe_insert("default_value", frame=f)
        # officers standing behind him (only visible as a reflection)
        for k in range(3):
            figure(f"M16_officer_{k}", (hx - 0.7 + k * 0.7, hy - 1.9, 0.02), S4["m_pol"][k])

# ------------------------------------------------------------------ render settings
w, h = (int(v) for v in args.res.split("x"))
sc.render.resolution_x, sc.render.resolution_y = w, h
sc.eevee.taa_render_samples = args.samples
sc.frame_step = args.step
sc["shot_id"] = SHOT
sc["source_class"] = "DRAMATISED / ILLUSTRATIVE" if SHOT.startswith("SH-06") else "RECONSTRUCTED FROM EVIDENCE (S06–S10), generic set"
blend = os.path.join(OUT, f"{SHOT}_v001.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend)
print("saved", blend)
if args.render == "stills":
    for f in (1, N // 2, N):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(OUT, f"{SHOT}_still_f{f:04d}.png")
        bpy.ops.render.render(write_still=True)
elif args.render == "anim":
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.join(OUT, "frames", f"{SHOT}_")
    bpy.ops.render.render(animation=True)
print("done", SHOT)
