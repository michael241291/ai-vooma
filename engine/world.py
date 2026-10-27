"""Backgrounds, props and effects for AIVOOMA videos. Every draw function takes (ctx, t, p) where p holds the
actor's current track values. Floor line is y≈1330; a sitting Nugget at scale 1 stands at y=1255."""
import math
import random
import cairo
from core import hexc, INK, OUTLINE_W, fill_stroke, ellipse, rrect, text, tri, clamp, lerp, W, H

# ============================== BACKGROUNDS ==============================

def _floor_wood(ctx, top, c1, c2, line):
    g = cairo.LinearGradient(0, top, 0, top + 700)
    g.add_color_stop_rgba(0, *hexc(c1)); g.add_color_stop_rgba(1, *hexc(c2))
    ctx.rectangle(-600, top, W + 1200, 1400); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(*hexc(line, 0.35)); ctx.set_line_width(4)
    for i, y in enumerate((top + 70, top + 170, top + 300, top + 460)):
        ctx.move_to(-600, y); ctx.line_to(W + 600, y); ctx.stroke()
        for k in range(-3, 9):
            x = k * 230 + (i % 2) * 115
            ctx.move_to(x, y); ctx.line_to(x - 10, y + (110 if i < 3 else 160)); ctx.stroke()
    ctx.set_source_rgba(*hexc(c1, 1)); ctx.rectangle(-600, top - 6, W + 1200, 10); ctx.fill()


def _window(ctx, x, y, w, h, night=False, curtains=None, t=0):
    ctx.save(); ctx.translate(x, y)
    rrect(ctx, -w / 2, 0, w, h, 14); fill_stroke(ctx, hexc('#FFFFFF') if not night else hexc('#C9D3F2'), 12, hexc('#8FB9C9') if not night else hexc('#4A5687'))
    sky = cairo.LinearGradient(0, 0, 0, h)
    if night:
        sky.add_color_stop_rgba(0, *hexc('#1B2350')); sky.add_color_stop_rgba(1, *hexc('#3B4A8C'))
    else:
        sky.add_color_stop_rgba(0, *hexc('#7CCBF5')); sky.add_color_stop_rgba(1, *hexc('#CDEFFF'))
    ctx.rectangle(-w / 2 + 18, 18, w - 36, h - 36); ctx.set_source(sky); ctx.fill()
    if night:
        ctx.arc(w * 0.18, h * 0.28, 46, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFF6C8')); ctx.fill()
        ctx.arc(w * 0.18 + 22, h * 0.28 - 12, 40, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#24306A')); ctx.fill()
        rnd = random.Random(5)
        for i in range(14):
            sx = rnd.uniform(-w / 2 + 30, w / 2 - 30); sy = rnd.uniform(30, h - 40)
            a = 0.5 + 0.5 * math.sin(t * 3 + i)
            ctx.arc(sx, sy, rnd.uniform(2, 4.5), 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 0.85, a); ctx.fill()
    else:
        ctx.set_source_rgba(1, 1, 1, 0.92)
        for cx, cy, r in ((-60, 120, 34), (-25, 108, 44), (15, 124, 30), (60, 250, 26), (92, 242, 34)):
            ctx.arc(cx + 20 * math.sin(t * 0.2), cy, r, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgba(*hexc('#8FB9C9' if not night else '#4A5687')); ctx.set_line_width(12)
    ctx.move_to(0, 18); ctx.line_to(0, h - 18); ctx.move_to(-w / 2 + 18, h / 2); ctx.line_to(w / 2 - 18, h / 2); ctx.stroke()
    if curtains:
        for sx in (-1, 1):
            ctx.move_to(sx * (w / 2 + 40), -30); ctx.line_to(sx * (w / 2 - 50), -30)
            ctx.curve_to(sx * (w / 2 - 20), h * 0.4, sx * (w / 2 - 60), h * 0.7, sx * (w / 2 - 10), h + 40)
            ctx.line_to(sx * (w / 2 + 40), h + 40); ctx.close_path(); fill_stroke(ctx, hexc(curtains), 7)
        ctx.rectangle(-w / 2 - 70, -44, w + 140, 16); fill_stroke(ctx, hexc('#9A6B45'), 6)
    ctx.restore()


def bg_kitchen(ctx, t, p):
    g = cairo.LinearGradient(0, 0, 0, 1330)
    g.add_color_stop_rgba(0, *hexc('#BFE6F2')); g.add_color_stop_rgba(1, *hexc('#E5F5EA'))
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.45)
    for row in range(-6, 15):
        for col in range(-6, 16):
            x = col * 110 + (55 if row % 2 else 0); y = row * 95
            ctx.arc(x, y, 10, 0, 2 * math.pi); ctx.fill()
    _window(ctx, 170, 300, 330, 420, t=t)
    # counter with cabinets on the right
    ctx.rectangle(660, 820, 700, 520); fill_stroke(ctx, hexc('#F4E3C8'), 9)
    ctx.rectangle(640, 790, 740, 40); fill_stroke(ctx, hexc('#D9B98F'), 9)
    for x in (700, 900):
        rrect(ctx, x, 870, 170, 400, 16); fill_stroke(ctx, hexc('#FFF4E2'), 7)
        ctx.arc(x + 140, 1060, 10, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
    # floor tiles
    top = 1330
    ctx.rectangle(-600, top, W + 1200, 1400); ctx.set_source_rgba(*hexc('#F3E9DA')); ctx.fill()
    ctx.set_source_rgba(*hexc('#E2D3BD'))
    for r in range(0, 8):
        for c in range(-4, 10):
            if (r + c) % 2 == 0:
                y0 = top + r * 90; x0 = c * 160 + (r * 26)
                ctx.move_to(x0, y0); ctx.line_to(x0 + 160, y0); ctx.line_to(x0 + 186, y0 + 90); ctx.line_to(x0 + 26, y0 + 90)
                ctx.close_path(); ctx.fill()
    ctx.set_source_rgba(*hexc('#CDB89A')); ctx.rectangle(-600, top - 8, W + 1200, 14); ctx.fill()


def bg_living(ctx, t, p):
    wall = p.get('wall', '#F6D9B8')
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source_rgba(*hexc(wall)); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.18)
    for x in range(-600, W + 600, 90):
        ctx.rectangle(x, -600, 40, 1940); ctx.fill()
    _window(ctx, 300, 260, 360, 460, curtains='#E86F5B', t=t)
    # framed picture
    rrect(ctx, 740, 330, 220, 170, 10); fill_stroke(ctx, hexc('#FFFFFF'), 9)
    ctx.move_to(770, 470); ctx.line_to(830, 390); ctx.line_to(880, 450); ctx.line_to(910, 420); ctx.line_to(935, 470)
    ctx.close_path(); ctx.set_source_rgba(*hexc('#7FB77E')); ctx.fill()
    ctx.arc(905, 375, 18, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFC94D')); ctx.fill()
    # sofa back-left
    rrect(ctx, -260, 980, 620, 300, 60); fill_stroke(ctx, hexc('#6E8FD8'), 9)
    rrect(ctx, -300, 1120, 700, 210, 50); fill_stroke(ctx, hexc('#5A79C2'), 9)
    rrect(ctx, 300, 1060, 120, 250, 50); fill_stroke(ctx, hexc('#6E8FD8'), 9)
    ctx.rectangle(-600, 1180, W + 1200, 6)
    _floor_wood(ctx, 1330, '#D9A06A', '#B9814F', '#7A4E2F')
    ellipse(ctx, 540, 1560, 520, 120); ctx.set_source_rgba(*hexc('#E8C9E8', 0.9)); ctx.fill()
    ellipse(ctx, 540, 1560, 440, 90); ctx.set_source_rgba(*hexc('#D9A9D9', 0.7)); ctx.fill()


def bg_bedroom_night(ctx, t, p):
    lamp = p.get('lamp', 0.0)
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source_rgba(*hexc('#2B3466')); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.05)
    for row in range(-6, 15):
        for col in range(-6, 16):
            x = col * 120 + (60 if row % 2 else 0); y = row * 110
            ctx.move_to(x, y - 12); ctx.line_to(x + 8, y); ctx.line_to(x, y + 12); ctx.line_to(x - 8, y); ctx.close_path(); ctx.fill()
    _window(ctx, 760, 250, 330, 420, night=True, curtains='#5161A8', t=t)
    _floor_wood(ctx, 1330, '#5B4637', '#3E2F25', '#20160F')
    # nightstand + lamp (right)
    rrect(ctx, 740, 1040, 330, 300, 14); fill_stroke(ctx, hexc('#6B4E3A'), 9)
    ctx.rectangle(770, 1110, 270, 10); ctx.set_source_rgba(*INK); ctx.fill()
    ctx.rectangle(990, 900, 20, 140); fill_stroke(ctx, hexc('#C9B79C'), 6)
    ctx.move_to(935, 900); ctx.line_to(1065, 900); ctx.line_to(1035, 810); ctx.line_to(965, 810); ctx.close_path()
    fill_stroke(ctx, hexc('#F2D98E') if lamp > 0.5 else hexc('#B9A77A'), 7)
    if lamp > 0:
        rg = cairo.RadialGradient(1000, 880, 10, 1000, 880, 700)
        rg.add_color_stop_rgba(0, 1, 0.92, 0.6, 0.55 * lamp); rg.add_color_stop_rgba(1, 1, 0.92, 0.6, 0)
        ctx.rectangle(-600, -600, W + 1200, 2600); ctx.set_source(rg); ctx.fill()


def bg_plain(ctx, t, p):
    c1 = p.get('c1', '#FFE7A8'); c2 = p.get('c2', '#FFB86B')
    rg = cairo.RadialGradient(540, 900, 50, 540, 900, 1300)
    rg.add_color_stop_rgba(0, *hexc(c1)); rg.add_color_stop_rgba(1, *hexc(c2))
    ctx.rectangle(-600, -600, W + 1200, 3200); ctx.set_source(rg); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.18)
    for i in range(16):
        a = i * math.pi / 8 + t * 0.15
        ctx.move_to(540, 900); ctx.arc(540, 900, 2000, a, a + math.pi / 16); ctx.close_path(); ctx.fill()
    ellipse(ctx, 540, 1460, 700, 90); ctx.set_source_rgba(0, 0, 0, 0.08); ctx.fill()


def _blinds_window(ctx, x, y, w, h, t):
    ctx.save(); ctx.translate(x, y)
    rrect(ctx, -w / 2, 0, w, h, 10); fill_stroke(ctx, hexc('#FFFFFF'), 12, hexc('#9AA7B8'))
    sky = cairo.LinearGradient(0, 0, 0, h)
    sky.add_color_stop_rgba(0, *hexc('#FFB88C')); sky.add_color_stop_rgba(1, *hexc('#FFE3B3'))  # late-afternoon sky
    ctx.rectangle(-w / 2 + 16, 16, w - 32, h - 32); ctx.set_source(sky); ctx.fill()
    ctx.arc(w * 0.2, h * 0.62, 50, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFF1C4')); ctx.fill()
    ctx.set_source_rgba(*hexc('#EDE6DA', 0.95))
    for i in range(int(h * 0.55 / 34)):
        ctx.rectangle(-w / 2 + 16, 16 + i * 34, w - 32, 22); ctx.fill()
    ctx.set_source_rgba(*hexc('#9AA7B8')); ctx.set_line_width(4)
    ctx.move_to(w / 2 - 40, 16); ctx.line_to(w / 2 - 40, h * 0.62); ctx.stroke()
    ctx.restore()


def bg_living_b(ctx, t, p):
    """Second living room: window with blinds on the right, bookshelf + floor lamp on the left, rectangular rug."""
    wall = p.get('wall', '#CFE3D8')
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source_rgba(*hexc(wall)); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.22)
    for row in range(-6, 16):
        for col in range(-6, 16):
            x = col * 140 + (70 if row % 2 else 0); y = row * 120
            ctx.save(); ctx.translate(x, y); ctx.rotate(math.pi / 4); ctx.rectangle(-9, -9, 18, 18); ctx.restore(); ctx.fill()
    ctx.rectangle(-600, 1060, W + 1200, 270); ctx.set_source_rgba(*hexc('#FFFFFF', 0.35)); ctx.fill()
    ctx.rectangle(-600, 1052, W + 1200, 14); ctx.set_source_rgba(*hexc('#FFFFFF', 0.8)); ctx.fill()
    _blinds_window(ctx, 790, 230, 380, 480, t)
    # bookshelf left
    rrect(ctx, -60, 520, 330, 820, 10); fill_stroke(ctx, hexc('#A9744A'))
    cols = ['#E86F5B', '#5A79C2', '#FFC94D', '#7FB77E', '#B08BE8', '#F49AC1']
    for sh, y in enumerate((700, 880, 1060, 1240)):
        ctx.rectangle(-40, y, 290, 16); fill_stroke(ctx, hexc('#8B5E3C'), 6)
        x = -30
        for k in range(6):
            bw = 30 + (k * 7 + sh * 5) % 22; bh = 120 + (k * 13 + sh * 11) % 40
            ctx.rectangle(x, y - bh, bw, bh); fill_stroke(ctx, hexc(cols[(k + sh) % 6]), 5); x += bw + 6
            if x > 220: break
    # floor lamp
    ctx.rectangle(395, 780, 14, 550); fill_stroke(ctx, hexc('#3A3F4B'), 5)
    ctx.move_to(340, 780); ctx.line_to(465, 780); ctx.line_to(440, 690); ctx.line_to(365, 690); ctx.close_path()
    fill_stroke(ctx, hexc('#FFE8A8'), 7)
    ellipse(ctx, 402, 1330, 60, 14); fill_stroke(ctx, hexc('#3A3F4B'), 5)
    _floor_wood(ctx, 1330, '#C9925E', '#A87645', '#6E4526')
    rrect(ctx, 120, 1470, 840, 210, 30); ctx.set_source_rgba(*hexc('#F2C14E', 0.85)); ctx.fill()
    rrect(ctx, 160, 1500, 760, 150, 20); ctx.set_source_rgba(*hexc('#E5A93A', 0.6)); ctx.fill()


def bg_bedroom_day(ctx, t, p):
    wall = p.get('wall', '#FFF1C9')
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source_rgba(*hexc(wall)); ctx.fill()
    ctx.set_source_rgba(*hexc('#F7B267', 0.35))
    for x in range(-600, W + 600, 120):
        ctx.rectangle(x, -600, 18, 1940); ctx.fill()
    _window(ctx, 540, 230, 420, 470, curtains='#7FB7E8', t=t)
    # wall shelf with plant + books
    ctx.rectangle(80, 860, 300, 22); fill_stroke(ctx, hexc('#B9835A'), 7)
    for i, c in enumerate(('#E86F5B', '#5A79C2', '#FFC94D')):
        ctx.rectangle(110 + i * 44, 730, 36, 130); fill_stroke(ctx, hexc(c), 5)
    ctx.move_to(270, 860); ctx.line_to(282, 790); ctx.line_to(348, 790); ctx.line_to(360, 860); ctx.close_path(); fill_stroke(ctx, hexc('#E9785A'), 6)
    ctx.set_source_rgba(*hexc('#4FAE62'))
    for ang in (-0.9, 0, 0.9):
        ctx.save(); ctx.translate(315, 790); ctx.rotate(ang + 0.05 * math.sin(t * 2)); ctx.scale(1, 2.2)
        ctx.arc(0, -20, 16, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    # string lights
    ctx.set_source_rgba(*INK); ctx.set_line_width(4)
    ctx.move_to(-20, 120); ctx.curve_to(300, 220, 780, 220, 1100, 120); ctx.stroke()
    for i in range(10):
        k = i / 9; x = lerp(0, 1080, k); y = 120 + 75 * math.sin(math.pi * k)
        a = 0.6 + 0.4 * math.sin(t * 3 + i)
        ctx.arc(x, y + 16, 12, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(['#FFD43B', '#FF8FA3', '#7CF0FF'][i % 3], a)); ctx.fill()
    # carpet floor
    ctx.rectangle(-600, 1330, W + 1200, 1400); ctx.set_source_rgba(*hexc('#B7A3D9')); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.12)
    for i in range(80):
        x = (i * 137) % (W + 200) - 100; y = 1340 + (i * 89) % 560
        ctx.arc(x, y, 6, 0, 2 * math.pi); ctx.fill()
    ctx.rectangle(-600, 1322, W + 1200, 14); ctx.set_source_rgba(*hexc('#FFFFFF')); ctx.fill()


def bg_hallway(ctx, t, p):
    wall = p.get('wall', '#F3D6C7')
    ctx.rectangle(-600, -600, W + 1200, 1940); ctx.set_source_rgba(*hexc(wall)); ctx.fill()
    ctx.rectangle(-600, 980, W + 1200, 350); ctx.set_source_rgba(*hexc('#E2B9A4')); ctx.fill()  # wainscot
    ctx.rectangle(-600, 972, W + 1200, 16); ctx.set_source_rgba(*hexc('#FFFFFF')); ctx.fill()
    for x in range(-560, W + 600, 200):
        rrect(ctx, x, 1020, 160, 270, 8); ctx.set_source_rgba(1, 1, 1, 0.25); ctx.set_line_width(6); ctx.stroke()
    # front door (right)
    rrect(ctx, 720, 420, 360, 920, 12); fill_stroke(ctx, hexc('#2F6F8F'), 10)
    rrect(ctx, 770, 480, 260, 200, 10); fill_stroke(ctx, hexc('#BFE6F2'), 7)
    for y in (740, 960):
        rrect(ctx, 770, y, 260, 180, 8); ctx.set_source_rgba(1, 1, 1, 0.18); ctx.set_line_width(6); ctx.stroke()
    ctx.arc(1050, 900, 16, 0, 2 * math.pi); fill_stroke(ctx, hexc('#F2C14E'), 5)
    # coat hooks + coat, mirror (left)
    ctx.rectangle(60, 520, 360, 26); fill_stroke(ctx, hexc('#8B5E3C'), 6)
    for x in (110, 230, 350):
        ctx.arc(x, 560, 12, 0, 2 * math.pi); fill_stroke(ctx, hexc('#F2C14E'), 4)
    ctx.move_to(200, 560); ctx.line_to(140, 640); ctx.line_to(120, 900); ctx.line_to(300, 900); ctx.line_to(280, 640); ctx.close_path()
    fill_stroke(ctx, hexc('#E86F5B'), 8)
    ctx.move_to(350, 560); ctx.curve_to(380, 640, 330, 700, 360, 800); ctx.set_line_width(26); ctx.set_source_rgba(*INK); ctx.stroke()
    ctx.move_to(350, 560); ctx.curve_to(380, 640, 330, 700, 360, 800); ctx.set_line_width(16); ctx.set_source_rgba(*hexc('#FFC94D')); ctx.stroke()
    # tiled floor + runner
    top = 1330
    ctx.rectangle(-600, top, W + 1200, 1400); ctx.set_source_rgba(*hexc('#EDE3D3')); ctx.fill()
    ctx.set_source_rgba(*hexc('#D6C7B0')); ctx.set_line_width(4)
    for r in range(0, 9):
        ctx.move_to(-600, top + r * 80); ctx.line_to(W + 600, top + r * 80); ctx.stroke()
    for c in range(-6, 14):
        ctx.move_to(c * 140, top); ctx.line_to(c * 140 - 120, top + 700); ctx.stroke()
    rrect(ctx, 60, 1440, 900, 230, 18); ctx.set_source_rgba(*hexc('#C0392B', 0.85)); ctx.fill()
    rrect(ctx, 90, 1465, 840, 180, 12); ctx.set_source_rgba(1, 1, 1, 0.25); ctx.set_line_width(8); ctx.stroke()
    ctx.rectangle(-600, top - 8, W + 1200, 14); ctx.set_source_rgba(*hexc('#B98F74')); ctx.fill()


BACKGROUNDS = dict(kitchen=bg_kitchen, living=bg_living, living_b=bg_living_b, bedroom_night=bg_bedroom_night,
                   bedroom_day=bg_bedroom_day, hallway=bg_hallway, plain=bg_plain)

# ============================== PROPS ==============================
LEMON = hexc('#FFD43B'); LEMON_RIND = hexc('#F2B705')


def prop_lemon(ctx, t, p):
    r = 62; flat = p.get('flat', 1.0)
    ctx.save(); ctx.scale(1, flat)
    if p.get('bitten'):
        ctx.rectangle(-500, -500, 1000, 1000)
        for bx, by, br in ((-38, -46, 26), (-6, -63, 27), (27, -54, 24)):
            ctx.new_sub_path(); ctx.arc(bx, by, br, 0, 2 * math.pi)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); ctx.clip(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    ctx.arc(0, 0, r, 0, 2 * math.pi); fill_stroke(ctx, LEMON_RIND, OUTLINE_W / max(flat, 0.5))
    ctx.arc(0, 0, r * 0.86, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFF8CF')); ctx.fill()
    ctx.arc(0, 0, r * 0.78, 0, 2 * math.pi); ctx.set_source_rgba(*LEMON); ctx.fill()
    for i in range(9):
        a = 2 * math.pi * i / 9
        ctx.move_to(0, 0); ctx.line_to(r * 0.78 * math.cos(a), r * 0.78 * math.sin(a))
    ctx.set_source_rgba(*hexc('#FFF8CF')); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def prop_cucumber(ctx, t, p):
    pickle = p.get('pickle', False)
    col = hexc('#7A9E3A') if pickle else hexc('#3E9B4F'); light = hexc('#A9C96A') if pickle else hexc('#7DCB6E')
    L, R = 230, 52
    ctx.save()
    if p.get('bitten'):
        ctx.rectangle(-500, -500, 1000, 1000)
        for bx, by, br in ((L - 10, -18, 30), (L + 6, 20, 28)):
            ctx.new_sub_path(); ctx.arc(bx, by, br, 0, 2 * math.pi)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); ctx.clip(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    ctx.move_to(-L, 0)
    ctx.curve_to(-L, -R * 1.2, -L * 0.4, -R * 1.05, 0, -R); ctx.curve_to(L * 0.5, -R * 1.05, L, -R * 1.1, L, 0)
    ctx.curve_to(L, R * 1.1, L * 0.5, R * 1.05, 0, R); ctx.curve_to(-L * 0.4, R * 1.05, -L, R * 1.2, -L, 0)
    ctx.close_path(); fill_stroke(ctx, col)
    ctx.set_source_rgba(*light)
    rnd = random.Random(2)
    for i in range(16):
        x = rnd.uniform(-L * 0.85, L * 0.85); y = rnd.uniform(-R * 0.6, R * 0.6)
        ellipse(ctx, x, y, 9, 6); ctx.fill()
    ctx.move_to(-L * 0.7, -R * 0.55); ctx.curve_to(-L * 0.2, -R * 0.8, L * 0.3, -R * 0.75, L * 0.7, -R * 0.5)
    ctx.set_source_rgba(1, 1, 1, 0.45); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()
    if p.get('eyes'):  # menacing cartoon eyes
        for sx in (-50, 30):
            ellipse(ctx, sx, -8, 22, 26); fill_stroke(ctx, hexc('#FFFFFF'), 6)
            ctx.arc(sx + 6, -4, 10, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
        ctx.move_to(-80, -42); ctx.line_to(-28, -28); ctx.move_to(56, -42); ctx.line_to(6, -28)
        ctx.set_source_rgba(*INK); ctx.set_line_width(8); ctx.stroke()


def prop_vacuum(ctx, t, p):
    on = p.get('on', False)
    j = (math.sin(t * 80) * 4, math.cos(t * 67) * 3) if on else (0, 0)
    ctx.save(); ctx.translate(*j)
    # handle + body (upright vacuum, ~700 tall), origin at floor center of head
    ctx.move_to(40, -420); ctx.line_to(70, -900); ctx.set_line_width(30); ctx.set_source_rgba(*INK); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.move_to(40, -420); ctx.line_to(70, -900); ctx.set_line_width(16); ctx.set_source_rgba(*hexc('#9AA3B5')); ctx.stroke()
    rrect(ctx, 10, -960, 120, 60, 26); fill_stroke(ctx, hexc('#2E3440'), 8)
    rrect(ctx, -90, -520, 240, 400, 70); fill_stroke(ctx, hexc('#E2463F'), 9)
    rrect(ctx, -50, -470, 160, 180, 40); fill_stroke(ctx, hexc('#C8E6F5'), 7)
    ctx.set_source_rgba(*hexc('#9C8C80', 0.8))
    for i in range(7):
        ctx.arc(-20 + (i % 4) * 30, -340 - (i // 4) * 40 + (math.sin(t * 30 + i) * 8 if on else 0), 12, 0, 2 * math.pi); ctx.fill()
    rrect(ctx, -170, -130, 360, 120, 40); fill_stroke(ctx, hexc('#3A3F4B'), 9)
    rrect(ctx, -150, -40, 320, 34, 14); fill_stroke(ctx, hexc('#22262E'), 6)
    ctx.arc(150, -80, 14, 0, 2 * math.pi); ctx.set_source_rgba(*(hexc('#7CFF7A') if on else hexc('#555555'))); ctx.fill()
    if p.get('face'):
        for sx in (-70, 20):
            ellipse(ctx, sx, -90, 20, 16); fill_stroke(ctx, hexc('#FFFFFF'), 5)
            ctx.arc(sx + 4, -88, 8, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
    ctx.restore()
    if on:
        ctx.set_source_rgba(1, 1, 1, 0.7); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(4):
            ph = (t * 3 + i * 0.25) % 1
            x = -220 - 160 * (1 - ph)
            ctx.move_to(x, -100 + i * 20 - 40); ctx.line_to(x + 70, -90 + i * 16 - 40); ctx.stroke()


def prop_clock(ctx, t, p):
    rrect(ctx, -150, -80, 300, 160, 30); fill_stroke(ctx, hexc('#2B2B33'), 9)
    rrect(ctx, -125, -58, 250, 116, 14); ctx.set_source_rgba(*hexc('#120A0A')); ctx.fill()
    blink = (t % 1.0) < 0.5 or not p.get('blinkcolon', True)
    txt = p.get('time', '3:00')
    glow = hexc('#FF3B30')
    text(ctx, txt if blink else txt.replace(':', ' '), 0, 4, 92, glow, ink=hexc('#3A0606'), sw=6)
    text(ctx, 'AM', 98, 34, 26, glow, ink=hexc('#3A0606'), sw=3)


def prop_bed(ctx, t, p):
    """Bed seen from the side, lying along the bottom of the frame. Owner asleep under the blanket."""
    rrect(ctx, -520, -300, 70, 420, 20); fill_stroke(ctx, hexc('#8B5E3C'), 9)
    rrect(ctx, -470, -60, 1000, 170, 20); fill_stroke(ctx, hexc('#F3F1FA'), 9)
    rrect(ctx, -430, -150, 230, 110, 50); fill_stroke(ctx, hexc('#FFFFFF'), 8)
    wake = p.get('wake', 0.0)
    breathe = math.sin(t * 1.8) * 8
    ctx.move_to(-300, -60); ctx.curve_to(-250, -230 - breathe, 300, -200 - breathe, 520, -60)
    ctx.line_to(520, 40); ctx.line_to(-300, 40); ctx.close_path(); fill_stroke(ctx, hexc('#7FA7E8'), 9)
    ctx.set_source_rgba(1, 1, 1, 0.25); ctx.set_line_width(14)
    for x in (-100, 100, 300):
        ctx.move_to(x, -150); ctx.line_to(x - 40, 30); ctx.stroke()
    ellipse(ctx, -310, -125, 75, 55); fill_stroke(ctx, hexc('#4A3426'), 8)  # hair
    if wake > 0.05:
        for sx in (-340, -285):
            ellipse(ctx, sx, -118, 16, 18 * wake); fill_stroke(ctx, hexc('#FFFFFF'), 5)
            ctx.arc(sx + 3, -116, 7 * wake, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()


def prop_mug(ctx, t, p):
    rrect(ctx, -60, -110, 120, 120, 18); fill_stroke(ctx, hexc(p.get('color', '#FF8FA3')))
    ctx.arc(70, -55, 30, -math.pi / 2, math.pi / 2); ctx.set_line_width(16); ctx.set_source_rgba(*INK); ctx.stroke()
    ctx.arc(70, -55, 30, -math.pi / 2, math.pi / 2); ctx.set_line_width(6); ctx.set_source_rgba(*hexc(p.get('color', '#FF8FA3'))); ctx.stroke()
    text(ctx, p.get('label', '#1'), 0, -50, 42, hexc('#FFFFFF'), sw=6)


def prop_table(ctx, t, p):
    w = p.get('w', 360)
    rrect(ctx, -w / 2, -26, w, 40, 10); fill_stroke(ctx, hexc('#B9835A'))
    for sx in (-w / 2 + 30, w / 2 - 50):
        ctx.rectangle(sx, 14, 20, p.get('h', 300)); fill_stroke(ctx, hexc('#9A6B45'), 7)


def prop_shards(ctx, t, p):
    rnd = random.Random(p.get('seed', 1))
    col = hexc(p.get('color', '#FF8FA3'))
    for i in range(7):
        x = rnd.uniform(-150, 150); y = rnd.uniform(-10, 20); s = rnd.uniform(18, 38); a = rnd.uniform(0, 6.28)
        ctx.save(); ctx.translate(x, y); ctx.rotate(a)
        ctx.move_to(-s, 0); ctx.line_to(s * 0.4, -s * 0.6); ctx.line_to(s, s * 0.3); ctx.close_path()
        ctx.restore(); fill_stroke(ctx, col, 5)


def prop_fancybed(ctx, t, p):
    ellipse(ctx, 0, 30, 300, 70); ctx.set_source_rgba(0, 0, 0, 0.12); ctx.fill()
    ctx.move_to(-290, 0); ctx.curve_to(-300, -180, 300, -180, 290, 0); ctx.curve_to(290, 70, -290, 70, -290, 0)
    ctx.close_path(); fill_stroke(ctx, hexc('#A98BE8'))
    ellipse(ctx, 0, -10, 210, 55); fill_stroke(ctx, hexc('#F3E9FF'), 7)
    ctx.set_source_rgba(1, 1, 1, 0.8)
    for i in range(3):
        ctx.arc(-120 + i * 120, -120 + (i % 2) * 14, 7, 0, 2 * math.pi); ctx.fill()
    if p.get('tag', True):
        ctx.save(); ctx.translate(230, -150); ctx.rotate(0.25 + 0.06 * math.sin(t * 3))
        ctx.move_to(-20, -80); ctx.line_to(0, -10); ctx.set_line_width(5); ctx.set_source_rgba(*INK); ctx.stroke()
        rrect(ctx, -70, -10, 150, 80, 12); fill_stroke(ctx, hexc('#FFF59A'), 6)
        text(ctx, p.get('price', '$80'), 5, 30, 50, hexc('#E2463F'), sw=6)
        ctx.restore()


def prop_box(ctx, t, p):
    part = p.get('part', 'all'); w = p.get('w', 300); h = p.get('h', 200)
    if part in ('back', 'all'):
        ctx.move_to(-w / 2, -h); ctx.line_to(-w / 2 + 40, -h - 60); ctx.line_to(w / 2 + 40, -h - 60); ctx.line_to(w / 2, -h)
        ctx.close_path(); fill_stroke(ctx, hexc('#B98A55'))
    if part in ('front', 'all'):
        ctx.rectangle(-w / 2, -h, w, h); fill_stroke(ctx, hexc('#D9A86C'))
        ctx.move_to(w / 2, -h); ctx.line_to(w / 2 + 40, -h - 60); ctx.line_to(w / 2 + 40, -60); ctx.line_to(w / 2, 0)
        ctx.close_path(); fill_stroke(ctx, hexc('#C4945C'))
        ctx.rectangle(-30, -h, 60, h); ctx.set_source_rgba(*hexc('#E9D2A6', 0.7)); ctx.fill()
        ctx.move_to(-w / 2, -h); ctx.line_to(-w / 2 - 70, -h - 40); ctx.line_to(-w / 2 - 50, -h + 40); ctx.close_path()
        fill_stroke(ctx, hexc('#D9A86C'), 7)
        if p.get('label'):
            text(ctx, p['label'], -w / 4 - 10, -h / 2, 34, hexc('#7A4E2F'), ink=hexc('#D9A86C'), sw=2)


def prop_tv(ctx, t, p):
    mode = p.get('mode', 'fish'); shake = p.get('wobble', 0.0)
    ctx.save(); ctx.rotate(math.sin(t * 25) * 0.03 * shake)
    rrect(ctx, -260, -620, 520, 70, 12); fill_stroke(ctx, hexc('#6B4E3A'))
    rrect(ctx, -330, -1000, 660, 420, 30); fill_stroke(ctx, hexc('#2E3440'))
    sx0, sy0, sw, sh = -300, -970, 600, 360
    ctx.save(); rrect(ctx, sx0, sy0, sw, sh, 18); ctx.clip()
    if mode == 'fish':
        g = cairo.LinearGradient(0, sy0, 0, sy0 + sh)
        g.add_color_stop_rgba(0, *hexc('#43B5E8')); g.add_color_stop_rgba(1, *hexc('#155E9B'))
        ctx.rectangle(sx0, sy0, sw, sh); ctx.set_source(g); ctx.fill()
        ctx.set_source_rgba(1, 1, 1, 0.5)
        for i in range(8):
            bx = sx0 + 60 + (i * 83) % sw; by = sy0 + sh - ((t * 90 + i * 57) % sh)
            ctx.arc(bx, by, 6 + i % 3 * 3, 0, 2 * math.pi); ctx.fill()
        fx = p.get('fishx', math.sin(t * 1.3) * 180); fy = sy0 + sh / 2 + math.sin(t * 2.1) * 60
        d = 1 if math.cos(t * 1.3) > 0 else -1
        ctx.save(); ctx.translate(fx, fy); ctx.scale(d, 1)
        ellipse(ctx, 0, 0, 70, 42); fill_stroke(ctx, hexc('#FF9F1C'), 7)
        ctx.move_to(-60, 0); ctx.line_to(-110, -36); ctx.line_to(-110, 36); ctx.close_path(); fill_stroke(ctx, hexc('#FF9F1C'), 7)
        ctx.arc(34, -8, 9, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
        ctx.restore()
        ctx.set_source_rgba(*hexc('#2E8B57'))
        for i in range(5):
            x = sx0 + 40 + i * 130
            ctx.move_to(x, sy0 + sh); ctx.curve_to(x - 20, sy0 + sh - 60, x + 30 * math.sin(t * 2 + i), sy0 + sh - 120, x, sy0 + sh - 170)
            ctx.set_line_width(14); ctx.stroke()
    elif mode == 'static':
        rnd = random.Random(int(t * 30))
        ctx.rectangle(sx0, sy0, sw, sh); ctx.set_source_rgba(0.5, 0.5, 0.5, 1); ctx.fill()
        for i in range(500):
            v = rnd.random()
            ctx.rectangle(sx0 + rnd.random() * sw, sy0 + rnd.random() * sh, 14, 8); ctx.set_source_rgba(v, v, v, 1); ctx.fill()
        rrect(ctx, -170, sy0 + sh / 2 - 50, 340, 100, 12); ctx.set_source_rgba(0, 0, 0, 0.75); ctx.fill()
        text(ctx, 'NO SIGNAL', 0, sy0 + sh / 2, 60, hexc('#FFFFFF'), ink=hexc('#000000'), sw=4)
    else:
        ctx.rectangle(sx0, sy0, sw, sh); ctx.set_source_rgba(*hexc('#14171C')); ctx.fill()
    if p.get('crack'):
        ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(5)
        cx, cy = p.get('crackx', 80), sy0 + sh * 0.45
        rnd = random.Random(9)
        for i in range(7):
            a = i * 0.9 + 0.3; x, y = cx, cy; ctx.move_to(x, y)
            for k in range(4):
                a += rnd.uniform(-0.5, 0.5); x += 40 * math.cos(a); y += 40 * math.sin(a); ctx.line_to(x, y)
            ctx.stroke()
    ctx.set_source_rgba(1, 1, 1, 0.12)
    ctx.move_to(sx0, sy0); ctx.line_to(sx0 + 220, sy0); ctx.line_to(sx0, sy0 + 200); ctx.close_path(); ctx.fill()
    ctx.restore()
    ctx.restore()


def prop_treat(ctx, t, p):
    ctx.move_to(-40, 0); ctx.curve_to(-20, -26, 20, -26, 34, 0); ctx.curve_to(20, 26, -20, 26, -40, 0); ctx.close_path()
    fill_stroke(ctx, hexc('#C98A55'), 6)
    ctx.move_to(30, 0); ctx.line_to(56, -18); ctx.line_to(56, 18); ctx.close_path(); fill_stroke(ctx, hexc('#C98A55'), 6)


def prop_plate(ctx, t, p):
    ctx.save(); ctx.scale(1, 0.36); ctx.arc(0, 0, 185, 0, 2 * math.pi); ctx.restore(); fill_stroke(ctx, hexc('#FFFFFF'))
    ctx.save(); ctx.scale(1, 0.36); ctx.arc(0, 0, 140, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(*hexc('#8CC8E8')); ctx.set_line_width(6); ctx.stroke()


def prop_bowl(ctx, t, p):
    fill = p.get('fill', 0.5)
    ctx.move_to(-130, -60); ctx.line_to(130, -60); ctx.line_to(100, 10); ctx.line_to(-100, 10); ctx.close_path()
    fill_stroke(ctx, hexc(p.get('color', '#4DA3FF')))
    ellipse(ctx, 0, -60, 130, 26); fill_stroke(ctx, hexc('#2D6FB8'), 7)
    if fill > 0:
        ctx.save(); ellipse(ctx, 0, -60, 122, 20); ctx.clip()
        rnd = random.Random(4)
        for i in range(int(30 * fill)):
            x = rnd.uniform(-110, 110); y = -60 + rnd.uniform(-10, 14) - (8 if abs(x) < 70 * fill else 0)
            ellipse(ctx, x, y, 12, 9); ctx.set_source_rgba(*hexc('#B5703A')); ctx.fill()
        ctx.restore()
    text(ctx, p.get('label', 'NUGGET'), 0, -22, 30, hexc('#FFFFFF'), sw=5)


PROPS = dict(lemon=prop_lemon, cucumber=prop_cucumber, vacuum=prop_vacuum, clock=prop_clock, bed=prop_bed,
             mug=prop_mug, table=prop_table, shards=prop_shards, fancybed=prop_fancybed, box=prop_box, tv=prop_tv,
             treat=prop_treat, plate=prop_plate, bowl=prop_bowl)

# ============================== EFFECTS ==============================

def fx_target(ctx, t, p):
    """Dashed 'put your finger here' circle with a pointing finger icon."""
    pulse = 1 + 0.08 * math.sin(t * 8)
    r = p.get('r', 120) * pulse
    col = hexc(p.get('color', '#FF3B30'))
    ctx.set_line_width(12); ctx.set_dash([28, 18], t * 40)
    ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(20); ctx.stroke_preserve()
    ctx.set_source_rgba(*col); ctx.set_line_width(12); ctx.stroke()
    ctx.set_dash([])
    ctx.arc(0, 0, r * 0.18, 0, 2 * math.pi); ctx.set_source_rgba(col[0], col[1], col[2], 0.5); ctx.fill()
    bob = math.sin(t * 6) * 14
    ctx.save(); ctx.translate(r * 0.55, r * 0.75 + bob); ctx.rotate(-0.5)
    _finger_icon(ctx, 1.0); ctx.restore()
    if p.get('label'):
        text(ctx, p['label'], 0, -r - 70, p.get('label_size', 54), hexc('#FFFFFF'), sw=14)


def _hand_parts(ctx, pose, arm=True):
    """Yield closures that each add one rounded part of a cartoon hand (palm facing viewer, fingers up)."""
    parts = []
    def cap(x, y, w, h):  # rounded finger/thumb, (x,y) = bottom centre
        return lambda: rrect(ctx, x - w / 2, y - h, w, h, w / 2)
    if pose == 'finger':
        parts.append(lambda: rrect(ctx, -95, -40, 190, 210, 70))     # palm / fist
        parts.append(cap(-28, -10, 64, 230))                          # index finger up
        for x, h in ((24, 70), (62, 62), (92, 50)):
            parts.append(cap(x, 0, 52, h))                            # curled fingers (knuckles)
        parts.append(lambda: ellipse(ctx, -100, 40, 40, 55))          # thumb
        if arm: parts.append(lambda: rrect(ctx, -80, 120, 160, 700, 40))     # wrist/arm
    else:
        parts.append(lambda: rrect(ctx, -140, -60, 280, 290, 110))   # palm
        for x, h in ((-100, 200), (-35, 245), (35, 240), (100, 195)):
            parts.append(cap(x, -10, 64, h))
        parts.append(lambda: (ctx.save(), ctx.translate(150, 60), ctx.rotate(0.7), rrect(ctx, -32, -170, 64, 180, 32), ctx.restore()))
        if arm: parts.append(lambda: rrect(ctx, -110, 180, 220, 700, 60))
    return parts


def _draw_hand(ctx, pose, fill, line, lw, dash=None, t=0, arm=True):
    parts = _hand_parts(ctx, pose, arm)
    for mk in parts:
        ctx.new_path(); mk()
        ctx.set_source_rgba(*line); ctx.set_line_width(lw * 2)
        if dash: ctx.set_dash(dash, t * 30)
        ctx.stroke(); ctx.set_dash([])
    for mk in parts:
        ctx.new_path(); mk(); ctx.set_source_rgba(*fill); ctx.fill()


def _finger_icon(ctx, s):
    ctx.save(); ctx.scale(s * 0.42, s * 0.42)
    _draw_hand(ctx, 'finger', hexc('#FFE0BD'), hexc('#3A2216'), 9, arm=False)
    ctx.set_source_rgba(*hexc('#E8B98F')); ctx.set_line_width(6)
    for x in (24, 62):
        ctx.move_to(x - 14, -40); ctx.line_to(x - 14, -10); ctx.stroke()
    ctx.restore()


def fx_hand(ctx, t, p):
    """The viewer's 'hand': a big translucent palm (pose=palm) or pointing finger (pose=finger) coming from below."""
    a = p.get('alpha', 0.85)
    ctx.push_group()
    _draw_hand(ctx, p.get('pose', 'palm'), (0.93, 0.97, 1, 1), hexc('#5AB2FF'), 7)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(0.62 * a)


def fx_burst(ctx, t, p):
    r = p.get('r', 300); a = p.get('alpha', 1.0)
    ctx.set_source_rgba(*hexc(p.get('color', '#3A2216'), a)); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(14):
        ang = 2 * math.pi * i / 14 + 0.1
        r0 = r + 18 * (i % 2); r1 = r0 + 70 + 40 * (i % 3 == 0)
        ctx.move_to(r0 * math.cos(ang), r0 * math.sin(ang)); ctx.line_to(r1 * math.cos(ang), r1 * math.sin(ang)); ctx.stroke()


def fx_sweat(ctx, t, p):
    for i, (ox, oy, sp) in enumerate(((0, 0, 1.0), (-430, 40, 1.35))):
        ph = (t * sp * 1.4 + i * 0.4) % 1.0
        x = ox; y = oy + 140 * ph; a = math.sin(math.pi * ph) * p.get('alpha', 1)
        ctx.save(); ctx.translate(x, y)
        ctx.move_to(0, -34); ctx.curve_to(16, -6, 22, 12, 0, 20); ctx.curve_to(-22, 12, -16, -6, 0, -34); ctx.close_path()
        ctx.set_source_rgba(*hexc('#8FD3FF', a)); ctx.fill_preserve()
        ctx.set_source_rgba(*hexc('#2E7FB8', a)); ctx.set_line_width(5); ctx.stroke(); ctx.restore()


def fx_hearts(ctx, t, p):
    rnd = random.Random(p.get('seed', 3))
    n = p.get('n', 7)
    for i in range(n):
        ph = (t * 0.55 + i / n) % 1.0
        x = rnd.uniform(-200, 200) + 40 * math.sin(t * 2 + i); y = -360 * ph
        s = rnd.uniform(18, 34) * (0.6 + 0.4 * ph)
        a = math.sin(math.pi * ph) * p.get('alpha', 1.0)
        ctx.save(); ctx.translate(x, y)
        ctx.move_to(0, s * 0.9); ctx.curve_to(-s * 1.6, -s * 0.2, -s * 0.8, -s * 1.4, 0, -s * 0.5)
        ctx.curve_to(s * 0.8, -s * 1.4, s * 1.6, -s * 0.2, 0, s * 0.9); ctx.close_path()
        ctx.set_source_rgba(*hexc('#FF4F7B', a)); ctx.fill_preserve(); ctx.set_source_rgba(*hexc('#3A2216', a)); ctx.set_line_width(5); ctx.stroke()
        ctx.restore()


def fx_zzz(ctx, t, p):
    for i in range(3):
        ph = (t * 0.6 + i / 3) % 1.0
        text(ctx, 'z', 40 * i + 30 * math.sin(t + i), -200 * ph, 40 + 40 * ph, hexc('#FFFFFF'), sw=8, alpha=math.sin(math.pi * ph) * p.get('alpha', 1))


def fx_speed(ctx, t, p):
    a = p.get('alpha', 1.0); ang = p.get('angle', math.pi); L = p.get('length', 260)
    ctx.set_source_rgba(1, 1, 1, 0.9 * a); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(10)
    for i in (-1, 0, 1):
        ox, oy = -math.sin(ang) * i * 50, math.cos(ang) * i * 50
        ctx.move_to(ox, oy); ctx.line_to(ox + math.cos(ang) * L * (1 - 0.2 * abs(i)), oy + math.sin(ang) * L * (1 - 0.2 * abs(i))); ctx.stroke()


def fx_dust(ctx, t, p):
    ph = p.get('ph', (t * 2) % 1.0); a = (1 - ph) * p.get('alpha', 1)
    for i, dx in enumerate((-60, 0, 60)):
        ctx.arc(dx + dx * ph, -20 * ph - (i % 2) * 10, 26 + 30 * ph, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.75 * a); ctx.fill()


def fx_mark(ctx, t, p):
    s = p.get('scale', 1.0)
    text(ctx, p.get('char', '!'), 0, 0, 160, hexc(p.get('color', '#FFE14D')), sw=18, rot=0.12 * math.sin(t * 9), scale=s)


def fx_sparkle(ctx, t, p):
    rnd = random.Random(p.get('seed', 6)); r = p.get('r', 240)
    for i in range(8):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0.5, 1.0) * r
        ph = (t * 1.5 + i / 8) % 1.0; s = 22 * math.sin(math.pi * ph) * p.get('alpha', 1)
        x, y = d * math.cos(a), d * math.sin(a)
        ctx.move_to(x, y - s * 2); ctx.line_to(x + s * 0.5, y - s * 0.5); ctx.line_to(x + s * 2, y); ctx.line_to(x + s * 0.5, y + s * 0.5)
        ctx.line_to(x, y + s * 2); ctx.line_to(x - s * 0.5, y + s * 0.5); ctx.line_to(x - s * 2, y); ctx.line_to(x - s * 0.5, y - s * 0.5)
        ctx.close_path(); ctx.set_source_rgba(1, 0.95, 0.5, 1); ctx.fill()


def fx_waves(ctx, t, p):
    a = p.get('alpha', 1.0)
    for i in range(3):
        ph = (t * 1.2 + i / 3) % 1.0; r = 60 + 220 * ph
        for side in (-1, 1):
            ctx.arc(0, 0, r, (-0.5 if side > 0 else math.pi - 0.5), (0.5 if side > 0 else math.pi + 0.5))
            ctx.set_source_rgba(1, 1, 1, (1 - ph) * a); ctx.set_line_width(10); ctx.stroke()


def fx_flash(ctx, t, p):
    a = p.get('alpha', 0)
    if a > 0:
        ctx.rectangle(-2000, -2000, 5000, 6000); ctx.set_source_rgba(*hexc(p.get('color', '#FFFFFF'), a)); ctx.fill()


def fx_sunburst(ctx, t, p):
    a = p.get('alpha', 1.0)
    if a <= 0: return
    ctx.save(); ctx.rotate(t * 0.9)
    for i in range(18):
        a0 = 2 * math.pi * i / 18
        ctx.move_to(0, 0); ctx.arc(0, 0, 1800, a0, a0 + math.pi / 18); ctx.close_path()
        ctx.set_source_rgba(*hexc(p.get('color', '#FFF06A'), 0.55 * a)); ctx.fill()
    ctx.restore()
    rg = cairo.RadialGradient(0, 0, 0, 0, 0, 900)
    rg.add_color_stop_rgba(0, 1, 1, 0.88, 0.85 * a); rg.add_color_stop_rgba(1, 1, 1, 0.88, 0)
    ctx.arc(0, 0, 900, 0, 2 * math.pi); ctx.set_source(rg); ctx.fill()


def fx_stars(ctx, t, p):
    for i in range(4):
        a = t * 5 + i * math.pi / 2
        x, y = 170 * math.cos(a), 45 * math.sin(a)
        s = 20
        ctx.move_to(x, y - s); ctx.line_to(x + s * 0.3, y - s * 0.3); ctx.line_to(x + s, y); ctx.line_to(x + s * 0.3, y + s * 0.3)
        ctx.line_to(x, y + s); ctx.line_to(x - s * 0.3, y + s * 0.3); ctx.line_to(x - s, y); ctx.line_to(x - s * 0.3, y - s * 0.3)
        ctx.close_path(); fill_stroke(ctx, hexc('#FFE14D'), 4)


def fx_text(ctx, t, p):
    s = p.get('pop', 1.0) * p.get('scale', 1.0) * (1 + p.get('pulse', 0) * 0.03 * math.sin(t * 20))
    text(ctx, p.get('text', ''), 0, 0, p.get('size', 100), hexc(p.get('fill', '#FFFFFF')), ink=hexc(p.get('ink', '#3A2216')),
         sw=p.get('sw', 20), rot=p.get('tilt', 0.0), scale=s, alpha=p.get('alpha', 1.0),
         shadow=hexc(p['shadow'], p.get('shadow_a', 1.0)) if p.get('shadow') else hexc('#2B1A10', 0.35))


FX = dict(target=fx_target, hand=fx_hand, burst=fx_burst, sweat=fx_sweat, hearts=fx_hearts, zzz=fx_zzz, speed=fx_speed,
          dust=fx_dust, mark=fx_mark, sparkle=fx_sparkle, waves=fx_waves, flash=fx_flash, sunburst=fx_sunburst,
          stars=fx_stars, text=fx_text)
