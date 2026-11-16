"""Tiny Chaos bar-chart race (batch 5, 2026-11-17): relatable 'data' that races, re-ranks and ends on a punchline.

Usage: python engine/race.py episodes/<id>/race.json [--frames 0 3 6]
cfg: id, ver, duration, seed, mood, title, bg [a,b],
     clock {t0_min, t1_min, end_t}  (clock label runs from t0_min to t1_min minutes after midnight, stops at end_t),
     bars [{label, color, keys [[t, minutes], ...]}],  values interpolate (ease in-out) between keys,
     cards [[t0, t1, msg, y, size, color]], focus {label, t}: from t that bar flashes + gets a big pointer,
     unit_fmt "hm" (shows 2H 14M) or "{}" format string, footer.
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
from core import W, H, FPS, hexc, text, rrect, fill_stroke, FONT  # noqa: E402
import sound  # noqa: E402

INK = hexc('#2A1636')


def ease(k):
    k = min(1.0, max(0.0, k)); return k * k * (3 - 2 * k)


def value(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if a <= t <= b: return va + (vb - va) * ease((t - a) / max(1e-6, b - a))
    return keys[-1][1]


def fmt_val(v, f):
    if f == 'hm':
        m = int(round(v)); return f"{m // 60}H {m % 60:02d}M" if m >= 60 else f"{m}M"
    return f.format(int(round(v)))


def clock_label(m):
    m = int(m) % (24 * 60); h = m // 60; mm = m % 60
    ap = 'AM' if h < 12 else 'PM'; h12 = h % 12 or 12
    return f"{h12}:{mm:02d} {ap}"


class Race:
    def __init__(self, cfg):
        self.c = cfg; self.bars = cfg['bars']; n = len(self.bars)
        # precompute smoothed rank positions + swap events
        self.pos = []; self.swaps = []; cur = None; order_prev = None
        for fi in range(int((cfg['duration'] + 1) * FPS)):
            t = fi / FPS
            vals = [value(b['keys'], t) for b in self.bars]
            order = sorted(range(n), key=lambda i: -vals[i])
            rank = [0] * n
            for r, i in enumerate(order): rank[i] = r
            if cur is None: cur = [float(r) for r in rank]
            else: cur = [c + (r - c) * 0.22 for c, r in zip(cur, rank)]
            if order_prev is not None and order != order_prev and t > 0.1: self.swaps.append(t)
            order_prev = order
            self.pos.append((list(cur), vals))

    def frame(self, t):
        c = self.c
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
        a, b = c.get('bg', ['#101830', '#2A1450'])
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
        ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
        # faint grid
        ctx.set_source_rgba(1, 1, 1, 0.06); ctx.set_line_width(2)
        for x in range(120, W, 120):
            ctx.move_to(x, 540); ctx.line_to(x, 1560); ctx.stroke()
        fi = min(len(self.pos) - 1, int(t * FPS)); cur, vals = self.pos[fi]
        vmax = max(max(vals), 1.0)
        top, gap, bh = c.get('top', 560), c.get('gap', 172), c.get('bar_h', 132); x0 = 70; wmax = W - 140 - 230
        foc = c.get('focus'); fl = None
        if foc and t >= foc['t']: fl = foc['label']
        punch = 0.0
        for st in self.swaps:
            if 0 <= t - st < 0.25: punch = max(punch, 1 - (t - st) / 0.25)
        for i, bar in enumerate(self.bars):
            y = top + cur[i] * gap
            w = max(36, wmax * vals[i] / vmax)
            col = bar['color']; is_f = fl == bar['label']
            if is_f:
                k = 0.5 + 0.5 * math.sin((t - foc['t']) * 14)
                rrect(ctx, x0 - 12, y - 12, w + 24, bh + 24, 30); ctx.set_source_rgba(1, 0.9, 0.3, 0.35 + 0.4 * k); ctx.fill()
            rrect(ctx, x0, y, w, bh, 24); fill_stroke(ctx, hexc(col), 8)
            ctx.select_font_face(FONT); ctx.set_font_size(52)
            lw = ctx.text_extents(bar['label']).x_advance
            if lw + 50 < w:
                text(ctx, bar['label'], x0 + 26 + lw / 2, y + bh / 2, 52, hexc('#FFFFFF'), ink=INK, sw=12)
                vx = x0 + w + 20
            else:  # label outside, value after it
                text(ctx, bar['label'], x0 + w + 20 + lw / 2, y + bh / 2, 52, hexc('#FFFFFF'), ink=INK, sw=12)
                vx = x0 + w + 40 + lw
            vs = fmt_val(vals[i], c.get('unit_fmt', 'hm'))
            ctx.set_font_size(46); vw = ctx.text_extents(vs).x_advance
            vx = min(vx, W - 30 - vw)
            text(ctx, vs, vx + vw / 2, y + bh / 2, 46, hexc('#FFE14D' if not is_f else '#FF5A5F'), ink=INK, sw=10,
                 scale=1 + (0.25 * (0.5 + 0.5 * math.sin(t * 14)) if is_f else 0))
        # header + clock
        text(ctx, c['title'], W / 2, 175, 80, hexc('#FFFFFF'), ink=INK, sw=18, shadow=hexc('#000000', 0.4))
        ck = c.get('clock')
        if ck:
            kt = min(1, t / ck['end_t']); m = ck['t0_min'] + (ck['t1_min'] - ck['t0_min']) * kt
            rrect(ctx, W / 2 - 230, 330, 460, 130, 40); fill_stroke(ctx, hexc('#FFFFFF'), 8)
            text(ctx, clock_label(m), W / 2, 397, 92 + 10 * punch, hexc('#FF5A5F'), ink=INK, sw=0)
        for (t0, t1, msg, y, size, col) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(col), ink=INK, sw=18, scale=0.6 + 0.4 * k, rot=-0.04,
                     shadow=hexc('#000000', 0.5))
        if c.get('footer') and not (foc and t >= foc['t']):
            text(ctx, c['footer'], W / 2, 1720, 54, hexc('#FFFFFF'), ink=INK, sw=12)
        return surf

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        mus = sound.music(c.get('mood', 'playful'), c['duration'], c.get('seed', 3))
        gm = np.ones(len(mus)); foc = c.get('focus')
        if foc: gm[int(foc['t'] * sound.SR):] = 0.25
        bus[:len(mus)] += mus * gm * 0.75
        last = -9
        for st in self.swaps:
            if st - last > 0.12:
                sound.place(bus, sound.syn_pop(0.08, 600 + 80 * (len(self.swaps) % 5), 1300), st, 0.5); last = st
        ck = c.get('clock')
        if ck:
            for k in range(int(ck['end_t'] / 0.5)):
                sound.place(bus, sound.syn_tick(), 0.25 + k * 0.5, 0.25)
        if foc:
            sound.place(bus, sound.syn_slide(False, 0.7), foc['t'], 0.8)
            for (t0, _t1, _m, _y, _s, _c) in c.get('cards', []):
                if t0 >= foc['t']: sound.place(bus, sound.syn_thud(), t0, 0.7)
        for (t0, _t1, _m, _y, _s, _c) in c.get('cards', []):
            if not foc or t0 < foc['t']: sound.place(bus, sound.syn_swoosh(0.3), t0, 0.5)
        bus = bus[:n]; peak = np.max(np.abs(bus)) + 1e-9
        bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
        k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
        with wave.open(dst, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
            w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


def render(path, frames=None):
    cfg = json.load(open(path)); epdir = os.path.dirname(os.path.abspath(path)); eid = cfg['id']
    r = Race(cfg)
    if frames:
        from PIL import Image
        ims = []
        for tt in frames:
            p_ = os.path.join(epdir, f'kf_{tt}.png'); r.frame(tt).write_to_png(p_); ims.append(Image.open(p_))
        sheet = Image.new('RGB', (270 * len(ims), 480), 'white')
        for i, im in enumerate(ims): sheet.paste(im.convert('RGB').resize((270, 480)), (270 * i, 0))
        sheet.save(os.path.join(epdir, 'sheet.png')); print(os.path.join(epdir, 'sheet.png')); return
    wav = os.path.join(epdir, f'{eid}.wav'); r.audio(wav)
    encode(lambda fi: r.frame(fi / FPS), cfg, epdir, wav)


def encode(frame_fn, cfg, epdir, wav):
    eid = cfg['id']; silent = os.path.join(epdir, f'{eid}-silent.mp4')
    proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                             '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                             '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    for fi in range(int(cfg['duration'] * FPS)):
        proc.stdin.write(bytes(frame_fn(fi).get_data()))
    proc.stdin.close(); proc.wait()
    out = os.path.join(epdir, f"{eid}-v{cfg.get('ver', 1)}.mp4")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', out], check=True)
    os.remove(silent); os.remove(wav); print(out)


if __name__ == '__main__':
    a = sys.argv[1:]; fr = None
    if '--frames' in a:
        i = a.index('--frames'); fr = [float(x) for x in a[i + 1:]]; a = a[:i]
    render(a[0], fr)
