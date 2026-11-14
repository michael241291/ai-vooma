"""Tiny Chaos mini-games (batch 4, 2026-11-15).

shell: classic cup shuffle. An object (keys, a cookie...) is slammed under a cup at frame 0, the cups swap faster and
faster, the viewer picks 1/2/3, then the cups lift. The shuffle is fair: the object really follows its cup.

Usage: python engine/games.py episodes/<id>/game.json [--frames 0 2 5]
cfg: id, ver, title, object ("keys"|"cookie"), start_slot, swaps [[a, b], ...] (slot pairs), swap_t0, swap_d0, swap_d1,
     ask_t, reveal_t, duration, seed, mood, bg [a, b], cup_color, cards [[t0, t1, msg, y, size, color]]
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
from core import W, H, FPS, hexc, text, rrect, fill_stroke, ellipse  # noqa: E402
import sound  # noqa: E402

INK = hexc('#2A1636')
SLOTS = [210, 540, 870]
BASE = 1250


def ease(k):
    k = min(1, max(0, k)); return k * k * (3 - 2 * k)


class Shell:
    def __init__(self, c):
        self.c = c
        n = len(c['swaps']); t = c.get('swap_t0', 1.0)
        d0, d1 = c.get('swap_d0', 0.6), c.get('swap_d1', 0.22)
        self.moves = []  # (t0, d, a, b)
        for i, (a, b) in enumerate(c['swaps']):
            d = d0 + (d1 - d0) * (i / max(1, n - 1))
            self.moves.append((t, d, a, b)); t += d + 0.04
        self.shuffle_end = t
        # cup i sits in slot i at start; track which cup is in which slot
        self.order = [list(range(3))]
        cur = list(range(3))
        for (_t, _d, a, b) in self.moves:
            cur = cur[:]; cur[a], cur[b] = cur[b], cur[a]; self.order.append(cur)
        self.ocup = c.get('start_slot', 1)  # the cup that hides the object
        self.final_slot = self.order[-1].index(self.ocup)
        print('object ends in slot', self.final_slot + 1, 'shuffle ends', round(t, 2))

    def cup_pos(self, cup, t):
        """x, y, lift for one cup at time t."""
        slot = self.order[0].index(cup); x = SLOTS[slot]; y = BASE
        for i, (t0, d, a, b) in enumerate(self.moves):
            prev = self.order[i]; nxt = self.order[i + 1]
            if t < t0: break
            s0 = prev.index(cup); s1 = nxt.index(cup)
            if t >= t0 + d:
                x = SLOTS[s1]; y = BASE; continue
            k = ease((t - t0) / d)
            x = SLOTS[s0] + (SLOTS[s1] - SLOTS[s0]) * k
            if s0 != s1:
                y = BASE + (120 if s1 > s0 else -120) * math.sin(math.pi * k)
            break
        lift = 0.0
        c = self.c
        # slam at the start: the hiding cup drops onto the object
        if cup == self.ocup:
            lift = max(0.0, 1 - t / c.get('slam', 0.45)) ** 2
        rt = c['reveal_t']
        slot_now = self.order[-1].index(cup)
        order = [s for s in range(3) if s != self.final_slot] + [self.final_slot]
        k = order.index(slot_now)
        tl = rt + 0.55 * k
        if t > tl:
            lift = max(lift, ease((t - tl) / 0.35))
        return x, y, lift

    def draw_cup(self, ctx, x, y, lift, col):
        yy = y - lift * 360
        ctx.save(); ctx.translate(x, yy)
        ctx.move_to(-120, 0); ctx.line_to(-80, -300); ctx.line_to(80, -300); ctx.line_to(120, 0); ctx.close_path()
        fill_stroke(ctx, hexc(col), 9, INK)
        ctx.move_to(-108, -60); ctx.line_to(-100, -110); ctx.line_to(100, -110); ctx.line_to(108, -60); ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 0.85); ctx.fill()
        ellipse(ctx, 0, -300, 80, 16); fill_stroke(ctx, hexc(col), 7, INK)
        ctx.move_to(-60, -270); ctx.line_to(-80, -30); ctx.set_line_width(14); ctx.set_source_rgba(1, 1, 1, 0.25); ctx.stroke()
        ellipse(ctx, 0, 0, 120, 20); ctx.set_source_rgba(*hexc(col)); ctx.fill_preserve(); ctx.set_source_rgba(*INK); ctx.set_line_width(9); ctx.stroke()
        ctx.restore()

    def draw_object(self, ctx, x, y, t):
        ctx.save(); ctx.translate(x, y - 10)
        if self.c.get('object', 'keys') == 'keys':
            ctx.arc(-30, -40, 32, 0, 2 * math.pi); ctx.set_line_width(12); ctx.set_source_rgba(*INK); ctx.stroke()
            ctx.arc(-30, -40, 32, 0, 2 * math.pi); ctx.set_line_width(6); ctx.set_source_rgba(*hexc('#D6DEE6')); ctx.stroke()
            for k, (col, ang) in enumerate((('#FFC93C', -0.5), ('#C0C8D0', 0.35))):
                ctx.save(); ctx.translate(-30 + math.cos(ang) * 32, -40 + math.sin(ang) * 32); ctx.rotate(ang)
                ctx.arc(14, 0, 18, 0, 2 * math.pi); fill_stroke(ctx, hexc(col), 6, INK)
                rrect(ctx, 28, -7, 70, 14, 4); fill_stroke(ctx, hexc(col), 6, INK)
                ctx.rectangle(70, 6, 9, 10); ctx.rectangle(84, 6, 9, 8); ctx.set_source_rgba(*hexc(col)); ctx.fill()
                ctx.restore()
        ctx.restore()

    def draw(self, ctx, t):
        c = self.c
        a, b = c.get('bg', ['#1E6F5C', '#0B3D33'])
        g = cairo.RadialGradient(540, 1000, 100, 540, 1000, 1300)
        g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
        ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
        # table
        ctx.rectangle(0, BASE - 20, W, 700); ctx.set_source_rgba(*hexc('#8B5A3C')); ctx.fill()
        ctx.rectangle(0, BASE - 20, W, 16); ctx.set_source_rgba(*hexc('#5E3A24')); ctx.fill()
        moving = any(t0 <= t < t0 + d for (t0, d, _a, _b) in self.moves)
        z = 1.2 + (0.04 if moving else 0) + 0.08 * max(0, 1 - abs(t - c['reveal_t'] - 1.4))
        ctx.save(); ctx.translate(540, 1150); ctx.scale(z, z); ctx.translate(-540, -1150)
        for i in range(3):
            ellipse(ctx, SLOTS[i], BASE + 6, 130, 22); ctx.set_source_rgba(0, 0, 0, 0.25); ctx.fill()
        # object under its cup (drawn first, follows the cup)
        ox, oy, _l = self.cup_pos(self.ocup, t)
        self.draw_object(ctx, ox, oy, t)
        if t > c['reveal_t'] + 1.2:
            k = min(1, (t - c['reveal_t'] - 1.2) * 3)
            for i in range(10):
                an = i * math.pi / 5 + t
                ctx.arc(ox + math.cos(an) * 160 * k, oy - 60 + math.sin(an) * 120 * k, 8, 0, 2 * math.pi)
                ctx.set_source_rgba(*hexc('#FFE14D', 1 - k * 0.5)); ctx.fill()
        cols = c.get('cup_colors', ['#E63946', '#E63946', '#E63946'])
        for cup in range(3):
            x, y, lift = self.cup_pos(cup, t)
            self.draw_cup(ctx, x, y, lift, cols[cup])
        ctx.restore()
        # HUD
        text(ctx, c['title'], W / 2, 210, 86, hexc('#FFFFFF'), ink=INK, sw=18, shadow=hexc('#000000', 0.4))
        done = sum(1 for (t0, d, _a, _b) in self.moves if t >= t0 + d)
        if t < self.shuffle_end + 0.1:
            text(ctx, f"SWAP {done}/{len(self.moves)}", W / 2, 420, 70, hexc('#FFE14D'), ink=INK, sw=14)
        if c['ask_t'] <= t < c['reveal_t'] + 0.2:
            for i in range(3):
                kk = min(1, (t - c['ask_t'] - 0.12 * i) * 4)
                if kk > 0:
                    ctx.arc(SLOTS[i], BASE + 180, 70 * kk, 0, 2 * math.pi); fill_stroke(ctx, hexc('#FFD23F'), 8, INK)
                    text(ctx, str(i + 1), SLOTS[i], BASE + 182, 90 * kk, hexc('#FFFFFF'), ink=INK, sw=12)
            left = c['reveal_t'] - t
            text(ctx, 'WHICH CUP?', W / 2, 420, 100 + 8 * math.sin(t * 10), hexc('#FFFFFF'), ink=INK, sw=18)
            text(ctx, str(max(1, int(math.ceil(left)))), W / 2, 560, 90, hexc('#FF5A5F'), ink=INK, sw=14)
        for (t0, t1, msg, y, size, col) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(col), ink=INK, sw=16, scale=0.6 + 0.4 * k, rot=-0.03, shadow=hexc('#000000', 0.45))

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        mus = sound.music(c.get('mood', 'tense'), c['duration'], c.get('seed', 6))
        gm = np.ones(len(mus)); gm[int(c['ask_t'] * sound.SR):int((c['reveal_t'] + 1.2) * sound.SR)] = 0.25
        bus[:len(mus)] += mus * gm * 0.55
        sound.place(bus, sound.syn_thud(), c.get('slam', 0.45), 1.0)
        for (t0, d, _a, _b) in self.moves:
            sound.place(bus, sound.syn_swoosh(max(0.18, d)), t0, 0.45)
            sound.place(bus, sound.syn_thud(), t0 + d, 0.25)
        tk = c['ask_t']
        while tk < c['reveal_t']:
            sound.place(bus, sound.syn_tick(), tk, 0.9); tk += 0.5
        for k in range(3):
            sound.place(bus, sound.syn_slide(True, 0.3), c['reveal_t'] + 0.55 * k, 0.4)
        sound.place(bus, sound.syn_ding(), c['reveal_t'] + 1.2, 1.0)
        sound.place(bus, sound.syn_sparkle(), c['reveal_t'] + 1.25, 0.7)
        bus = bus[:n]; peak = np.max(np.abs(bus)) + 1e-9
        bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
        k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
        with wave.open(dst, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
            w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


def render(path, frames=None):
    cfg = json.load(open(path)); epdir = os.path.dirname(os.path.abspath(path)); eid = cfg['id']
    g = Shell(cfg)

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
