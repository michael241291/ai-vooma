"""Soundtrack for AIVOOMA videos: original procedural music (seeded per episode, so no two videos share a tune),
an SFX library (assets/sfx/*.mp3 from ElevenLabs) plus synthesized effects, and the final mix."""
import os
import subprocess
import wave
import numpy as np

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX_DIR = os.path.join(ROOT, 'assets', 'sfx')


# ---------------- basic tools ----------------
def fade(x, fin=0.005, fout=0.05):
    x = x.copy(); n = len(x); a = min(n, int(fin * SR)); b = min(n, int(fout * SR))
    if a: x[:a] *= np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)
    return x


def place(bus, x, t, gain=1.0):
    i = int(round(t * SR))
    if i >= len(bus) or i + len(x) <= 0: return
    s = max(0, -i); i = max(0, i); j = min(len(bus), i + len(x) - s)
    bus[i:j] += x[s:s + j - i] * gain


def load(name):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(SFX_DIR, name + '.mp3'), '-f', 'f32le',
                          '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def resample(x, rate):
    if abs(rate - 1) < 1e-3: return x
    idx = np.arange(0, len(x) - 1, rate)
    return np.interp(idx, np.arange(len(x)), x)


def midi(n): return 440.0 * 2 ** ((n - 69) / 12)


def env_exp(n, k): return np.exp(-np.linspace(0, k, n))


# ---------------- synthesized effects ----------------
rng = np.random.default_rng(11)


def noise(n): return rng.uniform(-1, 1, n)


def lowpass(x, a):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y


def syn_pop(d=0.09, f0=500, f1=1100):
    tt = np.arange(int(d * SR)) / SR
    return fade(np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, len(tt))) / SR) * np.exp(-tt * 28), 0.002, 0.02)


def syn_ding():
    tt = np.arange(int(0.9 * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * tt) * a for f, a in ((1568, 1), (3136, 0.4), (4704, 0.2)))
    return fade(x * np.exp(-tt * 5) * 0.5)


def syn_thud():
    tt = np.arange(int(0.3 * SR)) / SR
    x = np.sin(2 * np.pi * np.cumsum(120 - 260 * tt) / SR) * np.exp(-tt * 18) + 0.3 * noise(len(tt)) * np.exp(-tt * 40)
    return fade(x)


def syn_slide(up=True, d=0.6):
    tt = np.arange(int(d * SR)) / SR
    f = np.linspace(500, 1500, len(tt)) if up else np.linspace(1500, 450, len(tt))
    f = f * (1 + 0.02 * np.sin(2 * np.pi * 6 * tt))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return fade(x * 0.5, 0.03, 0.08)


def syn_swoosh(d=0.45):
    n = int(d * SR); x = noise(n)
    a = np.linspace(0.02, 0.5, n)
    y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += a[i] * (x[i] - acc); y[i] = acc
    return fade(y * np.sin(np.linspace(0, np.pi, n)) * 2.2, 0.01, 0.05)


def syn_purr(d=4.0):
    n = int(d * SR); tt = np.arange(n) / SR
    x = lowpass(noise(n), 0.04) * 6
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 26 * tt) ** 2
    breath = 0.6 + 0.4 * np.sin(2 * np.pi * 0.45 * tt) ** 2
    return fade(x * am * breath * 0.9, 0.2, 0.3)


def syn_vacuum(d=4.0):
    n = int(d * SR); tt = np.arange(n) / SR
    hum = 0.35 * np.sin(2 * np.pi * 118 * tt) + 0.2 * np.sin(2 * np.pi * 236 * tt) + 0.1 * np.sin(2 * np.pi * 354 * tt)
    hiss = lowpass(noise(n), 0.35) * 0.9
    whine = 0.08 * np.sin(2 * np.pi * np.cumsum(1800 + 60 * np.sin(2 * np.pi * 0.7 * tt)) / SR)
    return fade((hum + hiss + whine) * 0.7, 0.25, 0.4)


def syn_static(d=2.0):
    n = int(d * SR)
    return fade(noise(n) * 0.35, 0.01, 0.2)


def syn_sparkle():
    out = np.zeros(int(0.8 * SR))
    for i, m in enumerate((84, 88, 91, 96, 100)):
        tt = np.arange(int(0.35 * SR)) / SR
        place(out, np.sin(2 * np.pi * midi(m) * tt) * np.exp(-tt * 14) * 0.4, i * 0.07)
    return out


def syn_crunch():
    n = int(0.32 * SR); out = np.zeros(n)
    for st, g in ((0.0, 1.0), (0.045, 0.7), (0.09, 0.55), (0.14, 0.35)):
        L = int(0.07 * SR)
        g_ = np.diff(noise(L) * np.exp(-np.linspace(0, 7, L)) * g, prepend=0) * 1.6
        place(out, g_, st)
    tt = np.arange(int(0.12 * SR)) / SR
    out[:len(tt)] += np.sin(2 * np.pi * (140 - 400 * tt) * tt) * np.exp(-tt * 30) * 0.8
    return fade(out)


def syn_tick():
    n = int(0.03 * SR)
    return np.diff(noise(n) * np.exp(-np.linspace(0, 9, n)), prepend=0) * 0.8


def syn_wobble(d=1.4):
    tt = np.arange(int(d * SR)) / SR
    f = 820 + 120 * np.sin(2 * np.pi * 13 * tt) + 160 * tt
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 17 * tt)) ** 2
    return fade(x * 0.5, 0.08, 0.25)


def syn_heartbeat():
    out = np.zeros(int(0.9 * SR))
    for st in (0.0, 0.22):
        tt = np.arange(int(0.18 * SR)) / SR
        place(out, np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 22), st)
    return out


SYNTH = dict(pop=syn_pop, ding=syn_ding, thud=syn_thud, slide_up=lambda: syn_slide(True), slide_down=lambda: syn_slide(False),
             swoosh=syn_swoosh, purr_long=syn_purr, vacuum_long=syn_vacuum, static=syn_static, sparkle=syn_sparkle,
             crunch=syn_crunch, tick=syn_tick, wobble=syn_wobble, heartbeat=syn_heartbeat)


def get_sfx(name, opts):
    if name in SYNTH:
        fn = SYNTH[name]
        x = fn(opts['dur']) if 'dur' in opts and name in ('purr_long', 'vacuum_long', 'static', 'swoosh', 'wobble') else fn()
    else:
        x = load(name)
    if 'start' in opts:
        x = x[int(opts['start'] * SR):]
    if 'rate' in opts:
        x = resample(x, opts['rate'])
    if 'dur' in opts and name not in SYNTH:
        n = int(opts['dur'] * SR)
        if len(x) < n and opts.get('loop'):
            reps = int(np.ceil(n / len(x))) + 1
            x = np.concatenate([fade(x, 0.02, 0.02)] * reps)
        x = x[:n]
    return fade(x, opts.get('fin', 0.004), opts.get('fade', 0.05))


# ---------------- music ----------------
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]
MOODS = {
    'playful': dict(bpm=132, key=60, scale=MAJOR, prog=[[0, 5, 3, 4], [0, 3, 4, 4], [5, 3, 0, 4]], inst='pluck', drums=True),
    'tense': dict(bpm=118, key=57, scale=MINOR, prog=[[0, 0, 5, 4], [0, 5, 0, 4]], inst='pluck', drums=False, ostinato=True),
    'sneaky': dict(bpm=100, key=50, scale=MINOR, prog=[[0, 3, 0, 4], [0, 0, 3, 4]], inst='pluck', drums=False, walking=True),
    'cozy': dict(bpm=84, key=65, scale=MAJOR, prog=[[0, 3, 4, 0], [0, 5, 3, 4]], inst='bell', drums=False),
    'night': dict(bpm=72, key=57, scale=MINOR, prog=[[0, 5, 3, 4], [0, 3, 5, 4]], inst='bell', drums=False, sparse=True),
    'triumph': dict(bpm=140, key=55, scale=MAJOR, prog=[[0, 3, 4, 4], [0, 4, 5, 3]], inst='pluck', drums=True, arps=True),
}


def ks_pluck(freq, dur, decay=0.994, bright=0.7):
    n = int(dur * SR); p = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, p)
    buf = bright * buf + (1 - bright) * np.convolve(buf, np.ones(3) / 3, 'same')
    out = np.empty(n); i = 0
    while i < n:
        k = min(p, n - i); out[i:i + k] = buf[:k]
        buf = decay * 0.5 * (buf + np.roll(buf, -1)); i += k
    return fade(out, 0.002, 0.04)


def bell(freq, dur):
    tt = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * freq * tt) + 0.35 * np.sin(2 * np.pi * freq * 2.76 * tt) * np.exp(-tt * 6) + 0.2 * np.sin(2 * np.pi * freq * 5.4 * tt) * np.exp(-tt * 12)
    return fade(x * np.exp(-tt * 3.2) * 0.5, 0.003, 0.08)


def music(mood, length, seed=1):
    m = MOODS[mood]; r = np.random.default_rng(seed)
    e = 60 / m['bpm'] / 2
    prog = m['prog'][r.integers(len(m['prog']))]
    sc = m['scale']; key = m['key'] + int(r.integers(-2, 3))
    bus = np.zeros(int(length * SR) + SR)
    cache = {}

    def note(mi, d, kind):
        k = (mi, round(d, 3), kind)
        if k not in cache:
            f = midi(mi)
            cache[k] = bell(f, d) if kind == 'bell' else ks_pluck(f, d, 0.995 if kind == 'bass' else 0.993, 0.4 if kind == 'bass' else 0.75)
        return cache[k]

    def deg(d, octv=0):
        return key + sc[d % 7] + 12 * (d // 7) + 12 * octv

    # pick 2 rhythm/melody motifs, repeat with variation (AABA)
    patterns = [[1, 0, 1, 1, 0, 1, 1, 0], [1, 1, 0, 1, 1, 0, 1, 0], [1, 0, 0, 1, 1, 1, 0, 1], [1, 1, 1, 0, 1, 0, 1, 1]]
    if m.get('sparse'):
        patterns = [[1, 0, 0, 1, 0, 0, 1, 0], [1, 0, 1, 0, 0, 0, 1, 0]]
    motifs = []
    for _ in range(2):
        pat = patterns[r.integers(len(patterns))]
        walk = []; d = int(r.integers(0, 5))
        for _s in pat:
            d = int(np.clip(d + r.choice([-2, -1, -1, 1, 1, 2, 0]), -2, 9)); walk.append(d)
        motifs.append((pat, walk))
    form = [0, 0, 1, 0]
    t = 0.0; bar = 0
    while t < length:
        root = prog[bar % len(prog)]
        pat, walk = motifs[form[bar % 4]]
        for s in range(8):
            tt = t + s * e
            if tt >= length: break
            if pat[s]:
                d = walk[s] + root
                kind = 'bell' if m['inst'] == 'bell' else 'lead'
                place(bus, note(deg(d, 1 if kind == 'bell' else 0), 0.5 if kind == 'bell' else 0.28, kind), tt, 0.26 if kind == 'lead' else 0.22)
            if m.get('arps') and s % 2 == 1:
                place(bus, note(deg(root + (2 * (s // 2)) % 7, 1), 0.2, 'lead'), tt, 0.1)
            if m.get('walking'):
                if s % 2 == 0:
                    place(bus, note(deg(root + [0, 2, 4, 2][s // 2], -1), 0.3, 'bass'), tt, 0.4)
            elif m.get('ostinato'):
                place(bus, note(deg(root + (0 if s % 2 == 0 else 4), -1), 0.2, 'bass'), tt, 0.3)
            elif s % 4 == 0:
                place(bus, note(deg(root, -1), 0.45, 'bass'), tt, 0.42)
            if m['drums']:
                if s % 2 == 1:
                    place(bus, syn_tick(), tt, 0.07)
                if s == 0 or s == 4:
                    tk = np.arange(int(0.15 * SR)) / SR
                    place(bus, np.sin(2 * np.pi * (90 - 200 * tk) * tk) * np.exp(-tk * 25), tt, 0.35)
        t += 8 * e; bar += 1
    return bus[:int(length * SR)]


# ---------------- mix ----------------
def gain_curve(keys, n):
    tt = np.arange(n) / SR
    if not keys:
        return np.ones(n)
    keys = sorted(keys, key=lambda k: k[0])
    out = np.full(n, float(keys[0][1]))
    for (t0, v0, *_), (t1, v1, *rest) in zip(keys, keys[1:]):
        mode = rest[0] if rest else 'linear'
        m = (tt >= t0) & (tt < t1)
        out[m] = v0 if mode == 'step' else v0 + (v1 - v0) * (tt[m] - t0) / max(1e-6, t1 - t0)
    out[tt >= keys[-1][0]] = keys[-1][1]
    return out


def mix(audio, length, dst, seed=1):
    n = int(length * SR); bus = np.zeros(n)
    mus_list = audio.get('music') or []
    if isinstance(mus_list, dict):
        mus_list = [mus_list]
    for k, mu in enumerate(mus_list):
        mus = music(mu['mood'], length, mu.get('seed', seed + 17 * k))
        bus += mus * gain_curve(mu.get('gain', []), n) * mu.get('volume', 1.0)
    for item in audio.get('sfx', []):
        t, name = item[0], item[1]
        g = item[2] if len(item) > 2 else 1.0
        opts = item[3] if len(item) > 3 else {}
        place(bus, get_sfx(name, opts), t, g)
    peak = np.max(np.abs(bus)) + 1e-9
    bus = np.tanh(bus / peak * 1.3) / np.tanh(1.3) * 0.89
    if len(bus) > int(0.03 * SR):  # tiny fade at edges so the loop does not click
        k = int(0.03 * SR); bus[-k:] *= np.linspace(1, 0, k)
    pcm = (np.clip(bus, -1, 1) * 32767).astype(np.int16)
    with wave.open(dst, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return dst
