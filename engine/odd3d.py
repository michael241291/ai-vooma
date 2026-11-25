"""3D odd-one-out (Blender/Cycles): a grid of 3D donuts on a Pixabay marble counter; one donut has no hole.
Camera drifts during the search, then flies to the odd donut for the reveal.

Usage: python3 engine/odd3d.py episodes/<id>/odd.json [--preview 0,150,300]
odd.json: fps, dur, seed, cols, rows, odd (index or -1 random), counter (texture path), icing colors,
          reveal_t, out_dir, res_pct, samples
Writes <out_dir>/frames/####.png (RGBA) and <out_dir>/layout.json (odd donut screen pos at the end).
"""
import json
import math
import os
import random
import sys

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(sys.argv[1]))
OUT = C['out_dir']
FPS, DUR = C.get('fps', 25), C.get('dur', 13.0)
N = int(round(FPS * DUR))
rng = random.Random(C.get('seed', 3))


def hexcol(h):
    h = h.lstrip('#'); s = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in s], 1.0)


def ease(u):
    u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = C.get('res_pct', 50); sc.render.fps = FPS
sc.frame_start, sc.frame_end = 0, N - 1
sc.render.film_transparent = True; sc.render.image_settings.color_mode = 'RGBA'
sc.render.use_persistent_data = True
sc.render.use_overwrite = False; sc.render.use_placeholder = True  # resumable
cy = sc.cycles; cy.device = 'CPU'; cy.samples = C.get('samples', 10); cy.use_adaptive_sampling = True
cy.adaptive_threshold = 0.05; cy.use_denoising = True; cy.denoising_prefilter = 'FAST'
cy.max_bounces = 3; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.transmission_bounces = 1; cy.transparent_max_bounces = 2
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.9, 0.85, 0.8, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.5


def mat(name, col, rough=0.5, coat=0.0, sss=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol(col); b.inputs['Roughness'].default_value = rough
    b.inputs['Coat Weight'].default_value = coat
    if sss:
        b.inputs['Subsurface Weight'].default_value = sss
    return m


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True


# counter
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.6, 0)); top = bpy.context.object
top.scale = (9, 14, 1); bpy.ops.object.transform_apply(scale=True)
m = bpy.data.materials.new('marble'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(ROOT, C['counter']))
mp = nt.nodes.new('ShaderNodeMapping'); tc = nt.nodes.new('ShaderNodeTexCoord')
mp.inputs['Scale'].default_value = (1.0, 1.6, 1)
nt.links.new(tc.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
nt.links.new(tex.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.25
top.data.materials.append(m)

dough = mat('dough', '#D9944A', 0.6, sss=0.1)
icings = [mat(f'ice{i}', c, 0.3, coat=0.4) for i, c in enumerate(C.get('icing', ['#FF7FAF']))]
spr_cols = [mat(f'spr{i}', c, 0.35) for i, c in enumerate(['#FFFFFF', '#FFD23F', '#2EC4B6', '#7B61FF', '#FF2E63'])]

# donut templates (meshes reused via linked data)
bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.2, major_segments=48, minor_segments=20)
t_dough = bpy.context.object; smooth(t_dough); t_dough.data.materials.append(dough)
bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.205, major_segments=48, minor_segments=20)
t_ice = bpy.context.object; smooth(t_ice); t_ice.data.materials.append(icings[0])
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.11, vertices=8)
t_spr = bpy.context.object; smooth(t_spr); t_spr.data.materials.append(spr_cols[0])
bpy.ops.mesh.primitive_cylinder_add(radius=0.27, depth=0.34, vertices=40)
t_fill = bpy.context.object; smooth(t_fill); t_fill.data.materials.append(dough)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.27, segments=32, ring_count=16)
t_cap = bpy.context.object; smooth(t_cap); t_cap.data.materials.append(icings[0])
templates = [t_dough, t_ice, t_spr, t_fill, t_cap]
for t in templates:
    t.hide_render = True; t.hide_viewport = True; t.location = (100, 100, 0)


def inst(tpl, parent, loc, rot=(0, 0, 0), scale=(1, 1, 1), material=None):
    o = bpy.data.objects.new(tpl.name + '_i', tpl.data)
    bpy.context.collection.objects.link(o)
    o.parent = parent; o.location = loc; o.rotation_euler = rot; o.scale = scale
    if material is not None:
        o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = material
    return o


cols, rows = C.get('cols', 4), C.get('rows', 6)
sp = C.get('spacing', 1.32)
n = cols * rows
odd = C.get('odd', -1)
if odd < 0:
    odd = rng.choice([i for i in range(n) if 0 < i % cols < cols - 1 and 0 < i // cols < rows - 1])
positions = []
for i in range(n):
    c, r = i % cols, i // cols
    x = (c - (cols - 1) / 2) * sp + rng.uniform(-0.06, 0.06)
    y = (rows - 1 - r - (rows - 1) / 2) * sp + 0.6 + rng.uniform(-0.06, 0.06)
    positions.append((x, y))
    bpy.ops.object.empty_add(location=(x, y, 0.2)); root = bpy.context.object
    root.rotation_euler = (0, 0, rng.uniform(0, 6.28)); s = rng.uniform(0.95, 1.04); root.scale = (s, s, s)
    ice_m = rng.choice(icings) if C.get('mix_icing') else icings[0]
    inst(t_dough, root, (0, 0, 0))
    inst(t_ice, root, (0, 0, 0.1), scale=(1, 1, 0.7), material=ice_m)
    otype = C.get('odd_type', 'nohole')
    if i == odd and otype == 'nohole':
        inst(t_fill, root, (0, 0, 0.0))
        inst(t_cap, root, (0, 0, 0.15), scale=(1, 1, 0.3), material=ice_m)
    for k in range(0 if (i == odd and otype == 'nosprinkles') else 16):
        th = rng.uniform(0, 6.28)
        rr = rng.uniform(0.3, 0.55) if (i != odd or otype != 'nohole') else rng.uniform(0.05, 0.55)
        h = 0.1 + 0.7 * math.sqrt(max(0, 0.205 ** 2 - (rr - 0.42) ** 2)) if rr > 0.25 else 0.15 + 0.3 * 0.27 * math.sqrt(max(0, 1 - (rr / 0.27) ** 2))
        inst(t_spr, root, (rr * math.cos(th), rr * math.sin(th), h + 0.012),
             rot=(math.radians(90), 0, rng.uniform(0, 6.28)), material=rng.choice(spr_cols))

# lights
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 7)); k = bpy.context.object
k.data.energy = 1400; k.data.size = 5; k.data.color = (1, 0.93, 0.85); k.rotation_euler = (math.radians(30), math.radians(-20), 0)
bpy.ops.object.light_add(type='AREA', location=(3.5, 4, 5)); r_ = bpy.context.object
r_.data.energy = 500; r_.data.size = 4; r_.data.color = (0.8, 0.88, 1); r_.rotation_euler = (math.radians(-40), math.radians(30), 0)

# camera
bpy.ops.object.camera_add(location=(0, -6.4, 11.2)); cam = bpy.context.object
sc.camera = cam; cam.data.lens = C.get('lens', 30); cam.data.sensor_fit = 'VERTICAL'
bpy.ops.object.empty_add(location=(0, 0.75, 0)); tgt = bpy.context.object
tcn = cam.constraints.new('TRACK_TO'); tcn.target = tgt; tcn.track_axis = 'TRACK_NEGATIVE_Z'; tcn.up_axis = 'UP_Y'
cam.data.dof.use_dof = True; cam.data.dof.focus_object = tgt; cam.data.dof.aperture_fstop = 5.6

reveal_t = C.get('reveal_t', 9.0)
ox, oy = positions[odd]
home_cam, home_tgt = Vector(C.get('cam', (0, -6.4, 11.2))), Vector((0, 0.75, 0))
near_cam, near_tgt = Vector((ox, oy - 2.0, 3.8)), Vector((ox, oy, 0.2))
for f in range(N):
    t = f / FPS
    u = ease((t - reveal_t) / 0.9)
    drift = Vector((0.35 * math.sin(t * 0.5), 0.15 * math.sin(t * 0.37), -0.25 * min(1, t / reveal_t)))
    cam.location = home_cam.lerp(near_cam, u) + drift * (1 - u)
    tgt.location = home_tgt.lerp(near_tgt, u)
    cam.keyframe_insert('location', frame=f); tgt.keyframe_insert('location', frame=f)

sc.frame_set(N - 1)
v = world_to_camera_view(sc, cam, Vector((ox, oy, 0.25)))
os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
json.dump({'fps': FPS, 'dur': DUR, 'odd': odd, 'odd_px_end': [round(v.x * 1080), round((1 - v.y) * 1920)],
           'reveal_t': reveal_t}, open(os.path.join(OUT, 'layout.json'), 'w'), indent=1)
print('ODD', odd, positions[odd])

if '--preview' in sys.argv:
    for f in [int(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, 'frames', f'prev_{f:04d}.png')
        bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(OUT, 'frames', ''); bpy.ops.render.render(animation=True)
