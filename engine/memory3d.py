"""3D memory test (Blender/Cycles): 6 gift boxes on a table, MEMORIZE countdown, lights go out, one box changes,
lights come back, viewers comment 1-6, then the changed box hops for the reveal.

Usage: python3 engine/memory3d.py episodes/<id>/memory.json [--preview 0,140,300]
memory.json: fps, dur, seed, colors (6 box colors), ribbon, changed (index 0-5 or -1), new_color, table (texture),
             t_dark0, t_dark1, reveal_t, out_dir, res_pct, samples
Writes frames + layout.json (box screen positions, answer 1-6).
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
rng = random.Random(C.get('seed', 4))


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
bgn = w.node_tree.nodes['Background']; bgn.inputs['Color'].default_value = (0.8, 0.7, 0.6, 1)
bgn.inputs['Strength'].default_value = 0.4


def mat(name, col, rough=0.45, coat=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol(col); b.inputs['Roughness'].default_value = rough
    b.inputs['Coat Weight'].default_value = coat; b.inputs['Metallic'].default_value = metal
    return m


def cube(loc, size, material, parent=None, bevel=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = o.modifiers.new('b', 'BEVEL'); b.width = bevel; b.segments = 3
    o.data.materials.append(material)
    if parent:
        o.parent = parent; o.location = loc
    return o


# table
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.5, 0)); top = bpy.context.object
top.scale = (10, 8, 1); bpy.ops.object.transform_apply(scale=True)
m = bpy.data.materials.new('table'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(ROOT, C['table']))
mp = nt.nodes.new('ShaderNodeMapping'); tc = nt.nodes.new('ShaderNodeTexCoord'); mp.inputs['Scale'].default_value = (1.4, 1.1, 1)
nt.links.new(tc.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
nt.links.new(tex.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.45
top.data.materials.append(m)

cols = C.get('colors', ['#E63946', '#2A9D8F', '#F4A261', '#7B61FF', '#FFD23F', '#3A86FF'])
rib_m = mat('ribbon', C.get('ribbon', '#FFFFFF'), 0.3, coat=0.5)
gold = mat('gold', '#F2C14E', 0.25, metal=1.0)
changed = C.get('changed', -1)
if changed < 0:
    changed = rng.randrange(6)
new_col = C.get('new_color', '#FF8FC7')

slots = []
for i in range(6):
    r, c = divmod(i, 3)
    x = (c - 1) * 1.5
    y = 1.0 - r * 2.0
    s = [1.0, 0.85, 1.1, 0.95, 1.05, 0.9][i]
    slots.append((x, y, s))


def gift(name, x, y, s, col, ribbon=rib_m):
    bpy.ops.object.empty_add(location=(x, y, 0)); root = bpy.context.object; root.name = name
    bm = mat(name + '_m', col, 0.5, coat=0.3)
    h = 0.85 * s; wdt = 0.95 * s
    cube((0, 0, h / 2), (wdt, wdt, h), bm, root)
    cube((0, 0, h + 0.06), (wdt * 1.06, wdt * 1.06, 0.14), bm, root)
    cube((0, 0, h / 2 + 0.04), (wdt * 1.07, 0.16 * s, h + 0.14), ribbon, root, bevel=0.01)
    cube((0, 0, h / 2 + 0.04), (0.16 * s, wdt * 1.07, h + 0.14), ribbon, root, bevel=0.01)
    for a in (35, -35):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.14 * s, minor_radius=0.045 * s,
                                         location=(0, 0, 0), rotation=(math.radians(90), 0, math.radians(a)))
        bow = bpy.context.object; bow.data.materials.append(ribbon); bow.parent = root
        bow.location = (math.cos(math.radians(a)) * 0.1 * s * (1 if a > 0 else -1), 0, h + 0.24 * s)
    root.rotation_euler = (0, 0, rng.uniform(-0.25, 0.25))
    return root


boxes = []
for i, (x, y, s) in enumerate(slots):
    boxes.append(gift(f'box{i}', x, y, s, cols[i]))
alt = gift('box_alt', slots[changed][0], slots[changed][1], slots[changed][2], new_col, ribbon=gold)
alt.rotation_euler = boxes[changed].rotation_euler.copy()

# lights
bpy.ops.object.light_add(type='AREA', location=(-3, -4, 6)); key = bpy.context.object
key.data.energy = 1500; key.data.size = 5; key.data.color = (1, 0.9, 0.8); key.rotation_euler = (math.radians(40), math.radians(-25), 0)
bpy.ops.object.light_add(type='AREA', location=(3.5, 3, 4)); rim = bpy.context.object
rim.data.energy = 600; rim.data.size = 4; rim.data.color = (0.75, 0.85, 1); rim.rotation_euler = (math.radians(-45), math.radians(35), 0)

# camera
bpy.ops.object.camera_add(location=(0, -8.4, 7.6)); cam = bpy.context.object
sc.camera = cam; cam.data.lens = 30; cam.data.sensor_fit = 'VERTICAL'
bpy.ops.object.empty_add(location=(0, -0.1, 0.4)); tgt = bpy.context.object
tcn = cam.constraints.new('TRACK_TO'); tcn.target = tgt; tcn.track_axis = 'TRACK_NEGATIVE_Z'; tcn.up_axis = 'UP_Y'

t_d0, t_d1 = C.get('t_dark0', 4.2), C.get('t_dark1', 5.4)
reveal_t = C.get('reveal_t', 10.8)
for f in range(N):
    t = f / FPS
    dark = ease((t - t_d0) / 0.25) * (1 - ease((t - t_d1) / 0.3))
    key.data.energy = 1500 * (1 - 0.97 * dark); key.data.keyframe_insert('energy', frame=f)
    rim.data.energy = 600 * (1 - 0.97 * dark); rim.data.keyframe_insert('energy', frame=f)
    bgn.inputs['Strength'].default_value = 0.4 * (1 - 0.95 * dark); bgn.inputs['Strength'].keyframe_insert('default_value', frame=f)
    swapped = t >= (t_d0 + t_d1) / 2
    boxes[changed].hide_render = swapped; boxes[changed].keyframe_insert('hide_render', frame=f)
    alt.hide_render = not swapped; alt.keyframe_insert('hide_render', frame=f)
    for ch in boxes[changed].children:
        ch.hide_render = swapped; ch.keyframe_insert('hide_render', frame=f)
    for ch in alt.children:
        ch.hide_render = not swapped; ch.keyframe_insert('hide_render', frame=f)
    hop = 0.0
    if t >= reveal_t:
        u = (t - reveal_t) % 0.7 / 0.7
        hop = 0.45 * math.sin(math.pi * u) if t - reveal_t < 1.4 else 0.0
    alt.location.z = hop; alt.keyframe_insert('location', frame=f)
    push = ease(t / DUR)
    cam.location = (0.25 * math.sin(t * 0.45), -8.4 + 0.7 * push, 7.6 - 0.5 * push)
    cam.keyframe_insert('location', frame=f)

sc.frame_set(int(8 * FPS))
lay = []
for (x, y, s) in slots:
    v = world_to_camera_view(sc, cam, Vector((x, y, 0.85 * s + 0.6)))
    lay.append([round(v.x * 1080), round((1 - v.y) * 1920)])
os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
json.dump({'fps': FPS, 'dur': DUR, 'answer': changed + 1, 'slots_px': lay, 'reveal_t': reveal_t,
           't_dark0': t_d0, 't_dark1': t_d1}, open(os.path.join(OUT, 'layout.json'), 'w'), indent=1)
print('ANSWER', changed + 1)

if '--preview' in sys.argv:
    for f in [int(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, 'frames', f'prev_{f:04d}.png')
        bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(OUT, 'frames', ''); bpy.ops.render.render(animation=True)
