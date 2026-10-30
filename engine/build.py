"""Tiny helpers to write episode.json from Python (batch 2+). Keeps episode scripts short.

    from build import Ep
    e = Ep('my-id', 14, 'reaction', scene='kitchen')
    e.nugget('nug', x=330, y=1280, scale=0.85, eye=[[0, 'happy'], [3, 'wide']])
    e.card('t1', 'HELLO', 0, 4)
    e.save()  # -> episodes/my-id/episode.json
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _tr(v):
    """A constant becomes [[0, v]]; a list of [t, v(, ease)] keys passes through."""
    if isinstance(v, list) and v and isinstance(v[0], list) and len(v[0]) in (2, 3) and isinstance(v[0][0], (int, float)):
        return v
    return [[0, v]]


def shown(*spans):
    """show track visible only inside (t0, t1) spans."""
    keys = [[0, False]]
    for a, b in spans:
        keys += [[a, True, 'step'], [b, False, 'step']]
    return keys


class Ep:
    def __init__(self, id, dur, fmt, scene='plain', ver=1, **meta):
        self.d = dict(id=id, ver=ver, duration=dur, format=fmt, scene={'name': scene}, camera={}, actors=[],
                      audio={'music': [], 'sfx': []}, **meta)

    def scene_tracks(self, **tr):
        self.d['scene']['tracks'] = {k: _tr(v) for k, v in tr.items()}

    def cam(self, **tr):
        self.d['camera'].update({k: _tr(v) for k, v in tr.items()})

    def add(self, id, kind, type=None, screen=False, clip=None, **tr):
        a = dict(id=id, kind=kind, tracks={k: _tr(v) for k, v in tr.items()})
        if type: a['type'] = type
        if screen: a['screen'] = True
        if clip: a['clip'] = clip
        self.d['actors'].append(a)
        return a

    def nugget(self, id, **tr):
        return self.add(id, 'nugget', **tr)

    def prop(self, id, type, **tr):
        return self.add(id, 'prop', type, **tr)

    def fx(self, id, type, screen=False, **tr):
        return self.add(id, 'fx', type, screen=screen, **tr)

    def card(self, id, msg, t0, t1=None, size=100, fill='#FFFFFF', y=250, pulse=0, x=540, tilt=0.0):
        alpha = [[0, 0], [t0, 1, 'step']] if t0 > 0 else [[0, 1]]
        if t1 is not None:
            alpha.append([t1, 0, 'step'])
        return self.fx(id, 'text', screen=True, x=x, y=y, text=msg, size=size, fill=fill, pulse=pulse, tilt=tilt,
                       pop=[[0, 0.2], [t0, 0.2], [t0 + 0.3, 1, 'back']], alpha=alpha)

    def music(self, mood, seed, gain=None, volume=1.0):
        self.d['audio']['music'].append(dict(mood=mood, seed=seed, gain=gain or [[0, 1]], volume=volume))

    def sfx(self, t, name, g=1.0, **opts):
        self.d['audio']['sfx'].append([t, name, g, opts] if opts else [t, name, g])

    def save(self):
        out = os.path.join(ROOT, 'episodes', self.d['id'])
        os.makedirs(out, exist_ok=True)
        p = os.path.join(out, 'episode.json')
        with open(p, 'w') as f:
            json.dump(self.d, f, indent=1, ensure_ascii=False)
        return p
