"""Tiny Chaos physics simulations ("life's little chaos, animated").

ring_drain(cfg): a labelled ball bounces inside a neon ring. Every wall hit costs something (a bill, a brain cell,
energy...) and the ball shrinks with the counter, plays the next note of an original melody, and pops a label.
At the end the counter hits zero and the ball pops. Everything (hits, labels, melody) comes from a deterministic
simulation, so the same cfg always renders the same video.

Usage: python engine/sims.py episodes/<id>/sim.json [--frames 0 2 5]
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
from core import W, H, FPS, hexc, text  # noqa: E402
import sound  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------- physics ----------------
def simulate(cfg):
    """Return per-frame states and the list of wall hits (time, angle)."""
    cx, cy, R = cfg.get('cx', 540), cfg.get('cy', 1080), cfg.get('ring_r', 430)
    T = cfg['drain_end']
    r0, r1 = cfg.get('ball_r0', 80), cfg.get('ball_r1', 16)
    g = cfg.get('gravity', 1500.0)
    vmin = cfg.get('vmin', 1150.0)
    p = np.array(cfg.get('p0', [cx - 60, cy - 120]), float)
    v = np.array(cfg.get('v0', [820.0, -260.0]), float)
    sub = 8; dt = 1 / FPS / sub
    hits = []; states = []
    # radius follows the "remaining" fraction, which we only know after the first pass: use time as a proxy first,
    # then pass 2 uses the real counter. Radius by time keeps it smooth and deterministic.
    def rad(t):
        f = min(1.0, max(0.0, 1 - t / T))
        return r1 + (r0 - r1) * f ** 0.8
    pre = cfg.get('preroll', 0.0)
    t = -pre; nframes = int((cfg['duration'] + pre) * FPS)
    last_hit = -1
    for fi in range(nframes):
        for _ in range(sub):
            if t < T:
                v[1] += g * dt
                p += v * dt
                r = rad(t)
                d = p - np.array([cx, cy]); dist = np.linalg.norm(d)
                if dist + r > R:
                    n = d / dist
                    p = np.array([cx, cy]) + n * (R - r)
                    vn = np.dot(v, n)
                    if vn > 0:
                        v = v - 2 * vn * n
                        # a little random-free "kick" so it never settles: rotate slightly, keep speed >= vmin
                        ang = 0.06 * math.sin(len(hits) * 1.7)
                        c, s = math.cos(ang), math.sin(ang)
                        v = np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])
                        sp = np.linalg.norm(v)
                        if sp < vmin: v *= vmin / sp
                        if t - last_hit > 0.06 and t >= 0:
                            hits.append((t, math.atan2(n[1], n[0])))
                            last_hit = t
            t += dt
        states.append((p.copy(), rad(min(t, T))))
    return hits, states[int(pre * FPS):]


# ---------------- audio ----------------
def melody(n, seed):
    """Original upbeat pentatonic line, AABA phrases, for n hits."""
    r = np.random.default_rng(seed)
    pent = [0, 2, 4, 7, 9]
    phrases = []
    for _ in range(2):
        d = int(r.integers(3, 7)); ph = []
        for _s in range(8):
            d = int(np.clip(d + r.choice([-2, -1, 1, 1, 2]), 0, 10)); ph.append(d)
        phrases.append(ph)
    seq = []
    form = [0, 0, 1, 0]
    while len(seq) < n:
        seq += phrases[form[(len(seq) // 8) % 4]]
    base = 60 + int(r.integers(-2, 3))
    return [base + pent[d % 5] + 12 * (d // 5) for d in seq[:n]]


def wah_wah(t0, bus):
    for k, (f0, d) in enumerate([(392, 0.35), (370, 0.35), (349, 0.35), (330, 0.9)]):
        tt = np.arange(int(d * sound.SR)) / sound.SR
        f = f0 * (1 + 0.012 * np.sin(2 * np.pi * 6 * tt)) * (np.linspace(1, 0.94, len(tt)) if k == 3 else 1)
        ph = 2 * np.pi * np.cumsum(f) / sound.SR
        x = np.sign(np.sin(ph)) * 0.25 + np.sin(ph) * 0.5 + 0.25 * np.sin(2 * ph)
        x = sound.lowpass(x, 0.18) * np.minimum(1, tt * 30) * np.exp(-tt * (1.2 if k == 3 else 2.5))
        sound.place(bus, sound.fade(x, 0.01, 0.08), t0 + 0.38 * k, 0.55)


def make_audio(cfg, hits, dst):
    n = int(cfg['duration'] * sound.SR); bus = np.zeros(n + sound.SR)
    notes = melody(len(hits), cfg.get('seed', 7))
    for (t, _a), m in zip(hits, notes):
        sound.place(bus, sound.ks_pluck(sound.midi(m), 0.45, 0.996, 0.8), t, 0.55)
        sound.place(bus, sound.bell(sound.midi(m + 12), 0.3), t, 0.12)
    # soft pad underneath so silence never happens
    tt = np.arange(n) / sound.SR
    pad = sum(np.sin(2 * np.pi * sound.midi(48 + k) * tt) for k in (0, 7, 12)) * 0.03
    bus[:n] += pad * np.minimum(1, tt / 0.5)
    T = cfg['drain_end']
    sound.place(bus, sound.syn_pop(0.2, 900, 200), T, 0.8)
    wah_wah(T + 0.2, bus)
    bus = bus[:n]
    peak = np.max(np.abs(bus)) + 1e-9
    bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
    k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
    with wave.open(dst, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
        w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


# ---------------- drawing ----------------
def money(v, fmt):
    return fmt.format(max(0, int(round(v))))


def draw_bg(ctx, cfg, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    a, b = cfg.get('bg', ['#1B1033', '#3A1450'])
    g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.06)
    for i in range(60):
        x = (i * 211 + 37) % W; y = (i * 389 + int(t * 20 * (1 + i % 3))) % H
        ctx.arc(x, y, 2 + i % 3, 0, 2 * math.pi); ctx.fill()


def draw_ring(ctx, cfg, t, flash):
    cx, cy, R = cfg.get('cx', 540), cfg.get('cy', 1080), cfg.get('ring_r', 430)
    cols = cfg.get('ring_cols', ['#FF4FD8', '#7B5CFF', '#38E1FF', '#FFD23F'])
    # glow
    for w_, a in ((46, 0.10), (30, 0.18), (16, 0.9)):
        n = 72
        for i in range(n):
            a0 = 2 * math.pi * i / n + t * 0.6; a1 = a0 + 2 * math.pi / n + 0.01
            c = hexc(cols[(i * len(cols)) // n])
            ctx.set_source_rgba(c[0], c[1], c[2], a * (1 + 0.6 * flash if w_ == 16 else 1))
            ctx.set_line_width(w_); ctx.arc(cx, cy, R + 8, a0, a1); ctx.stroke()
    # locked "gate" segment that keeps rotating away
    ga = -math.pi / 2 + t * cfg.get('gate_speed', 1.3)
    span = 0.42
    ctx.set_line_width(26); ctx.set_source_rgba(*hexc('#FFD23F'))
    ctx.arc(cx, cy, R + 8, ga - span / 2, ga + span / 2); ctx.stroke()
    lx, ly = cx + math.cos(ga) * (R + 78), cy + math.sin(ga) * (R + 78)
    text(ctx, cfg.get('gate_label', 'PAYDAY'), min(max(lx, 110), W - 110), ly, 46, hexc('#FFD23F'), sw=12)
    # lock icon
    ix, iy = cx + math.cos(ga) * (R + 8), cy + math.sin(ga) * (R + 8)
    ctx.save(); ctx.translate(ix, iy)
    ctx.set_source_rgba(*hexc('#2A1636')); ctx.rectangle(-16, -6, 32, 26); ctx.fill()
    ctx.set_line_width(6); ctx.arc(0, -6, 11, math.pi, 0); ctx.stroke()
    ctx.restore()


def draw_ball(ctx, cfg, p, r, frac, trail, alive, pop_k):
    col = hexc(cfg.get('ball_color', '#3DDC84'))
    for k, (q, rq) in enumerate(trail if alive else []):
        a = (k + 1) / (len(trail) + 1) * 0.35
        ctx.set_source_rgba(col[0], col[1], col[2], a)
        ctx.arc(q[0], q[1], rq * (0.5 + 0.5 * (k + 1) / len(trail)), 0, 2 * math.pi); ctx.fill()
    if not alive:
        # pop burst
        for i in range(18):
            ang = i * 2 * math.pi / 18
            d = 40 + 520 * pop_k
            ctx.set_source_rgba(col[0], col[1], col[2], max(0, 1 - pop_k))
            ctx.arc(p[0] + math.cos(ang) * d, p[1] + math.sin(ang) * d, 10 * (1 - pop_k) + 2, 0, 2 * math.pi); ctx.fill()
        return
    ctx.set_source_rgba(*hexc('#1E5E3A')); ctx.arc(p[0], p[1], r + 6, 0, 2 * math.pi); ctx.fill()
    g = cairo.RadialGradient(p[0] - r * 0.3, p[1] - r * 0.3, r * 0.1, p[0], p[1], r)
    g.add_color_stop_rgba(0, *hexc('#B8FFD4')); g.add_color_stop_rgba(1, *col)
    ctx.set_source(g); ctx.arc(p[0], p[1], r, 0, 2 * math.pi); ctx.fill()
    if r > 46:
        text(ctx, cfg.get('ball_label', 'MY\nSALARY'), p[0], p[1] - r * 0.12, r * 0.42, hexc('#FFFFFF'), sw=max(6, r * 0.09))
        # worried eyes get bigger as it shrinks
        e = 0.12 + 0.1 * (1 - frac)
        for sx in (-1, 1):
            ctx.set_source_rgba(1, 1, 1, 1); ctx.arc(p[0] + sx * r * 0.28, p[1] + r * 0.42, r * e, 0, 2 * math.pi); ctx.fill()
            ctx.set_source_rgba(0.1, 0.1, 0.1, 1); ctx.arc(p[0] + sx * r * 0.28, p[1] + r * 0.45, r * e * 0.5, 0, 2 * math.pi); ctx.fill()
    else:
        text(ctx, cfg.get('ball_small', '$'), p[0], p[1], max(18, r * 1.3), hexc('#FFFFFF'), sw=max(4, r * 0.15))


def render(cfg_path, frames=None):
    cfg = json.load(open(cfg_path))
    epdir = os.path.dirname(os.path.abspath(cfg_path)); eid = cfg['id']
    hits, states = simulate(cfg)
    T = cfg['drain_end']; start = cfg['start_value']
    costs = cfg['costs']  # list of [label, amount]; repeats if more hits than costs
    # assign each hit a cost; scale so the total equals start exactly at the last hit before T
    labels = [costs[i % len(costs)] for i in range(len(hits))]
    tot = sum(c[1] for c in labels) or 1
    scale = start / tot
    remaining = []; acc = start
    for (_t, _a), (_lab, amt) in zip(hits, labels):
        acc -= amt * scale; remaining.append(acc)
    remaining[-1] = 0 if remaining else 0
    pops = []  # floating labels: (t, x, y, label)
    cx, cy, R = cfg.get('cx', 540), cfg.get('cy', 1080), cfg.get('ring_r', 430)
    for (t, a), (lab, amt) in zip(hits, labels):
        x = cx + math.cos(a) * (R - 170); y = cy + math.sin(a) * (R - 150)
        pops.append((t, x, y, f"{cfg.get('cost_prefix', '-$')}{int(round(amt * scale)):,}\n{lab}"))

    def value_at(t):
        v = start
        for (ht, _a), rem in zip(hits, remaining):
            if ht <= t: v = rem
        return v

    def frame(fi):
        t = fi / FPS
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s)
        last = max([ht for ht, _ in hits if ht <= t] or [-9])
        flash = max(0.0, 1 - (t - last) * 6)
        # camera punch on hits
        z = 1 + 0.015 * flash
        ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2)
        draw_bg(ctx, cfg, t)
        draw_ring(ctx, cfg, t, flash)
        p, r = states[min(fi, len(states) - 1)]
        trail = [states[max(0, fi - k)] for k in range(10, 0, -1)]
        alive = t < T
        draw_ball(ctx, cfg, p, r, value_at(t) / start, trail, alive, min(1, (t - T) * 2.2))
        for (pt, x, y, lab) in pops:
            k = (t - pt) / 0.9
            if 0 <= k < 1:
                text(ctx, lab, min(max(x, 300), W - 300), y - 110 * k, 56, hexc('#FF6B6B'), sw=13, alpha=1 - k ** 2, scale=0.8 + 0.4 * min(1, k * 6))
        # header
        text(ctx, cfg['title'], W / 2, 170, 74, hexc('#FFFFFF'), sw=16, shadow=hexc('#000000', 0.5))
        v = value_at(t)
        text(ctx, money(v, cfg.get('fmt', '${:,}')), W / 2, 330, 150 + 14 * flash,
             hexc('#3DDC84' if v > start * 0.3 else ('#FFD23F' if v > 0 else '#FF5A5F')), sw=22, shadow=hexc('#000000', 0.5))
        day = 1 + int((cfg.get('days', 30) - 2) * min(1, t / T))
        text(ctx, f"{cfg.get('day_word', 'DAY')} {day}", W / 2, 455, 60, hexc('#FFD23F'), sw=12)
        if not alive:
            k = min(1, (t - T) * 3)
            text(ctx, cfg['end_text'], W / 2, cy, 120, hexc('#FF5A5F'), sw=22, scale=0.6 + 0.4 * k, alpha=k, rot=-0.05,
                 shadow=hexc('#000000', 0.6))
        text(ctx, cfg.get('footer', ''), W / 2, 1700, 54, hexc('#FFFFFF'), sw=12, alpha=0.95)
        return s

    if frames:
        from PIL import Image
        ims = []
        for tt in frames:
            fs = frame(int(tt * FPS)); p_ = os.path.join(epdir, f'kf_{tt}.png'); fs.write_to_png(p_); ims.append(Image.open(p_))
        sheet = Image.new('RGB', (270 * len(ims), 480), 'white')
        for i, im in enumerate(ims): sheet.paste(im.convert('RGB').resize((270, 480)), (270 * i, 0))
        sheet.save(os.path.join(epdir, 'sheet.png')); print('hits', len(hits), 'sheet', os.path.join(epdir, 'sheet.png'))
        return
    wav = os.path.join(epdir, f'{eid}.wav'); make_audio(cfg, hits, wav)
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
    os.remove(silent); print(out, 'hits', len(hits))


if __name__ == '__main__':
    args = sys.argv[1:]
    fr = None
    if '--frames' in args:
        i = args.index('--frames'); fr = [float(x) for x in args[i + 1:]]; args = args[:i]
    render(args[0], fr)
