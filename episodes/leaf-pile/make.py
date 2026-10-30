import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('leaf-pile', 13.5, 'interactive_protect', scene='backyard',
       situation="autumn leaves rain down on a freshly groomed Nugget; the viewer's palm shields him like an umbrella",
       twist="he spots the giant leaf pile, runs and dives in on purpose; only his ears stick out: 'HE IS A LEAF NOW'",
       title="Keep the leaves off Nugget! 🍂👆",
       description="He just got groomed. Hold your finger up and keep him clean... if he lets you. 🍂\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #fall #autumn #interactive #animation")
e.cam(zoom=[[0, 1.0], [8.0, 1.0], [8.6, 1.08], [9.6, 1.08], [9.75, 1.18, 'out'], [13.5, 1.12]],
      fx=[[0, 540], [8.0, 540], [9.6, 760]], fy=[[0, 1150]],
      shake=[[0, 0], [9.5, 0], [9.52, 16, 'step'], [9.9, 0]])
# leaf pile right (behind Nugget once he dives)
e.prop('pile', 'leafpile', x=800, y=1450, w=540, h=270, seed=4, scale=1.0,
       jiggle=[[0, 0], [9.45, 0, 'step'], [9.5, 1], [10.6, 0]])
e.nugget('nug', x=[[0, 360], [8.6, 360], [9.5, 800, 'inout']],
         y=[[0, 1290], [8.6, 1290], [9.05, 1020, 'out'], [9.5, 1380, 'in'], [9.6, 1490, 'out'], [10.2, 1470, 'back']],
         scale=[[0, 0.85], [8.6, 0.85], [9.5, 0.75]],
         pose=[[0, 'sit'], [8.6, 'run'], [9.45, 'sit']], run_speed=1.6,
         flip=1, eye=[[0, 'wide'], [1.2, 'normal'], [4.1, 'happy'], [7.6, 'normal'], [8.0, 'big'], [9.6, 'squeeze'], [10.3, 'happy']],
         look=[[0, [0.2, -0.9]], [4.0, [0.2, -0.9]], [4.2, [0, 0.3]], [7.6, [0.9, 0.3]]],
         mouth=[[0, 'frown'], [4.1, 'smile'], [8.0, 'o'], [8.6, 'open'], [10.3, 'smile']], mk=[[0, 0.3], [8.0, 0.6]],
         ear=[[0, 0.5], [4.1, 0], [8.0, -0.25], [9.0, 0]], tail=[[0, 0.6], [4.1, 1.5], [8.0, 2.5]],
         blush=[[0, 0.35], [10.3, 0.8]], show=shown((0, 13.6)))
# front leaves cover his body after the dive
e.prop('pile_front', 'leafpile', x=800, y=1575, w=620, h=300, seed=9, part='front',
       jiggle=[[0, 0], [9.45, 0, 'step'], [9.5, 1], [10.6, 0]], show=shown((9.45, 14)))
e.prop('pile_cover', 'leafpile', x=800, y=1575, w=600, h=320, seed=12, show=shown((9.45, 14)),
       jiggle=[[0, 0], [9.45, 1, 'step'], [10.6, 0]])
e.fx('glow', 'sparkle', x=360, y=1050, r=230, show=shown((0.1, 1.4), (4.1, 7.6)))
e.fx('bang', 'mark', x=430, y=720, char='!', scale=[[0, 0], [8.0, 0, 'step'], [8.15, 1.2, 'back'], [8.6, 0, 'step']])
e.fx('poof', 'dust', x=800, y=1250, scale=2.0, show=shown((9.5, 10.3)))
e.fx('fall', 'leaves', screen=True, n=18, seed=7, alpha=[[0, 0.0], [0.3, 1], [9.3, 1], [9.6, 0.5]])
e.fx('target', 'target', x=360, y=760, r=120, label='PUT YOUR\nFINGER HERE', label_size=56,
     alpha=[[0, 0], [0.9, 0], [1.1, 1], [3.75, 1], [3.85, 0]], scale=[[0, 0.3], [0.9, 0.3], [1.15, 1.0, 'back']])
e.fx('hand', 'hand', x=360, y=[[0, -900], [3.8, -900], [4.1, 700, 'out'], [8.5, 700], [8.9, -900, 'in']],
     rot=3.14159)
e.card('t1', 'KEEP THE LEAVES\nOFF NUGGET!', 0, 4.1, size=96, pulse=1)
e.card('t2', 'HE JUST GOT\nGROOMED!', 4.1, 7.9, size=100, fill='#FFE14D')
e.card('t3', 'WAIT... NUGGET\nNO!!!', 8.0, 9.6, size=104, fill='#FF8F6B')
e.card('t4', 'HE IS A\nLEAF NOW', 10.1, None, size=116, fill='#F7B733')
e.music('tense', 51, [[0, 1], [7.9, 1], [8.0, 0, 'step']])
e.music('playful', 52, [[0, 0], [9.6, 0, 'step'], [9.7, 1]])
for t, n, g in [(0.1, 'pop', 0.4), (0.9, 'swoosh', 0.35), (1.1, 'pop', 0.3), (3.85, 'whoosh', 0.6), (4.15, 'sparkle', 0.5),
                (4.3, 'aww', 0.4), (8.0, 'boing', 0.5), (8.05, 'meow', 0.8), (8.55, 'swoosh', 0.5), (9.5, 'crash', 0.5),
                (9.55, 'rustle', 1.0), (10.2, 'pop', 0.4), (10.4, 'purr', 0.7), (12.0, 'sparkle', 0.4)]:
    e.sfx(t, n, g)
e.d['audio']['sfx'][-5][3:] = [{'dur': 1.2}]
print(e.save())
