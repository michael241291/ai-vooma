import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('whipped-cream', 9.5, 'reaction', scene='dining',
       situation="on the Thanksgiving table a whipped-cream can sprays Nugget in the face (frame 0); shock, then he tastes it",
       twist="he paw-taps the can for MORE and ends up with a full cream helmet: 'WORTH IT'; he eats it down and gets sprayed again (loop)",
       title="The whipped cream fought back 😳🥧",
       description="He regrets nothing. Rate his face 1-10 👇\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #thanksgiving #whippedcream #funny #animation")
e.cam(zoom=[[0, 1.75], [1.0, 1.75], [1.1, 2.0, 'out'], [2.0, 1.85], [4.1, 1.85], [4.3, 1.3, 'out'], [5.3, 1.3], [5.6, 1.3, 'out'], [7.4, 1.3], [7.7, 1.6, 'out'], [9.5, 1.75]],
      fx=[[0, 560]], fy=[[0, 1000], [5.3, 1000], [5.6, 1050], [7.4, 1050], [7.7, 1000]],
      shake=[[0, 10], [0.9, 10], [1.0, 0, 'step'], [4.2, 0], [4.25, 12, 'step'], [5.2, 12], [5.25, 0, 'step'], [9.0, 0], [9.05, 10, 'step']])
e.prop('pie', 'pie', x=160, y=1420, scale=1.1)
e.nugget('nug', x=540, y=1264, scale=0.95, flip=1,
         eye=[[0, 'wide'], [1.0, 'big'], [2.6, 'heart'], [3.6, 'happy'], [4.2, 'squeeze'], [7.4, 'happy'], [9.0, 'wide']],
         look=[[0, [0.6, 0]], [2.0, [0, -0.2]], [3.6, [0.8, -0.1]], [7.4, [0, 0]], [9.0, [0.6, 0]]],
         mouth=[[0, 'o'], [1.0, 'line'], [2.0, 'open'], [2.6, 'smile'], [4.2, 'open'], [7.4, 'chew'], [9.0, 'o']],
         mk=[[0, 0.8], [1.0, 0.3], [2.0, 0.5]], tongue=[[0, False], [2.0, True], [2.6, False], [7.4, False]],
         puff=[[0, 0.8], [1.0, 0.5], [2.6, 0.0], [9.0, 0.8]], ear=[[0, -0.3], [1.0, 0.3], [2.6, 0], [9.0, -0.3]],
         blush=[[0, 0.35], [2.6, 0.9], [4.2, 0.4]], tail=[[0, 0.5], [2.6, 2.5], [9.0, 0.5]],
         paw=[[0, None], [3.4, None], [3.45, [150, -250], 'step'], [3.7, [230, -260]], [3.85, [170, -250]], [4.0, [230, -260]], [4.2, None, 'step']])
e.prop('can', 'whipcan', x=[[0, 880], [3.6, 880], [3.7, 905], [3.85, 880], [4.0, 905], [4.1, 880]], y=1075, rot=-1.5708, scale=0.9,
       spray=[[0, 1], [0.9, 1], [1.0, 0, 'step'], [4.2, 1, 'step'], [5.2, 1], [5.25, 0, 'step'], [9.0, 1, 'step']], jet=170)
e.fx('beard', 'cream', x=545, y=1080, w=170, h=95, seed=3, amount=[[0, 0.6], [0.9, 1.0], [2.0, 1.0], [2.6, 0.75], [4.2, 0.75], [4.3, 0, 'step'], [9.0, 0.3, 'step'], [9.5, 0.6]])
e.fx('helmet', 'cream', x=545, y=960, w=280, h=250, seed=9, amount=[[0, 0], [4.2, 0], [5.2, 1.0, 'out'], [7.4, 1.0], [8.9, 0.15], [9.0, 0, 'step']])
e.fx('love', 'hearts', x=560, y=820, show=shown((2.6, 3.5), (5.4, 7.4)))
e.fx('shine', 'sparkle', x=545, y=1060, r=160, show=shown((2.6, 3.4)))
e.card('t1', 'PFSSSHT!', 0, 1.0, size=150, y=330, fill='#FFFFFF', tilt=-0.08, pulse=1)
e.card('t2', '...', 1.0, 2.0, size=160, y=330)
e.card('t3', 'OH.', 2.0, 2.6, size=150, y=330, fill='#FFE14D')
e.card('t4', 'OHHHH.', 2.6, 3.4, size=150, y=330, fill='#FFE14D')
e.card('t5', 'AGAIN.', 3.4, 4.2, size=150, y=330, fill='#FF8F6B')
e.card('t6', 'WORTH IT.', 5.5, 7.4, size=150, y=1560, fill='#FFE14D', pulse=1)
e.card('t7', '*NOM NOM*', 7.5, 9.0, size=110, y=330)
e.card('t8', 'PFSSSHT!', 9.0, None, size=150, y=330, fill='#FFFFFF', tilt=-0.08, pulse=1)
e.music('playful', 401, [[0, 0.3], [1.0, 0.3], [1.05, 0, 'step'], [2.0, 0], [2.05, 1, 'step'], [9.0, 1], [9.05, 0.3, 'step']])
for t, n, g, o in [(0.0, 'static', 0.55, {'dur': 0.95}), (0.05, 'yowl', 0.7, {}), (1.0, 'thud', 0.4, {}), (2.0, 'slide_up', 0.4, {}),
                   (2.6, 'sparkle', 0.6, {}), (2.65, 'purr', 0.7, {'loop': True, 'dur': 0.8}), (3.45, 'tick', 0.8, {}), (3.7, 'tick', 0.8, {}),
                   (4.0, 'tick', 0.8, {}), (4.2, 'static', 0.65, {'dur': 1.0}), (4.25, 'boing', 0.5, {}), (5.5, 'ding', 0.6, {}),
                   (5.6, 'aww', 0.4, {}), (7.5, 'crunch', 0.5, {}), (8.1, 'crunch', 0.5, {}), (9.0, 'static', 0.55, {'dur': 0.5})]:
    e.sfx(t, n, g, **o)
print(e.save())
