"""Nugget — the AIVOOMA cat. Drawn in local coordinates: body centre (0,0), head centre (0,-295) when sitting.
Size at scale 1: roughly 480 px wide, 700 px tall (sitting)."""
import math
import random
import cairo
from core import hexc, INK, OUTLINE_W, fill_stroke, ellipse, tri, lerp, clamp

ORANGE = hexc('#F7A24E'); ORANGE_D = hexc('#DC7B2C'); ORANGE_L = hexc('#FFC27E')
CREAM = hexc('#FFF2DE'); PINK = hexc('#FF94AA')

DEFAULTS = dict(pose='sit', eye='normal', look=[0.0, 0.3], lid=0.0, blink=None, mouth='smile', mk=0.0,
                green=0.0, blush=0.35, puff=0.0, ear=0.0, squish=0.0, tail=1.0, paw=None, paw2=None,
                inflate=0.0, sunglasses=False, wet=0.0, red=0.0, tongue=False, headtilt=0.0, run_speed=1.0)


def blob_path(ctx, cx, cy, rx, ry, puff, phase, tufts=0.0, spikes=13):
    n = 200
    for i in range(n + 1):
        th = 2 * math.pi * i / n
        c, sn = math.cos(th), math.sin(th)
        r = 1 / math.sqrt((c / rx) ** 2 + (sn / ry) ** 2)
        r += puff * 34 * tri(th * spikes / (2 * math.pi) + phase * 0.05) ** 1.6
        if tufts:
            w = max(0, math.cos(th - 0.42)) ** 16 + max(0, math.cos(th - (math.pi - 0.42))) ** 16
            r += tufts * w * 26 * tri(th * 32 / (2 * math.pi))
        (ctx.move_to if i == 0 else ctx.line_to)(cx + r * c, cy + r * sn)
    ctx.close_path()


# ---------------- face parts ----------------
def _ear(ctx, hx, hy, side, R, flat, puff):
    base_ang = -math.pi / 2 + side * (0.62 + 0.38 * flat)
    tip_len = R * (1.42 - 0.22 * flat) + 18 * puff
    spread = 0.42
    b1 = (hx + R * 0.92 * math.cos(base_ang - spread), hy + R * 0.92 * math.sin(base_ang - spread))
    b2 = (hx + R * 0.92 * math.cos(base_ang + spread), hy + R * 0.92 * math.sin(base_ang + spread))
    tip = (hx + tip_len * math.cos(base_ang), hy + tip_len * math.sin(base_ang))
    ctx.move_to(*b1); ctx.line_to(*tip); ctx.line_to(*b2); ctx.close_path()
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    fill_stroke(ctx, ORANGE)
    def l2(p, q, k): return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
    ib1 = l2(l2(b1, tip, 0.18), (hx, hy), 0.08); ib2 = l2(l2(b2, tip, 0.18), (hx, hy), 0.08)
    itip = l2(tip, (hx, hy), 0.22)
    ctx.move_to(*ib1); ctx.line_to(*itip); ctx.line_to(*ib2); ctx.close_path()
    ctx.set_source_rgba(*PINK); ctx.fill()


def _heart(ctx, x, y, s):
    ctx.move_to(x, y + s * 0.9)
    ctx.curve_to(x - s * 1.6, y - s * 0.2, x - s * 0.8, y - s * 1.4, x, y - s * 0.5)
    ctx.curve_to(x + s * 0.8, y - s * 1.4, x + s * 1.6, y - s * 0.2, x, y + s * 0.9)
    ctx.close_path()


def _eye(ctx, ex, ey, side, p, t, blink):
    mode = p['eye']; lx, ly = p['look']
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if mode == 'happy':
        ctx.move_to(ex - 36, ey + 10); ctx.curve_to(ex - 20, ey - 26, ex + 20, ey - 26, ex + 36, ey + 10)
        ctx.set_source_rgba(*INK); ctx.set_line_width(12); ctx.stroke(); return
    if mode == 'closed':
        ctx.move_to(ex - 36, ey); ctx.curve_to(ex - 20, ey + 22, ex + 20, ey + 22, ex + 36, ey)
        ctx.set_source_rgba(*INK); ctx.set_line_width(11); ctx.stroke(); return
    if mode == 'squeeze':
        d = 1 if side < 0 else -1; j = math.sin(t * 50 + side) * 3
        ctx.move_to(ex - 34 * d, ey - 30 + j); ctx.line_to(ex + 26 * d, ey + j); ctx.line_to(ex - 34 * d, ey + 30 + j)
        ctx.set_source_rgba(*INK); ctx.set_line_width(14); ctx.stroke(); return
    if mode == 'heart':
        pulse = 1 + 0.12 * math.sin(t * 12)
        _heart(ctx, ex, ey, 34 * pulse); fill_stroke(ctx, hexc('#FF4F7B'), 7)
        return
    if mode == 'dizzy':
        ctx.set_source_rgba(*INK); ctx.set_line_width(8)
        a0 = t * 9 * side
        for i in range(60):
            a = a0 + i * 0.32; r = 4 + i * 0.75
            (ctx.move_to if i == 0 else ctx.line_to)(ex + r * math.cos(a), ey + r * math.sin(a))
        ctx.stroke(); return
    if mode == 'wide':
        rx = ry = 82; pr = 12; po = (math.sin(t * 70) * 3, math.cos(t * 63) * 3)
    elif mode == 'big':  # cute sparkly puppy eyes
        rx, ry = 58, 70; pr = 44; po = (lx * 8, ly * 8)
    else:
        rx, ry = 52, 64; pr = 31; po = (lx * 16, ly * 18)
    ry_eff = ry * (1 - blink * 0.94)
    ellipse(ctx, ex, ey, rx, ry_eff); fill_stroke(ctx, hexc('#FFFFFF'), 8)
    if blink < 0.85:
        ctx.save(); ellipse(ctx, ex, ey, rx - 4, max(1, ry_eff - 4)); ctx.clip()
        px, py = ex + po[0], ey + po[1]
        ellipse(ctx, px, py, pr, pr * (1.18 if mode != 'wide' else 1.0))
        ctx.set_source_rgba(*hexc('#2B1A10')); ctx.fill()
        if mode != 'wide':
            ctx.set_source_rgba(1, 1, 1, 1)
            ctx.arc(px - pr * 0.3, py - pr * 0.48, pr * 0.32, 0, 2 * math.pi); ctx.fill()
            ctx.arc(px + pr * 0.3, py + pr * 0.32, pr * 0.15, 0, 2 * math.pi); ctx.fill()
            if mode == 'big':
                ctx.arc(px + pr * 0.42, py - pr * 0.1, pr * 0.1, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    lid = p['lid']
    if lid > 0.01 and mode in ('normal', 'big'):
        ctx.save(); ellipse(ctx, ex, ey, rx, ry_eff); ctx.clip()
        yl = ey - ry + 2 * ry * lid
        ctx.rectangle(ex - rx - 10, ey - ry - 10, 2 * rx + 20, yl - (ey - ry - 10))
        ctx.set_source_rgba(*ORANGE); ctx.fill(); ctx.restore()
        half = math.sqrt(max(0, 1 - ((yl - ey) / ry) ** 2)) * rx
        ctx.move_to(ex - half - 4, yl); ctx.line_to(ex + half + 4, yl)
        ctx.set_source_rgba(*INK); ctx.set_line_width(9); ctx.stroke()


def _mouth(ctx, hx, hy, p, t):
    m, k = p['mouth'], p['mk']
    nx, ny = hx, hy + 62
    ctx.set_source_rgba(*INK); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if m in ('smile', 'chew', 'line', 'frown'):
        bob = math.sin(t * 2 * math.pi * 1.6) * 7 if m == 'chew' else 0
        if m == 'line':
            ctx.move_to(nx - 26, ny + 22); ctx.line_to(nx + 26, ny + 22); ctx.set_line_width(8); ctx.stroke(); return
        if m == 'frown':
            ctx.move_to(nx - 34, ny + 34); ctx.curve_to(nx - 20, ny + 14, nx + 20, ny + 14, nx + 34, ny + 34)
            ctx.set_line_width(8); ctx.stroke(); return
        ctx.move_to(nx, ny + 8); ctx.line_to(nx, ny + 18 + bob)
        ctx.move_to(nx, ny + 18 + bob); ctx.curve_to(nx - 6, ny + 40 + bob, nx - 30, ny + 40 + bob, nx - 38, ny + 22)
        ctx.move_to(nx, ny + 18 + bob); ctx.curve_to(nx + 6, ny + 40 + bob, nx + 30, ny + 40 + bob, nx + 38, ny + 22)
        ctx.set_line_width(8); ctx.stroke()
        if p.get('tongue'):
            ctx.save(); ctx.translate(nx + 10, ny + 40 + bob); ctx.scale(0.75, 1)
            ctx.arc(0, 0, 18, 0, math.pi); ctx.restore(); fill_stroke(ctx, PINK, 5)
        if m == 'chew':
            b = 0.5 + 0.5 * math.sin(t * 2 * math.pi * 1.6)
            ctx.set_source_rgba(*ORANGE_L)
            for sx in (-1, 1):
                ctx.arc(nx + sx * 72, ny + 22, 24 + 9 * b, 0, 2 * math.pi); ctx.fill()
    elif m in ('open', 'pant', 'scream'):
        kk = 1.5 if m == 'scream' else 1.0
        rx, ry = 46 * max(k, 0.12) * kk, 58 * max(k, 0.12) * kk
        cy = ny + 22 + ry * 0.75
        ellipse(ctx, nx, cy, rx, ry); fill_stroke(ctx, hexc('#7A1F2B'), 8)
        ctx.save(); ellipse(ctx, nx, cy, rx - 3, ry - 3); ctx.clip()
        ctx.arc(nx, cy + ry * (0.55 if m != 'pant' else 0.35), rx * 0.8, 0, 2 * math.pi)
        ctx.set_source_rgba(*PINK); ctx.fill(); ctx.restore()
        if m == 'pant':
            ctx.save(); ctx.translate(nx + 8, cy + ry * 0.9); ctx.scale(0.8, 1)
            ctx.arc(0, 0, 26, 0, math.pi); ctx.restore(); fill_stroke(ctx, PINK, 6)
        ctx.move_to(nx, ny + 8); ctx.line_to(nx, cy - ry)
        ctx.set_source_rgba(*INK); ctx.set_line_width(8); ctx.stroke()
    elif m == 'pucker':
        j = math.sin(t * 47) * 2.5; cx, cy = nx + j, ny + 38
        ctx.arc(cx, cy, 15, 0, 2 * math.pi); fill_stroke(ctx, hexc('#7A1F2B'), 8)
        ctx.set_source_rgba(*INK); ctx.set_line_width(6)
        for i in range(8):
            a = 2 * math.pi * i / 8 + 0.2
            ctx.move_to(cx + 24 * math.cos(a), cy + 24 * math.sin(a)); ctx.line_to(cx + 36 * math.cos(a), cy + 36 * math.sin(a))
        ctx.stroke()
    elif m == 'o':
        ellipse(ctx, nx, ny + 40, 16, 20); fill_stroke(ctx, hexc('#7A1F2B'), 7)


def draw_head(ctx, hx, hy, p, t, blink):
    sq = p['squish']
    rx, ry = 236 * (1 - 0.05 * sq), 206 * (1 + 0.05 * sq)
    R = (rx + ry) / 2
    phase = t * 9
    for side in (-1, 1):
        _ear(ctx, hx, hy, side, R, max(-0.3, p['ear']), p['puff'])
    blob_path(ctx, hx, hy, rx, ry, p['puff'], phase, tufts=1.0)
    fill_stroke(ctx, ORANGE)
    ctx.save(); blob_path(ctx, hx, hy, rx, ry, p['puff'], phase, tufts=1.0); ctx.clip()
    ellipse(ctx, hx, hy + 85, 1.35 * 92, 0.9 * 92); ctx.set_source_rgba(*CREAM); ctx.fill()
    ctx.set_source_rgba(*ORANGE_D); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx, l in ((-46, 62), (0, 82), (46, 62)):
        ctx.move_to(hx + dx, hy - ry - 10); ctx.line_to(hx + dx * 0.85, hy - ry + l); ctx.set_line_width(20); ctx.stroke()
    for col, amt, top in (('#7CC544', p['green'], True), ('#FF5A4E', p['red'], True)):
        if amt > 0:
            gg = cairo.LinearGradient(0, hy - ry, 0, hy + ry)
            c = hexc(col)
            gg.add_color_stop_rgba(0, c[0], c[1], c[2], 0.9 * amt)
            gg.add_color_stop_rgba(0.75, c[0], c[1], c[2], 0.5 * amt)
            gg.add_color_stop_rgba(1, c[0], c[1], c[2], 0.0)
            ctx.rectangle(hx - 400, hy - 400, 800, 800); ctx.set_source(gg); ctx.fill()
    ctx.restore()
    bl = p['blush'] * (1 - clamp(p['green'] / 0.4))
    if bl > 0.01:
        ctx.set_source_rgba(*hexc('#FF7F98', bl))
        for sx in (-1, 1):
            ellipse(ctx, hx + sx * 140, hy + 58, 34, 21); ctx.fill()
    for side in (-1, 1):
        _eye(ctx, hx + side * 88, hy - 12, side, p, t, blink)
    if p['eye'] in ('squeeze',) or p.get('angry'):
        ctx.set_source_rgba(*INK); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for side in (-1, 1):
            ctx.move_to(hx + side * 130, hy - 92); ctx.line_to(hx + side * 52, hy - 66); ctx.stroke()
    if p['sunglasses']:
        ctx.set_source_rgba(*hexc('#15151A'))
        for side in (-1, 1):
            ctx.save(); ctx.translate(hx + side * 88, hy - 14)
            ctx.move_to(-66, -36); ctx.line_to(66, -36); ctx.line_to(56, 22); ctx.curve_to(40, 50, -40, 50, -56, 22)
            ctx.close_path(); ctx.restore(); ctx.fill()
        ctx.rectangle(hx - 40, hy - 52, 80, 12); ctx.fill()
        ctx.set_source_rgba(1, 1, 1, 0.55)
        for side in (-1, 1):
            ctx.move_to(hx + side * 88 - 40, hy - 36); ctx.line_to(hx + side * 88 - 10, hy - 36)
            ctx.set_line_width(7); ctx.stroke()
    nx, ny = hx, hy + 52
    ctx.move_to(nx - 20, ny - 8); ctx.curve_to(nx - 20, ny - 16, nx + 20, ny - 16, nx + 20, ny - 8)
    ctx.curve_to(nx + 16, ny + 4, nx + 4, ny + 12, nx, ny + 12); ctx.curve_to(nx - 4, ny + 12, nx - 16, ny + 4, nx - 20, ny - 8)
    ctx.close_path(); fill_stroke(ctx, PINK, 6)
    _mouth(ctx, hx, hy, p, t)
    droop = 26 * sq
    ctx.set_source_rgba(*INK); ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for side in (-1, 1):
        for i in range(3):
            y0 = hy + 66 + i * 16; j = math.sin(t * 40 + i) * 4 * p['puff']
            ctx.move_to(hx + side * 112, y0)
            ctx.curve_to(hx + side * 170, y0 - 14 + i * 8 + droop * 0.5, hx + side * 210, y0 - 8 + i * 14 + droop + j,
                         hx + side * 250, y0 - 2 + i * 22 + droop + j)
            ctx.stroke()
    if p['wet'] > 0:
        rnd = random.Random(3)
        for i in range(6):
            x = hx + rnd.uniform(-200, 200); y0 = hy - 120 + rnd.uniform(-40, 120)
            ph = (t * 1.6 + rnd.random()) % 1.0
            y = y0 + 160 * ph
            ctx.save(); ctx.translate(x, y)
            ctx.move_to(0, -18); ctx.curve_to(9, -3, 12, 7, 0, 11); ctx.curve_to(-12, 7, -9, -3, 0, -18)
            ctx.restore(); ctx.set_source_rgba(*hexc('#8FD3FF', p['wet'] * math.sin(math.pi * ph))); ctx.fill()


def _limb(ctx, a, b, w):
    for ww, col in ((w + 18, INK), (w, ORANGE)):
        ctx.move_to(*a); ctx.line_to(*b)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(ww); ctx.set_source_rgba(*col); ctx.stroke()


def _paw(ctx, x, y, s=1.0):
    ellipse(ctx, x, y, 40 * s, 34 * s); fill_stroke(ctx, ORANGE_L)
    ctx.set_source_rgba(*INK); ctx.set_line_width(5)
    for dx in (-13, 13):
        ctx.move_to(x + dx * s, y - 30 * s); ctx.line_to(x + dx * s, y - 14 * s); ctx.stroke()


def _tail(ctx, pts, w, puff):
    for ww, col in ((w + 18 + 22 * puff, INK), (w + 22 * puff, ORANGE)):
        ctx.move_to(*pts[0]); ctx.curve_to(*pts[1], *pts[2], *pts[3])
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(ww); ctx.set_source_rgba(*col); ctx.stroke()
    ctx.arc(pts[3][0], pts[3][1], (w + 22 * puff) / 2 - 2, 0, 2 * math.pi); ctx.set_source_rgba(*ORANGE_D); ctx.fill()


def auto_blink(p, t):
    if p.get('blink') is not None:
        return p['blink']
    if p['eye'] not in ('normal', 'big') or p['lid'] > 0.4:
        return 0.0
    ph = (t + 0.7) % 3.4
    return tri(ph / 0.3 * 0.5) if ph < 0.3 else 0.0


def draw(ctx, t, p):
    """p: merged params (DEFAULTS + current track values) incl. x, y, scale, rot, flip."""
    q = dict(DEFAULTS); q.update({k: v for k, v in p.items() if v is not None or k in ('paw', 'paw2', 'blink')})
    p = q
    blink = auto_blink(p, t)
    ctx.save()
    ctx.translate(p.get('x', 540), p.get('y', 1255))
    ctx.rotate(p.get('rot', 0.0))
    s = p.get('scale', 1.0)
    ctx.scale(s * p.get('flip', 1), s)
    pose = p['pose']; puff = p['puff']; phase = t * 9
    infl = p['inflate']
    if pose == 'sit':
        breathe = math.sin(t * 2.6) * 4
        wig = math.sin(t * 3.2) * 30 * p['tail'] + puff * math.sin(t * 40) * 12
        _tail(ctx, [(150, 130), (300, 120), (330 + wig, -40), (260 + wig * 1.5, -150)], 44, puff)
        ellipse(ctx, 0, 170, 220 * (1 + infl * 0.5), 55); ctx.set_source_rgba(0, 0, 0, 0.13); ctx.fill()
        brx, bry = 200 * (1 + infl), (172 + breathe) * (1 + infl * 0.9)
        blob_path(ctx, 0, -infl * 120, brx, bry, puff * 0.8, phase + 3, spikes=15); fill_stroke(ctx, ORANGE)
        ctx.save(); blob_path(ctx, 0, -infl * 120, brx, bry, puff * 0.8, phase + 3, spikes=15); ctx.clip()
        ctx.set_source_rgba(*ORANGE_D); ctx.set_line_width(16)
        for dy in (-60, 0, 60):
            for sx in (-1, 1):
                ctx.move_to(sx * (brx + 10), dy - infl * 120)
                ctx.curve_to(sx * (brx - 30), dy - 12 - infl * 120, sx * (brx - 50), dy + 8 - infl * 120, sx * (brx - 70), dy - infl * 120)
                ctx.stroke()
        ctx.restore()
        ellipse(ctx, 0, 35 - infl * 120, 112 * (1 + infl), 118 * (1 + infl)); ctx.set_source_rgba(*CREAM); ctx.fill()
        if p['paw2'] is None:
            ctx.save(); ctx.translate(-88, 155); ctx.scale(1, 0.62); ctx.arc(0, 0, 58, 0, 2 * math.pi); ctx.restore()
            fill_stroke(ctx, ORANGE_L)
        if p['paw'] is None:
            ctx.save(); ctx.translate(90, 155); ctx.scale(1, 0.62); ctx.arc(0, 0, 58, 0, 2 * math.pi); ctx.restore()
            fill_stroke(ctx, ORANGE_L)
        hx, hy = 0 + p['headtilt'] * 20, -295 - infl * 200
        ctx.save(); ctx.translate(hx, hy); ctx.rotate(p['headtilt'] * 0.25); ctx.translate(-hx, -hy)
        draw_head(ctx, hx, hy, p, t, blink)
        ctx.restore()
        for key, sh in (('paw', (120, 40)), ('paw2', (-120, 40))):
            if p[key] is not None:
                px, py = p[key]
                _limb(ctx, sh, (px, py), 52); _paw(ctx, px, py)
    elif pose == 'loaf':
        breathe = math.sin(t * 2.0) * 3
        ellipse(ctx, 0, 175, 250, 45); ctx.set_source_rgba(0, 0, 0, 0.13); ctx.fill()
        _tail(ctx, [(200, 120), (260, 170), (60, 200), (-150, 175)], 40, puff)
        blob_path(ctx, 0, 70, 240, 120 + breathe, puff * 0.8, phase + 3, spikes=15); fill_stroke(ctx, ORANGE)
        ctx.save(); blob_path(ctx, 0, 70, 240, 120 + breathe, puff * 0.8, phase + 3, spikes=15); ctx.clip()
        ctx.set_source_rgba(*ORANGE_D); ctx.set_line_width(16)
        for dx in (-150, -90, 90, 150):
            ctx.move_to(dx, -60); ctx.line_to(dx * 0.95, 20); ctx.stroke()
        ctx.restore()
        for sx in (-70, 70):
            ellipse(ctx, sx, 172, 46, 22); fill_stroke(ctx, ORANGE_L, 7)
        draw_head(ctx, 0, -150, p, t, blink)
    elif pose == 'run':
        sp = p['run_speed']; ph = t * 14 * sp
        ellipse(ctx, 0, 190, 240, 40); ctx.set_source_rgba(0, 0, 0, 0.13); ctx.fill()
        wig = math.sin(t * 20) * 25
        _tail(ctx, [(-200, 20), (-300, -10), (-360, -90 + wig), (-420, -150 + wig)], 40, puff)
        legs = [(-140, 0.0), (-70, 0.5), (90, 0.25), (160, 0.75)]
        for i, (lx, off) in enumerate(legs):
            a = math.sin(ph + off * 2 * math.pi)
            top = (lx, 80); foot = (lx + 55 * a, 170 - 20 * max(0, -math.cos(ph + off * 2 * math.pi)))
            _limb(ctx, top, foot, 46); _paw(ctx, foot[0], foot[1], 0.8)
        blob_path(ctx, 0, 40, 235, 135, puff * 0.8, phase + 3, spikes=15); fill_stroke(ctx, ORANGE)
        ctx.save(); blob_path(ctx, 0, 40, 235, 135, puff * 0.8, phase + 3, spikes=15); ctx.clip()
        ctx.set_source_rgba(*ORANGE_D); ctx.set_line_width(16)
        for dx in (-140, -70, 0):
            ctx.move_to(dx, -100); ctx.line_to(dx - 10, -20); ctx.stroke()
        ellipse(ctx, 40, 110, 150, 60); ctx.set_source_rgba(*CREAM); ctx.fill()
        ctx.restore()
        ctx.save(); ctx.translate(190, -150); ctx.scale(0.9, 0.9)
        draw_head(ctx, 0, 0, p, t, blink); ctx.restore()
    ctx.restore()
