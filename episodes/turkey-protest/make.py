import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('turkey-protest', 11.5, 'skit_seasonal', scene='backyard',
       situation="3 days before Thanksgiving Gravy the turkey marches through the backyard with a protest sign: 'EAT PIZZA NOT ME', then 'TOFU IS DELICIOUS'",
       twist="his only supporter marching behind him is the orange cat, whose sign reads 'I'M JUST HERE FOR LEFTOVERS'; Gravy faints",
       title="The turkey started a protest 🦃🪧",
       description="3 days to go and he is not giving up. Team Gravy or team leftovers? 👇\n\nTiny Chaos: life's little chaos, animated. New video every day.\n\n#shorts #thanksgiving #turkey #funny #relatable #animation")
GY = 1450
# camera follows the march to the right, then pulls back to reveal the cat
e.cam(zoom=[[0, 1.35], [5.4, 1.35], [5.9, 1.0, 'out'], [8.4, 1.0], [8.5, 1.08, 'step']],
      fx=[[0, 540]], fy=[[0, 1050], [5.4, 1050], [5.9, 1000, 'out']],
      px=[[0, -120], [5.4, 160, 'linear'], [5.9, 120, 'out'], [8.4, 120], [8.5, 200, 'step']],
      shake=[[0, 0], [8.95, 0], [9.0, 18, 'step'], [9.4, 0]])
gx = [[0, 380], [5.4, 680, 'linear'], [8.4, 840, 'linear']]
e.prop('gravy', 'turkey', x=gx, y=GY, scale=0.95, walk=[[0, True], [8.4, False, 'step']], bob=1,
       rot=[[0, 0], [8.9, 0], [9.2, 1.4, 'in']], flip=1,
       eye=[[0, 'wide'], [3.0, 'normal'], [5.9, 'side'], [8.5, 'wide'], [9.0, 'closed']], look=[[0, [0.6, 0]], [5.9, [-1, 0]]],
       mouth=[[0, 'scream'], [1.4, 'open'], [2.6, 'scream'], [4.0, 'smile'], [5.9, 'closed'], [8.5, 'scream']],
       flap=[[0, 0.9], [0.3, 0.2], [0.6, 0.9], [0.9, 0.2], [1.2, 0.9], [1.5, 0.3], [5.9, 0.0], [8.5, 1.0]],
       sweat=[[0, False], [5.9, True, 'step']])
signx = [[0, 520], [5.4, 820, 'linear'], [8.4, 980, 'linear']]
e.prop('sign1', 'picket', x=signx, y=GY - 120, scale=0.95, label='EAT PIZZA\nNOT ME', size=74,
       rot=[[0, 0.05], [8.9, 0.05], [9.2, 1.25, 'in']], show=[[0, True], [3.0, False, 'step']])
e.prop('sign2', 'picket', x=signx, y=GY - 120, scale=0.95, label='TOFU IS\nDELICIOUS', size=74, color='#E8FFE0', ink='#2E7D32',
       rot=[[0, 0.05], [8.9, 0.05], [9.2, 1.25, 'in']], show=[[0, False], [3.0, True, 'step']])
nx = [[0, -400], [5.4, -100, 'linear'], [8.4, 380, 'linear']]
e.nugget('nug', x=nx, y=1330 - 170 * 0.75 + 95 + 120, scale=0.75, flip=1, pose=[[0, 'run'], [8.4, 'sit']], run_speed=0.6,
         eye=[[0, 'happy'], [9.2, 'heart']], mouth=[[0, 'smile'], [9.2, 'pant']], tongue=[[0, 0], [9.2, 1]], tail=2.0, blush=0.6)
e.prop('sign3', 'picket', x=[[0, -260], [5.4, 40, 'linear'], [8.4, 520, 'linear']], y=1430, scale=0.95,
       label="I'M JUST HERE\nFOR LEFTOVERS", size=58, color='#FFF0C2', ink='#E8552B')
e.fx('leaves', 'leaves', screen=True, n=12, seed=4, wind=0.4)
e.card('t1', '3 DAYS BEFORE\nTHANKSGIVING', 0, 3.0, size=94, fill='#FFE14D')
e.card('t2', 'PLAN B', 3.0, 5.4, size=140, fill='#7CF0A0', tilt=-0.06)
e.card('t3', 'HIS ONLY\nSUPPORTER:', 5.9, 8.4, size=110)
e.card('t4', 'WAIT. READ\nTHE SIGN.', 8.4, 9.2, size=104, fill='#FF6B6B')
e.card('t5', 'TEAM GRAVY\nOR TEAM LEFTOVERS?', 9.2, None, size=84)
e.music('hoedown', 777, [[0, 1], [8.35, 1], [8.4, 0.2, 'step'], [9.3, 0.8]])
for t, n, g, o in [(0.0, 'gobble', 1.0, {}), (1.4, 'gobble', 0.7, {}), (2.6, 'gobble', 0.9, {}), (3.0, 'pop', 0.8, {}),
                   (4.0, 'ding', 0.6, {}), (5.4, 'swoosh', 0.7, {}), (5.9, 'meow', 0.8, {'rate': 1.2}),
                   (8.4, 'tick', 0.8, {}), (8.5, 'scared', 0.8, {'start': 0.3, 'dur': 1.2}), (9.0, 'thud', 1.0, {}),
                   (9.2, 'meow', 0.7, {'rate': 1.35}), (9.6, 'purr_long', 0.5, {'dur': 1.6})]:
    e.sfx(t, n, g, **o)
print(e.save())
