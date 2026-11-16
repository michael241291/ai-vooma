import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('gravy-translator', 11.6, 'skit_translator', scene='kitchen',
       situation="TURKEY TRANSLATOR: Gravy screams 'THIS IS NOT A DRILL', sees the 26th circled on the kitchen calendar, packs a suitcase: 'MOVE TO CANADA. THEIR THANKSGIVING WAS IN OCTOBER. SAFE!'",
       twist="the cat strolls in with a giant fork: 'CAN I COME? I'LL BRING A FORK.' Gravy: 'PACK FASTER.' (loops to the scream)",
       title="I put a translator on the turkey 🦃🧳",
       description="He has a plan. It is not a good plan. Would you help Gravy escape? 👇\n\nTiny Chaos: life's little chaos, animated. New video every day.\n\n#shorts #thanksgiving #turkey #translator #funny #relatable",
       experiment=True)
e.scene_tracks(wall=[[0, '#CDE7D8']])
GY = 1480
e.cam(zoom=[[0, 1.5], [1.75, 1.5], [1.8, 1.7, 'step'], [3.45, 1.75], [3.5, 1.3, 'step'], [7.25, 1.32], [7.3, 1.0, 'step'], [9.25, 1.05], [9.3, 1.5, 'step']],
      fx=[[0, 440], [1.8, 760, 'step'], [3.5, 520, 'step'], [7.3, 540, 'step'], [9.3, 440, 'step']],
      fy=[[0, 1050], [1.8, 760, 'step'], [3.5, 1150, 'step'], [7.3, 1100, 'step'], [9.3, 1050, 'step']],
      shake=[[0, 10], [1.6, 10], [1.7, 0, 'step'], [9.3, 12, 'step']])
e.prop('cal', 'calendar', x=780, y=440, scale=1.0, month='NOVEMBER', day=26, circle=True, color='#E8552B')
e.prop('case', 'suitcase', x=[[0, 1400], [3.5, 760, 'step'], [9.3, 1400, 'step']], y=1470, scale=0.95,
       label='CANADA\nOR BUST', size=40, stuffed=[[0, 0], [3.5, 0.2], [4.6, 1.0, 'back']], color='#E8552B')
e.prop('gravy', 'turkey', x=[[0, 400], [3.5, 380, 'step'], [7.3, 330, 'step']], y=GY, scale=0.95, flip=1,
       eye=[[0, 'wide'], [1.8, 'side'], [3.5, 'normal'], [5.4, 'happy'], [7.3, 'normal'], [8.2, 'wide'], [9.3, 'wide']],
       look=[[0, [0, 0]], [1.8, [1, -0.6]], [3.5, [1, 0]], [5.4, [0, 0]], [7.3, [1, 0]]],
       mouth=[[0, 'scream'], [1.8, 'open'], [3.5, 'smile'], [7.3, 'closed'], [8.2, 'open'], [9.3, 'scream']],
       flap=[[0, 0.9], [0.25, 0.2], [0.5, 0.9], [0.75, 0.2], [1.0, 0.9], [1.25, 0.2], [1.5, 0.9], [1.8, 0.1], [3.5, 0.3], [4.0, 0.7], [4.5, 0.3],
             [7.3, 0.0], [9.3, 1.0], [9.55, 0.2], [9.8, 1.0], [10.05, 0.2], [10.3, 1.0], [10.55, 0.2], [10.8, 1.0], [11.05, 0.2], [11.3, 0.9]],
       sweat=[[0, True], [3.5, False, 'step'], [8.2, True, 'step']], blush=[[0, 0], [5.4, 0.8], [7.3, 0]])
e.fx('love', 'hearts', x=380, y=780, show=shown((5.4, 7.25)))
e.nugget('nug', x=[[0, 1300], [7.3, 1250, 'step'], [8.1, 800, 'out']], y=1330 - 170 * 0.8 + 95, scale=0.8, flip=-1,
         pose=[[0, 'run'], [8.1, 'sit', 'step']], run_speed=0.6, show=[[0, False], [7.3, True, 'step'], [9.3, False, 'step']],
         eye=[[0, 'happy'], [8.1, 'happy']], mouth=[[0, 'smile'], [8.1, 'pant']], tongue=[[0, 0], [8.1, 1]], tail=2.0, blush=0.6)
e.prop('fork', 'fork', x=[[0, 1300], [7.3, 1250, 'step'], [8.1, 900, 'out']], y=1060, scale=0.55, rot=0.15,
       show=[[0, False], [7.3, True, 'step'], [9.3, False, 'step']])
e.fx('badge', 'tag', screen=True, x=540, y=200, text='TURKEY TRANSLATOR: ON', color='#E8552B', size=48, w=700)
e.card('days', '5 DAYS LEFT', 0, 1.8, size=70, y=330, fill='#FFE14D')
cap = [(0.0, 1.8, 'GOBBLE GOBBLE!!', 'THIS IS NOT A DRILL.'), (1.8, 3.5, 'gobble?', 'WHY IS THE 26TH\nCIRCLED IN RED?'),
       (3.5, 5.4, 'gobble gobble', 'NEW PLAN:\nMOVE TO CANADA.'), (5.4, 7.3, 'gobble :)', 'THEIR THANKSGIVING WAS\nIN OCTOBER. SAFE!'),
       (7.3, 9.3, 'meow (cat)', "CAN I COME?\nI'LL BRING A FORK."), (9.3, None, 'GOBBLE!!!', 'PACK FASTER.')]
for i, (a, b, top, msg) in enumerate(cap):
    al = [[0, 0], [a, 1, 'step']] if a > 0 else [[0, 1]]
    if b: al.append([b, 0, 'step'])
    e.fx(f'cap{i}', 'caption', screen=True, x=540, y=1560, top=top, text=msg, size=62 if len(msg) < 26 else 52, alpha=al)
e.music('hoedown', 818, [[0, 0.9], [1.75, 0.9], [1.8, 0.4, 'step'], [3.5, 0.9, 'step'], [7.25, 0.9], [7.3, 0.3, 'step'], [9.3, 1.0, 'step']])
for t, n, g, o in [(0.0, 'gobble', 1.0, {}), (0.9, 'gobble', 0.8, {}), (1.8, 'ding', 0.6, {}), (2.0, 'gobble', 0.5, {}),
                   (3.5, 'pop', 0.8, {}), (3.6, 'gobble', 0.7, {}), (4.6, 'box', 0.6, {}), (5.4, 'sparkle', 0.7, {}),
                   (7.3, 'run', 0.6, {'loop': True, 'dur': 0.8}), (8.1, 'meow', 0.8, {'rate': 1.2}), (8.25, 'ding', 0.5, {}),
                   (9.3, 'gobble', 1.0, {}), (9.35, 'whoosh', 0.7, {}), (10.4, 'gobble', 0.8, {})]:
    e.sfx(t, n, g, **o)
print(e.save())
