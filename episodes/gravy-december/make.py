import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('gravy-december', 11.8, 'skit_seasonal', scene='living',
       situation="December 1st: Gravy the turkey survived Thanksgiving and throws a one-turkey dance party in the living room, confetti flying",
       twist="the wall calendar flips to DECEMBER 25 with 'CHRISTMAS DINNER' circled; Gravy freezes, screams and faints; viewer votes 1 (safe) or 2 (not safe)",
       title="The turkey thought he was safe 🦃🎄",
       description="He had 24 good days left. Is Gravy safe? Comment 1 or 2 👇\n\nTiny Chaos: life's little chaos, animated. New video every day.\n\n#shorts #turkey #christmas #thanksgiving #funny #animation",
       experiment=False)
e.scene_tracks(wall=[[0, '#7FC8A9']])
GY = 1470
e.cam(zoom=[[0, 1.3], [3.6, 1.3], [4.1, 1.0, 'out'], [6.4, 1.0], [6.9, 1.7, 'out'], [7.9, 1.7], [8.2, 1.15, 'in']],
      fx=[[0, 540]], fy=[[0, 1100], [3.6, 1100], [4.1, 960, 'out'], [6.4, 960], [6.9, 820, 'out'], [7.9, 820], [8.2, 1000, 'in']],
      px=[[0, 0], [6.4, 0], [6.9, 180, 'out'], [7.9, 180], [8.2, 0, 'in']],
      shake=[[0, 0], [8.2, 0], [8.25, 22, 'step'], [8.7, 0]])
dance = []
for k in range(14):
    dance.append([k * 0.45, 0.95 if k % 2 == 0 else 0.15])
e.prop('cal', 'calendar', x=760, y=600, scale=0.9, month=[[0, 'DECEMBER'], [6.75, 'DECEMBER', 'step']],
       day=[[0, 1], [6.75, 25, 'step']], color='#2E8B57', circle=[[0, False], [6.8, True, 'step']],
       flip=[[0, 0], [6.4, 0], [6.75, 0.5, 'linear'], [7.1, 1.0, 'linear'], [7.11, 0, 'step']])
e.prop('tagx', 'sign', x=760, y=1050, scale=0.95, label='XMAS DINNER', show=[[0, False], [7.1, True, 'step']])
e.prop('gravy', 'turkey', x=[[0, 430], [3.6, 430], [6.4, 520]], y=GY, scale=0.95, flip=[[0, 1], [1.8, -1, 'step'], [3.6, 1, 'step'], [6.4, -1, 'step']],
       eye=[[0, 'happy'], [6.4, 'side'], [7.6, 'wide', 'step'], [8.2, 'closed', 'step']],
       look=[[0, [0, 0]], [6.4, [1, -1]]],
       mouth=[[0, 'scream'], [0.9, 'smile'], [2.4, 'open'], [3.6, 'smile'], [6.4, 'closed'], [7.6, 'scream', 'step']],
       flap=dance[:14] + [[6.4, 0.0], [7.6, 1.0, 'step']], fan=[[0, 1.25]], bob=1, walk=[[0, True], [6.4, False, 'step']],
       rot=[[0, 0], [8.2, 0], [8.55, 1.45, 'in']], sweat=[[0, False], [7.6, True, 'step']], blush=[[0, 0.7], [6.4, 0]])
e.fx('stars', 'stars', x=430, y=1000, show=shown((0, 6.4)))
e.fx('spark', 'sparkle', x=430, y=1050, r=330, show=shown((0, 6.4)))
e.card('t1', 'DEC 1ST.\nHE SURVIVED\nTHANKSGIVING', 0, 3.6, size=84, fill='#FFE14D')
e.card('t2', 'VICTORY DANCE', 3.6, 6.4, size=120, fill='#7CF0A0', tilt=-0.05)
e.card('t3', 'WAIT.', 6.4, 7.6, size=150, fill='#FF6B6B')
e.card('t4', 'IS HE SAFE?', 8.3, None, size=120, fill='#FFFFFF')
e.card('o1', '1) YES', 8.6, None, size=90, fill='#3DDC84', y=1250, x=330)
e.card('o2', '2) NO', 8.8, None, size=90, fill='#FF5A5F', y=1250, x=750)
e.music('triumph', 1203, [[0, 1], [6.35, 1], [6.4, 0.0, 'step'], [8.3, 0.0], [8.6, 0.5]])
for t, n, g, o in [(0.0, 'gobble', 1.0, {}), (0.05, 'sparkle', 0.6, {}), (1.8, 'boing', 0.6, {}), (3.6, 'gobble', 0.8, {}),
                   (3.6, 'whoosh', 0.6, {}), (6.4, 'tick', 0.9, {}), (6.75, 'swoosh', 0.7, {}), (7.1, 'ding', 0.8, {}),
                   (7.6, 'gobble', 1.0, {'rate': 1.3}), (7.7, 'scared', 0.8, {'start': 0.3, 'dur': 1.2}), (8.25, 'thud', 1.0, {}),
                   (8.6, 'pop', 0.7, {}), (8.8, 'pop', 0.7, {})]:
    e.sfx(t, n, g, **o)
print(e.save())
