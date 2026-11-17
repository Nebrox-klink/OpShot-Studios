"""SH-031 · 3D 1 "Through the Glass" · opening shot (7 s @ 24 fps).

Builds the shared NOKAS courtyard set (M01), the lit window (M02, intact state),
a crouched stylised silhouette (M03b), a wall lamp (M04b) and frost (FX01),
animates a crane-down camera, and saves a .blend.

The set is a STYLISED, GENERIC reconstruction. It does not reproduce the real
NOKAS building, which we have no verified references for.

Usage (Blender 4.2+ / 5.x, or the bpy module):
  blender -b -P build_SH031_courtyard.py -- --out <dir> [--render stills|anim] [--res 1280x720] [--samples 16]
  python build_SH031_courtyard.py --out <dir> ...        (with `pip install bpy`)

On the Lenovo laptop: open the saved .blend and render with EEVEE, or run the
command above. Every material is procedural, and nothing needs an external
texture.
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

# ----------------------------------------------------------------- args
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--render", choices=["none", "stills", "anim"], default="none")
ap.add_argument("--res", default="1280x720")
ap.add_argument("--samples", type=int, default=16)
ap.add_argument("--frames", default="")  # e.g. "1,84,168" for stills
args = ap.parse_args(argv)
OUT = os.path.abspath(args.out)
os.makedirs(OUT, exist_ok=True)

FPS, F_START, F_END = 24, 1, 168  # 7.0 s

# Palette (style guide 02_VISUAL_DEVELOPMENT/style_guide/THE_GLASS_style_guide.md)
NAVY = (0.009, 0.016, 0.024)      # #17212B in linear-ish
SLATE = (0.10, 0.13, 0.155)       # #556774 darkened
AMBER = (1.0, 0.55, 0.25)         # #C78B55 warm light
IVORY = (0.81, 0.79, 0.74)        # #E9E6DE


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def mat(name, base, rough=0.8, emit=None, emit_strength=0.0, noise_scale=None, noise_mix=0.0,
        frost=False, transmission=0.0, alpha=1.0, spec=0.3):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base, 1)
    bsdf.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = spec
    if transmission:
        bsdf.inputs["Transmission Weight"].default_value = transmission
        bsdf.inputs["IOR"].default_value = 1.52
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    if emit:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1)
        bsdf.inputs["Emission Strength"].default_value = emit_strength
    if noise_scale:
        tex = nt.nodes.new("ShaderNodeTexNoise")
        tex.inputs["Scale"].default_value = noise_scale
        tex.inputs["Detail"].default_value = 8
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*[c * (1 - noise_mix) for c in base], 1)
        ramp.color_ramp.elements[1].color = (*[min(1, c * (1 + noise_mix)) for c in base], 1)
        nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
        out = ramp.outputs["Color"]
        if frost:
            # white-blue frost patches mixed by a second, larger noise
            tex2 = nt.nodes.new("ShaderNodeTexNoise")
            tex2.inputs["Scale"].default_value = 26.0
            tex2.inputs["Detail"].default_value = 6
            r2 = nt.nodes.new("ShaderNodeValToRGB")
            r2.color_ramp.elements[0].position = 0.52
            r2.color_ramp.elements[1].position = 0.62
            mix = nt.nodes.new("ShaderNodeMix")
            mix.data_type = "RGBA"
            mix.inputs[7].default_value = (0.082, 0.092, 0.104, 1)  # frost colour (B input), subtle
            nt.links.new(tex2.outputs["Fac"], r2.inputs["Fac"])
            nt.links.new(r2.outputs["Color"], mix.inputs["Factor"])
            nt.links.new(out, mix.inputs[6])
            out = mix.outputs[2]
            rmix = nt.nodes.new("ShaderNodeMapRange")
            rmix.inputs["To Min"].default_value = rough
            rmix.inputs["To Max"].default_value = 0.45
            nt.links.new(r2.outputs["Color"], rmix.inputs["Value"])
            nt.links.new(rmix.outputs["Result"], bsdf.inputs["Roughness"])
        nt.links.new(out, bsdf.inputs["Base Color"])
    return m


def box(name, loc, size, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    o.data.materials.append(material)
    return o


def build():
    reset()
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
    w, h = (int(v) for v in args.res.split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = F_START, F_END
    sc.eevee.taa_render_samples = args.samples
    for attr, val in (("shadow_ray_count", 1), ("shadow_step_count", 2), ("use_raytracing", False)):
        if hasattr(sc.eevee, attr):
            setattr(sc.eevee, attr, val)
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Base Contrast" if "AgX - Base Contrast" in [i.identifier for i in sc.view_settings.bl_rna.properties["look"].enum_items] else "None"
    sc.view_settings.exposure = 0.9

    # world: deep navy pre-dawn sky
    world = bpy.data.worlds.new("NightSky")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.012, 0.020, 0.034, 1)
    bg.inputs["Strength"].default_value = 0.9

    # --------------------------------------------------- materials
    m_ground = mat("M01_ground_cobble_frost", (0.050, 0.055, 0.060), rough=0.85, noise_scale=38,
                   noise_mix=0.45, frost=True)
    m_wall = mat("M01_wall_plaster", (0.105, 0.115, 0.115), rough=0.95, noise_scale=6, noise_mix=0.25)
    m_wall2 = mat("M01_wall_plaster_dark", (0.060, 0.068, 0.072), rough=0.95, noise_scale=5, noise_mix=0.3)
    m_trim = mat("M01_trim_concrete", (0.14, 0.145, 0.14), rough=0.9, noise_scale=12, noise_mix=0.2)
    m_frame = mat("M02_window_frame_steel", (0.035, 0.04, 0.045), rough=0.45, spec=0.5)
    m_glass = mat("M02_glass_laminated", (0.42, 0.58, 0.50), rough=0.08, alpha=0.16, spec=0.7)  # alpha-blended: EEVEE-laptop friendly
    m_room = mat("M06_room_wall", (0.55, 0.42, 0.30), rough=0.9, emit=(1.0, 0.62, 0.32), emit_strength=0.9)
    m_room_props = mat("M06_room_props", (0.12, 0.09, 0.07), rough=0.9)
    m_ceiling = mat("M06_ceiling_light", (1, 0.85, 0.65), emit=(1.0, 0.78, 0.52), emit_strength=12)
    m_fig = mat("M03b_silhouette_cloth", (0.018, 0.020, 0.024), rough=0.9, spec=0.25)
    m_lamp = mat("M04b_lamp_emit", (0.9, 0.95, 1.0), emit=(0.75, 0.86, 1.0), emit_strength=18)
    m_metal = mat("props_metal", (0.05, 0.055, 0.06), rough=0.5, spec=0.5)
    m_door = mat("props_door", (0.04, 0.05, 0.055), rough=0.7)

    # --------------------------------------------------- M01 courtyard
    W, D, H = 11.0, 9.0, 9.5  # courtyard width (x), depth (y), wall height
    box("ground", (0, 0, -0.05), (W + 2, D + 2, 0.1), m_ground)
    # back wall (NOKAS facade) at y = +D/2, with window opening
    win_w, win_h, sill = 2.2, 1.6, 0.9
    wx = 0.6  # window centre x
    t = 0.45  # wall thickness
    yb = D / 2
    # build back wall from 4 pieces around window
    box("wall_back_L", (-(W / 2) + (W / 2 + wx - win_w / 2) / 2, yb + t / 2, H / 2), (W / 2 + wx - win_w / 2, t, H), m_wall)
    rw = W / 2 - (wx + win_w / 2)
    box("wall_back_R", (wx + win_w / 2 + rw / 2, yb + t / 2, H / 2), (rw, t, H), m_wall)
    box("wall_back_bottom", (wx, yb + t / 2, sill / 2), (win_w, t, sill), m_wall)
    top_h = H - sill - win_h
    box("wall_back_top", (wx, yb + t / 2, sill + win_h + top_h / 2), (win_w, t, top_h), m_wall)
    # side walls + front wall
    box("wall_left", (-W / 2 - t / 2, 0, H / 2 + 0.6), (t, D + 2 * t, H + 1.2), m_wall2)
    box("wall_right", (W / 2 + t / 2, 0, H / 2 - 1.2), (t, D + 2 * t, H - 2.4), m_wall2)
    box("wall_front", (0, -D / 2 - t / 2, H / 2), (W + 2 * t, t, H), m_wall2)
    # parapets / roof edges
    for nm, loc, sz in (("parapet_back", (0, yb + 0.35, H + 0.15), (W + 1.0, 1.0, 0.3)),
                        ("parapet_left", (-W / 2 - 0.4, 0, H + 0.75), (1.0, D + 1, 0.3)),
                        ("parapet_right", (W / 2 + 0.4, 0, H - 2.25), (1.0, D + 1, 0.3))):
        box(nm, loc, sz, m_trim)
    # horizontal string course + sill
    box("string_course", (0, yb - 0.05, 3.6), (W, 0.12, 0.18), m_trim)
    box("window_sill", (wx, yb - 0.12, sill - 0.04), (win_w + 0.3, 0.3, 0.08), m_trim)
    # steel door + drainpipe + utility box for scale
    box("door_service", (-3.6, yb - 0.02, 1.1), (1.1, 0.08, 2.2), m_door)
    box("door_frame", (-3.6, yb - 0.01, 1.15), (1.3, 0.05, 2.35), m_metal)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=H, location=(-1.6, yb - 0.12, H / 2))
    bpy.context.object.name = "drainpipe"
    bpy.context.object.data.materials.append(m_metal)
    box("utility_box", (4.2, yb - 0.25, 0.5), (0.9, 0.5, 1.0), m_metal, bevel=0.03)
    box("bin_A", (-W / 2 + 0.7, 2.2, 0.55), (0.9, 0.8, 1.1), m_metal, bevel=0.04)

    # --------------------------------------------------- M02 window
    fr = 0.07
    for nm, loc, sz in (("frame_top", (wx, yb, sill + win_h - fr / 2), (win_w, 0.16, fr)),
                        ("frame_bot", (wx, yb, sill + fr / 2), (win_w, 0.16, fr)),
                        ("frame_L", (wx - win_w / 2 + fr / 2, yb, sill + win_h / 2), (fr, 0.16, win_h)),
                        ("frame_R", (wx + win_w / 2 - fr / 2, yb, sill + win_h / 2), (fr, 0.16, win_h)),
                        ("frame_mullion", (wx, yb, sill + win_h / 2), (0.05, 0.12, win_h))):
        box(nm, loc, sz, m_frame)
    # laminated glass: three thin layers, slightly separated (reads as thick armoured glass)
    for i, dy in enumerate((-0.03, 0.0, 0.03)):
        g = box(f"glass_layer_{i}", (wx, yb + dy, sill + win_h / 2), (win_w - 2 * fr, 0.008, win_h - 2 * fr), m_glass)

    # --------------------------------------------------- M06 room behind window (warm)
    ry = yb + t + 2.0
    box("room_back", (wx, ry + 2.0, 2.0), (6, 0.1, 4), m_room)
    box("room_side_L", (wx - 3.0, ry, 2.0), (0.1, 4.2, 4), m_room)
    box("room_side_R", (wx + 3.0, ry, 2.0), (0.1, 4.2, 4), m_room)
    box("room_ceiling", (wx, ry, 3.05), (6, 4.2, 0.1), m_room_props)
    box("room_floor", (wx, ry, 0.0), (6, 4.2, 0.05), m_room_props)
    box("room_ceiling_light", (wx, ry, 2.95), (2.2, 0.5, 0.05), m_ceiling)
    box("room_shelf", (wx - 1.6, ry + 1.4, 1.0), (1.4, 0.5, 2.0), m_room_props)
    box("room_table", (wx + 0.8, ry + 0.4, 0.75), (1.6, 0.8, 0.08), m_room_props)
    for i, lx in enumerate((-1.2, 1.4)):
        bpy.ops.object.light_add(type="POINT", location=(wx + lx, ry - 0.6, 2.4))
        pl = bpy.context.object
        pl.name = f"room_light_{i}"
        pl.data.energy = 350
        pl.data.color = AMBER
        pl.data.shadow_soft_size = 0.05
    # two blurred staff silhouettes (M21) far behind the glass, read as shapes only
    box("M21_staff_A", (wx - 0.9, ry + 0.9, 0.85), (0.45, 0.3, 1.7), m_room_props, bevel=0.15)
    box("M20_trolley_A", (wx - 0.3, ry + 0.8, 0.45), (0.8, 0.5, 0.9), m_room_props, bevel=0.03)
    bpy.ops.object.light_add(type="AREA", location=(wx, yb + t + 0.6, sill + win_h / 2))
    l = bpy.context.object
    l.name = "window_spill_light"
    l.data.shape = "RECTANGLE"
    l.data.size, l.data.size_y = win_w, win_h
    l.data.energy = 520
    l.data.color = AMBER
    l.rotation_euler = (math.radians(-90), 0, 0)  # local -Z -> world -Y (into courtyard)

    # --------------------------------------------------- M04b wall lamp (cold)
    box("lamp_arm", (3.0, yb - 0.25, 3.2), (0.08, 0.5, 0.08), m_metal)
    box("lamp_head", (3.0, yb - 0.5, 3.12), (0.35, 0.22, 0.12), m_lamp)
    bpy.ops.object.light_add(type="SPOT", location=(3.0, yb - 0.5, 3.0))
    s = bpy.context.object
    s.name = "lamp_spot"
    s.data.energy = 260
    s.data.color = (0.72, 0.84, 1.0)
    s.data.spot_size = math.radians(110)
    s.data.spot_blend = 0.8
    s.data.shadow_soft_size = 0.05
    s.rotation_euler = (0, 0, 0)

    # cold moonlight / pre-dawn sun
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 20))
    sun = bpy.context.object
    sun.data.energy = 0.35
    sun.data.color = (0.55, 0.68, 1.0)
    sun.rotation_euler = (math.radians(50), math.radians(-20), math.radians(30))

    # --------------------------------------------------- M03b crouched silhouette
    fig_loc = Vector((wx - 1.15, yb - 0.55, 0))
    parts = []
    def ellipsoid(name, loc, scale, rot=(0, 0, 0)):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=fig_loc + Vector(loc))
        o = bpy.context.object
        o.name = name
        o.scale = scale
        o.rotation_euler = rot
        bpy.ops.object.shade_smooth()
        o.data.materials.append(m_fig)
        parts.append(o)
        return o
    def bbox(name, loc, size, rot=(0, 0, 0), bev=0.06):
        o = box(name, fig_loc + Vector(loc), size, m_fig, bevel=bev)
        o.rotation_euler = rot
        parts.append(o)
        return o
    # crouched, hugging knees, hood up, back to camera: angular jacket shapes read as a person, not a toy
    torso = bbox("M03b_torso", (0, 0.02, 0.72), (0.46, 0.30, 0.62), (math.radians(-28), 0, 0), bev=0.12)
    bbox("M03b_shoulders", (0, -0.06, 0.98), (0.50, 0.26, 0.16), (math.radians(-28), 0, 0), bev=0.07)
    ellipsoid("M03b_head_hood", (0, -0.17, 1.13), (0.105, 0.12, 0.125), (math.radians(-15), 0, 0))
    bbox("M03b_hood_peak", (0, -0.25, 1.17), (0.18, 0.08, 0.10), (math.radians(-35), 0, 0), bev=0.03)
    bbox("M03b_thigh_L", (-0.12, -0.24, 0.50), (0.16, 0.46, 0.17), (math.radians(-38), 0, 0), bev=0.06)
    bbox("M03b_thigh_R", (0.13, -0.26, 0.48), (0.16, 0.46, 0.17), (math.radians(-34), 0, 0), bev=0.06)
    bbox("M03b_shin_L", (-0.12, -0.44, 0.24), (0.13, 0.14, 0.46), bev=0.05)
    bbox("M03b_shin_R", (0.14, -0.47, 0.23), (0.13, 0.14, 0.44), bev=0.05)
    bbox("M03b_boot_L", (-0.12, -0.52, 0.05), (0.14, 0.28, 0.10), bev=0.04)
    bbox("M03b_boot_R", (0.14, -0.55, 0.05), (0.14, 0.28, 0.10), bev=0.04)
    bbox("M03b_arm_L", (-0.25, -0.28, 0.70), (0.12, 0.42, 0.12), (math.radians(-12), 0, math.radians(14)), bev=0.05)
    bbox("M03b_arm_R", (0.26, -0.30, 0.68), (0.12, 0.42, 0.12), (math.radians(-12), 0, math.radians(-14)), bev=0.05)
    # breathing: torso scale
    for f, s in ((1, 1.0), (40, 1.03), (80, 1.0), (120, 1.03), (168, 1.0)):
        torso.scale = (s, s, 1.0)
        torso.keyframe_insert("scale", frame=f)
    # parent all to an empty so the figure can be moved as one
    bpy.ops.object.empty_add(location=fig_loc)
    root = bpy.context.object
    root.name = "M03b_root"
    for p in parts:
        p.parent = root
        p.matrix_parent_inverse = root.matrix_world.inverted()
    root.rotation_euler = (0, 0, math.radians(8))  # faces the wall/window a little
    # cold rim light from the lamp side + low fill so the dark silhouette separates from the dark wall
    bpy.ops.object.light_add(type="AREA", location=(fig_loc.x + 1.6, fig_loc.y - 0.2, 1.4))
    rim = bpy.context.object
    rim.name = "rim_figure_cold"
    rim.data.energy = 60
    rim.data.size = 0.6
    rim.data.color = (0.62, 0.78, 1.0)
    rim.rotation_euler = (0, math.radians(-90), 0)  # local -Z -> world -X (towards figure)
    bpy.ops.object.light_add(type="AREA", location=(fig_loc.x - 0.4, fig_loc.y - 2.2, 2.2))
    fill = bpy.context.object
    fill.name = "fill_back_cold"
    fill.data.energy = 25
    fill.data.size = 2.0
    fill.data.color = (0.45, 0.58, 0.85)
    fill.rotation_euler = (math.radians(-60), 0, 0)

    # --------------------------------------------------- camera crane
    bpy.ops.object.empty_add(location=(wx - 0.2, yb, 1.55))
    target = bpy.context.object
    target.name = "cam_target_window"
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.name = "CAM_SH031_crane"
    sc.camera = cam
    tc = cam.constraints.new("TRACK_TO")
    tc.target = target
    tc.track_axis = "TRACK_NEGATIVE_Z"
    tc.up_axis = "UP_Y"
    cam.data.sensor_width = 36
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = root
    cam.data.dof.aperture_fstop = 4.0
    # path: start above the front-left parapet, looking down; end low behind the figure
    keys = [
        (1,   (-3.8, -3.6, 10.6), 24, (wx - 0.4, yb - 1.0, 0.4)),
        (60,  (-3.0, -2.3, 7.4), 26, (wx - 0.4, yb - 0.6, 0.7)),
        (120, (-2.2, -0.9, 3.0), 29, (wx - 0.3, yb - 0.2, 1.1)),
        (168, (-1.75, 0.95, 1.42), 32, (wx - 0.05, yb, 1.45)),
    ]
    for f, loc, lens, tgt in keys:
        cam.location = loc
        cam.data.lens = lens
        target.location = tgt
        cam.keyframe_insert("location", frame=f)
        cam.data.keyframe_insert("lens", frame=f)
        target.keyframe_insert("location", frame=f)
    for ob in (cam, target):
        if ob.animation_data and ob.animation_data.action:
            act = ob.animation_data.action
            curves = getattr(act, "fcurves", None)
            if curves is None:  # Blender 5 layered actions
                curves = [c for layer in act.layers for strip in layer.strips for cb in strip.channelbags for c in cb.fcurves]
            for fc in curves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
                    kp.easing = "AUTO"

    # metadata for continuity with SH-050 (3D 2 reuses this set)
    sc["shot_id"] = "SH-031"
    sc["sequence"] = "3D 1 · Through the Glass"
    sc["source_class"] = "RECONSTRUCTED FROM EVIDENCE (S04,S05) – lighting/weather dramatised"
    return sc


sc = build()
blend = os.path.join(OUT, "SH-031_courtyard_v001.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend)
print("saved", blend)

if args.render == "stills":
    frames = [int(f) for f in (args.frames or "1,84,168").split(",")]
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(OUT, f"SH-031_still_f{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print("still", sc.render.filepath)
elif args.render == "anim":
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.join(OUT, "frames", "SH-031_")
    bpy.ops.render.render(animation=True)
    print("anim done")
