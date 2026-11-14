"""Tiny Chaos puzzles: "find the odd one out" grids drawn in code.

Usage: python engine/puzzle.py episodes/<id>/puzzle.json [--frames 0 3 7]
cfg: id, ver, title, item ("mug"|"donut"|"phone"), cols, rows, odd [col,row], seconds, duration, seed, bg [a,b]
"""
import json
import math
import os
import subprocess
import sys
import wave

import cairo
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import W, H, FPS, hexc, text, rrect, fill_stroke  # noqa: E402
import sound  # noqa: E402


# ---------------- items (normal, odd) ----------------
def mug(ctx, s, odd, wob):
    ctx.save(); ctx.scale(s, s); ctx.rotate(wob)
    side = -1 if odd else 1
    ctx.set_line_width(7); ctx.set_source_rgba(*hexc('#2A1636'))
    ctx.arc(side * 30, 2, 17, -math.pi / 2, math.pi / 2) if side > 0 else ctx.arc_negative(side * 30, 2, 17, -math.pi / 2, math.pi / 2)
    ctx.stroke()
    rrect(ctx, -30, -30, 60, 62, 10); fill_stroke(ctx, hexc('#FF6FB1'), 6)
    ctx.rectangle(-30, -30, 60, 10); ctx.set_source_rgba(*hexc('#6B3E26')); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.8)
    for k in (-10, 8):
        ctx.move_to(k, -38); ctx.curve_to(k + 8, -48, k - 8, -54, k, -64); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def donut(ctx, s, odd, wob):
    ctx.save(); ctx.scale(s, s); ctx.rotate(wob)
    ctx.arc(0, 0, 36, 0, 2 * math.pi); fill_stroke(ctx, hexc('#E9A75B'), 6)
    ctx.arc(0, 0, 30, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FF6FB1')); ctx.fill()
    ctx.arc(0, 0, 11, 0, 2 * math.pi); fill_stroke(ctx, hexc('#2A1050'), 5)
    cols = ['#FFD23F', '#38E1FF', '#FFFFFF', '#7B5CFF']
    n = 7 if not odd else 6
    for i in range(n):
        a = i * 2 * math.pi / 7 + 0.3
        ctx.save(); ctx.translate(math.cos(a) * 21, math.sin(a) * 21); ctx.rotate(a * 2)
        ctx.rectangle(-5, -2, 10, 4); ctx.set_source_rgba(*hexc(cols[i % 4])); ctx.fill(); ctx.restore()
    ctx.restore()


ITEMS = dict(mug=mug, donut=donut)


def make_audio(cfg, dst):
    n = int(cfg['duration'] * sound.SR); bus = np.zeros(n + sound.SR)
    mus = sound.music(cfg.get('mood', 'tense'), cfg['duration'], cfg.get('seed', 5))
    reveal = cfg['seconds'] + cfg.get('start', 0.3)
    g = np.ones(len(mus)); ri = int(reveal * sound.SR); g[ri:] = 0.35
    bus[:len(mus)] += mus * g * 0.8
    for k in range(cfg['seconds']):
        sound.place(bus, sound.syn_tick(), cfg.get('start', 0.3) + k, 0.9)
        sound.place(bus, sound.syn_tick(), cfg.get('start', 0.3) + k + 0.5, 0.4)
    sound.place(bus, sound.syn_ding(), reveal, 1.0)
    sound.place(bus, sound.syn_sparkle(), reveal + 0.1, 0.6)
    bus = bus[:n]; peak = np.max(np.abs(bus)) + 1e-9
    bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
    k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
    with wave.open(dst, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
        w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


def render(path, frames=None):
    cfg = json.load(open(path)); epdir = os.path.dirname(os.path.abspath(path)); eid = cfg['id']
    cols, rows = cfg['cols'], cfg['rows']; ox, oy = cfg['odd']
    item = ITEMS[cfg['item']]
    top, bottom = 470, 1640
    cw = (W - 80) / cols; ch = (bottom - top) / rows
    s = min(cw, ch) / 104
    start = cfg.get('start', 0.3); secs = cfg['seconds']; reveal = start + secs
    r = np.random.default_rng(cfg.get('seed', 5))
    phase = r.uniform(0, 6.28, (cols, rows))

    def frame(fi):
        t = fi / FPS
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
        a, b = cfg.get('bg', ['#FFF1C9', '#FFD6E8'])
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
        ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
        kz = 0.0
        if t >= reveal:
            kz = min(1, (t - reveal) / 0.5); kz = 1 - (1 - kz) ** 3
        # zoom toward the odd one after reveal
        tx = 40 + cw * (ox + 0.5); ty = top + ch * (oy + 0.5)
        z = 1 + 1.4 * kz
        ctx.save()
        ctx.translate(W / 2 * kz + tx * (1 - kz), H / 2 * kz + ty * (1 - kz)); ctx.scale(z, z); ctx.translate(-tx, -ty)
        for i in range(cols):
            for j in range(rows):
                x = 40 + cw * (i + 0.5); y = top + ch * (j + 0.5)
                wob = 0.06 * math.sin(t * 3 + phase[i, j])
                ctx.save(); ctx.translate(x, y); item(ctx, s, (i, j) == (ox, oy), wob); ctx.restore()
        if t >= reveal:
            rr = max(cw, ch) * 0.62
            ctx.set_line_width(10 / z * 1.6); ctx.set_source_rgba(*hexc('#FF2E63'))
            ctx.arc(tx, ty, rr * (1.4 - 0.4 * kz), 0, 2 * math.pi); ctx.stroke()
        ctx.restore()
        # header
        text(ctx, cfg['title'], W / 2, 190, 86, hexc('#FFFFFF'), ink=hexc('#2A1636'), sw=18, shadow=hexc('#7B5CFF', 0.8))
        left = max(0.0, secs - max(0.0, t - start))
        if t < reveal:
            text(ctx, str(int(math.ceil(left))), W / 2, 370, 140 + 30 * (1 - (left % 1)), hexc('#FF2E63'), ink=hexc('#2A1636'), sw=20)
            # timer bar
            rrect(ctx, 120, 1730, W - 240, 44, 22); fill_stroke(ctx, hexc('#FFFFFF'), 8)
            rrect(ctx, 126, 1736, max(10, (W - 252) * left / secs), 32, 16); ctx.set_source_rgba(*hexc('#FF2E63')); ctx.fill()
        else:
            k = min(1, (t - reveal) * 3)
            text(ctx, cfg.get('reveal_text', 'THERE IT IS!'), W / 2, 380, 110, hexc('#3DDC84'), ink=hexc('#2A1636'), sw=20, scale=0.6 + 0.4 * k)
            text(ctx, cfg.get('end_text', 'Did you find it? Be honest'), W / 2, 1750, 66, hexc('#FFFFFF'), ink=hexc('#2A1636'), sw=14, alpha=k)
        return surf

    if frames:
        from PIL import Image
        ims = []
        for tt in frames:
            p_ = os.path.join(epdir, f'kf_{tt}.png'); frame(int(tt * FPS)).write_to_png(p_); ims.append(Image.open(p_))
        sheet = Image.new('RGB', (270 * len(ims), 480), 'white')
        for i, im in enumerate(ims): sheet.paste(im.convert('RGB').resize((270, 480)), (270 * i, 0))
        sheet.save(os.path.join(epdir, 'sheet.png')); print(os.path.join(epdir, 'sheet.png')); return
    wav = os.path.join(epdir, f'{eid}.wav'); make_audio(cfg, wav)
    silent = os.path.join(epdir, f'{eid}-silent.mp4')
    proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                             '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                             '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    for fi in range(int(cfg['duration'] * FPS)):
        proc.stdin.write(bytes(frame(fi).get_data()))
    proc.stdin.close(); proc.wait()
    out = os.path.join(epdir, f"{eid}-v{cfg.get('ver', 1)}.mp4")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', out], check=True)
    os.remove(silent); print(out)


if __name__ == '__main__':
    a = sys.argv[1:]; fr = None
    if '--frames' in a:
        i = a.index('--frames'); fr = [float(x) for x in a[i + 1:]]; a = a[:i]
    render(a[0], fr)
