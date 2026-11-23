[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/bal-mond/news-image-20261122-v2/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/bal-mond/news-image-20261122-v2/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday 22 November 2026

A newspaper front page that sums up Sunday 22 November 2026's world news
in a single 1024×1024 image: **32 dated stories** across war & diplomacy,
Americas & markets, and science, sport & culture, plus a news ticker.

The three lead stories: COP31 collapses in Antalya with no deal; Iran
strikes US bases in Bahrain as tankers burn near Hormuz; Mexico captures
cartel boss "El Chapo Isidro". Every story happened, or was first reported,
on 22 November 2026, and is sourced from Reuters, AP, AFP, Al Jazeera, BBC,
ESA, Dawn, CBS or the Washington Post (sources are named on the poster).

## How it works

`main.py` (Python 3.13, standard library + Pillow only, no network) draws
the poster deterministically and writes it to `$MAKEFUN_OUTPUT_DIR`
(default `/output`, falling back to `./out`). Running it twice produces
byte-identical output.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Verification

- `entry.png`: 1024×1024 PNG, 175,279 bytes (≤ 1 MiB), Pillow
  `verify()` + `load()` pass; sha256
  `1abe20f84bf5c76c3d8c01991d445c515da0b3bc204e84a0b5cabea24a6bdf6b`.
- Two runs into fresh directories produce byte-identical files
  (same sha256).
- No network access in `main.py` (no socket / urllib / requests / http /
  subprocess).

## Licence

MIT — see `LICENSE`.
