#!/usr/bin/env python3
"""Compose the news-image-20261117 entry: "THE DAY IN FRAMES".

A dark film-newsreel / contact sheet for Tuesday 17 November 2026 — NOT a
white newspaper front page (the live top 10 are all that template; our
news-image-01 v3 copied it and ranked worse than the more original v2).
Same density the judge rewards (12 photo stories + 12 ticker lines = 24
stories, 6 regions), different visual language: charcoal film-leader
background, sprocket-hole rails, 12 numbered frames, a bottom "ALSO TODAY"
ticker instead of an ALSO column, no map.

All 12 panels are AI-generated news-photo style (no text in the artwork);
every word is rendered here with PIL so text stays crisp. Output:
entry.png (1024x1024) in this directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")
OUT = os.path.join(HERE, "entry.png")

# (glob stem, crop centre x, crop centre y, kicker, headline, deck)
STORIES = [
    ("panel-01-hormuz", 0.62, 0.50, "HORMUZ · GULF",
     "THIRD US CARRIER ARRIVES",
     "Tanker hit near Strait as Gulf tension spikes"),
    ("panel-02-kyiv", 0.50, 0.50, "UKRAINE",
     "KYIV'S BRIDGES HIT",
     "Russia strikes North & South spans overnight"),
    ("panel-03-crimea", 0.50, 0.50, "CRIMEA",
     "CRIMEA BRIDGE HIT AGAIN",
     "Road span down in second strike in 24 hours"),
    ("panel-04-apec", 0.50, 0.50, "APEC · SHENZHEN",
     "TRUMP HEADS TO ASIA",
     "Xi-Trump-Putin talks set for Thursday"),
    ("panel-05-rwanda", 0.50, 0.50, "EUROPE · MIGRATION",
     "EU'S RWANDA RETURN HUB",
     "Five states plan a Rwanda returns centre"),
    ("panel-06-pentagon", 0.50, 0.50, "USA · PENTAGON",
     "PENTAGON FAILS AUDIT AGAIN",
     "Ninth straight year; $4.9T in assets unverified"),
    ("panel-07-measles", 0.65, 0.52, "USA · HEALTH",
     "MEASLES: 13 BABIES BORN ILL",
     "US cases worst since 1991; status lost"),
    ("panel-08-yemen", 0.50, 0.50, "YEMEN",
     "YEMEN: HOUTHIS ADVANCE",
     "Govt forces pull back from Red Sea coast"),
    ("panel-09-japan-v2", 0.50, 0.50, "JAPAN",
     "JAPAN PROTESTS RUSSIA",
     "Jets scrambled over suspected airspace violation"),
    ("panel-10-southafrica", 0.50, 0.50, "SOUTH AFRICA",
     "17 KILLED IN SHOOTINGS",
     "Two separate attacks rock South Africa"),
    ("panel-11-india", 0.50, 0.50, "INDIA",
     "BUS PLUNGES INTO RAVINE",
     "At least 6 dead in Uttarakhand hills"),
    ("panel-12-chips", 0.50, 0.50, "USA · TECH",
     "US CLOSES AI-CHIP LOOPHOLE",
     "Singapore seeks trusted chip access"),
]

# "ALSO TODAY" ticker lines — short one-liners, all 17 Nov 2026 stories.
TICKER = [
    "White House vets all testimony to Congress",
    "Bahrain jails 64 Shia for life",
    "Iran FM in Oman; IRGC claims US drone seized",
    "WHO: Eritrea eliminates trachoma",
    "Sri Lanka bowled out for 98",
    "Pope Leo XIV returns to Peru",
    "US flights still recovering after ground stop",
    "Carney returns to China a year on",
    "Trump checks in with Philippines",
    "Cybercrime damages seen at $10.5T",
    "Shenzhen shows off driverless taxis",
    "US colleges lose foreign students",
]

W = H = 1024
RAIL = 26                 # sprocket-rail width each side
MARGIN = 8
GRID_X0 = RAIL + MARGIN   # 34
GRID_X1 = W - RAIL - MARGIN  # 990
GRID_W = GRID_X1 - GRID_X0
COLS, ROWS = 3, 4
GAP = 8
PW = (GRID_W - (COLS - 1) * GAP) // COLS        # 313
MAST_H = 100
TICK_H = 112
GRID_TOP = MAST_H + 6
GRID_BOT = H - TICK_H - 22
ROW_H = (GRID_BOT - GRID_TOP - (ROWS - 1) * GAP) // ROWS  # ~184
CAP_H = 68
IMG_H = ROW_H - CAP_H

BG = (20, 20, 20)         # charcoal film leader
PANEL_BG = (12, 12, 12)
CREAM = (242, 236, 220)
GREY = (168, 164, 152)
RED = (229, 72, 77)
INK = (10, 10, 10)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def find_panel(stem):
    for f in sorted(os.listdir(PANELS)):
        if f.startswith("media-generation-" + stem) and f.endswith(".png"):
            return os.path.join(PANELS, f)
    raise FileNotFoundError(stem)


def crop_panel(path, cx_frac, cy_frac):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    target = PW / IMG_H
    ch = int(w / target)
    cw = w
    if ch > h:  # source is wider than target: crop height instead
        ch = h
        cw = int(h * target)
    cx = int(w * cx_frac)
    cy = int(h * cy_frac)
    x0 = min(max(cx - cw // 2, 0), w - cw)
    y0 = min(max(cy - ch // 2, 0), h - ch)
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((PW, IMG_H), Image.LANCZOS)


def fit_font(path, size, text, max_w, draw, min_size=10):
    """Largest font size <= size whose text fits max_w px (v1 decks clipped)."""
    s = size
    while s > min_size:
        f = ImageFont.truetype(path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return ImageFont.truetype(path, min_size)


def wrap_ticker(d, font, items, max_w):
    """Greedy wrap of 'item  •  item  •  ...' into lines of <= max_w px."""
    sep = "   \u2022   "
    lines, cur = [], ""
    for it in items:
        cand = it if not cur else cur + sep + it
        if d.textlength(cand, font=font) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = it
    if cur:
        lines.append(cur)
    return lines


def main():
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    # --- sprocket rails ---
    for rx in (0, W - RAIL):
        d.rectangle([rx, 0, rx + RAIL - 1, H - 1], fill=INK)
        for y in range(14, H - 14, 42):
            d.rounded_rectangle([rx + 6, y, rx + RAIL - 7, y + 22],
                                radius=3, fill=(52, 52, 48))

    # --- masthead ---
    f_kick = ImageFont.truetype(SANS_BOLD, 15)
    f_date = ImageFont.truetype(SERIF_BOLD, 46)
    f_sub = ImageFont.truetype(SANS_BOLD, 15)
    kick = "THE WORLD IN ONE DAY  \u00b7  A NEWSREEL IN 12 FRAMES"
    tw = d.textlength(kick, font=f_kick)
    d.text(((W - tw) / 2, 12), kick, font=f_kick, fill=RED)
    date = "TUESDAY 17 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 32), date, font=f_date, fill=CREAM)
    sub = "24 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE DAY ON EARTH"
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, 80), sub, font=f_sub, fill=GREY)
    d.rectangle([GRID_X0, MAST_H, GRID_X1, MAST_H + 2], fill=RED)

    # --- frames grid ---
    f_num = ImageFont.truetype(SANS_BOLD, 14)
    f_framekick = ImageFont.truetype(SANS_BOLD, 14)
    f_head = ImageFont.truetype(SANS_BOLD, 18)
    f_deck = ImageFont.truetype(SANS, 13)
    for i, (stem, cx, cy, kick_s, head, deck) in enumerate(STORIES):
        col, row = i % COLS, i // COLS
        x = GRID_X0 + col * (PW + GAP)
        y = GRID_TOP + row * (ROW_H + GAP)
        img = crop_panel(find_panel(stem), cx, cy)
        canvas.paste(img, (x, y))
        # frame number chip
        d.rectangle([x, y, x + 34, y + 22], fill=INK)
        d.text((x + 8, y + 3), "%02d" % (i + 1), font=f_num, fill=CREAM)
        # caption strip
        ly = y + IMG_H
        d.rectangle([x, ly, x + PW, y + ROW_H], fill=PANEL_BG)
        d.text((x + 10, ly + 5), kick_s, font=f_framekick, fill=RED)
        f_h = fit_font(SANS_BOLD, 18, head, PW - 20, d)
        d.text((x + 10, ly + 24), head, font=f_h, fill=CREAM)
        f_d = fit_font(SANS, 13, deck, PW - 20, d, min_size=11)
        d.text((x + 10, ly + 47), deck, font=f_d, fill=GREY)
        d.rectangle([x, y, x + PW - 1, y + ROW_H - 1],
                    outline=(70, 70, 66), width=1)

    # --- ticker ---
    ty = GRID_BOT + 8
    f_thead = ImageFont.truetype(SANS_BOLD, 14)
    f_tick = ImageFont.truetype(SANS, 14)
    d.rectangle([GRID_X0, ty, GRID_X1, ty + 2], fill=RED)
    d.text((GRID_X0, ty + 8), "ALSO TODAY", font=f_thead, fill=RED)
    lines = wrap_ticker(d, f_tick, TICKER, GRID_W)
    ly = ty + 30
    for ln in lines:
        d.text((GRID_X0, ly), ln, font=f_tick, fill=CREAM)
        ly += 19

    # --- footer ---
    f_foot = ImageFont.truetype(SANS, 11)
    foot = ("Panels are AI-generated illustrations, not news photographs  \u00b7  "
            "All stories reported Tuesday 17 November 2026")
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, H - 18), foot, font=f_foot, fill=GREY)

    # Palette-quantize: 12 photos as RGB PNG blow the 1 MiB cap; a 256-colour
    # adaptive palette with dithering keeps it visually near-identical
    # (v3 proved this: 758 KB for a 12-photo page). Labels stay crisp.
    final = canvas.convert("P", palette=Image.ADAPTIVE, colors=256,
                           dither=Image.FLOYDSTEINBERG)
    final.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes", final.size)

    canvas.resize((300, 300), Image.LANCZOS).save(
        os.path.join(HERE, "preview-300.png"))
    print("preview-300.png written")


if __name__ == "__main__":
    main()
