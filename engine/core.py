"""Shared helpers: colours, easing, keyframe tracks, small drawing utilities."""
import math
import cairo

W, H, FPS = 1080, 1920, 30
FONT = "Luckiest Guy"


def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= b)


def lerp(a, b, k):
    return a + (b - a) * k


def tri(x):
    return 1 - abs((x % 1.0) * 2 - 1)


EASES = {
    'linear': lambda x: x,
    'in': lambda x: x * x,
    'out': lambda x: 1 - (1 - x) ** 3,
    'inout': lambda x: x * x * (3 - 2 * x),
    'back': lambda x: 1 + 2.9 * (x - 1) ** 3 + 1.9 * (x - 1) ** 2,
    'bounce': lambda x: 1 - abs(math.cos(x * math.pi * 2.5)) * (1 - x) ** 1.5,
    'elastic': lambda x: 1 - math.cos(x * math.pi * 3.5) * math.exp(-5 * x),
    'step': lambda x: 0.0,
}


class Track:
    """Keyframes: list of [t, value] or [t, value, ease]. The ease shapes the move INTO that key.
    Numbers and lists of numbers interpolate; strings/bools/None hold until the next key."""

    def __init__(self, keys):
        self.keys = sorted(keys, key=lambda k: k[0])

    def at(self, t):
        ks = self.keys
        if not ks:
            return None
        if t <= ks[0][0]:
            return ks[0][1]
        for i in range(1, len(ks)):
            if t < ks[i][0]:
                a, b = ks[i - 1], ks[i]
                va, vb = a[1], b[1]
                ease = b[2] if len(b) > 2 else 'inout'
                if not _numeric(va) or not _numeric(vb) or ease == 'step':
                    return va
                k = EASES.get(ease, EASES['inout'])(clamp((t - a[0]) / max(1e-6, b[0] - a[0])))
                if isinstance(va, (list, tuple)):
                    return [lerp(x, y, k) for x, y in zip(va, vb)]
                return lerp(va, vb, k)
        return ks[-1][1]


def _numeric(v):
    if isinstance(v, bool) or v is None:
        return False
    if isinstance(v, (int, float)):
        return True
    return isinstance(v, (list, tuple)) and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v)


INK = hexc('#3A2216')
OUTLINE_W = 9


def fill_stroke(ctx, fill, lw=OUTLINE_W, ink=INK):
    ctx.set_source_rgba(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgba(*ink)
    ctx.set_line_width(lw)
    ctx.stroke()


def ellipse(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def text(ctx, msg, x, y, size, fill, ink=INK, sw=18, rot=0.0, scale=1.0, alpha=1.0, shadow=None, font=FONT):
    if alpha <= 0.01 or scale <= 0.01 or not msg:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(scale, scale)
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    lines = str(msg).split('\n')
    ctx.set_font_size(size)
    lh = size * 1.02
    total = lh * len(lines)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for i, line in enumerate(lines):
        ext = ctx.text_extents(line)
        ox = -ext.x_advance / 2
        oy = -total / 2 + lh * (i + 0.82)
        if shadow:
            ctx.move_to(ox + size * 0.05, oy + size * 0.06)
            ctx.text_path(line)
            ctx.set_source_rgba(shadow[0], shadow[1], shadow[2], shadow[3] * alpha)
            ctx.set_line_width(sw)
            ctx.stroke_preserve()
            ctx.fill()
        ctx.move_to(ox, oy)
        ctx.text_path(line)
        ctx.set_source_rgba(ink[0], ink[1], ink[2], alpha)
        ctx.set_line_width(sw)
        ctx.stroke_preserve()
        ctx.set_source_rgba(fill[0], fill[1], fill[2], alpha)
        ctx.fill()
    ctx.restore()
