# HANDOFF — news-image-20261122

## Competition

- **Slug:** news-image-20261122
- **Title:** "Sum up 22 November's world news in one image"
- **Prize:** $100 — 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20
- **Deadline:** 2026-11-24 08:00 CST (2026-11-24T00:00:00Z)
- **Results:** 2026-12-08 08:00 UTC
- **Judge:** z-ai/glm-5.3-flash, pairwise image comparison, no ties
- **Limits:** at most 10 submissions/day, 20 total; last submission is final
- **Rules (competition.yaml + RULES.txt):** program at repo root, main.py
  (Python 3.13) or main.ts (Node 22); writes one image to
  /output/entry.png; PNG or JPEG, at most 1 MiB, at most 1024×1024 px;
  no network; program runs twice and both runs must write the same bytes.
  News = events that happened, or were first reported, on 22 November
  2026 in any time zone.
- **Kit:** kit/ (kit.tar.gz 7,799,485 bytes, unpacked to kit/;
  nested kit/news-image-20261122-kit/ is the tarball's own inner folder).
  requirements.json fetched from the API (x-api-key).

## What the image contains (36 stories, 7 regions)

Front page "THE WORLD IN ONE DAY — SUNDAY, 22 NOVEMBER 2026",
1024×1024, hand-drawn flat vector with PIL, no photos, no wire images.

- **6 big numbers:** 24 dead (Nigeria boat), 39 missing (Jakarta fire),
  10% (Trump card-rate cap), $48bn (Iran war cost to US), 11 dead
  (Sinaloa), 35% (COP31 electrification target by 2035).
- **3 big illustrated headlines:** COP31 in double overtime (globe +
  clock at 11:55 + "DOUBLE OVERTIME" banner); Jakarta candy-factory
  fire (3 dead, 39 missing); Trump vows a 10% cap on card rates
  (tilted credit card).
- **10 small illustrated stories:** Hormuz reopening, Nvidia US probe,
  Sinaloa 11 dead, Pentagon curbs Canada defence ties, Seoul education
  chief quits in AI scandal, sanctioned Russian ship ablaze in Baltic,
  Nigeria boat 24 dead, Paris sixth weekend of protests, Belgium air
  shutdown, lab mosquitoes beat dengue.
- **Map "WHERE IT HAPPENED"** with 12 numbered red pins + **23 numbered
  briefs** (14–36): Brazil storm, Haiti farmers, Mexico caravan,
  Seattle airport arrests, Trump gags contractors, FDA roles, Senate
  Democrats vote, China telecom ban, Taiwan warns Carney, Lee on AI
  race, Meta India protests, West Bengal Christians, Rome ex-police
  chief, Geneva killer-robots accord, UN youth insecurity, Kim factory
  visits, Rohingya verdict, Gulf F-16 claim, Bahrain warning, Saudi
  GTA stake, FBI hack probe, Bulgari dies at 89, "Black Saturn" 5D
  black-hole model.
- **Region bar:** Europe 8, North America 11, Asia 10, Middle East 4,
  Africa 1, South America 1, Space 1 (total 36).
- **DATE CHECK box** (left out — not 22 Nov): BepiColombo reaches
  Mercury (Sat 21 Nov); missiles over Riyadh / coalition hits Hodeidah
  (Fri–Sat 20–21 Nov); Peru M6.7 quake (Fri 20 Nov; Sunday toll update
  1 dead, 16 hurt).
- **Footer:** "HOW THIS PAGE WAS MADE — Drawn by hand with code: no
  photos, no wire images. Every story was first reported on 22 November
  2026." + sources line (AFP, AP, Reuters, Al Jazeera, The Hindu, Dawn,
  Economic Times, Manila Times, Channel News Asia, ESA, Nature).

All 36 stories were verified against live sources on 22 Nov 2026; see
NEWS.md for the story list with outlets and dates. Two judgement calls
worth knowing: the Peru quake (20 Nov) is in DATE CHECK, not a story;
the Nigeria boat and Jakarta fire figures use the latest 22 Nov wires
(24 dead; 3 dead / 39 missing).

## File layout (~/workspace/makefun/news-image-20261122/)

- `main.py` — the entrypoint. Self-contained: full generator + entry
  code, written by hand in this session (write, then one edit adding
  the whole-image decode check). Reads $MAKEFUN_OUTPUT_DIR (default
  /output), writes entry.png, asserts PNG magic, ≤1 MiB, ≤1024 px,
  re-opens and decodes the file, prints size + sha256.
- `entry.png` — reference render produced by main.py (see verification).
- `tools/gen_image.py` — the dev generator (same drawing code, OUT_PATH
  env). Kept for iteration; main.py is the submitted program.
- `NEWS.md` — all 36 stories with sources, numbers, DATE CHECK items,
  region counts.
- `HANDOFF.md` — this file.
- `prompt.txt` — the user's exact quote, one line, no trailing newline.
- `kit/` — unpacked kit (kit.tar.gz kept alongside).
- `requirements.json` — competition requirements from the API.

## Verification (all done in this session)

- `python3 tools/gen_image.py` → entry.png 1024×1024, 183,715 bytes.
  Viewed the image twice: first pass found invisible text (PIL's
  default text fill is white on paper) and a "10%/CAP" overlap on the
  card; fixed fills to INK, re-laid the card interior, moved three map
  labels clear of pins; second view confirmed all text legible, no
  overlaps, map labels visible.
- **Two-run determinism (main.py):** ran twice with different
  MAKEFUN_OUTPUT_DIR values (out-run1, out-run2), then deleted the
  scratch dirs. Both runs:
  - size 1024×1024, PNG, 183,715 bytes
  - sha256 `f74817975bf00af5175698db1c249f7155a6f42e595a63e22f0ac32397cf0825`
  - identical to each other AND to the tools/gen_image.py reference
    render. Byte-identical confirmed.
- **Requirements check:** 1024×1024 ≤ 1024×1024 ✓; 183,715 ≤ 1,048,576 ✓;
  PNG magic `\x89PNG\r\n\x1a\n` ✓; whole-image decode (PIL load) ✓;
  36 stories, 7 regions, date Sunday 22 November 2026 ✓.

## Still to do (parent — NOT done here)

- Do NOT submit yet (per task). When ready: create the GitHub repo
  (must be created after the competition opened, 2026-11-22T00:00:00Z),
  push main.py + entry.png + NEWS.md + HANDOFF.md + prompt.txt +
  LICENSE (MIT with SPDX line) + README, add .makefun/owner.json,
  set About, write usage, bundle with this session as --session,
  check, submit before 2026-11-24 08:00 CST. Quota: check
  /api/competitions/news-image-20261122/quota before submitting.
- Note: main.py uses PIL (Pillow). The 11-21 edition also used PIL and
  its reproduces check passed (96.5%), so Pillow is available in the
  grader's Python environment.
- prompt.txt must stay exactly one line with no trailing newline.
