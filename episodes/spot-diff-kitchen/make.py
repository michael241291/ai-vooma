import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('spot-diff-kitchen', 12.5, 'puzzle_spot', scene='kitchen',
       situation="spot-the-difference: two stacked kitchen panels with Nugget, 8-second countdown, find 3 differences (mug colour, calendar day, tongue)",
       twist="after the 3 red circles: 'THERE ARE 4' - the bottom Nugget's tail was wagging the whole time",
       title="Only 2% find all 3 differences 👀🐱",
       description="8 seconds. 3 differences. How many did you get? Be honest 👇\n\nNugget the orange cat. New video every day.\n\n#shorts #spotthedifference #puzzle #cat #animation #brainteaser",
       experiment=True)
S = 1000 / 1080
e.panels(dict(rect=[40, 330, 1000, 610], ox=0, oy=650, s=S), dict(rect=[40, 1030, 1000, 610], ox=0, oy=650, s=S))
e.prop('cal0', 'calendar', panel=0, x=560, y=745, scale=0.5, month='NOV', day=26, color='#E8552B')
e.prop('cal1', 'calendar', panel=1, x=560, y=745, scale=0.5, month='NOV', day=25, color='#E8552B')
e.prop('mug0', 'mug', panel=0, x=900, y=800, scale=0.9, color='#FF8FA3', label='#1')
e.prop('mug1', 'mug', panel=1, x=900, y=800, scale=0.9, color='#6CCB7E', label='#1')
look = [[0, [0, 0]], [2.5, [0.8, -0.2]], [3.6, [0, 0]], [5.0, [0, 0.3]], [8.0, [0, 0]]]
eye = [[0, 'normal'], [5.0, 'squeeze'], [6.6, 'normal'], [10.6, 'wide']]
e.nugget('n0', panel=0, x=330, y=1262, scale=0.9, look=look, eye=eye, mouth=[[0, 'smile'], [5.0, 'line'], [6.6, 'smile']], tail=0.2)
e.nugget('n1', panel=1, x=330, y=1262, scale=0.9, look=look, eye=eye, mouth=[[0, 'smile'], [5.0, 'line'], [6.6, 'smile']],
         tongue=True, tail=[[0, 2.6]])
for i, (x, y, r, t0) in enumerate([(900, 740, 95, 8.1), (560, 880, 110, 8.6), (330, 1078, 85, 9.1)]):
    e.fx(f'ring{i}', 'ring', panel=1, x=x, y=y, r=r, label=str(i + 1), draw=[[0, 0], [t0, 0], [t0 + 0.35, 1, 'out']])
e.fx('ring4', 'ring', panel=1, x=500, y=1200, r=115, sy=0.8, color='#FFCC00', label='4?!', draw=[[0, 0], [10.4, 0], [10.75, 1, 'out']])
e.fx('timer', 'timerbar', screen=True, x=585, y=985, w=780,
     left=[[0, 1], [8.0, 0, 'linear']], label=[[0, 8]] + [[k, 8 - k, 'step'] for k in range(1, 8)] + [[8.0, 0, 'step']],
     alpha=[[0, 1], [8.0, 1], [8.05, 0, 'step']])
e.card('t1', 'FIND 3 DIFFERENCES', 0, 8.0, size=92, y=230, pulse=1, fill='#FFE14D')
e.card('t1b', 'IN 8 SECONDS', 0.0, 8.0, size=58, y=300 - 5, fill='#FFFFFF')
e.card('t2', 'TIME!', 8.0, 10.3, size=120, y=240, fill='#FF8F6B')
e.card('t3', 'WAIT... THERE ARE 4', 10.3, None, size=88, y=240, fill='#FFCC00', pulse=1)
e.card('t4', 'HOW MANY DID YOU GET?', 10.9, None, size=62, y=985, fill='#FFFFFF')
e.music('sneaky', 301, [[0, 0.8], [8.0, 0.8], [8.05, 0.35, 'step'], [10.3, 0.35], [10.35, 0.9, 'step']])
for k in range(8):
    e.sfx(k + 0.02, 'tick', 0.7)
for t, n, g in [(0.05, 'pop', 0.5), (8.0, 'ding', 0.8), (8.1, 'swoosh', 0.5), (8.45, 'pop', 0.6), (8.6, 'swoosh', 0.5), (8.95, 'pop', 0.6),
                (9.1, 'swoosh', 0.5), (9.45, 'pop', 0.6), (10.3, 'slide_up', 0.6), (10.4, 'boing', 0.7), (10.75, 'meow', 0.8)]:
    e.sfx(t, n, g)
print(e.save())
