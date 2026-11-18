import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('translator-3am-kitchen', 11.0, 'skit_translator_photo', scene='photo',
       situation="CAT TRANSLATOR part 3, first PHOTO-BACKGROUND test: real kitchen photo (Pixabay) at 3AM; cartoon cat on the counter demands breakfast",
       twist="owner points at the clock: 'TIME IS A HUMAN CONCEPT'; mug pushed off ('OOPS.'), fed, eats while saying 'WORST DAY OF MY LIFE', loafs: 'WAKE ME AT 4' and loops",
       title="Cat translator: 3AM edition 😾🕒",
       description="Same time. Every. Night. What time does yours start? 👇\n\nTiny Chaos: life's little chaos, animated. New video every day.\n\n#shorts #cat #cattranslator #3am #catlife #funny",
       experiment=True, pixabay='episodes/translator-3am-kitchen/bg.jpg.json')
e.scene_tracks(photo=[[0, 'episodes/translator-3am-kitchen/bg.jpg']], dim=[[0, 0.42]], tint=[[0, '#0E1638']], kb=[[0, 0.01]], floor_y=[[0, 1200]], floor_dark=[[0, 0.0]])
Y = 1215
e.cam(zoom=[[0, 1.25], [2.1, 1.25], [2.3, 1.1, 'out'], [4.3, 1.1], [4.4, 1.35, 'step'], [6.5, 1.35], [6.6, 1.15, 'step'], [8.7, 1.15], [8.8, 1.3, 'step'], [10.2, 1.3], [10.25, 1.25, 'step']],
      fx=[[0, 500], [4.4, 640, 'step'], [6.6, 480, 'step'], [8.8, 500, 'step']],
      fy=[[0, 1000], [2.1, 1000], [2.3, 960, 'out'], [4.4, 1080, 'step'], [6.6, 1000, 'step'], [8.8, 1040, 'step']],
      shake=[[0, 9], [1.8, 9], [1.9, 0, 'step'], [4.6, 14, 'step'], [5.1, 0, 'step'], [10.2, 9, 'step']])
# glow of the open fridge / night light behind the cat
e.prop('clock', 'clock', x=770, y=620, scale=0.7, time='3:02', show=[[0, True]])
e.prop('mug', 'mug', label='#1 MOM', color='#FF8FA3', x=[[0, 780], [4.4, 780], [4.75, 900, 'in'], [5.3, 980, 'in']],
       y=[[0, Y], [4.4, Y], [4.75, Y - 60, 'out'], [5.3, 1750, 'in']], rot=[[0, 0], [4.4, 0], [5.3, 2.6, 'in']], scale=0.9,
       show=[[0, True], [5.35, False, 'step'], [10.25, True, 'step']])
e.fx('crash', 'burst', x=980, y=1720, r=260, show=shown((5.3, 5.8)))
e.prop('bowl', 'bowl', x=[[0, 250], [6.6, 250]], y=Y, fill=[[0, 0.0], [6.6, 0.9, 'step'], [8.7, 0.35]], scale=0.8, show=shown((6.6, 8.8)))
nug = e.nugget('nug', x=[[0, 480], [4.4, 480], [4.6, 600, 'out'], [6.6, 470, 'step']], y=Y, scale=0.72, flip=1,
               pose=[[0, 'sit'], [8.8, 'loaf', 'step'], [10.25, 'sit', 'step']],
               eye=[[0, 'squeeze'], [2.1, 'normal'], [4.4, 'wide'], [6.6, 'happy'], [8.8, 'closed'], [10.25, 'squeeze']],
               look=[[0, [0.5, -0.2]], [2.1, [0.9, -0.6]], [4.4, [0.9, 0.2]], [6.6, [-0.6, 0.6]], [8.8, [0, 0]]],
               lid=[[0, 0], [2.1, 0.55, 'step'], [4.4, 0, 'step']],
               mouth=[[0, 'scream'], [2.1, 'line'], [4.4, 'o'], [6.6, 'chew'], [8.8, 'smile'], [10.25, 'scream']],
               mk=[[0, 1.0], [2.0, 1.0], [2.1, 0.3, 'step'], [10.25, 1.0, 'step']], puff=[[0, 0.6], [2.1, 0.2], [4.4, 0.0]],
               ear=[[0, 1.0], [2.1, 0.5], [6.6, 0.2]], tail=[[0, 3.0], [2.1, 1.0], [4.4, 2.0], [8.8, 0.3]],
               paw=[[0, [0, 0]], [4.3, [0, 0]], [4.45, [150, -60], 'out'], [4.8, [0, 0]]])
e.fx('hand', 'ownerhand', rot=3.14159, pose='point',
     x=[[0, 770]], y=[[0, -900], [2.0, -900], [2.3, 400, 'out'], [4.1, 400], [4.4, -900, 'in']])
e.fx('zz', 'zzz', x=600, y=980, show=shown((9.0, 10.2)))
e.fx('badge', 'tag', screen=True, x=540, y=200, text='CAT TRANSLATOR: ON', color='#E2463F', size=50, w=640)
cap = [(0.0, 2.1, 'MEOOOOOW!!', 'IT IS 3AM.\nI DEMAND BREAKFAST.'), (2.1, 4.4, '*slow blink*', 'TIME IS A\nHUMAN CONCEPT.'),
       (4.4, 6.6, '*tink*', 'OOPS.'), (6.6, 8.8, '*crunch crunch*', 'THIS IS THE WORST\nDAY OF MY LIFE.'),
       (8.8, 10.25, 'purrrr', 'WAKE ME UP AT 4.'), (10.25, None, 'MEOOOOOW!!', 'IT IS 3AM.\nI DEMAND BREAKFAST.')]
for i, (a, b, top, msg) in enumerate(cap):
    al = [[0, 0], [a, 1, 'step']] if a > 0 else [[0, 1]]
    if b: al.append([b, 0, 'step'])
    e.fx(f'cap{i}', 'caption', screen=True, x=540, y=1540, top=top, text=msg, size=62 if len(msg) < 26 else 54, alpha=al)
e.music('night', 731, [[0, 0.7]])
for t, n, g, o in [(0.02, 'yowl', 0.9, {}), (2.1, 'tick', 0.6, {}), (4.45, 'swoosh', 0.7, {}), (5.3, 'crash', 1.0, {}),
                   (6.6, 'rustle', 0.8, {'dur': 0.5}), (6.9, 'crunch', 0.8, {}), (7.6, 'crunch', 0.7, {}),
                   (8.8, 'purr', 0.9, {'loop': True, 'dur': 1.4}), (10.25, 'yowl', 0.9, {})]:
    e.sfx(t, n, g, **o)
print(e.save())
