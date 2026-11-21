"""Tiny Chaos memory test (batch 6, 2026-11-22): memorize a grid, the lights flicker, ONE item changes.
The viewer comments the number before the reveal (commit-before-reveal CTA, the keys-cup-shuffle lesson).

Usage: python engine/memory.py episodes/<id>/memory.json [--frames 0 3 6]
cfg: id, ver, title, items [{box, ribbon, pattern (plain|dots|stripes|stars), bow (round|flat)}], change {i, key, value},
     look_t (end of memorize phase), ask_t, reveal_t, duration, seed, mood, bg [a, b], cards [[t0, t1, msg, y, size, color]]
Items are gift boxes (2 cols x 3 rows) numbered 1..6.
"""
import copy
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

INK = hexc('#2A1636')
COLS = [300, 780]
ROWS = [720, 1080, 1440]


def ease(k):
    k = min(1, max(0, k)); return k * k * (3 - 2 * k)


def gift(ctx, x, y, g, s=1.0, wob=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(wob); ctx.scale(s, s)
    w, h = 300, 220
    rrect(ctx, -w / 2, -h / 2, w, h, 16); fill_stroke(ctx, hexc(g['box']), 8, INK)
    ctx.save(); rrect(ctx, -w / 2 + 4, -h / 2 + 4, w - 8, h - 8, 14); ctx.clip()
    pat = g.get('pattern', 'plain'); pc = hexc(g.get('pcol', '#FFFFFF'), 0.75)
    if pat == 'dots':
        for i in range(-3, 4):
            for j in range(-2, 3):
                ctx.arc(i * 46 + (j % 2) * 23, j * 46, 9, 0, 2 * math.pi); ctx.set_source_rgba(*pc); ctx.fill()
    elif pat == 'stripes':
        for i in range(-8, 9):
            ctx.move_to(i * 40, -h); ctx.line_to(i * 40 + h, h); ctx.set_line_width(13); ctx.set_source_rgba(*pc); ctx.stroke()
    elif pat == 'stars':
        for i in range(-3, 4):
            for j in range(-2, 3):
                cx, cy = i * 52 + (j % 2) * 26, j * 50
                for k in range(5):
                    a = -math.pi / 2 + k * 4 * math.pi / 5
                    (ctx.move_to if k == 0 else ctx.line_to)(cx + 13 * math.cos(a), cy + 13 * math.sin(a))
                ctx.close_path(); ctx.set_source_rgba(*pc); ctx.fill()
    ctx.restore()
    rc = hexc(g['ribbon'])
    ctx.rectangle(-22, -h / 2, 44, h); fill_stroke(ctx, rc, 6, INK)
    ctx.rectangle(-w / 2, -22, w, 44); fill_stroke(ctx, rc, 6, INK)
    # bow on top
    if g.get('bow', 'round') == 'round':
        for sx in (-1, 1):
            ctx.save(); ctx.translate(sx * 46, -h / 2 - 22); ctx.scale(1.3, 0.8)
            ctx.arc(0, 0, 36, 0, 2 * math.pi); ctx.restore(); fill_stroke(ctx, rc, 7, INK)
    else:
        for sx in (-1, 1):
            ctx.move_to(0, -h / 2 - 10); ctx.line_to(sx * 80, -h / 2 - 50); ctx.line_to(sx * 70, -h / 2 + 6); ctx.close_path()
            fill_stroke(ctx, rc, 7, INK)
    ctx.arc(0, -h / 2 - 18, 22, 0, 2 * math.pi); fill_stroke(ctx, rc, 7, INK)
    ctx.restore()


class Memory:
    def __init__(self, c):
        self.c = c
        self.before = c['items']
        self.after = copy.deepcopy(c['items'])
        ch = c['change']; self.after[ch['i']][ch['key']] = ch['value']

    def pos(self, i):
        return COLS[i % 2], ROWS[i // 2]

    def draw(self, ctx, t):
        c = self.c
        a, b = c.get('bg', ['#1E6F5C', '#0B3D33'])
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
        ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
        lt, at, rt = c['look_t'], c['ask_t'], c['reveal_t']
        items = self.before if t < lt + 0.25 else self.after
        # lights-off flicker between look_t and ask_t
        dark = 0.0
        if lt <= t < at:
            k = (t - lt) / (at - lt)
            dark = 1.0 if k < 0.55 else (0.0 if int(k * 14) % 2 else 0.85)
        ch = c['change']['i']
        for i, gi in enumerate(items):
            x, y = self.pos(i)
            wob = 0.03 * math.sin(t * 3 + i * 1.7)
            s = 1.0
            if t < 0.5:  # frame 0: boxes already bouncing in place
                s = 1.0 + 0.08 * math.sin(t * 20 + i) * (1 - t / 0.5)
            if t >= rt and i == ch:
                k = ease((t - rt) / 0.4); s = 1 + 0.18 * k; wob = 0.08 * math.sin(t * 18) * k
            gift(ctx, x, y, gi, s, wob)
            # number tag
            ctx.arc(x - 150, y - 110, 44, 0, 2 * math.pi); fill_stroke(ctx, hexc('#FFD23F'), 7, INK)
            text(ctx, str(i + 1), x - 150, y - 108, 60, hexc('#FFFFFF'), ink=INK, sw=10)
            if t >= rt + 0.3 and i != ch:
                rrect(ctx, x - 165, y - 125, 330, 250, 20); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()
        if t >= rt + 0.3:
            x, y = self.pos(ch); k = ease((t - rt - 0.3) / 0.4)
            ctx.arc(x, y, 230 * k + 1, 0, 2 * math.pi); ctx.set_line_width(14); ctx.set_source_rgba(*hexc('#3DDC84')); ctx.stroke()
            if t >= rt + 1.0:
                ph = int((t - rt - 1.0) / 0.6) % 2
                gg = self.before[ch] if ph == 0 else self.after[ch]
                gift(ctx, x, y, gg, 1.18)
                ctx.arc(x - 150, y - 110, 44, 0, 2 * math.pi); fill_stroke(ctx, hexc('#FFD23F'), 7, INK)
                text(ctx, str(ch + 1), x - 150, y - 108, 60, hexc('#FFFFFF'), ink=INK, sw=10)
                text(ctx, 'BEFORE' if ph == 0 else 'AFTER', x, y + 175, 64, hexc('#FFFFFF' if ph == 0 else '#3DDC84'), ink=INK, sw=12)
        if dark > 0:
            ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.02, 0.01, 0.05, dark); ctx.fill()
            if dark > 0.9:
                text(ctx, 'LIGHTS OUT...', W / 2, 960, 110, hexc('#FFE14D'), ink=INK, sw=18)
        # HUD
        text(ctx, c['title'], W / 2, 200, 84, hexc('#FFFFFF'), ink=INK, sw=18, shadow=hexc('#000000', 0.4))
        if t < lt:
            left = lt - t
            text(ctx, f"MEMORIZE: {int(math.ceil(left))}", W / 2, 430, 84, hexc('#FFE14D'), ink=INK, sw=16)
        elif at <= t < rt:
            text(ctx, c.get('ask', 'WHICH ONE CHANGED?'), W / 2, 400, 80 + 6 * math.sin(t * 9), hexc('#FFFFFF'), ink=INK, sw=16)
            text(ctx, str(max(1, int(math.ceil(rt - t)))), W / 2, 510, 80, hexc('#FF5A5F'), ink=INK, sw=14)
        for (t0, t1, msg, y, size, col) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(col), ink=INK, sw=16, scale=0.6 + 0.4 * k, rot=-0.03, shadow=hexc('#000000', 0.45))

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        mus = sound.music(c.get('mood', 'sneaky'), c['duration'], c.get('seed', 6))
        gm = np.ones(len(mus))
        gm[int(c['look_t'] * sound.SR):int(c['ask_t'] * sound.SR)] = 0.0
        gm[int(c['ask_t'] * sound.SR):int((c['reveal_t'] + 1.0) * sound.SR)] = 0.3
        bus[:len(mus)] += mus * gm * 0.55
        for i in range(6):
            sound.place(bus, sound.syn_pop(), 0.02 + 0.05 * i, 0.5)
        tk = 1.0
        while tk < c['look_t']:
            sound.place(bus, sound.syn_tick(), tk, 0.7); tk += 1.0
        sound.place(bus, sound.syn_thud(), c['look_t'], 1.0)
        sound.place(bus, sound.syn_static(0.5), c['look_t'] + 0.55 * (c['ask_t'] - c['look_t']), 0.4)
        tk = c['ask_t']
        while tk < c['reveal_t']:
            sound.place(bus, sound.syn_tick(), tk, 0.9); tk += 0.5
        sound.place(bus, sound.syn_ding(), c['reveal_t'], 1.0)
        sound.place(bus, sound.syn_sparkle(), c['reveal_t'] + 0.05, 0.7)
        sound.place(bus, sound.syn_swoosh(0.3), c['reveal_t'] + 1.0, 0.5)
        bus = bus[:n]; peak = np.max(np.abs(bus)) + 1e-9
        bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
        k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
        with wave.open(dst, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
            w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


def render(path, frames=None):
    cfg = json.load(open(path)); epdir = os.path.dirname(os.path.abspath(path)); eid = cfg['id']
    g = Memory(cfg)

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
