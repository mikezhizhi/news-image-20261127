#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Friday 27 November 2026.

One 1024x1024 PNG summarising the day's world news, drawn with Pillow.
Run:  python3 draw_frontpage.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
M = 36                      # page margin
CW = W - 2 * M              # content width

PAPER = (248, 244, 232)
INK = (18, 18, 18)
GREY = (90, 86, 76)
RED = (176, 30, 36)
NAVY = (29, 53, 87)
GOLD = (233, 163, 25)
TEAL = (42, 127, 111)
BLUE = (43, 98, 168)
BROWN = (146, 94, 42)
PANEL = (255, 253, 246)
PANEL_LINE = (216, 210, 192)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, max_w, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(d, x, y, s, col):
    d.ellipse([x, y, x + s, y + s], outline=col, width=4)
    d.ellipse([x + 4, y + s * 0.22, x + s - 4, y + s * 0.78], outline=col, width=3)
    d.line([(x + s / 2, y), (x + s / 2, y + s)], fill=col, width=3)
    d.line([(x, y + s / 2), (x + s, y + s / 2)], fill=col, width=3)


def draw_ballot(d, x, y, s, col):
    d.rectangle([x + 2, y + s * 0.38, x + s - 2, y + s - 4],
                outline=col, width=4)
    d.line([(x + s * 0.2, y + s * 0.38), (x + s * 0.8, y + s * 0.38)],
           fill=col, width=4)
    d.line([(x + s * 0.28, y + s * 0.62), (x + s * 0.45, y + s * 0.8),
            (x + s * 0.78, y + s * 0.42)], fill=col, width=5)


def draw_flame(d, x, y, s, col):
    pts = [(x + s * 0.5, y + 2), (x + s * 0.66, y + s * 0.34),
           (x + s * 0.9, y + s * 0.3), (x + s * 0.82, y + s * 0.58),
           (x + s * 0.95, y + s * 0.72), (x + s * 0.68, y + s * 0.86),
           (x + s * 0.72, y + s * 0.98), (x + s * 0.42, y + s * 0.9),
           (x + s * 0.28, y + s * 0.98), (x + s * 0.2, y + s * 0.72),
           (x + s * 0.05, y + s * 0.6), (x + s * 0.3, y + s * 0.44)]
    d.polygon(pts, fill=col)


def draw_barrel(d, x, y, s, col):
    d.rounded_rectangle([x + s * 0.18, y + 4, x + s * 0.82, y + s - 4],
                        radius=8, outline=col, width=4)
    d.line([(x + s * 0.18, y + s * 0.32), (x + s * 0.82, y + s * 0.32)],
           fill=col, width=4)
    d.line([(x + s * 0.18, y + s * 0.68), (x + s * 0.82, y + s * 0.68)],
           fill=col, width=4)


def draw_boat(d, x, y, s, col):
    d.polygon([(x + 4, y + s * 0.62), (x + s - 4, y + s * 0.62),
               (x + s * 0.82, y + s * 0.88), (x + s * 0.18, y + s * 0.88)],
              fill=col)
    d.line([(x + s * 0.5, y + s * 0.6), (x + s * 0.5, y + 4)], fill=col, width=4)
    d.polygon([(x + s * 0.54, y + 8), (x + s * 0.54, y + s * 0.56),
               (x + s * 0.88, y + s * 0.56)], fill=col)
    d.line([(x, y + s * 0.94), (x + s, y + s * 0.94)], fill=col, width=3)


def draw_stars(d, x, y, s, col):
    import math
    cx, cy, r = x + s / 2, y + s / 2, s * 0.36
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)


ICONS = [
    ("globe", NAVY), ("ballot", TEAL), ("flame", RED),
    ("barrel", BROWN), ("boat", BLUE), ("stars", NAVY),
]
DRAW_ICON = {"globe": draw_globe, "ballot": draw_ballot, "flame": draw_flame,
             "barrel": draw_barrel, "boat": draw_boat, "stars": draw_stars}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    mast = font(SERIF_B, 86)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 22), title, font=mast, fill=INK)
    rule(d, M, W - M, 128, 3)
    rule(d, M, W - M, 134, 1)

    # ---- dateline row ----
    dl = font(SANS_B, 21)
    d.text((M, 146), "FRIDAY 27 NOVEMBER 2026", font=dl, fill=RED)
    right = "ONE DAY  •  ONE PAGE  •  THE WORLD"
    rw = d.textlength(right, font=dl)
    d.text((W - M - rw, 146), right, font=dl, fill=INK)
    rule(d, M, W - M, 180, 2)

    # ---- lead story: the Thanksgiving storm ----
    ly = 198
    kick = font(SANS_B, 23)
    d.text((M, ly), "UNITED STATES  —  THANKSGIVING DAY", font=kick, fill=RED)
    head = font(SERIF_B, 74)
    y = ly + 34
    for line in ["STORM STOPS", "THANKSGIVING"]:
        d.text((M, y), line, font=head, fill=INK)
        y += 82
    deck = font(SERIF_R, 25)
    y = para(d, M, y + 6,
             "A fierce storm lashes the US East Coast on the holiday: "
             "the Thanksgiving parade in New York is postponed, about "
             "400 flights are cancelled and 724,000 homes lose power.",
             deck, 592, INK, leading=32)
    stat = font(SANS_B, 21)
    d.text((M, y + 12), "400 FLIGHTS CANCELLED", font=stat, fill=RED)
    d.text((M, y + 40), "724,000 HOMES WITHOUT POWER", font=stat, fill=RED)

    # ---- lead illustration: storm over the city ----
    ix, iy, iw, ih = 656, 198, 332, 316
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=(23, 42, 68))
    d.rectangle([ix, iy, ix + iw, iy + ih], outline=INK, width=2)
    # clouds
    for cx, cy, cr in [(ix + 60, iy + 46, 52), (ix + 150, iy + 30, 64),
                       (ix + 250, iy + 52, 56), (ix + 110, iy + 66, 46)]:
        d.ellipse([cx - cr, cy - cr * 0.55, cx + cr, cy + cr * 0.55],
                  fill=(58, 74, 96))
    # lightning (drawn after the skyline so the bolt stays visible)
    # rain
    for rx in range(ix + 18, ix + iw - 10, 26):
        d.line([(rx, iy + 130), (rx - 12, iy + 178)], fill=(140, 170, 205), width=3)
    # skyline
    base = iy + ih
    for bx, bw, bh in [(ix + 8, 46, 92), (ix + 62, 58, 128), (ix + 128, 52, 84),
                       (ix + 188, 62, 140), (ix + 258, 58, 100)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(12, 20, 32))
        for wy in range(base - bh + 12, base - 10, 20):
            for wx in range(bx + 10, bx + bw - 8, 18):
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=GOLD)
    d.polygon([(ix + 218, iy + 92), (ix + 188, iy + 172), (ix + 208, iy + 172),
               (ix + 186, iy + 240), (ix + 236, iy + 148), (ix + 214, iy + 148)],
              fill=GOLD)
    # stray parade balloon
    d.ellipse([ix + 40, iy + 150, ix + 104, iy + 196], fill=RED)
    d.line([(ix + 72, iy + 196), (ix + 60, iy + 232)], fill=(220, 220, 220), width=2)
    cap = font(SERIF_I, 19)
    para(d, ix, iy + ih + 10,
         "Rain and wind batter the East Coast as Thanksgiving Day is disrupted.",
         cap, iw, GREY, leading=23)

    rule(d, M, W - M, 588, 2)

    # ---- six more stories, 3 x 2 grid ----
    stories = [
        ("UKRAINE  •  EUROPE", "Trump to Putin: pull back",
         "Trump says he urged Putin to end \u201cmilitary aggression\u201d in Europe."),
        ("NEW ZEALAND", "Coalition one seat short",
         "Official results leave Luxon a seat short; a centrist party decides."),
        ("MIDDLE EAST", "Two Italians killed in Kuwait",
         "An Iranian drone strike on a Kuwait facility kills two Italians."),
        ("ENERGY", "Brent crude nears $97",
         "Oil climbs after Middle East attacks; OPEC+ faces tricky 2027 talks."),
        ("THE KOREAS", "Six fishermen sent home",
         "Seoul sends home six North Koreans found on a drifting boat; one stays."),
        ("EUROPE", "EU split over $49bn loan",
         "Leaders are divided over the budget and a $49 billion loan to Ukraine."),
    ]
    gx, gy = M, 606
    cw, ch, gapx, gapy = 304, 146, 20, 14
    hf = font(SERIF_B, 25)
    bf = font(SERIF_R, 18)
    kf = font(SANS_B, 16)
    for i, (kicker, headline, body) in enumerate(stories):
        cx = gx + (i % 3) * (cw + gapx)
        cy = gy + (i // 3) * (ch + gapy)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=PANEL,
                    outline=PANEL_LINE, width=1)
        name, colour = ICONS[i]
        d.rounded_rectangle([cx + 12, cy + 12, cx + 88, cy + 88],
                            radius=10, fill=colour)
        DRAW_ICON[name](d, cx + 22, cy + 22, 56, (255, 255, 255))
        d.text((cx + 100, cy + 14), kicker, font=kf, fill=RED)
        hy = para(d, cx + 100, cy + 36, headline, hf, cw - 112, INK, leading=27)
        para(d, cx + 12, cy + 96, body, bf, cw - 24, INK, leading=22)

    # ---- also today ticker ----
    ty = 922
    d.rectangle([M, ty, W - M, ty + 62], fill=INK)
    tf = font(SANS_B, 19)
    para(d, M + 14, ty + 8,
         "ALSO TODAY:  Sanofi seals $41bn Insmed buyout  •  Duterte's ICC "
         "trial set to start  •  Tokyo prices rise 2.9%  •  Houthis push "
         "towards Aden",
         tf, CW - 28, (255, 255, 255), leading=23)

    foot = font(SERIF_I, 16)
    note = "All stories first reported on Friday 27 November 2026  —  The World Today"
    nw = d.textlength(note, font=foot)
    d.text(((W - nw) / 2, 994), note, font=foot, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
