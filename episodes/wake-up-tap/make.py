import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('wake-up-tap', 13, 'interactive_play', scene='bedroom_day',
       situation="the viewer taps a sleeping Nugget 3 times to wake him up; nothing, not even an ear",
       twist="a treat bag rustles off-screen and he is wide awake in 0.1 s; the bag leaves and he is instantly asleep again",
       title="Tap Nugget 3 times to wake him up 👆😴",
       description="Count with me: 1... 2... 3... nothing. Then the treat bag. 😴\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #interactive #funny #animation #sleepycat")
e.scene_tracks(wall=[[0, '#FFE8D6']])
e.cam(zoom=[[0, 1.08], [7.5, 1.08], [7.7, 1.0, 'out'], [11.3, 1.0], [11.5, 1.1, 'out']], fx=[[0, 560]], fy=[[0, 1200]],
      shake=[[0, 0], [7.6, 0], [7.62, 14, 'step'], [8.0, 0]])
pokes = [2.6, 4.0, 5.4]
sq = [[0, 0]]
for p in pokes:
    sq += [[p, 0], [p + 0.08, 0.35, 'out'], [p + 0.45, 0, 'elastic']]
e.nugget('nug', x=[[0, 520], [7.6, 520], [8.0, 600, 'out'], [11.4, 600]],
         y=[[0, 1330], [7.6, 1330], [7.8, 1020, 'out'], [8.0, 1290, 'in'], [11.4, 1290], [11.45, 1335, 'step']],
         scale=0.85, flip=1, pose=[[0, 'loaf'], [7.6, 'sit'], [11.4, 'loaf']],
         eye=[[0, 'closed'], [7.6, 'wide'], [8.4, 'big'], [9.6, 'heart'], [11.4, 'closed']],
         look=[[0, [0.6, 0.4]], [7.6, [0.9, 0.6]]], mouth=[[0, 'smile'], [7.6, 'o'], [8.4, 'pant'], [11.4, 'smile']], mk=[[0, 0.2], [7.6, 0.6]],
         squish=sq + [[7.5, 0]], ear=[[0, 0.1], [7.6, -0.3], [8.4, 0]], tail=[[0, 0.2], [7.6, 3.0], [11.4, 0.2]],
         paw=[[0, None], [9.55, None], [9.6, [150, -60]], [9.9, [150, -200], 'out'], [10.2, [150, -160]], [10.5, [150, -200]],
              [10.8, [150, -160]], [11.1, [150, -200]], [11.35, None, 'step']], blush=[[0, 0.5], [9.6, 0.9], [11.4, 0.5]])
e.prop('bag', 'foodbag', x=[[0, 1400], [7.1, 1400], [7.45, 930, 'out'], [11.3, 930], [11.7, 1450, 'in']], y=1560, scale=1.0,
       shake=[[0, 0], [7.1, 1], [9.0, 1], [9.2, 0], [11.3, 0], [11.35, 1]], label='CRUNCHY\nTREATS')
e.fx('zzz', 'zzz', x=600, y=1080, show=shown((0, 7.6), (11.45, 13.1)))
e.fx('zoomies', 'speed', x=430, y=1200, angle=3.6, show=shown((7.6, 8.1)))
e.fx('love', 'hearts', x=700, y=880, show=shown((9.6, 11.3)))
e.fx('target', 'target', x=540, y=1150, r=110, label='TAP HERE', label_size=56,
     alpha=[[0, 0], [0.8, 0], [1.0, 1], [6.2, 1], [6.3, 0]], scale=[[0, 0.3], [0.8, 0.3], [1.05, 1.0, 'back']])
fy = [[0, 2700], [2.2, 2700], [2.5, 1430, 'out']]
for p in pokes:
    fy += [[p, 1390, 'in'], [p + 0.2, 1450, 'out'], [p + 0.9, 1430]]
fy += [[6.3, 1430], [6.7, 2700, 'in']]
e.fx('finger', 'hand', x=560, y=fy, pose='finger', rot=-0.08)
e.card('t1', 'TAP NUGGET 3 TIMES\nTO WAKE HIM UP', 0, 2.6, size=88, pulse=1)
for i, p in enumerate(pokes):
    e.card(f'n{i}', str(i + 1), p, (pokes[i + 1] if i < 2 else 6.2), size=200, fill=['#FFE14D', '#FFB347', '#FF8F6B'][i])
e.card('t2', '...NOTHING.', 6.2, 7.2, size=120)
e.card('t3', '*TREAT BAG*', 7.2, 8.0, size=110, fill='#B9A6FF')
e.card('t4', '0.1 SECONDS.', 8.0, 9.6, size=116, fill='#FFE14D')
e.card('t5', 'GOOD MORNING\nTO THE BAG ONLY', 9.6, 11.4, size=96)
e.card('t6', 'BACK TO SLEEP.', 11.5, None, size=104, fill='#9BE7FF')
e.music('night', 91, [[0, 1], [7.1, 1], [7.15, 0, 'step'], [11.4, 0], [11.45, 1, 'step']])
e.music('triumph', 92, [[0, 0], [7.6, 0, 'step'], [7.65, 1], [11.35, 1], [11.4, 0, 'step']])
for i, p in enumerate(pokes):
    e.sfx(p, 'pop', 0.7, rate=1.0 + 0.15 * i)
    e.sfx(p + 0.05, 'boing', 0.3, dur=0.5)
for t, n, g, o in [(0.1, 'purr_long', 0.4, {'dur': 2.4}), (6.25, 'tick', 0.6, {}), (7.15, 'rustle', 1.0, {'dur': 1.9}),
                   (7.6, 'whoosh', 0.7, {}), (7.65, 'meow', 0.9, {'rate': 1.2}), (8.0, 'thud', 0.6, {}), (9.6, 'aww', 0.5, {}),
                   (10.3, 'meow', 0.6, {'rate': 1.35}), (11.35, 'rustle', 0.6, {'dur': 0.4}), (11.45, 'slide_down', 0.5, {}),
                   (11.6, 'purr_long', 0.5, {'dur': 1.4})]:
    e.sfx(t, n, g, **o)
print(e.save())
