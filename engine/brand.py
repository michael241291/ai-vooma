"""Channel art: profile picture (800x800) and banner (2560x1440, text inside the 1546x423 safe area)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairo  # noqa: E402
from core import hexc, text  # noqa: E402
import nugget  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'brand')
os.makedirs(OUT, exist_ok=True)


def rays(ctx, cx, cy, r, n, col, a):
    for i in range(n):
        a0 = 2 * math.pi * i / n
        ctx.move_to(cx, cy); ctx.arc(cx, cy, r, a0, a0 + math.pi / n); ctx.close_path()
        ctx.set_source_rgba(*hexc(col, a)); ctx.fill()


def avatar():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800); ctx = cairo.Context(s)
    g = cairo.RadialGradient(400, 380, 40, 400, 400, 560)
    g.add_color_stop_rgba(0, *hexc('#FFE98A')); g.add_color_stop_rgba(1, *hexc('#FF9F43'))
    ctx.rectangle(0, 0, 800, 800); ctx.set_source(g); ctx.fill()
    rays(ctx, 400, 420, 900, 20, '#FFFFFF', 0.16)
    p = dict(x=400, y=760, scale=1.08, pose='sit', eye='big', look=[0.0, 0.2], mouth='smile', blush=0.7, tongue=True, blink=0.0)
    nugget.draw(ctx, 1.0, p)
    s.write_to_png(os.path.join(OUT, 'avatar.png'))


def banner(name='AIVOOMA', line1='ONE ORANGE CAT. ONE BRAIN CELL.', line2='NEW NUGGET VIDEO EVERY DAY', out=None):
    W, H = 2560, 1440
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, W, 0)
    g.add_color_stop_rgba(0, *hexc('#FFB35C')); g.add_color_stop_rgba(0.5, *hexc('#FFD77A')); g.add_color_stop_rgba(1, *hexc('#FF9A6B'))
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    rays(ctx, W / 2, H / 2, 2400, 28, '#FFFFFF', 0.12)
    ctx.set_source_rgba(1, 1, 1, 0.35)
    for i in range(40):
        x = (i * 263) % W; y = (i * 151) % H
        ctx.arc(x, y, 6 + i % 4 * 3, 0, 2 * math.pi); ctx.fill()
    # Nugget on the left of the safe area, peeking up from the bottom of it
    p = dict(x=W / 2 - 560, y=H / 2 + 330, scale=0.78, pose='sit', eye='big', look=[0.6, 0.0], mouth='smile', blush=0.7,
             tongue=True, blink=0.0, paw=[150, -110])
    nugget.draw(ctx, 1.0, p)
    text(ctx, name, W / 2 + 170, H / 2 - 55, 190 if len(name) <= 9 else int(190 * 9.5 / len(name)), hexc('#FFFFFF'), sw=34, shadow=hexc('#B4541E', 0.9))
    text(ctx, line1, W / 2 + 170, H / 2 + 95, 62, hexc('#3A2216'), ink=hexc('#FFFFFF'), sw=14)
    text(ctx, line2, W / 2 + 170, H / 2 + 165, 50, hexc('#FFFFFF'), sw=12)
    s.write_to_png(out or os.path.join(OUT, 'banner.png'))


def banner_cast(name, line1, line2, out):
    import extra  # noqa: F401  registers Gravy (prop_turkey)
    W, H = 2560, 1440
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, W, 0)
    g.add_color_stop_rgba(0, *hexc('#7B5CFF')); g.add_color_stop_rgba(0.5, *hexc('#FF6FB1')); g.add_color_stop_rgba(1, *hexc('#FFB35C'))
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    rays(ctx, W / 2, H / 2, 2400, 28, '#FFFFFF', 0.10)
    ctx.set_source_rgba(1, 1, 1, 0.35)
    for i in range(40):
        x = (i * 263) % W; y = (i * 151) % H
        ctx.arc(x, y, 6 + i % 4 * 3, 0, 2 * math.pi); ctx.fill()
    nugget.draw(ctx, 1.0, dict(x=W / 2 - 600, y=H / 2 + 330, scale=0.72, pose='sit', eye='big', look=[0.6, 0.0],
                                mouth='smile', blush=0.7, tongue=True, blink=0.0, paw=[150, -110]))
    import world
    ctx.save(); ctx.translate(W / 2 + 610, H / 2 + 300); ctx.scale(0.62, 0.62)
    world.PROPS['turkey'](ctx, 1.0, dict(flip=-1)); ctx.restore()
    text(ctx, name, W / 2, H / 2 - 55, 200, hexc('#FFFFFF'), sw=34, shadow=hexc('#4A1E6B', 0.9))
    text(ctx, line1, W / 2, H / 2 + 95, 60, hexc('#2A1636'), ink=hexc('#FFFFFF'), sw=14)
    text(ctx, line2, W / 2, H / 2 + 165, 48, hexc('#FFFFFF'), sw=12)
    s.write_to_png(out)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'v3':
        d = os.path.join(os.path.dirname(OUT), 'brand-v3'); os.makedirs(d, exist_ok=True)
        banner_cast('TINY CHAOS', "LIFE'S LITTLE CHAOS, ANIMATED.", 'NEW VIDEO EVERY DAY', os.path.join(d, 'banner.png'))
        import shutil; avatar(); shutil.copy(os.path.join(OUT, 'avatar.png'), os.path.join(d, 'avatar.png'))
        print(d); sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == 'v2':
        d = os.path.join(os.path.dirname(OUT), 'brand-v2'); os.makedirs(d, exist_ok=True)
        banner('ORANGE CAT HOURS', 'CAT OWNER LIFE, ANIMATED.', 'NEW VIDEO EVERY DAY', os.path.join(d, 'banner.png'))
        import shutil; avatar(); shutil.copy(os.path.join(OUT, 'avatar.png'), os.path.join(d, 'avatar.png'))
        print(d)
    else:
        avatar(); banner(); print(OUT)
