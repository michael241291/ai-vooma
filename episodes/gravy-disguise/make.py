import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('gravy-disguise', 13.5, 'new_character', scene='living_b',
       situation="NEW CHARACTER Gravy the turkey sees the calendar flip to November, panics, and comes back disguised as a cat (paper ears + marker whiskers) next to Nugget",
       twist="the owner falls for it and pets him... until Thanksgiving: 'WHERE'S THE TURKEY?' and Nugget silently points at him: 'NUGGET IS A SNITCH'",
       title="POV: you're a turkey and it's November 🦃😰",
       description="Meet Gravy. He has 26 days and one plan. 🦃\n\nNugget the orange cat and his new roommate Gravy. New video every day.\n\n#shorts #turkey #thanksgiving #cat #funny #animation")
e.scene_tracks(wall=[[0, '#E4D7F2']])
e.cam(zoom=[[0, 1.0], [0.95, 1.0], [1.1, 1.14, 'out'], [2.3, 1.06], [11.3, 1.06], [11.45, 1.16, 'out'], [13.5, 1.12]],
      fx=[[0, 540], [11.3, 540], [11.45, 470]], fy=[[0, 1150]], shake=[[0, 0], [1.0, 0], [1.02, 12, 'step'], [1.6, 0]])
e.prop('cal', 'calendar', x=300, y=420, scale=0.72,
       month=[[0, 'OCTOBER'], [0.8, 'NOVEMBER', 'step'], [9.8, 'NOVEMBER']], color=[[0, '#E8552B'], [0.8, '#7A4A2E', 'step']],
       day=[[0, '31'], [0.8, '1', 'step'], [10.0, '26', 'step']], circle=[[0, False], [10.0, True]],
       flip=[[0, 0], [0.5, 0, 'step'], [0.8, 1, 'linear'], [0.81, 0, 'step'], [9.7, 0], [10.0, 1, 'linear'], [10.01, 0, 'step']])
e.nugget('nug', x=270, y=[[0, 1340], [5.7, 1340], [5.9, 1290, 'out']], scale=0.78, flip=1,
         pose=[[0, 'loaf'], [5.7, 'sit']], eye=[[0, 'closed'], [5.7, 'normal'], [11.3, 'normal']],
         lid=[[0, 0], [5.7, 0.0], [6.6, 0.45], [7.6, 0.0], [11.3, 0.55]], look=[[0, [0.9, 0.2]]],
         mouth=[[0, 'smile'], [5.7, 'line'], [7.8, 'frown'], [11.3, 'line']], tail=[[0, 0.3], [11.3, 0.3]],
         paw=[[0, None], [11.35, None], [11.4, [180, -40]], [11.7, [300, -200], 'out']], headtilt=[[0, 0], [6.2, 0.25], [7.4, 0.0]])
e.fx('zzz', 'zzz', x=320, y=980, show=shown((0, 5.6)))
e.prop('gravy', 'turkey', x=[[0, 640], [2.4, 640], [3.2, -320, 'in'], [4.4, -320], [5.4, 650, 'out']],
       y=1500, scale=0.8, flip=[[0, 1], [2.35, -1, 'step'], [4.4, 1, 'step']],
       walk=[[0, False], [2.4, True], [3.2, False], [4.4, True], [5.4, False]], bob=[[0, 0], [2.4, 1], [3.2, 0], [4.4, 1], [5.4, 0]],
       eye=[[0, 'happy'], [1.0, 'wide'], [4.4, 'normal'], [5.5, 'happy'], [7.6, 'normal'], [7.9, 'happy'], [9.8, 'wide'], [11.4, 'wide']],
       look=[[0, [0, 0]], [9.8, [-0.6, -0.5]], [11.4, [-0.9, 0.2]]],
       mouth=[[0, 'smile'], [1.0, 'scream'], [2.4, 'open'], [4.4, 'smile'], [5.5, 'open'], [6.2, 'smile'], [9.8, 'open'], [11.4, 'scream']],
       flap=[[0, 0], [1.0, 0, 'step'], [1.1, 1, 'out'], [2.4, 0.6], [3.2, 0], [11.4, 0], [11.5, 1, 'out']],
       fan=[[0, 1.0], [1.0, 1.0], [1.1, 1.25, 'out'], [3.0, 1.0]],
       sweat=[[0, False], [1.0, True], [3.2, False], [9.8, True]],
       disguise=[[0, False], [4.0, True, 'step']], blush=[[0, 0.4], [7.9, 0.9], [9.8, 0.3]])
e.fx('panic', 'burst', x=640, y=1150, r=230, color='#E2463F', show=shown((1.0, 2.3)))
e.fx('huh', 'mark', x=330, y=760, char='?', color='#FFFFFF', scale=[[0, 0], [6.0, 0, 'step'], [6.15, 1.0, 'back'], [7.5, 1.0], [7.55, 0, 'step']])
e.fx('hand', 'hand', x=[[0, 640], [7.9, 640], [8.2, 600], [8.5, 680], [8.8, 600], [9.1, 680], [9.4, 640]],
     y=[[0, -900], [7.5, -900], [7.9, 880, 'out'], [9.4, 880], [9.75, -900, 'in']], rot=3.14159, pose='palm')
e.fx('love', 'hearts', x=640, y=1000, show=shown((8.0, 9.8)))
e.fx('busted', 'mark', x=660, y=760, char='!!', color='#FF5A4E', scale=[[0, 0], [11.4, 0, 'step'], [11.55, 1.1, 'back']])
e.card('t1', "POV: YOU'RE A TURKEY\nAND IT'S NOVEMBER", 0, 3.2, size=84, pulse=1)
e.card('t2', '5 MINUTES LATER...', 3.2, 4.6, size=96, fill='#9BE7FF')
e.card('t3', 'I AM CAT.\nMEOW.', 5.5, 7.6, size=116, fill='#F7A24E')
e.card('t4', "IT'S WORKING?!", 7.9, 9.8, size=110, fill='#FFE14D')
e.card('t5', "THANKSGIVING:\n\"WHERE'S THE TURKEY?\"", 9.9, 11.4, size=84)
e.card('t6', 'NUGGET IS\nA SNITCH', 11.4, None, size=120, fill='#FF8F6B')
e.music('sneaky', 71, [[0, 0.8], [0.95, 0.8], [1.0, 0.25, 'step'], [2.3, 0.25], [2.4, 1], [9.8, 1], [9.85, 0.3, 'step'], [11.35, 0.3], [11.4, 0, 'step']])
e.music('hoedown', 72, [[0, 0], [11.4, 0, 'step'], [11.5, 1]])
for t, n, g, o in [(0.5, 'swoosh', 0.4, {}), (1.0, 'gobble', 1.0, {}), (1.05, 'scared', 0.7, {'start': 0.3, 'dur': 1.2, 'fade': 0.3}),
                   (2.4, 'run', 0.6, {'loop': True, 'dur': 0.9}), (3.2, 'pop', 0.4, {}), (4.4, 'run', 0.5, {'loop': True, 'dur': 1.0}),
                   (5.6, 'meow', 0.9, {'rate': 0.72}), (6.05, 'boing', 0.4, {'dur': 0.6}), (7.9, 'purr_long', 0.6, {'dur': 1.8}),
                   (8.1, 'aww', 0.5, {}), (9.7, 'swoosh', 0.4, {}), (9.9, 'ding', 0.6, {}), (10.4, 'heartbeat', 0.7, {}),
                   (11.4, 'gobble', 1.0, {}), (11.45, 'whoosh', 0.5, {})]:
    e.sfx(t, n, g, **o)
print(e.save())
