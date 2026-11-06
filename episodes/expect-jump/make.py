import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('expect-jump', 9.5, 'split_screen', scene='living_b',
       situation="split screen EXPECTATION (top) vs REALITY (bottom): the same jump onto a side table; top lands like a gymnast with sunglasses",
       twist="bottom bonks the table edge, slides down, then overshoots out of frame (crash), walks back and sits beside the table: 'I MEANT TO DO THAT'; top cat looks down at him",
       title="Expectation vs reality: the cat jump 😭",
       description="Which one is YOUR cat? Top or bottom 👇\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #expectationvsreality #funny #animation #catfails",
       experiment=True)
e.scene_tracks(wall=[[0, '#D9F0E3']])
S = 1000 / 1080
e.panels(dict(rect=[40, 290, 1000, 660], ox=0, oy=590, s=S), dict(rect=[40, 980, 1000, 660], ox=0, oy=590, s=S, scene={'wall': '#F3DDE0'}))
for i in (0, 1):
    e.prop(f'table{i}', 'table', panel=i, x=780, y=1096, w=360, h=220)
    e.prop(f'plant{i}', 'mug', panel=i, x=850, y=1075, scale=0.6, color='#7FB77E', label='')
# EXPECTATION
e.nugget('top', panel=0, scale=0.8, flip=1,
         x=[[0, 300], [0.9, 760, 'linear'], [9.5, 760]], y=[[0, 1289], [0.45, 860, 'out'], [0.9, 1055, 'in'], [9.5, 1055]],
         pose=[[0, 'run'], [0.9, 'sit']], run_speed=0.6, squish=[[0, 0.0], [0.9, 0.25], [1.1, 0, 'bounce']],
         eye=[[0, 'normal'], [0.9, 'happy'], [6.4, 'normal']], mouth=[[0, 'open'], [0.9, 'smile']], look=[[0, [0.8, -0.4]], [6.4, [-0.4, 0.9]]],
         sunglasses=[[0, False], [1.2, True, 'step']], tail=[[0, 1.0], [0.9, 2.0]], headtilt=[[0, 0], [6.4, 0], [7.0, 0.3], [7.5, -0.2], [8.0, 0.2]])
e.fx('spark', 'sparkle', panel=0, x=760, y=960, r=200, show=shown((0.9, 1.9)))
# REALITY
RX = [[0, 300], [0.6, 600, 'linear'], [1.4, 590], [2.5, 590], [3.2, 1400, 'linear'], [4.3, 1400], [5.1, 520, 'linear'], [9.5, 520]]
RY = [[0, 1289], [0.3, 1080, 'out'], [0.6, 1130, 'in'], [1.4, 1300, 'in'], [2.5, 1300], [2.85, 640, 'out'], [3.2, 900, 'in'], [4.3, 1289, 'step'], [9.5, 1289]]
e.nugget('bot', panel=1, scale=0.8, flip=[[0, 1], [4.3, -1, 'step'], [5.1, 1, 'step']], x=RX, y=RY,
         pose=[[0, 'run'], [0.6, 'sit'], [1.4, 'loaf'], [2.4, 'sit'], [2.5, 'run'], [4.3, 'run'], [5.1, 'sit']], run_speed=1.5,
         eye=[[0, 'normal'], [0.6, 'squeeze'], [1.4, 'dizzy'], [2.3, 'big'], [2.5, 'wide'], [4.3, 'normal'], [5.1, 'closed'], [6.4, 'big']],
         mouth=[[0, 'open'], [0.6, 'scream'], [1.4, 'line'], [2.5, 'open'], [4.3, 'line'], [5.1, 'smile'], [6.4, 'line']],
         look=[[0, [0.8, -0.4]], [6.4, [0.4, -0.9]]], squish=[[0, 0], [0.6, 0.35], [0.8, 0.0]], ear=[[0, 0], [0.6, 1.0], [2.3, 0], [6.4, 0.6]],
         blush=[[0, 0.35], [5.1, 0.9]], tail=[[0, 1.0], [5.1, 0.4]])
e.fx('bonk', 'stars', panel=1, x=600, y=920, scale=0.6, show=shown((0.6, 2.3)))
e.fx('crash', 'burst', panel=1, x=1020, y=900, r=200, color='#FFE14D', show=shown((3.3, 3.9)))
e.fx('dust', 'dust', panel=1, x=1000, y=1250, show=shown((3.3, 4.3)))
e.fx('sweat', 'sweat', panel=1, x=600, y=980, show=shown((5.1, 9.5)))
e.fx('lab0', 'tag', screen=True, x=250, y=350, text='EXPECTATION', color='#2E9E5B', size=48, w=380)
e.fx('lab1', 'tag', screen=True, x=200, y=1040, text='REALITY', color='#E2463F', size=48, w=280)
e.card('t1', 'THE JUMP', 0, 6.4, size=110, y=200, fill='#FFE14D')
e.card('t2', '10/10 LANDING', 1.0, 6.4, size=58, y=880, fill='#9BE7FF')
e.card('t3', 'I MEANT TO DO THAT', 5.1, None, size=64, y=1560, fill='#FFFFFF')
e.card('t4', 'WHICH ONE IS YOUR CAT?', 6.4, None, size=74, y=200, fill='#FFE14D', pulse=1)
e.music('triumph', 701, [[0, 1], [0.6, 1], [0.62, 0.25, 'step'], [5.0, 0.25], [5.05, 0.8, 'step']])
for t, n, g, o in [(0.0, 'whoosh', 0.6, {}), (0.6, 'thud', 1.0, {}), (0.62, 'boing', 0.7, {}), (0.9, 'sparkle', 0.5, {}), (0.95, 'ding', 0.4, {}),
                   (0.8, 'slide_down', 0.6, {}), (1.4, 'thud', 0.5, {}), (2.5, 'whoosh', 0.7, {}), (3.3, 'crash', 0.9, {}),
                   (4.3, 'run', 0.6, {'loop': True, 'dur': 0.8}), (5.1, 'pop', 0.4, {}), (6.4, 'meow', 0.6, {'rate': 1.2})]:
    e.sfx(t, n, g, **o)
print(e.save())
