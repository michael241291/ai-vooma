"""Tiny Chaos simulations, batch 4 (2026-11-15): three new code-native modes.

  plinko : labelled balls (hours, dollars...) drop through a peg board into labelled bins. Each ball has a target bin
           (soft steering), so the final counts tell the joke. The last ball runs in slow motion.
  duel   : two labelled balls fight in an arena; HP bars on top; a scripted mid-video flip (e.g. COFFEE -> DECAF).
  grow   : a labelled ball bounces in a ring and GROWS with every wall hit (food labels), until the ring cracks.

Usage: python engine/sims2.py episodes/<id>/sim.json [--frames 0 2 5]
All motion is a deterministic simulation: the same cfg always renders the same video.
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
import sims  # noqa: E402

INK = hexc('#2A1636')


def grad_bg(ctx, a, b, t, dots=True):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
    ctx.rectangle(-200, -200, W + 400, H + 400); ctx.set_source(g); ctx.fill()
    if dots:
        ctx.set_source_rgba(1, 1, 1, 0.07)
        for i in range(50):
            x = (i * 211 + 37) % W; y = (i * 389 + int(t * 25 * (1 + i % 3))) % H
            ctx.arc(x, y, 3 + i % 4, 0, 2 * math.pi); ctx.fill()


def finish_audio(bus, n, dst):
    bus = bus[:n]
    peak = np.max(np.abs(bus)) + 1e-9
    bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
    k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
    with wave.open(dst, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
        w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


def pad(bus, n, root=48, g=0.03):
    tt = np.arange(n) / sound.SR
    bus[:n] += sum(np.sin(2 * np.pi * sound.midi(root + k) * tt) for k in (0, 7, 12)) * g * np.minimum(1, tt / 0.5)


# =============================== PLINKO ===============================
class Plinko:
    def __init__(self, cfg):
        self.c = cfg
        self.rows = cfg.get('rows', 9); self.top = cfg.get('peg_top', 600); self.gap = cfg.get('peg_gap', 82)
        self.dx = cfg.get('peg_dx', 104); self.pr = cfg.get('peg_r', 13); self.br = cfg.get('ball_r', 27)
        self.bins = cfg['bins']  # [[label, color], ...]
        self.nb = len(self.bins); self.bx0, self.bx1 = 50, W - 50
        self.bw = (self.bx1 - self.bx0) / self.nb
        self.bin_top = self.top + self.gap * (self.rows - 1) + 70; self.floor = cfg.get('floor', 1610)
        self.pegs = []
        for r in range(self.rows):
            y = self.top + r * self.gap
            off = 0 if r % 2 == 0 else self.dx / 2
            x = W / 2 - self.dx * 5 + off
            while x < W - 60:
                if x > 60: self.pegs.append((x, y))
                x += self.dx
        for i in range(1, self.nb):  # rounded divider tips act as pegs too
            self.pegs.append((self.bx0 + i * self.bw, self.bin_top))
        self.simulate()

    def tmap(self, t):
        """video time -> sim time (slow motion for the last ball)."""
        a, b, k = self.c.get('slowmo', [99, 99, 1.0])
        if t <= a: return t
        if t <= b: return a + (t - a) * k
        return a + (b - a) * k + (t - b)

    def simulate(self):
        c = self.c; balls = c['balls']  # [[label, bin_index], ...]
        every = c.get('every', 0.55); pre = c.get('preroll', 1.3)
        g = c.get('gravity', 2600.0); dt = 1 / 240
        self.paths = []; self.hits = []; self.lands = []
        counts = [0] * self.nb
        for i, (lab, tb) in enumerate(balls):
            t0 = i * every - pre
            if i == len(balls) - 1: t0 += c.get('last_delay', 0.6)
            p = np.array([W / 2 + 18 * math.sin(i * 2.3), 330.0]); v = np.array([60 * math.cos(i * 1.7), 0.0])
            tx = self.bx0 + (tb + 0.5) * self.bw
            path = []; t = t0; landed = None; inbin = None; last = -9
            fake = c.get('fake_target') if i == len(balls) - 1 else None
            while t < c['duration'] + 3:
                if landed is None:
                    v[1] += g * dt
                    tgt = tx
                    if fake is not None and p[1] < self.bin_top - self.c.get('fake_until', 120):
                        tgt = self.bx0 + (fake + 0.5) * self.bw
                    if self.top - 40 < p[1] < self.bin_top + 10:
                        v[0] += ((tgt - p[0]) * c.get('steer', 30.0) - v[0] * c.get('damp', 7.0)) * dt
                    p += v * dt
                    for (qx, qy) in self.pegs:
                        d = p - np.array([qx, qy]); dist = np.hypot(*d)
                        if dist < self.br + self.pr:
                            n = d / max(dist, 1e-6); p = np.array([qx, qy]) + n * (self.br + self.pr)
                            vn = np.dot(v, n)
                            if vn < 0:
                                v = v - self.c.get('bounce', 1.3) * vn * n
                                if t - last > 0.05 and t > -0.05:
                                    self.hits.append((t, i)); last = t
                    p[0] = min(max(p[0], 60 + self.br), W - 60 - self.br)
                    if p[1] > self.bin_top + 20:
                        if inbin is None:
                            inbin = int(min(self.nb - 1, max(0, (p[0] - self.bx0) // self.bw)))
                        lo = self.bx0 + inbin * self.bw + 8 + self.br; hi = lo + self.bw - 16 - 2 * self.br
                        if p[0] < lo: p[0] = lo; v[0] = abs(v[0]) * 0.4
                        if p[0] > hi: p[0] = hi; v[0] = -abs(v[0]) * 0.4
                        k = counts[inbin]; per = max(1, int((self.bw - 16) // (2 * self.br + 2)))
                        sx = self.bx0 + inbin * self.bw + self.bw / 2 + ((k % per) - (per - 1) / 2) * (2 * self.br + 2)
                        sy = self.floor - self.br - (k // per) * (2 * self.br + 2)
                        if p[1] >= sy:
                            landed = (t, inbin); counts[inbin] += 1; self.lands.append((t, inbin, i))
                            p = np.array([sx, sy]); v[:] = 0
                path.append((t, p.copy()))
                t += dt
            self.paths.append((t0, path, lab))
        self.counts = counts
        print('plinko counts', dict(zip([b[0] for b in self.bins], counts)), 'targets',
              [sum(1 for _l, b in balls if b == j) for j in range(self.nb)])

    def pos(self, i, ts):
        t0, path, _ = self.paths[i]
        if ts < t0: return None
        k = int((ts - t0) * 240)
        return path[min(k, len(path) - 1)][1]

    def count_at(self, j, ts):
        return sum(1 for (lt, b, _i) in self.lands if b == j and lt <= ts)

    def draw(self, ctx, t):
        c = self.c; ts = self.tmap(t)
        a, b, _k = c.get('slowmo', [99, 99, 1])
        zoom = 0.0
        if a < t < b + 0.8:
            zoom = min(1, (t - a) / 0.4) * (1 if t < b else max(0, 1 - (t - b) / 0.8))
        grad_bg(ctx, *c.get('bg', ['#2B1B5A', '#FF7A9A']), t)
        ctx.save()
        if zoom > 0:
            lp = self.pos(len(self.paths) - 1, ts)
            fy = lp[1] if lp is not None else 1200
            fx = min(max(lp[0], 300), 780) if lp is not None else 540
            z = 1 + 0.3 * zoom
            ctx.translate(fx, fy); ctx.scale(z, z); ctx.translate(-fx, -fy)
        # pegs
        for (x, y) in self.pegs[:-(self.nb - 1)]:
            lit = any(0 <= ts - ht < 0.15 and (lambda q: q is not None and abs(q[0] - x) < 60 and abs(q[1] - y) < 60)(self.pos(bi, ht))
                      for ht, bi in self.hits[-40:]) if False else False
            ctx.arc(x, y, self.pr, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.92 if not lit else 1); ctx.fill()
        # bins
        for j, (lab, col) in enumerate(self.bins):
            x0 = self.bx0 + j * self.bw
            rrect(ctx, x0 + 6, self.bin_top, self.bw - 12, self.floor - self.bin_top + 10, 18)
            cc = hexc(col); ctx.set_source_rgba(cc[0], cc[1], cc[2], 0.28); ctx.fill_preserve()
            ctx.set_source_rgba(*cc); ctx.set_line_width(6); ctx.stroke()
            text(ctx, lab, x0 + self.bw / 2, self.bin_top + 60, 34 if len(lab) < 9 else 28, hexc('#FFFFFF'), ink=INK, sw=9)
        for i in range(1, self.nb):
            ctx.arc(self.bx0 + i * self.bw, self.bin_top, 12, 0, 2 * math.pi); ctx.set_source_rgba(*hexc('#FFD23F')); ctx.fill()
        # balls
        for i, (t0, path, lab) in enumerate(self.paths):
            p = self.pos(i, ts)
            if p is None or p[1] < 300: continue
            last = i == len(self.paths) - 1
            col = hexc(c.get('ball_col_last', '#FFD23F') if last else c.get('ball_col', '#38E1FF'))
            ctx.arc(p[0], p[1], self.br + 4, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
            gr = cairo.RadialGradient(p[0] - 8, p[1] - 10, 3, p[0], p[1], self.br)
            gr.add_color_stop_rgba(0, 1, 1, 1, 1); gr.add_color_stop_rgba(1, *col)
            ctx.arc(p[0], p[1], self.br, 0, 2 * math.pi); ctx.set_source(gr); ctx.fill()
            text(ctx, lab, p[0], p[1], self.br * (0.62 if len(lab) > 3 else 0.8), hexc('#FFFFFF'), ink=INK, sw=6)
        ctx.restore()
        # counts over bins (screen space)
        for j in range(self.nb):
            n = self.count_at(j, ts)
            recent = [lt for (lt, b, _i) in self.lands if b == j and lt <= ts]
            pk = max(0, 1 - (ts - max(recent)) * 5) if recent else 0
            col = '#FFFFFF' if n else '#FF5A5F'
            text(ctx, f"{n}{c.get('unit', 'H')}", self.bx0 + (j + 0.5) * self.bw, self.bin_top - 50, 58 + 20 * pk, hexc(col), ink=INK, sw=12)
        text(ctx, c['title'], W / 2, 175, 82, hexc('#FFFFFF'), ink=INK, sw=18, shadow=hexc('#000000', 0.4))
        if c.get('sub'):
            text(ctx, c['sub'], W / 2, 290, 54, hexc('#FFD23F'), ink=INK, sw=12)
        for (t0, t1, msg, y, size, col) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(col), ink=INK, sw=18, scale=0.6 + 0.4 * k, rot=-0.04, shadow=hexc('#000000', 0.5))

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        notes = sims.melody(len(self.hits), c.get('seed', 3))
        inv = {}
        for (ht, _bi), m in zip(sorted(self.hits), notes):
            # sim time -> video time (invert tmap)
            a, b, k = c.get('slowmo', [99, 99, 1])
            vt = ht if ht <= a else (a + (ht - a) / k if ht <= a + (b - a) * k else ht - (b - a) * k + (b - a))
            key = round(vt * 12)
            if key in inv or vt < 0: continue
            inv[key] = 1
            sound.place(bus, sound.ks_pluck(sound.midi(m + 12), 0.25, 0.993, 0.8), vt, 0.22)
        for (lt, _b, i) in self.lands:
            a, b, k = c.get('slowmo', [99, 99, 1])
            vt = lt if lt <= a else (a + (lt - a) / k if lt <= a + (b - a) * k else lt - (b - a) * k + (b - a))
            if vt < 0: continue
            sound.place(bus, sound.syn_pop(0.1, 700, 1300), vt, 0.5)
            sound.place(bus, sound.syn_thud(), vt, 0.35)
        mus = sound.music(c.get('mood', 'playful'), c['duration'], c.get('seed', 3))
        gm = np.ones(len(mus)); a, b, _k = c.get('slowmo', [99, 99, 1])
        gm[int(a * sound.SR):int(b * sound.SR)] = 0.15
        bus[:len(mus)] += mus * gm * 0.45
        if a < 90:
            sound.place(bus, sound.syn_heartbeat(), a + 0.1, 0.8)
            sound.place(bus, sound.syn_heartbeat(), a + 0.7, 0.8)
            sims.wah_wah(c.get('wah', b + 0.1), bus)
        finish_audio(bus, n, dst)


# =============================== DUEL ===============================
class Duel:
    def __init__(self, cfg):
        self.c = cfg; self.cx, self.cy, self.R = 540, 1080, cfg.get('ring_r', 440)
        self.simulate()

    def simulate(self):
        c = self.c; A, B = c['a'], c['b']
        pa = np.array([400.0, 980.0]); pb = np.array([700.0, 1200.0])
        va = np.array([900.0, 420.0]); vb = np.array([-760.0, -560.0])
        flip = c.get('flip_t', 99); T = c['end_t']; pre = c.get('preroll', 0.6)
        hpA, hpB = 100.0, 100.0
        dt = 1 / 240; t = -pre
        self.states = []; self.events = []  # (t, kind, text, x, y)
        last_ab = -9; last_wall = [-9, -9]
        ra, rb = A.get('r', 110), B.get('r', 95)
        while t < c['duration']:
            alive = t < T
            if alive:
                ra_t = ra * (0.45 + 0.55 * hpA / 100) if t > flip else ra
                rb_t = rb * (0.75 + 0.6 * hpB / 100) if t > flip else rb * (0.55 + 0.45 * hpB / 100)
                for (p, v, r, side) in ((pa, va, ra_t, 0), (pb, vb, rb_t, 1)):
                    p += v * dt
                    d = p - np.array([self.cx, self.cy]); dist = np.hypot(*d)
                    if dist + r > self.R:
                        nrm = d / dist; p[:] = np.array([self.cx, self.cy]) + nrm * (self.R - r)
                        vn = np.dot(v, nrm)
                        if vn > 0:
                            v[:] = v - 2 * vn * nrm
                            ang = 0.08 * math.sin(len(self.events) * 1.3); cs, sn = math.cos(ang), math.sin(ang)
                            v[:] = [cs * v[0] - sn * v[1], sn * v[0] + cs * v[1]]
                            if t - last_wall[side] > 0.25 and t > 0:
                                last_wall[side] = t
                                self.events.append((t, 'wall', side, p[0] - nrm[0] * 150, p[1] - nrm[1] * 150))
                                if side == 1 and t > flip: hpB = min(100, hpB + c.get('regen', 6))
                d = pb - pa; dist = np.hypot(*d)
                if dist < ra_t + rb_t:
                    nrm = d / dist; ov = ra_t + rb_t - dist
                    pa -= nrm * ov / 2; pb += nrm * ov / 2
                    rel = np.dot(vb - va, nrm)
                    if rel < 0:
                        va += rel * nrm; vb -= rel * nrm
                        sp = max(900, np.hypot(*va)); va *= sp / np.hypot(*va)
                        sp = max(900, np.hypot(*vb)); vb *= sp / np.hypot(*vb)
                        if t - last_ab > 0.12 and t > 0:
                            last_ab = t
                            mid = (pa + pb) / 2
                            if t < flip:
                                hpB = max(c.get('b_floor', 18), hpB - c.get('dmg_b', 16))
                                self.events.append((t, 'hit', 1, mid[0], mid[1]))
                            else:
                                hpA = max(0, hpA - c.get('dmg_a', 22))
                                self.events.append((t, 'hit', 0, mid[0], mid[1]))
                if t > flip and hpA <= 0 and T > t + 0.06: T = t + 0.05
            else:
                ra_t = ra * 0.45; rb_t = rb * 1.35
                pb += (np.array([self.cx, self.cy]) - pb) * 4 * dt
            self.states.append((t, pa.copy(), pb.copy(), ra_t, rb_t, hpA, hpB))
            t += dt
        self.T = T
        print('duel end_t', round(T, 2), 'events', len(self.events))

    def st(self, t):
        pre = self.c.get('preroll', 0.6); k = int((t + pre) * 240)
        return self.states[min(max(0, k), len(self.states) - 1)]

    def ball(self, ctx, p, r, col, label, face, t):
        ctx.arc(p[0], p[1], r + 7, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
        gr = cairo.RadialGradient(p[0] - r * 0.3, p[1] - r * 0.35, r * 0.1, p[0], p[1], r)
        gr.add_color_stop_rgba(0, 1, 1, 1, 0.9); gr.add_color_stop_rgba(0.35, *hexc(col)); gr.add_color_stop_rgba(1, *hexc(col))
        ctx.arc(p[0], p[1], r, 0, 2 * math.pi); ctx.set_source(gr); ctx.fill()
        text(ctx, label, p[0], p[1] - r * 0.25, max(18, r * 0.36 if len(label) > 5 else r * 0.45), hexc('#FFFFFF'), ink=INK, sw=max(5, r * 0.08))
        ey = p[1] + r * 0.28
        for sx in (-1, 1):
            ex = p[0] + sx * r * 0.27
            ctx.arc(ex, ey, r * 0.13, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
            ctx.arc(ex, ey + r * 0.03, r * 0.065, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
            ctx.set_line_width(max(3, r * 0.05)); ctx.set_source_rgba(*INK)
            if face == 'angry':
                ctx.move_to(ex - sx * r * 0.16, ey - r * 0.24); ctx.line_to(ex + sx * r * 0.14, ey - r * 0.14); ctx.stroke()
            elif face == 'sad':
                ctx.move_to(ex - sx * r * 0.16, ey - r * 0.12); ctx.line_to(ex + sx * r * 0.14, ey - r * 0.24); ctx.stroke()

    def bar(self, ctx, x, y, w, hp, col, label, right):
        rrect(ctx, x, y, w, 46, 23); fill_stroke(ctx, hexc('#1A1030'), 7, INK)
        fw = max(0, (w - 12) * hp / 100)
        if fw > 2:
            rrect(ctx, x + 6 + ((w - 12 - fw) if right else 0), y + 6, fw, 34, 17); ctx.set_source_rgba(*hexc(col)); ctx.fill()
        text(ctx, label, x + w / 2, y - 34, 44, hexc('#FFFFFF'), ink=INK, sw=10)

    def draw(self, ctx, t):
        c = self.c; A, B = c['a'], c['b']
        (_t, pa, pb, ra, rb, hpA, hpB) = self.st(t)
        last = max([e[0] for e in self.events if e[0] <= t and e[1] == 'hit'] or [-9])
        fl = max(0, 1 - (t - last) * 7)
        grad_bg(ctx, *c.get('bg', ['#FFE27A', '#FF8A5B']), t, dots=False)
        # checker arena
        ctx.save(); ctx.arc(self.cx, self.cy, self.R, 0, 2 * math.pi); ctx.clip()
        for i in range(-6, 7):
            for j in range(-6, 7):
                if (i + j) % 2 == 0:
                    ctx.rectangle(self.cx + i * 90, self.cy + j * 90, 90, 90); ctx.set_source_rgba(1, 1, 1, 0.18); ctx.fill()
        ctx.restore()
        ctx.arc(self.cx, self.cy, self.R + 10, 0, 2 * math.pi); ctx.set_line_width(22); ctx.set_source_rgba(*INK); ctx.stroke()
        ctx.arc(self.cx, self.cy, self.R + 10, 0, 2 * math.pi); ctx.set_line_width(10); ctx.set_source_rgba(1, 1, 1, 0.9 + 0.1 * fl); ctx.stroke()
        flip = c.get('flip_t', 99)
        sh = 10 * fl
        ctx.save(); ctx.translate(sh * math.sin(t * 90), sh * math.cos(t * 77))
        alive = t < self.T
        labA = A['label'] if t < flip else A.get('flip_label', A['label'])
        colA = A['color'] if t < flip else A.get('flip_color', A['color'])
        if alive:
            self.ball(ctx, pa, ra, colA, labA, 'angry' if t < flip else 'sad', t)
        else:
            k = min(1, (t - self.T) * 2)
            for i in range(16):
                a = i * math.pi / 8
                ctx.arc(pa[0] + math.cos(a) * 400 * k, pa[1] + math.sin(a) * 400 * k, 14 * (1 - k) + 2, 0, 2 * math.pi)
                ctx.set_source_rgba(*hexc(colA, 1 - k)); ctx.fill()
        self.ball(ctx, pb, rb, B['color'], B['label'], 'angry' if t > flip else 'sad', t)
        ctx.restore()
        for (et, kind, side, x, y) in self.events:
            k = (t - et) / 0.8
            if 0 <= k < 1:
                if kind == 'hit':
                    msg = (c.get('hit_b', ['-10%']) if side == 1 else c.get('hit_a', ['-20%']))
                    msg = msg[int(et * 7) % len(msg)]
                    text(ctx, msg, min(max(x, 220), W - 220), y - 130 * k - 60, 60, hexc('#FF3B5C'), ink=INK, sw=12, alpha=1 - k * k)
                elif side == 1 and et > flip:
                    msg = c.get('regen_labels', ['+1 EMAIL']); msg = msg[int(et * 5) % len(msg)]
                    text(ctx, msg, min(max(x, 220), W - 220), y - 100 * k, 46, hexc('#7CF0FF'), ink=INK, sw=10, alpha=1 - k * k)
        # HUD
        self.bar(ctx, 60, 420, 440, hpA, colA, labA, False)
        self.bar(ctx, 580, 420, 440, hpB, B['color'], B['label'], True)
        text(ctx, 'VS', 540, 443, 64, hexc('#FFFFFF'), ink=INK, sw=14)
        text(ctx, c['title'], W / 2, 190, 80, hexc('#FFFFFF'), ink=INK, sw=18, shadow=hexc('#000000', 0.35))
        for (t0, t1, msg, y, size, col) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(col), ink=INK, sw=18, scale=0.6 + 0.4 * k, rot=-0.04, shadow=hexc('#000000', 0.5))

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        mus = sound.music(c.get('mood', 'tense'), c['duration'], c.get('seed', 4))
        gm = np.ones(len(mus)); fi = int(c.get('flip_t', 99) * sound.SR)
        if fi < len(gm): gm[fi:fi + int(0.9 * sound.SR)] = 0.0
        bus[:len(mus)] += mus * gm * 0.5
        for (et, kind, side, _x, _y) in self.events:
            if kind == 'hit':
                sound.place(bus, sound.syn_thud(), et, 0.8); sound.place(bus, sound.syn_pop(0.08, 400, 900), et, 0.5)
            elif side == 1 and et > c.get('flip_t', 99):
                sound.place(bus, sound.syn_ding(), et, 0.25)
            else:
                sound.place(bus, sound.ks_pluck(sound.midi(67 + 5 * side), 0.2, 0.99, 0.7), et, 0.25)
        ft = c.get('flip_t', 99)
        if ft < 90:
            sound.place(bus, sound.syn_slide(False, 0.7), ft, 0.8)
        sound.place(bus, sound.syn_pop(0.2, 900, 200), self.T, 0.9)
        sims.wah_wah(self.T + 0.25, bus)
        finish_audio(bus, n, dst)


# =============================== GROW ===============================
class Grow:
    def __init__(self, cfg):
        self.c = cfg; self.cx, self.cy, self.R = cfg.get('cx', 540), cfg.get('cy', 1080), cfg.get('ring_r', 430)
        sc = dict(cfg); sc['ball_r0'] = cfg.get('r_start', 55); sc['ball_r1'] = cfg.get('r_end', 400)
        sc['drain_end'] = cfg['crack_t']
        self.hits, self.states = sims.simulate(sc)

    def draw(self, ctx, t):
        c = self.c; T = c['crack_t']
        fi = min(int(t * FPS), len(self.states) - 1); p, r = self.states[fi]
        if t >= T:
            k = min(1, (t - T) / 0.5); p = p + (np.array([self.cx, self.cy]) - p) * k
        last = max([ht for ht, _ in self.hits if ht <= t] or [-9]); fl = max(0, 1 - (t - last) * 6)
        grad_bg(ctx, *c.get('bg', ['#3B1F0E', '#C8551E']), t)
        z = 1 + 0.02 * fl + (0.04 * min(1, (t - T) * 3) if t > T else 0)
        ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2)
        sh = 14 * max(0, 1 - abs(t - T) * 3)
        ctx.translate(sh * math.sin(t * 80), sh * math.cos(t * 63))
        # ring (plate rim) + cracks
        cols = c.get('ring_cols', ['#FFB347', '#FF7043', '#FFD54F'])
        if t < T + 0.05:
            for w_, a in ((40, 0.12), (24, 0.25), (14, 1.0)):
                for i in range(48):
                    a0 = 2 * math.pi * i / 48 + t * 0.4
                    cc = hexc(cols[i % len(cols)])
                    ctx.set_source_rgba(cc[0], cc[1], cc[2], a); ctx.set_line_width(w_)
                    ctx.arc(self.cx, self.cy, self.R + 8, a0, a0 + 2 * math.pi / 48 + 0.01); ctx.stroke()
            nc = int(max(0, (r / c.get('r_end', 400) - 0.75) * 40))
            ctx.set_source_rgba(*INK); ctx.set_line_width(6)
            for i in range(min(nc, 10)):
                a = i * 2.39
                x0, y0 = self.cx + math.cos(a) * (self.R + 8), self.cy + math.sin(a) * (self.R + 8)
                ctx.move_to(x0, y0)
                for s in range(3):
                    x0 += math.cos(a + 0.6 * (-1) ** s) * 28; y0 += math.sin(a + 0.6 * (-1) ** s) * 28; ctx.line_to(x0, y0)
                ctx.stroke()
        else:
            k = min(1, (t - T) / 1.0)
            for i in range(24):
                a = 2 * math.pi * i / 24
                d = self.R + 8 + 700 * k
                cc = hexc(cols[i % len(cols)])
                ctx.save(); ctx.translate(self.cx + math.cos(a) * d, self.cy + math.sin(a) * d); ctx.rotate(a + k * 6)
                ctx.set_source_rgba(cc[0], cc[1], cc[2], 1 - k); ctx.rectangle(-50, -8, 100, 16); ctx.fill(); ctx.restore()
        # trail
        col = hexc(c.get('ball_color', '#F4A261'))
        for kk in range(8, 0, -1):
            q, rq = self.states[max(0, fi - kk)]
            if t < T:
                ctx.set_source_rgba(col[0], col[1], col[2], 0.25 * (8 - kk) / 8); ctx.arc(q[0], q[1], rq, 0, 2 * math.pi); ctx.fill()
        wob = 1 + 0.06 * fl
        pt = c.get('pie_t', 99)
        if t > pt:
            kp = min(1, (t - pt) / 0.6)
            if kp < 1:
                py_ = -150 + (p[1] - r * 0.4 + 150) * kp * kp
                ctx.save(); ctx.translate(p[0], py_); ctx.rotate(t * 4)
                ctx.move_to(0, -90); ctx.line_to(80, 70); ctx.line_to(-80, 70); ctx.close_path()
                fill_stroke(ctx, hexc('#F2C14E'), 7, INK)
                ctx.move_to(0, -60); ctx.line_to(58, 46); ctx.line_to(-58, 46); ctx.close_path(); ctx.set_source_rgba(*hexc('#E07A2E')); ctx.fill()
                ctx.restore()
            else:
                gulp = max(0, 1 - (t - pt - 0.6) * 3)
                wob *= 1 + 0.12 * gulp
                r *= 1.05
        ctx.save(); ctx.translate(p[0], p[1]); ctx.scale(wob, 1 / wob)
        ctx.arc(0, 0, r + 8, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
        gr = cairo.RadialGradient(-r * 0.3, -r * 0.35, r * 0.1, 0, 0, r)
        gr.add_color_stop_rgba(0, *hexc('#FFE9C7')); gr.add_color_stop_rgba(1, *col)
        ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.set_source(gr); ctx.fill()
        text(ctx, c.get('ball_label', 'MY\nSTOMACH'), 0, -r * 0.18, max(22, r * 0.3), hexc('#FFFFFF'), ink=INK, sw=max(6, r * 0.05))
        # face: happy -> stuffed
        full = r / c.get('r_end', 400)
        for sx in (-1, 1):
            ex, ey = sx * r * 0.25, r * 0.32
            ctx.set_source_rgba(*INK); ctx.set_line_width(max(4, r * 0.035))
            if full < 0.7:
                ctx.arc(ex, ey, r * 0.08, math.pi * 1.1, math.pi * 1.9); ctx.stroke()
            else:
                ctx.move_to(ex - r * 0.07, ey - r * 0.05); ctx.line_to(ex + r * 0.07, ey); ctx.line_to(ex - r * 0.07, ey + r * 0.05); ctx.stroke() if sx < 0 else None
                if sx > 0:
                    ctx.new_path(); ctx.move_to(ex + r * 0.07, ey - r * 0.05); ctx.line_to(ex - r * 0.07, ey); ctx.line_to(ex + r * 0.07, ey + r * 0.05); ctx.stroke()
        ctx.arc(0, r * 0.52, r * (0.06 if full < 0.7 else 0.1), 0, math.pi); ctx.set_source_rgba(*INK); ctx.fill()
        ctx.restore()
        # food labels
        foods = c['foods']; lastl = -9
        for i, (ht, a) in enumerate(self.hits):
            if ht - lastl < 0.3: continue
            lastl = ht
            kk = (t - ht) / 0.9
            if 0 <= kk < 1 and ht < T:
                x = self.cx + math.cos(a) * (self.R - 40); y = self.cy + math.sin(a) * (self.R - 40)
                text(ctx, '+' + foods[i % len(foods)], min(max(x, 260), W - 260), y - 120 * kk, 54, hexc('#FFE14D'), ink=INK, sw=12,
                     alpha=1 - kk * kk, scale=0.8 + 0.3 * min(1, kk * 6))
        ctx.restore()
        # HUD
        text(ctx, c['title'], W / 2, 190, 80, hexc('#FFFFFF'), ink=INK, sw=18, shadow=hexc('#000000', 0.4))
        if t < T:
            plates = 1 + sum(1 for ht, _ in self.hits if ht <= t) // c.get('per_plate', 6)
            text(ctx, f"{c.get('meter', 'PLATE')} {plates}", W / 2, 390, 96 + 10 * fl, hexc('#FFE14D'), ink=INK, sw=18)
            pct = min(100, int(100 * full))
            text(ctx, f"{pct}% FULL", W / 2, 1680, 64, hexc('#FFFFFF' if pct < 85 else '#FF5A5F'), ink=INK, sw=14)
        for (t0, t1, msg, y, size, colr) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(colr), ink=INK, sw=18, scale=0.6 + 0.4 * k, rot=-0.04, shadow=hexc('#000000', 0.5))

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        T = c['crack_t']
        notes = sims.melody(len(self.hits), c.get('seed', 9))
        for (ht, _a), m in zip(self.hits, notes):
            if ht >= T: continue
            sound.place(bus, sound.ks_pluck(sound.midi(m), 0.4, 0.995, 0.8), ht, 0.5)
            sound.place(bus, sound.syn_crunch(), ht, 0.12)
        pad(bus, n, 50, 0.03)
        sound.place(bus, sound.syn_crunch(), T, 1.0); sound.place(bus, sound.syn_thud(), T, 1.0)
        sound.place(bus, sound.syn_slide(True, 0.5), T + 0.6, 0.5)
        pt = c.get('pie_t', 99)
        if pt < 90:
            sound.place(bus, sound.syn_slide(False, 0.6), pt, 0.6); sound.place(bus, sound.syn_crunch(), pt + 0.6, 0.9)
            sound.place(bus, sound.syn_pop(0.15, 300, 900), pt + 0.65, 0.8)
        for (t0, _t1, _m, _y, _s, _c) in c.get('cards', []):
            if t0 > 0.2: sound.place(bus, sound.syn_pop(), t0, 0.6)
        finish_audio(bus, n, dst)


MODES = dict(plinko=Plinko, duel=Duel, grow=Grow)


def render(path, frames=None):
    cfg = json.load(open(path)); epdir = os.path.dirname(os.path.abspath(path)); eid = cfg['id']
    sim = MODES[cfg['mode']](cfg)

    def frame(fi):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s)
        sim.draw(ctx, fi / FPS); return s
    if frames:
        from PIL import Image
        ims = []
        for tt in frames:
            p_ = os.path.join(epdir, f'kf_{tt}.png'); frame(int(tt * FPS)).write_to_png(p_); ims.append(Image.open(p_))
        sheet = Image.new('RGB', (270 * len(ims), 480), 'white')
        for i, im in enumerate(ims): sheet.paste(im.convert('RGB').resize((270, 480)), (270 * i, 0))
        sheet.save(os.path.join(epdir, 'sheet.png')); print(os.path.join(epdir, 'sheet.png')); return
    wav = os.path.join(epdir, f'{eid}.wav'); sim.audio(wav)
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
