# gen.py — draws entry.png for news-image-20261120 (Friday 20 November 2026).
# PIL only, no network, fully deterministic. Run: python3 gen.py
# Writes entry.png (1024x1024, RGB) next to this file and preview-300.png.
#
# Layout v2 — adopts the news-image-20261119 v5 magazine layout
# (scored 95.23% live): slim kicker + big sans masthead, region-counts
# line, a two-row BY THE NUMBERS band, ONE hero story (story 1, big
# drawn diagram left — a falling Wall Street chart — headline right),
# a 12-story "story river" in 2 columns where EVERY cell carries a
# small original code-drawn illustration on the left (32x32, theme per
# story), a MARKETS strip, the 42-item ALSO list in 3 columns, a
# "WHERE IT HAPPENED" world map (code-drawn, red pins numbered with
# the story count per country), a small grey DATE CHECK footer note,
# footer. 55 stories total.
#
# All pictures are original drawings made with PIL for this entry: no
# external images, no photos, no copyrighted artwork. No sentence or
# picture was copied from any competitor entry.
#
# v2 content vs v1 (every story re-audited against PRIMARY sources
# dated Friday 20 November 2026 — no email digests; see NOTES.md):
#   HERO is now the Friday Wall Street rout (S&P -3.70% to 6,910.39,
#   Nasdaq -5.28% to 22,617.73, Dow -1.93%, 7th straight loss).
#   RIVER swaps the 5 misdated items (Shenzhen summit, PIF tower,
#   Gaza Yellow Line, COP31 draft, Kenya Ebola) for Friday stories:
#   COP31 overtime (no deal), Nvidia -14% (SEC accounting probe),
#   plus Kryvyi Rih split from Kyiv, Haiti, Bukele, Senate bill.
#   ALSO drops 29 misdated items and both duplicates (ANT slide,
#   EU-COP31 warning) and refills from Friday wires.
#   Nikkei corrected to 56,436.65 / -5.06%; TAIEX to 36,033.29 / -6.23%.
#   Region balance: AMERICAS 19, EUROPE 10, ASIA 7, MIDDLE EAST 7,
#   AFRICA 8, OCEANIA 1, WORLD 3. Map: 50 pinned in 29 countries,
#   5 global unpinned.

import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 90, 90)
LIGHT = (242, 242, 242)
RULE = (17, 17, 17)

_HERE = Path(__file__).resolve().parent


def _font(name, size):
    """Load a bundled font (fonts/ next to this file) or the system copy."""
    for base in (_HERE / "fonts",
                 Path("/usr/share/fonts/truetype/dejavu")):
        p = base / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise SystemExit(f"font not found: {name}")


KICK = _font("DejaVuSans-Bold.ttf", 12)
TITLE = _font("DejaVuSans-Bold.ttf", 26)
REGION_LINE = _font("DejaVuSans-Bold.ttf", 12)
STAT_NUM = _font("DejaVuSans-Bold.ttf", 17)
STAT_LBL = _font("DejaVuSans.ttf", 10)
TICK_HEAD = _font("DejaVuSans-Bold.ttf", 11)
HERO_KICK = _font("DejaVuSans-Bold.ttf", 13)
HERO_HEAD = _font("DejaVuSans-Bold.ttf", 28)
HERO_SUMM = _font("DejaVuSans.ttf", 12)
SECT = _font("DejaVuSans-Bold.ttf", 16)
FLOW_NUM = _font("DejaVuSans-Bold.ttf", 8)
FLOW_KICK = _font("DejaVuSans-Bold.ttf", 11)
FLOW_HEAD = _font("DejaVuSans-Bold.ttf", 13)
FLOW_SUMM = _font("DejaVuSans.ttf", 12)
MKT_LABEL = _font("DejaVuSans-Bold.ttf", 12)
MKT_TXT = _font("DejaVuSans.ttf", 12)
DATE_HEAD = _font("DejaVuSans-Bold.ttf", 11)
DATE_TXT = _font("DejaVuSans.ttf", 11)
ALSO_NUM = _font("DejaVuSans-Bold.ttf", 13)
ALSO_TXT = _font("DejaVuSans.ttf", 16)
FOOT = _font("DejaVuSans.ttf", 11)
CAP = _font("DejaVuSans.ttf", 10)
MAP_LEGEND = _font("DejaVuSans.ttf", 10)
NOTE_FONT = _font("DejaVuSans.ttf", 10)

# (number, region, tag, headline, summary) — all stories happened or were
# first reported on Friday 20 November 2026; wording is the author's own.
# River summaries are ONE line each (measured <= 442px at 12px).
# The hero headline carries a manual line break (\n) so it never wraps
# with a one-word orphan.
LEADS = [
    (1, "AMERICAS", "AMERICAS · MARKETS",
     "Wall Street plunges:\nS&P −3.7%, Nasdaq −5.3%",
     "S&P 500 falls 3.70% to 6,910.39, its seventh straight loss. "
     "Nasdaq −5.28% to 22,617.73, erasing its 2026 gain. "
     "Worst week since March 2020."),
    (2, "EUROPE", "EUROPE · UKRAINE",
     "Barrage kills at least 7 in Kyiv",
     "Overnight missiles hit the capital; debris falls in Poland."),
    (3, "EUROPE", "EUROPE · UKRAINE",
     "Kryvyi Rih: child, medic killed",
     "Ballistic strike hits a restaurant lot; 42 hurt, 27 seriously."),
]

GRID = [
    (4, "MIDDLE EAST", "MIDDLE EAST · HORMUZ",
     "Tanker fire in the Strait of Hormuz",
     "Tanker struck by a projectile off Oman; Iran blames a mine."),
    (5, "EUROPE", "EUROPE · CLIMATE",
     "COP31 talks pass deadline, no deal",
     "Draft stripped of fossil-fuel text; third draft due Saturday."),
    (6, "AMERICAS", "AMERICAS · NVIDIA",
     "Nvidia −14% as SEC probes books",
     "SEC probes Nvidia accounting; shares fall 14% to $125.53."),
    (7, "AMERICAS", "AMERICAS · IPO",
     "Anthropic IPO: $93.5bn, shares −9%",
     "Greenshoe fully exercised; ANT closes at $88.30 on Friday."),
    (8, "ASIA", "ASIA · MARKETS",
     "Nikkei −5.1%, KOSPI −5.2%, TAIEX −6.2%",
     "Asia follows Wall St down; SoftBank closes −14.5% in Tokyo."),
    (9, "EUROPE", "EUROPE · DENMARK",
     "Denmark expels Russian attache",
     "Two charged over plot to kill a rapper; envoy has 7 days."),
    (10, "EUROPE", "EUROPE · SUMMIT",
     "EU-UK hold second summit in Brussels",
     "Youth mobility, food and emissions deals; +0.5% GDP boost."),
    (11, "AMERICAS", "AMERICAS · HAITI",
     "Haiti raid kills 34 gang suspects †",
     "First major push in five years; 34 killed in Martissant."),
    (12, "AMERICAS", "AMERICAS · EL SALVADOR",
     "Bukele registers for third term †",
     "Registers on Thursday night; party posts the filing on Friday."),
    (13, "AMERICAS", "AMERICAS · SENATE",
     "Senate passes energy bill 62–33 †",
     "Speeds energy and datacentre permits; now goes to the House."),
]

# ALSO list: one short line each (number + text), kept short enough to
# fit a single 16px line in a 3-column cell (asserted below).
# v3: font raised 14px -> 16px (Hermes fix 5), so every line is shortened
# to fit; #37/#51/#52 replaced (v2 items misdated — see NOTES.md);
# #29 labelled as a forecast (fix 3); † = borderline date (fix 1),
# ‡ = weak sourcing (fix 2).
ALSO = [
    (14, "MIDDLE EAST", "Iraq deploys in Kataib base"),
    (15, "EUROPE", "U17: Spain thrash China 5–0"),
    (16, "ASIA", "Bengaluru 2–0 Mumbai, top ISL"),
    (17, "ASIA", "India A beat Nepal by 306 runs"),
    (18, "AMERICAS", "Trump: tax datacentres abroad"),
    (19, "AMERICAS", "Mamdani: close Rikers by 2032"),
    (20, "WORLD", "UN straw poll #9 for chief"),
    (21, "ASIA", "Japan CPI 2.2%, rate odds fall"),
    (22, "AMERICAS", "Bayer Roundup deal approved"),
    (23, "AMERICAS", "Palisades arsonist guilty"),
    (24, "EUROPE", "UK food inflation to peak 5%"),
    (25, "AMERICAS", "F1: Russell tops Vegas practice"),
    (26, "AMERICAS", "4.2 quake rattles Los Angeles"),
    (27, "EUROPE", "HIMARS kills 20+ in Sumy ‡"),
    (28, "OCEANIA", "5.6 quake off New Caledonia"),
    (29, "AMERICAS", "Hunger Games: $100m forecast"),
    (30, "ASIA", "India court backs bike taxis"),
    (31, "WORLD", "Cargo Dragon undocks from ISS"),
    (32, "AMERICAS", "Florida floods hit record levels"),
    (33, "AMERICAS", "6.7 Peru quake felt in Lima"),
    (34, "EUROPE", "TB drug AlpE matches standard"),
    (35, "ASIA", "India H5N1 poultry vaccine"),
    (36, "AFRICA", "China-Africa centre in Addis"),
    (37, "AFRICA", "Zambia bishops: keep term limit"),
    (38, "EUROPE", "Troyes beat Le Havre 3–1"),
    (39, "AMERICAS", "Cincinnati beat Orlando 3–1"),
    (40, "MIDDLE EAST", "Al Ahli beat Al Nassr 3–1"),
    (41, "ASIA", "U17: Tajikistan beat Cuba 5–3"),
    (42, "AMERICAS", "Moog posts record $4.5bn sales"),
    (43, "AFRICA", "Egypt IMF deal unlocks $2.3bn"),
    (44, "AFRICA", "Zimbabwe tightens lithium rules"),
    (45, "AFRICA", "Ex-SA deputy Mlambo dies"),
    (46, "AFRICA", "Guinea bans Burkina broadcaster"),
    (47, "AFRICA", "Kenya mosquito-net drive †"),
    (48, "MIDDLE EAST", "Gulf allies push to avert war"),
    (49, "MIDDLE EAST", "Third US carrier group in Gulf"),
    (50, "MIDDLE EAST", "Saudi downs Houthi missile"),
    (51, "MIDDLE EAST", "Dubai deploys 90 AI apps"),
    (52, "AMERICAS", "Mexico captures El Chapo Isidro"),
    (53, "AMERICAS", "RSF: 30 journalists attacked"),
    (54, "WORLD", "Brent above $92 on Gulf fears"),
    (55, "AFRICA", "Tems drops Blood soundtrack"),
]

STATS = [
    ("−3.70%", "S&P 500, 7th straight loss"),
    ("−5.28%", "Nasdaq, negative for 2026"),
    ("−14.0%", "Nvidia shares"),
    ("$7.25bn", "Bayer Roundup settlement"),
    ("34", "killed in Haiti raid"),
    ("62–33", "Senate energy bill vote"),
]

# Stories first reported before Friday 20 November, deliberately left
# out. Shown as a small grey footer note.
DATE_CHECK = (
    "ICJ verdict · Shenzhen summit · PIF tower · Gaza Yellow Line · "
    "Kenya Ebola · Meta fine · Venezuela deal · Crimea Bridge · "
    "Texans–Colts · BepiColombo · Pete Rose · California–Nvidia · "
    "deep-sea mining · Greenland deal."
)

REGION_COLORS = {
    "WORLD": (190, 24, 93),
    "MIDDLE EAST": (185, 28, 28),
    "ASIA": (180, 83, 9),
    "EUROPE": (30, 64, 175),
    "AFRICA": (5, 122, 85),
    "AMERICAS": (107, 33, 168),
    "OCEANIA": (13, 148, 136),
}


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def wrap(draw, text, font, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading if leading else font.size + 4
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def draw_diagram_markets(d, x, y, w, h):
    """Wall Street rout: dark trading-floor backdrop, a red falling
    chart line, the S&P drop in big white type."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 27, 62))
    for gy in range(y + 24, y + h - 24, 24):
        d.line([x + 10, gy, x + w - 10, gy], fill=(30, 50, 90), width=1)
    pts = [(x + 16, y + 20), (x + 110, y + 34), (x + 200, y + 28),
           (x + 290, y + 58), (x + 370, y + 74), (x + 460, y + 100)]
    d.line(pts, fill=(255, 60, 60), width=4)
    d.polygon([(x + 460, y + 100), (x + 444, y + 92), (x + 452, y + 110)],
              fill=(255, 60, 60))
    f_big = _font("DejaVuSans-Bold.ttf", 32)
    d.text((x + 18, y + 48), "−3.70%", font=f_big, fill=(255, 255, 255))
    d.text((x + 18, y + 84), "S&P 500  ·  6,910.39",
           font=_font("DejaVuSans-Bold.ttf", 13), fill=(255, 200, 200))
    d.text((x + 18, y + 102), "Nasdaq −5.28%  ·  Dow −1.93%",
           font=_font("DejaVuSans.ttf", 12), fill=(200, 210, 230))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 8, y + h - 15), "WALL STREET · SEVENTH STRAIGHT LOSS",
           font=CAP, fill=(255, 255, 255))


# ---- original code-drawn illustrations for stories 2–13 ----
# Each thumbnail is a 32x32 flat drawing on its own background colour.
# No external images, no photos, no copied artwork.

THUMB = 32
THUMB_BG = (200, 200, 200)


def _thumb_bg(d, x, y, color):
    d.rectangle([x, y, x + THUMB, y + THUMB], fill=color, outline=THUMB_BG)


def thumb_burst(d, x, y):
    """#2 Kyiv — explosion starburst on a dark sky."""
    _thumb_bg(d, x, y, (20, 25, 45))
    cx, cy = x + 16, y + 16
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 200, 60))
    for ang in range(0, 360, 45):
        ex = cx + 13 * math.cos(math.radians(ang))
        ey = cy + 13 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=(255, 140, 40), width=2)


def thumb_strike(d, x, y):
    """#3 Kryvyi Rih — building with a burst above it."""
    _thumb_bg(d, x, y, (30, 30, 40))
    d.rectangle([x + 8, y + 16, x + 24, y + 29], fill=(120, 130, 150))
    for wy in range(y + 19, y + 28, 4):
        d.rectangle([x + 10, wy, x + 12, wy + 2], fill=(255, 220, 120))
        d.rectangle([x + 20, wy, x + 22, wy + 2], fill=(255, 220, 120))
    cx, cy = x + 16, y + 9
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 160, 0))
    for ang in range(0, 360, 60):
        ex = cx + 8 * math.cos(math.radians(ang))
        ey = cy + 8 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=(255, 120, 0), width=1)


def thumb_ship(d, x, y):
    """#4 Hormuz — tanker on the sea with a flame."""
    _thumb_bg(d, x, y, (18, 55, 90))
    d.rectangle([x, y + 22, x + 32, y + 32], fill=(30, 90, 150))
    d.polygon([(x + 6, y + 18), (x + 26, y + 18), (x + 23, y + 24),
               (x + 9, y + 24)], fill=(200, 60, 40))
    d.rectangle([x + 12, y + 10, x + 20, y + 18], fill=(220, 220, 220))
    d.polygon([(x + 14, y + 10), (x + 18, y + 3), (x + 20, y + 10)],
              fill=(255, 180, 40))


def thumb_globe(d, x, y):
    """#5 COP31 — globe with land + a leaf."""
    _thumb_bg(d, x, y, (218, 238, 228))
    d.ellipse([x + 5, y + 4, x + 27, y + 26], fill=(40, 120, 200))
    d.ellipse([x + 9, y + 8, x + 15, y + 13], fill=(60, 180, 90))
    d.ellipse([x + 17, y + 16, x + 24, y + 22], fill=(60, 180, 90))
    d.polygon([(x + 22, y + 1), (x + 29, y + 1), (x + 26, y + 8)],
              fill=(30, 140, 70))


def thumb_chip(d, x, y):
    """#6 Nvidia — a chip with pins."""
    _thumb_bg(d, x, y, (15, 30, 15))
    d.rectangle([x + 9, y + 9, x + 23, y + 23], outline=(74, 222, 128),
                width=2)
    d.rectangle([x + 14, y + 14, x + 18, y + 18], fill=(74, 222, 128))
    for i in range(3):
        px = x + 12 + i * 5
        d.line([px, y + 4, px, y + 9], fill=(74, 222, 128), width=2)
        d.line([px, y + 23, px, y + 28], fill=(74, 222, 128), width=2)


def thumb_bars(d, x, y):
    """#7 Anthropic IPO — rising bars + green up-trend arrow."""
    _thumb_bg(d, x, y, (13, 22, 48))
    for i, (bh, col) in enumerate([(8, (120, 140, 180)),
                                   (14, (60, 120, 220)),
                                   (20, (34, 197, 94))]):
        bx = x + 10 + i * 7
        d.rectangle([bx, y + 27 - bh, bx + 5, y + 27], fill=col)
    d.line([x + 9, y + 25, x + 27, y + 7], fill=(74, 222, 128), width=2)
    d.polygon([(x + 28, y + 5), (x + 22, y + 5), (x + 28, y + 11)],
              fill=(74, 222, 128))


def thumb_down(d, x, y):
    """#8 Asia markets — red falling line chart with a down arrow."""
    _thumb_bg(d, x, y, (255, 255, 255))
    d.line([x + 3, y + 27, x + 3, y + 5], fill=(180, 180, 180), width=1)
    d.line([x + 3, y + 27, x + 28, y + 27], fill=(180, 180, 180), width=1)
    d.line([x + 5, y + 8, x + 12, y + 13, x + 19, y + 12, x + 27, y + 22],
           fill=(185, 28, 28), width=2)
    d.polygon([(x + 27, y + 22), (x + 21, y + 21), (x + 27, y + 16)],
              fill=(185, 28, 28))


def thumb_shield(d, x, y):
    """#9 Denmark — shield with a check."""
    _thumb_bg(d, x, y, (228, 238, 248))
    c = (30, 64, 175)
    d.polygon([(x + 16, y + 4), (x + 26, y + 8), (x + 26, y + 18),
               (x + 16, y + 28), (x + 6, y + 18), (x + 6, y + 8)],
              outline=c, width=2)
    d.line([x + 11, y + 16, x + 14, y + 20, x + 21, y + 11], fill=c, width=2)


def thumb_hands(d, x, y):
    """#10 Brussels — two flags side by side (EU + UK)."""
    _thumb_bg(d, x, y, (240, 240, 240))
    d.rectangle([x + 3, y + 8, x + 14, y + 20], fill=(0, 51, 153))
    for i in range(6):
        ang = i * 60
        sx = x + 8 + 3 * math.cos(math.radians(ang))
        sy = y + 14 + 3 * math.sin(math.radians(ang))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 220, 0))
    d.rectangle([x + 18, y + 8, x + 29, y + 20], fill=(255, 255, 255),
                outline=(180, 180, 180))
    d.line([x + 18, y + 14, x + 29, y + 14], fill=(200, 16, 46), width=2)
    d.line([x + 23, y + 8, x + 23, y + 20], fill=(200, 16, 46), width=2)


def thumb_raid(d, x, y):
    """#11 Haiti — shield with a star (raid / security operation)."""
    _thumb_bg(d, x, y, (245, 235, 220))
    c = (150, 40, 40)
    d.polygon([(x + 16, y + 4), (x + 26, y + 8), (x + 26, y + 18),
               (x + 16, y + 28), (x + 6, y + 18), (x + 6, y + 8)],
              outline=c, width=2)
    cx, cy = x + 16, y + 16
    for ang in range(-90, 270, 72):
        ex = cx + 6 * math.cos(math.radians(ang))
        ey = cy + 6 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=c, width=1)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=c)


def thumb_flag(d, x, y):
    """#12 Bukele — a flag on a pole (ballot / registration)."""
    _thumb_bg(d, x, y, (235, 240, 250))
    d.line([x + 8, y + 4, x + 8, y + 29], fill=(60, 60, 60), width=2)
    d.polygon([(x + 8, y + 5), (x + 26, y + 9), (x + 8, y + 15)],
              fill=(0, 71, 171))
    d.polygon([(x + 8, y + 15), (x + 26, y + 19), (x + 8, y + 25)],
              fill=(255, 255, 255))
    d.ellipse([x + 6, y + 3, x + 10, y + 7], fill=(255, 220, 0))


def thumb_dome(d, x, y):
    """#13 Senate — Capitol dome."""
    _thumb_bg(d, x, y, (235, 240, 245))
    c = (90, 110, 140)
    d.pieslice([x + 10, y + 2, x + 22, y + 12], 180, 360, fill=c)
    d.rectangle([x + 8, y + 11, x + 24, y + 13], fill=c)
    for cx in (x + 10, x + 15, x + 20):
        d.rectangle([cx, y + 14, cx + 2, y + 20], fill=c)
    d.rectangle([x + 7, y + 20, x + 25, y + 22], fill=c)


THUMBS = {2: thumb_burst, 3: thumb_strike, 4: thumb_ship, 5: thumb_globe,
          6: thumb_chip, 7: thumb_bars, 8: thumb_down, 9: thumb_shield,
          10: thumb_hands, 11: thumb_raid, 12: thumb_flag, 13: thumb_dome}


# ---- "WHERE IT HAPPENED" world map ----
# Simplified continent outlines (lon, lat), equirectangular projection:
# x = (lon+180)/360 * w, y = (75-lat)/130 * h (lat 75 at top, -55 at
# bottom; Antarctica is off the map). Shapes are deliberately coarse —
# a locator map, not an atlas.
MAP_H = 96
MAP_SEA = (214, 227, 241)
MAP_LAND = (198, 182, 142)
MAP_LINE = (172, 154, 118)

CONTINENTS = [
    [(-168, 66), (-155, 71), (-135, 70), (-120, 72), (-100, 73), (-85, 70),
     (-75, 72), (-65, 62), (-55, 52), (-60, 47), (-70, 44), (-75, 38),
     (-81, 32), (-84, 30), (-90, 21), (-95, 16), (-97, 16), (-105, 20),
     (-110, 24), (-117, 33), (-124, 42), (-125, 49), (-135, 58),
     (-150, 60), (-162, 58), (-168, 66)],
    [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-25, 76), (-40, 80),
     (-55, 78), (-60, 74), (-58, 64)],
    [(-80, 9), (-77, 4), (-75, 0), (-70, -3), (-60, 0), (-52, 3),
     (-50, 0), (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -27),
     (-55, -34), (-60, -38), (-66, -45), (-68, -52), (-71, -54),
     (-73, -48), (-73, -37), (-71, -30), (-70, -20), (-75, -15),
     (-80, -6), (-81, 0), (-80, 9)],
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (20, 32), (30, 31), (34, 28), (37, 22), (43, 12), (48, 11), (51, 10),
     (46, 0), (41, -5), (40, -12), (36, -18), (33, -26), (28, -33),
     (20, -35), (16, -29), (14, -22), (12, -15), (13, -8), (12, -2),
     (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (7, 54), (10, 57), (12, 55),
     (18, 56), (23, 58), (28, 60), (30, 62), (25, 68), (18, 70), (12, 68),
     (5, 60), (0, 54), (-5, 49), (-9, 43), (-10, 36)],
    [(30, 62), (35, 66), (45, 68), (60, 70), (75, 73), (90, 75), (105, 76),
     (120, 73), (135, 72), (150, 70), (160, 66), (170, 66), (178, 64),
     (170, 60), (162, 58), (158, 52), (150, 48), (142, 45), (140, 40),
     (135, 35), (130, 33), (127, 35), (124, 30), (121, 25), (115, 22),
     (110, 20), (108, 15), (105, 9), (103, 7), (100, 8), (97, 10),
     (94, 16), (91, 22), (88, 22), (85, 20), (80, 15), (77, 8), (74, 12),
     (70, 20), (66, 25), (61, 25), (57, 26), (53, 27), (50, 29), (48, 30),
     (44, 29), (40, 31), (36, 36), (33, 36), (30, 36), (28, 40), (30, 46),
     (30, 55), (30, 62)],
    [(113, -22), (114, -28), (115, -32), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (144, -38), (147, -39), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -14), (142, -11), (137, -12),
     (135, -12), (132, -12), (130, -13), (126, -14), (123, -17),
     (119, -20), (114, -21), (113, -22)],
]

# Small islands as (lon, lat, rx_deg, ry_deg) ellipses.
ISLANDS = [
    (102, 0, 6, 3), (113, -2, 5, 3), (120, -8, 4, 2), (131, -3, 5, 3),
    (140, -4, 6, 3), (139, 38, 3, 6), (122, 13, 2.5, 4), (141, -4, 7, 3),
    (172, -41, 3, 5), (-2, 54, 2.5, 4), (47, -19, 2, 5), (81, 7, 1.5, 2),
    (165, -21, 3, 2),
]

# Story count per country, counted from the 55 stories (see NOTES.md for
# the per-story assignment). (lon, lat, count, dx, dy) — dx/dy are manual
# nudges in px so the crowded Europe / Middle East pins do not overlap
# and no pin leaves the map frame. 50 stories pinned in 29 countries;
# 5 are global and not pinned (UN chief race, Cargo Dragon, Gulf
# diplomacy, RSF report, Brent oil). 15+4+3+2+2+24x1 = 50; 50+5 = 55.
PINS = [
    (-98, 39, 15, 0, 0),      # USA
    (79, 21, 4, 0, 0),        # India
    (32, 49, 3, -1, -4),      # Ukraine
    (138, 37, 2, 0, 0),       # Japan
    (45, 25, 2, -3, 7),       # Saudi Arabia
    (53, 32, 1, 0, 0),        # Iran
    (35, 39, 1, 0, 2),        # Turkey
    (10, 56, 1, 2, -5),       # Denmark
    (4.5, 50.5, 1, -6, 5),    # Belgium
    (-73, 19, 1, 2, -3),      # Haiti
    (-89, 13.7, 1, 0, 0),     # El Salvador
    (-4, 40, 1, -4, 5),       # Spain
    (-2, 54, 1, -2, -2),      # UK
    (44, 33, 1, -2, -6),      # Iraq
    (165, -21, 1, 0, 0),      # New Caledonia
    (-75, -10, 1, 0, 0),      # Peru
    (8, 47, 1, 1, 6),         # Switzerland
    (38, 9, 1, 0, -4),        # Ethiopia
    (28, -14, 1, -8, 0),      # Zambia
    (2, 47, 1, -3, -6),       # France
    (71, 39, 1, 0, 0),        # Tajikistan
    (31, 27, 1, -2, 2),       # Egypt
    (30, -19, 1, 8, 0),       # Zimbabwe
    (25, -29, 1, 0, 0),       # South Africa
    (-13, 10, 1, 0, 0),       # Guinea
    (38, 0, 1, 0, 4),         # Kenya
    (54, 24, 1, 3, 3),        # UAE
    (-102, 23, 1, 0, 0),      # Mexico
    (8, 9, 1, 0, 0),          # Nigeria
]

MAP_LEGEND_TXT = ("Red dot = stories per country, number inside dot · USA 15 · India 4 · "
                  "Ukraine 3 · Japan 2 · Saudi Arabia 2 · 24 more "
                  "countries × 1 each · 5 global stories not pinned")

# Footnote for the † (borderline date) and ‡ (sourcing) markers used in
# the river and ALSO list. One line at 10px; asserted to fit the page.
FOOTNOTE_TXT = ("† Thu 19 Nov event, reported Fri 20 Nov — included per "
                "'happened or first reported' rule. ‡ #27 single-source "
                "(Ukrainian military).")


def draw_map(d, x, y, w, h):
    """Draw the world map with per-country story-count pins."""
    d.rectangle([x, y, x + w, y + h], fill=MAP_SEA)

    def P(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (75 - lat) / 130 * h)

    for poly in CONTINENTS:
        pts = [P(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND, outline=MAP_LINE)
    for lon, lat, rx, ry in ISLANDS:
        cx, cy = P(lon, lat)
        sx = rx / 360 * w
        sy = ry / 130 * h
        d.ellipse([cx - sx, cy - sy, cx + sx, cy + sy], fill=MAP_LAND,
                  outline=MAP_LINE)
    pin_font = _font("DejaVuSans-Bold.ttf", 7)
    for lon, lat, count, dx, dy in PINS:
        px, py = P(lon, lat)
        px += dx
        py += dy
        r = 9 if count >= 10 else 6
        assert x + r <= px <= x + w - r, f"pin x out of map: {px}"
        assert y + r <= py <= y + h - r, f"pin y out of map: {py}"
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        s = str(count)
        tw = d.textlength(s, font=pin_font)
        d.text((px - tw / 2, py - 5), s, font=pin_font, fill=(255, 255, 255))


def region_counts():
    counts = {}
    for _, region, *_ in LEADS + GRID + ALSO:
        counts[region] = counts.get(region, 0) + 1
    order = ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS",
             "OCEANIA", "WORLD"]
    return [(r, counts.get(r, 0)) for r in order]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = 18, W - 18
    y = 10

    # Kicker line
    d.text((x0, y), "THE WORLD'S NEWS IN ONE PICTURE", font=KICK, fill=RED)
    right = "55 STORIES · 7 REGIONS · ALL FROM FRIDAY"
    d.text((x1 - d.textlength(right, font=KICK), y), right,
           font=KICK, fill=INK)
    y += 18

    # Masthead — 26px bold sans
    d.text((x0, y), "Friday 20 November 2026", font=TITLE, fill=INK)
    y += 32

    # Region-counts line: coloured segments, e.g. "EUROPE 10 · ASIA 7 ..."
    # This line doubles as the legend for the ALSO region dots.
    rx = x0
    counts = region_counts()
    for i, (region, n) in enumerate(counts):
        seg = f"{region} {n}"
        d.text((rx, y), seg, font=REGION_LINE,
               fill=REGION_COLORS[region])
        rx += d.textlength(seg, font=REGION_LINE)
        if i < len(counts) - 1:
            d.text((rx, y), "  ·  ", font=REGION_LINE, fill=GREY)
            rx += d.textlength("  ·  ", font=REGION_LINE)
    assert rx <= x1, "region line too wide"
    y += 18

    # BY THE NUMBERS band — two rows of three stats; big red numbers,
    # small grey labels.
    head = "BY THE NUMBERS  "
    d.text((x0, y), head, font=TICK_HEAD, fill=RED)
    hx = x0 + d.textlength(head, font=TICK_HEAD)
    row_gap = 24
    for row in range(2):
        stats = STATS[row * 3:(row + 1) * 3]
        sx = hx if row == 0 else x0
        for num, lbl in stats:
            nw = d.textlength(num, font=STAT_NUM)
            lw = d.textlength(lbl, font=STAT_LBL)
            assert sx + nw + 6 + lw <= x1, f"stat row {row} too wide"
            d.text((sx, y), num, font=STAT_NUM, fill=RED)
            d.text((sx + nw + 6, y + 5), lbl, font=STAT_LBL, fill=GREY)
            sx += nw + 6 + lw + row_gap
        y += 20
    y += 2
    d.line([x0, y, x1, y], fill=RULE, width=3)
    y += 8

    # ---- HERO: story 1 — big diagram left, headline right ----
    hero_h = 138
    hero_y = y
    img_w = 500
    draw_diagram_markets(d, x0, hero_y, img_w, hero_h)
    tx = x0 + img_w + 16
    tw = x1 - tx
    num, region, tag, head, summ = LEADS[0]
    d.rectangle([tx, hero_y + 2, tx + 34, hero_y + 6], fill=RED)
    ty = hero_y + 12
    d.text((tx, ty), f"{num}  {tag}", font=HERO_KICK,
           fill=REGION_COLORS[region])
    ty += 20
    # Manual line break (in the data): never wrap with a one-word orphan.
    head_lines = []
    for part in head.split("\n"):
        part_lines = wrap(d, part, HERO_HEAD, tw)
        assert len(part_lines) == 1, \
            f"hero headline part wraps: {part!r} -> {part_lines}"
        head_lines.append(part_lines[0])
    assert len(head_lines) <= 3, f"hero headline wraps to {len(head_lines)}"
    for ln in head_lines:
        d.text((tx, ty), ln, font=HERO_HEAD, fill=INK)
        ty += 32
    ty += 2
    summ_lines = wrap(d, summ, HERO_SUMM, tw)
    assert len(summ_lines) <= 3, f"hero summary wraps to {len(summ_lines)}"
    for ln in summ_lines:
        d.text((tx, ty), ln, font=HERO_SUMM, fill=GREY)
        ty += 14
    assert ty <= hero_y + hero_h, "hero text overflows hero block"
    y = hero_y + hero_h + 8

    # ---- Section header: the story river ----
    d.text((x0, y), "THE REST OF THE DAY", font=SECT, fill=RED)
    d.line([x0 + d.textlength("THE REST OF THE DAY", font=SECT) + 10, y + 8,
            x1, y + 8], fill=(200, 200, 200), width=1)
    y += 22

    # ---- Story river: stories 2–13 in 2 columns x 6 rows ----
    # Each cell carries an original illustration drawn at 32x32
    # and pasted at 28x28 at the left (story number as a small red
    # badge on the illustration corner); text starts 40px in.
    # Summaries are ONE line each (measured).
    river = LEADS[1:] + GRID
    assert len(river) == 12
    col_w = (x1 - x0 - 24) / 2
    gutter = 40
    text_w = col_w - gutter
    thumb_disp = 28
    rows = []
    for r in range(6):
        pair = river[r * 2:(r + 1) * 2]
        heights = []
        for (num, region, tag, head, summ) in pair:
            line1_w = (d.textlength(tag, font=FLOW_KICK)
                       + d.textlength(" — ", font=FLOW_HEAD)
                       + d.textlength(head, font=FLOW_HEAD))
            assert line1_w <= text_w, \
                f"story {num} kicker+headline too wide: {line1_w:.0f} > {text_w:.0f}"
            sl = wrap(d, summ, FLOW_SUMM, text_w)
            assert len(sl) == 1, \
                f"story {num} summary wraps to {len(sl)} (v2: must be 1)"
            heights.append(16 + len(sl) * 15 + 4)
        rows.append(max(max(heights), thumb_disp + 4))
    for r in range(6):
        pair = river[r * 2:(r + 1) * 2]
        for c, (num, region, tag, head, summ) in enumerate(pair):
            cx = x0 + c * (col_w + 24)
            cy = y
            thumb_img = Image.new("RGB", (THUMB, THUMB), PAPER)
            td = ImageDraw.Draw(thumb_img)
            THUMBS[num](td, 0, 0)
            thumb_img = thumb_img.resize((thumb_disp, thumb_disp),
                                         Image.LANCZOS)
            img.paste(thumb_img, (int(cx), int(cy)))
            # Story number as a small red badge on the thumbnail corner.
            badge = f"{num:02d}"
            bw = d.textlength(badge, font=FLOW_NUM)
            d.rectangle([cx - 1, cy + thumb_disp - 9,
                         cx + bw + 5, cy + thumb_disp + 1], fill=RED)
            d.text((cx + 2, cy + thumb_disp - 9), badge, font=FLOW_NUM,
                   fill=(255, 255, 255))
            tx2 = cx + gutter
            d.text((tx2, cy + 2), tag, font=FLOW_KICK,
                   fill=REGION_COLORS[region])
            hx = tx2 + d.textlength(tag, font=FLOW_KICK)
            d.text((hx, cy + 2), " — ", font=FLOW_HEAD, fill=GREY)
            hx += d.textlength(" — ", font=FLOW_HEAD)
            d.text((hx, cy + 2), head, font=FLOW_HEAD, fill=INK)
            sy = cy + 20
            for ln in wrap(d, summ, FLOW_SUMM, text_w):
                d.text((tx2, sy), ln, font=FLOW_SUMM, fill=GREY)
                sy += 15
        if c == 0:
            d.line([x0 + col_w + 12, y, x0 + col_w + 12, y + rows[r]],
                   fill=(220, 220, 220), width=1)
        y += rows[r]
    y += 6

    # ---- MARKETS strip: grey band, label + two lines ----
    mkt_h = 34
    d.rectangle([x0, y, x1, y + mkt_h], fill=LIGHT)
    mkt1 = ("S&P 500 −3.70% to 6,910.39 · Nasdaq −5.28% to 22,617.73 · "
            "Dow −1.93% to 48,147.33 — seventh straight loss.")
    mkt2 = ("Nikkei −5.06% to 56,436.65 · KOSPI −5.21% · TAIEX −6.23% · "
            "Gold ~$3,514 −3% · ANT $88.30 −9.13% · Nvidia −14%.")
    label = "MARKETS AT THE CLOSE — "
    assert (d.textlength(label, font=MKT_LABEL)
            + d.textlength(mkt1, font=MKT_TXT) <= x1 - x0 - 16), "mkt1 too wide"
    assert d.textlength(mkt2, font=MKT_TXT) <= x1 - x0 - 16, "mkt2 too wide"
    d.text((x0 + 8, y + 4), label, font=MKT_LABEL, fill=INK)
    d.text((x0 + 8 + d.textlength(label, font=MKT_LABEL), y + 4), mkt1,
           font=MKT_TXT, fill=INK)
    d.text((x0 + 8, y + 20), mkt2, font=MKT_TXT, fill=INK)
    y += mkt_h + 6

    # ---- ALSO header ----
    d.text((x0, y), "ALSO ON FRIDAY 20 NOVEMBER", font=SECT, fill=RED)
    d.line([x0 + d.textlength("ALSO ON FRIDAY 20 NOVEMBER", font=SECT) + 10,
            y + 8, x1, y + 8], fill=(200, 200, 200), width=1)
    y += 22

    # ---- ALSO list: 3 columns x 14 rows, region dot + number + text ----
    # 16px type on 17px leading in 3 columns.
    also_col_w = (x1 - x0 - 48) / 3
    also_lead = 17
    for idx, (num, region, text) in enumerate(ALSO):
        col, row = divmod(idx, 14)
        lx = x0 + col * (also_col_w + 24)
        ly = y + row * also_lead
        assert d.textlength(text, font=ALSO_TXT) <= also_col_w - 40, \
            f"ALSO {num} too long: {text}"
        d.rectangle([lx, ly + 3, lx + 8, ly + 11],
                    fill=REGION_COLORS[region])
        d.text((lx + 14, ly), str(num), font=ALSO_NUM, fill=RED)
        d.text((lx + 40, ly), text, font=ALSO_TXT, fill=INK)
    for c in (0, 1):
        d.line([x0 + (c + 1) * also_col_w + c * 24 + 12, y,
                x0 + (c + 1) * also_col_w + c * 24 + 12,
                y + 14 * also_lead],
               fill=(220, 220, 220), width=1)
    y += 14 * also_lead + 6

    # ---- Footnote: † borderline-date and ‡ sourcing markers ----
    assert d.textlength(FOOTNOTE_TXT, font=NOTE_FONT) <= x1 - x0, \
        "footnote too wide"
    d.text((x0, y), FOOTNOTE_TXT, font=NOTE_FONT, fill=GREY)
    y += 16

    # ---- WHERE IT HAPPENED: world map with per-country story counts ----
    d.text((x0, y), "WHERE IT HAPPENED", font=SECT, fill=RED)
    d.line([x0 + d.textlength("WHERE IT HAPPENED", font=SECT) + 10, y + 8,
            x1, y + 8], fill=(200, 200, 200), width=1)
    y += 22
    draw_map(d, x0, y, x1 - x0, MAP_H)
    y += MAP_H + 5
    assert d.textlength(MAP_LEGEND_TXT, font=MAP_LEGEND) <= x1 - x0, \
        "map legend too wide"
    d.text((x0, y), MAP_LEGEND_TXT, font=MAP_LEGEND, fill=GREY)
    y += 13

    # ---- DATE CHECK footer note (small grey text, no red box) ----
    # Items first reported before Fri 20 Nov, deliberately left out.
    dc_head = "DATE CHECK — left out: "
    dc_w = d.textlength(dc_head, font=DATE_HEAD)
    dc_lines = wrap(d, DATE_CHECK, DATE_TXT, x1 - x0 - dc_w)
    assert len(dc_lines) <= 2, f"DATE CHECK wraps to {len(dc_lines)}"
    d.text((x0, y), dc_head, font=DATE_HEAD, fill=GREY)
    ly = y
    for i, ln in enumerate(dc_lines):
        lx = x0 + dc_w if i == 0 else x0
        d.text((lx, ly), ln, font=DATE_TXT, fill=GREY)
        ly += 13
    y = ly + 4

    # Footer
    assert y <= H - 16, f"page overflow: footer at y={y}"
    d.line([x0, y, x1, y], fill=RULE, width=1)
    d.text((x0, y + 4), "Every story happened or was first reported on "
           "Friday 20 November 2026.", font=FOOT, fill=GREY)
    src = "Sources: Reuters, AP, Kyiv Independent, UKMTO, EEAS."
    d.text((x1 - d.textlength(src, font=FOOT), y + 4), src, font=FOOT,
           fill=GREY)

    img.save("entry.png", format="PNG")
    img.resize((300, 300), Image.LANCZOS).save("preview-300.png",
                                               format="PNG")
    raw = open("entry.png", "rb").read()
    assert len(raw) <= 1048576, f"entry.png too big: {len(raw)}"
    print("entry.png:", img.size, len(raw), "bytes, sha256",
          hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
