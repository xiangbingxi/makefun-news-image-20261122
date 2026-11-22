#!/usr/bin/env python3
"""news-image-20261122 — one-page front page of Sunday 22 November 2026.

Entrypoint for the make.fun bounty "Sum up 22 November's world news in
one image". Written by hand in this session. Draws the whole page with
PIL primitives only: no photos, no wire images, no network, no randomness.
Deterministic: the same code always writes the same bytes.

Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""
import hashlib
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
TEAL = (18, 63, 58)
GOLD = (176, 124, 16)
MUTED = (112, 107, 96)
HAIR = (160, 152, 136)
OCEAN = (216, 231, 240)
LAND = (232, 216, 184)

FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def _find(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def font(kind, size):
    names = {
        "serif": ["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"],
        "serif_reg": ["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"],
        "serif_it": ["LiberationSerif-Italic.ttf", "DejaVuSerif-Italic.ttf"],
        "sans": ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
        "sans_reg": ["LiberationSans-Regular.ttf", "DejaVuSans.ttf"],
        "sans_it": ["LiberationSans-Italic.ttf", "DejaVuSans-Oblique.ttf"],
    }[kind]
    for n in names:
        p = _find(n)
        if p:
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def wrap(drw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if drw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(drw, cx, y, text, fnt, fill=INK):
    w = drw.textlength(text, font=fnt)
    drw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def text_block(drw, x, y, text, fnt, max_w, leading, fill=INK):
    """Wrapped left-aligned block; returns y after the last line."""
    for line in wrap(drw, text, fnt, max_w):
        drw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes

def scene_cop31(drw, x, y, w, h):
    drw.rectangle([x, y, x + w, y + h], fill=TEAL)
    # stars
    for sx, sy, r in [(14, 14, 2), (300, 10, 2), (260, 26, 1), (60, 30, 1),
                      (180, 12, 2), (316, 46, 1)]:
        drw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                    fill=(240, 230, 190))
    # globe, left
    gx, gy, gr = x + 78, y + 62, 44
    drw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(74, 144, 164))
    drw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(240, 230, 190),
                width=2)
    for k in (-22, 0, 22):
        drw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 90 + k, 270 + k,
                fill=(240, 230, 190), width=1)
    drw.line([gx - gr, gy, gx + gr, gy], fill=(240, 230, 190), width=1)
    drw.polygon([(gx - 26, gy - 30), (gx - 4, gy - 34), (gx + 6, gy - 18),
                 (gx - 12, gy - 10)], fill=(201, 214, 107))
    drw.polygon([(gx + 2, gy + 8), (gx + 26, gy + 4), (gx + 30, gy + 22),
                 (gx + 8, gy + 26)], fill=(201, 214, 107))
    # clock, right (just before midnight)
    cx, cy, cr = x + 244, y + 58, 36
    drw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(247, 243, 232),
                outline=(26, 26, 26), width=3)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x1 = cx + (cr - 4) * math.sin(a)
        y1 = cy - (cr - 4) * math.cos(a)
        x2 = cx + (cr - 9) * math.sin(a)
        y2 = cy - (cr - 9) * math.cos(a)
        drw.line([x1, y1, x2, y2], fill=INK, width=2)
    drw.line([cx, cy, cx - 8, cy - 20], fill=INK, width=4)
    drw.line([cx, cy, cx + 4, cy - 28], fill=RED, width=3)
    drw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
    # banner
    drw.rectangle([x, y + h - 30, x + w, y + h], fill=RED)
    center(drw, x + w / 2, y + h - 26, "DOUBLE OVERTIME",
           font("sans", 17), fill=(255, 255, 255))


def scene_fire(drw, x, y, w, h):
    # flat orange bands
    bands = [(230, 126, 34), (214, 90, 32), (192, 57, 43)]
    bh = h // 3 + 1
    for i, c in enumerate(bands):
        drw.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    # smoke
    for sx, sy, r in [(238, 26, 12), (252, 14, 9), (224, 12, 8)]:
        drw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                    fill=(120, 110, 100))
    # chimney
    drw.rectangle([x + 228, y + 34, x + 254, y + 108], fill=(44, 44, 44))
    drw.rectangle([x + 224, y + 28, x + 258, y + 36], fill=(44, 44, 44))
    # factory hall with sawtooth roof
    drw.rectangle([x + 22, y + 78, x + 214, y + 138], fill=(44, 44, 44))
    teeth = [(22, 78), (60, 56), (98, 78), (136, 56), (174, 78), (214, 56),
             (214, 78)]
    drw.polygon([(x + px, y + py) for px, py in teeth], fill=(44, 44, 44))
    for wx in (44, 96, 148):
        drw.rectangle([x + wx, y + 96, x + wx + 26, y + 118],
                      fill=(247, 200, 90))
    # flames above the roofline
    flame = [(52, 78), (62, 52), (70, 66), (80, 42), (90, 64), (98, 52),
             (108, 78)]
    drw.polygon([(x + px, y + py) for px, py in flame], fill=(241, 196, 15))
    flame2 = [(150, 78), (158, 58), (166, 70), (174, 48), (182, 66),
              (190, 56), (196, 78)]
    drw.polygon([(x + px, y + py) for px, py in flame2], fill=(241, 196, 15))
    # ground
    drw.rectangle([x, y + h - 8, x + w, y + h], fill=(60, 30, 20))


def scene_card(img, x, y, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=BLUE)
    for sx, sy, r in [(16, 16, 2), (306, 12, 2), (288, 120, 2), (24, 122, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 255))
    # credit card on its own layer, tilted
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    cx0, cy0, cw, ch = 38, 22, 250, 96
    ld.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=10,
                         fill=(247, 243, 232), outline=(26, 26, 26), width=2)
    ld.rectangle([cx0, cy0 + 12, cx0 + cw, cy0 + 22], fill=(29, 78, 137))
    ld.text((cx0 + 18, cy0 + 27), "CREDIT CARD  ·  INTEREST RATE",
            font=font("sans", 9), fill=(112, 107, 96))
    ld.rectangle([cx0 + 18, cy0 + 46, cx0 + 52, cy0 + 70], fill=(212, 175, 55),
                 outline=(26, 26, 26), width=1)
    ld.text((cx0 + 64, cy0 + 40), "10%", font=font("serif", 40), fill=BLUE)
    ld.text((cx0 + 198, cy0 + 52), "CAP", font=font("sans", 15), fill=RED)
    rot = layer.rotate(-7, resample=Image.BICUBIC, center=(w / 2, h / 2))
    img.paste(rot, (x, y), rot)


# ---------------------------------------------------------------- small icons

def icon_tanker(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.polygon([(x + 6, y + 22), (x + 40, y + 22), (x + 36, y + 32),
                 (x + 10, y + 32)], fill=(29, 78, 137))
    drw.rectangle([x + 28, y + 12, x + 36, y + 22], fill=(179, 38, 30))
    for wx in (10, 22, 34):
        drw.arc([x + wx - 6, y + 34, x + wx + 6, y + 42], 0, 180,
                fill=(29, 78, 137), width=2)


def icon_chip(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.rectangle([x + 12, y + 12, x + 34, y + 34], fill=(26, 26, 26))
    drw.rectangle([x + 18, y + 18, x + 28, y + 28], fill=(212, 175, 55))
    for px in (17, 23, 29):
        drw.line([x + px, y + 6, x + px, y + 12], fill=(26, 26, 26), width=2)
        drw.line([x + px, y + 34, x + px, y + 40], fill=(26, 26, 26), width=2)
        drw.line([x + 6, y + px, x + 12, y + px], fill=(26, 26, 26), width=2)
        drw.line([x + 34, y + px, x + 40, y + px], fill=(26, 26, 26), width=2)


def icon_badge(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.ellipse([x + 8, y + 8, x + 38, y + 38], fill=(212, 175, 55),
                outline=(26, 26, 26), width=2)
    cx, cy = x + 23, y + 23
    pts = []
    for i in range(10):
        r = 11 if i % 2 == 0 else 5
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    drw.polygon(pts, fill=(179, 38, 30))


def icon_shield(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.polygon([(x + 10, y + 8), (x + 36, y + 8), (x + 36, y + 24),
                 (x + 23, y + 38), (x + 10, y + 24)], fill=(29, 78, 137),
                outline=(26, 26, 26))
    drw.line([x + 12, y + 16, x + 34, y + 16], fill=(255, 255, 255), width=2)
    drw.line([x + 12, y + 22, x + 34, y + 22], fill=(255, 255, 255), width=2)


def icon_cap(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.polygon([(x + 23, y + 10), (x + 40, y + 18), (x + 23, y + 26),
                 (x + 6, y + 18)], fill=(26, 26, 26))
    drw.polygon([(x + 14, y + 22), (x + 32, y + 22), (x + 32, y + 30),
                 (x + 23, y + 34), (x + 14, y + 30)], fill=(26, 26, 26))
    drw.line([x + 40, y + 18, x + 40, y + 30], fill=(179, 38, 30), width=2)
    drw.ellipse([x + 37, y + 29, x + 43, y + 35], fill=(179, 38, 30))


def icon_ship_fire(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.polygon([(x + 8, y + 26), (x + 38, y + 26), (x + 34, y + 34),
                 (x + 12, y + 34)], fill=(44, 44, 44))
    drw.rectangle([x + 26, y + 18, x + 32, y + 26], fill=(44, 44, 44))
    drw.polygon([(x + 16, y + 26), (x + 20, y + 14), (x + 24, y + 22),
                 (x + 28, y + 12), (x + 31, y + 26)], fill=(241, 196, 15))
    for wx in (10, 22, 34):
        drw.arc([x + wx - 6, y + 36, x + wx + 6, y + 44], 0, 180,
                fill=(29, 78, 137), width=2)


def icon_boat(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.ellipse([x + 26, y + 6, x + 40, y + 20], fill=(241, 196, 15))
    drw.arc([x + 6, y + 16, x + 40, y + 34], 0, 180, fill=(44, 44, 44),
            width=3)
    drw.line([x + 6, y + 25, x + 40, y + 25], fill=(44, 44, 44), width=2)
    drw.ellipse([x + 15, y + 14, x + 19, y + 18], fill=(179, 38, 30))
    drw.ellipse([x + 24, y + 14, x + 28, y + 18], fill=(179, 38, 30))
    for wx in (10, 22, 34):
        drw.arc([x + wx - 6, y + 34, x + wx + 6, y + 42], 0, 180,
                fill=(29, 78, 137), width=2)


def icon_megaphone(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.polygon([(x + 8, y + 18), (x + 30, y + 10), (x + 30, y + 30),
                 (x + 8, y + 24)], fill=(179, 38, 30))
    drw.rectangle([x + 14, y + 24, x + 20, y + 34], fill=(26, 26, 26))
    for r in (4, 9):
        drw.arc([x + 30, y + 16 - r, x + 38, y + 24 + r], -60, 60,
                fill=(26, 26, 26), width=2)


def icon_plane(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.ellipse([x + 8, y + 18, x + 38, y + 28], fill=(29, 78, 137))
    drw.polygon([(x + 20, y + 20), (x + 26, y + 8), (x + 30, y + 20)],
                fill=(29, 78, 137))
    drw.polygon([(x + 14, y + 26), (x + 18, y + 38), (x + 22, y + 26)],
                fill=(29, 78, 137))
    drw.line([x + 6, y + 6, x + 40, y + 40], fill=RED, width=3)
    drw.line([x + 6, y + 40, x + 40, y + 6], fill=RED, width=3)


def icon_mosquito(drw, x, y, s=46):
    drw.rectangle([x, y, x + s, y + s], fill=(233, 226, 208))
    drw.ellipse([x + 14, y + 20, x + 32, y + 28], fill=(26, 26, 26))
    drw.ellipse([x + 8, y + 12, x + 22, y + 22], fill=(160, 160, 160))
    drw.ellipse([x + 24, y + 12, x + 38, y + 22], fill=(160, 160, 160))
    for lx, ly in [(16, 28), (23, 30), (30, 28)]:
        drw.line([x + lx, y + ly, x + lx - 4, y + 40], fill=(26, 26, 26),
                 width=1)
        drw.line([x + lx, y + ly, x + lx + 4, y + 40], fill=(26, 26, 26),
                 width=1)
    drw.line([x + 32, y + 22, x + 42, y + 18], fill=(26, 26, 26), width=1)


# ---------------------------------------------------------------- map

def lonlat_to_xy(lon, lat):
    mx, my, mw, mh = 8, 646, 422, 222
    return (mx + (lon + 180) / 360 * mw, my + (75 - lat) / 130 * mh)


def draw_map(drw):
    drw.rectangle([8, 646, 430, 868], fill=OCEAN)
    # rough continent blobs (my own schematic shapes)
    na = [(30, 690), (60, 658), (120, 652), (150, 668), (140, 700),
          (110, 720), (80, 740), (50, 730), (28, 710)]
    sa = [(140, 756), (168, 748), (182, 770), (172, 810), (152, 852),
          (138, 820), (134, 780)]
    eu = [(196, 686), (220, 668), (252, 662), (268, 678), (258, 700),
          (232, 706), (206, 700)]
    af = [(200, 720), (236, 712), (272, 722), (282, 750), (268, 790),
          (244, 828), (222, 812), (204, 772), (196, 742)]
    asia = [(272, 668), (320, 650), (380, 648), (424, 660), (424, 700),
            (392, 730), (360, 756), (330, 748), (300, 720), (276, 694)]
    au = [(352, 828), (392, 822), (404, 838), (388, 856), (358, 850)]
    for poly in (na, sa, eu, af, asia, au):
        drw.polygon(poly, fill=LAND, outline=(180, 168, 140))
    for label, (lx, ly) in {
        "NORTH AMERICA": (52, 676), "SOUTH AMERICA": (116, 806),
        "EUROPE": (168, 664), "AFRICA": (204, 806), "ASIA": (330, 690),
        "AUSTRALIA": (352, 838),
    }.items():
        drw.text((lx, ly), label, font=font("sans", 8), fill=MUTED)
    pins = [
        (1, 30.7, 36.9), (2, 106.8, -6.2), (3, -77.0, 38.9),
        (4, 56.5, 26.5), (6, -107.4, 24.8), (9, 21.0, 57.0),
        (10, 8.5, 9.0), (11, 2.35, 48.9), (14, -52.0, -10.0),
        (21, 116.4, 39.9), (27, 6.1, 46.2), (30, 96.2, 16.8),
    ]
    for num, lon, lat in pins:
        px, py = lonlat_to_xy(lon, lat)
        drw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                    outline=(255, 255, 255), width=1)
        t = str(num)
        tw = drw.textlength(t, font=font("sans", 9))
        drw.text((px - tw / 2, py - 6), t, font=font("sans", 9),
                 fill=(255, 255, 255))


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([8, 8, 1016, 10], fill=INK)
    d.rectangle([8, 12, 1016, 13], fill=INK)
    center(d, W / 2, 20, "—  THE WORLD IN ONE DAY  —", font("sans", 12),
           fill=RED)
    center(d, W / 2, 36, "SUNDAY, 22 NOVEMBER 2026", font("serif", 38))
    center(d, W / 2, 78,
           "Climate talks run into double overtime; a factory burns in "
           "Jakarta, a boat sinks in Nigeria — and Washington talks of a "
           "10% cap on card rates.",
           font("serif_it", 13), fill=MUTED)
    d.line([8, 90, 1016, 90], fill=INK, width=1)

    # big numbers
    numbers = [
        ("24", "dead as a boat carrying mourners capsizes in Nigeria"),
        ("39", "missing in the Jakarta candy-factory fire"),
        ("10%", "the cap on card rates Trump vows to pass"),
        ("$48bn", "what the Iran war has cost the US, per the Pentagon"),
        ("11", "dead in Sinaloa after a cartel boss is captured"),
        ("35%", "of final energy from electricity in the COP31 draft by 2035"),
    ]
    for i, (num, lab) in enumerate(numbers):
        cx = 8 + i * 170 + 85
        center(d, cx, 96, num, font("serif", 28), fill=BLUE)
        y = 128
        for line in wrap(d, lab, font("sans_reg", 9), 164):
            center(d, cx, y, line, font("sans_reg", 9), fill=MUTED)
            y += 11
        if i:
            d.line([8 + i * 170, 100, 8 + i * 170, 146], fill=HAIR, width=1)
    d.line([8, 150, 1016, 150], fill=INK, width=1)

    # three big stories
    bigs = [
        ("ANTALYA · CLIMATE", "Climate talks in double overtime",
         "COP31 stretches into a second day of overtime as a fossil-fuel "
         "standoff threatens the deal. A last-minute text has no mention "
         "of coal, oil or gas — but a 1-billion-tonne carbon-capture "
         "goal. Delegates have until 03:00 GMT to object.",
         scene_cop31),
        ("JAKARTA · DISASTER", "Three dead, 39 missing in factory fire",
         "A fire at a candy factory in Serang, Banten, kills three "
         "workers; at least 39 are missing as rescuers search the site "
         "west of Jakarta.",
         scene_fire),
        ("WASHINGTON · POLITICS", "Trump vows a 10% cap on card rates",
         "The president says he will work with Democrats to cap "
         "credit-card interest rates at 10%.",
         scene_card),
    ]
    for i, (kick, head, lead, scene) in enumerate(bigs):
        x = 8 + i * 341
        wcol = 326
        if scene is scene_card:
            scene(img, x, 156, wcol, 138)
            d = ImageDraw.Draw(img)
        else:
            scene(d, x, 156, wcol, 138)
        d.text((x, 300), kick, font=font("sans", 11), fill=RED)
        y = 316
        for line in wrap(d, head, font("serif", 20), wcol):
            d.text((x, y), line, font=font("serif", 20), fill=INK)
            y += 24
        text_block(d, x, y + 4, lead, font("sans_reg", 10), wcol, 14)
        if i:
            d.line([x - 8, 158, x - 8, 448], fill=HAIR, width=1)
    d.line([8, 454, 1016, 454], fill=INK, width=1)

    # ten small stories
    smalls = [
        ("HORMUZ", "Iran: strait can reopen",
         "Tehran says a Hormuz reopening is possible if the US accepts "
         "\u201creasonable\u201d terms.", icon_tanker),
        ("WALL STREET", "Nvidia faces US probe",
         "The chipmaker faces a US accounting probe as its turmoil "
         "deepens.", icon_chip),
        ("SINALOA", "11 dead after cartel boss captured",
         "Violence follows the capture of cartel boss \u201cEl Chapo "
         "Isidro\u201d.", icon_badge),
        ("WASHINGTON", "US curbs Canada defence ties",
         "The Pentagon moves to restrict defence ties with Canada.",
         icon_shield),
        ("SEOUL", "Education chief quits in AI scandal",
         "South Korea\u2019s education chief resigns amid an AI cheating "
         "scandal.", icon_cap),
        ("BALTIC", "Sanctioned ship ablaze in Baltic",
         "A Russian cargo ship under sanctions catches fire after a "
         "drone strike.", icon_ship_fire),
        ("LAGOS", "Boat capsizes, 24 dead",
         "A boat carrying mourners to a funeral capsizes in Nigeria.",
         icon_boat),
        ("PARIS", "Sixth weekend of protests",
         "Cost-of-living rallies enter a sixth weekend across France.",
         icon_megaphone),
        ("BRUSSELS", "Belgium faces air shutdown",
         "A national strike threatens to halt air traffic on Monday.",
         icon_plane),
        ("DENGUE", "Lab mosquitoes beat dengue",
         "Strong new evidence that specially bred mosquitoes can fend "
         "off dengue.", icon_mosquito),
    ]
    for i, (place, head, lead, icon) in enumerate(smalls):
        row, col = divmod(i, 5)
        x = 8 + col * 202
        y = 460 + row * 82
        icon(d, x, y + 4)
        tx = x + 52
        d.text((tx, y), place, font=font("sans", 9), fill=RED)
        hy = y + 13
        for line in wrap(d, head, font("sans", 10), 144):
            d.text((tx, hy), line, font=font("sans", 10), fill=INK)
            hy += 12
        text_block(d, tx, hy + 2, lead, font("sans_reg", 9), 144, 11,
                   fill=MUTED)
    d.line([8, 624, 1016, 624], fill=INK, width=1)

    # map + briefs heading
    d.text((8, 630), "WHERE IT HAPPENED — 12 PLACES, 23 MORE STORIES",
           font=font("sans", 11), fill=RED)
    draw_map(d)

    briefs_a = [
        "14  Brazil — town clears rubble after a deadly storm.",
        "15  Haiti — farmers rebuild amid violence and hunger.",
        "16  Mexico — US-bound migrant caravan reaches Mexico.",
        "17  Seattle — immigration arrests at the airport.",
        "18  Washington — Trump gags federal contractors.",
        "19  Washington — Brenner, Vacirca weighed for top FDA roles.",
        "20  Washington — Senate Democrats face a leadership vote.",
        "21  Beijing — China warns of retaliation over US telecom ban.",
        "22  Taipei — Taiwan warns Canada\u2019s Carney on China ties.",
        "23  Seoul — Lee: speed is decisive in the AI race.",
        "24  New Delhi — protests hit Meta\u2019s offices in India.",
        "25  West Bengal — Christians report rising attacks.",
    ]
    briefs_b = [
        "26  Rome — ex-police chief dies by suicide.",
        "27  Geneva — states open path to a \u201ckiller robots\u201d accord.",
        "28  Geneva — UN: youth enter adulthood in insecurity.",
        "29  Pyongyang — Kim visits factories after \u201cTrump snub\u201d.",
        "30  Yangon — Rohingya hail genocide verdict on Myanmar.",
        "31  Gulf — Iran claims F-16 hit; US denies it.",
        "32  Manama — Bahrain warns of a potential threat.",
        "33  Riyadh — Saudi fund takes a stake in GTA.",
        "34  Washington — FBI probes hack of police database.",
        "35  Rome — Bulgari jeweller Paolo Bulgari dies at 89.",
        "36  Space — \u201cBlack Saturn\u201d: a 5D black-hole model.",
    ]
    for j, line in enumerate(briefs_a):
        d.text((446, 650 + j * 18), line, font=font("sans_reg", 9), fill=INK)
    for j, line in enumerate(briefs_b):
        d.text((736, 650 + j * 18), line, font=font("sans_reg", 9), fill=INK)

    # region bar
    regions = [("NORTH AMERICA", 11, BLUE), ("ASIA", 10, (44, 120, 110)),
               ("EUROPE", 8, GOLD), ("MIDDLE EAST", 4, RED),
               ("AFRICA", 1, (120, 110, 90)), ("SOUTH AMERICA", 1, (150, 140, 110)),
               ("SPACE", 1, (90, 90, 110))]
    bx = 8
    for name, count, col in regions:
        seg = int(1008 * count / 36)
        d.rectangle([bx, 878, bx + seg - 1, 888], fill=col)
        bx += seg
    legend = ("EUROPE 8   ·   NORTH AMERICA 11   ·   ASIA 10   ·   "
              "MIDDLE EAST 4   ·   AFRICA 1   ·   SOUTH AMERICA 1   ·   "
              "SPACE 1")
    center(d, W / 2, 893, legend, font("sans", 10), fill=MUTED)

    # date check box
    d.rectangle([8, 912, 1016, 974], outline=RED, width=2)
    d.text((18, 918), "DATE CHECK — WHAT WE LEFT OUT (NOT 22 NOVEMBER)",
           font=font("sans", 11), fill=RED)
    d.text((18, 934),
           "BepiColombo reaches Mercury — Sat 21 Nov (ESA/JAXA)",
           font=font("sans_reg", 9), fill=INK)
    d.text((18, 948),
           "Three missiles over Riyadh; coalition hits Hodeidah — Fri–Sat "
           "20–21 Nov",
           font=font("sans_reg", 9), fill=INK)
    d.text((18, 962),
           "Peru M6.7 quake — Fri 20 Nov; Sunday toll update: 1 dead, "
           "16 hurt",
           font=font("sans_reg", 9), fill=INK)

    # footer
    center(d, W / 2, 982,
           "HOW THIS PAGE WAS MADE — Drawn by hand with code: no photos, "
           "no wire images. Every story was first reported on 22 November "
           "2026.",
           font("serif_it", 10), fill=MUTED)
    center(d, W / 2, 996,
           "Sources: AFP · AP · Reuters · Al Jazeera · The Hindu · Dawn · "
           "Economic Times · Manila Times · Channel News Asia · ESA · Nature",
           font("sans_reg", 9), fill=MUTED)
    center(d, W / 2, 1010,
           "THE WORLD IN ONE DAY · SUNDAY 22 NOVEMBER 2026 · 36 STORIES · "
           "7 REGIONS",
           font("sans", 9), fill=INK)

    return img


if __name__ == "__main__":
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    image = build()
    out_path = os.path.join(out_dir, "entry.png")
    image.save(out_path, format="PNG")
    with open(out_path, "rb") as fh:
        data = fh.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "output is not a PNG"
    assert len(data) <= 1048576, "output is over the 1 MiB cap"
    assert image.size[0] <= 1024 and image.size[1] <= 1024, "over 1024 px"
    # whole-image check: the pixels the header describes must decode
    with Image.open(out_path) as check:
        check.load()
        assert check.size == image.size, "decoded size differs from header"
    print("wrote", out_path, image.size, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())
