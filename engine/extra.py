"""Batch 2 additions (2026-10-31): Gravy the turkey (second original character), backyard + bathroom backgrounds,
new props (mirror, leaf pile, food bag, calendar, toy mouse, yarn, bottle cap, pizza box, fork) and falling-leaves FX.
Registered into world.BACKGROUNDS / PROPS / FX at import (render.py imports this module)."""
import math
import random
import cairo
from core import hexc, INK, fill_stroke, ellipse, rrect, text, lerp, clamp, W, H
import world

# ============================== BACKGROUNDS ==============================

def bg_backyard(ctx, t, p):
    """Autumn backyard: sky, wooden fence, big orange tree left, grass floor."""
    sky = cairo.LinearGradient(0, -600, 0, 1330)
    sky.add_color_stop_rgba(0, *hexc(p.get('sky1', '#8FD0FF'))); sky.add_color_stop_rgba(1, *hexc(p.get('sky2', '#FFE2B8')))
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source(sky); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.9)
    for cx, cy, r in ((700, 260, 60), (760, 240, 75), (830, 265, 55), (240, 420, 40), (290, 405, 52)):
        ctx.arc(cx + 15 * math.sin(t * 0.25), cy, r, 0, 2 * math.pi); ctx.fill()
    # distant hills
    ctx.move_to(-600, 1000); ctx.curve_to(100, 860, 500, 1020, 800, 900); ctx.curve_to(1000, 830, 1300, 950, 1700, 900)
    ctx.line_to(1700, 1330); ctx.line_to(-600, 1330); ctx.close_path(); ctx.set_source_rgba(*hexc('#C9D98A')); ctx.fill()
    # fence
    for x in range(-560, W + 600, 110):
        ctx.move_to(x, 1330); ctx.line_to(x, 940); ctx.line_to(x + 45, 900); ctx.line_to(x + 90, 940); ctx.line_to(x + 90, 1330); ctx.close_path()
        fill_stroke(ctx, hexc('#F3E3C8'), 7)
    for y in (990, 1200):
        ctx.rectangle(-600, y, W + 1200, 30); fill_stroke(ctx, hexc('#E2CBA6'), 6)
    # tree (left)
    ctx.move_to(60, 1330); ctx.curve_to(110, 1100, 70, 900, 120, 620); ctx.line_to(220, 620); ctx.curve_to(210, 900, 250, 1100, 300, 1330)
    ctx.close_path(); fill_stroke(ctx, hexc('#8A5A3B'))
    rnd = random.Random(11)
    for i in range(14):
        cx = 170 + rnd.uniform(-260, 260); cy = 470 + rnd.uniform(-200, 140); r = rnd.uniform(90, 150)
        ctx.arc(cx + 6 * math.sin(t * 1.2 + i), cy, r, 0, 2 * math.pi)
        fill_stroke(ctx, hexc(['#F28C28', '#E8552B', '#F7B733', '#D9662B'][i % 4]), 7)
    # grass floor
    g = cairo.LinearGradient(0, 1330, 0, 2000)
    g.add_color_stop_rgba(0, *hexc('#8CC152')); g.add_color_stop_rgba(1, *hexc('#5E9B3A'))
    ctx.rectangle(-600, 1330, W + 1200, 1400); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(*hexc('#4E8A2E', 0.55)); ctx.set_line_width(5)
    for i in range(70):
        x = (i * 151) % (W + 400) - 200; y = 1360 + (i * 83) % 520
        ctx.move_to(x, y); ctx.line_to(x - 8, y - 26); ctx.move_to(x, y); ctx.line_to(x + 9, y - 22); ctx.stroke()
    for i in range(18):  # fallen leaves on grass
        x = (i * 211) % (W + 200) - 100; y = 1380 + (i * 127) % 460
        _leaf(ctx, x, y, 22, i * 1.7, ['#F28C28', '#E8552B', '#F7B733'][i % 3])
    ctx.rectangle(-600, 1325, W + 1200, 10); ctx.set_source_rgba(*hexc('#6EA83F')); ctx.fill()


def bg_bathroom(ctx, t, p):
    """Bathroom: square mint tiles, bathtub on the right, towel rack left, tiled floor."""
    wall = p.get('wall', '#CFEFE6')
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source_rgba(*hexc(wall)); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.55); ctx.set_line_width(5)
    for x in range(-600, W + 600, 110):
        ctx.move_to(x, -600); ctx.line_to(x, 1330); ctx.stroke()
    for y in range(-600, 1330, 110):
        ctx.move_to(-600, y); ctx.line_to(W + 600, y); ctx.stroke()
    # towel rack + towel
    ctx.rectangle(40, 640, 280, 18); fill_stroke(ctx, hexc('#B8C2CC'), 6)
    rrect(ctx, 80, 650, 200, 330, 20); fill_stroke(ctx, hexc('#FF8FA3'))
    for y in (900, 930):
        ctx.move_to(80, y); ctx.line_to(280, y); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(10); ctx.stroke()
    # little window
    rrect(ctx, 420, 260, 240, 240, 120); fill_stroke(ctx, hexc('#BFE6F2'), 10)
    ctx.move_to(540, 270); ctx.line_to(540, 490); ctx.move_to(430, 380); ctx.line_to(650, 380)
    ctx.set_source_rgba(*INK); ctx.set_line_width(7); ctx.stroke()
    # bathtub (right)
    rrect(ctx, 760, 1010, 520, 340, 70); fill_stroke(ctx, hexc('#FFFFFF'))
    ctx.rectangle(740, 990, 560, 40); fill_stroke(ctx, hexc('#F2F6FA'), 8)
    for x in (820, 1180):
        ellipse(ctx, x, 1360, 26, 20); fill_stroke(ctx, hexc('#F2C14E'), 6)
    ctx.set_source_rgba(1, 1, 1, 0.95)
    for i in range(6):
        ctx.arc(820 + i * 55, 985 - 18 * math.sin(i * 1.3 + t * 2), 34 + 6 * (i % 2), 0, 2 * math.pi); ctx.fill()
    # floor
    top = 1330
    ctx.rectangle(-600, top, W + 1200, 1400); ctx.set_source_rgba(*hexc('#F5F1E8')); ctx.fill()
    ctx.set_source_rgba(*hexc('#9FB7C2', 0.6)); ctx.set_line_width(4)
    for r in range(0, 10):
        ctx.move_to(-600, top + r * 70); ctx.line_to(W + 600, top + r * 70); ctx.stroke()
    for c in range(-6, 16):
        ctx.move_to(c * 120, top); ctx.line_to(c * 120 - 80, top + 700); ctx.stroke()
    rrect(ctx, 150, 1480, 560, 170, 80); ctx.set_source_rgba(*hexc('#7FB7E8', 0.85)); ctx.fill()
    ctx.rectangle(-600, top - 8, W + 1200, 14); ctx.set_source_rgba(*hexc('#9FB7C2')); ctx.fill()


# ============================== GRAVY THE TURKEY ==============================
FEATHERS = ['#E8552B', '#F28C28', '#F7B733', '#B5562B', '#E8552B', '#F28C28', '#F7B733']


def prop_turkey(ctx, t, p):
    """Gravy: a round, anxious cartoon turkey. Origin = floor contact (feet). ~560 px tall at scale 1.
    params: eye normal|wide|happy|closed|heart|side, look [x,y], mouth closed|open|scream|smile, flap 0..1 (wings up),
    fan 0..1 (tail spread), disguise (cat ears + whiskers + painted nose), walk (leg cycle on), sweat (bool),
    blush, bob (hop amplitude)."""
    walk = p.get('walk', False); flap = p.get('flap', 0.0); fan = p.get('fan', 1.0)
    bob = abs(math.sin(t * 9)) * 18 * p.get('bob', 0) if walk or p.get('bob') else 0
    ctx.save(); ctx.translate(0, -bob)
    # shadow
    ellipse(ctx, 0, bob, 170, 30); ctx.set_source_rgba(0, 0, 0, 0.14); ctx.fill()
    # legs
    ph = t * 10 if walk else 0
    for side in (-1, 1):
        lx = side * 55 + (math.sin(ph + (0 if side < 0 else math.pi)) * 18 if walk else 0)
        ctx.move_to(side * 50, -90); ctx.line_to(lx, -10); ctx.set_source_rgba(*INK); ctx.set_line_width(26); ctx.stroke()
        ctx.move_to(side * 50, -90); ctx.line_to(lx, -10); ctx.set_source_rgba(*hexc('#F2A13A')); ctx.set_line_width(14); ctx.stroke()
        for a in (-0.6, 0, 0.6):
            ctx.move_to(lx, -10); ctx.line_to(lx + 40 * math.sin(a), -10 + 22 * math.cos(a) * 0.4 + 6)
            ctx.set_source_rgba(*INK); ctx.set_line_width(20); ctx.stroke()
            ctx.move_to(lx, -10); ctx.line_to(lx + 40 * math.sin(a), -10 + 22 * math.cos(a) * 0.4 + 6)
            ctx.set_source_rgba(*hexc('#F2A13A')); ctx.set_line_width(10); ctx.stroke()
    # tail fan
    n = len(FEATHERS)
    for i, c in enumerate(FEATHERS):
        a = -math.pi / 2 + (i - (n - 1) / 2) * 0.32 * (0.35 + 0.65 * fan) + 0.03 * math.sin(t * 3 + i)
        ctx.save(); ctx.translate(0, -230); ctx.rotate(a + math.pi / 2)
        ctx.move_to(0, 0); ctx.curve_to(-70, -120, -60, -300, 0, -350); ctx.curve_to(60, -300, 70, -120, 0, 0); ctx.close_path()
        fill_stroke(ctx, hexc(c), 8)
        ctx.move_to(0, -40); ctx.curve_to(-30, -150, -24, -250, 0, -290); ctx.curve_to(24, -250, 30, -150, 0, -40); ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 0.22); ctx.fill()
        ctx.restore()
    # wings (behind body edges)
    for side in (-1, 1):
        ctx.save(); ctx.translate(side * 150, -240); ctx.rotate(side * (0.3 + 1.1 * flap) + side * 0.12 * math.sin(t * 30) * flap)
        ctx.move_to(0, 0); ctx.curve_to(side * 90, 20, side * 110, 120, side * 40, 170); ctx.curve_to(side * 10, 120, -side * 10, 60, 0, 0)
        ctx.close_path(); fill_stroke(ctx, hexc('#7A4A2E'), 8); ctx.restore()
    # body
    ellipse(ctx, 0, -240, 185, 175); fill_stroke(ctx, hexc('#9C6239'))
    ctx.save(); ellipse(ctx, 0, -240, 185, 175); ctx.clip()
    ellipse(ctx, 0, -175, 120, 110); ctx.set_source_rgba(*hexc('#C48557')); ctx.fill()
    ctx.set_source_rgba(*hexc('#7A4A2E', 0.6)); ctx.set_line_width(7)
    for y in (-300, -250):
        for x in (-110, 110):
            ctx.arc(x, y, 30, 0.2, math.pi - 0.2); ctx.stroke()
    ctx.restore()
    # head + neck
    hx, hy = 0, -440 + 6 * math.sin(t * 2.2)
    ctx.move_to(-55, -330); ctx.curve_to(-60, -380, -50, -400, hx - 40, hy + 40); ctx.line_to(hx + 40, hy + 40)
    ctx.curve_to(50, -400, 60, -380, 55, -330); ctx.close_path(); fill_stroke(ctx, hexc('#B9785A'))
    ellipse(ctx, hx, hy, 105, 100); fill_stroke(ctx, hexc('#C98B66'))
    if p.get('disguise'):
        for side in (-1, 1):  # cat ears (orange, a bit too small)
            ctx.move_to(hx + side * 40, hy - 85); ctx.line_to(hx + side * 95, hy - 175); ctx.line_to(hx + side * 98, hy - 60); ctx.close_path()
            fill_stroke(ctx, hexc('#F7A24E'), 8)
            ctx.move_to(hx + side * 58, hy - 88); ctx.line_to(hx + side * 88, hy - 145); ctx.line_to(hx + side * 88, hy - 80); ctx.close_path()
            ctx.set_source_rgba(*hexc('#FF94AA')); ctx.fill()
        ctx.rectangle(hx - 110, hy - 92, 220, 14); fill_stroke(ctx, hexc('#3A3F4B'), 5)  # headband
    blush = p.get('blush', 0.4)
    if blush > 0:
        ctx.set_source_rgba(*hexc('#FF7F98', blush))
        for sx in (-1, 1):
            ellipse(ctx, hx + sx * 70, hy + 30, 22, 14); ctx.fill()
    # eyes
    mode = p.get('eye', 'normal'); lx, ly = p.get('look', [0, 0])
    blink = (t * 0.7) % 3.7 < 0.12 and mode in ('normal', 'side')
    for side in (-1, 1):
        ex, ey = hx + side * 40, hy - 18
        if mode == 'happy':
            ctx.move_to(ex - 22, ey + 6); ctx.curve_to(ex - 12, ey - 18, ex + 12, ey - 18, ex + 22, ey + 6)
            ctx.set_source_rgba(*INK); ctx.set_line_width(9); ctx.stroke(); continue
        if mode == 'closed' or blink:
            ctx.move_to(ex - 22, ey); ctx.line_to(ex + 22, ey); ctx.set_source_rgba(*INK); ctx.set_line_width(9); ctx.stroke(); continue
        if mode == 'heart':
            world_heart(ctx, ex, ey, 22); ctx.set_source_rgba(*hexc('#FF4F7B')); ctx.fill_preserve()
            ctx.set_source_rgba(*INK); ctx.set_line_width(5); ctx.stroke(); continue
        r = 38 if mode == 'wide' else 30
        ellipse(ctx, ex, ey, r * 0.85, r); fill_stroke(ctx, hexc('#FFFFFF'), 6)
        pr = 9 if mode == 'wide' else 14
        if mode == 'side':
            lx = 0.8
        ctx.arc(ex + lx * r * 0.4, ey + ly * r * 0.4, pr, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
        ctx.arc(ex + lx * r * 0.4 - 4, ey + ly * r * 0.4 - 5, pr * 0.35, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
        if mode == 'side':  # suspicious half lid
            ctx.rectangle(ex - r, ey - r - 2, 2 * r, r * 0.9); ctx.set_source_rgba(*hexc('#C98B66')); ctx.fill()
            ctx.move_to(ex - r * 0.85, ey - r * 0.1); ctx.line_to(ex + r * 0.85, ey - r * 0.1); ctx.set_source_rgba(*INK); ctx.set_line_width(7); ctx.stroke()
    # beak + wattle
    mouth = p.get('mouth', 'closed')
    open_ = {'closed': 0, 'smile': 0, 'open': 22, 'scream': 44}.get(mouth, 0)
    ctx.move_to(hx - 26, hy + 18); ctx.line_to(hx + 26, hy + 18); ctx.line_to(hx, hy + 48 - open_ * 0.2); ctx.close_path()
    fill_stroke(ctx, hexc('#F7B733'), 6)
    if open_:
        ctx.move_to(hx - 22, hy + 24); ctx.line_to(hx + 22, hy + 24); ctx.line_to(hx, hy + 30 + open_); ctx.close_path()
        fill_stroke(ctx, hexc('#F2A13A'), 6)
    ctx.move_to(hx + 8, hy + 40); ctx.curve_to(hx + 40, hy + 60, hx + 30, hy + 110, hx + 6, hy + 100)
    ctx.curve_to(hx - 6, hy + 80, hx - 4, hy + 60, hx + 8, hy + 40); fill_stroke(ctx, hexc('#E8352B'), 6)
    if p.get('disguise'):  # whiskers drawn on with marker + pink nose
        ellipse(ctx, hx, hy + 14, 14, 10); fill_stroke(ctx, hexc('#FF94AA'), 4)
        ctx.set_source_rgba(*INK); ctx.set_line_width(5)
        for sd in (-1, 1):
            for dy in (-6, 10):
                ctx.move_to(hx + sd * 34, hy + 30 + dy); ctx.line_to(hx + sd * 110, hy + 20 + dy * 1.6); ctx.stroke()
    if p.get('sweat'):
        ph = (t * 1.6) % 1.0
        ctx.save(); ctx.translate(hx + 110, hy - 60 + 90 * ph)
        ctx.move_to(0, -26); ctx.curve_to(12, -4, 16, 9, 0, 15); ctx.curve_to(-16, 9, -12, -4, 0, -26); ctx.close_path()
        ctx.set_source_rgba(*hexc('#8FD3FF', math.sin(math.pi * ph))); ctx.fill(); ctx.restore()
    ctx.restore()


def world_heart(ctx, x, y, s):
    ctx.move_to(x, y + s * 0.9); ctx.curve_to(x - s * 1.6, y - s * 0.2, x - s * 0.8, y - s * 1.4, x, y - s * 0.5)
    ctx.curve_to(x + s * 0.8, y - s * 1.4, x + s * 1.6, y - s * 0.2, x, y + s * 0.9); ctx.close_path()


# ============================== PROPS ==============================

def _leaf(ctx, x, y, s, rot, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.move_to(0, -s); ctx.curve_to(s * 0.9, -s * 0.6, s * 0.7, s * 0.6, 0, s); ctx.curve_to(-s * 0.7, s * 0.6, -s * 0.9, -s * 0.6, 0, -s)
    ctx.close_path(); ctx.set_source_rgba(*hexc(col)); ctx.fill_preserve()
    ctx.set_source_rgba(*INK); ctx.set_line_width(max(2, s * 0.12)); ctx.stroke()
    ctx.move_to(0, -s * 0.8); ctx.line_to(0, s * 1.2); ctx.stroke()
    ctx.restore()


def prop_leafpile(ctx, t, p):
    """Mound of autumn leaves, origin = floor centre. w width, h height, jiggle 0..1, part back|front|all."""
    w = p.get('w', 520); h = p.get('h', 260); jig = p.get('jiggle', 0.0); part = p.get('part', 'all')
    rnd = random.Random(p.get('seed', 3))
    leaves = []
    for i in range(110):
        u = rnd.uniform(-1, 1); v = rnd.random()
        x = u * w / 2 * (1 - 0.35 * v); y = -v * h * math.sqrt(max(0, 1 - u * u))
        leaves.append((x, y, rnd.uniform(26, 40), rnd.uniform(0, 6.28), FEATHERS[i % 3 + (i % 2) * 3 if i % 5 else 2]))
    if part in ('back', 'all'):
        ctx.move_to(-w / 2, 0); ctx.curve_to(-w / 2, -h * 1.1, w / 2, -h * 1.1, w / 2, 0); ctx.close_path()
        fill_stroke(ctx, hexc('#D9662B'), 8)
    sel = leaves if part == 'all' else (leaves[:70] if part == 'back' else leaves[70:])
    for (x, y, s, r, c) in sel:
        if part == 'front' and y < -h * 0.45:
            continue
        _leaf(ctx, x + jig * 10 * math.sin(t * 40 + x), y + jig * 8 * math.cos(t * 37 + y), s, r + jig * 0.3 * math.sin(t * 30 + s), c)


def prop_mirror(ctx, t, p):
    """Standing oval mirror. part 'glass' (draw first) or 'frame' (draw after the reflection). Glass centre at (0,-500)."""
    part = p.get('part', 'frame'); rx, ry = 250, 400
    if part == 'glass':
        g = cairo.LinearGradient(-rx, -900, rx, -100)
        g.add_color_stop_rgba(0, *hexc('#E6F6FF')); g.add_color_stop_rgba(1, *hexc('#B9DDF0'))
        ellipse(ctx, 0, -500, rx, ry); ctx.set_source(g); ctx.fill()
        return
    ctx.set_source_rgba(1, 1, 1, 0.35)
    ctx.move_to(-150, -760); ctx.line_to(-60, -790); ctx.line_to(-190, -480); ctx.line_to(-220, -560); ctx.close_path(); ctx.fill()
    ellipse(ctx, 0, -500, rx, ry); ctx.set_source_rgba(*INK); ctx.set_line_width(48); ctx.stroke()
    ellipse(ctx, 0, -500, rx, ry); ctx.set_source_rgba(*hexc(p.get('color', '#D9A441'))); ctx.set_line_width(34); ctx.stroke()
    for sx in (-1, 1):
        ctx.move_to(sx * 120, -130); ctx.line_to(sx * 200, 0); ctx.set_source_rgba(*INK); ctx.set_line_width(30); ctx.stroke()
        ctx.move_to(sx * 120, -130); ctx.line_to(sx * 200, 0); ctx.set_source_rgba(*hexc(p.get('color', '#D9A441'))); ctx.set_line_width(18); ctx.stroke()


def prop_foodbag(ctx, t, p):
    """Crinkly treat bag, origin = bottom centre. shake 0..1 rustles it."""
    sh = p.get('shake', 0.0)
    ctx.save(); ctx.rotate(sh * 0.12 * math.sin(t * 45))
    ctx.move_to(-120, 0); ctx.line_to(-135, -300); ctx.line_to(135, -300); ctx.line_to(120, 0); ctx.close_path()
    fill_stroke(ctx, hexc(p.get('color', '#7B5CE6')))
    ctx.rectangle(-140, -335, 280, 40); fill_stroke(ctx, hexc('#B9A6FF'), 7)
    ctx.set_source_rgba(*INK); ctx.set_line_width(4)
    for x in range(-130, 140, 20):
        ctx.move_to(x, -335); ctx.line_to(x + 10, -315); ctx.line_to(x + 20, -335); ctx.stroke()
    ellipse(ctx, 0, -160, 90, 70); fill_stroke(ctx, hexc('#FFE14D'), 6)
    text(ctx, p.get('label', 'CRUNCHY\nTREATS'), 0, -160, 34, hexc('#E2463F'), sw=6)
    ctx.restore()


def prop_calendar(ctx, t, p):
    """Wall calendar, origin = top hook. month text, day big number, flip 0..1 (page lifting)."""
    rrect(ctx, -170, 20, 340, 380, 16); fill_stroke(ctx, hexc('#FFFFFF'))
    ctx.rectangle(-170, 20, 340, 110); fill_stroke(ctx, hexc(p.get('color', '#E8552B')))
    text(ctx, p.get('month', 'NOVEMBER'), 0, 76, 52, hexc('#FFFFFF'), sw=8)
    text(ctx, str(p.get('day', '')), 0, 270, 160, hexc('#3A2216'), ink=hexc('#FFFFFF'), sw=2)
    if p.get('circle'):
        ctx.arc(0, 265, 115, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#E2463F')); ctx.set_line_width(12); ctx.stroke()
    ctx.arc(0, 10, 16, 0, 2 * math.pi); fill_stroke(ctx, hexc('#B8C2CC'), 6)
    fl = p.get('flip', 0.0)
    if fl > 0:
        sy = -lerp(1, 0, fl) if fl > 0.5 else lerp(1, 0, fl)
        if abs(sy) > 0.02:  # a zero scale makes the cairo matrix non-invertible
            ctx.save(); ctx.translate(0, 20); ctx.scale(1, sy)
            rrect(ctx, -170, 0, 340, 380, 16); fill_stroke(ctx, hexc('#F2F2F2'))
            ctx.restore()


def prop_toymouse(ctx, t, p):
    ellipse(ctx, 0, -45, 80, 45); fill_stroke(ctx, hexc(p.get('color', '#B8C2CC')))
    ctx.arc(-50, -85, 26, 0, 2 * math.pi); fill_stroke(ctx, hexc('#FF94AA'), 6)
    ctx.arc(75, -50, 9, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
    ctx.arc(30, -60, 7, 0, 2 * math.pi); ctx.fill()
    ctx.move_to(-80, -40); ctx.curve_to(-150, -40, -140, 10, -200, -10); ctx.set_line_width(8); ctx.stroke()
    if p.get('tag'):
        rrect(ctx, -40, -150, 120, 50, 8); fill_stroke(ctx, hexc('#FFF59A'), 5)
        text(ctx, p['tag'], 20, -125, 34, hexc('#E2463F'), sw=5)


def prop_yarn(ctx, t, p):
    ctx.arc(0, -70, 70, 0, 2 * math.pi); fill_stroke(ctx, hexc(p.get('color', '#FF6FA0')))
    ctx.save(); ctx.arc(0, -70, 70, 0, 2 * math.pi); ctx.clip()
    ctx.set_source_rgba(*hexc('#C9447A')); ctx.set_line_width(6)
    for i in range(6):
        ctx.arc(-40 + i * 18, -70, 60, -1.2, 1.2); ctx.stroke()
    ctx.restore()
    ctx.move_to(60, -30); ctx.curve_to(120, 0, 150, -10, 200, 0); ctx.set_source_rgba(*INK); ctx.set_line_width(8); ctx.stroke()


def prop_bottlecap(ctx, t, p):
    ctx.save(); ctx.scale(1, 0.5)
    for i in range(24):
        a = i * 2 * math.pi / 24
        r = 48 if i % 2 else 42
        (ctx.move_to if i == 0 else ctx.line_to)(r * math.cos(a), -40 + r * math.sin(a))
    ctx.close_path(); ctx.restore(); fill_stroke(ctx, hexc('#E2463F'), 6)
    ctx.rectangle(-44, -20, 88, 20); fill_stroke(ctx, hexc('#C0392B'), 6)


def prop_pizzabox(ctx, t, p):
    """Pizza box, origin floor centre. open 0..1 lifts the lid showing the pizza."""
    op = p.get('open', 0.0)
    ctx.rectangle(-200, -60, 400, 60); fill_stroke(ctx, hexc('#F3E3C8'))
    if op > 0.05:
        ellipse(ctx, 0, -60, 170, 40); fill_stroke(ctx, hexc('#F7B733'), 7)
        ellipse(ctx, 0, -62, 150, 32); ctx.set_source_rgba(*hexc('#E8552B')); ctx.fill()
        for dx, dy in ((-80, -60), (-10, -72), (60, -58), (100, -66), (20, -52)):
            ellipse(ctx, dx, dy, 18, 8); ctx.set_source_rgba(*hexc('#B5262B')); ctx.fill()
    ctx.save(); ctx.translate(0, -60); ctx.scale(1, math.cos(op * math.pi * 0.55))
    ctx.rectangle(-200, -2 - (0 if op < 0.5 else 0), 400, 2); ctx.restore()
    lid_h = 60 + 300 * math.sin(op * math.pi / 2)
    ctx.move_to(-200, -60); ctx.line_to(-200, -60 - lid_h * (1 if op > 0 else 0)); ctx.line_to(200, -60 - lid_h * (1 if op > 0 else 0)); ctx.line_to(200, -60)
    if op > 0.05:
        ctx.close_path(); fill_stroke(ctx, hexc('#EAD7B5'))
        text(ctx, p.get('label', 'PIZZA'), 0, -60 - lid_h * 0.55, 60, hexc('#E2463F'), sw=8)
    else:
        ctx.new_path()
        ctx.rectangle(-200, -75, 400, 18); fill_stroke(ctx, hexc('#EAD7B5'), 7)
        text(ctx, p.get('label', 'PIZZA'), 0, -35, 40, hexc('#E2463F'), sw=6)


def prop_fork(ctx, t, p):
    """Giant fork pointing down, origin = tip area (bottom)."""
    for x in (-45, -15, 15, 45):
        rrect(ctx, x - 9, -260, 18, 260, 9); fill_stroke(ctx, hexc('#D6DEE6'), 6)
    rrect(ctx, -62, -320, 124, 80, 30); fill_stroke(ctx, hexc('#D6DEE6'), 7)
    rrect(ctx, -26, -900, 52, 600, 26); fill_stroke(ctx, hexc('#B8C2CC'), 7)


def prop_table_sign(ctx, t, p):
    rrect(ctx, -160, -110, 320, 110, 14); fill_stroke(ctx, hexc('#FFF59A'), 7)
    text(ctx, p.get('label', '1'), 0, -55, 70, hexc('#3A2216'), ink=hexc('#FFFFFF'), sw=2)


# ============================== FX ==============================

def fx_leaves(ctx, t, p):
    """Leaves falling across the whole frame (screen or world). density n, wind."""
    rnd = random.Random(p.get('seed', 7)); n = p.get('n', 16); a = p.get('alpha', 1.0)
    if a <= 0: return
    for i in range(n):
        sx = rnd.uniform(-100, W + 100); sp = rnd.uniform(0.18, 0.32); ph = (t * sp + rnd.random()) % 1.0
        x = sx + 80 * math.sin(t * 1.8 + i) + p.get('wind', 0) * ph * 300; y = -150 + ph * (H + 300)
        _leaf(ctx, x - p.get('ox', 0), y - p.get('oy', 0), rnd.uniform(24, 38), t * 2 + i, ['#F28C28', '#E8552B', '#F7B733', '#D9662B'][i % 4])


def fx_question(ctx, t, p):
    """Numbered choice badge (1/2/3) with bounce."""
    s = p.get('scale', 1.0)
    ctx.arc(0, 0, 60 * s, 0, 2 * math.pi); fill_stroke(ctx, hexc(p.get('color', '#5A79C2')), 8)
    text(ctx, p.get('label', '1'), 0, 2, 76 * s, hexc('#FFFFFF'), sw=8)


world.BACKGROUNDS.update(backyard=bg_backyard, bathroom=bg_bathroom)
world.PROPS.update(turkey=prop_turkey, leafpile=prop_leafpile, mirror=prop_mirror, foodbag=prop_foodbag, calendar=prop_calendar,
                   toymouse=prop_toymouse, yarn=prop_yarn, bottlecap=prop_bottlecap, pizzabox=prop_pizzabox, fork=prop_fork,
                   sign=prop_table_sign)
world.FX.update(leaves=fx_leaves, badge=fx_question)
world.SELF_ALPHA_EXTRA = {'leaves', 'badge'}


def prop_bowl2(ctx, t, p):
    """Food bowl seen from slightly above (batch 2). hole 0..1 = bare patch in the middle (the 'half full' cat-owner trope)."""
    hole = p.get('hole', 0.0); label = p.get('label', 'NUGGET')
    ctx.move_to(-170, -70); ctx.line_to(170, -70); ctx.line_to(130, 20); ctx.line_to(-130, 20); ctx.close_path()
    fill_stroke(ctx, hexc(p.get('color', '#4DA3FF')))
    ellipse(ctx, 0, -70, 170, 55); fill_stroke(ctx, hexc('#2D6FB8'), 8)
    ellipse(ctx, 0, -70, 150, 44); ctx.set_source_rgba(*hexc('#D8ECFF')); ctx.fill()
    ctx.save(); ellipse(ctx, 0, -70, 150, 44); ctx.clip()
    rnd = random.Random(8)
    for i in range(140):
        x = rnd.uniform(-150, 150); y = -70 + rnd.uniform(-44, 44)
        if (x / 150) ** 2 + ((y + 70) / 44) ** 2 > 1: continue
        if hole > 0 and (x / (120 * hole + 1e-6)) ** 2 + ((y + 70) / (36 * hole + 1e-6)) ** 2 < 1: continue
        ellipse(ctx, x, y, 13, 9); ctx.set_source_rgba(*hexc(['#B5703A', '#9C5B2C', '#C98A55'][i % 3])); ctx.fill_preserve()
        ctx.set_source_rgba(*hexc('#6E3B1A')); ctx.set_line_width(2); ctx.stroke()
    ctx.restore()
    text(ctx, label, 0, -15, 36, hexc('#FFFFFF'), sw=6)


world.PROPS.update(bowl2=prop_bowl2)
