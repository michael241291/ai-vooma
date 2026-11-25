"""3D marble race (Blender rigid-body physics + Cycles) on a zigzag of wooden ramps.
Marbles wait behind a gate (suspense), the gate drops, physics decides the winner, the camera follows the leader.

Usage: python3 engine/marble3d.py episodes/<id>/race.json [--preview 0,120,300]
race.json: fps, dur, seed, marbles [{"name","color"}], gate_t, ramps, wood, out_dir, res_pct, samples
Writes <out_dir>/frames/####.png (RGBA) and <out_dir>/layout.json (winner, finish times).
"""
import json
import math
import os
import random
import sys

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(sys.argv[1]))
OUT = C['out_dir']
FPS, DUR = C.get('fps', 25), C.get('dur', 13.5)
N = int(round(FPS * DUR))
rng = random.Random(C.get('seed', 5))


def hexcol(h):
    h = h.lstrip('#'); s = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in s], 1.0)


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = C.get('res_pct', 50); sc.render.fps = FPS
sc.frame_start, sc.frame_end = 0, N - 1
sc.render.film_transparent = True; sc.render.image_settings.color_mode = 'RGBA'
sc.render.use_persistent_data = True
cy = sc.cycles; cy.device = 'CPU'; cy.samples = C.get('samples', 10); cy.use_adaptive_sampling = True
cy.adaptive_threshold = 0.05; cy.use_denoising = True; cy.denoising_prefilter = 'FAST'
cy.max_bounces = 3; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.transmission_bounces = 2; cy.transparent_max_bounces = 2
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5, 0.45, 0.55, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6


def mat(name, col, rough=0.4, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol(col); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; b.inputs['Coat Weight'].default_value = coat
    return m


def wood_mat():
    m = bpy.data.materials.new('wood'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(ROOT, C['wood']))
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.35, 0.35, 0.35)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
    tex.projection = 'BOX'
    nt.links.new(tex.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.5
    return m


def box(name, loc, size, rot=(0, 0, 0), material=None, passive=True, render=True):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if material:
        o.data.materials.append(material)
    bev = o.modifiers.new('b', 'BEVEL'); bev.width = 0.03; bev.segments = 2
    bpy.ops.rigidbody.object_add(); o.rigid_body.type = 'PASSIVE' if passive else 'ACTIVE'
    o.rigid_body.collision_shape = 'CONVEX_HULL'; o.rigid_body.friction = C.get('ramp_friction', 0.15); o.rigid_body.restitution = 0.2
    o.hide_render = not render
    return o


bpy.ops.rigidbody.world_add()
rbw = sc.rigidbody_world; rbw.substeps_per_frame = 20; rbw.solver_iterations = 20
rbw.point_cache.frame_start = 0; rbw.point_cache.frame_end = N

WOOD = wood_mat()
rail_cols = C.get('rail_colors', ['#FF2E63', '#FFD23F', '#2EC4B6', '#7B61FF'])
rails = [mat(f'rail{i}', c, 0.25, coat=0.6) for i, c in enumerate(rail_cols)]

R = C.get('radius', 0.24)
L = C.get('ramp_len', 3.4)
tilt = math.radians(C.get('tilt', 11))
gap = C.get('ramp_gap', 1.55)
nramps = C.get('ramps', 6)
top_z = gap * nramps + 1.0
ramps = []
for k in range(nramps):
    d = 1 if k % 2 == 0 else -1           # k even: rolls toward +x
    cx = -0.45 * d
    cz = top_z - k * gap
    rot = (0, d * tilt, 0)                # tilt so that +x side is lower when d=1
    ramp = box(f'ramp{k}', (cx, 0, cz), (L, 1.0, 0.14), rot, WOOD)
    # stopper on the high end
    hx = cx - d * (L / 2) * math.cos(tilt); hz = cz + (L / 2) * math.sin(tilt)
    if k == 0:
        box(f'stop{k}', (hx - d * 0.05, 0, hz + 0.25), (0.12, 1.0, 0.55), rot, rails[k % len(rails)])
    # back rail (visible) and front rail (invisible glass)
    box(f'back{k}', (cx, 0.47, cz + 0.22), (L, 0.06, 0.32), rot, rails[k % len(rails)])
    box(f'front{k}', (cx, -0.47, cz + 0.22), (L, 0.06, 0.32), rot, None, render=False)
    ramps.append((cx, cz, d))
# catch walls so marbles cannot fly sideways out of the zigzag
xw = 0.45 + (L / 2) * math.cos(tilt) + C.get('wall_gap', 0.06)
box('wallL', (-xw, 0, top_z / 2), (0.1, 1.0, top_z + 3), material=None, render=False)
box('wallR', (xw, 0, top_z / 2), (0.1, 1.0, top_z + 3), material=None, render=False)
box('glassF', (0, -0.56, top_z / 2), (2 * xw, 0.05, top_z + 3), material=None, render=False)
box('glassB', (0, 0.56, top_z / 2), (2 * xw, 0.05, top_z + 3), material=None, render=False)
# finish tray
finish_z = top_z - nramps * gap + 0.2
box('floor', (0, 0, finish_z - 0.6), (2 * xw, 1.0, 0.2), material=WOOD)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.2, finish_z - 0.49)); fl = bpy.context.object
fl.scale = (2 * xw, 0.08, 1); fl.data.materials.append(mat('finish', '#FFFFFF', 0.3))

# gate (animated passive box) at the first ramp
cx0, cz0, d0 = ramps[0]
gx = cx0 - d0 * (L / 2) * math.cos(tilt) + d0 * 2.45
gate = box('gate', (gx, 0, cz0 - (gx - cx0) * d0 * math.tan(tilt) + 0.45), (0.12, 1.0, 0.7), (0, d0 * tilt, 0), mat('gate', '#FFFFFF', 0.3, coat=0.5))
gate.rigid_body.kinematic = True
gate_t = C.get('gate_t', 2.0)
for f, z in ((0, gate.location.z), (int(gate_t * FPS), gate.location.z), (int(gate_t * FPS) + 4, gate.location.z + 1.6)):
    gate.location.z = z; gate.keyframe_insert('location', frame=f)

# marbles
marbles = []
names = []
for i, mb in enumerate(C['marbles']):
    mm = bpy.data.materials.new(f'm{i}'); mm.use_nodes = True; b = mm.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol(mb['color']); b.inputs['Roughness'].default_value = 0.08
    b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Specular IOR Level'].default_value = 0.7
    sx = cx0 - d0 * (L / 2) * math.cos(tilt) + d0 * (0.38 + 0.5 * i) + rng.uniform(-0.02, 0.02)
    sz = cz0 - (sx - cx0) * d0 * math.tan(tilt) + 0.07 / math.cos(tilt) + R + 0.03
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, segments=48, ring_count=24, location=(sx, rng.uniform(-0.15, 0.15), sz))
    o = bpy.context.object
    for p in o.data.polygons:
        p.use_smooth = True
    o.data.materials.append(mm)
    bpy.ops.rigidbody.object_add(); o.rigid_body.type = 'ACTIVE'; o.rigid_body.collision_shape = 'SPHERE'
    o.rigid_body.mass = 1.0 + rng.uniform(-0.05, 0.05); o.rigid_body.friction = 0.3 + rng.uniform(-0.05, 0.05)
    o.rigid_body.restitution = 0.35; o.rigid_body.linear_damping = 0.02; o.rigid_body.angular_damping = 0.05
    marbles.append(o); names.append(mb['name'])

# lights
bpy.ops.object.light_add(type='AREA', location=(-4, -6, top_z + 2)); k = bpy.context.object
k.data.energy = 2500; k.data.size = 6; k.data.color = (1, 0.92, 0.85); k.rotation_euler = (math.radians(60), math.radians(-25), 0)
bpy.ops.object.light_add(type='AREA', location=(5, -4, top_z / 2)); r2 = bpy.context.object
r2.data.energy = 1200; r2.data.size = 6; r2.data.color = (0.8, 0.85, 1); r2.rotation_euler = (math.radians(70), math.radians(40), 0)

# bake physics
bpy.ops.ptcache.bake_all(bake=True)

# read trajectories, find finish order
traj = []
finish = [None] * len(marbles)
for f in range(N):
    sc.frame_set(f)
    pts = [m.matrix_world.translation.copy() for m in marbles]
    traj.append(pts)
    for i, p in enumerate(pts):
        if finish[i] is None and p.z < finish_z - 0.1:
            finish[i] = f / FPS
order = sorted(range(len(marbles)), key=lambda i: (finish[i] is None, finish[i] if finish[i] is not None else 1e9))
winner = order[0]
print('FINISH', [(names[i], finish[i]) for i in order])

# camera follows the leader (lowest z), smoothed
bpy.ops.object.camera_add(location=(0, -C.get('cam_dist', 11.5), top_z)); cam = bpy.context.object
sc.camera = cam; cam.data.lens = 35; cam.data.sensor_fit = 'VERTICAL'
cam.rotation_euler = (math.radians(86), 0, 0)
zc = traj[0][0].z - 1.0
for f in range(N):
    lead = min(p.z for p in traj[f])
    target = max(finish_z + 2.2, lead - 0.8)
    zc += (target - zc) * 0.08
    cam.location = (0.0, -C.get('cam_dist', 11.5), zc + 0.6)
    cam.keyframe_insert('location', frame=f)
    r2.location = (5, -4, zc)

os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
json.dump({'fps': FPS, 'dur': DUR, 'winner': names[winner], 'winner_color': C['marbles'][winner]['color'],
           'order': [names[i] for i in order], 'finish': {names[i]: finish[i] for i in range(len(marbles))},
           'gate_t': gate_t}, open(os.path.join(OUT, 'layout.json'), 'w'), indent=1)

if '--preview' in sys.argv:
    for f in [int(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, 'frames', f'prev_{f:04d}.png')
        bpy.ops.render.render(write_still=True)
elif '--bake-only' not in sys.argv:
    sc.render.filepath = os.path.join(OUT, 'frames', ''); bpy.ops.render.render(animation=True)
