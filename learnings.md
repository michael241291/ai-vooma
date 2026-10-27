# AIVOOMA — learnings

Newest first. Every weekly run adds what it learned here (from channel data and fresh YouTube research)
before planning the next batch. The weekly skill reads this file first.

## 2026-10-27 — not locked to Nugget (user request)
- User: do not get stuck on Nugget; update whenever something new appears. Rules 11–14 in README: ≥2 of 7 videos per batch are experiments (new format/character/style/trend), data decides the share, shift gradually and report.

## 2026-10-27 — anti-monotony pass (user request)
- Week 1 first draft had the same living-room background 4 times, 3 days in a row, and two "Protect Nugget from the X!" titles. Formats alone are not enough variety; the viewer sees the room first.
- Fix: 3 new backgrounds (living_b, bedroom_day, hallway); now 6 backgrounds in 7 videos, no background or opening mood twice in a row; vacuum title changed to "Hold the vacuum back or Nugget is DONE".
- New standing rules 5–10 in README.md (background, mood, title template, hook, length, 1 new engine element per batch). log.json now records background, opening_mood, title_template.

## 2026-10-27 — first batch built (engine v1)
- Built a reusable code engine (engine/) instead of one-off scripts: Nugget with 8 eye modes, 9 mouths, 3 poses; 4 scenes; 14 props; 15 effects; 6 procedural music moods; 13 file + 14 synth SFX. ~35 s to render a 14 s video.
- Week 1 (planned 29 Oct – 4 Nov, 07:00 WIB): protect-cucumber (interactive_protect), 3am-zoomies (relatable), pet-nugget (interactive_play), sour-cat-lemon (reaction), protect-vacuum (interactive_protect), bed-vs-box (relatable), tv-fish (mini_story). 5 formats, max 2 per format.
- Production lessons: props must be big to read on a phone; never interpolate flip; a cat riding a prop needs a second Nugget actor drawn after it; zooming near an edge needs a px pan; ElevenLabs short SFX (purr, vacuum) come back ~1 s, so long ambiences are synthesized.

## 2026-10-27 — starting research
- Channel state: 253 subs, 23 old Shorts (surreal AI scenes + animal facts), 0–8 views each, 0 likes, 0 comments. No fixed format or character, weak first-second hook, uploads stopped 19 Sep.
- Simple 2D is enough: Hamoudi Animation (white blob cat) gets 1–6M views per interactive Short.
- Format beats art: on the same channel, interactive Shorts ("Protect my cat from X!", "Put your finger on the screen…") get ~10x the views of non-interactive ones (1–4M vs 90–180k).
- Relatable cat-owner moments also work: equmi (2D black cat, channel started Oct 2024) 42k subs, 19.6M views; best titles talk to cat owners ("How do they know it's exactly 3am?").
- Plain silent cat stories with no hook stay small (Mime Toon: 1–2.5k views). 2D "cat eats lemon" Shorts mostly < 6k.
- Interactive anatomy: big command text at second 0 + cat already in danger; finger target appears by second 1–5; the viewer's "hand" protects the cat; funny twist at the end (hand squashes cat → "are you ok?", cat says thanks with a heart). 12–24 s, no dialogue, music + SFX + short text.
- Keep it teen/adult meme humor so videos are not "made for kids" (that would switch off comments and notifications).
- First prototype: `episodes/sour-cat-lemon` (reaction format, 10 s). Not published yet.
