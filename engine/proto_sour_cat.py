"""Sour Cat — 10s cartoon Short (1080x1920, 30fps), drawn with cairo.
Usage:
  python3 render.py frames 0.5 3.2 4.6 ...   -> PNG keyframes into out/
  python3 render.py video                    -> out/sour_cat_silent.mp4
"""
import cairo, math, sys, os, subprocess, random

W, H, FPS, DUR = 1080, 1920, 30, 10.0
N = int(FPS * DUR)
FONT = "Luckiest Guy"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


# ---------- helpers ----------
def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= b)
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def ein(x): x = clamp(x); return x * x
def back(x):
    x = clamp(x); c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, k): return a + (b - a) * k
def lerp2(p, q, k): return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
def tri(x):  # triangle wave 0..1, period 1
    return 1 - abs((x % 1.0) * 2 - 1)

ORANGE = hexc('#F7A24E'); ORANGE_D = hexc('#DC7B2C'); ORANGE_L = hexc('#FFC27E')
CREAM = hexc('#FFF2DE'); PINK = hexc('#FF94AA'); INK = hexc('#3A2216')
LEMON = hexc('#FFD43B'); LEMON_IN = hexc('#FFF4A3'); LEMON_RIND = hexc('#F2B705')
OUTLINE_W = 9


def fill_stroke(ctx, fill, lw=OUTLINE_W, ink=INK):
    ctx.set_source_rgba(*fill); ctx.fill_preserve()
    ctx.set_source_rgba(*ink); ctx.set_line_width(lw); ctx.stroke()


# ---------- timeline ----------
CAT = (470, 1255)           # body centre
HEAD = (470, 960)           # head centre (before lean)
PAW_REST = (560, 1410)
PLATE = (775, 1500)
SLICE_PLATE = (760, 1478)
HOLD = (600, 1150)
BITE_POS = (528, 1080)


def state(t):
    s = dict(lean=(0, 0), look=(0.65, 0.55), blink=0.0, eye='normal', lid=0.0,
             mouth='smile', mk=0.0, green=0.0, puff=0.0, phase=t * 9.0, shake=0.0,
             ear=0.0, paw=None, slice=None, zoom=1.17 + 0.035 * ease(seg(t, 0, 4)),
             burst=0.0, sun=0.0, sweat=0.0, squish=0.0, chew=0.0, sniff=[],
             juice=None, speed=0.0)

    # A: idle, blink
    s['blink'] = max(tri(seg(t, 0.52, 0.70) * 0.5 + 0.0) if 0.52 < t < 0.70 else 0,
                     tri(seg(t, 9.62, 9.78) * 0.5) if 9.62 < t < 9.78 else 0)

    # B: lean and sniff
    k = ease(seg(t, 1.0, 1.4)) * (1 - ease(seg(t, 2.45, 2.95)))
    s['lean'] = (34 * k, 20 * k)
    for st in (1.15, 1.42, 1.69):
        if st <= t < st + 0.32:
            s['sniff'].append(seg(t, st, st + 0.32))

    # C: grab slice and lift to mouth
    sl = dict(pos=SLICE_PLATE, rot=0.0, flat=0.42, bitten=False, scale=1.0)
    if t < 2.0:
        pass
    elif t < 2.5:
        k = ease(seg(t, 2.0, 2.5))
        s['paw'] = lerp2(PAW_REST, (SLICE_PLATE[0] - 10, SLICE_PLATE[1] + 18), k)
    elif t < 2.95:
        k = ease(seg(t, 2.5, 2.95))
        sl['pos'] = lerp2(SLICE_PLATE, HOLD, k)
        sl['flat'] = lerp(0.42, 1.0, k)
        sl['rot'] = lerp(0, -0.25, k)
        s['paw'] = (sl['pos'][0] - 6, sl['pos'][1] + 52 * sl['flat'])
        s['look'] = lerp2((0.65, 0.55), (0.45, 0.75), k)
    elif t < 3.12:  # open mouth, move slice in
        k = ease(seg(t, 2.95, 3.12))
        sl['pos'] = lerp2(HOLD, BITE_POS, k); sl['flat'] = 1.0; sl['rot'] = -0.25
        s['paw'] = (sl['pos'][0] - 6, sl['pos'][1] + 52)
        s['mouth'] = 'open'; s['mk'] = eout(seg(t, 2.95, 3.08))
        s['look'] = (0.3, 0.85)
    elif t < 7.0:
        sl['bitten'] = True; sl['flat'] = 1.0
        k = ease(seg(t, 3.12, 3.4))
        sl['pos'] = lerp2(BITE_POS, HOLD, k); sl['rot'] = -0.25
        if t > 4.12:  # trembling paw
            j = 7 * ease(seg(t, 4.12, 4.3))
            sl['pos'] = (HOLD[0] + j * math.sin(t * 61), HOLD[1] + j * math.cos(t * 53))
        s['paw'] = (sl['pos'][0] - 6, sl['pos'][1] + 52)
    else:  # throw
        sl['bitten'] = True; sl['flat'] = 1.0
        k = seg(t, 7.0, 7.5)
        start = HOLD; end = (1300, 180)
        p = lerp2(start, end, ein(k))
        p = (p[0], p[1] - 260 * math.sin(math.pi * k))
        sl['pos'] = p; sl['rot'] = -0.25 + 14 * ein(k); sl['scale'] = lerp(1, 0.7, k)
        s['speed'] = 1.0 if 7.02 < t < 7.5 else 0.0
        pk = seg(t, 7.0, 7.12); pb = ease(seg(t, 7.15, 7.75))
        flick = lerp2(HOLD, (700, 1010), eout(pk))
        s['paw'] = lerp2((flick[0] - 6, flick[1] + 52), PAW_REST, pb) if t < 7.75 else None
        if t >= 7.5: sl = None
    s['slice'] = sl

    # D: chomp + juice
    if 3.12 <= t < 3.2:
        s['mouth'] = 'open'; s['mk'] = 1 - seg(t, 3.12, 3.2)
    if 3.12 <= t < 3.75:
        s['juice'] = seg(t, 3.12, 3.75)
    # E: happy chewing
    if 3.2 <= t < 4.0:
        s['eye'] = 'happy'; s['mouth'] = 'chew'; s['chew'] = (t - 3.2) * 9.5
    # F: realisation
    if 4.0 <= t < 4.12:
        s['eye'] = 'normal'; s['look'] = (0, 0); s['mouth'] = 'line'
    if 4.12 <= t < 4.45:
        s['eye'] = 'wide'; s['mouth'] = 'open'; s['mk'] = 0.55
        s['puff'] = eout(seg(t, 4.12, 4.25)); s['ear'] = -0.25
        s['burst'] = 1 - seg(t, 4.3, 4.6)
    if t >= 4.12:
        s['zoom'] = 1.205 + lerp(0, 0.2, eout(seg(t, 4.12, 4.22))) \
                    - 0.09 * ease(seg(t, 4.3, 6.9)) - 0.145 * ease(seg(t, 7.4, 8.4))
        s['shake'] = 11 * (1 - 0.4 * seg(t, 4.5, 7.0)) * (1 - ease(seg(t, 7.3, 8.2)))
    if 4.3 <= t < 4.6:
        s['burst'] = max(s['burst'], 1 - seg(t, 4.3, 4.6))
    # G: SOUR face
    if 4.45 <= t < 7.4:
        s['eye'] = 'squeeze'; s['mouth'] = 'pucker'
        s['puff'] = 1.0; s['ear'] = ease(seg(t, 4.45, 4.7)); s['squish'] = ease(seg(t, 4.45, 4.6))
        s['sweat'] = seg(t, 4.7, 7.2)
    if t >= 4.45:
        s['green'] = 0.9 * ease(seg(t, 4.45, 5.3)) * (1 - ease(seg(t, 7.6, 8.9)))
        s['sun'] = ease(seg(t, 4.2, 4.5)) * (1 - ease(seg(t, 7.2, 7.8)))
    # I: recover, deadpan
    if t >= 7.4:
        s['eye'] = 'normal'; s['lid'] = 0.52 * (1 - ease(seg(t, 9.45, 9.95)))
        s['look'] = lerp2((0, 0.15), (0.65, 0.55), ease(seg(t, 8.9, 9.6)))
        s['puff'] = 1 - ease(seg(t, 7.4, 8.2))
        s['ear'] = lerp(1.0, 0.0, ease(seg(t, 7.6, 9.4)))
        s['squish'] = 1 - ease(seg(t, 7.4, 7.8))
        if t < 8.7:
            s['mouth'] = 'pant'; s['mk'] = 0.42 + 0.06 * math.sin(t * 18)
        else:
            s['mouth'] = 'smile'
    return s


# ---------- drawing: scene ----------
def draw_bg(ctx, t, s):
    g = cairo.LinearGradient(0, 0, 0, 1350)
    g.add_color_stop_rgba(0, *hexc('#BFE6F2')); g.add_color_stop_rgba(1, *hexc('#E5F5EA'))
    ctx.rectangle(-400, -400, W + 800, 1740); ctx.set_source(g); ctx.fill()
    # wallpaper dots
    ctx.set_source_rgba(1, 1, 1, 0.45)
    for row in range(-3, 18):
        for col in range(-3, 14):
            x = col * 110 + (55 if row % 2 else 0); y = row * 95
            if y > 1300: continue
            ctx.arc(x, y, 10, 0, 2 * math.pi); ctx.fill()
    # window
    ctx.save(); ctx.translate(150, 300)
    ctx.rectangle(-150, 0, 330, 420); fill_stroke(ctx, hexc('#FFFFFF'), 12, hexc('#8FB9C9'))
    sky = cairo.LinearGradient(0, 0, 0, 420)
    sky.add_color_stop_rgba(0, *hexc('#7CCBF5')); sky.add_color_stop_rgba(1, *hexc('#CDEFFF'))
    ctx.rectangle(-132, 18, 294, 384); ctx.set_source(sky); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.9)
    for cx, cy, r in ((-60, 120, 34), (-25, 108, 44), (15, 124, 30), (70, 250, 26), (100, 242, 34)):
        ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgba(*hexc('#8FB9C9')); ctx.set_line_width(12)
    ctx.move_to(15, 18); ctx.line_to(15, 402); ctx.move_to(-132, 210); ctx.line_to(162, 210); ctx.stroke()
    ctx.restore()
    # shelf + plant on right
    ctx.rectangle(700, 520, 330, 26); fill_stroke(ctx, hexc('#B9835A'), 7, hexc('#7A4E2F'))
    ctx.save(); ctx.translate(870, 520)
    ctx.move_to(-55, 0); ctx.line_to(-42, -95); ctx.line_to(42, -95); ctx.line_to(55, 0); ctx.close_path()
    fill_stroke(ctx, hexc('#E9785A'), 7, hexc('#7A4E2F'))
    ctx.set_source_rgba(*hexc('#4FAE62'))
    for ang in (-1.2, -0.6, 0, 0.6, 1.2):
        ctx.save(); ctx.translate(0, -95); ctx.rotate(ang + 0.05 * math.sin(t * 2 + ang))
        ctx.scale(1, 2.6); ctx.arc(0, -28, 22, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    ctx.restore()
    # table top
    top = cairo.LinearGradient(0, 1320, 0, 1760)
    top.add_color_stop_rgba(0, *hexc('#E2A56E')); top.add_color_stop_rgba(1, *hexc('#CF8C55'))
    ctx.move_to(-400, 1330); ctx.line_to(W + 400, 1330); ctx.line_to(W + 400, 1760); ctx.line_to(-400, 1760)
    ctx.close_path(); ctx.set_source(top); ctx.fill()
    ctx.set_source_rgba(*hexc('#F3BE8A')); ctx.rectangle(-400, 1322, W + 800, 14); ctx.fill()
    ctx.set_source_rgba(0.55, 0.32, 0.16, 0.18); ctx.set_line_width(4)
    for i, y in enumerate((1420, 1530, 1650)):
        ctx.move_to(-400, y); ctx.curve_to(200, y - 12, 600, y + 14, W + 400, y - 4); ctx.stroke()
    ctx.rectangle(-400, 1760, W + 800, 600); ctx.set_source_rgba(*hexc('#A86A3B')); ctx.fill()
    ctx.set_source_rgba(*hexc('#8E5631')); ctx.rectangle(-400, 1760, W + 800, 16); ctx.fill()


def draw_sun(ctx, t, s, c):
    if s['sun'] <= 0: return
    ctx.save(); ctx.translate(*c); ctx.rotate(t * 0.9)
    n = 18
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = a0 + math.pi / n
        ctx.move_to(0, 0); ctx.arc(0, 0, 1700, a0, a1); ctx.close_path()
        ctx.set_source_rgba(*hexc('#FFF06A', 0.55 * s['sun'])); ctx.fill()
    rg = cairo.RadialGradient(0, 0, 0, 0, 0, 900)
    rg.add_color_stop_rgba(0, *hexc('#FFFDE0', 0.85 * s['sun'])); rg.add_color_stop_rgba(1, *hexc('#FFFDE0', 0))
    ctx.arc(0, 0, 900, 0, 2 * math.pi); ctx.set_source(rg); ctx.fill()
    ctx.restore()


def lemon_slice(ctx, x, y, r, flat=1.0, rot=0.0, bitten=False, scale=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(scale, scale * flat)
    if bitten:
        ctx.rectangle(-500, -500, 1000, 1000)
        for bx, by, br in ((-38, -46, 26), (-6, -63, 27), (27, -54, 24)):
            ctx.new_sub_path(); ctx.arc(bx, by, br, 0, 2 * math.pi)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); ctx.clip(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    ctx.arc(0, 0, r, 0, 2 * math.pi); fill_stroke(ctx, LEMON_RIND, OUTLINE_W / max(flat, 0.5))
    ctx.arc(0, 0, r * 0.86, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFF8CF')); ctx.fill()
    ctx.arc(0, 0, r * 0.78, 0, 2 * math.pi); ctx.set_source_rgba(*LEMON); ctx.fill()
    for i in range(9):  # segments
        a = 2 * math.pi * i / 9
        ctx.move_to(0, 0); ctx.line_to(r * 0.78 * math.cos(a), r * 0.78 * math.sin(a))
    ctx.set_source_rgba(*hexc('#FFF8CF')); ctx.set_line_width(6); ctx.stroke()
    ctx.arc(0, 0, r * 0.12, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFF8CF')); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.55)
    ctx.arc(-r * 0.35, -r * 0.4, r * 0.12, 0, 2 * math.pi); ctx.fill()
    ctx.restore()


def draw_plate(ctx, t, s):
    x, y = PLATE
    ctx.save(); ctx.translate(x, y + 18); ctx.scale(1, 0.36)
    ctx.arc(0, 0, 190, 0, 2 * math.pi); ctx.set_source_rgba(0, 0, 0, 0.15); ctx.fill(); ctx.restore()
    ctx.save(); ctx.translate(x, y); ctx.scale(1, 0.36)
    ctx.arc(0, 0, 185, 0, 2 * math.pi); ctx.restore(); fill_stroke(ctx, hexc('#FFFFFF'))
    ctx.save(); ctx.translate(x, y); ctx.scale(1, 0.36)
    ctx.arc(0, 0, 140, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(*hexc('#8CC8E8')); ctx.set_line_width(6); ctx.stroke()
    # two slices that stay
    lemon_slice(ctx, 695, 1492, 62, 0.42, 0.0)
    lemon_slice(ctx, 840, 1500, 62, 0.42, 0.0)


# ---------- drawing: cat ----------
def blob_path(ctx, cx, cy, rx, ry, puff, phase, tufts=0.0, spikes=13):
    n = 220
    for i in range(n + 1):
        th = 2 * math.pi * i / n
        c, sn = math.cos(th), math.sin(th)
        r = 1 / math.sqrt((c / rx) ** 2 + (sn / ry) ** 2)
        sp = tri(th * spikes / (2 * math.pi) + phase * 0.05)
        r += puff * 34 * sp ** 1.6
        if tufts:
            w = max(0, math.cos(th - 0.42)) ** 16 + max(0, math.cos(th - (math.pi - 0.42))) ** 16
            r += tufts * w * 26 * tri(th * 32 / (2 * math.pi))
        x, y = cx + r * c, cy + r * sn
        (ctx.move_to if i == 0 else ctx.line_to)(x, y)
    ctx.close_path()


def draw_tail(ctx, t, s):
    cx, cy = CAT
    wig = math.sin(t * 3.2) * 30 + s['puff'] * math.sin(t * 40) * 12
    pts = [(cx + 150, cy + 130), (cx + 300, cy + 120), (cx + 330 + wig, cy - 40), (cx + 260 + wig * 1.5, cy - 150)]
    for w, col in ((62 + 22 * s['puff'], INK), (44 + 22 * s['puff'], ORANGE)):
        ctx.move_to(*pts[0]); ctx.curve_to(*pts[1], *pts[2], *pts[3])
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(w); ctx.set_source_rgba(*col); ctx.stroke()
    # dark tip
    ctx.arc(pts[3][0], pts[3][1], 19 + 10 * s['puff'], 0, 2 * math.pi); ctx.set_source_rgba(*ORANGE_D); ctx.fill()


def draw_body(ctx, t, s):
    cx, cy = CAT
    breathe = math.sin(t * 2.6) * 4
    ctx.save(); ctx.translate(cx, cy + 170); ctx.scale(1, 0.25)
    ctx.arc(0, 0, 220, 0, 2 * math.pi); ctx.set_source_rgba(0, 0, 0, 0.15); ctx.fill(); ctx.restore()
    blob_path(ctx, cx, cy, 200, 172 + breathe, s['puff'] * 0.8, s['phase'] + 3, spikes=15)
    fill_stroke(ctx, ORANGE)
    ctx.save(); blob_path(ctx, cx, cy, 200, 172 + breathe, s['puff'] * 0.8, s['phase'] + 3, spikes=15); ctx.clip()
    ctx.set_source_rgba(*ORANGE_D)
    for i, dy in enumerate((-60, 0, 60)):  # side stripes
        ctx.move_to(cx - 210, cy + dy); ctx.curve_to(cx - 170, cy + dy - 12, cx - 150, cy + dy + 8, cx - 130, cy + dy)
        ctx.set_line_width(16); ctx.stroke()
        ctx.move_to(cx + 210, cy + dy); ctx.curve_to(cx + 170, cy + dy - 12, cx + 150, cy + dy + 8, cx + 130, cy + dy)
        ctx.stroke()
    ctx.restore()
    ctx.save(); ctx.translate(cx, cy + 35); ctx.scale(1, 1.05)
    ctx.arc(0, 0, 112, 0, 2 * math.pi); ctx.restore(); ctx.set_source_rgba(*CREAM); ctx.fill()
    # left paw (resting)
    ctx.save(); ctx.translate(cx - 88, cy + 155); ctx.scale(1, 0.62); ctx.arc(0, 0, 58, 0, 2 * math.pi)
    ctx.restore(); fill_stroke(ctx, ORANGE_L)
    if s['paw'] is None:
        ctx.save(); ctx.translate(PAW_REST[0], PAW_REST[1]); ctx.scale(1, 0.62); ctx.arc(0, 0, 58, 0, 2 * math.pi)
        ctx.restore(); fill_stroke(ctx, ORANGE_L)


def draw_arm(ctx, s):
    if s['paw'] is None: return
    cx, cy = CAT
    sh = (cx + 120, cy + 40); px, py = s['paw']
    mid = ((sh[0] + px) / 2 + 30, (sh[1] + py) / 2 + 30)
    for w, col in ((70, INK), (52, ORANGE)):
        ctx.move_to(*sh); ctx.curve_to(mid[0], mid[1], mid[0], mid[1], px, py)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(w); ctx.set_source_rgba(*col); ctx.stroke()
    ctx.save(); ctx.translate(px, py); ctx.scale(1, 0.85); ctx.arc(0, 0, 40, 0, 2 * math.pi); ctx.restore()
    fill_stroke(ctx, ORANGE_L)
    ctx.set_source_rgba(*INK); ctx.set_line_width(5)
    for dx in (-13, 13):
        ctx.move_to(px + dx, py - 30); ctx.line_to(px + dx, py - 14); ctx.stroke()


def ear(ctx, hx, hy, side, R, flat, puff):
    base_ang = -math.pi / 2 + side * (0.62 + 0.38 * flat)
    tip_len = R * (1.42 - 0.22 * flat) + 18 * puff
    spread = 0.42
    b1 = (hx + R * 0.92 * math.cos(base_ang - spread), hy + R * 0.92 * math.sin(base_ang - spread))
    b2 = (hx + R * 0.92 * math.cos(base_ang + spread), hy + R * 0.92 * math.sin(base_ang + spread))
    tip = (hx + tip_len * math.cos(base_ang), hy + tip_len * math.sin(base_ang))
    ctx.move_to(*b1); ctx.line_to(*tip); ctx.line_to(*b2); ctx.close_path()
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); fill_stroke(ctx, ORANGE)
    ib1 = lerp2(b1, tip, 0.18); ib2 = lerp2(b2, tip, 0.18)
    ib1 = lerp2(ib1, (hx, hy), 0.08); ib2 = lerp2(ib2, (hx, hy), 0.08)
    itip = lerp2(tip, (hx, hy), 0.22)
    ctx.move_to(*ib1); ctx.line_to(*itip); ctx.line_to(*ib2); ctx.close_path()
    ctx.set_source_rgba(*PINK); ctx.fill()


def eye(ctx, ex, ey, side, s, t):
    mode = s['eye']
    lx, ly = s['look']
    if mode == 'happy':
        ctx.move_to(ex - 36, ey + 10); ctx.curve_to(ex - 20, ey - 26, ex + 20, ey - 26, ex + 36, ey + 10)
        ctx.set_source_rgba(*INK); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        return
    if mode == 'squeeze':
        d = 1 if side < 0 else -1  # '>' on left, '<' on right
        j = math.sin(t * 50 + side) * 3
        ctx.move_to(ex - 34 * d, ey - 30 + j); ctx.line_to(ex + 26 * d, ey + j); ctx.line_to(ex - 34 * d, ey + 30 + j)
        ctx.set_source_rgba(*INK); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
        return
    if mode == 'wide':
        rx = ry = 82
        pr = 12; po = (math.sin(t * 70) * 3, math.cos(t * 63) * 3)
    else:
        rx, ry = 52, 64; pr = 31; po = (lx * 16, ly * 18)
    blink = s['blink']
    ry_eff = ry * (1 - blink * 0.94)
    ctx.save(); ctx.translate(ex, ey); ctx.scale(1, ry_eff / ry)
    ctx.arc(0, 0, rx, 0, 2 * math.pi); ctx.restore()
    fill_stroke(ctx, hexc('#FFFFFF'), 8)
    if blink < 0.85:
        ctx.save(); ctx.translate(ex, ey); ctx.scale(1, ry_eff / ry)
        ctx.arc(0, 0, rx - 4, 0, 2 * math.pi); ctx.clip()
        px, py = po
        ctx.save(); ctx.translate(px, py); ctx.scale(1, 1.18 if mode != 'wide' else 1.0)
        ctx.arc(0, 0, pr, 0, 2 * math.pi); ctx.restore(); ctx.set_source_rgba(*hexc('#2B1A10')); ctx.fill()
        if mode != 'wide':
            ctx.arc(px - 9, py - 15, 10, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
            ctx.arc(px + 9, py + 10, 4.5, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    # eyelid (deadpan)
    lid = s['lid']
    if lid > 0.01 and mode == 'normal':
        ctx.save(); ctx.translate(ex, ey); ctx.scale(1, ry_eff / ry)
        ctx.arc(0, 0, rx, 0, 2 * math.pi); ctx.restore(); ctx.save(); ctx.clip()
        yl = ey - ry + 2 * ry * lid
        ctx.rectangle(ex - rx - 10, ey - ry - 10, 2 * rx + 20, yl - (ey - ry - 10))
        ctx.set_source_rgba(*ORANGE); ctx.fill(); ctx.restore()
        half = math.sqrt(max(0, 1 - ((yl - ey) / ry) ** 2)) * rx
        ctx.move_to(ex - half - 4, yl); ctx.line_to(ex + half + 4, yl)
        ctx.set_source_rgba(*INK); ctx.set_line_width(9); ctx.stroke()


def mouth(ctx, hx, hy, s, t):
    m, k = s['mouth'], s['mk']
    nx, ny = hx, hy + 62
    ctx.set_source_rgba(*INK); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if m in ('smile', 'chew', 'line'):
        bob = math.sin(s['chew'] * 2 * math.pi) * 7 if m == 'chew' else 0
        if m == 'line':
            ctx.move_to(nx - 26, ny + 22); ctx.line_to(nx + 26, ny + 22)
            ctx.set_line_width(8); ctx.stroke(); return
        ctx.move_to(nx, ny + 8); ctx.line_to(nx, ny + 18 + bob)
        ctx.move_to(nx, ny + 18 + bob); ctx.curve_to(nx - 6, ny + 40 + bob, nx - 30, ny + 40 + bob, nx - 38, ny + 22)
        ctx.move_to(nx, ny + 18 + bob); ctx.curve_to(nx + 6, ny + 40 + bob, nx + 30, ny + 40 + bob, nx + 38, ny + 22)
        ctx.set_line_width(8); ctx.stroke()
        if m == 'chew':  # cheek bulges
            b = 0.5 + 0.5 * math.sin(s['chew'] * 2 * math.pi)
            ctx.set_source_rgba(*ORANGE_L)
            for sx in (-1, 1):
                ctx.arc(nx + sx * 72, ny + 22, 24 + 9 * b, 0, 2 * math.pi); ctx.fill()
    elif m in ('open', 'pant'):
        rx, ry = 46 * max(k, 0.12), 58 * max(k, 0.12)
        cy = ny + 22 + ry * 0.75
        ctx.save(); ctx.translate(nx, cy); ctx.scale(rx / 50, ry / 50); ctx.arc(0, 0, 50, 0, 2 * math.pi); ctx.restore()
        fill_stroke(ctx, hexc('#7A1F2B'), 8)
        ctx.save(); ctx.translate(nx, cy); ctx.scale(rx / 50, ry / 50); ctx.arc(0, 0, 47, 0, 2 * math.pi); ctx.restore()
        ctx.save(); ctx.clip()
        tongue_y = cy + ry * (0.55 if m == 'open' else 0.35)
        ctx.arc(nx, tongue_y, rx * 0.8, 0, 2 * math.pi); ctx.set_source_rgba(*PINK); ctx.fill(); ctx.restore()
        if m == 'pant':  # tongue out
            ctx.save(); ctx.translate(nx + 8, cy + ry * 0.9); ctx.scale(0.8, 1)
            ctx.arc(0, 0, 26, 0, math.pi); ctx.restore(); fill_stroke(ctx, PINK, 6)
        ctx.move_to(nx, ny + 8); ctx.line_to(nx, cy - ry); ctx.set_source_rgba(*INK); ctx.set_line_width(8); ctx.stroke()
    elif m == 'pucker':
        j = math.sin(t * 47) * 2.5
        cx, cy = nx + j, ny + 38
        ctx.arc(cx, cy, 15, 0, 2 * math.pi); fill_stroke(ctx, hexc('#7A1F2B'), 8)
        ctx.set_source_rgba(*INK); ctx.set_line_width(6)
        for i in range(8):
            a = 2 * math.pi * i / 8 + 0.2
            ctx.move_to(cx + 24 * math.cos(a), cy + 24 * math.sin(a))
            ctx.line_to(cx + 36 * math.cos(a), cy + 36 * math.sin(a))
        ctx.stroke()


def draw_head(ctx, t, s):
    hx = HEAD[0] + s['lean'][0]; hy = HEAD[1] + s['lean'][1]
    if s['mouth'] == 'chew': hy += math.sin(s['chew'] * 2 * math.pi) * 4
    sq = s['squish']
    rx, ry = 236 * (1 - 0.05 * sq), 206 * (1 + 0.05 * sq)
    R = (rx + ry) / 2
    for side in (-1, 1):
        ear(ctx, hx, hy, side, R, max(-0.3, s['ear']), s['puff'])
    blob_path(ctx, hx, hy, rx, ry, s['puff'], s['phase'], tufts=1.0)
    fill_stroke(ctx, ORANGE)
    # muzzle, stripes, green tint (clipped to head)
    ctx.save(); blob_path(ctx, hx, hy, rx, ry, s['puff'], s['phase'], tufts=1.0); ctx.clip()
    ctx.save(); ctx.translate(hx, hy + 85); ctx.scale(1.35, 0.9); ctx.arc(0, 0, 92, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(*CREAM); ctx.fill()
    ctx.set_source_rgba(*ORANGE_D); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx, l in ((-46, 62), (0, 82), (46, 62)):
        ctx.move_to(hx + dx, hy - ry - 10); ctx.line_to(hx + dx * 0.85, hy - ry + l); ctx.set_line_width(20); ctx.stroke()
    if s['green'] > 0:
        gg = cairo.LinearGradient(0, hy - ry, 0, hy + ry)
        gg.add_color_stop_rgba(0, *hexc('#7CC544', 0.9 * s['green']))
        gg.add_color_stop_rgba(0.75, *hexc('#9AD65A', 0.55 * s['green']))
        gg.add_color_stop_rgba(1, *hexc('#9AD65A', 0.0))
        ctx.rectangle(hx - 400, hy - 400, 800, 800); ctx.set_source(gg); ctx.fill()
    ctx.restore()
    # blush
    if s['green'] < 0.4:
        ctx.set_source_rgba(*hexc('#FF7F98', 0.35 * (1 - s['green'] / 0.4)))
        for sx in (-1, 1):
            ctx.save(); ctx.translate(hx + sx * 140, hy + 58); ctx.scale(1.3, 0.8)
            ctx.arc(0, 0, 26, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    # eyes
    for side in (-1, 1):
        eye(ctx, hx + side * 88, hy - 12, side, s, t)
    # brows during squeeze
    if s['eye'] == 'squeeze':
        ctx.set_source_rgba(*INK); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for side in (-1, 1):
            ctx.move_to(hx + side * 130, hy - 92); ctx.line_to(hx + side * 52, hy - 66); ctx.stroke()
    # nose
    nx, ny = hx, hy + 52
    ctx.move_to(nx - 20, ny - 8); ctx.curve_to(nx - 20, ny - 16, nx + 20, ny - 16, nx + 20, ny - 8)
    ctx.curve_to(nx + 16, ny + 4, nx + 4, ny + 12, nx, ny + 12); ctx.curve_to(nx - 4, ny + 12, nx - 16, ny + 4, nx - 20, ny - 8)
    ctx.close_path(); fill_stroke(ctx, PINK, 6)
    mouth(ctx, hx, hy, s, t)
    # whiskers
    droop = 26 * s['squish']
    ctx.set_source_rgba(*INK); ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for side in (-1, 1):
        for i in range(3):
            y0 = hy + 66 + i * 16; j = math.sin(t * 40 + i) * 4 * s['puff']
            ctx.move_to(hx + side * 112, y0)
            ctx.curve_to(hx + side * 170, y0 - 14 + i * 8 + droop * 0.5, hx + side * 210, y0 - 8 + i * 14 + droop + j,
                         hx + side * 250, y0 - 2 + i * 22 + droop + j)
            ctx.stroke()
    return hx, hy, rx, ry


def draw_fx(ctx, t, s, hx, hy, rx, ry):
    # sniff marks
    for p in s['sniff']:
        a = math.sin(math.pi * p)
        ctx.set_source_rgba(*hexc('#3A2216', 0.75 * a)); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(3):
            ox = hx + 70 + 22 * p + i * 18; oy = hy + 40 + i * 10 - 8 * p
            ctx.arc(ox, oy, 12 + 4 * i, -0.9, 0.9); ctx.stroke()
    # juice
    if s['juice'] is not None:
        p = s['juice']
        rnd = random.Random(7)
        for i in range(9):
            vx = rnd.uniform(-420, 380); vy = rnd.uniform(-650, -250)
            x = BITE_POS[0] - 20 + vx * p; y = BITE_POS[1] - 20 + vy * p + 1300 * p * p
            r = rnd.uniform(9, 16) * (1 - 0.5 * p)
            ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFE14D', 1 - p ** 3)); ctx.fill()
            ctx.arc(x - r * 0.3, y - r * 0.3, r * 0.35, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.8 * (1 - p)); ctx.fill()
    # impact burst
    if s['burst'] > 0:
        ctx.set_source_rgba(*hexc('#3A2216', s['burst'])); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(14):
            a = 2 * math.pi * i / 14 + 0.1
            r0 = max(rx, ry) + 70 + 18 * (i % 2); r1 = r0 + 70 + 40 * (i % 3 == 0)
            ctx.move_to(hx + r0 * math.cos(a), hy + r0 * math.sin(a))
            ctx.line_to(hx + r1 * math.cos(a), hy + r1 * math.sin(a)); ctx.stroke()
    # sweat
    if s['sweat'] > 0:
        for i, (ox, oy, sp) in enumerate(((210, -150, 1.0), (-235, -110, 1.35))):
            p = (s['sweat'] * sp * 2.2 + i * 0.4) % 1.0
            x = hx + ox + (8 if ox > 0 else -8) * p; y = hy + oy + 140 * p
            a = math.sin(math.pi * p)
            ctx.save(); ctx.translate(x, y)
            ctx.move_to(0, -34); ctx.curve_to(16, -6, 22, 12, 0, 20); ctx.curve_to(-22, 12, -16, -6, 0, -34); ctx.close_path()
            ctx.set_source_rgba(*hexc('#8FD3FF', a)); ctx.fill_preserve()
            ctx.set_source_rgba(*hexc('#2E7FB8', a)); ctx.set_line_width(5); ctx.stroke(); ctx.restore()


def text(ctx, msg, x, y, size, fill, ink=INK, sw=18, rot=0.0, scale=1.0, alpha=1.0, shadow=None):
    if alpha <= 0 or scale <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(scale, scale)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(msg)
    ox = -ext.x_advance / 2; oy = ext.height / 2
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if shadow:
        ctx.move_to(ox + 10, oy + 12); ctx.text_path(msg)
        ctx.set_source_rgba(*shadow[:3], shadow[3] * alpha); ctx.set_line_width(sw); ctx.stroke_preserve(); ctx.fill()
    ctx.move_to(ox, oy); ctx.text_path(msg)
    ctx.set_source_rgba(*ink[:3], alpha); ctx.set_line_width(sw); ctx.stroke_preserve()
    ctx.set_source_rgba(*fill[:3], alpha); ctx.fill()
    ctx.restore()


def draw_texts(ctx, t, s):
    # WAIT FOR IT...
    if 0.12 < t < 4.2:
        sc = back(seg(t, 0.12, 0.45)); a = 1 - seg(t, 3.95, 4.15)
        dots = '.' * (1 + int((t * 3) % 3))
        bob = math.sin(t * 4) * 6
        text(ctx, 'WAIT FOR IT' + dots.ljust(3), W / 2 + 20, 330 + bob, 108, hexc('#FFFFFF'), sw=20, scale=sc, alpha=a,
             shadow=hexc('#2B1A10', 0.35))
    # SOUR!!!
    if 4.4 < t < 7.35:
        sc = back(seg(t, 4.4, 4.62)) * (1 + 0.08 * seg(t, 7.05, 7.35)) * (1 + 0.025 * math.sin(t * 22))
        a = 1 - seg(t, 7.1, 7.35)
        j = s['shake'] * 0.6
        text(ctx, 'SOUR!!!', W / 2 + j * math.sin(t * 83), 360 + j * math.cos(t * 71), 250, hexc('#FFE14D'),
             sw=30, rot=-0.08, scale=sc, alpha=a, shadow=hexc('#6FBF3A', 1.0))
    # AGAIN?
    if t > 9.05:
        sc = back(seg(t, 9.05, 9.35))
        text(ctx, 'AGAIN?', W / 2, 330, 120, hexc('#FFFFFF'), sw=20, scale=sc,
             alpha=1 - seg(t, 9.85, 10.0), shadow=hexc('#2B1A10', 0.35))


def draw_speed(ctx, s):
    if s['speed'] <= 0 or s['slice'] is None: return
    x, y = s['slice']['pos']
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(10)
    for i in (-1, 0, 1):
        ctx.move_to(x - 70 + i * 10, y + 70 + i * 34); ctx.line_to(x - 230 + i * 10, y + 190 + i * 34); ctx.stroke()


def frame(t):
    s = state(t)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    focus = (HEAD[0] + 50, HEAD[1] + 110)
    z = s['zoom']
    ctx.save()
    ctx.translate(*focus); ctx.scale(z, z); ctx.translate(-focus[0], -focus[1])
    draw_bg(ctx, t, s)
    draw_sun(ctx, t, s, (HEAD[0], HEAD[1] + 40))
    ctx.save()
    sh = s['shake']
    ctx.translate(sh * math.sin(t * 91), sh * 0.7 * math.cos(t * 79))
    draw_tail(ctx, t, s)
    draw_body(ctx, t, s)
    hx, hy, rx, ry = draw_head(ctx, t, s)
    ctx.restore()
    draw_plate(ctx, t, s)
    ctx.save(); ctx.translate(sh * math.sin(t * 91), sh * 0.7 * math.cos(t * 79))
    sl = s['slice']
    if sl:
        lemon_slice(ctx, sl['pos'][0], sl['pos'][1], 62, sl['flat'], sl['rot'], sl['bitten'], sl['scale'])
    draw_arm(ctx, s)
    draw_fx(ctx, t, s, hx, hy, rx, ry)
    ctx.restore()
    draw_speed(ctx, s)
    ctx.restore()
    # vignette
    vg = cairo.RadialGradient(W / 2, H / 2, 500, W / 2, H / 2, 1250)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0, 0.28)
    ctx.rectangle(0, 0, W, H); ctx.set_source(vg); ctx.fill()
    draw_texts(ctx, t, s)
    return surf


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'video'
    if mode == 'frames':
        for a in sys.argv[2:]:
            tt = float(a); frame(tt).write_to_png(os.path.join(OUT, f'kf_{tt:05.2f}.png'))
    else:
        dst = os.path.join(OUT, 'sour_cat_silent.mp4')
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra',
                              '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                              '-crf', '18', '-pix_fmt', 'yuv420p', dst], stdin=subprocess.PIPE)
        for i in range(N):
            surf = frame(i / FPS); surf.flush()
            p.stdin.write(bytes(surf.get_data()))
        p.stdin.close(); p.wait()
        print('wrote', dst)
