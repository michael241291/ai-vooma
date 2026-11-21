"""Tiny Chaos spot-the-difference on a real photo (batch 6, 2026-11-22).

The same Pixabay photo is shown twice (top / bottom panel). Cartoon props drawn from world.PROPS sit on the photo;
some props differ between panels. Countdown, then "COMMENT YOUR SCORE 0-3" (commit-before-reveal), then rings.

Usage: python engine/spotphoto.py episodes/<id>/spot.json [--frames 0 3 9]
cfg: id, ver, photo, title, sub, seconds (countdown), ask_t, reveal_t, duration, seed, mood, bg, dim,
     props [{type, x, y, scale, top {params}, bottom {params}}]  (x, y in photo pixels; params None = absent in that panel)
     diffs [[x, y, r]] (photo pixels, ring order), cards [[t0, t1, msg, y, size, color]]
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
import world  # noqa: E402
import extra  # noqa: E402,F401
import extra3  # noqa: E402,F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = hexc('#2A1636')
PANELS = [(70, 330, 940, 622), (70, 985, 940, 622)]


def ease(k):
    k = min(1, max(0, k)); return k * k * (3 - 2 * k)


class Spot:
    def __init__(self, c):
        self.c = c
        self.img = cairo.ImageSurface.create_from_png(self._png(c['photo']))
        self.iw, self.ih = self.img.get_width(), self.img.get_height()

    def _png(self, path):
        p = os.path.join(ROOT, path)
        out = p + '.png'
        if not os.path.exists(out):
            from PIL import Image
            Image.open(p).convert('RGB').save(out)
        return out

    def panel(self, ctx, t, k):
        x, y, w, h = PANELS[k]; c = self.c
        ctx.save()
        rrect(ctx, x, y, w, h, 22); ctx.clip()
        s = max(w / self.iw, h / self.ih)
        ctx.translate(x + w / 2, y + h / 2); ctx.scale(s, s); ctx.translate(-self.iw / 2, -self.ih / 2)
        ctx.set_source_surface(self.img, 0, 0); ctx.paint()
        ctx.rectangle(0, 0, self.iw, self.ih); ctx.set_source_rgba(0, 0, 0, c.get('dim', 0.08)); ctx.fill()
        side = 'top' if k == 0 else 'bottom'
        for pr in c['props']:
            pp = pr.get(side)
            if pp is None:
                continue
            ctx.save(); ctx.translate(pr['x'], pr['y']); sc = pr.get('scale', 1.0); ctx.scale(sc, sc)
            world.PROPS[pr['type']](ctx, t, dict(pp))
            ctx.restore()
        if k == 1 and t >= c['reveal_t']:
            for i, (dx, dy, r) in enumerate(c['diffs']):
                kk = ease((t - c['reveal_t'] - 0.5 * i) / 0.35)
                if kk <= 0:
                    continue
                ctx.new_path(); ctx.arc(dx, dy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * kk)
                ctx.set_line_width(14); ctx.set_source_rgba(*hexc('#FF2E63')); ctx.stroke()
                if kk >= 1:
                    text(ctx, str(i + 1), dx + r * 0.75, dy - r * 0.75, 70, hexc('#FFFFFF'), ink=INK, sw=12)
        ctx.restore()
        rrect(ctx, x, y, w, h, 22); ctx.set_line_width(10); ctx.set_source_rgba(*hexc('#FFFFFF')); ctx.stroke()

    def draw(self, ctx, t):
        c = self.c
        a, b = c.get('bg', ['#FF8A5B', '#B83B5E'])
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
        ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
        # frame 0 punch-in so the opening moves
        z = 1 + 0.04 * max(0, 1 - t / 0.6)
        ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2)
        for k in range(2):
            self.panel(ctx, t, k)
        ctx.restore()
        secs = c['seconds']
        if t < secs:
            left = 1 - t / secs
            rrect(ctx, 150, 958, 780, 22, 11); ctx.set_source_rgba(0, 0, 0, 0.35); ctx.fill()
            rrect(ctx, 150, 958, 780 * left, 22, 11); ctx.set_source_rgba(*hexc('#FFE14D' if left > 0.3 else '#FF5A5F')); ctx.fill()
            text(ctx, c['title'], W / 2, 215, 88, hexc('#FFE14D'), ink=INK, sw=18, scale=1 + 0.03 * math.sin(t * 8))
            text(ctx, f"{c.get('sub', 'IN')} {int(math.ceil(secs - t))} SECONDS", W / 2, 290, 56, hexc('#FFFFFF'), ink=INK, sw=12)
        elif t < c['reveal_t']:
            text(ctx, 'TIME!', W / 2, 215, 110, hexc('#FF5A5F'), ink=INK, sw=18)
            text(ctx, c.get('ask', 'COMMENT YOUR SCORE: 0, 1, 2 OR 3'), W / 2, 295, 48, hexc('#FFFFFF'), ink=INK, sw=10)
        for (t0, t1, msg, y, size, col) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(col), ink=INK, sw=16, scale=0.6 + 0.4 * k, rot=-0.03, shadow=hexc('#000000', 0.45))

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        mus = sound.music(c.get('mood', 'sneaky'), c['duration'], c.get('seed', 6))
        gm = np.ones(len(mus)); gm[int(c['seconds'] * sound.SR):int(c['reveal_t'] * sound.SR)] = 0.25
        bus[:len(mus)] += mus * gm * 0.55
        sound.place(bus, sound.syn_pop(), 0.02, 0.7)
        for k in range(int(c['seconds'])):
            sound.place(bus, sound.syn_tick(), k + 0.02, 0.7)
        sound.place(bus, sound.syn_ding(), c['seconds'], 0.9)
        tk = c['seconds'] + 0.5
        while tk < c['reveal_t']:
            sound.place(bus, sound.syn_heartbeat(), tk, 0.6); tk += 0.8
        for i in range(len(c['diffs'])):
            sound.place(bus, sound.syn_swoosh(0.3), c['reveal_t'] + 0.5 * i, 0.5)
            sound.place(bus, sound.syn_pop(), c['reveal_t'] + 0.5 * i + 0.33, 0.7)
        sound.place(bus, sound.syn_sparkle(), c['reveal_t'] + 0.5 * len(c['diffs']), 0.7)
        bus = bus[:n]; peak = np.max(np.abs(bus)) + 1e-9
        bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
        k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
        with wave.open(dst, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
            w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


def render(path, frames=None):
    cfg = json.load(open(path)); epdir = os.path.dirname(os.path.abspath(path)); eid = cfg['id']
    g = Spot(cfg)

    def frame(fi):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s); g.draw(ctx, fi / FPS); return s
    if frames:
        from PIL import Image
        ims = []
        for tt in frames:
            p_ = os.path.join(epdir, f'kf_{tt}.png'); frame(int(tt * FPS)).write_to_png(p_); ims.append(Image.open(p_))
        sheet = Image.new('RGB', (270 * len(ims), 480), 'white')
        for i, im in enumerate(ims): sheet.paste(im.convert('RGB').resize((270, 480)), (270 * i, 0))
        sheet.save(os.path.join(epdir, 'sheet.png')); print(os.path.join(epdir, 'sheet.png')); return
    wav = os.path.join(epdir, f'{eid}.wav'); g.audio(wav)
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
    os.remove(silent); os.remove(wav); print(out)


if __name__ == '__main__':
    a = sys.argv[1:]; fr = None
    if '--frames' in a:
        i = a.index('--frames'); fr = [float(x) for x in a[i + 1:]]; a = a[:i]
    render(a[0], fr)
