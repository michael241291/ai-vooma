"""Batch 5 additions (2026-11-17, Tiny Chaos): pet carrier, suitcase.
Registered into world.PROPS at import (render.py imports this module)."""
import math
from core import hexc, INK, fill_stroke, rrect, text
import world


def prop_carrier(ctx, t, p):
    """Plastic pet carrier, origin = floor centre, ~420 wide x 300 tall at scale 1.
    label (sticker text), door 0..1 (grid door swings open to the left), rattle (shake amount)."""
    sh = p.get('rattle', 0.0)
    ctx.save(); ctx.rotate(math.sin(t * 31) * 0.035 * sh); ctx.translate(math.sin(t * 23) * 6 * sh, 0)
    col = p.get('color', '#9AA7B8')
    # body
    rrect(ctx, -210, -290, 420, 290, 60); fill_stroke(ctx, hexc(col))
    ctx.rectangle(-210, -150, 420, 14); ctx.set_source_rgba(*hexc('#6E7A8A')); ctx.fill()
    for sx in (-1, 1):  # vent slots
        for k in range(3):
            rrect(ctx, sx * 150 - 12, -250 + k * 34, 24, 18, 8); ctx.set_source_rgba(*hexc('#4A5361')); ctx.fill()
    # handle
    ctx.move_to(-90, -290); ctx.curve_to(-90, -370, 90, -370, 90, -290); ctx.set_line_width(26); ctx.set_source_rgba(*INK); ctx.stroke()
    ctx.move_to(-90, -290); ctx.curve_to(-90, -370, 90, -370, 90, -290); ctx.set_line_width(14); ctx.set_source_rgba(*hexc(col)); ctx.stroke()
    # door (front grid)
    d = p.get('door', 0.0)
    ctx.save(); ctx.translate(-110, -250); ctx.scale(max(0.05, 1 - 1.6 * d), 1)
    rrect(ctx, 0, 0, 220, 200, 30); ctx.set_source_rgba(*hexc('#2E3440')); ctx.fill()
    ctx.set_source_rgba(*hexc('#C9D1DB')); ctx.set_line_width(7)
    for k in range(1, 6):
        ctx.move_to(k * 220 / 6, 10); ctx.line_to(k * 220 / 6, 190); ctx.stroke()
    for k in range(1, 4):
        ctx.move_to(10, k * 50); ctx.line_to(210, k * 50); ctx.stroke()
    rrect(ctx, 0, 0, 220, 200, 30); ctx.set_line_width(10); ctx.set_source_rgba(*INK); ctx.stroke()
    ctx.restore()
    if p.get('eyes'):  # glowing eyes in the dark carrier
        for sx in (-1, 1):
            ctx.arc(sx * 34, -160, 13, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFE14D')); ctx.fill()
    if p.get('label'):
        rrect(ctx, 120, -120, 150, 70, 14); fill_stroke(ctx, hexc('#FFFFFF'), 6)
        text(ctx, p['label'], 195, -84, 44, hexc('#E53935'), ink=hexc('#FFFFFF'), sw=0)
    ctx.restore()


def prop_suitcase(ctx, t, p):
    """Rolling suitcase, origin = floor centre (~300 wide, 360 tall). label sticker, color, stuffed 0..1 (bulge + sock poking out)."""
    col = p.get('color', '#E8552B'); b = p.get('stuffed', 0.0)
    ctx.move_to(-60, -360); ctx.line_to(-60, -470); ctx.line_to(60, -470); ctx.line_to(60, -360)
    ctx.set_line_width(14); ctx.set_source_rgba(*INK); ctx.stroke()
    w = 300 + 30 * b
    rrect(ctx, -w / 2, -370, w, 340, 40); fill_stroke(ctx, hexc(col))
    for sx in (-1, 1):
        ctx.rectangle(sx * 70 - 6, -360, 12, 320); ctx.set_source_rgba(0, 0, 0, 0.18); ctx.fill()
        ctx.arc(sx * 100, -12, 22, 0, 2 * math.pi); fill_stroke(ctx, hexc('#2E3440'), 6)
    if b > 0.3:
        ctx.move_to(w / 2 - 10, -250); ctx.line_to(w / 2 + 60, -230); ctx.line_to(w / 2 + 50, -200); ctx.line_to(w / 2 - 10, -215)
        ctx.close_path(); fill_stroke(ctx, hexc('#7BD389'), 6)
    if p.get('label'):
        ctx.save(); ctx.rotate(-0.12)
        rrect(ctx, -110, -260, 220, 90, 16); fill_stroke(ctx, hexc('#FFF6D5'), 6)
        text(ctx, p['label'], 0, -214, p.get('size', 44), hexc('#2E3440'), ink=hexc('#FFF6D5'), sw=0)
        ctx.restore()


world.PROPS.update(carrier=prop_carrier, suitcase=prop_suitcase)
