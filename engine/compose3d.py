"""Composite a transparent 3D render (engine/shell3d.py etc.) over a Pixabay video background, add captions
(Luckiest Guy, outlined) and the procedural soundtrack, and write the final 1080x1920 MP4.

Usage: python3 engine/compose3d.py episodes/<id>/comp.json
comp.json: {"id", "frames": dir with 0000.png..., "layout": layout.json path (optional), "bg": video path,
            "bg_crop_x": px in source, "bg_blur": sigma, "dur", "fps",
            "captions": [{"text", "t0", "t1", "y", "size", "fill", "x" (default 540), "slot": 1..3 (x/y from layout)}],
            "audio": {"music": {...}, "sfx": [[t, name, gain, opts], ...]}, "out": mp4 path}
"""
import json
import os
import subprocess
import sys

import cairo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sound  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
FONT = 'Luckiest Guy'


def rp(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def caption_png(c, dst):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(s)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    size = c.get('size', 96); ctx.set_font_size(size)
    lines = c['text'].split('\n')
    y = c['y']
    for ln in lines:
        ext = ctx.text_extents(ln)
        x = c.get('x', 540) - ext.width / 2 - ext.x_bearing
        ctx.move_to(x, y); ctx.text_path(ln)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgba(0.07, 0.04, 0.12, 0.95); ctx.set_line_width(size * 0.22); ctx.stroke_preserve()
        ctx.set_source_rgb(*hexrgb(c.get('fill', '#FFFFFF'))); ctx.fill()
        y += size * 1.08
    s.write_to_png(dst)


def main(cfg_path):
    C = json.load(open(cfg_path))
    ep_dir = os.path.dirname(os.path.abspath(cfg_path))
    work = os.path.join(C.get('work', '/tmp/claude-0/compose3d'), C['id']); os.makedirs(work, exist_ok=True)
    fps, dur = C.get('fps', 25), C['dur']
    lay = json.load(open(rp(C['layout']))) if C.get('layout') else {}
    # captions
    caps = []
    for k, c in enumerate(C.get('captions', [])):
        c = dict(c)
        if 'slot' in c and lay:
            x, y = lay['slots_px'][c['slot'] - 1]
            c.setdefault('x', x); c['y'] = c.get('y', y)
        c['text'] = c['text'].replace('{answer}', str(lay.get('answer', '?')))
        p = os.path.join(work, f'cap{k:02d}.png'); caption_png(c, p); caps.append((p, c['t0'], c['t1']))
    # audio
    au = C.get('audio', {})
    sfx = list(au.get('sfx', []))
    if au.get('swoosh_swaps') and lay:
        for t0, d in lay['swaps']:
            sfx.append([t0, 'swoosh', au.get('swoosh_gain', 0.35), {'dur': max(0.25, d)}])
    wav = sound.mix({'music': au.get('music'), 'sfx': sfx}, dur, os.path.join(work, 'mix.wav'), seed=au.get('seed', 3))
    # ffmpeg graph
    bx = C.get('bg_crop_x', 875); bw = C.get('bg_crop_w', 810); bh = C.get('bg_crop_h', 1440)
    inputs = ['-stream_loop', '-1', '-i', rp(C['bg']),
              '-framerate', str(fps), '-i', os.path.join(rp(C['frames']), '%04d.png')]
    for p, _, _ in caps:
        inputs += ['-loop', '1', '-framerate', str(fps), '-i', p]
    inputs += ['-i', wav]
    g = [f"[0:v]crop={bw}:{bh}:{bx}:0,scale={W}:{H},gblur=sigma={C.get('bg_blur', 9)},"
         f"eq=brightness={C.get('bg_bright', -0.03)}:saturation=1.1,fps={fps},setpts=PTS-STARTPTS[bg]",
         f"[1:v]scale={W}:{H}:flags=lanczos,format=rgba[fg]",
         "[bg][fg]overlay=0:0:format=auto[v0]"]
    last = 'v0'
    for k, (p, t0, t1) in enumerate(caps):
        g.append(f"[{last}][{k + 2}:v]overlay=0:0:enable='between(t,{t0},{t1})'[v{k + 1}]"); last = f'v{k + 1}'
    out = rp(C['out'])
    cmd = ['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(g), '-map', f'[{last}]',
           '-map', f'{len(caps) + 2}:a', '-t', str(dur), '-r', str(fps), '-c:v', 'libx264', '-preset', 'veryfast',
           '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    print(out)


if __name__ == '__main__':
    main(sys.argv[1])
