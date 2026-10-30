"""Render an AIVOOMA episode.

  python3 engine/render.py episodes/<id>/episode.json            -> episodes/<id>/<id>-v<ver>.mp4
  python3 engine/render.py episodes/<id>/episode.json --frames 0.5 3 6   -> keyframe PNGs + contact sheet
  python3 engine/render.py episodes/<id>/episode.json --audio-only

episode.json (see engine/README.md for the full spec):
{
  "id": "...", "ver": 1, "duration": 14,
  "scene": {"name": "kitchen", "tracks": {...}},
  "camera": {"zoom": [[0, 1.1]], "fx": [[0, 540]], "fy": [[0, 1000]], "shake": [[0, 0]]},
  "actors": [ {"kind": "nugget"|"prop"|"fx", "type": "...", "screen": false, "tracks": {name: [[t, value, ease?], ...]}} ],
  "audio": {"music": {"mood": "playful", "seed": 3, "gain": [[0, 1], [4, 0, "step"]]}, "sfx": [[t, "name", gain, {opts}]]}
}
"""
import json
import zlib
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairo  # noqa: E402
from core import W, H, FPS, Track  # noqa: E402
import nugget  # noqa: E402
import world  # noqa: E402
import sound  # noqa: E402
import extra  # noqa: E402,F401  (registers batch-2 backgrounds/props/fx)


SELF_ALPHA = {'text', 'hearts', 'sweat', 'zzz', 'burst', 'speed', 'dust', 'sparkle', 'waves', 'flash', 'sunburst', 'hand', 'leaves'}


class Episode:
    def __init__(self, path):
        self.path = path
        self.dir = os.path.dirname(os.path.abspath(path))
        with open(path) as f:
            self.d = json.load(f)
        self.id = self.d['id']
        self.dur = float(self.d['duration'])
        self.scene = self.d.get('scene', {'name': 'plain'})
        self.scene_tracks = {k: Track(v) for k, v in self.scene.get('tracks', {}).items()}
        cam = self.d.get('camera', {})
        self.cam = {k: Track(cam.get(k, [[0, dflt]])) for k, dflt in (('zoom', 1.0), ('fx', 540), ('fy', 1000), ('shake', 0), ('px', 0), ('py', 0))}
        self.actors = []
        for a in self.d['actors']:
            self.actors.append(dict(a, _tracks={k: Track(v) for k, v in a.get('tracks', {}).items()}))

    def values(self, actor, t):
        vals = {k: tr.at(t) for k, tr in actor['_tracks'].items()}
        vals.update({k: v for k, v in actor.get('static', {}).items() if k not in vals})
        return vals

    def draw_actor(self, ctx, a, t):
        p = self.values(a, t)
        if p.get('show') is False:
            return
        alpha = p.get('alpha', 1.0)
        if alpha is not None and alpha <= 0.005:
            return
        if abs(p.get('scale', 1.0) or 0) < 0.01:
            return
        kind = a['kind']
        sh = p.get('shake', 0) or 0
        jx, jy = (sh * math.sin(t * 91 + zlib.crc32(a.get('id', '').encode()) % 7), sh * 0.7 * math.cos(t * 79)) if sh else (0, 0)
        group = alpha is not None and alpha < 0.999 and not (kind == 'fx' and a['type'] in SELF_ALPHA)
        clip = a.get('clip')  # [cx, cy, rx, ry] ellipse in world/screen coords (e.g. inside a mirror)
        if clip:
            ctx.save(); ctx.translate(clip[0], clip[1]); ctx.scale(clip[2], clip[3]); ctx.arc(0, 0, 1, 0, 2 * math.pi)
            ctx.restore(); ctx.save(); ctx.clip()
        if group:
            ctx.push_group()
        if kind == 'nugget':
            q = dict(p); q['x'] = p.get('x', 540) + jx; q['y'] = p.get('y', 1255) + jy
            nugget.draw(ctx, t, q)
        else:
            fn = (world.PROPS if kind == 'prop' else world.FX)[a['type']]
            ctx.save()
            ctx.translate(p.get('x', 540) + jx, p.get('y', 960) + jy)
            ctx.rotate(p.get('rot', 0.0) or 0.0)
            s = p.get('scale', 1.0)
            ctx.scale(s * (p.get('flip', 1) or 1), s)
            if kind == 'fx' and 'alpha' not in p:
                p['alpha'] = 1.0
            fn(ctx, t, p)
            ctx.restore()
        if group:
            ctx.pop_group_to_source(); ctx.paint_with_alpha(alpha)
        if clip:
            ctx.restore()

    def frame(self, t):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        ctx = cairo.Context(surf)
        ctx.set_antialias(cairo.ANTIALIAS_BEST)
        z = self.cam['zoom'].at(t); fx = self.cam['fx'].at(t); fy = self.cam['fy'].at(t); csh = self.cam['shake'].at(t)
        ctx.save()
        ctx.translate(csh * math.sin(t * 97), csh * 0.8 * math.cos(t * 83))
        # zoom around the focus point (it stays where it is on screen); pan with camera px/py
        ctx.translate(-self.cam['px'].at(t), -self.cam['py'].at(t))
        ctx.translate(fx, fy); ctx.scale(z, z); ctx.translate(-fx, -fy)
        sp = {k: tr.at(t) for k, tr in self.scene_tracks.items()}
        world.BACKGROUNDS[self.scene['name']](ctx, t, sp)
        for a in self.actors:
            if not a.get('screen'):
                self.draw_actor(ctx, a, t)
        ctx.restore()
        dark = sp.get('dark', 0) or 0
        if dark > 0:
            ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.02, 0.03, 0.1, dark); ctx.fill()
        vg = cairo.RadialGradient(W / 2, H / 2, 500, W / 2, H / 2, 1250)
        vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0, 0.26)
        ctx.rectangle(0, 0, W, H); ctx.set_source(vg); ctx.fill()
        for a in self.actors:
            if a.get('screen'):
                self.draw_actor(ctx, a, t)
        return surf


def render(path, frames=None, audio_only=False):
    ep = Episode(path)
    ver = ep.d.get('ver', 1)
    if frames:
        from PIL import Image
        ims = []
        for tt in frames:
            fp = os.path.join(ep.dir, f'kf_{tt:05.2f}.png'); ep.frame(tt).write_to_png(fp); ims.append(Image.open(fp))
        cols = min(len(ims), 6); rows = (len(ims) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * 270, rows * 480), 'white')
        for i, im in enumerate(ims):
            sheet.paste(im.convert('RGB').resize((270, 480)), ((i % cols) * 270, (i // cols) * 480))
        sp = os.path.join(ep.dir, 'sheet.png'); sheet.save(sp); print(sp); return sp
    wav = os.path.join(ep.dir, f'{ep.id}.wav')
    sound.mix(ep.d.get('audio', {}), ep.dur, wav, seed=ep.d.get('seed', zlib.crc32(ep.id.encode()) % 1000))
    if audio_only:
        print(wav); return wav
    silent = os.path.join(ep.dir, f'{ep.id}-silent.mp4')
    n = int(round(ep.dur * FPS))
    proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                             '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                             '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    for i in range(n):
        s = ep.frame(i / FPS); s.flush(); proc.stdin.write(bytes(s.get_data()))
    proc.stdin.close(); proc.wait()
    out = os.path.join(ep.dir, f'{ep.id}-v{ver}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(silent); os.remove(wav)
    print(out); return out


if __name__ == '__main__':
    args = sys.argv[1:]
    path = args[0]
    if '--frames' in args:
        render(path, frames=[float(x) for x in args[args.index('--frames') + 1:]])
    else:
        render(path, audio_only='--audio-only' in args)
