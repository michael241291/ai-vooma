"""Batch 3 additions (2026-11-07): Thanksgiving dining-table background, new props (whipped-cream can, pie, cookie jar,
cookie, tuna can, bathroom scale, yoga mat) and FX (cream blob, reveal ring, subtitle caption, timer bar, panel label).
Split-screen / spot-the-difference panels live in render.py (episode key "panels").
Registered into world.BACKGROUNDS / PROPS / FX at import (render.py imports this module)."""
import math
import random
import cairo
from core import hexc, INK, fill_stroke, ellipse, rrect, text, lerp, clamp, W, H
import world

# ============================== BACKGROUND ==============================

def bg_dining(ctx, t, p):
    """Thanksgiving dining room. The tablecloth top is the 'floor' (y 1330): characters sit ON the table.
    Wall with leaf garland, window with autumn dusk, framed pumpkin picture; plaid orange tablecloth."""
    wall = p.get('wall', '#F3D6A4')
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source_rgba(*hexc(wall)); ctx.fill()
    ctx.set_source_rgba(*hexc('#E9C38A', 0.55))
    for x in range(-600, W + 600, 160):  # soft vertical damask stripes
        ctx.rectangle(x, -600, 60, 1940); ctx.fill()
    # window (dusk)
    sky = cairo.LinearGradient(0, 360, 0, 860)
    sky.add_color_stop_rgba(0, *hexc('#6B5BA8')); sky.add_color_stop_rgba(1, *hexc('#FFB36B'))
    rrect(ctx, 620, 380, 340, 480, 14); ctx.set_source(sky); ctx.fill_preserve(); ctx.set_source_rgba(*INK); ctx.set_line_width(9); ctx.stroke()
    ctx.move_to(790, 380); ctx.line_to(790, 860); ctx.move_to(620, 620); ctx.line_to(960, 620); ctx.set_line_width(14)
    ctx.set_source_rgba(*hexc('#FFF4E2')); ctx.stroke()
    ctx.arc(700, 470, 34, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFF1B8')); ctx.fill()
    # picture with pumpkin
    rrect(ctx, 120, 420, 260, 220, 10); fill_stroke(ctx, hexc('#FFF8EC'), 9)
    ellipse(ctx, 250, 560, 80, 55); fill_stroke(ctx, hexc('#F28C28'), 6)
    ctx.rectangle(244, 490, 12, 20); fill_stroke(ctx, hexc('#6E8B3D'), 4)
    # leaf garland across the top
    for i in range(-3, 14):
        x = i * 100; y = 300 + 40 * math.sin(i * 0.9)
        world_leaf(ctx, x, y, 28, i * 1.3 + 0.2 * math.sin(t * 2 + i), ['#F28C28', '#E8552B', '#F7B733', '#B5582B'][i % 4])
    # back wall chair rail
    ctx.rectangle(-600, 1000, W + 1200, 18); ctx.set_source_rgba(*hexc('#FFFFFF', 0.7)); ctx.fill()
    # table: tablecloth from y 1330 down, plaid
    top = 1330
    ctx.rectangle(-600, top, W + 1200, 1400); ctx.set_source_rgba(*hexc(p.get('cloth', '#E8792E'))); ctx.fill()
    ctx.set_source_rgba(*hexc('#FFE3B8', 0.35))
    for x in range(-600, W + 600, 120):
        ctx.rectangle(x, top, 40, 1400); ctx.fill()
    for y in range(top + 40, top + 1400, 120):
        ctx.rectangle(-600, y, W + 1200, 40); ctx.fill()
    ctx.rectangle(-600, top - 10, W + 1200, 20); ctx.set_source_rgba(*hexc('#C65A1E')); ctx.fill()


def world_leaf(ctx, x, y, s, rot, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.move_to(0, -s); ctx.curve_to(s * 0.9, -s * 0.5, s * 0.9, s * 0.5, 0, s); ctx.curve_to(-s * 0.9, s * 0.5, -s * 0.9, -s * 0.5, 0, -s)
    ctx.close_path(); fill_stroke(ctx, hexc(col), 4)
    ctx.restore()


# ============================== PROPS ==============================

def prop_whipcan(ctx, t, p):
    """Whipped-cream can lying on its side, nozzle pointing left (use flip). origin = can centre.
    spray 0..1 draws a cream jet of length `jet` from the nozzle."""
    ctx.save()
    rrect(ctx, -60, -170, 120, 300, 30); fill_stroke(ctx, hexc('#E8F0FA'))
    ctx.rectangle(-60, -90, 120, 120); fill_stroke(ctx, hexc('#4DA3FF'), 7)
    text(ctx, 'WHIP', 0, -30, 40, hexc('#FFFFFF'), sw=6)
    rrect(ctx, -40, -215, 80, 50, 12); fill_stroke(ctx, hexc('#FF6FA0'), 7)
    ctx.move_to(-14, -215); ctx.line_to(-8, -270); ctx.line_to(8, -270); ctx.line_to(14, -215); ctx.close_path()
    fill_stroke(ctx, hexc('#FFFFFF'), 6)
    sp = p.get('spray', 0.0)
    if sp > 0:
        L = p.get('jet', 260) * sp
        jet = [(3 * math.sin(t * 50 + i), -280 - i / 8 * L, 18 + 8 * math.sin(t * 40 + i)) for i in range(9)]
        for x, y, r in jet:
            ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.set_line_width(10); ctx.stroke()
        for x, y, r in jet:
            ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFFDF5')); ctx.fill()
    ctx.restore()


def prop_pie(ctx, t, p):
    """Pumpkin pie on a dish, origin = floor contact."""
    ellipse(ctx, 0, -20, 200, 50); fill_stroke(ctx, hexc('#FFFFFF'))
    ellipse(ctx, 0, -45, 170, 45); fill_stroke(ctx, hexc('#D99A4E'))
    ellipse(ctx, 0, -50, 140, 34); fill_stroke(ctx, hexc('#E37B2B'), 6)
    if p.get('cream', True):
        for dx in (-60, 0, 60):
            ellipse(ctx, dx, -70, 26, 18); fill_stroke(ctx, hexc('#FFFDF5'), 5)


def prop_cookiejar(ctx, t, p):
    """Glass cookie jar, origin = bottom centre. lid 0..1 (lifted), n cookies inside."""
    ctx.move_to(-110, 0); ctx.line_to(-120, -230); ctx.curve_to(-120, -270, 120, -270, 120, -230); ctx.line_to(110, 0); ctx.close_path()
    ctx.set_source_rgba(*hexc('#DDF3FF', 0.75)); ctx.fill_preserve(); ctx.set_source_rgba(*INK); ctx.set_line_width(9); ctx.stroke()
    rnd = random.Random(3)
    for i in range(int(p.get('n', 6))):
        x = rnd.uniform(-70, 70); y = -30 - (i // 3) * 55 - rnd.uniform(0, 15)
        _cookie(ctx, x, y, 38, i)
    lid = p.get('lid', 0.0)
    ctx.save(); ctx.translate(-lid * 60, -270 - lid * 120); ctx.rotate(-lid * 0.5)
    ellipse(ctx, 0, 0, 125, 22); fill_stroke(ctx, hexc('#E2463F'), 8)
    ctx.arc(0, -26, 22, 0, 2 * math.pi); fill_stroke(ctx, hexc('#E2463F'), 7)
    ctx.restore()
    text(ctx, p.get('label', 'COOKIES'), 0, -120, 38, hexc('#E2463F'), ink=hexc('#FFFFFF'), sw=8)


def _cookie(ctx, x, y, r, seed=0):
    ctx.arc(x, y, r, 0, 2 * math.pi); fill_stroke(ctx, hexc('#D9A35E'), 6)
    rnd = random.Random(seed + 10)
    for _ in range(5):
        ctx.arc(x + rnd.uniform(-r * 0.6, r * 0.6), y + rnd.uniform(-r * 0.6, r * 0.6), r * 0.13, 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc('#4A2A14')); ctx.fill()


def prop_cookie(ctx, t, p):
    """One cookie, origin = centre. half=True draws half a cookie; crumb=True draws a tiny crumb."""
    if p.get('crumb'):
        ctx.arc(0, 0, 12, 0, 2 * math.pi); fill_stroke(ctx, hexc('#D9A35E'), 4); return
    if p.get('half'):
        ctx.save(); ctx.rectangle(-80, -80, 80, 160); ctx.clip(); _cookie(ctx, 0, 0, 60, 2); ctx.restore()
        ctx.move_to(0, -60); ctx.line_to(-8, -30); ctx.line_to(6, 0); ctx.line_to(-6, 30); ctx.line_to(0, 60)
        ctx.set_source_rgba(*INK); ctx.set_line_width(6); ctx.stroke(); return
    _cookie(ctx, 0, 0, 60, 2)


def prop_tunacan(ctx, t, p):
    """Tuna can, origin = bottom centre. open 0..1 lifts the lid; label text."""
    ctx.rectangle(-110, -110, 220, 110); fill_stroke(ctx, hexc('#BFC9D4'))
    ctx.rectangle(-110, -95, 220, 80); fill_stroke(ctx, hexc(p.get('color', '#2F80ED')), 6)
    text(ctx, p.get('label', 'TUNA'), 0, -55, 50, hexc('#FFFFFF'), sw=8)
    ellipse(ctx, 0, -110, 110, 26); fill_stroke(ctx, hexc('#E5ECF2'), 7)
    op = p.get('open', 0.0)
    if op > 0:
        ellipse(ctx, 0, -110, 92, 20); ctx.set_source_rgba(*hexc('#F2B8A0')); ctx.fill()
        ctx.save(); ctx.translate(90, -112); ctx.rotate(-op * 1.6)
        ellipse(ctx, -90, 0, 100, 22); fill_stroke(ctx, hexc('#DCE3EA'), 6); ctx.restore()


def prop_scale(ctx, t, p):
    """Bathroom scale, origin = floor contact. reading text in the window, glow 0..1 makes it blink red."""
    rrect(ctx, -170, -60, 340, 60, 20); fill_stroke(ctx, hexc('#F5F7FA'))
    rrect(ctx, -90, -52, 180, 40, 8); ctx.set_source_rgba(*hexc('#1E2A30')); ctx.fill()
    g = p.get('glow', 0.0)
    col = '#FF5A4E' if (g > 0 and (t * 6) % 1 < 0.6) else '#7CF0A0'
    text(ctx, p.get('reading', '0.0'), 0, -32, 34, hexc(col), ink=hexc('#0B1418'), sw=3)
    if p.get('big'):
        rrect(ctx, -230, -340, 460, 200, 20); fill_stroke(ctx, hexc('#1E2A30'), 9)
        text(ctx, p.get('reading', '0.0'), 0, -240, 120, hexc(col), ink=hexc('#0B1418'), sw=4)


def prop_yogamat(ctx, t, p):
    ctx.move_to(-330, 0); ctx.line_to(330, 0); ctx.line_to(300, -40); ctx.line_to(-300, -40); ctx.close_path()
    fill_stroke(ctx, hexc(p.get('color', '#9B7BEA')), 7)


world.BACKGROUNDS.update(dining=bg_dining)
world.PROPS.update(whipcan=prop_whipcan, pie=prop_pie, cookiejar=prop_cookiejar, cookie=prop_cookie, tunacan=prop_tunacan,
                   scale=prop_scale, yogamat=prop_yogamat)

# ============================== FX ==============================

def fx_cream(ctx, t, p):
    """Whipped-cream blob (beard / helmet). amount 0..1 grows it; w,h set its full size."""
    a = p.get('amount', 1.0)
    if a <= 0.01: return
    w = p.get('w', 220) * a; h = p.get('h', 120) * a
    rnd = random.Random(p.get('seed', 5))
    pts = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1)) for _ in range(22)]
    pts = [(u, v) for (u, v) in pts if u * u + v * v <= 1]
    circ = [(u * w * 0.72, v * h * 0.66, (w + h) * 0.2 * (0.85 + 0.15 * math.sin(t * 3 + u * 5))) for (u, v) in pts]
    for x, y, r in circ:  # outline pass, then fill pass = one merged fluffy silhouette
        ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.set_line_width(14); ctx.stroke()
    for x, y, r in circ:
        ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFFDF5')); ctx.fill()
    for x, y, r in circ[:7]:  # soft shading swirls
        ctx.arc(x + r * 0.15, y + r * 0.2, r * 0.55, 0.2, 2.2); ctx.set_source_rgba(*hexc('#E9E1D0')); ctx.set_line_width(5); ctx.stroke()


def fx_ring(ctx, t, p):
    """Red 'found it' circle drawn on (draw 0..1)."""
    d = clamp(p.get('draw', 1.0))
    if d <= 0: return
    r = p.get('r', 90)
    ctx.save(); ctx.scale(1, p.get('sy', 1.0))
    ctx.arc(0, 0, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * d)
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(22); ctx.stroke_preserve()
    ctx.set_source_rgba(*hexc(p.get('color', '#FF2D2D'))); ctx.set_line_width(13); ctx.stroke()
    ctx.restore()
    if p.get('label') and d >= 1:
        text(ctx, p['label'], r * 0.75, -r * 0.85, 60, hexc('#FFE14D'), sw=12)


def fx_caption(ctx, t, p):
    """Subtitle box (bottom-of-frame style). top: small grey 'heard' line; text: big white translation."""
    a = p.get('alpha', 1.0)
    if a <= 0.01: return
    msg = p.get('text', ''); top = p.get('top', '')
    ctx.save(); ctx.push_group()
    lines = msg.split('\n'); n = len(lines) + (1 if top else 0)
    h = 70 + 78 * len(lines) + (60 if top else 0); w = p.get('w', 920)
    rrect(ctx, -w / 2, -h / 2, w, h, 26); ctx.set_source_rgba(0.05, 0.05, 0.08, 0.82); ctx.fill()
    y = -h / 2 + 50
    if top:
        text(ctx, top, 0, y, 44, hexc('#BFC4D0'), ink=hexc('#111111'), sw=4); y += 64
    for ln in lines:
        text(ctx, ln, 0, y + 14, p.get('size', 66), hexc(p.get('fill', '#FFFFFF')), ink=hexc('#111111'), sw=6); y += 78
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()


def fx_timerbar(ctx, t, p):
    """Countdown bar. left 0..1 = remaining; label (e.g. seconds) drawn at the left."""
    w = p.get('w', 820); left = clamp(p.get('left', 1.0))
    rrect(ctx, -w / 2, -26, w, 52, 26); fill_stroke(ctx, hexc('#FFFFFF'), 7)
    if left > 0.01:
        col = '#4CD964' if left > 0.5 else ('#FFCC00' if left > 0.25 else '#FF3B30')
        rrect(ctx, -w / 2 + 6, -20, (w - 12) * left, 40, 20); ctx.set_source_rgba(*hexc(col)); ctx.fill()
    if p.get('label') is not None:
        ctx.arc(-w / 2 - 10, 0, 62, 0, 2 * math.pi); fill_stroke(ctx, hexc('#FF3B30'), 8)
        text(ctx, str(p['label']), -w / 2 - 10, 4, 66, hexc('#FFFFFF'), sw=8)


def fx_tag(ctx, t, p):
    """Panel label pill, e.g. EXPECTATION / REALITY."""
    msg = p.get('text', '')
    w = p.get('w', 30 + 34 * len(msg))
    rrect(ctx, -w / 2, -42, w, 84, 42); fill_stroke(ctx, hexc(p.get('color', '#111111')), 7)
    text(ctx, msg, 0, 2, p.get('size', 54), hexc(p.get('fill', '#FFFFFF')), sw=6)


world.FX.update(cream=fx_cream, ring=fx_ring, caption=fx_caption, timerbar=fx_timerbar, tag=fx_tag)
SELF_ALPHA = {'caption'}


def fx_ownerhand(ctx, t, p):
    """The OWNER's hand (solid skin colour with a sleeve), unlike the viewer's translucent 'hand'. Same poses/origin as hand."""
    world._draw_hand(ctx, p.get('pose', 'palm'), hexc(p.get('skin', '#F2C7A0')), hexc('#3A2216'), 7)
    rrect(ctx, -135, 330, 270, 900, 30); fill_stroke(ctx, hexc(p.get('sleeve', '#5A79C2')), 9)


world.FX.update(ownerhand=fx_ownerhand)
