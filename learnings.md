# AIVOOMA — learnings

Newest first. Every weekly run adds what it learned here (from channel data and fresh YouTube research)
before planning the next batch. The weekly skill reads this file first.

## 2026-11-25 (Wed WIB, 11:30) — all-3D + Zernio switch (user); 3 videos scheduled in Zernio
- User: posting YouTube via Zernio only (Buffer no longer used), ALL videos 3D, +1–2 s suspense before reveal, and if a 3D render fails make nothing (no 2D fallback).
- Zernio scheduled: 26 Nov ring-shuffle-3d v2 (12.5 s), 27 Nov donut-no-hole-3d (13 s), 28 Nov marble-race-3d (14 s). Buffer copy of ring moved to draft (no double post).
- Engines: odd3d.py (grid odd-one-out, ~7–9 s/frame for 24 donuts + sprinkles), marble3d.py (rigid body: BOX collision on tilted boxes = balls stuck/fall through → use CONVEX_HULL; spawn marbles without overlap; walls flush with ramp ends or marbles skip ramps).
- Renders are now resumable (use_overwrite False + placeholder): a container restart mid-render lost nothing.
- Scheduled task still lacks the Zernio connector (user must add it); its 25 Nov run failed on usage limit.

## 2026-11-25 (Wed WIB, 09:00–10:45) — user: "tidak ada perubahan, harus lebih 3D + Pixabay"; first real 3D video
Buffer metrics 24 Nov 06:00 UTC: keys-cup-shuffle 4,347 (9 comments), we-need-to-talk 3,697, lost-sock 3,332 (3 videos >3k = first breakouts),
social-battery 2,106, cat-loaf 2,050; Thanksgiving skits weak (turkey-protest 1,136; thanksgiving-stomach 2 views at 6 h; gravy-translator fresh).
- User still feels no growth → new visual direction ordered: more 3D + Pixabay images/videos.
- Built engine/shell3d.py (Blender 5.3 via pip `bpy`, Cycles CPU, film transparent) + engine/compose3d.py (Pixabay video bg, captions, audio).
  Cycles 540x960, 12 samples adaptive + OIDN FAST ≈ 3.5 s/frame idle, ≈7 s/frame with other load; EEVEE unusable headless (no GPU).
- Pixabay VIDEO downloads now work (429 earlier was temporary). Shadow-catcher not needed: 3D table in front + blurred video behind looks natural.
- First 3D video ring-shuffle-3d (cup game = best format) scheduled 26 Nov 07:00; wallet-bag-shuffle (2D cup game) moved to 6 Dec to keep 1 cup game per 3+ days.
- Compare at 48 h vs keys-cup-shuffle (4.3k) / wallet-bag-shuffle (2D). If 3D wins, raise 3D share.

## 2026-11-23 (Mon WIB, 05:35) — daily run: SECOND BREAKOUT = we-need-to-talk (chat) 3.5k; no errors
Buffer metrics refreshed 22 Nov 04:09 UTC (new since last run).
| video | type | age at refresh | views | likes | like rate | comments | Δ views vs 21 Nov |
|---|---|---|---|---|---|---|---|
| salary-vs-bills | sim | ~172 h | 1,450 | 8 | 0.55% | 0 | flat |
| odd-mug-out | puzzle | ~160 h | 1,498 | 4 | 0.27% | 0 | flat |
| cat-translator | skit (translator) | ~148 h | 1,263 | 17 | 1.35% | 0 | flat |
| day-off-plinko | sim (plinko) | ~136 h | 1,846 | 5 | 0.27% | 0 | flat |
| cat-loaf-bakery | puzzle | ~124 h | 2,041 | 10 | 0.49% | 1 | flat |
| cat-work-call | skit (WFH) | ~112 h | 1,448 | 10 | 0.69% | 0 | flat |
| coffee-vs-monday | sim (duel) | ~100 h | 31 | 1 | – | 0 | dead |
| keys-cup-shuffle | puzzle (cup game) | ~88 h | **4,328** | 24 | 0.55% | 9 | +147 (+3.5%) — push over |
| black-friday-budget | sim (plinko) | ~76 h | 1,330 | 2 | 0.15% | 0 | flat |
| find-nugget-photo | puzzle (photo) | ~52 h | 1,378 | 8 | 0.58% | 0 | +32 — stopped at seed |
| **we-need-to-talk** | chat | ~40 h | **3,513** | 15 | 0.43% | 1 | **+1,917 (+120%)** — 2nd video >3k |
| social-battery | sim (ring) | ~28 h | 1,991 | 6 | 0.30% | 0 | +794 (+66%) — second push |
| lost-sock | puzzle (odd one out) | ~4 h | 824 | 5 | 0.61% | 0 | new |
- **2nd "tembus": we-need-to-talk (chat "X to different people")**, +120% in a day at 40 h, without a numbered CTA. So the second push is not only comment-bait: the chat format (relatable people, readable text, fast punchlines) also gets it. Both breakouts are formats where the viewer has to READ/TRACK until the end (cup tracking, message replies) → probably high stayed-to-watch. Chat part 2 (last-slice-text, 29 Nov) is already queued; give chat 2 slots in batch 4.
- social-battery (ring sim, relatable "introvert" label) got a second push (+66%) while plinko sims stay flat → sims with a person-label topic beat money/plinko sims.
- find-nugget-photo stopped at the seed (1.4k at 52 h) → photo test B verdict: no advantage over cartoon puzzles; keep max 1 photo video per batch (rule unchanged).
- Daily: gravy-translator scheduled 25 Nov 07:00 (3 scheduled: 23 turkey-protest, 24 thanksgiving-stomach, 25 gravy-translator). 10 drafts to 5 Dec → no batch. No new error. vet-translator / translator-3am-kitchen still show the old error text but are drafts (28 Nov, 1 Dec).
- Batch 4 due ≈ 1–2 Dec (when the 07:00 queue is ≤4 days). Do Apify trend research then (skipped in batch 3).

## 2026-11-22 (Sun WIB, 05:35) — daily + batch 3: 2nd daily-limit ERROR → now 1 video/day (07:00); keys-cup-shuffle keeps growing
Buffer metrics refreshed 21 Nov 05:19 UTC (new since last run).
| video | type | age at refresh | views | likes | like rate | comments | Δ views vs 20 Nov |
|---|---|---|---|---|---|---|---|
| salary-vs-bills | sim | ~149 h | 1,447 | 8 | 0.55% | 0 | flat |
| odd-mug-out | puzzle | ~137 h | 1,496 | 4 | 0.27% | 0 | flat |
| cat-translator | skit (translator) | ~125 h | 1,258 | 17 | 1.35% | 0 | +14 |
| day-off-plinko | sim (plinko) | ~113 h | 1,844 | 5 | 0.27% | 0 | flat |
| cat-loaf-bakery | puzzle (find the cat) | ~101 h | 2,040 | 10 | 0.49% | 1 | +13 — stopped |
| cat-work-call | skit (WFH) | ~89 h | 1,449 | 10 | 0.69% | 0 | +108 |
| coffee-vs-monday | sim (duel) | ~77 h | 29 | 0 | – | 0 | dead |
| **keys-cup-shuffle** | puzzle (cup game) | ~65 h | **4,181** | 23 | 0.55% | **9** | **+1,165 (+39%)** — still a 2nd/3rd push |
| black-friday-budget | sim (plinko) | ~53 h | 1,324 | 2 | 0.15% | 0 | flat |
| find-nugget-photo | puzzle (photo) | ~29 h | 1,346 | 9 | 0.67% | 0 | +294 |
| we-need-to-talk | chat | ~17 h | 1,596 | 13 | **0.82%** | 1 | new — best like rate after translator |
| social-battery | sim (ring) | ~5 h | 1,197 | 5 | 0.42% | 0 | new |
- **2nd Buffer error "daily posting limit"**: vet-translator (21 Nov 19:00 WIB). Both errors were the 19:00 slot of a day whose 07:00 slot had posted, while 20 Nov had 2 successes. Per the rule, the channel is now on **1 video/day at 07:00 WIB** (ROUTINE.md updated). vet-translator → draft 28 Nov 07:00 (not reuploaded). Retry 2/day only after ~2 clean weeks, and tell the user.
- keys-cup-shuffle is the only video still growing after 48 h (+39%/day at 65 h). Commit-before-reveal = the channel's working lever. Batch 3 puts a numbered guess in 6 of 7 videos (shell part 2, battery sim guess, memory 1-6, spot score 0-3, race 1-6, Gravy vote 1/2; chat asks "who hides the pie").
- Photo test B verdict (48 h rule not reached yet, ~29 h): find-nugget-photo 1,346 vs cat-loaf 1,592 at a similar age (−15%), like rate 0.67% vs 0.63%. Within ±30% → keep exactly 1 photo video per batch (spot-diff-photo this batch).
- Chat format (we-need-to-talk 0.82%, 1 comment) is the 2nd-best like rate → part 2 in batch 3 (last-slice-text).
- Trend research skipped this run (time went to the 2-new-engine batch). Do Apify trend research at the next batch.
- Batch 3 (made 22 Nov, all 07:00 WIB): 27 wallet-bag-shuffle (shell part 2, Black Friday) · 29 last-slice-text (chat) · 30 phone-battery-guess (ring sim + guess, EXP) · 2 Dec memory-gifts (NEW memory.py, EXP) · 3 Dec gravy-december (skit) · 4 Dec spot-diff-photo (NEW spotphoto.py + Pixabay, EXP) · 5 Dec december-money-race (race + guess). Queue now: 22 lost-sock, 23 turkey, 24 stomach (scheduled) · drafts 25 gravy-translator, 26 screen-time-race, 27 wallet, 28 vet-translator, 29 last-slice, 30 battery, 1 Dec translator-3am, 2–5 Dec batch 3 → covered to 5 Dec, next batch around 2 Dec.

## 2026-11-21 (Sat WIB, 05:35) — daily run: FIRST BREAKOUT (keys-cup-shuffle 3k + 9 comments); daily-limit error did not repeat
Buffer metrics refreshed 20 Nov 03:47 UTC (new since last run). we-need-to-talk (20 Nov 19:00) measured 1 min after posting = 0, judge next run.
| video | type | age at refresh | views | likes | like rate | comments | Δ views vs 19 Nov |
|---|---|---|---|---|---|---|---|
| salary-vs-bills | sim | ~124 h | 1,447 | 8 | 0.55% | 0 | flat |
| odd-mug-out | puzzle | ~112 h | 1,494 | 4 | 0.27% | 0 | flat |
| cat-translator | skit (translator) | ~100 h | 1,244 | 17 | 1.37% | 0 | flat |
| day-off-plinko | sim (plinko) | ~88 h | 1,836 | 5 | 0.27% | 0 | flat |
| cat-loaf-bakery | puzzle (find the cat) | ~76 h | 2,027 | 10 | 0.49% | 1 | +112 (+6%) — slowing |
| cat-work-call | skit (WFH) | ~64 h | 1,341 | 9 | 0.67% | 0 | flat |
| coffee-vs-monday | sim (duel) | ~52 h | 29 | 0 | – | 0 | dead |
| **keys-cup-shuffle** | puzzle (cup game) | ~40 h | **3,016** | **20** | 0.66% | **9** | **+1,754 (+139%)** |
| black-friday-budget | sim (plinko) | ~28 h | 1,318 | 2 | 0.15% | 0 | +134 |
| find-nugget-photo | puzzle (photo bg, find the cat) | ~3.8 h | 1,052 | 8 | 0.76% | 0 | new — fast seed, best early like rate of any puzzle |
- **First "tembus" (>3k): keys-cup-shuffle.** It is the only Short with a commit-before-reveal CTA ("Comment 1, 2 or 3 before the reveal") and it has 9 of the channel's 10 comments. Comments (not likes) look like the signal that buys the second/third push. Rule from now on: every puzzle AND sim ends with a commit-before-reveal choice (numbered options on screen, answer revealed after a pause), and the title asks for the guess.
- Make it a SERIES in batch 3: cup shuffle part 2 (new object + new twist, e.g. faster swaps / 4 cups / the cup itself is the trick), not a reupload.
- Plinko sims keep getting seed views but the lowest like rates (0.15–0.27%) and no comments: max 1 plinko per batch, and only with a "which bin?" guess before the drop.
- Photo-background test B (find-nugget-photo) seeded as fast as cartoon puzzles with a higher early like rate (0.76% at 4 h vs cat-loaf 0.54% at 5 h). Verdict at 48 h (next 1–2 runs).
- The daily posting limit error did NOT repeat: we-need-to-talk (20 Nov 19:00) and find-nugget-photo (20 Nov 07:00) both posted. Keep 2/day; the 19 Nov error was a one-off.
- Scheduled: vet-translator 21 Nov 19:00, lost-sock 22 Nov 07:00 (3 scheduled with social-battery 21 Nov 07:00). Drafts left 5 (turkey 23/07, screen-time 23/19, stomach 24/07, gravy-translator 24/19, translator-3am 27/19). Empty slots: 22 Nov 19:00, 25 Nov 07:00 – 27 Nov 07:00 → batch 3 at the next run (drafts will drop to 3). Batch 3 porsi: 2 commit-before-reveal puzzles (incl. cup shuffle part 2), 2 skits, 1 sim with a guess, 2 new formats.

## 2026-11-20 (Fri WIB, 05:35) — daily run: first Buffer ERROR (daily posting limit); coffee-vs-monday confirmed dead
Buffer metrics refreshed 19 Nov 03:44 UTC (new since last run).
| video | type | age at refresh | views | likes | like rate | comments | Δ views vs 18 Nov |
|---|---|---|---|---|---|---|---|
| salary-vs-bills | sim | ~100 h | 1,439 | 8 | 0.56% | 0 | flat |
| odd-mug-out | puzzle | ~88 h | 1,506 | 4 | 0.27% | 0 | +16 |
| cat-translator | skit (translator) | ~76 h | 1,245 | 17 | 1.37% | 0 | +10 |
| day-off-plinko | sim (plinko) | ~64 h | 1,832 | 5 | 0.27% | 0 | +41 (+2%) — second push over |
| cat-loaf-bakery | puzzle (find the cat) | ~52 h | 1,915 | 10 | 0.52% | 1 | +323 (+20%) — still growing, channel #1 |
| cat-work-call | skit (WFH) | ~40 h | 1,335 | 9 | 0.67% | 0 | +61 |
| coffee-vs-monday | sim (duel) | ~28 h | **15** | 0 | – | 0 | +11 → never got the seed test |
| keys-cup-shuffle | puzzle (cup game) | ~16 h | 1,262 | 9 | 0.71% | **4** | new — most comments ever |
| black-friday-budget | sim (plinko) | ~3.7 h | 1,184 | 2 | 0.17% | 0 | new (fast seed, low likes) |
- **Buffer error:** translator-3am-kitchen (19 Nov 19:00 WIB) failed with "The daily posting limit for this channel has been reached". Same 2/day pattern worked 15–18 Nov, so it is a YouTube/Buffer per-channel upload cap on a brand-new channel (likely rolling 24 h). Moved back to draft and re-dated **27 Nov 19:00** (not 22 Nov 19:00, to keep translator ≤1 per 6 slots: vet 21 Nov 19:00, gravy 24 Nov 19:00). If the 20 Nov 19:00 post also errors, drop to 1 video/day (07:00) until the channel is older and tell the user.
- coffee-vs-monday is the only Tiny Chaos Short that did not get the 1.1k seed (15 views at 28 h). Do NOT reupload. Before another sim_duel: compare its frame 0/title with the others (title "Coffee vs Monday"-style head-to-head may read as a generic ball sim).
- Comment bait works when the answer is a number the viewer commits to before the reveal: keys-cup-shuffle "Comment 1, 2 or 3 before the reveal" → 4 comments in 16 h (the channel had 1 comment total before). Use a commit-before-reveal CTA on every puzzle.
- cat-loaf-bakery keeps growing (+20%/day at 52 h) — closest to "tembus"; candidate for a SERIES ("part 2": hide a character among look-alike objects) in batch 3.
- Like rate ranking unchanged: translator skit (1.37%) > cup/character puzzles (0.5–0.7%) > sims (0.17–0.56%). Plinko gets views but almost no likes.
- Scheduled: we-need-to-talk 20 Nov 19:00, social-battery 21 Nov 07:00 (3 scheduled with find-nugget-photo 20 Nov 07:00). Drafts 7 → no batch. Empty slots: 22 Nov 19:00, 25 Nov 07:00 – 27 Nov 07:00 → batch 3 at the run when drafts < 4 (≈22 Nov).

## 2026-11-19 (Thu WIB, 05:35) — daily run: two videos got a second push; coffee-vs-monday may be stuck
Buffer metrics refreshed 18 Nov 03:52 UTC (new since last run). keys-cup-shuffle still 0 = updated 1 min after posting, judge next run.
| video | type | age at refresh | views | likes | like rate | comments | Δ views vs 17 Nov |
|---|---|---|---|---|---|---|---|
| salary-vs-bills | sim | ~76 h | 1,456 | 8 | 0.55% | 0 | +5 (flat) |
| odd-mug-out | puzzle | ~64 h | 1,490 | 4 | 0.27% | 0 | +23 |
| cat-translator | skit (translator) | ~52 h | 1,235 | 16 | 1.30% | 0 | +21 |
| day-off-plinko | sim (plinko) | ~40 h | 1,791 | 5 | 0.28% | 0 | **+398 (+29%)** |
| cat-loaf-bakery | puzzle (find the cat) | ~28 h | 1,592 | 10 | 0.63% | 1 | **+486 (+44%)** |
| cat-work-call | skit (WFH) | ~16 h | 1,274 | 9 | 0.71% | 0 | new |
| coffee-vs-monday | sim (duel) | ~3.8 h | **4** | 0 | – | 0 | new |
- First signs of a second push: day-off-plinko and cat-loaf-bakery kept growing past the 1.1–1.5k seed ceiling (both now channel top 2 by views). Not yet "tembus" (>3k) — check again at the next refresh whether growth continues >20%/24 h.
- Views ≠ likes: day-off-plinko has the most views but the lowest like rate (0.28%); cat-translator has the best like rate but stalled at 1.2k. Watch-through (not visible in Buffer) may be what drives the second push; plinko's 15.7 s of falling balls is a "watch to the end" format.
- Warning: coffee-vs-monday had only 4 views at ~3.8 h, while every other Tiny Chaos Short had 700–1,300 at a similar age. Could be just the snapshot time, but it is the AIVOOMA "0–4 views" pattern. If it is still <100 at the next refresh, compare its frame 0 / title with the others before more sim_duel videos.
- Pet + character puzzles (cat-loaf) beat object puzzles again (0.63% vs 0.27%): keep the rule "puzzles hide a character".
- Nothing scheduled (3 already: black-friday-budget 19 Nov 07:00, translator-3am-kitchen 19 Nov 19:00, find-nugget-photo 20 Nov 07:00). 8 drafts left → no batch. Free slots: 22 Nov 19:00 is still empty; batch 3 due when drafts < 4 (around 21 Nov).

## 2026-11-18 (Wed WIB, ~23:00) — Pixabay photo-background test launched (user request)
- engine/world.py `bg_photo` (scene='photo'): Pixabay photo cover-fit + slow Ken Burns + tint/dim + floor shadow. Photos only (video CDN 429; no SFX API; no Pixabay music = Content ID risk). Key only in the scheduled-task env, never in repo.
- Test A `translator-3am-kitchen` (19 Nov 19:00): strongest format (translator skit) on a real kitchen photo. Compare vs cat-translator 1,214 views / 1.32% likes and vet-translator (20 Nov 19:00, cartoon bg) in the same week.
- Test B `find-nugget-photo` (20 Nov 07:00): hide-the-cat in a real living-room photo. Compare vs cat-loaf-bakery (cartoon, 1,106 views, first comment) and lost-sock (22 Nov 07:00).
- Production notes: dim 0.4+ and no sunburst glow keep the photo readable; cat scale ~0.7 on a photo (it looks huge otherwise); hidden-object cat scale 0.13 on a windowsill is findable but not instant. Pick photos by tags, not query ("dark kitchen night" returned the Milky Way).
- Verdict rule: if a photo video beats its cartoon twin by >30% views or like rate at 48 h, raise photo share to 2-3 per batch; if worse, keep at most 1 per batch as variety.

## 2026-11-18 (Wed WIB, 05:35) — daily run: 5 Tiny Chaos results, all stuck at the seed test
Buffer metrics refreshed 17 Nov 05:13 UTC (new since last run). cat-work-call (aired 17 Nov 19:00) still 0 = stale, judge next run.
| video | type | age at refresh | views | likes | like rate | comments |
|---|---|---|---|---|---|---|
| salary-vs-bills | sim | ~53 h | 1,451 | 8 | 0.55% | 0 |
| odd-mug-out | puzzle | ~41 h | 1,467 | 4 | 0.27% | 0 |
| cat-translator | skit (translator) | ~29 h | 1,214 | 16 | 1.32% | 0 |
| day-off-plinko | sim | ~17 h | 1,393 | 5 | 0.36% | 0 |
| cat-loaf-bakery | puzzle (find the cat) | ~5 h | 1,106 | 6 | 0.54% | 1 (first ever) |
- Every Short lands at 1.1–1.5k and then flattens (salary +75 views in ~25 h). No breakout (>3k) yet: the ceiling is the second push, not the seed test.
- Like rate by type (≥24 h): translator skit 1.32% > sim 0.46–0.55% > puzzle 0.27%. Ranking unchanged, so batch-2 porsi (2 translator skits as series) stands.
- cat-loaf-bakery (puzzle with a cat + "not bread" joke) doubled the plain odd-mug puzzle like rate and got the channel's first comment: puzzles with a character/joke beat abstract object puzzles. Next puzzle should hide a character, not a shape.
- Scheduled keys-cup-shuffle 18 Nov 19:00 and black-friday-budget 19 Nov 07:00 (3 scheduled). Drafts left 8 (19 Nov 19:00 → 22 Nov 07:00 + date-locked 23/24 Nov) → no batch needed; next batch due when drafts < 4 (around the 20 Nov run).

## 2026-11-17 (Tue WIB) — daily run + Tiny Chaos batch 2 (19–22 Nov)
- Buffer metrics were NOT refreshed since 16 Nov 04:23 UTC (salary 1,376 / odd-mug 1,240 / cat-translator 730 + 12 likes; day-off-plinko 0, updated 1 min after posting). Nothing new to judge; re-check at the next run. If Buffer stays stale >24 h, note it and judge on the next refresh (no Apify on our own channel).
- Scheduled cat-work-call 17 Nov 19:00 and coffee-vs-monday 18 Nov 07:00 (3 scheduled). Drafts left: keys 18 Nov 19:00 + date-locked turkey 23 / stomach 24 = 3 < 4 → batch 2 built.
- Porsi from data so far (like rate: translator skit 1.64% > sim 0.51% > puzzle 0.24%): 2 translator skits as a SERIES (vet-translator, gravy-translator) + chat skit, 2 sims, 1 puzzle, 2 experiments.
- Research (Apify, BlobbyClips /shorts, 16 Nov): still 4.8–35M per Short. New winners use comparison templates: "FaceTime with Different People!" 10.6M, "Play With vs. Against Your Friend!" 7.3M, "Minecraft Mods Then vs Now!" 13.2M, "When You Lose Your Job!" 9.1M; 19–33 s. → Experiment 1: **chat_different_people** (new engine/chat.py, phone UI, 'we need to talk' sent to Mom / best friend / boss / group chat / bank). Experiment 2: **race_bars** (new engine/race.py, bar-chart race "my screen time on a work day", WORK: 14 minutes). Both are code-native and not ball sims.
- The @equmi handle in our notes now points to a Dead-by-Daylight clips channel (1–2k views): the cat channel 'equmi' must have another handle. Don't reuse that URL.
- Production: plinko `fake_target` needs `fake_until` ≈ 260 (switch target ~2.5 peg rows above the bins) or the last ball stays in the fake bin; slow-mo window = [a, a + (land − a)/k]. Hand from the top covers a sitting cat's face: put it ≥300 px to the side and slide the treat to the mouth. Seasonal maths: Thanksgiving 2026 = Thu 26 Nov.

## 2026-11-16 — first 3 Tiny Chaos results (Buffer, 04:23 UTC)
| video | type | age | views | likes | like rate |
|---|---|---|---|---|---|
| salary-vs-bills | sim | ~28 h | 1,376 | 7 | 0.51% |
| odd-mug-out | puzzle | ~16 h | 1,240 | 3 | 0.24% |
| cat-translator | skit (subtitle "translator") | ~4 h | 730 | 12 | 1.64% |
- All three got a normal seed test (~1.2–1.4k); none has broken out yet (salary flat: +108 in 24 h).
- cat-translator has 3x the like rate of the sim and 7x the puzzle while still early: emotional, relatable punchline + readable subtitles beats pure visuals. Next batch: 3 skits with the translator/subtitle device (as a series), 2 sims, 1 puzzle, 1 experiment. Puzzle stays at most 1 per batch until a puzzle beats 0.5%.
- n=3, different ages: re-check at 48 h before locking in.

## 2026-11-16 — user rule: own channel data only via Buffer
- Never scrape @tinychaosland with Apify; use Buffer list_posts includeMetrics. Apify is only for researching other channels and trends.

## 2026-11-16 (Mon WIB) — daily run: both first Tiny Chaos videos got the seed test
- Apify 15 Nov 22:35 UTC: salary-vs-bills 1,369 views / 7 likes at ~46 h (was 1,268 at 4 h, so it plateaued after the first push); odd-mug-out 1,186 views / 3 likes at ~10.5 h. 0 subscribers, 0 comments on both. Buffer metrics for odd-mug-out were stale (0, updated 3 min after posting): trust Apify for fresh numbers.
- Reading: the new channel is shown to people normally (old AIVOOMA got 0–4); the blocker was the channel. Next problem is the second push: ~1.2–1.4k is the seed-test ceiling, and 0 comments despite comment-bait questions. Judge stayed-to-watch % (needs Studio screenshot from user) before changing format mix.
- Scheduled cat-loaf-bakery 17 Nov 07:00 WIB. Queue: 16 Nov 07:00 cat-translator, 16 Nov 19:00 day-off-plinko, 17 Nov 07:00 cat-loaf-bakery; 5 drafts (17 Nov 19:00 → 18 Nov 19:00, plus date-locked 23/24 Nov). Gap 19–22 Nov: next batch must be made by the 18 Nov run at the latest (drafts drop below 4 at that run).

## 2026-11-15 — first Tiny Chaos video works; 2 posts per day
- salary-vs-bills (sim_relatable): 1,268 views + 8 likes about 4 h after posting (Buffer 04:46 UTC). Same seed-test size AIVOOMA got only twice in 16 tries, on the first upload: the new channel is being tested normally.
- User asked to start faster: now 2 slots per day, 07:00 and 19:00 WIB (19:00 WIB = morning in the US). Queue: 15 Nov 19:00 odd-mug-out, 16 Nov 07:00 cat-translator, 16 Nov 19:00 day-off-plinko, 17 Nov cat-loaf-bakery / cat-work-call, 18 Nov coffee-vs-monday / keys-cup-shuffle; turkey-protest 23 Nov and thanksgiving-stomach 24 Nov stay date-locked. Batch trigger is now drafts < 4.

## 2026-11-15 (Sun WIB) — Tiny Chaos batch 1 (18–24 Nov)
- Nothing had aired yet at run time (first Short, salary-vs-bills, goes out 15 Nov 07:00 WIB), so no channel data: this batch is built on the 13 Nov validation research. Judge the first 3 at the 17–18 Nov runs (views at 48 h; hundreds+ = channel was the blocker).
- Queue had 3 scheduled + 0 drafts, so the weekly batch ran. 7 drafts made for 18–24 Nov, rotating sim / puzzle / skit (3/2/2) and 5 pillars: adult life 2 (day-off plinko, coffee vs Monday), pets 1 (cat work call), brain 2 (cat-loaf puzzle, keys cup shuffle), seasonal 2 (turkey protest, stomach at Thanksgiving).
- Research (web, 15 Nov): marble runs / falling-ball sims still trend in late 2026 (Nerdbot Sep 2026), so plinko + duel + grow sims are the experiments; generic "will the ball escape" is saturated, so every sim carries a relatable label and a scripted punchline.
- Experiments this batch (5): sim_plinko, sim_duel, sim_grow, puzzle_shell (fair cup shuffle), skit_wfh (laptop video call). Compare their 48 h views vs. salary-vs-bills / odd-mug-out / cat-translator.
- Production lessons: plinko balls need damped steering (ax = k·(target−x) − d·vx), an undamped spring makes balls wander 5–6 s; forcing the last ball to swerve into a different bin looks fake, so the joke was rewritten to fit the physics ("THE PLAN gets 1 hour... at 11PM"). Duel: the HP-zero end time must be set once (a bug kept pushing it forward). build.py `shown()` starting at t=0 hides the actor at frame 0: use an explicit show list. On-screen text cannot use emoji (Luckiest Guy). Wide skit shots waste the bottom third: put the action on a table top and zoom 1.2–1.3.

## 2026-11-14 — Tiny Chaos launch (@tinychaosland, Buffer 6af7ee0462b70b94b027acfe)
- First 3 videos scheduled 07:00 WIB: 15 Nov salary-vs-bills (sim_relatable, new engine/sims.py ring_drain), 16 Nov odd-mug-out (puzzle_odd_one, new engine/puzzle.py), 17 Nov cat-translator (skit, made for AIVOOMA batch 3 but never aired).
- Judge after 48 h each on views + stayed-to-watch: hundreds+ views = old channel was the blocker; 0–4 = content/style problem.
- sims.py: preroll so frame 0 already has motion; costs scaled so the counter hits 0 exactly at drain_end; no emoji in on-screen text (Luckiest Guy has none); clamp labels inside 300..780 px.

## 2026-11-13 — validation research for Tiny Chaos (Apify)
- BlobbyClips (2.89M subs): varied everyday/gaming topics, 5–35M views per Short, 16–33 s, title template "X Be Like!" / "When X!" + doubled emoji. equmi (cat-only, Oct 2024): 58.5k subs, median ~330k per Short. Both prove the format; variety is fine if the promise and title pattern stay consistent.
- Biggest risk is animation quality, not topic: both winners have expressive acting and smooth motion; our code puppets are stiff. Plan: first 6 videos on the new channel = 3 upgraded engine + 3 Google Flow (Veo) clips, judged on stayed-to-watch at 48 h.
- Search queries with sortingOrder=views + dateFilter=month mostly return NO_VIDEOS; plain searchQueries can hang >5 min (aborted). Scraping known channels' /shorts pages is fast and reliable.

## 2026-11-13 — user: new channel must not be cat-only
- User wants varied videos, not only cats. New channel renamed from "Orange Cat Hours" to **Tiny Chaos** ("life's little chaos, animated"): one consistent promise (relatable everyday comedy for US 18–34), many topics and characters. 5 rotating pillars per week (pets, adult daily life, food/seasonal, brain/interactive, trend wildcard), max 2 per pillar, no same lead character two days running. Engine needs a human character and a dog before the first batch. Plan in NEW-CHANNEL.md.

## 2026-11-13 — Apify cross-check + user asks for a full overhaul ("0 terus, rombak ulang, apa kena children?")
- Apify (13 Nov 04:23 UTC) confirms Buffer: pet 1,370, lemon 1,215, 3am 14, cucumber 12, and every other Short 0–4 views, **including the first Creative v2 videos** (spot-diff "Only 2% find all 3 differences" 0 at ~28 h, whipped-cream 4). Comments on, not age-restricted, not made for kids (Studio: "set by you", channel = not for kids).
- Channel now shows 16 videos / 2,618 total views / 254 subs: the 23 old AI Shorts are gone (deleted), and pet+lemon are 99% of all channel views. Channel description is empty.
- Conclusion: format, character, layout and Creative v2 all failed the same way (12 Shorts in a row, shown to ~0–4 people, 100% swiped). The common factor is the channel, not the video: 254 subscribers who followed old surreal-AI content and never watch (Shorts tests start with them), deleted back catalogue, plus automated daily cartoon uploads. Made-for-kids is ruled out by Studio; "kid-appeal" cannot be measured from here.
- Options given to the user: (1) fresh channel + new visual style (recommended), (2) keep AIVOOMA but switch visuals to Google Flow/Veo 3D, (3) keep AIVOOMA and change niche. Pause AIVOOMA posting while deciding so more 100%-swipe Shorts don't lower trust further.

## 2026-11-12 (Thu WIB) — daily run
- Scheduled cat-translator for 14 Nov. Queue: spot-diff-kitchen 12, whipped-cream 13, cat-translator 14 Nov scheduled; 4 drafts (15–18 Nov). No errors. No batch (Thursday, 4 drafts).
- Buffer metrics (metricsUpdatedAt 11 Nov 21:23 UTC): **hide-gravy 0 at ~45 h** (interactive_protect, Gravy), **pick-one still 0 at ~45 h**, wake-up-tap 3, gravy-disguise 3, mirror-nugget 1. Now 10 Shorts in a row at 0–3 views. spot-diff-kitchen (first Creative v2) airs today 07:00 WIB: it is the key test; judge it at the 14 Nov run (~48 h).
- Apify had not reset yet at run time (05:37 WIB, cycle ends 07:00 WIB), so no scrape this run. Next run: scrape @aivooma/shorts first.
- Still waiting on the user: set "AI use: No" in Studio, and "stayed to watch" % for pet-nugget / sour-cat-lemon.

## 2026-11-11 — YouTube Studio screenshots from the user (first real Studio data)
- Audience is fine: video "Not made for kids (set by you)" and channel set to "No, not made for kids". Made-for-kids is ruled out as the cause.
- "AI use" question on the video is unanswered (neither Yes nor No), even though Buffer sends isAiGenerated=false. Our 2D cartoons are not realistic, so the honest answer is No; asked the user to set it. Effect on reach unknown.
- "How viewers engaged" on one of the recent 0–3 view Shorts: **0% stayed to watch, 100% swiped away**. With Shorts views counting every play, 0–3 views means YouTube showed it to only 1–3 people, and all of them swiped in the first second. The channel now gets a tiny test per video and fails it instantly. Main problem = frame 0 does not stop the scroll (and low channel trust shrinks each test).
- Need next: "stayed to watch" % for pet-nugget and sour-cat-lemon (the two that got ~1.2k) as the baseline to beat.

## 2026-11-11 — review with the user ("statistik jelek banget, mesti ngapain")
- Buffer (10 Nov 22:00 UTC): since 2 Nov, 9 Shorts in a row at 0–3 views (vacuum, box, tv, leaf, bowl, gravy, mirror, wake-up, pick-one). Only pet-nugget 1,370 and lemon 1,214 ever got a seed test. intinyaaje uses the same Buffer pipeline and gets ~1.2k per Short, so Buffer/API upload alone is not the cause.
- 0–3 views is not "bad content": a weak Short still gets shown to some people and swiped. Near-zero means it is barely shown at all. Most likely causes to check, in order: (1) YouTube set the videos/channel to "made for kids" (cartoon cat) despite madeForKids=false; (2) a restriction/limited state on the channel or videos; (3) low channel trust (23 old AI Shorts at 0 views + automated daily uploads). Only YouTube Studio shows which: Content → Audience + Restrictions columns, and per-video Analytics "Shown in feed" vs "Viewed vs swiped away".
- Batch 2 posts went out with notifySubscribers=false (batch 1 was true). Keep notifySubscribers=true.
- Next tests proposed to the user: one manual upload from the YouTube phone app with a trending Shorts sound (isolates upload method), and posting the same video on TikTok/Reels (isolates content vs YouTube channel).

## 2026-11-11 (Wed WIB) — daily run
- Scheduled whipped-cream for 13 Nov. Queue: hide-gravy 11, spot-diff-kitchen 12, whipped-cream 13 Nov scheduled; 5 drafts (14–18 Nov). No errors. No batch (Wednesday, 5 drafts).
- Buffer metrics (fresh, metricsUpdatedAt 10 Nov 22:00 UTC): **pick-one 0 at ~22 h** (guess_choice + comment prompt, first try: no seed test, 0 comments), wake-up-tap 3 at ~46 h, gravy-disguise 2, mirror-nugget 1, leaf-pile 1, half-full-bowl 0. Now 8 Shorts in a row at ≤3 views, across 4 formats and 2 characters, so format alone is not the cause. Creative v2 (spot-diff-kitchen, 12 Nov) is the next real test; Apify resets 12 Nov 07:00 WIB — next run should scrape @aivooma/shorts to confirm the zeros.

## 2026-11-10 (Tue WIB) — daily run
- Scheduled spot-diff-kitchen (first Creative v2 / puzzle_spot) for 12 Nov. Queue: pick-one 10, hide-gravy 11, spot-diff-kitchen 12 Nov scheduled; 6 drafts (13–18 Nov). No errors. No batch (Tuesday, 6 drafts).
- Buffer metrics (metricsUpdatedAt 8 Nov 23:22 UTC): gravy-disguise 2 (~2 d), mirror-nugget 1 (~1 d), leaf-pile 1, half-full-bowl 0; wake-up-tap 0 measured 3 min after posting (no verdict). Now 7 Shorts in a row at ≤3 views. Nothing new to learn until Creative v2 airs (12 Nov) and Apify resets (12 Nov 07:00 WIB): the next run after reset should scrape @aivooma/shorts to confirm the zeros are real.

## 2026-11-09 (Mon WIB) — daily run
- Scheduled hide-gravy for 11 Nov. Queue: wake-up-tap 9, pick-one 10, hide-gravy 11 Nov scheduled; 7 drafts (batch 3, 12–18 Nov). No errors. No batch (Monday, 7 drafts).
- Buffer metrics (metricsUpdatedAt 8 Nov 00:03 UTC): pet-nugget 1,371, sour-cat-lemon 1,214, 3am-zoomies 14, protect-cucumber 12, **gravy-disguise 3 at ~24 h** (first Gravy experiment, no seed test), leaf-pile 1, protect-vacuum / bed-vs-box / tv-fish / half-full-bowl 0. mirror-nugget 0 was measured ~4 min after posting, no verdict. 0 comments on everything. Six Shorts in a row at 3 views or fewer.
- A character change alone (Gravy) did not unlock distribution, on one sample. Real test is still the Creative v2 batch from 12 Nov; judge ~25 Nov.
- Setup note: /home/claude/ai-vooma can already exist on a detached HEAD; `git fetch && git checkout main && git reset --hard origin/main` before working.

## 2026-11-08 (Sun WIB) — daily run, Sunday batch skipped (batch 3 is <1 day old, 9 drafts)
- Scheduled pick-one (guess_choice experiment) for 10 Nov. Queue: mirror-nugget 8, wake-up-tap 9, pick-one 10 Nov scheduled; drafts hide-gravy 11 + batch 3 (12–18 Nov) = 8 drafts. No errors.
- Buffer metrics (metricsUpdatedAt 7 Nov 00:51 UTC, no refresh in ~22 h): unchanged — pet-nugget 1,371, sour-cat-lemon 1,211, 3am-zoomies 14, protect-cucumber 12, protect-vacuum / bed-vs-box / tv-fish / leaf-pile / half-full-bowl 0. gravy-disguise (first Gravy experiment) 0 but measured only ~48 min after posting, so no verdict yet.
- **Apify cycle confirmed**: Free plan cycle runs 12th→11th of each month (current cycle 12 Oct – 11 Nov 23:59 UTC, $5.12 used). Apify works again from **12 Nov 07:00 WIB** — the first run after that should scrape @aivooma/shorts to cross-check Buffer's zeros, then a trend search. Read `https://api.apify.com/v2/users/me/limits` (MCP resource) instead of guessing the reset.
- Windsor youtube still has only one account (66967, a brand-account address, previously identified as Intinya Aje) — not read. AIVOOMA retention data still needs the user to connect AIVOOMA in Windsor or send a Studio screenshot.

## 2026-11-07 (Sat WIB) — daily run + batch 3 (12–18 Nov), first full Creative v2 batch
- Daily: wake-up-tap scheduled for 9 Nov. Queue: gravy-disguise 7, mirror-nugget 8, wake-up-tap 9 Nov scheduled; drafts pick-one 10, hide-gravy 11 + 7 new (12–18 Nov). Drafts had dropped to 2, so batch 3 ran on Saturday.
- Data (Buffer, metricsUpdatedAt 6 Nov 03:21 UTC): pet-nugget 1,371, sour-cat-lemon 1,211, 3am-zoomies 14, protect-cucumber 12, and **5 Shorts in a row at 0 views** (protect-vacuum ~4 d, bed-vs-box ~3 d, tv-fish ~2 d, leaf-pile ~1 d, half-full-bowl ~3 h). Buffer has been right before (it showed the lemon spike within 5 h), so this is most likely real: YouTube stopped giving the template-look Shorts even a seed test. Apify still blocked (Free plan $5 cycle used) — cannot cross-check; a Studio screenshot or the AIVOOMA Windsor connection is still the missing piece.
- Research (web; Apify blocked): ViralMint W45 tracker — top breakouts are visual gags/fails/reactions, 38% of viral Shorts have no speech in the first 3 s, median 19 s. Anijam (vendor blog): song-timed animation memes where creators swap in their own character, POV skits. No Thanksgiving-specific trend found; US seasonal hook stays Thanksgiving (26 Nov). vidIQ: a Short that fails its seed audience freezes; re-uploading stuck Shorts can be flagged as spam (so never re-upload the 0-view ones).
- Batch 3 response: every video follows Creative v2 (action or task in frame 0, close-ups, cuts every 1–3 s, 9.5–12.5 s, loopable ending, comment prompt) and 7 different formats. 4 experiments: puzzle_spot (spot-diff-kitchen), translator (cat-translator), split_screen (expect-jump), Gravy #3 (gravy-yoga). New engine: split-screen panels, dining background, 7 props, 6 FX incl. owner's hand.
- Weakness to fix next batch: 3 of 7 still use top-centre cards as the main text layout (cookie-climb, tuna-teleport, gravy-yoga). Rule 17 says max 2.
- Judge on ~25 Nov: if the Creative v2 videos also get 0 while the old ones stay at 0, the problem is the channel (distribution/trust), not the template — then test posting time (US evening is 07:00 WIB already) and ask the user for Studio "shown in feed" numbers.
- No ElevenLabs credits used.

## 2026-11-06 (Fri WIB) — daily run
- Buffer metrics refreshed once (metricsUpdatedAt 5 Nov 04:01 UTC) but numbers barely moved: pet-nugget 1,371, sour-cat-lemon 1,211, 3am-zoomies 14, protect-cucumber 12, protect-vacuum / bed-vs-box / tv-fish 0; leaf-pile 0 at ~4 h (too early). Third straight daily run with no usable signal; 3 of the last 4 Shorts are at 0, which points to distribution, not Buffer lag. Batch 3 (Sun 8 Nov) must lean hard on Creative v2 and the experiments.
- Scheduled mirror-nugget for 8 Nov. Queue: half-full-bowl 6, gravy-disguise 7, mirror-nugget 8 Nov scheduled; 3 drafts (wake-up-tap 9, pick-one 10, hide-gravy 11 Nov). No batch (Friday, 3 drafts).

## 2026-11-05 (Thu WIB) — daily run
- Buffer metrics unchanged since the last snapshot (metricsUpdatedAt still 4 Nov 03:37 UTC): pet-nugget 1,370, sour-cat-lemon 1,211, 3am-zoomies 14, protect-cucumber 12, protect-vacuum / bed-vs-box / tv-fish 0. Buffer metrics did not refresh in ~25 h, so no new signal; retention data still needs Windsor (AIVOOMA account) or a Studio screenshot.
- Scheduled gravy-disguise (first Gravy experiment) for 7 Nov. Queue: leaf-pile 5, half-full-bowl 6, gravy-disguise 7 Nov scheduled; 4 drafts to 11 Nov (all pre-Creative-v2 template). No batch (Thursday, 4 drafts). Batch 3 is due Sun 8 Nov (batch 2 is 8 days old by then) and is the first one built under Creative v2 rules 15–20.

## 2026-11-04 — creative review with the user ("views 0 terus, terlalu monoton, kurang kreatif")
- Views so far (Buffer, 4 Nov 03:37 UTC): pet-nugget 1,370 / 9 likes, sour-cat-lemon 1,211 / 6, 3am-zoomies 14, protect-cucumber 12, protect-vacuum 0 (~50 h), bed-vs-box 0 (~27 h), tv-fish 0 (~3 h). 0 comments on all.
- Pattern: every Short gets either a small seed test (~1.2–1.4k, then stops) or almost nothing. None passed the seed test. Sources on the seed test (joyspace.ai, vidIQ) say the push depends on viewed-vs-swiped (≥70% viewed), average view % (>100% on short videos = replays), comments and shares.
- Visual audit of frames 0.3/1/2 s of all 7 videos: the same template every time (top title bar, small calm cat centered in a flat room, nothing happens for 1–2 s). The two pushed videos had a task or action in frame 0. This is the monotony the user sees. Batch 2 is slightly better (half-full-bowl opens mid-scream) but still the same layout.
- Response: Creative v2 rules 15–20 in README (frame 0 = peak, big subject, camera moves every 2–3 s, rotate text layouts, 7–12 s loops, comment/share reason, ≥1 totally different visual format per batch, no "Nugget" at the start of titles).
- Retention data missing: Windsor.ai youtube only has Intinya Aje connected; user asked to connect the AIVOOMA brand account.

## 2026-11-04 (Wed WIB) — daily run
- Buffer metrics (metricsUpdatedAt 3 Nov 04:32 UTC): pet-nugget 1,369 (flat vs yesterday's snapshot), sour-cat-lemon 1,210, **protect-vacuum 0 views after ~28 h**, bed-vs-box 0 at ~4.5 h (too early), 3am-zoomies 14, protect-cucumber 12. Still 0 comments.
- Warning sign: both interactive_protect videos (cucumber, vacuum) got ~0 distribution, while the two single-gag videos broke out. If vacuum is still ~0 at the next snapshot, cut interactive_protect share in batch 3 (hide-gravy on 11 Nov is the last protect-style one queued). Possible causes: longer premise/text hook (15.5 s, threat must be read), or Buffer metrics lag. YouTube Studio screenshot would settle it.
- Both breakouts have also stopped growing in the Buffer snapshot (possible metric lag). Watch tv-fish (4 Nov) and leaf-pile (5 Nov).
- Scheduled half-full-bowl for 6 Nov. Queue: tv-fish 4, leaf-pile 5, half-full-bowl 6 Nov scheduled; 5 drafts to 11 Nov. No batch (Wednesday, 5 drafts).

## 2026-11-03 (Tue WIB) — daily run
- Buffer metrics (metricsUpdatedAt 2 Nov 06:58 UTC): pet-nugget 1,369 views / 9 likes (+305 in ~26 h), sour-cat-lemon 1,208 / 6 (+7 only: the lemon spike was a one-day push that stalled), protect-vacuum 0 at ~7 h (too early), 3am-zoomies 14, protect-cucumber 12. Still 0 comments on every video.
- Pattern update: pet-nugget (interactive_play, finger-on-screen) keeps growing while lemon stopped, so interactive_play has the better tail so far. Watch protect-vacuum (interactive_protect) and wake-up-tap/leaf-pile (interactive) before shifting share.
- Scheduled leaf-pile for 5 Nov. Queue: bed-vs-box 3 Nov, tv-fish 4 Nov, leaf-pile 5 Nov scheduled; 6 drafts to 11 Nov. No batch (Tuesday, 6 drafts).

## 2026-11-02 (Mon WIB) — daily run: first breakout
- Buffer metrics (metricsUpdatedAt 1 Nov 05:24 UTC): sour-cat-lemon (reaction, 10 s) **1,201 views / 6 likes** only ~5 h after posting; pet-nugget (interactive_play, 14 s) **1,064 views / 9 likes** after ~29 h; protect-cucumber 12 and 3am-zoomies 13 views (0 likes). The channel is now being distributed: the last two Shorts got ~100x the first two.
- Early pattern (n=4, weak): the two winners are the shortest/simplest single-gag videos with an immediate visual hook (cat + lemon, finger + cat). The two losers needed a premise to be read first (cucumber threat, 3AM text). Partly also timing: YouTube may have needed a few uploads before testing the channel. Do not over-weight yet; re-check after tv-fish, protect-vacuum, bed-vs-box.
- Like rate ~0.5–0.9%, 0 comments: the comment-bait guess_choice experiment (pick-one, 10 Nov) is the test for comments.
- Implication for batch 3: favour ≤12 s single-gag reaction/interactive_play ideas, keep the hook visible in frame 0 without needing to read text.
- Scheduled tv-fish for 4 Nov. Queue: 3 scheduled (2–4 Nov), 7 drafts to 11 Nov. No batch today (Monday WIB, batch 2 is 2 days old).

## 2026-11-01 (Sun) — daily run, weekly batch skipped
- Buffer metrics (metricsUpdatedAt 31 Oct 06:21 UTC): protect-cucumber 0 views after ~2.3 days, 3am-zoomies 4, pet-nugget 1; 0 likes/comments. Old pre-relaunch Shorts also 0–3. Too few views to compare formats; 0 views on a 2-day-old Short may mean YouTube is not distributing it at all (or Buffer metrics are stale). Need a YouTube Studio screenshot (views, "shown in feed", swipe-away rate) from the user before any format decision.
- Apify still blocked ("Monthly usage hard limit exceeded") on 1 Nov 05:40 WIB; the reset is not on the 1st of the calendar month.
- Batch 2 was built Sat 31 Oct (<24 h earlier), the queue runs to 11 Nov and none of its experiments (Gravy, guess_choice) has aired, so the Sunday batch was skipped: a batch now would be planned with zero new data and push the queue to 18 Nov. Rule added to ROUTINE.md: Sunday batch only if the last batch is ≥4 days old (the draft < 3 trigger always applies).
- Buffer `edit_post` re-validates the whole post: send text, assets (video url), and full youtube metadata (title, categoryId...) together with mode/dueAt, or it fails with "YouTube posts require a video/title/category". Added to ROUTINE.md.

## 2026-10-31 — batch 2 (Nov 5–11), first experiments
- Data: Buffer still shows 0 views for protect-cucumber and 3am-zoomies (metricsUpdatedAt 30 Oct 07:19, ~31 h and ~7 h after posting). Too early and possibly stale; no format decision possible yet. Apify monthly limit still hit (31 Oct), so no YouTube scrape. Next run: if Buffer still says 0 after 3+ days, ask the user for a YouTube Studio screenshot.
- Trend research (web, Apify down): sources are thin marketing blogs. Usable signals: silent physical comedy travels across languages; strongest visual in the first 2–3 s; "POV:" titles and Halloween transformation/reveal edits peaked in October; November = Thanksgiving (Thu 26 Nov 2026) is the next US seasonal hook.
- Experiments this batch (3 of 7): (1) NEW CHARACTER Gravy the anxious turkey, a seasonal Thanksgiving arc (gravy-disguise, hide-gravy); (2) NEW FORMAT guess_choice "Which one will Nugget pick? Comment 1, 2 or 3" with a 3-2-1 countdown, built to pull comments (pick-one). Judge them against the channel median after ≥7 days.
- Engine: +2 backgrounds (backyard, bathroom), +11 props, +2 FX, hoedown mood, gobble/rustle synth SFX, mirror clipping, build.py so episodes are short Python scripts. Production went faster with build.py (one file per video, ~60 lines).
- Production lessons: hand from the top needs origin y ≈ target − 250; anything at y < 340 hides under the title; a "dive into the pile" needs a front copy of the pile drawn after the cat and lowered so his feet don't show; a quiz needs items ≥1.5 scale and badges offset so they don't cover the items.
- No ElevenLabs credits used this batch (all new sounds synthesized).

## 2026-10-29 — first upload day
- protect-cucumber went live 07:01 WIB. Buffer metrics were fetched only 3 min after posting (metricsUpdatedAt) so they showed 0; do not trust Buffer views until metricsUpdatedAt is >24 h after sentAt.
- Apify hit its monthly usage hard limit on 29 Oct; YouTube pages/RSS are blocked to WebFetch and the shell. Fallback added to ROUTINE.md.

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
