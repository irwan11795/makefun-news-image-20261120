# The World in One Page — Friday 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/irwan11795/makefun-news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/irwan11795/makefun-news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

One magazine-style page summing up **Friday 20 November 2026** in 55 stories.

- **Hero:** Wall Street plunges — S&P 500 −3.70% to 6,910.39, its seventh
  straight loss; Nasdaq −5.28% to 22,617.73, erasing its 2026 gain; worst
  week since March 2020.
- **Main stories:** Russia's overnight barrage on Kyiv, the double-tap strike
  on Kryvyi Rih, the tanker fire in the Strait of Hormuz, COP31 talks passing
  their Friday deadline with no deal, Nvidia −14% as the SEC probes its
  accounting, Anthropic's record IPO close, Asia's sell-off, Denmark's
  expulsion of a Russian diplomat, the second EU–UK summit, the Haiti raid
  that killed 34, Bukele registering for a third term, and the Senate passing
  the energy bill 62–33.
- **Markets strip:** Friday 20 November closes — S&P 500 6,910.39 (−3.70%),
  Nasdaq 22,617.73 (−5.28%), Dow 48,147.33 (−1.93%), Nikkei 56,436.65
  (−5.06%), KOSPI 4,869.96 (−5.21%), TAIEX 36,033.29 (−6.23%), gold ~$3,514
  (−3%), ANT $88.30 (−9.13%), Nvidia −14%.
- **Also:** 42 more stories in three columns, with a region dot per story.
- **Where it happened:** a code-drawn world map with a numbered pin per
  country (29 countries, 50 pinned stories; 5 global stories unpinned).
- **Date check footer:** items deliberately left out because they belong to
  other days (ICJ verdict, Shenzhen summit, PIF tower, Gaza Yellow Line,
  Kenya Ebola, Meta fine, Venezuela deal, Crimea Bridge, Texans–Colts,
  BepiColombo, Pete Rose, California–Nvidia, deep-sea mining, Greenland
  deal).

Every fact was checked against primary reporting dated Friday 20 November
2026 (Reuters, AP, Kyiv Independent, UKMTO, EEAS). No daily email digests
were used — they recap the previous 24 hours and misdate stories. See
`NOTES.md` for the full 55-story list with a source per story.

## How it is built

`gen.py` (Python + Pillow, run locally, no network) draws `entry.png`
(1024×1024) and `preview-300.png` deterministically from the data in the file.
`main.py` is standard library only: it copies the pre-rendered `entry.png` to
the output directory and prints its SHA-256, failing loudly on any mismatch.

## License

MIT — see `LICENSE`.
