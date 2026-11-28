import bpy, math, sys
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.engine='CYCLES'
sc.render.resolution_x=sc.render.resolution_y=1024
cy=sc.cycles; cy.device='CPU'; cy.samples=96; cy.use_denoising=True
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Punchy'
def lin(h):
    h=h.lstrip('#'); s=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return (*[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in s],1)
def mat(n,c,r=0.25,coat=0.7,metal=0,emit=0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=lin(c); b.inputs['Roughness'].default_value=r
    b.inputs['Coat Weight'].default_value=coat; b.inputs['Metallic'].default_value=metal
    if emit: b.inputs['Emission Color'].default_value=lin(c); b.inputs['Emission Strength'].default_value=emit
    return m
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True
w.node_tree.nodes['Background'].inputs['Color'].default_value=lin('#141B2D'); w.node_tree.nodes['Background'].inputs['Strength'].default_value=1.0
# floor (dark glossy)
bpy.ops.mesh.primitive_plane_add(size=400); fl=bpy.context.object; fl.data.materials.append(mat('fl','#1B2440',0.35,0.3))
def cup(x,col,lift=0,tilt=0):
    bpy.ops.mesh.primitive_cone_add(vertices=96,radius1=0.6,radius2=0.44,depth=1.15,location=(x,0,0.575+lift),rotation=(0,tilt,0))
    c=bpy.context.object
    for p in c.data.polygons: p.use_smooth=True
    s=c.modifiers.new('s','SOLIDIFY'); s.thickness=0.04
    b=c.modifiers.new('b','BEVEL'); b.width=0.03; b.segments=3; b.limit_method='ANGLE'
    c.data.materials.append(mat('c'+col,col))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.535,minor_radius=0.03,location=(0,0,0))
    t=bpy.context.object; t.data.materials.append(mat('w'+col,'#FFFFFF')); t.parent=c; t.location=(0,0,-0.125)
    for p in t.data.polygons: p.use_smooth=True
    return c
cup(-1.32,'#FF2E63'); cup(1.32,'#2EC4B6'); cup(0,'#FFD23F',lift=1.0,tilt=math.radians(-8))
# glowing chaos star under the lifted cup
gold=mat('gold','#F6C453',0.15,0,1.0)
bpy.ops.mesh.primitive_torus_add(major_radius=0.3,minor_radius=0.065,major_segments=64,minor_segments=24,location=(0,0,0.36),rotation=(math.radians(90),0,math.radians(18)))
rg=bpy.context.object; rg.data.materials.append(gold)
for p in rg.data.polygons: p.use_smooth=True
g=bpy.data.materials.new('dia'); g.use_nodes=True; bb=g.node_tree.nodes['Principled BSDF']
bb.inputs['Transmission Weight'].default_value=1; bb.inputs['IOR'].default_value=2.2; bb.inputs['Roughness'].default_value=0
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=0.15,location=(0,0,0.72)); d=bpy.context.object; d.scale=(1,1,0.8); d.data.materials.append(g)
bpy.ops.object.light_add(type='POINT',location=(0.3,-1.3,0.55)); pl=bpy.context.object; pl.data.energy=60; pl.data.color=(1,0.85,0.4)
bpy.ops.object.light_add(type='AREA',location=(-3,-4,5)); k=bpy.context.object; k.data.energy=900; k.data.size=4
k.rotation_euler=(math.radians(40),math.radians(-30),0)
bpy.ops.object.light_add(type='AREA',location=(3,2,3)); r=bpy.context.object; r.data.energy=500; r.data.size=3; r.data.color=(0.6,0.75,1)
r.rotation_euler=(math.radians(-50),math.radians(40),0)
bpy.ops.object.camera_add(location=(0,-6.2,2.3)); cam=bpy.context.object; sc.camera=cam; cam.data.lens=50
bpy.ops.object.empty_add(location=(0,0,0.75)); t=bpy.context.object
tc=cam.constraints.new('TRACK_TO'); tc.target=t; tc.track_axis='TRACK_NEGATIVE_Z'; tc.up_axis='UP_Y'
sc.render.filepath='/tmp/claude-0/avatar/cups.png'; bpy.ops.render.render(write_still=True)
