"""Batch 4 additions (2026-11-15, Tiny Chaos): laptop with a video call on screen, protest sign on a stick.
Registered into world.PROPS at import (render.py imports this module)."""
import math
from core import hexc, INK, fill_stroke, ellipse, rrect, text
import world

TILE_COLS = ['#5B8DEF', '#F28C8C', '#7BD389', '#F2C14E']


def _cat_face(ctx, x, y, r, col):
    for sx in (-1, 1):
        ctx.move_to(x + sx * r * 0.35, y - r * 0.7); ctx.line_to(x + sx * r * 0.9, y - r * 1.25); ctx.line_to(x + sx * r * 0.95, y - r * 0.35)
        ctx.close_path(); fill_stroke(ctx, hexc(col), 4)
    ctx.arc(x, y, r, 0, 2 * math.pi); fill_stroke(ctx, hexc(col), 4)
    for sx in (-1, 1):
        ctx.arc(x + sx * r * 0.38, y - r * 0.1, r * 0.13, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
    ctx.move_to(x - r * 0.1, y + r * 0.2); ctx.line_to(x + r * 0.1, y + r * 0.2); ctx.line_to(x, y + r * 0.32); ctx.close_path()
    ctx.set_source_rgba(*hexc('#FF8FA3')); ctx.fill()


def _person(ctx, x, y, r, col, hair):
    ctx.arc(x, y + r * 1.5, r * 1.1, math.pi, 0); fill_stroke(ctx, hexc(col), 4)
    ctx.arc(x, y, r * 0.7, 0, 2 * math.pi); fill_stroke(ctx, hexc('#F1C6A5'), 4)
    ctx.arc(x, y - r * 0.15, r * 0.72, math.pi, 0); ctx.set_source_rgba(*hexc(hair)); ctx.fill()
    for sx in (-1, 1):
        ctx.arc(x + sx * r * 0.25, y + r * 0.05, r * 0.07, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()


def prop_laptop(ctx, t, p):
    """Laptop, origin = front centre of the base (put it on a table top). Screen 560x360 above the base.
    tiles: list of labels (2x2 call grid); cats: list of tile indexes showing a cat face; butt: tile index showing a
    giant orange fluff + tail; chat: text in the chat strip; banner: red banner text over the screen; glow 0..1."""
    # base / keyboard
    ctx.move_to(-330, 0); ctx.line_to(330, 0); ctx.line_to(290, -60); ctx.line_to(-290, -60); ctx.close_path()
    fill_stroke(ctx, hexc('#C9D1DA'), 8)
    ctx.set_source_rgba(*hexc('#8E99A6'))
    for row in range(3):
        for k in range(12):
            x = -250 + k * 42 + row * 6; y = -50 + row * 15
            ctx.rectangle(x, y, 34, 10); ctx.fill()
    # screen
    rrect(ctx, -300, -440, 600, 390, 18); fill_stroke(ctx, hexc('#2B2F36'), 8)
    sx0, sy0, sw, sh = -280, -420, 560, 350
    ctx.rectangle(sx0, sy0, sw, sh); ctx.set_source_rgba(*hexc('#14171C')); ctx.fill()
    tiles = p.get('tiles', ['BOSS', 'KAREN', 'DAVE', 'ME'])
    cats = p.get('cats', []); butt = p.get('butt', -1)
    tw, th = (sw - 30) / 2, (sh - 80) / 2
    for i, lab in enumerate(tiles[:4]):
        x = sx0 + 10 + (i % 2) * (tw + 10); y = sy0 + 10 + (i // 2) * (th + 10)
        ctx.save(); rrect(ctx, x, y, tw, th, 10); ctx.clip()
        ctx.rectangle(x, y, tw, th); ctx.set_source_rgba(*hexc(TILE_COLS[i % 4], 0.55)); ctx.fill()
        cx, cy = x + tw / 2, y + th / 2
        if i == butt:
            ellipse(ctx, cx, cy + 40, tw * 0.62, th * 0.75); fill_stroke(ctx, hexc('#F28C28'), 6)
            ctx.move_to(cx + 20, cy - 10); ctx.curve_to(cx + 90, cy - 80, cx + 30, cy - 120, cx + 70, cy - 140)
            ctx.set_line_width(26); ctx.set_source_rgba(*INK); ctx.stroke()
            ctx.move_to(cx + 20, cy - 10); ctx.curve_to(cx + 90, cy - 80, cx + 30, cy - 120, cx + 70, cy - 140)
            ctx.set_line_width(16); ctx.set_source_rgba(*hexc('#F28C28')); ctx.stroke()
        elif i in cats:
            _cat_face(ctx, cx, cy + 10, 42, ['#9AA0A6', '#2E2E2E', '#F5F5F5', '#F28C28'][i % 4])
        else:
            _person(ctx, cx, cy - 10, 40, ['#3A4A6B', '#A23B72', '#2E7D32', '#555555'][i % 4], ['#3B2A20', '#C68B59', '#1E1E1E', '#5A3A1A'][i % 4])
        ctx.restore()
        rrect(ctx, x + 8, y + th - 36, 120, 28, 8); ctx.set_source_rgba(0, 0, 0, 0.55); ctx.fill()
        text(ctx, lab, x + 68, y + th - 22, 22, hexc('#FFFFFF'), sw=0.01)
    chat = p.get('chat', '')
    rrect(ctx, sx0 + 10, sy0 + sh - 56, sw - 20, 44, 10); ctx.set_source_rgba(*hexc('#2C3440')); ctx.fill()
    if chat:
        text(ctx, chat[-26:], 0, sy0 + sh - 34, 30, hexc('#FFFFFF'), sw=0.01)
    ban = p.get('banner', '')
    if ban:
        rrect(ctx, -260, sy0 + 4, 520, 70, 16); fill_stroke(ctx, hexc('#E53935'), 6)
        text(ctx, ban, 0, sy0 + 39, 40, hexc('#FFFFFF'), sw=6)
    ctx.arc(0, -430, 5, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#7CF0A0')); ctx.fill()  # webcam light


def prop_picket(ctx, t, p):
    """Protest sign on a wooden stick; origin = bottom of the stick (held at ~y -200). label, color."""
    rrect(ctx, -14, -520, 28, 520, 8); fill_stroke(ctx, hexc('#B9835A'), 7)
    ctx.save(); ctx.translate(0, -620); ctx.rotate(math.sin(t * 5) * 0.04)
    rrect(ctx, -230, -150, 460, 260, 16); fill_stroke(ctx, hexc(p.get('color', '#FFF7E0')), 9)
    text(ctx, p.get('label', 'NO!'), 0, -20, p.get('size', 72), hexc(p.get('ink', '#E53935')), ink=hexc('#3A2216'), sw=8)
    ctx.restore()


world.PROPS.update(laptop=prop_laptop, picket=prop_picket)
