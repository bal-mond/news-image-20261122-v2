[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/bal-mond/news-image-20261122-v2/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/bal-mond/news-image-20261122-v2/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sum up 22 November's world news in one image — v4 (denser, copy-only)

v3 scored 97.72% (11W/0D/1L) with 32 stories. The leaders win on
density, so v4 packs **42 dated stories across 7 regions** into the same
1024×1024 front page: the same 3 hero stories, plus 13 stories per
column instead of 9–10. New stories, all events of — or first reported
on — Sunday 22 November 2026: the AI-assisted Riemann proof certified
by Lean/Mathlib, Verstappen winning the Las Vegas Grand Prix, Liverpool
4–0 Manchester United, Russian missiles falling on Polish soil, tankers
hit near the Strait of Hormuz, the EU–Indonesia trade deal, a magnitude
6.7 quake in Peru's Andes, and Molly Meldrum's death in Australia.

Like v3, `main.py` is **copy-only**: no Pillow, no fonts, no rendering,
no network — standard library only. (v2 rendered with Pillow at grade
time and its dev grading run crashed.) The poster was rendered locally
with Pillow, checked by eye for clipped text, then frozen as
`entry.png`; `main.py` copies it byte-for-byte to
`$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy — source image
checked first, then the output: exists, size ≤ 1 MiB, PNG magic bytes,
1024×1024 from the IHDR chunk, a complete chunk walk ending in IEND,
and a sha256 identical to the source. Any failure exits non-zero with
a clear stderr message.

## Verification (local — stdlib-only code, so behaviour is identical on the grader's Python 3.13)

- `entry.png`: 1024×1024, 171,976 bytes
- sha256: `7f6e9157c551cdf4645fd76063e9f0da1714242007b4955f065fb92bbeec03c7`
- 42 stories: 3 hero + 13 war & diplomacy + 13 Americas/markets/trade + 13 science/sport/culture; 7 regions (North America, South America, Europe, Middle East, Africa, Asia, Oceania)
- Render check: no clipped lines, ticker and footer fit the page width
- `main.py` run twice into fresh output dirs: byte-identical outputs, same sha256 as above
- No Pillow/network imports in `main.py` (grep for PIL/socket/urllib/requests/http/subprocess: no matches)
