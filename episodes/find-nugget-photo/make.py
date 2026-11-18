import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('find-nugget-photo', 10.5, 'puzzle_find_photo', scene='photo',
       situation="PHOTO-BACKGROUND test 2: real cozy living-room photo (Pixabay); a tiny cartoon cat loaf is hidden on the windowsill next to the plant; 7-second countdown",
       twist="reveal zooms in: the cat was staring at the viewer the whole time; card 'MOST PEOPLE CHECK THE CANDLES FIRST'",
       title="Find the cat in this room in 7 seconds 👀🐈",
       description="He was there the whole time. How fast did you find him? Be honest 👇\n\nTiny Chaos: life's little chaos, animated. New video every day.\n\n#shorts #puzzle #findthecat #hiddencat #brainteaser #eyetest",
       experiment=True, pixabay='episodes/find-nugget-photo/bg.jpg.json')
e.scene_tracks(photo=[[0, 'episodes/find-nugget-photo/bg.jpg']], dim=[[0, 0.12]], tint=[[0, '#1A0E08']], kb=[[0, 0.006]], floor_dark=[[0, 0.0]])
CX, CY = 960, 968
R = 7.3
e.cam(zoom=[[0, 1.0], [R, 1.0], [R + 0.6, 3.0, 'out'], [10.0, 3.1], [10.4, 1.0, 'in']],
      fx=[[0, 540], [R, 540], [R + 0.6, CX, 'out'], [10.0, CX], [10.4, 540, 'in']],
      fy=[[0, 960], [R, 960], [R + 0.6, CY - 20, 'out'], [10.0, CY - 20], [10.4, 960, 'in']])
e.nugget('nug', x=CX, y=CY, scale=0.13, flip=-1, pose='loaf',
         eye=[[0, 'normal'], [R + 0.7, 'wide', 'step'], [9.0, 'happy', 'step']], look=[[0, [0, 0]]],
         lid=[[0, 0.5], [R + 0.7, 0, 'step']], mouth=[[0, 'line'], [9.0, 'smile', 'step']], tail=[[0, 0.4]], blink=[[0, 0.0]])
e.fx('ring', 'target', x=CX, y=CY - 30, r=70, show=shown((R + 0.5, 10.0)))
e.card('title', 'FIND THE CAT\nIN 7 SECONDS', 0, R, size=96, y=230, fill='#FFFFFF')
for k in range(7):
    e.card(f'n{k}', str(7 - k), 0.3 + k if k else 0, 0.3 + k + 1, size=190, y=470, fill='#FF2E63')
e.card('found', 'THERE HE IS!', R + 0.4, 10.1, size=110, y=330, fill='#3DDC84')
e.card('tip', 'MOST PEOPLE CHECK\nTHE CANDLES FIRST', R + 1.2, 10.1, size=64, y=1600, fill='#FFD23F')
e.music('tense', 841, [[0, 0.8], [R, 0.8], [R + 0.05, 0.3, 'step']])
for k in range(7):
    e.sfx(0.3 + k, 'tick', 0.9)
e.sfx(R, 'ding', 1.0); e.sfx(R + 0.1, 'sparkle', 0.7); e.sfx(R + 0.75, 'meow', 0.7)
print(e.save())
