import bpy, math, random, sys
mode=sys.argv[-1]  # 'word' or 'mono'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.render.resolution_x=sc.render.resolution_y=1024
sc.cycles.samples=96; sc.cycles.use_denoising=True; sc.cycles.device='CPU'
sc.view_settings.view_transform='Standard'
def lin(h):
    h=h.lstrip('#'); s=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return (*[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in s],1)
def mat(n,c,r=0.22,coat=0.8):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=lin(c); b.inputs['Roughness'].default_value=r; b.inputs['Coat Weight'].default_value=coat; return m
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True
w.node_tree.nodes['Background'].inputs['Color'].default_value=lin('#151A33'); w.node_tree.nodes['Background'].inputs['Strength'].default_value=1
font=bpy.data.fonts.load('/root/.fonts/LuckiestGuy.ttf')
cols=['#FF2E63','#FFD23F','#2EC4B6','#7B61FF']
white=mat('white','#FFFFFF'); outline=mat('ol','#151A33',0.5,0)
rng=random.Random(7)
def letter(ch,x,y,size,col,rot):
    cu=bpy.data.curves.new('t','FONT'); cu.body=ch; cu.font=font; cu.size=size; cu.extrude=0.12*size; cu.bevel_depth=0.02*size; cu.bevel_resolution=3
    cu.align_x='CENTER'; cu.align_y='CENTER'
    o=bpy.data.objects.new(ch,cu); bpy.context.collection.objects.link(o)
    o.location=(x,y,0); o.rotation_euler=(math.radians(90)+rot[0],rot[1],rot[2]); o.data.materials.append(mat('m'+ch+str(x),col))
    return o
if mode=='word':
    rows=[('TINY',0.78,1.0),('CHAOS',-0.45,1.45)]
    k=0
    for word,z,size in rows:
        n=len(word); sp=size*(0.66 if word=='CHAOS' else 0.62)
        for i,ch in enumerate(word):
            x=(i-(n-1)/2)*sp
            jitter=(rng.uniform(-0.08,0.08), 0, rng.uniform(-0.18,0.18))
            o=letter(ch,x,0,size,cols[k%4] if word=='CHAOS' else '#FFFFFF',(0,jitter[2],rng.uniform(-0.25,0.25)))
            o.location=(x,0,z+rng.uniform(-0.08,0.08)) if word=='CHAOS' else (x,0,z)
            if word=='TINY': o.rotation_euler=(math.radians(90),0,rng.uniform(-0.06,0.06)); o.location.z=z
            k+=1
    # soft glow disc behind the letters
    bpy.ops.mesh.primitive_circle_add(vertices=96,radius=2.6,fill_type='NGON',location=(0,1.2,0),rotation=(math.radians(90),0,0))
    g=bpy.context.object; gm=bpy.data.materials.new('g'); gm.use_nodes=True; nt=gm.node_tree
    em=nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value=lin('#3A2E7A'); em.inputs['Strength'].default_value=1.0
    nt.links.new(em.outputs['Emission'], nt.nodes['Material Output'].inputs['Surface']); g.data.materials.append(gm)
    cam_d=6.4
else:
    o1=letter('T',-0.62,0,2.6,'#FFFFFF',(0,0,0)); o1.location=(-0.55,0,0.05)
    o2=letter('C',0.62,0,2.6,'#FF2E63',(0,math.radians(-12),math.radians(14))); o2.location=(0.6,-0.25,-0.1)
    # little chaos sparks
    for i,(x,z,c) in enumerate([(1.55,1.25,'#FFD23F'),(-1.6,-1.15,'#2EC4B6'),(1.45,-1.25,'#7B61FF')]):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=0.18,location=(x,-0.3,z)); s=bpy.context.object
        for p in s.data.polygons: p.use_smooth=True
        s.data.materials.append(mat('s%d'%i,c))
    cam_d=7.2
bpy.ops.object.light_add(type='AREA',location=(-3,-5,4)); k=bpy.context.object; k.data.energy=1500; k.data.size=5
k.rotation_euler=(math.radians(55),0,math.radians(-30))
bpy.ops.object.light_add(type='AREA',location=(4,-2,-2)); r=bpy.context.object; r.data.energy=700; r.data.size=4; r.data.color=(0.6,0.75,1)
r.rotation_euler=(math.radians(100),0,math.radians(60))
bpy.ops.object.camera_add(location=(0,-cam_d,0),rotation=(math.radians(90),0,0)); cam=bpy.context.object; sc.camera=cam; cam.data.lens=45
sc.render.filepath=f'/tmp/claude-0/logo/{mode}.png'; bpy.ops.render.render(write_still=True)
