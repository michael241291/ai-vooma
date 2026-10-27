# ai-vooma

Production repo for the YouTube Shorts channel **AIVOOMA** (overseas / US audience).
Videos are built automatically by Claude and scheduled through Buffer. This repo is public on purpose:
finished videos are served to Buffer from `raw.githubusercontent.com`.

## Main character
**Nugget** — an original chubby orange cartoon cat, naive and clumsy ("one brain cell" orange-cat energy).
Original design; never copy another channel's character or drawings.

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

Video URL pattern: `https://raw.githubusercontent.com/michael241291/ai-vooma/main/episodes/<id>/<file>.mp4`
