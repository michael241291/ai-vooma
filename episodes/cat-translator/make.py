import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('cat-translator', 11, 'translator', scene='hallway',
       situation="4AM in the hallway with a 'CAT TRANSLATOR: ON' badge: every meow gets a bottom subtitle ('I HAVE NOT EATEN IN 400 YEARS', 'NOT THAT FOOD')",
       twist="owner pets him: 'YOU MAY CONTINUE. FOR 3 SECONDS.' - chomp at second 4 - then he screams the starving line again next to a full bowl (loop)",
       title="I turned on the cat translator at 4AM 😐",
       description="The bowl was full the entire time. Which line is your cat? 👇\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #cattranslator #catlife #funny #animation",
       experiment=True)
e.scene_tracks(wall=[[0, '#C9D6F2']], dark=[[0, 0.32]])
e.cam(zoom=[[0, 1.55], [2.0, 1.55], [2.3, 1.15, 'out'], [4.8, 1.15], [5.1, 1.45, 'out'], [7.1, 1.45], [7.2, 1.7, 'out'], [8.4, 1.6], [8.6, 1.15, 'out'], [11, 1.2]],
      fx=[[0, 430], [2.0, 430], [2.3, 560], [4.8, 560], [5.1, 450], [8.4, 450], [8.6, 560]], fy=[[0, 1000], [2.0, 1000], [2.3, 1250], [4.8, 1250], [5.1, 980], [8.4, 980], [8.6, 1250]],
      shake=[[0, 9], [1.6, 9], [1.7, 0, 'step'], [7.15, 0], [7.2, 14, 'step'], [7.9, 0], [8.6, 0], [8.65, 9, 'step']])
e.prop('bowl', 'bowl2', x=770, y=1345, scale=1.2, label='NUGGET', hole=[[0, 0.0]])
e.nugget('nug', x=420, y=1264, scale=0.95, flip=1,
         eye=[[0, 'squeeze'], [1.7, 'normal'], [2.5, 'big'], [5.4, 'happy'], [7.2, 'wide'], [8.0, 'normal'], [8.6, 'squeeze']],
         look=[[0, [0, -0.3]], [1.7, [0.2, -0.6]], [2.5, [0.9, 0.6]], [3.6, [-0.2, -0.6]], [5.4, [0, 0]], [8.0, [-0.1, 0]]],
         mouth=[[0, 'scream'], [1.7, 'line'], [2.5, 'frown'], [3.6, 'line'], [5.4, 'smile'], [7.2, 'open'], [8.0, 'line'], [8.6, 'scream']],
         mk=[[0, 1.0], [1.7, 0.4], [7.2, 0.9], [8.0, 0.4], [8.6, 1.0]], puff=[[0, 0.5], [1.7, 0.0], [8.6, 0.5]],
         ear=[[0, -0.3], [1.7, 0], [5.4, 0.6], [7.2, -0.3], [8.0, 0.2], [8.6, -0.3]], blush=[[0, 0.35], [5.4, 0.9], [7.2, 0.35]],
         headtilt=[[0, 0], [2.5, 0.25], [3.6, -0.15], [5.0, 0]], tail=[[0, 1.5], [5.4, 0.3], [7.2, 3.0], [8.0, 1.0]])
e.fx('hand', 'ownerhand', rot=3.14159, pose='palm',
     x=[[0, 770], [4.8, 770], [4.9, 430, 'step'], [5.6, 410], [6.0, 450], [6.4, 410], [6.8, 450], [7.2, 430], [7.3, 470], [7.4, 400], [7.5, 470], [7.6, 430]],
     y=[[0, -900], [2.1, -900], [2.4, 1060, 'out'], [3.2, 1060], [3.5, -900, 'in'], [4.8, -900], [5.2, 640, 'out'], [7.6, 640], [8.0, -900, 'in']])
e.fx('food', 'sparkle', x=770, y=1280, r=160, show=shown((2.4, 3.2)))
e.fx('bite', 'stars', x=430, y=760, scale=0.7, show=shown((7.2, 8.2)))
e.fx('love', 'hearts', x=430, y=760, show=shown((5.4, 7.1)))
e.fx('badge', 'tag', screen=True, x=540, y=230, text='CAT TRANSLATOR: ON', color='#E2463F', size=50, w=640)
e.card('clock', '4:02 AM', 0, None, size=60, y=320, fill='#9BE7FF')
cap = [(0.0, 1.7, 'MEOOOOOW!!', 'I HAVE NOT EATEN\nIN 400 YEARS'), (2.5, 3.6, '*sniff*', 'NOT THAT FOOD.'),
       (3.6, 5.2, 'mrrp.', 'THE OTHER FOOD.\nTHE SAME ONE. BUT COLDER.'), (5.4, 7.1, 'purrrrrrr', 'YOU MAY CONTINUE.\nFOR 3 SECONDS.'),
       (7.2, 8.5, '*CHOMP*', 'THAT WAS 4.'), (8.6, None, 'MEOOOOOW!!', 'I HAVE NOT EATEN\nIN 400 YEARS')]
for i, (a, b, top, msg) in enumerate(cap):
    al = [[0, 0], [a, 1, 'step']] if a > 0 else [[0, 1]]
    if b: al.append([b, 0, 'step'])
    e.fx(f'cap{i}', 'caption', screen=True, x=540, y=1540, top=top, text=msg, size=62 if len(msg) < 26 else 54, alpha=al)
e.music('night', 501, [[0, 0.5], [1.7, 0.5], [1.75, 0.9, 'step'], [7.15, 0.9], [7.2, 0.3, 'step'], [8.6, 0.3]])
for t, n, g, o in [(0.02, 'yowl', 0.9, {}), (0.9, 'meow', 0.7, {'rate': 0.9}), (2.4, 'crunch', 0.7, {}), (2.55, 'sniff', 0.8, {}),
                   (3.6, 'meow', 0.5, {'rate': 1.3}), (5.2, 'pop', 0.3, {}), (5.4, 'purr', 0.9, {'loop': True, 'dur': 1.7}),
                   (7.2, 'crunch', 0.8, {}), (7.22, 'thud', 0.8, {}), (7.3, 'scared', 0.5, {'start': 0.3, 'dur': 1.0}), (8.6, 'yowl', 0.9, {})]:
    e.sfx(t, n, g, **o)
print(e.save())
