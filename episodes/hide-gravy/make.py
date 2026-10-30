import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('hide-gravy', 14, 'interactive_protect', scene='backyard',
       situation="a giant dinner fork hunts Gravy the turkey in the backyard; the viewer's palm hides him while the fork stabs left, right, then bonks the hand",
       twist="the fork gives up; Gravy rolls out a pizza box: 'THANKSGIVING PLAN B: PIZZA', and Nugget sprints in for a slice",
       title="Hide Gravy before Thanksgiving! 🦃🍕",
       description="Put your hand on the screen and keep Gravy safe. He has a plan B. 🍕\n\nGravy the turkey and Nugget the orange cat. New video every day.\n\n#shorts #turkey #thanksgiving #interactive #funny #animation")
e.scene_tracks(sky1=[[0, '#F7B98A']], sky2=[[0, '#FFE9C7']])
e.cam(zoom=[[0, 1.0], [7.25, 1.0], [7.4, 1.1, 'out'], [8.2, 1.04], [14, 1.06]], fx=[[0, 540]], fy=[[0, 1250]],
      shake=[[0, 0], [4.8, 0], [4.82, 12, 'step'], [5.1, 0], [6.2, 0], [6.22, 12, 'step'], [6.5, 0], [7.35, 0], [7.37, 18, 'step'], [7.8, 0]])
e.prop('pizza', 'pizzabox', x=[[0, 1450], [9.6, 1450], [10.0, 820, 'out']], y=1640, scale=1.0, label='PLAN B',
       open=[[0, 0], [10.2, 0], [10.6, 1, 'back']])
e.prop('gravy', 'turkey', x=[[0, 520]], y=1560, scale=0.92, flip=1,
       eye=[[0, 'wide'], [9.0, 'happy'], [10.6, 'heart']], look=[[0, [0, -0.9]], [4.4, [-0.8, -0.3]], [5.8, [0.8, -0.3]], [7.0, [0, -0.9]], [9.0, [0, 0]]],
       mouth=[[0, 'scream'], [3.9, 'open'], [9.0, 'smile'], [10.6, 'open']], sweat=[[0, True], [9.0, False]],
       flap=[[0, 0.8], [3.9, 0.1], [9.0, 0.2], [9.2, 1.0, 'out'], [9.6, 0.3], [10.6, 1.0, 'out'], [11.0, 0.4]], fan=[[0, 1.2], [3.9, 0.7], [9.0, 1.1]],
       bob=[[0, 0], [9.0, 0], [9.05, 1, 'step'], [9.6, 0, 'step'], [10.6, 1, 'step'], [12.0, 0, 'step']], blush=[[0, 0.3], [10.6, 0.9]])
e.nugget('nug', x=[[0, -400], [12.2, -400], [12.8, 190, 'out']], y=1300, scale=0.72, flip=1,
         pose=[[0, 'run'], [12.75, 'sit']], run_speed=1.8, eye=[[0, 'heart']], mouth=[[0, 'open']], mk=[[0, 0.7]], tongue=True,
         look=[[0, [0.9, 0.8]]], tail=[[0, 3.0]])
fx_ = [[0, 540], [4.0, 540], [4.4, 280], [5.3, 280], [5.8, 800], [6.6, 800], [7.0, 540]]
fy_ = [[0, 640], [0.5, 700], [1.0, 640], [1.5, 700], [2.0, 640], [2.5, 700], [3.0, 640], [3.5, 700], [4.4, 560],
       [4.8, 1450, 'in'], [5.3, 560, 'out'], [5.8, 560], [6.2, 1450, 'in'], [6.6, 560, 'out'], [7.0, 560], [7.35, 1080, 'in'],
       [7.5, 800, 'out'], [8.2, -1200, 'in']]
e.prop('fork', 'fork', x=fx_, y=fy_, scale=1.0, rot=[[0, 0.0], [7.35, 0.0], [7.5, 0.25, 'out'], [8.2, 0.6]])
e.fx('target', 'target', x=540, y=1250, r=130, label='COVER HIM!', label_size=60,
     alpha=[[0, 0], [0.9, 0], [1.1, 1], [3.6, 1], [3.7, 0]], scale=[[0, 0.3], [0.9, 0.3], [1.15, 1.0, 'back']])
e.fx('hand', 'hand', x=540, y=[[0, 2700], [3.6, 2700], [3.9, 1360, 'out'], [9.0, 1360], [9.35, 2700, 'in']],
     rot=[[0, 0.04], [7.35, -0.1], [7.6, 0.04]])
e.fx('bonk', 'stars', x=540, y=1080, scale=0.6, show=shown((7.4, 8.4)))
e.fx('fall', 'leaves', screen=True, n=10, seed=21)
e.fx('love', 'hearts', x=640, y=1050, show=shown((10.6, 14.1)))
e.card('t1', 'HIDE GRAVY BEFORE\nTHANKSGIVING!', 0, 4.4, size=90, pulse=1)
e.card('t2', 'LEFT!', 4.4, 5.6, size=130, fill='#FF8F6B')
e.card('t3', 'RIGHT!', 5.8, 6.9, size=130, fill='#FF8F6B')
e.card('t4', 'IT GAVE UP!', 7.6, 9.3, size=116, fill='#FFE14D')
e.card('t5', 'THANKSGIVING\nPLAN B: PIZZA', 10.2, 12.4, size=100, fill='#F7B733')
e.card('t6', 'NUGGET\nAPPROVES', 12.4, None, size=116, fill='#9BE7FF')
e.music('tense', 111, [[0, 1], [7.3, 1], [7.35, 0, 'step']])
e.music('hoedown', 112, [[0, 0], [9.0, 0, 'step'], [9.05, 1]])
for t, n, g, o in [(0.05, 'gobble', 0.9, {}), (0.9, 'swoosh', 0.35, {}), (1.1, 'pop', 0.3, {}), (3.65, 'whoosh', 0.6, {}),
                   (4.5, 'swoosh', 0.6, {}), (4.8, 'thud', 1.0, {}), (5.9, 'swoosh', 0.6, {}), (6.2, 'thud', 1.0, {}),
                   (7.1, 'swoosh', 0.6, {}), (7.35, 'boing', 0.8, {'dur': 0.9, 'fade': 0.3}), (7.36, 'thud', 0.8, {}),
                   (7.6, 'slide_up', 0.5, {}), (9.0, 'gobble', 1.0, {}), (9.6, 'slide_down', 0.4, {}), (10.2, 'pop', 0.5, {}),
                   (10.3, 'sparkle', 0.6, {}), (10.6, 'aww', 0.5, {}), (12.2, 'run', 0.6, {'loop': True, 'dur': 0.6}),
                   (12.8, 'meow', 0.9, {'rate': 1.15}), (13.1, 'crunch', 0.6, {})]:
    e.sfx(t, n, g, **o)
print(e.save())
