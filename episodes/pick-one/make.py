import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('pick-one', 14, 'guess_choice', scene='living',
       situation="NEW FORMAT guess-the-pick: three toys numbered 1-2-3 ($25 toy mouse, yarn ball, bottle cap), viewers vote in the comments, 3-2-1 countdown",
       twist="Nugget rejects every option; when the viewer's finger points at the yarn he attacks the finger: 'HE PICKED... YOUR FINGER' / 'NOBODY SAID 4'",
       title="Which toy will Nugget pick? Comment 1, 2 or 3 🤔",
       description="Lock in your answer before the countdown ends. 👇 1, 2 or 3?\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #quiz #guess #funny #animation")
e.scene_tracks(wall=[[0, '#D6ECFF']])
e.cam(zoom=[[0, 1.0], [10.2, 1.0], [10.45, 1.15, 'out'], [14, 1.1]], fx=[[0, 540]], fy=[[0, 1350]],
      shake=[[0, 0], [10.4, 0], [10.42, 14, 'step'], [10.9, 0]])
X = [210, 540, 870]
e.nugget('nug', x=[[0, 540], [6.6, 540], [7.1, 330, 'inout'], [8.0, 330], [8.5, 760, 'inout'], [10.2, 760], [10.45, 600, 'out']],
         y=[[0, 1330], [10.2, 1330], [10.32, 1180, 'out'], [10.45, 1360, 'in']], scale=0.62,
         flip=[[0, 1], [6.6, -1, 'step'], [8.0, 1, 'step'], [10.2, -1, 'step']],
         pose=[[0, 'sit'], [6.6, 'run'], [7.05, 'sit'], [8.0, 'run'], [8.45, 'sit']],
         look=[[0, [0, 0.8]], [4.0, [-0.9, 0.8], 'step'], [4.9, [0, 0.9], 'step'], [5.8, [0.9, 0.8], 'step'], [6.6, [0.9, 0.9]],
               [9.3, [0.9, 0.9]], [9.6, [-0.7, 0.6]]],
         eye=[[0, 'normal'], [7.1, 'normal'], [10.2, 'wide'], [10.5, 'happy']], lid=[[0, 0], [7.1, 0.5], [9.6, 0], [10.2, 0]],
         mouth=[[0, 'smile'], [7.1, 'line'], [10.2, 'open'], [10.5, 'chew']], mk=[[0, 0.2], [10.2, 0.8]],
         tail=[[0, 1.0], [9.6, 3.0]], ear=[[0, 0], [9.6, 0.6], [10.5, 0]],
         paw=[[0, None], [10.4, None], [10.45, [-150, -150]]], paw2=[[0, None], [10.4, None], [10.45, [-60, -230]]])
for i, (typ, extra) in enumerate([('toymouse', {}), ('yarn', {}), ('bottlecap', {})]):
    e.prop(f'item{i}', typ, x=X[i] + (30 if i == 0 else 0), y=1630, scale=[[0, 0], [0.3 + 0.2 * i, 0, 'step'], [0.55 + 0.2 * i, 1.5, 'back']], **extra)
    e.fx(f'badge{i}', 'badge', x=X[i] + (-90 if i == 0 else 90 if i == 2 else 0), y=1420 if i != 1 else 1440, label=str(i + 1), color=['#E2463F', '#5A79C2', '#4FAE62'][i],
         scale=[[0, 0], [0.3 + 0.2 * i, 0, 'step'], [0.55 + 0.2 * i, 1.0, 'back']],
         alpha=[[0, 1], [7.1, 1] if i != 0 else [7.1, 0.3, 'step'], [8.45, 1] if i != 2 else [8.45, 0.3, 'step']])
e.fx('sniff1', 'mark', x=260, y=980, char='?', color='#FFFFFF', scale=[[0, 0], [7.1, 0, 'step'], [7.25, 0.8, 'back'], [8.0, 0, 'step']])
e.fx('sniff3', 'mark', x=820, y=980, char='?', color='#FFFFFF', scale=[[0, 0], [8.5, 0, 'step'], [8.65, 0.8, 'back'], [9.3, 0, 'step']])
e.fx('finger', 'hand', x=[[0, 560], [10.45, 560], [10.55, 590], [10.65, 530], [10.75, 590], [10.85, 560]],
     y=[[0, 2700], [9.2, 2700], [9.55, 1700, 'out'], [10.25, 1700], [10.45, 1450, 'out']], pose='finger', rot=-0.12)
e.fx('pow', 'burst', x=580, y=1300, r=200, show=shown((10.45, 11.0)))
e.card('t1', 'WHICH ONE WILL\nNUGGET PICK?', 0, 4.0, size=96, pulse=1)
e.card('t1b', 'COMMENT 1, 2 OR 3!', 1.6, 4.0, size=78, fill='#FFE14D', y=430)
for i, t0 in enumerate([4.0, 4.9, 5.8]):
    e.card(f'c{i}', str(3 - i), t0, t0 + 0.9, size=220, fill=['#4FAE62', '#FFB347', '#E2463F'][i])
e.card('t2', '1? NOPE.', 7.1, 8.0, size=120, fill='#FF8F6B')
e.card('t3', '3? NOPE.', 8.5, 9.3, size=120, fill='#FF8F6B')
e.card('t4', 'PICK ONE,\nBUDDY', 9.4, 10.4, size=108)
e.card('t5', 'HE PICKED...\nYOUR FINGER', 10.45, 12.5, size=110, fill='#FFE14D')
e.card('t6', 'NOBODY SAID 4.', 12.5, None, size=104, fill='#9BE7FF')
e.music('playful', 101, [[0, 1], [3.95, 1], [4.0, 0.15, 'step'], [6.6, 0.15], [6.65, 1, 'step'], [10.4, 1], [10.45, 0, 'step'], [11.0, 0], [11.05, 1, 'step']])
for i, t0 in enumerate([0.3, 0.5, 0.7]):
    e.sfx(t0, 'pop', 0.5, rate=1.0 + 0.2 * i)
for t0 in (4.0, 4.9, 5.8):
    e.sfx(t0, 'tick', 0.9); e.sfx(t0, 'heartbeat', 0.5)
for t, n, g, o in [(6.6, 'ding', 0.6, {}), (6.65, 'run', 0.5, {'loop': True, 'dur': 0.45}), (7.1, 'sniff', 0.8, {}),
                   (7.5, 'slide_down', 0.4, {}), (8.0, 'run', 0.5, {'loop': True, 'dur': 0.45}), (8.5, 'sniff', 0.8, {}),
                   (8.9, 'slide_down', 0.4, {}), (9.3, 'swoosh', 0.4, {}), (10.2, 'yowl', 0.7, {}), (10.45, 'thud', 0.9, {}),
                   (10.5, 'scratch', 0.7, {}), (10.9, 'crunch', 0.5, {}), (11.3, 'crunch', 0.5, {}), (12.5, 'pop', 0.4, {})]:
    e.sfx(t, n, g, **o)
print(e.save())
