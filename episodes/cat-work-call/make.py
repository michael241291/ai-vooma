import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('cat-work-call', 12, 'skit_wfh', scene='living_b',
       situation="work-from-home video call with the boss: the cat lands on the laptop keyboard, types gibberish into the chat, sits on it and shares his butt to the whole meeting",
       twist="screen close-up: every other tile in the call is now ALSO a cat; the cats run the meeting, he falls asleep on the warm keyboard",
       title="When your cat joins the work call 💻🐈",
       description="Every remote worker has had this coworker. Who else's cat attends meetings? 👇\n\nTiny Chaos: life's little chaos, animated. New video every day.\n\n#shorts #wfh #workfromhome #cat #relatable #funny")
e.scene_tracks(wall=[[0, '#DCE8F2']])
TOP = 1180
# camera: wide punch-in on the landing, screen close-ups at 4.6-6.8 and 7.8-10
e.cam(zoom=[[0, 1.3], [0.9, 1.3], [1.1, 1.15, 'out'], [4.55, 1.15], [4.6, 1.65, 'step'], [6.75, 1.65], [6.8, 1.2, 'step'],
            [7.75, 1.2], [7.8, 1.65, 'step'], [9.95, 1.65], [10.0, 1.25, 'step']],
      fx=[[0, 540]], fy=[[0, 1000], [4.55, 1000], [4.6, 870, 'step'], [6.75, 870], [6.8, 1000, 'step'], [7.75, 1000], [7.8, 870, 'step'], [9.95, 870], [10.0, 1000, 'step']],
      shake=[[0, 0], [0.85, 0], [0.9, 16, 'step'], [1.2, 0], [4.95, 0], [5.0, 12, 'step'], [5.4, 0]])
e.prop('table', 'table', x=540, y=TOP + 26, w=1000, h=420)
chat = [[0, '']]
s = ''
for i in range(18):
    s += 'jjjj;;kkk  ;'[i % 12] * (1 + i % 3)
    chat.append([1.0 + i * 0.15, s, 'step'])
chat += [[7.8, 'CATS: meow meow meow', 'step']]
e.prop('lap', 'laptop', x=540, y=TOP, scale=1.3, chat=chat,
       tiles=['BOSS', 'KAREN', 'DAVE', 'ME (MUTED)'],
       butt=[[0, -1], [4.3, 3, 'step']], cats=[[0, []], [7.8, [0, 1, 2], 'step']],
       banner=[[0, ''], [3.9, 'YOU ARE PRESENTING', 'step'], [6.8, '', 'step'], [9.0, 'CATS ARE PRESENTING', 'step'], [10.0, '', 'step']])
e.nugget('nug', x=[[0, 250], [0.9, 330, 'out'], [3.7, 760, 'linear'], [4.2, 770]],
         y=[[0, 820], [0.5, 900, 'out'], [0.9, 1140, 'in'], [3.7, 1140], [4.2, 1140]],
         scale=0.8, flip=[[0, 1]], show=[[0, True], [4.6, False, 'step'], [6.8, True, 'step'], [7.8, False, 'step'], [10.0, True, 'step']], pose=[[0, 'run'], [3.7, 'sit'], [10.0, 'loaf']], run_speed=[[0, 2.0], [0.9, 0.9]],
         rot=[[0, -0.3], [0.9, 0, 'out']],
         eye=[[0, 'wide'], [0.9, 'normal'], [3.9, 'big'], [6.8, 'happy'], [10.0, 'closed']],
         look=[[0, [0.8, 0.3]], [3.9, [-0.6, -0.8]], [6.8, [0, 0]]],
         mouth=[[0, 'scream'], [0.9, 'smile'], [4.9, 'open'], [5.6, 'smile']], mk=[[0, 0.7], [0.9, 0.3]],
         tail=[[0, 2.0], [4.0, 1.0]], blush=[[0, 0.3], [6.8, 0.8]], sunglasses=[[0, False], [6.9, True, 'step'], [10.0, False, 'step']])
e.fx('zzz', 'zzz', x=840, y=930, show=shown((10.3, 12.1)))
e.fx('love', 'hearts', x=760, y=900, show=shown((10.3, 12.1)))
e.card('t1', 'IMPORTANT CALL\nWITH THE CEO', 0, 3.9, size=92)
e.card('t2', 'OH NO.', 3.9, 4.6, size=150, fill='#FF6B6B')
e.card('t3', 'YOU ARE NOW\nPRESENTING...', 4.6, 6.8, size=96, fill='#FFE14D')
e.card('t4', 'PROMOTED.', 6.8, 7.8, size=140, fill='#7CF0A0', tilt=-0.08)
e.card('t5', 'WAIT. THEIR CATS\nJOINED TOO', 7.8, 10.0, size=92, fill='#FFFFFF')
e.card('t6', 'MEETING COULD\nHAVE BEEN A NAP', 10.0, None, size=90, fill='#9BE7FF')
e.music('sneaky', 401, [[0, 1], [3.85, 1], [3.9, 0.3, 'step'], [6.8, 1, 'step']])
for t, n, g, o in [(0.0, 'whoosh', 0.8, {}), (0.9, 'thud', 0.8, {}), (0.92, 'boing', 0.4, {'dur': 0.5}),
                   (3.9, 'ding', 0.8, {}), (4.6, 'slide_down', 0.6, {}), (5.0, 'meow', 1.0, {'rate': 0.9}),
                   (6.8, 'sparkle', 0.7, {}), (7.8, 'meow', 0.7, {'rate': 1.2}), (8.1, 'meow', 0.6, {'rate': 1.4}), (8.4, 'meow', 0.6, {'rate': 1.05}),
                   (10.0, 'slide_down', 0.5, {}), (10.2, 'purr_long', 0.6, {'dur': 1.8})]:
    e.sfx(t, n, g, **o)
for i in range(18):
    e.sfx(1.0 + i * 0.15, 'tick', 0.35)
print(e.save())
