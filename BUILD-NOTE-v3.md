# news-image-20261120 v3 — build note (21 Nov 2026)

## Entry
- `entry.png` 1024×1024, **260,330 bytes**,
  sha256 `6b96202a53b7977db527e38a76562ec07349ede0c58a45f872949067e4e90662`
- Deterministic: same sha256 across repeated runs.
- `main.py` EXPECTED_SHA256 updated to the v3 hash; `python3 main.py`
  copies it to /output/entry.png with matching hash.
- Kit check: **4 passed, 1 failed** (transcripts_present — expected
  pre-bundle), 14 skipped, 5 checked at submission. Same as v2.
- Backups of v2: gen-v2.py, entry-v2.png, NOTES-v2.md in this dir.

## What changed vs v2 (Hermes v2: 88/100 FIX FIRST — all 6 fixes applied)
1. **† markers + footnote** for 4 borderline-date items (#11 Haiti,
   #12 Bukele, #13 Senate in the river; #47 Kenya in ALSO). Footnote:
   "† Thu 19 Nov event, reported Fri 20 Nov — included per 'happened
   or first reported' rule. ‡ #27 single-source (Ukrainian military)."
2. **‡ kept on #27 HIMARS** (single-source, Ukrainian military).
3. **#29 labelled forecast:** "Hunger Games: $100m forecast".
4. **Three misdated stories REPLACED** (see below).
5. **Smallest text 14px → 16px** (ALSO list, 17px leading); every ALSO
   line re-shortened and asserted to fit one line. Layout rebalanced:
   map 112→96, MARKETS 38→34, hero 142→138, header gaps 24→22 (×3),
   river row padding +8→+4, BY THE NUMBERS rows 21→20, kicker gap
   20→18. Footer rule at y=1000 (assert ≤1008). All asserts pass.
6. **Map legend strengthened:** "Red dot = stories per country, number
   inside dot · USA 15 · India 4 · Ukraine 3 · Japan 2 · Saudi Arabia 2
   · 24 more countries × 1 each · 5 global stories not pinned".

## Stories replaced (all verified to 20 Nov primary sources)
| # | v2 (removed — why) | v3 replacement — verification |
|---|---|---|
| 37 | Zambia awake brain surgery — article dated **16 Nov** (Zambian Observer) | Zambia bishops: keep term limit — ZCCB pastoral statement signed Lusaka **20 Nov**, leads Daily Nation; Hichilema responded same day (Zambian Observer / Daily Zambian, 20 Nov) |
| 51 | Abu Dhabi Binance freeze — ADGM order granted **18–19 Nov** (CoinDesk 2026-11-19T15:20:38Z; Reuters Nov 18) | Dubai deploys 90 AI apps — Dubai deploys 90+ AI apps across govt bodies (EIN News UAE newswire, published **Nov 20, 2026**) |
| 52 | Sinaloa cartel bombing — event **Tue 17 Nov**, reported 19 Nov (Breitbart URL 2026/11/19) | Mexico captures El Chapo Isidro — military captured Fausto Isidro Meza Flores in Guasave, Sinaloa, **Fri Nov 20** (CNN 2026-11-21 reporting the Friday operation; Particle; Sinaloa state govt) |

Replacements kept the same country/region, so counts (55 stories,
50 pinned / 29 countries + 5 global; regions 19/10/7/7/8/1/3) and all
map pins are unchanged. Verified anchors untouched (Wall St rout,
Nikkei, KOSPI, Anthropic IPO, ANT close).

## Also checked and rejected
- Somalia–UAE expulsion as a replacement: expulsion order was Thu
  19 Nov (Al Jazeera); only the Mogadishu rallies were Fri 20 Nov.
  Not used.
- #47 Kenya mosquito-net drive: launch was Thu 19 Nov (WHO AFRO),
  reported 20 Nov by some outlets — KEPT with †.

## Hermes v3 verdict
**NONE — both providers down.** Runcrate DeepSeek HTTP 529 (all 3
attempts, ~16:10 WIB); OpenRouter nemotron HTTP 429 daily free-model
limit, resets 00:00 UTC = 07:00 WIB 22 Nov (the deadline). No verdict
will be available before the deadline. See
hermes-judgment-v3-20261121.md for the coordinator's own
evidence-based assessment (labelled as such, NOT a Hermes score):
v3 is clearly stronger than v2 and worth submitting; estimated
~90–93/100 on Hermes's scale (below the standing ≥95 bar — the user
waived that bar for two submissions today, so the decision is theirs).

## Visual verification
- Full-res read: no overflow, no clipped text; hero, river, MARKETS,
  ALSO, footnote, map, legend, DATE CHECK, footer all render cleanly.
- ALSO section cropped at full res: 16px text crisp and legible.
- Map crop: pins + numbers readable at 96px height.
- preview-300.png regenerated from the v3 entry.

## Next steps (parent)
- Create the GitHub repo via browser (init-rooted), push, set About
  (homepage https://make.fun/c/news-image-20261120 + topic makefun).
- Kit check → submit ONLY on user approval. Deadline 07:00 WIB 22 Nov.
- Do NOT submit; do NOT claim anything.
