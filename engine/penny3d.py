"""3D 'would you rather': A = a pallet of $1,000,000 cash, B = one penny that doubles every day for 30 days.
The penny becomes a copper coin column whose height is proportional to its dollar value (cash pallet height = $1M),
so it stays invisible for most of the month and then shoots past the cash at the end.

Usage: python3 engine/penny3d.py episodes/<id>/penny.json [--preview 0,300,600]
penny.json: fps, dur, day_keys [[t, day], ...] (piecewise-linear, held between keys), table, out_dir, res_pct, samples
Writes frames + layout.json (day per frame for captions).
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(sys.argv[1]))
OUT = C['out_dir']
FPS, DUR = C.get('fps', 25), C.get('dur', 27.5)
N = int(round(FPS * DUR))


def hexcol(h):
    h = h.lstrip('#'); s = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in s], 1.0)


def ease(u):
    u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


def day_at(t):
    keys = C['day_keys']
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, d0), (t1, d1) in zip(keys, keys[1:]):
        if t <= t1:
            return d0 + (d1 - d0) * ease((t - t0) / max(1e-6, t1 - t0))
    return keys[-1][1]


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
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.85, 0.8, 0.75, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.45


def mat(name, col, rough=0.5, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol(col); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; b.inputs['Coat Weight'].default_value = coat
    return m


def copper():
    m = bpy.data.materials.new('copper'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol('#C8743E'); b.inputs['Metallic'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.3
    # coin-edge ridges: wave texture along Z drives a bump
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'
    wv.inputs['Scale'].default_value = 60; tc = nt.nodes.new('ShaderNodeTexCoord')
    nt.links.new(tc.outputs['Object'], wv.inputs['Vector'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35
    nt.links.new(wv.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def box(loc, size, material, bevel=0.01):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = o.modifiers.new('b', 'BEVEL'); b.width = bevel; b.segments = 2
    o.data.materials.append(material); return o


# table
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 1.5, 0)); top = bpy.context.object
top.scale = (14, 14, 1); bpy.ops.object.transform_apply(scale=True)
m = bpy.data.materials.new('table'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(ROOT, C['table']))
mp = nt.nodes.new('ShaderNodeMapping'); tcn = nt.nodes.new('ShaderNodeTexCoord'); mp.inputs['Scale'].default_value = (2.5, 2.5, 1)
nt.links.new(tcn.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
nt.links.new(tex.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.35
top.data.materials.append(m)

# A: $1,000,000 = 100 bundles of $10,000 ($100 bills), stacked 4 x 5 x 5
cash_x = -0.5
bill = mat('bill', '#BFD3B4', 0.6); band = mat('band', '#F4E3B5', 0.5)
bw, bd, bh = 0.30, 0.14, 0.095
for i in range(4):
    for j in range(5):
        for k in range(5):
            x = cash_x + (i - 1.5) * (bw + 0.006); y = (j - 2) * (bd + 0.006); z = bh / 2 + k * (bh + 0.004)
            box((x, y, z), (bw, bd, bh), bill, 0.004)
            box((x, y, z), (0.06, bd + 0.004, bh + 0.004), band, 0)
CASH_H = 5 * (bh + 0.004)   # height of $1,000,000

# B: the penny column (one cylinder, height = value scaled to CASH_H per $1M; never thinner than one coin)
pen_x = 0.62
bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=1.0, vertices=64, location=(pen_x, 0, 0.5))
col = bpy.context.object
for p in col.data.polygons:
    p.use_smooth = True
col.data.materials.append(copper())
bev = col.modifiers.new('b', 'BEVEL'); bev.width = 0.004; bev.segments = 2
# move origin to the bottom so scaling Z grows upward
bpy.context.scene.cursor.location = (pen_x, 0, 0); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
COIN = 0.02

# lights
bpy.ops.object.light_add(type='AREA', location=(-3, -4, 6)); k1 = bpy.context.object
k1.data.energy = 1600; k1.data.size = 5; k1.data.color = (1, 0.92, 0.85); k1.rotation_euler = (math.radians(40), math.radians(-25), 0)
bpy.ops.object.light_add(type='AREA', location=(4, 3, 5)); k2 = bpy.context.object
k2.data.energy = 700; k2.data.size = 4; k2.data.color = (0.8, 0.88, 1); k2.rotation_euler = (math.radians(-40), math.radians(35), 0)

# camera
bpy.ops.object.camera_add(location=(0, -5.0, 2.0)); cam = bpy.context.object
sc.camera = cam; cam.data.lens = 30; cam.data.sensor_fit = 'VERTICAL'
bpy.ops.object.empty_add(location=(0, 0, 0.4)); tgt = bpy.context.object
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'

days = []
for f in range(N):
    t = f / FPS
    d = day_at(t)
    value = 0.01 * 2 ** (d - 1)
    h = max(COIN, value / 1e6 * CASH_H)
    col.scale = (1, 1, h); col.keyframe_insert('scale', frame=f)
    # camera: frames both stacks, then pulls back and up as the column outgrows the cash
    top_z = max(CASH_H, h)
    dist = 5.0 + 1.5 * max(0.0, top_z - CASH_H)
    cam.location = (0.1 * math.sin(t * 0.4), -dist, 2.0 + 0.5 * max(0.0, top_z - CASH_H))
    tgt.location = (0.05, 0.0, 0.25 + 0.5 * max(0.0, top_z - CASH_H))
    cam.keyframe_insert('location', frame=f); tgt.keyframe_insert('location', frame=f)
    days.append(round(d, 3))

os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
json.dump({'fps': FPS, 'dur': DUR, 'days': days}, open(os.path.join(OUT, 'layout.json'), 'w'))
print('FINAL HEIGHT', round(max(COIN, 0.01 * 2 ** 29 / 1e6 * CASH_H), 2), 'cash', round(CASH_H, 2))

if '--preview' in sys.argv:
    for f in [int(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, 'frames', f'prev_{f:04d}.png')
        bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(OUT, 'frames', ''); bpy.ops.render.render(animation=True)
