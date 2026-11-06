# AIVOOMA engine

Pure-code 2D animation: cairo draws every frame, numpy makes music and effects, ffmpeg encodes.
No paid generator is needed to render. One `episode.json` = one video.

```
pip install --break-system-packages pycairo numpy pillow   # ffmpeg must be installed
# font: Luckiest Guy (OFL). If missing:
#   npm pack @fontsource/luckiest-guy && tar xzf *.tgz && pip install --break-system-packages fonttools brotli
#   python3 -c "from fontTools.ttLib import TTFont; f=TTFont('package/files/luckiest-guy-latin-400-normal.woff2'); f.flavor=None; f.save('/root/.fonts/LuckiestGuy.ttf')" && fc-cache -f
python3 engine/render.py episodes/<id>/episode.json --frames 0.5 3 6 9   # keyframes + sheet.png (LOOK at it)
python3 engine/render.py episodes/<id>/episode.json                     # -> episodes/<id>/<id>-v<ver>.mp4 (~35 s)
python3 engine/brand.py                                                  # avatar + banner
```

Files: `core.py` (tracks, easing, text), `nugget.py` (the cat), `world.py` (backgrounds, props, effects),
`sound.py` (music, SFX, mix), `render.py` (episode loader + renderer), `brand.py` (channel art).
`proto_sour_cat*.py` = the first prototype (sour-cat-lemon), kept for reference.

## Canvas
1080x1920, 30 fps. Floor line y≈1330. Text lives at y 250–330 (screen space). Keep the action between x 80 and 1000
and above y 1650 (the Shorts UI covers the bottom and right edge).

## episode.json
```json
{
  "id": "slug", "ver": 1, "duration": 14,
  "format": "interactive_protect | interactive_play | relatable_owner | reaction | mini_story | <new>",
  "situation": "...", "twist": "...", "title": "YouTube title (≤60 chars, 1–2 emoji)", "description": "...",
  "scene": {"name": "kitchen | living | living_b | bedroom_night | bedroom_day | hallway | plain", "tracks": {"wall": [[0, "#hex"]], "lamp": [[0, 0]], "dark": [[0, 0.3]]}},
  "camera": {"zoom": [[t, z]], "fx": [[t, x]], "fy": [[t, y]], "px": [[t, pan_x]], "py": [[t, pan_y]], "shake": [[t, px]]},
  "actors": [ {"id": "...", "kind": "nugget | prop | fx", "type": "<prop/fx type>", "screen": false, "tracks": {...}} ],
  "audio": {"music": [{"mood": "...", "seed": 1, "gain": [[t, g, "step"?]]}], "sfx": [[t, "name", gain, {"dur", "loop", "start", "rate", "fade"}]]}
}
```
**Tracks** are keyframes `[t, value]` or `[t, value, ease]`. Numbers and number lists interpolate (ease shapes the move INTO
that key: linear, in, out, inout (default), back, bounce, elastic, step). Strings/bools/null hold until the next key.
Every actor accepts `x, y, scale, rot, alpha, shake, show, flip`. Actors draw in list order (later = in front).
`screen: true` draws without camera (use for titles and flashes).
Camera zooms around (fx, fy), which stays put on screen; use `px`/`py` to pan (e.g. px=380 moves the view right).

**Nugget** (`kind: nugget`): `x, y` = body centre (sitting at scale s on the floor: y ≈ 1330 − 170·s + 95),
`scale` (0.6–1.0), `flip` (use `"step"` ease, never interpolate 1→−1), `pose` sit|loaf|run, `run_speed`,
`eye` normal|big|happy|closed|wide|squeeze|heart|dizzy, `look` [x,y] −1..1, `lid` 0..1, `blink` (auto if absent),
`mouth` smile|line|frown|chew|o|open|scream|pant|pucker, `mk` 0..1 (mouth size), `tongue`, `blush`, `green`, `red`,
`puff` (fur stands up), `ear` (−0.3 up … 1 flat), `squish`, `tail` (wag), `headtilt`, `inflate` 0..0.5 (balloon),
`paw` / `paw2` [x,y] local coords or null, `sunglasses`, `wet`. Head centre is local (0, −295).

**Props**: lemon(flat, bitten) · cucumber(eyes, pickle, bitten) · vacuum(on, face) · clock(time) · bed(wake) · mug(label,color)
· table(w,h) · shards · fancybed(price, tag) · box(part back|front|all, w, h, label) · tv(mode fish|static|off, crack, wobble)
· treat · plate · bowl(fill, label). Origins are at the object's floor contact point.

**FX**: text(text, size, fill, ink, pop, tilt, pulse, shadow) · target(r, label) · hand(pose palm|finger; rotate π to come
from the top; fingertip is 240 px above origin) · burst(r) · sweat · hearts · zzz · speed(angle, length) · dust · mark(char)
· sparkle(r) · waves · flash · sunburst · stars.

**Music moods** (procedural, seeded → every video gets its own tune): playful, tense, sneaky, cozy, night, triumph.
**SFX**: files in assets/sfx (aww, boing, box, crash, meow, purr, run, scared, scratch, sniff, vacuum, whoosh, yowl) and
synth (pop, ding, thud, slide_up, slide_down, swoosh, purr_long, vacuum_long, static, sparkle, crunch, tick, wobble, heartbeat).
`purr.mp3`, `vacuum.mp3`, `run.mp3` are short: use `"loop": true` + `"dur"`, or the synth `*_long` versions.
`scared.mp3` is 18 s: always pass `"start": 0.3, "dur": 1.2`.

## Batch 2 additions (2026-10-31) — `extra.py`, `build.py`
- **Gravy the turkey** (`kind: prop, type: turkey`), 2nd original character: anxious round turkey. Origin = feet, ~560 px tall at
  scale 1 (head centre local (0,−440)). Params: `eye` normal|wide|happy|closed|heart|side, `look`, `mouth` closed|smile|open|scream,
  `flap` 0..1 (wings up), `fan` (tail spread, 1 = normal), `walk` + `bob` (walk cycle), `sweat`, `blush`, `disguise` (paper cat ears,
  headband, marker whiskers, pink nose). `flip` works like any prop.
- Backgrounds: **backyard** (autumn tree, picket fence, grass with fallen leaves; tracks `sky1`, `sky2`), **bathroom** (mint tiles,
  bathtub right, pink towel left, round window).
- Props: leafpile(w, h, seed, jiggle, part back|front|all) · mirror(part glass|frame; glass centre (0,−500), rx 250 ry 400) ·
  foodbag(label, color, shake) · calendar(month, day, color, circle, flip; origin = top hook) · toymouse(tag) · yarn · bottlecap ·
  pizzabox(open 0..1, label) · fork(giant, origin = tip) · sign(label) · bowl2(hole 0..1 = bare middle, label).
- FX: leaves(n, seed, wind; use `screen: true`) · badge(label, color: numbered 1/2/3 choice circle).
- Actor `"clip": [cx, cy, rx, ry]` clips that actor to an ellipse (used for the reflection inside the mirror).
- Music mood **hoedown** (152 bpm, walking bass, drums). Synth SFX **gobble** (turkey), **rustle** (treat bag, takes `dur`).
- `build.py`: write episodes in Python (`episodes/<id>/make.py` → episode.json). Helpers `Ep.nugget/prop/fx/card/music/sfx`, `shown()`.
- Hand from the TOP (`rot: π`): the palm bottom sits ≈250 px below the origin y; to cover something at y Y use origin y ≈ Y − 250.

## Pitfalls already hit
- `scale` 0 is skipped automatically, but never interpolate `flip` through 0.
- A cat that rides/sits on a prop must be drawn after it: duplicate the Nugget actor and swap with `show`.
- Zooming near a frame edge pushes things off screen: pan with `px`.
- Keep props big enough to read on a phone (cucumber ≥0.7, TV ≥1.0, box ≥1.1).
- Always render `--frames` and look at sheet.png before the full render.
- Never let a prop scale an axis to exactly 0 (cairo "invalid matrix"): guard flip/squash animations (calendar flip crashed once).
- Wall decor near the top (y < 340) hides under the title text; hang calendars/signs at y ≥ 420.
- `living` background had a stray full-width line at y 1180 (fixed 2026-10-31).

## Backgrounds (keep adding — see anti-monotony rules in ../README.md)
- kitchen: counter, cabinets, tiled floor. living: red curtains window, picture, blue sofa, oval rug.
- living_b: bookshelf left, floor lamp, window with blinds right, yellow rectangular rug, diamond wallpaper.
- bedroom_night: dark, nightstand + lamp right. bedroom_day: striped wall, string lights, wall shelf + plant, purple carpet.
- hallway: blue front door right, coat hooks left, wainscot panels, tiled floor + red runner.
- All take `wall` color. Cat floor line is y≈1330–1500. Added: backyard, bathroom. Ideas for next ones: car, office desk, vet waiting room, snowy porch, kitchen table at Thanksgiving.

## Batch 3 additions (2026-11-07) — `extra3.py`, panels
- **Panels / split screen** (render.py): episode key `"panels": [{"rect": [x, y, w, h], "ox", "oy", "s", "scene": {param overrides}}]`
  (build.py: `e.panels(dict(...), dict(...))`). Each panel shows the world region starting at (ox, oy) scaled by s inside the rect.
  Actors with `"panel": i` (build: `panel=i`) draw only in that panel; others draw in all. Camera zoom still applies; shake/px/py do not.
  Used for spot-the-difference (spot-diff-kitchen) and expectation vs reality (expect-jump). Good values: rects [40, 290|330, 1000, 610-660],
  s = 1000/1080, oy ≈ 590-650 for a sitting cat on the floor.
- Background **dining**: Thanksgiving dining room; the plaid tablecloth top IS the floor line (y 1330), characters sit on the table.
- Props: whipcan(spray 0..1, jet; rot −π/2 = nozzle pointing left) · pie(cream) · cookiejar(lid 0..1, n, label) · cookie(half, crumb) ·
  tunacan(open 0..1, label, color) · scale(reading text, glow) · yogamat(color).
- FX: cream(amount, w, h, seed: merged fluffy blob, beard/helmet) · ring(draw 0..1, r, sy, label, color: "found it" circle) ·
  caption(top, text, size: bottom subtitle box) · timerbar(left 0..1, label) · tag(text, color, w: pill label) ·
  **ownerhand** (solid skin hand + sleeve = the OWNER's hand; `hand` stays the viewer's translucent hand).
- build.py `card()` at t0 = 0 now starts full size (frame 0 used to show a tiny popping title).
- Pitfall: camera `fx/fy` do NOT pan (they are the zoom pivot that stays put). To move the view use `px`/`py`.
- Blobs/jets made of overlapping circles: draw all outlines first, then all fills, or they look like a pile of bubbles.
