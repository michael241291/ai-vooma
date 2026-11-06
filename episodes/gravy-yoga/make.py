import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('gravy-yoga', 11, 'new_character', scene='bedroom_day',
       situation="8 days before Thanksgiving Gravy the turkey does frantic yoga to get too skinny to eat ('OPERATION: TOO SKINNY'), weighs in at 24.9 lb",
       twist="after the yoga montage the scale says 35.6 LB: the camera finds Nugget sitting on the back of the scale behind Gravy's tail, chewing, 'NUGGET IS NOT HELPING'",
       title="POV: it's 8 days before Thanksgiving 🦃🧘",
       description="Gravy is doing his best. Nugget is... helping? 👇\n\nGravy the turkey and Nugget the orange cat. New video every day.\n\n#shorts #turkey #thanksgiving #yoga #funny #animation",
       experiment=True)
e.scene_tracks(wall=[[0, '#E6DDF7']])
e.cam(zoom=[[0, 1.35], [1.9, 1.35], [2.0, 1.15, 'step'], [3.2, 1.15], [3.25, 1.5, 'step'], [3.9, 1.5], [3.95, 1.2, 'step'], [4.6, 1.2], [4.65, 1.6, 'step'],
            [5.3, 1.6], [5.35, 1.25, 'step'], [6.1, 1.25], [6.2, 1.15, 'step'], [7.5, 1.15], [7.9, 1.45, 'out'], [9.0, 1.45], [9.3, 1.3, 'out']],
      fx=[[0, 560]], fy=[[0, 1250]],
      px=[[0, 0], [1.9, 0], [2.0, 150, 'step'], [3.2, 150], [3.25, 0, 'step'], [6.1, 0], [6.2, 150, 'step'], [7.5, 150], [7.9, 130, 'out'], [9.0, 130], [9.3, 80, 'out']],
      py=[[0, 0], [7.5, 0], [7.9, 60, 'out'], [9.0, 60], [9.3, 0]],
      shake=[[0, 0], [6.6, 0], [6.65, 10, 'step'], [7.4, 0]])
e.prop('cal', 'calendar', x=930, y=560, scale=0.55, month='NOV', day=18, circle=True)
e.prop('mat', 'yogamat', x=470, y=1470, scale=1.0)
e.prop('scale', 'scale', x=880, y=1470, scale=1.2, reading=[[0, '0.0'], [2.1, '24.9', 'step'], [3.1, '0.0', 'step'], [6.3, '24.9', 'step'], [6.5, '29.8', 'step'],
                                                         [6.6, '33.1', 'step'], [6.7, '35.6', 'step'], [8.1, '10.7', 'step']], glow=[[0, 0], [6.7, 1, 'step']])
e.nugget('nug', x=[[0, 1010], [7.9, 1010], [8.2, 900, 'out']], y=1335, scale=0.62, flip=-1, show=[[0, False], [5.9, True, 'step']],
         eye=[[0, 'happy'], [7.9, 'normal'], [9.3, 'closed']], look=[[0, [-0.6, 0]], [7.9, [0, 0.2]]], mouth=[[0, 'chew'], [7.9, 'smile'], [9.3, 'smile']],
         blush=0.6, tail=[[0, 2.0]], headtilt=[[0, 0.15]])
GX = [[0, 470], [1.9, 470], [2.0, 860, 'step'], [3.2, 860], [3.25, 470, 'step'], [6.1, 470], [6.2, 860, 'step'], [7.8, 860], [8.1, 600, 'out']]
e.prop('gravy', 'turkey', x=GX, y=[[0, 1450], [2.0, 1420, 'step'], [3.25, 1450, 'step'], [6.2, 1420, 'step'], [7.8, 1420], [7.95, 1300, 'out'], [8.1, 1450, 'in']], scale=0.82,
       flip=[[0, 1], [3.95, -1, 'step'], [4.65, 1, 'step'], [5.35, -1, 'step'], [6.2, 1, 'step'], [8.1, -1, 'step']],
       rot=[[0, -0.22], [0.5, 0.22], [1.0, -0.22], [1.5, 0.22], [1.9, 0.0], [3.25, 0.5, 'step'], [3.95, -0.6, 'step'], [4.65, 0.9, 'step'], [5.35, -0.3, 'step'], [6.1, 0.0, 'step']],
       eye=[[0, 'closed'], [2.0, 'normal'], [2.5, 'happy'], [3.25, 'closed'], [6.2, 'normal'], [6.7, 'wide'], [9.0, 'side']],
       mouth=[[0, 'closed'], [2.5, 'smile'], [3.25, 'open'], [6.2, 'closed'], [6.7, 'scream'], [9.0, 'closed']],
       flap=[[0, 1.0], [1.9, 0.2], [3.25, 1.0, 'step'], [3.95, 0.3, 'step'], [4.65, 1.0, 'step'], [5.35, 0.6, 'step'], [6.2, 0.1, 'step'], [6.7, 1.0, 'out'], [7.4, 0.4]],
       fan=[[0, 1.1], [6.7, 1.4]], sweat=[[0, True], [2.0, False], [3.25, True], [6.2, False], [6.7, True]], blush=[[0, 0.3]],
       look=[[0, [0, -0.3]], [6.2, [0, 0.8]], [9.0, [0.9, 0.2]]])
e.fx('steam', 'speed', x=470, y=1100, angle=1.57, length=200, show=shown((3.25, 6.1)))
e.fx('love', 'sparkle', x=880, y=1100, r=160, show=shown((2.3, 3.1)))
e.card('t1', '8 DAYS TO THANKSGIVING', 0, 2.0, size=82, fill='#FFE14D')
e.card('t1b', 'OPERATION: TOO SKINNY TO EAT', 0, 2.0, size=56, y=345, fill='#FFFFFF')
e.card('t2', 'START: 24.9 LB', 2.1, 3.2, size=110, fill='#7CF0A0')
e.card('t3', '*INTENSE YOGA*', 3.25, 6.1, size=104, fill='#FF8F6B', pulse=1)
e.card('t4', '35.6 LB?!', 6.7, 8.1, size=150, fill='#FF5A4E', pulse=1)
e.card('t5', 'NUGGET IS\nNOT HELPING', 8.1, None, size=110, fill='#FFE14D')
e.card('t6', 'IS HE HELPING?', 9.3, None, size=70, y=1560, fill='#FFFFFF')
e.music('hoedown', 901, [[0, 0.6], [3.2, 0.6], [3.25, 1.0, 'step'], [6.1, 1.0], [6.15, 0.0, 'step'], [7.9, 0.0], [7.95, 0.6, 'step']])
for t, n, g, o in [(0.05, 'gobble', 0.7, {}), (0.5, 'wobble', 0.4, {}), (2.0, 'boing', 0.6, {}), (2.1, 'ding', 0.6, {}), (3.25, 'swoosh', 0.6, {}),
                   (3.95, 'swoosh', 0.6, {}), (4.65, 'swoosh', 0.6, {}), (5.35, 'swoosh', 0.6, {}), (6.2, 'boing', 0.5, {}),
                   (6.3, 'tick', 0.8, {}), (6.5, 'tick', 0.8, {}), (6.6, 'tick', 0.8, {}), (6.7, 'slide_up', 0.6, {}), (6.75, 'gobble', 1.0, {}),
                   (7.9, 'crunch', 0.6, {}), (8.3, 'crunch', 0.6, {}), (9.3, 'purr', 0.6, {'loop': True, 'dur': 1.5})]:
    e.sfx(t, n, g, **o)
print(e.save())
