import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('tuna-teleport', 10, 'relatable_owner', scene='living',
       situation="owner pops a can (*CLICK*): Nugget, fast asleep on the sofa, teleports to the can in 0.1 s; a slow-mo replay shows his ridiculous sprint",
       twist="the can is BEANS: he teleports straight back to the sofa, asleep; second *CLICK* (tuna) and he is back (loop)",
       title="He was asleep 0.1 seconds ago 🐟⚡",
       description="Every cat owner has seen this happen. Does yours come for beans too? 👇\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #catlife #tuna #funny #animation")
e.scene_tracks(wall=[[0, '#FBE3C4']])
e.cam(zoom=[[0, 1.2], [0.3, 1.2], [0.4, 1.45, 'out'], [2.5, 1.45], [2.6, 1.3, 'step'], [5.6, 1.3], [5.7, 1.55, 'out'], [6.6, 1.55], [6.7, 1.2, 'step'], [8.4, 1.2], [8.6, 1.45, 'out']],
      fx=[[0, 540]], fy=[[0, 1200]],
      px=[[0, 0], [0.3, 0], [0.4, 120, 'out'], [2.5, 120], [2.6, -180, 'step'], [5.6, 160, 'inout'], [6.6, 160], [6.7, 0, 'step'], [8.4, 0], [8.6, 120, 'out']],
      shake=[[0, 10], [0.4, 0, 'out'], [8.4, 0], [8.45, 10, 'step'], [8.8, 0, 'out']])
SOFA = (200, 1100)
AT = (520, 1289)
nx = [[0, SOFA[0]], [0.15, AT[0], 'step'], [2.6, SOFA[0], 'step'], [5.6, AT[0], 'linear'], [6.7, SOFA[0], 'step'], [8.45, AT[0], 'step']]
ny = [[0, SOFA[1]], [0.15, AT[1], 'step'], [2.6, SOFA[1] + 40, 'step'], [3.0, AT[1], 'out'], [5.6, AT[1]], [6.7, SOFA[1], 'step'], [8.45, AT[1], 'step']]
e.nugget('nug', x=nx, y=ny, scale=0.8, flip=1,
         pose=[[0, 'loaf'], [0.15, 'sit'], [2.6, 'run'], [5.6, 'sit'], [6.7, 'loaf'], [8.45, 'sit']], run_speed=0.35,
         eye=[[0, 'closed'], [0.15, 'heart'], [2.6, 'heart'], [5.6, 'heart'], [5.9, 'big'], [6.2, 'squeeze'], [6.7, 'closed'], [8.45, 'heart']],
         mouth=[[0, 'line'], [0.15, 'open'], [2.6, 'open'], [5.9, 'o'], [6.2, 'frown'], [6.7, 'line'], [8.45, 'open']], mk=[[0, 0.6], [2.6, 1.0], [5.6, 0.6]],
         tongue=[[0, False], [2.6, True], [5.6, False]], look=[[0, [0, 0]], [0.15, [0.9, 0.6]], [6.7, [0, 0]], [8.45, [0.9, 0.6]]],
         ear=[[0, 0.2], [0.15, -0.3], [2.6, 1.0], [5.6, -0.3], [6.2, 0.8], [6.7, 0.2], [8.45, -0.3]], tail=[[0, 0.2], [0.15, 3.0], [6.7, 0.2], [8.45, 3.0]],
         blush=[[0, 0.35], [0.15, 0.8]], headtilt=[[0, 0], [5.9, 0.0], [6.0, 0.25]])
e.prop('can', 'tunacan', x=850, y=1430, scale=1.2, label=[[0, 'TUNA'], [5.75, 'BEANS', 'step'], [8.3, 'TUNA', 'step']],
       color=[[0, '#2F80ED'], [5.75, '#C0392B', 'step'], [8.3, '#2F80ED', 'step']],
       open=[[0, 0.0], [0.15, 0.6, 'out'], [8.3, 0.0, 'step'], [8.45, 0.6, 'out']])
e.fx('hand', 'ownerhand', rot=3.14159, pose='palm', x=880, y=[[0, 1010], [0.5, 1000], [0.9, -900, 'in'], [8.0, -900], [8.3, 1000, 'out'], [8.8, 1000], [9.2, -900, 'in']])
e.fx('zzz', 'zzz', x=220, y=900, show=shown((0, 0.15), (6.9, 8.45)))
e.fx('poof1', 'dust', x=SOFA[0], y=1130, show=shown((0.15, 0.7), (6.7, 7.2)))
e.fx('poof2', 'dust', x=AT[0], y=1330, show=shown((0.15, 0.7), (6.7, 7.2), (8.45, 9.0)))
e.fx('zip', 'speed', x=380, y=1150, angle=0.0, length=500, show=shown((0.15, 0.6), (2.9, 5.6), (8.45, 8.9)))
e.fx('love', 'hearts', x=620, y=900, show=shown((0.4, 2.5), (8.6, 10.1)))
e.fx('flash', 'flash', screen=True, alpha=[[0, 0.3], [0.3, 0, 'out'], [8.4, 0.3, 'step'], [8.7, 0, 'out']])
e.card('t1', '*CLICK*', 0, 1.1, size=150, fill='#FFFFFF', tilt=-0.06, pulse=1)
e.card('t2', 'HE WAS ASLEEP\n0.1 SECONDS AGO', 1.1, 2.6, size=96, fill='#FFE14D')
e.card('t3', 'SLOW-MO REPLAY', 2.6, 5.6, size=96, fill='#9BE7FF')
e.card('t4', "...IT'S BEANS.", 5.7, 6.7, size=120, fill='#FF8F6B')
e.card('t5', '*ASLEEP AGAIN*', 6.7, 8.4, size=100, fill='#FFFFFF')
e.card('t6', '*CLICK*', 8.4, None, size=150, fill='#FFFFFF', tilt=-0.06, pulse=1)
e.fx('rec', 'tag', screen=True, x=870, y=420, text='0.25x', color='#E2463F', size=48, w=180, show=shown((2.6, 5.6)))
e.music('playful', 801, [[0, 1], [2.55, 1], [2.6, 0.3, 'step'], [5.6, 0.3], [5.65, 1, 'step'], [6.65, 1], [6.7, 0.4, 'step'], [8.4, 0.4], [8.45, 1, 'step']])
for t, n, g, o in [(0.0, 'pop', 1.0, {}), (0.02, 'tick', 1.0, {}), (0.15, 'whoosh', 0.9, {}), (0.4, 'meow', 0.9, {'rate': 1.2}),
                   (2.6, 'slide_down', 0.6, {}), (2.7, 'run', 0.5, {'loop': True, 'dur': 2.8, 'rate': 0.6}), (5.75, 'ding', 0.6, {}),
                   (6.2, 'wobble', 0.6, {}), (6.7, 'whoosh', 0.8, {}), (6.9, 'purr_long', 0.5, {'dur': 1.4}), (8.4, 'pop', 1.0, {}),
                   (8.42, 'tick', 1.0, {}), (8.45, 'whoosh', 0.9, {}), (8.7, 'meow', 0.9, {'rate': 1.2})]:
    e.sfx(t, n, g, **o)
print(e.save())
