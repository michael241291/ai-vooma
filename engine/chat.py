"""Tiny Chaos phone-chat skits (batch 5, 2026-11-17): "texting X to different people".

A big phone fills the frame; each scene is one contact's chat. Bubbles pop in, typing dots, missed-call rows,
"Seen" receipts. Scenes switch with a sideways swipe. Built for the BlobbyClips-style "X with different people" pattern.

Usage: python engine/chat.py episodes/<id>/chat.json [--frames 0 2 5]
cfg: id, ver, duration, seed, mood, bg [a,b], header (top text), scenes [
       {contact, color, tag (big label above the phone), t (scene start), msgs [[t_rel, kind, text], ...]}]
     kind: me | them | typing (text ignored, shows until next msg) | call (missed-call row, text = 'Missed call x3')
           | seen (small 'Seen' under the last 'me' bubble) | system (centred grey line)
     cards [[t0, t1, msg, y, size, color]], footer.
Bubble font: Inter (falls back to the cairo default sans if missing). Titles/tags: Luckiest Guy.
"""
import json
import math
import os
import sys
import wave

import cairo
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import W, H, FPS, hexc, text, rrect, fill_stroke  # noqa: E402
import sound  # noqa: E402
from race import encode  # noqa: E402

INK = hexc('#2A1636')
SANS = 'Inter'
PX, PY, PW, PH = 90, 430, 900, 1260  # phone screen rect


def ease_back(k):
    k = min(1.0, max(0.0, k)); s = 1.7; k -= 1; return k * k * ((s + 1) * k + s) + 1


def wrap_lines(ctx, msg, size, maxw):
    ctx.select_font_face(SANS, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    out = []
    for para in msg.split('\n'):
        cur = ''
        for w in para.split(' '):
            tr = (cur + ' ' + w).strip()
            if ctx.text_extents(tr).x_advance > maxw and cur:
                out.append(cur); cur = w
            else:
                cur = tr
        out.append(cur)
    return out


class Chat:
    def __init__(self, cfg):
        self.c = cfg; sc = cfg['scenes']
        for i, s in enumerate(sc):
            s['end'] = sc[i + 1]['t'] if i + 1 < len(sc) else cfg['duration'] + 1

    def scene_at(self, t):
        sc = self.c['scenes']; i = 0
        for k, s in enumerate(sc):
            if t >= s['t']: i = k
        return i

    def draw_scene(self, ctx, s, t):
        rt = t - s['t']
        # screen bg
        rrect(ctx, PX, PY, PW, PH, 50); ctx.set_source_rgba(*hexc('#F4F5FA')); ctx.fill()
        # header bar
        ctx.save(); rrect(ctx, PX, PY, PW, PH, 50); ctx.clip()
        ctx.rectangle(PX, PY, PW, 170); ctx.set_source_rgba(*hexc('#FFFFFF')); ctx.fill()
        ctx.rectangle(PX, PY + 170, PW, 3); ctx.set_source_rgba(0, 0, 0, 0.08); ctx.fill()
        ctx.restore()
        ctx.arc(PX + 120, PY + 95, 55, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(s['color'])); ctx.fill()
        text(ctx, s['contact'][0], PX + 120, PY + 97, 62, hexc('#FFFFFF'), ink=INK, sw=0)
        ctx.select_font_face(SANS, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(52)
        ctx.set_source_rgba(*hexc('#1C1C28')); ctx.move_to(PX + 200, PY + 90); ctx.show_text(s['contact'])
        ctx.set_font_size(32); ctx.set_source_rgba(0.45, 0.45, 0.5, 1)
        typing = any(k == 'typing' and rt >= tr and not any(tr < t2 <= rt for t2, k2, _ in s['msgs'] if k2 != 'typing' and t2 > tr)
                     for tr, k, _ in s['msgs'])
        ctx.move_to(PX + 200, PY + 135); ctx.show_text('typing...' if typing else 'online')
        # messages (bottom-anchored: newest at the bottom, older ones pushed up)
        items = []
        for (tr, kind, msg) in s['msgs']:
            if rt < tr: continue
            if kind == 'typing':
                nxt = [t2 for t2, k2, _ in s['msgs'] if t2 > tr and k2 != 'typing']
                if nxt and rt >= nxt[0]: continue
            items.append((tr, kind, msg))
        blocks = []
        for (tr, kind, msg) in items:
            k = ease_back((rt - tr) / 0.28)
            if kind in ('me', 'them'):
                size = self.c.get('font', 60) if len(msg) < 30 else self.c.get('font_small', 52)
                lines = wrap_lines(ctx, msg, size, PW * 0.62)
                lw = max(ctx.text_extents(ln).x_advance for ln in lines)
                bh = len(lines) * size * 1.25 + 44
                blocks.append(('bubble', kind, lines, size, lw, bh, k))
            elif kind == 'typing':
                blocks.append(('typing', None, None, 0, 150, 90, k))  # fixed size
            elif kind == 'call':
                blocks.append(('call', None, msg, 0, 0, 100, k))
            elif kind == 'seen':
                blocks.append(('seen', None, msg or 'Seen', 0, 0, 44, k))
            elif kind == 'system':
                blocks.append(('system', None, msg, 0, 0, 70, k))
        y = PY + PH - 50
        ctx.save(); ctx.rectangle(PX, PY + 175, PW, PH - 175); ctx.clip()
        for b in reversed(blocks):
            typ, kind, lines, size, lw, bh, k = b
            y -= bh + 22
            if typ == 'bubble':
                bw = lw + 70; me = kind == 'me'
                x = PX + PW - 40 - bw if me else PX + 40
                ctx.save(); cx_ = x + (bw if me else 0); ctx.translate(cx_, y + bh); ctx.scale(k, k); ctx.translate(-cx_, -(y + bh))
                rrect(ctx, x, y, bw, bh, 40)
                ctx.set_source_rgba(*hexc('#2F80FF' if me else '#E4E6EE')); ctx.fill()
                ctx.select_font_face(SANS, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
                ctx.set_source_rgba(*(hexc('#FFFFFF') if me else hexc('#16161E')))
                for i, ln in enumerate(lines):
                    ctx.move_to(x + 35, y + 22 + size * 0.95 + i * size * 1.25); ctx.show_text(ln)
                ctx.restore()
            elif typ == 'typing':
                x = PX + 40; rrect(ctx, x, y, 150, 90, 40); ctx.set_source_rgba(*hexc('#E4E6EE')); ctx.fill()
                for j in range(3):
                    a = 0.35 + 0.65 * max(0, math.sin(rt * 9 - j * 0.9))
                    ctx.arc(x + 42 + j * 33, y + 45 - 6 * a, 11, 0, 2 * math.pi); ctx.set_source_rgba(0.4, 0.4, 0.45, a); ctx.fill()
            elif typ == 'call':
                x = PX + 40; ctx.save(); ctx.translate(x, y + 100); ctx.scale(1, k); ctx.translate(-x, -(y + 100))
                rrect(ctx, x, y, PW - 80, 100, 30); ctx.set_source_rgba(*hexc('#FFE3E3')); ctx.fill()
                ctx.select_font_face(SANS, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(44)
                ctx.set_source_rgba(*hexc('#E5303B')); ctx.move_to(x + 40, y + 65); ctx.show_text(lines)
                ctx.restore()
            elif typ == 'seen':
                ctx.select_font_face(SANS, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(32)
                ww = ctx.text_extents(lines).x_advance
                ctx.set_source_rgba(0.45, 0.45, 0.5, k); ctx.move_to(PX + PW - 50 - ww, y + 32); ctx.show_text(lines)
            elif typ == 'system':
                ctx.select_font_face(SANS, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(36)
                ww = ctx.text_extents(lines).x_advance
                ctx.set_source_rgba(0.45, 0.45, 0.5, k); ctx.move_to(PX + PW / 2 - ww / 2, y + 45); ctx.show_text(lines)
        ctx.restore()

    def frame(self, t):
        c = self.c
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
        i = self.scene_at(t); s = c['scenes'][i]
        a, b = c.get('bg', ['#FFD86B', '#FF7AA2'])
        a = s.get('bg', [a, b])[0]; b = s.get('bg', [a, b])[1]
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc(a)); g.add_color_stop_rgba(1, *hexc(b))
        ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
        # swipe in from the right for the first 0.25 s of a scene (not the first scene: frame 0 is already mid-action)
        sw = 0.0
        if i > 0:
            k = min(1, (t - s['t']) / 0.25); sw = (1 - (1 - (1 - k) ** 3)) * W
        # phone body
        ctx.save(); ctx.translate(sw, 0)
        rrect(ctx, PX - 34, PY - 40, PW + 68, PH + 80, 80); fill_stroke(ctx, hexc('#1C1C28'), 10)
        self.draw_scene(ctx, s, t)
        ctx.restore()
        if sw > 0 and i > 0:  # previous scene sliding out
            ctx.save(); ctx.translate(sw - W, 0)
            p = c['scenes'][i - 1]
            rrect(ctx, PX - 34, PY - 40, PW + 68, PH + 80, 80); fill_stroke(ctx, hexc('#1C1C28'), 10)
            self.draw_scene(ctx, p, s['t'] - 0.001)
            ctx.restore()
        # header + tag
        text(ctx, c['header'], W / 2, 130, 66, hexc('#FFFFFF'), ink=INK, sw=16, shadow=hexc('#000000', 0.3))
        kt = min(1, (t - s['t']) / 0.25) if t > 0.01 else 1
        text(ctx, s['tag'], W / 2, 300, 110, hexc(s.get('tag_color', '#FFE14D')), ink=INK, sw=20, rot=-0.03,
             scale=0.5 + 0.5 * ease_back(kt), shadow=hexc('#000000', 0.35))
        for (t0, t1, msg, y, size, col) in c.get('cards', []):
            if t0 <= t < t1:
                k = 1 if t0 <= 0 else min(1, (t - t0) * 5)
                text(ctx, msg, W / 2, y, size, hexc(col), ink=INK, sw=18, scale=0.6 + 0.4 * k, rot=-0.04, shadow=hexc('#000000', 0.5))
        if c.get('footer'):
            text(ctx, c['footer'], W / 2, 1785, 50, hexc('#FFFFFF'), ink=INK, sw=12)
        return surf

    def audio(self, dst):
        c = self.c; n = int(c['duration'] * sound.SR); bus = np.zeros(n + sound.SR * 2)
        mus = sound.music(c.get('mood', 'playful'), c['duration'], c.get('seed', 3))
        bus[:len(mus)] += mus * 0.55
        for i, s in enumerate(c['scenes']):
            if i > 0: sound.place(bus, sound.syn_swoosh(0.3), s['t'], 0.6)
            for (tr, kind, _m) in s['msgs']:
                at = s['t'] + tr
                if at >= s['end'] or at < 0: continue
                if kind == 'me': sound.place(bus, sound.syn_swoosh(0.18), at, 0.45)
                elif kind == 'them': sound.place(bus, sound.syn_pop(0.09, 900, 1500), at, 0.8)
                elif kind == 'call':
                    for j in range(2): sound.place(bus, sound.syn_ding(), at + j * 0.18, 0.35)
                elif kind == 'typing':
                    for j in range(4): sound.place(bus, sound.syn_tick(), at + j * 0.12, 0.25)
        for (t0, _t1, _m, _y, _s, _c) in c.get('cards', []):
            sound.place(bus, sound.syn_thud(), t0, 0.6)
        bus = bus[:n]; peak = np.max(np.abs(bus)) + 1e-9
        bus = np.tanh(bus / peak * 1.2) / np.tanh(1.2) * 0.9
        k = int(0.03 * sound.SR); bus[-k:] *= np.linspace(1, 0, k)
        with wave.open(dst, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sound.SR)
            w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())


def render(path, frames=None):
    cfg = json.load(open(path)); epdir = os.path.dirname(os.path.abspath(path)); eid = cfg['id']
    r = Chat(cfg)
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


if __name__ == '__main__':
    a = sys.argv[1:]; fr = None
    if '--frames' in a:
        i = a.index('--frames'); fr = [float(x) for x in a[i + 1:]]; a = a[:i]
    render(a[0], fr)
