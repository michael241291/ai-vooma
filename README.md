# ai-vooma

Production repo for the YouTube Shorts channel **AIVOOMA** (overseas / US audience).
Videos are built automatically by Claude and scheduled through Buffer. This repo is public on purpose:
finished videos are served to Buffer from `raw.githubusercontent.com`.

## Characters (current, not locked)
**Nugget** — an original chubby orange cartoon cat, naive and clumsy ("one brain cell" orange-cat energy).
**Gravy** (added 2026-10-31, experiment) — an original round, anxious brown turkey who knows what November means; Thanksgiving arc with Nugget as his unreliable roommate.
Nugget is the current main character, NOT a permanent rule. The channel follows what is new and working:
new characters (other animals, side characters, a rival, an owner), new formats and new styles are added whenever
research or channel data shows something new. All designs must be original; never copy another channel's character or drawings.

## Evolution rules (always follow what is new)
11. Every weekly batch: at least 2 of 7 videos are experiments from the latest research — a new format, a new character,
    a new art/scene style or a new trend — not just new Nugget situations.
12. Experiments that beat the channel median for 2 weeks get a bigger share next week; formats or characters that stay
    below median for 2 weeks are reduced or dropped. Data decides, not habit.
13. If research shows a clearly stronger direction (e.g. a different animal or a non-cat niche), shift the channel step by
    step (more experiments each week) and tell the user in the weekly report. Never pivot everything in one week.
14. Every new character, format or style is added to ideas.json, engine/README.md and learnings.md so later runs reuse it.

## Layout
| Path | What |
|---|---|
| `engine/` | Code that draws, animates, scores and renders videos (cairo + ffmpeg + numpy). |
| `assets/sfx/` | Sound-effect library (ElevenLabs, generated once and reused). |
| `episodes/<id>/` | One folder per video: `episode.json` (story) + rendered `<id>-v<n>.mp4`. |
| `log.json` | Every video made: format, situation, twist, title, date, results. Used to block repeats. |
| `ideas.json` | Idea bank, grouped by format. Used ideas are marked, never reused. |
| `learnings.md` | Running list of what works and what doesn't. Updated on every weekly run. |

## Anti-repeat rules (YouTube "inauthentic content" policy)
1. A situation / threat / twist is never used twice.
2. In any 7 videos: at least 3 different formats, and no format more than 3 times.
3. Two videos in a row never share the same format.
4. Every video needs its own scene, props and ending, not just a different title.

## Anti-monotony rules (the channel must not feel like one template)
5. Two videos in a row never use the same background. One background at most 2 times in any 7 videos.
6. Two videos in a row never open with the same music mood.
7. Two videos in a row never share a title template (e.g. "Protect <character> from the X!"). One template at most 2 times per 7 videos.
8. Vary the hook: command text, owner-quote text, question, or no text with a strong visual. Vary length (10–20 s) and wall colors.
9. Every weekly batch adds at least 1 new thing to the engine (background, prop, effect, side character or music mood) and uses it.
10. Write `background`, `opening_mood` and `title_template` in log.json for every video, and check rules 5–7 against the last 7 before planning.

Video URL pattern: `https://raw.githubusercontent.com/michael241291/ai-vooma/main/episodes/<id>/<file>.mp4`

## Creative v2 (4 Nov 2026, after the first 7 videos) — the "template look" is banned
Every video so far opened the same way: title bar at the top, a small calm cat sitting in the middle of a flat room,
nothing moving for 1–2 s. The two videos that got pushed (pet-nugget 1.37k, lemon 1.21k) had something happening or
something to DO in frame 0; the calm openers got 0–14 views. Rules:
15. Frame 0 is the peak, not the setup: the character is already mid-scream / mid-jump / mid-crash, or the viewer's task is
    already on screen. No calm sitting intro. Check kf at 0.0 s and 0.5 s: if nothing is moving, rewrite.
16. Big subject: the main character or object fills ≥50% of the frame at 0 s (close-up), then the camera cuts or punches
    at least every 2–3 s (zoom, pan, new angle). Never one static wide shot for the whole video.
17. Break the layout template: the top title bar is optional, not default. Rotate text styles/positions (caption at the
    bottom, speech bubble, giant one-word reaction, no text). Max 2 videos per 7 with the same text layout.
18. Length 7–12 s and built to loop (last frame leads back into the first), so replays push average view % over 100%.
19. Every video gives a reason to comment or share: a choice (1/2/3), "tag the friend who…", a rating, or a wrong-looking
    ending. Titles describe what the viewer sees or does; do not lead with the name "Nugget" (new viewers don't know him).
20. Each batch tries at least 1 completely different visual format, not just a new situation in a room: e.g.
    spot-the-difference / find-the-odd-one puzzle, first-person POV, satisfying loop, transformation/glow-up reveal,
    fake "cat translator" subtitles, split-screen expectation vs reality, a new art style or palette.
