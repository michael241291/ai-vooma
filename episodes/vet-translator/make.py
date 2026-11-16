import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('vet-translator', 11.4, 'skit_translator', scene='living_b',
       situation="CAT TRANSLATOR part 2: the owner brings out the pet carrier with a VET sticker; the cat hisses 'I KNOW WHAT THAT BOX MEANS', gets bribed with a treat ('I FORGIVE YOU')",
       twist="cut: he is inside the rattling carrier, translator only outputs BETRAYAL in bigger and bigger letters; ends 'I WILL REMEMBER THIS UNTIL DINNER' and loops",
       title="Cat translator: vet day edition 😾🩺",
       description="He forgave me 4 minutes later. Does your cat hold grudges? 👇\n\nTiny Chaos: life's little chaos, animated. New video every day.\n\n#shorts #cat #cattranslator #vet #catlife #funny",
       experiment=False)
e.scene_tracks(wall=[[0, '#F2D9C9']])
# beats: 0 hiss | 1.9 treat | 3.5 forgive | 5.3 CUT carrier | 6.9 BETRAYAL bigger | 8.7 out, grudge | 10.2 hiss again (loop)
e.cam(zoom=[[0, 1.45], [1.8, 1.45], [2.1, 1.25, 'out'], [5.25, 1.3], [5.3, 1.5, 'step'], [6.85, 1.55], [6.9, 1.8, 'step'], [8.6, 1.85], [8.7, 1.4, 'step'], [10.15, 1.42], [10.2, 1.45, 'step']],
      fx=[[0, 500], [5.3, 700, 'step'], [8.7, 500, 'step']],
      fy=[[0, 1000], [1.8, 1000], [2.1, 1150, 'out'], [5.25, 1150], [5.3, 1130, 'step'], [8.6, 1130], [8.7, 1050, 'step']],
      shake=[[0, 10], [1.6, 10], [1.7, 0, 'step'], [5.3, 6, 'step'], [6.9, 16, 'step'], [8.6, 16], [8.7, 0, 'step'], [10.2, 10, 'step']])
e.prop('carrier', 'carrier', x=[[0, 720], [5.3, 640, 'step'], [8.7, 720, 'step']], y=1360, scale=[[0, 0.85], [5.3, 1.1, 'step'], [8.7, 0.85, 'step']],
       label='VET', rattle=[[0, 0], [5.3, 1.0, 'step'], [6.9, 2.2, 'step'], [8.7, 0, 'step']],
       door=[[0, 0]], eyes=[[0, False], [5.3, True, 'step'], [8.7, False, 'step']])
nshow = [[0, True], [5.3, False, 'step'], [8.7, True, 'step']]
e.nugget('nug', x=360, y=1264, scale=0.95, flip=1, show=nshow,
         eye=[[0, 'squeeze'], [1.9, 'big'], [3.5, 'happy'], [8.7, 'normal'], [10.2, 'squeeze']],
         look=[[0, [0.6, 0]], [1.9, [0.4, 0.7]], [3.5, [0, 0]], [8.7, [0.8, 0]]],
         lid=[[0, 0], [8.7, 0.45, 'step'], [10.2, 0, 'step']],
         mouth=[[0, 'scream'], [1.9, 'o'], [2.6, 'chew'], [3.5, 'smile'], [8.7, 'line'], [10.2, 'scream']],
         mk=[[0, 1.0], [1.9, 0.5], [10.2, 1.0, 'step']], puff=[[0, 0.8], [1.9, 0.0], [8.7, 0.5, 'step'], [10.2, 0.8]],
         ear=[[0, 1.0], [1.9, -0.2], [3.5, 0.3], [8.7, 0.8, 'step']], blush=[[0, 0.3], [3.5, 0.9], [5.3, 0.3]],
         headtilt=[[0, 0], [1.9, 0.25], [3.5, 0]], tail=[[0, 3.0], [1.9, 1.0], [3.5, 0.3], [8.7, 2.5]])
e.fx('hand', 'ownerhand', rot=3.14159, pose='palm',
     x=[[0, 740]], y=[[0, -900], [1.9, -900], [2.2, 930, 'out'], [3.1, 930], [3.4, -900, 'in']])
e.prop('treat', 'treat', x=[[0, 700], [2.6, 700], [2.9, 430, 'in']], y=[[0, 1190], [2.6, 1190], [2.9, 1000, 'in']], scale=1.4, show=shown((2.15, 2.95)))
e.fx('love', 'hearts', x=400, y=760, show=shown((3.5, 5.25)))
e.fx('bang', 'burst', x=640, y=1150, r=320, show=shown((6.9, 7.4)))
e.fx('badge', 'tag', screen=True, x=540, y=200, text='CAT TRANSLATOR: ON', color='#E2463F', size=50, w=640)
e.card('late', '20 MINUTES LATER', 8.7, 10.2, size=60, y=330, fill='#9BE7FF')
e.card('bt1', 'BETRAYAL', 5.5, 6.9, size=150, y=620, fill='#FF5A5F', tilt=-0.05)
e.card('bt2', 'BETRAYAL!!', 6.9, 8.7, size=210, y=640, fill='#FF2E2E', tilt=0.05, pulse=1)
cap = [(0.0, 1.9, '*HISSSSS*', 'I KNOW WHAT\nTHAT BOX MEANS.'), (1.9, 3.5, 'mrrp?', 'IS THAT... A TREAT?'),
       (3.5, 5.3, '*crunch* purrr', 'I FORGIVE YOU.\nYOU MAY LIVE.'), (5.3, 6.9, 'MEOOOOW', 'BETRAYAL.'),
       (6.9, 8.7, 'MEOOOOOOOOOW', 'BETRAYAL!!!!'), (8.7, 10.2, '*stare*', 'I WILL REMEMBER THIS.\nUNTIL DINNER.'),
       (10.2, None, '*HISSSSS*', 'I KNOW WHAT\nTHAT BOX MEANS.')]
for i, (a, b, top, msg) in enumerate(cap):
    al = [[0, 0], [a, 1, 'step']] if a > 0 else [[0, 1]]
    if b: al.append([b, 0, 'step'])
    e.fx(f'cap{i}', 'caption', screen=True, x=540, y=1540, top=top, text=msg, size=62 if len(msg) < 26 else 54, alpha=al)
e.music('sneaky', 612, [[0, 0.7], [5.25, 0.7], [5.3, 0.3, 'step'], [8.7, 0.6, 'step']])
e.music('tense', 613, [[0, 0], [5.3, 0.9, 'step'], [8.7, 0, 'step']])
for t, n, g, o in [(0.02, 'scared', 0.8, {'start': 0.3, 'dur': 1.2}), (1.9, 'rustle', 0.8, {'dur': 0.6}), (2.6, 'crunch', 0.8, {}),
                   (3.5, 'purr', 0.9, {'loop': True, 'dur': 1.7}), (5.3, 'whoosh', 0.8, {}), (5.35, 'yowl', 0.8, {}),
                   (6.9, 'yowl', 1.0, {'rate': 0.85}), (6.95, 'thud', 0.9, {}), (7.6, 'scratch', 0.6, {}),
                   (8.7, 'pop', 0.4, {}), (10.2, 'scared', 0.8, {'start': 0.3, 'dur': 1.1})]:
    e.sfx(t, n, g, **o)
print(e.save())
