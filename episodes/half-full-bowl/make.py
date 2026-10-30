import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('half-full-bowl', 13, 'relatable_owner', scene='kitchen',
       situation="Nugget screams 'EMERGENCY' at a bowl that is still half full, then faints dramatically",
       twist="the owner just shakes the bowl so the food spreads out: 'A FEAST!' He eats 3 pieces, walks away, and screams again",
       title="The bowl is NOT empty, Nugget 🙄🥣",
       description="Every cat owner has shaken a half-full bowl at 6am. Every. Single. Day. 🥣\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #catlife #funny #animation #relatable")
e.scene_tracks(wall=[[0, '#FFE3C2']])
e.cam(zoom=[[0, 1.05], [1.8, 1.05], [2.1, 1.55, 'out'], [3.8, 1.55], [4.1, 1.05], [13, 1.08]],
      fx=[[0, 540], [1.8, 540], [2.1, 720], [3.8, 720], [4.1, 540]], fy=[[0, 1250], [1.8, 1250], [2.1, 1390], [3.8, 1390], [4.1, 1250]],
      shake=[[0, 8], [1.7, 8], [1.8, 0, 'step'], [11.4, 0], [11.45, 10, 'step'], [12.6, 10]])
e.prop('bowl', 'bowl2', x=[[0, 720], [6.9, 720], [7.0, 700], [7.1, 740], [7.2, 700], [7.3, 740], [7.4, 700], [7.5, 720]],
       y=1470, scale=1.45, label='NUGGET', hole=[[0, 0.75], [7.5, 0.75], [7.55, 0.0, 'step'], [10.0, 0.0], [10.05, 0.25, 'step']])
e.nugget('nug', x=[[0, 330], [10.4, 330], [11.2, 200, 'inout']], y=[[0, 1290], [4.2, 1290], [4.5, 1360, 'in'], [8.0, 1360], [8.3, 1290, 'out']],
         scale=0.85, flip=[[0, 1], [10.3, -1, 'step'], [11.3, 1, 'step']],
         pose=[[0, 'sit'], [4.4, 'loaf'], [8.1, 'sit'], [10.3, 'run'], [11.2, 'sit']],
         eye=[[0, 'squeeze'], [1.8, 'wide'], [4.4, 'dizzy'], [7.6, 'big'], [8.4, 'heart'], [9.0, 'happy'], [10.2, 'normal'], [11.4, 'squeeze']],
         look=[[0, [0.9, 0.6]], [7.6, [0.9, 0.7]], [11.3, [0.9, 0.5]]],
         mouth=[[0, 'scream'], [1.8, 'frown'], [4.4, 'line'], [7.6, 'o'], [8.4, 'open'], [9.0, 'chew'], [10.2, 'line'], [11.4, 'scream']],
         mk=[[0, 1.0], [1.8, 0.4], [7.6, 0.6], [11.4, 1.0]], red=[[0, 0.35], [1.8, 0.0], [11.4, 0.35]],
         ear=[[0, -0.2], [1.8, 0.4], [4.4, 1.0], [7.6, -0.2], [8.6, 0]], tail=[[0, 3.0], [1.8, 0.3], [8.4, 2.0]],
         headtilt=[[0, 0], [10.2, 0], [10.3, 0.2]], blush=[[0, 0.35], [8.4, 0.9], [10.2, 0.35]])
e.fx('alarm', 'burst', x=330, y=960, r=280, color='#E2463F', show=shown((0, 1.8), (11.4, 13.1)))
e.fx('bang', 'mark', x=520, y=720, char='!!', color='#FF5A4E', scale=[[0, 1.0]], show=shown((0, 1.8), (11.4, 13.1)))
e.fx('rip', 'stars', x=330, y=1060, scale=0.7, show=shown((4.6, 7.4)))
e.fx('hand', 'hand', x=[[0, 720], [6.9, 720], [7.0, 700], [7.1, 740], [7.2, 700], [7.3, 740], [7.4, 700], [7.5, 720]],
     y=[[0, -900], [6.4, -900], [6.85, 1120, 'out'], [7.6, 1120], [7.95, -900, 'in']], rot=3.14159, pose='palm')
e.fx('love', 'hearts', x=380, y=880, show=shown((8.4, 10.2)))
e.fx('shine', 'sparkle', x=720, y=1380, r=200, show=shown((7.55, 8.6)))
e.card('t1', 'EMERGENCY!!!\nTHE BOWL IS EMPTY!', 0, 1.8, size=92, fill='#FF8F6B', pulse=1)
e.card('t2', 'THE BOWL:', 1.8, 4.1, size=110)
e.card('t2b', 'HALF FULL.', 2.4, 4.1, size=120, fill='#FFE14D', y=420)
e.card('t3', "HE HAS BEEN STARVING\nFOR 0 MINUTES", 4.3, 6.5, size=84)
e.card('t4', '*SHAKES BOWL*', 6.6, 7.9, size=110, fill='#9BE7FF')
e.card('t5', 'A FEAST!!!\nTHANK YOU!!!', 8.0, 10.2, size=104, fill='#FFE14D')
e.card('t6', '*ATE 3 PIECES*', 10.2, 11.4, size=100)
e.card('t7', 'EMERGENCY!!!', 11.4, None, size=116, fill='#FF8F6B', pulse=1)
e.music('playful', 61, [[0, 0.5], [1.8, 0.5], [1.85, 1, 'step'], [4.3, 1], [4.35, 0.2, 'step'], [6.5, 0.2], [6.55, 1, 'step'], [11.35, 1], [11.4, 0.4, 'step']])
for t, n, g, o in [(0.05, 'yowl', 0.9, {}), (0.9, 'meow', 0.8, {'rate': 1.15}), (1.85, 'ding', 0.5, {}), (2.4, 'pop', 0.5, {}),
                   (4.35, 'slide_down', 0.6, {}), (4.6, 'thud', 0.7, {}), (6.45, 'whoosh', 0.5, {}), (6.9, 'crunch', 0.6, {}),
                   (7.15, 'crunch', 0.6, {}), (7.4, 'crunch', 0.6, {}), (7.6, 'sparkle', 0.6, {}), (8.05, 'aww', 0.5, {}),
                   (8.9, 'crunch', 0.8, {}), (9.3, 'crunch', 0.8, {}), (9.7, 'crunch', 0.8, {}), (10.25, 'pop', 0.4, {}),
                   (11.4, 'yowl', 0.9, {}), (12.1, 'meow', 0.8, {'rate': 1.2})]:
    e.sfx(t, n, g, **o)
print(e.save())
