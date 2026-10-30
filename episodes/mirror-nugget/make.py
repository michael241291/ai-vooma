import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('mirror-nugget', 13, 'reaction', scene='bathroom',
       situation="Nugget meets a mirror for the first time: raises a paw, tilts his head, hisses, and the reflection copies everything",
       twist="the reflection stops copying, puts on sunglasses and smiles; Nugget bolts; the reflection waves: 'SEE YOU TONIGHT, NUGGET'",
       title="Nugget's reflection did NOT copy him 😳🪞",
       description="He's never trusting a mirror again. 🪞\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #mirror #funny #animation #orangecat")
e.cam(zoom=[[0, 1.06], [6.9, 1.06], [7.1, 1.2, 'out'], [7.8, 1.2], [8.0, 1.06]], fx=[[0, 560], [6.9, 560], [7.1, 380]], fy=[[0, 1100]],
      shake=[[0, 0], [7.8, 0], [7.82, 12, 'step'], [8.3, 0]])
e.prop('glass', 'mirror', x=360, y=1440, part='glass')
common = dict(paw=[[0, None], [1.55, None], [1.6, [120, -20]], [1.9, [170, -150], 'out'], [2.9, [170, -150]], [3.0, None, 'step']],
              headtilt=[[0, 0], [2.9, 0], [3.3, 0.28], [4.0, 0.0]],
              puff=[[0, 0], [4.15, 0], [4.25, 1, 'out'], [5.8, 1], [6.2, 0]], ear=[[0, 0], [4.2, 0.9], [6.2, 0]],
              mouth=[[0, 'o'], [1.6, 'smile'], [4.2, 'scream'], [6.0, 'line']], mk=[[0, 0.4], [4.2, 0.9], [6.0, 0.3]])
refl = dict(common)
refl.update(paw=[[0, None], [1.55, None], [1.6, [120, -20]], [1.9, [170, -150], 'out'], [2.9, [170, -150]], [3.0, None, 'step'],
                 [8.9, None], [9.0, [170, -200]], [9.3, [230, -170]], [9.6, [170, -200]], [9.9, [230, -170]], [10.2, [170, -200]],
                 [10.5, [230, -170]], [10.8, [170, -200]], [11.1, [230, -170]], [11.4, [170, -200]], [11.7, [230, -170]], [12.0, [170, -200]],
                 [12.3, [230, -170]], [12.6, [170, -200]]],
            mouth=[[0, 'o'], [1.6, 'smile'], [4.2, 'scream'], [6.0, 'line'], [6.7, 'smile']],
            sunglasses=[[0, False], [6.7, True, 'step']], eye=[[0, 'normal'], [6.7, 'happy']], look=[[0, [0.9, 0.2]]])
e.nugget('mirror_cat', x=360, y=1220, scale=0.62, flip=1, **refl)
e.add  # reflection drawn inside the oval glass
e.d['actors'][-1]['clip'] = [360, 940, 238, 388]
e.prop('frame', 'mirror', x=360, y=1440, part='frame')
real = dict(common)
real.update(eye=[[0, 'normal'], [7.0, 'big'], [7.8, 'wide'], [11.2, 'normal']], look=[[0, [0.9, 0.2]], [11.2, [0.9, 0.3]]],
            lid=[[0, 0], [11.2, 0.5]], mouth=[[0, 'o'], [1.6, 'smile'], [4.2, 'scream'], [6.0, 'line'], [7.0, 'o'], [7.8, 'scream'], [11.2, 'line']],
            puff=[[0, 0], [4.15, 0], [4.25, 1, 'out'], [5.8, 1], [6.2, 0], [7.8, 0], [7.9, 1.2, 'out']],
            ear=[[0, 0], [4.2, 0.9], [6.2, 0], [7.8, -0.3]])
e.nugget('nug', x=[[0, 790], [7.95, 790], [8.7, 1550, 'in'], [11.1, 1550], [11.2, 1080, 'step']],
         y=[[0, 1300], [7.8, 1300], [8.0, 1150, 'out'], [8.25, 1300, 'in']], scale=0.82,
         flip=[[0, -1], [7.9, 1, 'step'], [11.2, -1, 'step']], pose=[[0, 'sit'], [7.95, 'run'], [11.2, 'sit']], run_speed=1.8, **real)
e.fx('huh', 'mark', x=830, y=760, char='?', color='#FFFFFF', scale=[[0, 0.9], [1.5, 0.9], [1.55, 0, 'step'], [6.9, 0], [7.0, 1.0, 'back'], [7.8, 0, 'step']])
e.fx('zoom', 'speed', x=900, y=1150, angle=3.14159, show=shown((8.0, 8.7)))
e.fx('glint', 'sparkle', x=360, y=900, r=160, show=shown((6.7, 8.0)))
e.card('t1', 'NUGGET SEES A MIRROR\nFOR THE FIRST TIME', 0, 4.2, size=82)
e.card('t2', 'WHO IS THIS GUY?!', 4.2, 6.1, size=100, fill='#FF8F6B', pulse=1)
e.card('t3', '...WAIT.', 6.2, 7.0, size=120)
e.card('t4', "HE DIDN'T\nCOPY ME", 7.0, 7.8, size=112, fill='#FFE14D')
e.card('t5', 'NOPE.', 7.8, 9.0, size=150, fill='#FF8F6B')
e.card('t6', 'SEE YOU TONIGHT,\nNUGGET ;)', 9.0, None, size=96, fill='#9BE7FF')
e.music('cozy', 81, [[0, 1], [4.15, 1], [4.2, 0.2, 'step'], [6.1, 0.2], [6.15, 0, 'step']])
e.music('sneaky', 82, [[0, 0], [8.9, 0, 'step'], [9.0, 1]])
for t, n, g, o in [(0.1, 'pop', 0.4, {}), (1.6, 'boing', 0.4, {'dur': 0.6}), (3.3, 'wobble', 0.3, {'dur': 0.7}), (4.2, 'yowl', 0.9, {}),
                   (4.25, 'scratch', 0.5, {}), (6.2, 'tick', 0.5, {}), (6.7, 'sparkle', 0.7, {}), (7.0, 'ding', 0.4, {}),
                   (7.8, 'scared', 0.9, {'start': 0.3, 'dur': 1.2, 'fade': 0.3}), (7.95, 'run', 0.7, {'loop': True, 'dur': 0.8}),
                   (8.6, 'crash', 0.4, {'dur': 1.0}), (9.0, 'pop', 0.4, {}), (11.2, 'slide_up', 0.4, {}), (11.5, 'meow', 0.6, {'rate': 0.9})]:
    e.sfx(t, n, g, **o)
print(e.save())
