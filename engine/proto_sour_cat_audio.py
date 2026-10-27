"""Mix the soundtrack for the Sour Cat Short: original pizzicato loop + ElevenLabs SFX + synth crunch/pops."""
import numpy as np, subprocess, os, wave

SR = 44100
DUR = 10.0
HERE = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(HERE, 'sfx')
OUT = os.path.join(HERE, 'out')
rng = np.random.default_rng(3)


def load(name):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(SFX, name), '-f', 'f32le',
                          '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def fade(x, fin=0.005, fout=0.05):
    n = len(x); a = int(fin * SR); b = int(fout * SR)
    if a: x[:a] *= np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)
    return x


def place(bus, x, t, gain=1.0):
    i = int(t * SR); j = min(len(bus), i + len(x))
    bus[i:j] += x[:j - i] * gain


def midi(n): return 440.0 * 2 ** ((n - 69) / 12)


def pluck(freq, dur, decay=0.995, bright=0.6):
    n = int(dur * SR); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p)
    buf = bright * buf + (1 - bright) * np.convolve(buf, np.ones(3) / 3, 'same')
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = decay * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return fade(out, 0.002, 0.04)


def music(length):
    bpm = 132; e = 60 / bpm / 2  # eighth note
    mel = [60, 64, 67, 64, 69, 67, 64, 67, 65, 69, 72, 69, 67, None, 71, None,
           60, 64, 67, 64, 69, 67, 64, 67, 65, 64, 62, 59, 60, None, 55, None]
    bass = [48, 45, 41, 43, 48, 45, 41, 43]
    bus = np.zeros(int(length * SR) + SR)
    cache = {}
    def note(m, d, dec, br):
        k = (m, d, dec, br)
        if k not in cache: cache[k] = pluck(midi(m), d, dec, br)
        return cache[k]
    t = 0.0; i = 0
    while t < length:
        m = mel[i % len(mel)]
        if m is not None: place(bus, note(m, 0.28, 0.994, 0.7), t, 0.32)
        if i % 2 == 0:
            place(bus, note(bass[(i // 2) % len(bass)], 0.4, 0.996, 0.4), t, 0.42)
        else:  # soft hat tick
            h = rng.uniform(-1, 1, int(0.03 * SR)) * np.exp(-np.linspace(0, 9, int(0.03 * SR)))
            h = np.diff(h, prepend=0)
            place(bus, h, t, 0.06)
        t += e; i += 1
    return bus[:int(length * SR)]


def crunch():
    n = int(0.32 * SR); out = np.zeros(n)
    for k, (st, g) in enumerate(((0.0, 1.0), (0.045, 0.7), (0.09, 0.55), (0.14, 0.35))):
        L = int(0.07 * SR)
        g_ = rng.uniform(-1, 1, L) * np.exp(-np.linspace(0, 7, L)) * g
        g_ = np.diff(g_, prepend=0) * 1.6
        place(out, g_, st, 1.0)
    tt = np.arange(int(0.12 * SR)) / SR
    thump = np.sin(2 * np.pi * (140 - 400 * tt) * tt) * np.exp(-tt * 30)
    out[:len(thump)] += thump * 0.8
    return fade(out)


def pop(f0=500, f1=1100, d=0.09):
    tt = np.arange(int(d * SR)) / SR
    f = np.linspace(f0, f1, len(tt))
    return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 28), 0.002, 0.02)


def wobble(d=1.45):
    tt = np.arange(int(d * SR)) / SR
    f = 820 + 120 * np.sin(2 * np.pi * 13 * tt) + 160 * tt
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 17 * tt)) ** 2
    x += 0.3 * np.sin(2 * np.pi * np.cumsum(f / 2) / SR)
    return fade(x * 0.5, 0.08, 0.25)


def main():
    L = int(DUR * SR)
    bus = np.zeros(L)
    # music: plays until the sour hit, comedic stop, returns softly at the end
    m = music(DUR)
    env = np.ones(L)
    tt = np.arange(L) / SR
    env[(tt >= 4.12) & (tt < 7.9)] = 0.0
    k = (tt >= 4.08) & (tt < 4.12); env[k] = np.linspace(1, 0, k.sum())
    k = (tt >= 7.9) & (tt < 8.6); env[k] = np.linspace(0, 0.7, k.sum())
    env[tt >= 8.6] = 0.7
    bus += m * env

    place(bus, pop(), 0.12, 0.35)
    place(bus, fade(load('sniff.mp3')), 1.12, 0.9)
    place(bus, crunch(), 3.12, 0.85)
    boing = load('boing.mp3')[:int(3.1 * SR)]
    place(bus, fade(boing, 0.002, 0.6), 4.1, 0.85)
    place(bus, pop(300, 900, 0.12), 4.4, 0.4)
    place(bus, fade(load('yowl.mp3')), 4.75, 1.0)
    place(bus, wobble(), 5.6, 0.55)
    place(bus, fade(load('yowl.mp3')), 6.3, 0.6)
    place(bus, fade(load('whoosh.mp3')), 7.0, 0.9)
    place(bus, pop(700, 1300, 0.08), 9.05, 0.3)

    peak = np.max(np.abs(bus)) + 1e-9
    bus = np.tanh(bus / peak * 1.3) / np.tanh(1.3) * 0.89
    pcm = (np.clip(bus, -1, 1) * 32767).astype(np.int16)
    dst = os.path.join(OUT, 'sour_cat_audio.wav')
    with wave.open(dst, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print('wrote', dst)


if __name__ == '__main__':
    main()
