import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'engine'))
from build import Ep, shown
e = Ep('cookie-climb', 11, 'interactive_play', scene='kitchen',
       situation="Nugget keeps sliding down the kitchen counter trying to reach the cookie jar; the viewer's finger becomes his step stool",
       twist="he gets a cookie, splits it 'half for you' and hands the viewer a single crumb while keeping the giant half; then asks for the finger AGAIN",
       title="Hold your finger here so he can reach the cookies 👆🍪",
       description="He shared. Technically. Did you get your crumb? 👇\n\nNugget is an orange cat with exactly one brain cell. New video every day.\n\n#shorts #cat #interactive #cookies #funny #animation")
e.scene_tracks(wall=[[0, '#FFE6D6']])
e.cam(zoom=[[0, 1.45], [2.4, 1.3], [3.0, 1.3], [3.6, 1.45, 'out'], [6.0, 1.45], [6.3, 1.75, 'out'], [8.0, 1.75], [8.3, 1.45, 'out'], [11, 1.4]],
      fx=[[0, 560], [2.6, 560], [3.6, 760], [6.0, 760], [6.3, 830], [8.0, 830], [8.3, 760], [10.0, 760], [10.4, 560]],
      fy=[[0, 1050], [2.6, 1050], [3.6, 760], [6.0, 760], [6.3, 700], [8.0, 700], [8.3, 760], [10.0, 760], [10.4, 1050]],
      px=[[0, 0], [6.0, 0], [6.3, 160, 'out'], [8.0, 160], [8.3, 0, 'out']],
      shake=[[0, 0], [0.55, 0], [0.6, 8, 'step'], [0.8, 0]])
e.prop('jar', 'cookiejar', x=930, y=792, scale=0.85, n=6, lid=[[0, 0], [4.3, 0], [4.5, 1, 'back']])
X = [[0, 610], [0.6, 610], [1.2, 260, 'out'], [2.9, 260], [3.15, 540, 'out'], [3.5, 540], [3.85, 740, 'out']]
Y = [[0, 880], [0.6, 900], [1.2, 1272, 'in'], [2.9, 1272], [3.15, 1036, 'out'], [3.5, 1036], [3.7, 640, 'out'], [3.85, 768, 'in'],
     [10.0, 768], [10.2, 620, 'out'], [10.5, 1272, 'in']]
X += [[10.0, 740], [10.5, 260]]
e.nugget('nug', x=X, y=Y, scale=[[0, 0.85], [2.9, 0.85], [3.15, 0.7]], flip=[[0, 1]],
         pose=[[0, 'run'], [1.2, 'sit'], [2.9, 'run'], [3.15, 'sit'], [3.5, 'run'], [3.85, 'sit'], [10.0, 'run'], [10.5, 'sit']], run_speed=2.0,
         eye=[[0, 'squeeze'], [1.2, 'big'], [2.9, 'wide'], [3.85, 'normal'], [4.5, 'heart'], [6.3, 'happy'], [8.0, 'normal'], [8.6, 'happy'], [10.5, 'big']],
         look=[[0, [0.6, -0.8]], [1.2, [0.3, -0.5]], [2.6, [0.2, 0.6]], [3.85, [0.8, 0]], [6.3, [0, 0.2]], [8.6, [0, 0]], [10.5, [0.2, 0.6]]],
         mouth=[[0, 'scream'], [1.2, 'frown'], [2.9, 'open'], [3.85, 'smile'], [4.5, 'open'], [6.3, 'smile'], [8.6, 'chew'], [10.5, 'o']],
         mk=[[0, 0.8], [1.2, 0.4]], sweat=[[0, True], [1.2, False]], blush=[[0, 0.35], [6.3, 0.9], [8.6, 0.5]], tail=[[0, 2.5], [3.85, 2.0]],
         paw=[[0, None], [4.6, None], [4.65, [170, -220], 'step'], [5.2, [120, -150]], [6.2, [80, -130]], [6.3, [200, -60]], [8.6, [60, -160]], [9.8, None, 'step']],
         paw2=[[0, None], [6.2, None], [6.3, [-60, -80], 'step'], [8.6, [-40, -140]], [9.8, None, 'step']])
# cookie: in jar -> paw -> split (half kept, crumb offered)
e.prop('ck', 'cookie', x=[[0, 880], [4.6, 880], [5.2, 830]], y=[[0, 600], [4.6, 600], [5.2, 670]], scale=0.6, show=shown((4.65, 6.25)))
e.prop('half', 'cookie', half=True, x=[[0, 712], [8.6, 712], [9.6, 760]], y=[[0, 700], [8.6, 700], [9.6, 640]],
       scale=[[0, 1.05], [8.6, 1.05], [9.7, 0.0]], show=shown((6.3, 9.75)))
e.prop('crumb', 'cookie', crumb=True, x=900, y=726, scale=1.4, show=shown((6.3, 10.0)))
e.fx('target', 'target', x=540, y=1060, r=110, label='HOLD HERE!', label_size=56,
     alpha=[[0, 0], [1.2, 0, 'step'], [1.4, 1], [2.75, 1], [2.85, 0], [10.4, 0], [10.6, 1]], scale=[[0, 0.3], [1.2, 0.3], [1.45, 1.0, 'back']])
e.fx('finger', 'hand', pose='finger', x=540, y=[[0, 2700], [2.6, 2700], [2.9, 1300, 'out'], [3.6, 1300], [3.95, 2700, 'in']])
e.fx('shine', 'sparkle', x=880, y=640, r=150, show=shown((4.5, 5.4)))
e.fx('love', 'hearts', x=760, y=520, show=shown((4.6, 6.0)))
e.fx('yours', 'text', x=900, y=630, text='YOURS', size=46, fill='#FFE14D', tilt=0.15, show=shown((6.6, 10.0)))
e.card('t1', "HE CAN'T REACH\nTHE COOKIES", 0, 1.3, size=96, fill='#FF8F6B', pulse=1)
e.card('t2', 'HOLD YOUR\nFINGER HERE', 1.3, 2.9, size=100, fill='#FFE14D')
e.card('t3', 'GOT IT!', 4.5, 6.2, size=140, fill='#9BE7FF')
e.card('t4', 'HALF FOR YOU', 6.3, 8.0, size=120, fill='#FFFFFF')
e.card('t5', 'SHARING IS CARING', 8.0, 10.4, size=100, fill='#FFE14D')
e.card('t6', 'AGAIN?', 10.5, None, size=150, fill='#FF8F6B', pulse=1)
e.music('cozy', 601, [[0, 0.5], [1.3, 0.5], [1.35, 1, 'step']])
for t, n, g, o in [(0.0, 'scratch', 0.8, {}), (0.6, 'slide_down', 0.6, {}), (1.2, 'thud', 0.7, {}), (1.4, 'pop', 0.5, {}),
                   (2.9, 'boing', 0.6, {}), (3.5, 'boing', 0.6, {}), (3.85, 'thud', 0.5, {}), (4.5, 'pop', 0.7, {}), (4.55, 'sparkle', 0.6, {}),
                   (6.3, 'crunch', 0.8, {}), (6.35, 'ding', 0.5, {}), (7.0, 'pop', 0.4, {}), (8.0, 'aww', 0.5, {}), (8.6, 'crunch', 0.6, {}),
                   (9.1, 'crunch', 0.6, {}), (10.0, 'swoosh', 0.5, {}), (10.5, 'thud', 0.5, {}), (10.6, 'meow', 0.8, {'rate': 1.1})]:
    e.sfx(t, n, g, **o)
print(e.save())
