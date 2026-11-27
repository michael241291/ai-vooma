"""3D shell game (Blender/Cycles, CPU) for Tiny Chaos.

Renders transparent RGBA frames of 3 glossy cups on a wooden table (Pixabay wood photo texture).
The background (a Pixabay video) and captions are composited afterwards by engine/compose3d.py.

Usage: python3 engine/shell3d.py episodes/<id>/shell.json [--preview 0,60,250]
shell.json keys: fps, dur, seed, cup_colors, prize ('ring'|'keys'|'coin'), wood, swaps_from, swaps_to,
                 d0, d1 (swap duration first->last), reveal_t, out_dir, res_pct
Writes <out_dir>/frames/####.png and <out_dir>/layout.json (cup screen positions, answer, swap times).
"""
import json
import math
import os
import random
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg_path = sys.argv[1]
C = json.load(open(cfg_path))
OUT = C.get('out_dir') or os.path.dirname(cfg_path)
FPS = C.get('fps', 25)
DUR = C.get('dur', 11.0)
N = int(round(FPS * DUR))
SLOTS = [-1.3, 0.0, 1.3]


def hexcol(h):
    h = h.lstrip('#')
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (*lin, 1.0)


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def ease_out(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


# ---------------- scene ----------------
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = C.get('res_pct', 50)
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 0, N - 1
sc.render.film_transparent = True
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.render.use_persistent_data = True
sc.render.use_overwrite = False; sc.render.use_placeholder = True  # resumable
cy = sc.cycles
cy.device = 'CPU'; cy.samples = C.get('samples', 12); cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05
cy.use_denoising = True; cy.denoising_prefilter = 'FAST'
cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.transmission_bounces = 3; cy.transparent_max_bounces = 2
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Punchy'

world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.35, 0.25, 0.18, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6


def mat_plastic(name, col):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol(col)
    b.inputs['Roughness'].default_value = 0.28
    b.inputs['Coat Weight'].default_value = 0.6
    b.inputs['Coat Roughness'].default_value = 0.08
    return m


def mat_metal(name, col, rough=0.18):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexcol(col)
    b.inputs['Metallic'].default_value = 1.0
    b.inputs['Roughness'].default_value = rough
    return m


def mat_glass(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (1, 1, 1, 1)
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['IOR'].default_value = 2.2
    b.inputs['Roughness'].default_value = 0.0
    return m


def mat_image(name, path, scale=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(path)
    mapping = nt.nodes.new('ShaderNodeMapping'); coord = nt.nodes.new('ShaderNodeTexCoord')
    mapping.inputs['Scale'].default_value = (scale, scale, 1)
    nt.links.new(coord.outputs['UV'], mapping.inputs['Vector'])
    nt.links.new(mapping.outputs['Vector'], tex.inputs['Vector'])
    nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.55
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.25
    nt.links.new(tex.outputs['Color'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True


# table
wood = os.path.join(ROOT, C['wood'])
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -1.6, -0.15))
table = bpy.context.object; table.scale = (9.0, 9.4, 0.3)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.modifier_add(type='BEVEL'); table.modifiers['Bevel'].width = 0.06; table.modifiers['Bevel'].segments = 3
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.uv.cube_project(cube_size=4.0); bpy.ops.object.mode_set(mode='OBJECT')
table.data.materials.append(mat_image('wood', wood, 1.0))


# cups (upside-down tapered cup, open at the bottom, rim + band)
def make_cup(col, i):
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.6, radius2=0.44, depth=1.15, end_fill_type='NGON', location=(0, 0, 0.575))
    cup = bpy.context.object
    # remove the bottom face (largest radius at z=0)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.object.mode_set(mode='OBJECT')
    for p in cup.data.polygons:
        if len(p.vertices) > 4 and p.center.z < 0:
            p.select = True
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.delete(type='FACE'); bpy.ops.object.mode_set(mode='OBJECT')
    sol = cup.modifiers.new('s', 'SOLIDIFY'); sol.thickness = 0.04
    bev = cup.modifiers.new('b', 'BEVEL'); bev.width = 0.03; bev.segments = 3; bev.limit_method = 'ANGLE'
    smooth(cup)
    cup.data.materials.append(mat_plastic(f'cup{i}', col))
    # band
    bpy.ops.mesh.primitive_torus_add(major_radius=0.535, minor_radius=0.03, location=(0, 0, 0.45))
    band = bpy.context.object; smooth(band); band.data.materials.append(mat_plastic(f'band{i}', '#FFFFFF'))
    band.parent = cup; band.location = (0, 0, 0.45 - 0.575)
    # rim lip
    bpy.ops.mesh.primitive_torus_add(major_radius=0.6, minor_radius=0.035, location=(0, 0, 0.03))
    lip = bpy.context.object; smooth(lip); lip.data.materials.append(mat_plastic(f'lip{i}', col))
    lip.parent = cup; lip.location = (0, 0, 0.03 - 0.575)
    return cup


cols = C.get('cup_colors', ['#FF2E63', '#FFD23F', '#2EC4B6'])
cups = [make_cup(cols[i], i) for i in range(3)]


# prize
def make_ring():
    bpy.ops.mesh.primitive_torus_add(major_radius=0.17, minor_radius=0.035, major_segments=64, minor_segments=24,
                                     location=(0, 0, 0.21), rotation=(math.radians(90), 0, 0))
    ring = bpy.context.object; smooth(ring); ring.data.materials.append(mat_metal('gold', '#F6C453'))
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.08, location=(0, 0, 0.42))
    gem = bpy.context.object; gem.scale = (1, 1, 0.8); gem.data.materials.append(mat_glass('diamond'))
    bpy.ops.object.empty_add(location=(0, 0, 0)); root = bpy.context.object
    ring.parent = root; ring.location = (0, 0, 0.21)
    gem.parent = root; gem.location = (0, 0, 0.42)
    return root


def make_coin():
    # a standing gold coin with a raised rim, leaning slightly so the face catches the light
    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.045, vertices=64, location=(0, 0, 0.26),
                                        rotation=(math.radians(80), 0, math.radians(15)))
    coin = bpy.context.object; smooth(coin); coin.data.materials.append(mat_metal('coin', '#F2C14E', 0.22))
    bev = coin.modifiers.new('b', 'BEVEL'); bev.width = 0.012; bev.segments = 3
    bpy.ops.object.empty_add(location=(0, 0, 0)); root = bpy.context.object
    coin.parent = root; coin.location = (0, 0, 0.26)
    return root


def make_keys():
    # a car-key bunch lying on the table: key ring + two keys + a fob
    bpy.ops.object.empty_add(location=(0, 0, 0)); root = bpy.context.object
    steel = mat_metal('steel', '#C9CED6', 0.25); brass = mat_metal('brass', '#D8A84A', 0.3)
    fob_m = mat_plastic('fob', '#1E1E24')
    bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.018, location=(0, 0, 0.02))
    r = bpy.context.object; smooth(r); r.data.materials.append(steel); r.parent = root; r.location = (-0.12, 0.05, 0.02)
    for k, (ang, m_) in enumerate(((20, steel), (-35, brass))):
        a = math.radians(ang)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.03, location=(0, 0, 0))
        head = bpy.context.object; head.data.materials.append(m_); head.parent = root
        cx, cy = -0.12 + 0.2 * math.cos(a), 0.05 + 0.2 * math.sin(a)
        head.location = (cx, cy, 0.02 + 0.01 * k)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); sh = bpy.context.object
        sh.scale = (0.26, 0.05, 0.02); sh.data.materials.append(m_); sh.parent = root
        sh.rotation_euler = (0, 0, a); sh.location = (cx + 0.2 * math.cos(a), cy + 0.2 * math.sin(a), 0.02 + 0.01 * k)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); fob = bpy.context.object
    fob.scale = (0.16, 0.26, 0.06); fob.data.materials.append(fob_m); fob.parent = root
    fob.rotation_euler = (0, 0, math.radians(200)); fob.location = (-0.3, -0.12, 0.035)
    b = fob.modifiers.new('b', 'BEVEL'); b.width = 0.03; b.segments = 4
    return root


if C.get('prize', 'ring') == 'keys':
    prize = make_keys(); prize.scale = (1.3, 1.3, 1.3)
elif C.get('prize', 'ring') == 'coin':
    prize = make_coin(); prize.scale = (1.4, 1.4, 1.4)
else:
    prize = make_ring(); prize.scale = (1.5, 1.5, 1.5)

# lights
bpy.ops.object.light_add(type='AREA', location=(-2.5, -2.5, 5.0)); key = bpy.context.object
key.data.energy = 900; key.data.size = 3.5; key.data.color = (1.0, 0.84, 0.66)
key.rotation_euler = (math.radians(40), math.radians(-25), 0)
bpy.ops.object.light_add(type='AREA', location=(2.8, 3.5, 3.2)); rim = bpy.context.object
rim.data.energy = 500; rim.data.size = 2.5; rim.data.color = (0.65, 0.75, 1.0)
rim.rotation_euler = (math.radians(-55), math.radians(30), 0)
bpy.ops.object.light_add(type='POINT', location=(0, -3.0, 1.2)); fill = bpy.context.object
fill.data.energy = 120; fill.data.color = (1.0, 0.9, 0.8)

# camera
bpy.ops.object.camera_add(location=(0, -6.9, 4.6)); cam = bpy.context.object
sc.camera = cam; cam.data.lens = 25; cam.data.sensor_fit = 'VERTICAL'
bpy.ops.object.empty_add(location=(0, 0.2, 0.35)); tgt = bpy.context.object
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
cam.data.dof.use_dof = True; cam.data.dof.focus_object = tgt; cam.data.dof.aperture_fstop = 4.0

# ---------------- animation ----------------
rng = random.Random(C.get('seed', 7))
slot_of = [0, 1, 2]          # cup i sits in slot slot_of[i]
prize_cup = C.get('prize_cup', 1)
t_drop0, t_drop1 = C.get('drop', [0.0, 0.9])
swap_t0, swap_t1 = C.get('swaps_from', 1.1), C.get('swaps_to', 8.0)
d0, d1 = C.get('d0', 0.7), C.get('d1', 0.36)
swaps = []
t = swap_t0
while True:
    u = (t - swap_t0) / (swap_t1 - swap_t0)
    d = d0 + (d1 - d0) * min(1, u)
    if t + d > swap_t1 + 0.01:
        break
    a, b = rng.sample([0, 1, 2], 2)
    # bias: involve the prize cup often so tracking matters
    if rng.random() < 0.55 and prize_cup not in (a, b):
        a = prize_cup
        b = rng.choice([c for c in range(3) if c != a])
    swaps.append((t, d, a, b))
    t += d + 0.04
reveal_t = C.get('reveal_t', 9.4)


def cup_state(i, tt):
    """xyz of cup i at time tt."""
    s = [0, 1, 2]
    x = None
    for (ts, d, a, b) in swaps:
        if tt < ts:
            break
        if tt < ts + d:
            if i in (a, b):
                o = b if i == a else a
                xa, xb = SLOTS[s[i]], SLOTS[s[o]]
                u = ease((tt - ts) / d)
                r = (0.72 + 0.2 * abs(xb - xa)) * (1 if i == a else -1)
                x = (xa + (xb - xa) * u, math.sin(math.pi * u) * r, 0.0)
            break
        s[a], s[b] = s[b], s[a]
    if x is None:
        x = (SLOTS[s[i]], 0.0, 0.0)
    z = 0.0
    if i == prize_cup and tt < t_drop1:
        u = (tt - t_drop0) / (t_drop1 - t_drop0)
        z = 1.35 * (1 - ease(max(0, (u - 0.25) / 0.75)))
    if i == prize_cup and tt >= reveal_t:
        z = 1.45 * ease_out((tt - reveal_t) / 0.4)
    return (x[0], x[1], z), s


final_slots = cup_state(0, swap_t1 + 0.5)[1]
answer_slot = final_slots[prize_cup] + 1  # 1..3 left to right

for f in range(N):
    tt = f / FPS
    for i, cup in enumerate(cups):
        (x, y, z), _ = cup_state(i, tt)
        cup.location = (x, y, 0.575 + z)
        cup.keyframe_insert('location', frame=f)
    (x, y, _), _ = cup_state(prize_cup, tt)
    prize.location = (x, y, 0.0)
    prize.keyframe_insert('location', frame=f)
    # slow push-in + tiny handheld drift
    push = ease(tt / DUR)
    cam.location = (0.04 * math.sin(tt * 1.7), -6.9 + 0.5 * push + 0.03 * math.sin(tt * 1.3), 4.6 - 0.25 * push)
    cam.keyframe_insert('location', frame=f)

# screen positions of the 3 slots (for captions), in 1080x1920 px
sc.frame_set(int(9.0 * FPS))
lay = []
for xs in SLOTS:
    from mathutils import Vector
    v = world_to_camera_view(sc, cam, Vector((xs, 0, 1.35)))
    lay.append([round(v.x * 1080), round((1 - v.y) * 1920)])
os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
json.dump({'fps': FPS, 'dur': DUR, 'n': N, 'answer': answer_slot, 'slots_px': lay,
           'swaps': [[round(s[0], 3), round(s[1], 3)] for s in swaps], 'reveal_t': reveal_t,
           'drop_t': t_drop1}, open(os.path.join(OUT, 'layout.json'), 'w'), indent=1)
print('ANSWER', answer_slot, 'SWAPS', len(swaps))

prev = [a for a in sys.argv if a.startswith('--preview')]
if prev:
    frames = [int(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(OUT, 'frames', f'prev_{f:04d}.png')
        bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(OUT, 'frames', '')
    bpy.ops.render.render(animation=True)
