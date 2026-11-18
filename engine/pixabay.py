"""Pixabay photo helper for Tiny Chaos.

Key: environment variable PIXABAY_KEY (never commit it; the repo is public).
Usage:
  PIXABAY_KEY=... python engine/pixabay.py "cozy kitchen" episodes/<id>/bg.jpg [--orientation vertical] [--pick 0]
Writes the image plus <file>.json with the Pixabay page URL, user and tags (for our records).
Notes (Nov 2026): photo downloads work from the cloud sandbox; video files on cdn.pixabay.com answer 429
("Rate limit exceeded") here, so only photos are used. Pixabay has no sound-effect/music API; music is never used
anyway (some Pixabay tracks are registered in Content ID).
Use photos only as backgrounds/props under our own animation and jokes (never a stock image alone = reused content).
"""
import json
import os
import sys
import urllib.parse
import urllib.request


def search(q, orientation='vertical', per_page=20, image_type='photo'):
    key = os.environ['PIXABAY_KEY']
    url = 'https://pixabay.com/api/?' + urllib.parse.urlencode(dict(
        key=key, q=q, image_type=image_type, orientation=orientation, per_page=per_page, safesearch='true',
        order='popular'))
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)['hits']


def fetch(q, dst, orientation='vertical', pick=0):
    hits = search(q, orientation)
    if not hits:
        raise SystemExit(f'no Pixabay results for {q!r}')
    h = hits[min(pick, len(hits) - 1)]
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    req = urllib.request.Request(h['largeImageURL'], headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r, open(dst, 'wb') as f:
        f.write(r.read())
    meta = {k: h[k] for k in ('id', 'pageURL', 'user', 'tags', 'imageWidth', 'imageHeight')}
    json.dump(meta, open(dst + '.json', 'w'), indent=1)
    return dst, meta


if __name__ == '__main__':
    a = sys.argv[1:]
    o = a[a.index('--orientation') + 1] if '--orientation' in a else 'vertical'
    p = int(a[a.index('--pick') + 1]) if '--pick' in a else 0
    print(fetch(a[0], a[1], o, p))
