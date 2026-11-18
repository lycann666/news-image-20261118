#!/usr/bin/env python3
"""THE WORLD TODAY - Wednesday 18 November 2026.

Draws a one-page newspaper poster summing up the day's world news and
writes it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

Deterministic: fixed colours, fixed geometry, no network, no randomness,
no clock reads. Two runs write byte-identical PNGs.

Stories (all reported on 18 November 2026):
  - Iran hits a US military radar system in Bahrain with drones
  - Ukraine strikes the Crimean Bridge for a second day; Russia hits Kyiv bridges
  - Trump arrives in Manila for Quad talks ahead of a China visit
  - Canada and China extend trade deals as Xi meets Carney before APEC
  - Britain sanctions eight firms over illegal West Bank settlements
  - Also: Cyclone Akvan, Nvidia +103% revenue, Dhoni retires from the IPL,
    Amazon's $7bn for Indian renewables, Gaza ceasefire warning.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PAPER = (246, 241, 229)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY_SOFT = (38, 58, 102)
GOLD = (201, 162, 39)
RED = (179, 38, 30)
TEAL = (15, 118, 110)
SKY = (148, 178, 205)
STEEL = (96, 116, 138)
CREAM = (246, 241, 229)
LIGHT = (255, 255, 255)
GREY = (90, 90, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(draw, x, y, w, h, kicker, headline, body, head_size=30,
               body_size=19):
    """One story panel: kicker, headline, body, thin border."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    kf = font(SANS_B, 17)
    draw.text((x + 14, y + 10), kicker, font=kf, fill=RED)
    hf = font(SERIF_B, head_size)
    lines = wrap(draw, headline, hf, w - 28)
    ty = y + 36
    for ln in lines:
        draw.text((x + 14, ty), ln, font=hf, fill=INK)
        ty += head_size + 4
    bf = font(SANS, body_size)
    blines = wrap(draw, body, bf, w - 28)
    by = ty + 6
    for ln in blines:
        draw.text((x + 14, by), ln, font=bf, fill=(60, 60, 60))
        by += body_size + 5
    return by


def draw_radar_scene(draw, x, y, w, h):
    """Night sky over Bahrain: radar dish, drones, red burst."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    stars = [(18, 22), (52, 48), (96, 16), (140, 40), (188, 20), (232, 52),
             (268, 24), (312, 46), (352, 18), (400, 38), (440, 22), (72, 70),
             (210, 66), (330, 70), (420, 64)]
    for sx, sy in stars:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=CREAM)
    # radar dish on a mast, left side
    mx, my = x + 90, y + h - 26
    draw.line([mx, my, mx, my - 56], fill=CREAM, width=5)
    draw.arc([mx - 40, my - 96, mx + 40, my - 16], start=200, end=340,
             fill=CREAM, width=6)
    draw.line([mx, my - 56, mx - 30, my - 82], fill=CREAM, width=4)
    draw.line([mx, my - 56, mx + 28, my - 86], fill=CREAM, width=4)
    # three drones crossing the sky
    for dx, dy, s in [(250, 46, 9), (330, 84, 7), (400, 40, 8)]:
        draw.ellipse([x + dx - s, y + dy - s // 2, x + dx + s, y + dy + s // 2],
                     fill=(220, 220, 220))
        draw.line([x + dx - s - 6, y + dy - 8, x + dx + s + 6, y + dy - 8],
                  fill=(220, 220, 220), width=2)
        draw.line([x + dx - s - 6, y + dy + 8, x + dx + s + 6, y + dy + 8],
                  fill=(220, 220, 220), width=2)
    # red impact burst on the dish
    bx, by = x + 132, y + h - 84
    for ang in range(0, 360, 45):
        import math
        ex = bx + int(26 * math.cos(math.radians(ang)))
        ey = by + int(26 * math.sin(math.radians(ang)))
        draw.line([bx, by, ex, ey], fill=(255, 90, 70), width=4)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 120, 90))
    # ground line
    draw.line([x, y + h - 8, x + w, y + h - 8], fill=GOLD, width=3)


def draw_bridge_scene(draw, x, y, w, h):
    """The Crimean Bridge: deck, towers, a broken span falling into the sea."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 235))
    # sea
    draw.rectangle([x, y + h - 42, x + w, y + h], fill=(70, 120, 160))
    for wx in range(20, w, 46):
        draw.arc([x + wx, y + h - 30, x + wx + 30, y + h - 12],
                 start=180, end=360, fill=CREAM, width=3)
    deck_y = y + 62
    # towers
    for tx in (70, 330):
        draw.rectangle([x + tx, y + 8, x + tx + 14, deck_y], fill=STEEL)
        draw.rectangle([x + tx - 6, y + 2, x + tx + 20, y + 10], fill=STEEL)
    # cables
    draw.line([x + 77, y + 10, x + 200, deck_y], fill=STEEL, width=2)
    draw.line([x + 337, y + 10, x + 240, deck_y], fill=STEEL, width=2)
    # deck: intact left, broken gap, intact right
    draw.rectangle([x + 6, deck_y, x + 176, deck_y + 10], fill=INK)
    draw.rectangle([x + 268, deck_y, x + w - 6, deck_y + 10], fill=INK)
    # falling span, tilted into the sea
    draw.polygon([(x + 190, deck_y + 4), (x + 256, deck_y + 2),
                  (x + 236, deck_y + 34), (x + 176, deck_y + 40)],
                 fill=(120, 40, 30))
    # smoke over the gap
    for cx, cy, r in [(216, 44, 16), (238, 30, 20), (262, 46, 14)]:
        draw.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                     fill=(150, 150, 150))
    # small red blast star at the break
    bx, by = x + 222, deck_y - 6
    for dx, dy in [(-14, 0), (14, 0), (0, -14), (0, 14), (-10, -10), (10, 10),
                   (-10, 10), (10, -10)]:
        draw.line([bx, by, bx + dx, by + dy], fill=RED, width=3)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 120, 160),
                 outline=NAVY, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=CREAM,
                 width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=CREAM, width=2)
    draw.arc([cx - r + 8, cy - r // 2, cx + r - 8, cy + r // 2], start=270,
             end=90, fill=CREAM, width=2)
    draw.arc([cx - r + 8, cy - r // 2, cx + r - 8, cy + r // 2], start=90,
             end=270, fill=CREAM, width=2)


def draw_trade_arrows(draw, x, y, w, h):
    """Two opposing trade arrows, teal and gold."""
    # teal arrow right
    draw.rectangle([x + 10, y + 26, x + w - 60, y + 44], fill=TEAL)
    draw.polygon([(x + w - 60, y + 12), (x + w - 8, y + 35),
                  (x + w - 60, y + 58)], fill=TEAL)
    # gold arrow left
    draw.rectangle([x + 52, y + h - 44, x + w - 10, y + h - 26], fill=GOLD)
    draw.polygon([(x + 52, y + h - 58), (x + 8, y + h - 35),
                  (x + 52, y + h - 12)], fill=GOLD)


def draw_scales(draw, cx, cy):
    """Simple scales of justice, sized to fit a 62px strip."""
    draw.line([cx, cy - 26, cx, cy + 26], fill=INK, width=4)
    draw.line([cx - 44, cy - 22, cx + 44, cy - 22], fill=INK, width=4)
    draw.ellipse([cx - 5, cy - 31, cx + 5, cy - 21], fill=GOLD)
    for sx in (cx - 44, cx + 44):
        draw.line([sx, cy - 22, sx - 13, cy + 2], fill=INK, width=2)
        draw.line([sx, cy - 22, sx + 13, cy + 2], fill=INK, width=2)
        draw.arc([sx - 15, cy - 2, sx + 15, cy + 16], start=0, end=180,
                 fill=GOLD, width=4)
    draw.line([cx - 26, cy + 26, cx + 26, cy + 26], fill=INK, width=4)


def draw_cyclone(draw, cx, cy):
    import math
    for i, r in enumerate(range(8, 36, 7)):
        start = i * 55
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=start,
                 end=start + 200, fill=TEAL, width=4)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=TEAL)


def draw_chip(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=NAVY)
    draw.rectangle([x + 12, y + 12, x + s - 12, y + s - 12], outline=GOLD,
                   width=3)
    for i in range(4):
        px = x + 14 + i * (s - 28) // 3
        draw.line([px, y - 8, px, y], fill=NAVY, width=4)
        draw.line([px, y + s, px, y + s + 8], fill=NAVY, width=4)
        py = y + 14 + i * (s - 28) // 3
        draw.line([x - 8, py, x, py], fill=NAVY, width=4)
        draw.line([x + s, py, x + s + 8, py], fill=NAVY, width=4)


def draw_bat_ball(draw, x, y):
    # cricket bat, leaning
    draw.polygon([(x + 6, y), (x + 24, y), (x + 21, y + 52),
                  (x + 3, y + 52)], fill=(190, 140, 80))
    draw.rectangle([x + 10, y - 22, x + 17, y], fill=(120, 80, 40))
    # red ball with seam
    draw.ellipse([x + 44, y + 28, x + 66, y + 50], fill=RED)
    draw.arc([x + 44, y + 28, x + 66, y + 50], start=300, end=120,
             fill=CREAM, width=2)


def draw_solar(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 80, 140))
    for gx in range(1, 4):
        draw.line([x + gx * w // 4, y, x + gx * w // 4, y + h], fill=CREAM,
                  width=2)
    for gy in range(1, 3):
        draw.line([x, y + gy * h // 3, x + w, y + gy * h // 3], fill=CREAM,
                  width=2)
    # sun
    sx, sy = x + w - 26, y - 2
    draw.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=GOLD)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.text((W // 2, 14), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=CREAM, anchor="ma")
    d.rectangle([0, 112, W, 116], fill=GOLD)
    d.text((W // 2, 126), "W E D N E S D A Y   ·   1 8   N O V E M B E R   2 0 2 6",
           font=font(SANS_B, 22), fill=INK, anchor="ma")
    d.line([16, 158, W - 16, 158], fill=INK, width=2)

    # ---- lead row: two big stories ----
    lead_y, lead_h = 170, 316
    lw = 486
    # left: Iran / Bahrain
    draw_radar_scene(d, 16, lead_y, lw, 128)
    draw_panel(d, 16, lead_y + 128, lw, lead_h - 128, "MIDDLE EAST",
               "IRAN STRIKES US RADAR IN BAHRAIN",
               "Drones hit a US military radar system in Bahrain, "
               "the third attack in days. Gulf states on alert.",
               head_size=28)
    # right: Ukraine / Crimean Bridge
    draw_bridge_scene(d, 522, lead_y, lw, 128)
    draw_panel(d, 522, lead_y + 128, lw, lead_h - 128, "WAR IN UKRAINE",
               "UKRAINE HITS CRIMEAN BRIDGE AGAIN",
               "Kyiv strikes the bridge to Crimea for a second day "
               "as Russia pounds bridges around Kyiv.",
               head_size=28)

    # ---- middle row: three stories ----
    mid_y, mid_h = 496, 272
    mw = 322
    xs = [16, 351, 686]
    # Manila: globe strip on top of panel
    d.rectangle([16, mid_y, 16 + mw, mid_y + 62], fill=NAVY_SOFT)
    draw_globe(d, 16 + 52, mid_y + 31, 24)
    d.text((16 + 88, mid_y + 18), "MANILA", font=font(SANS_B, 20),
           fill=CREAM)
    draw_panel(d, 16, mid_y + 62, mw, mid_h - 62, "ASIA-PACIFIC",
               "TRUMP LANDS IN MANILA FOR QUAD TALKS",
               "The US president opens Quad talks in the "
               "Philippines ahead of a China visit.",
               head_size=25, body_size=18)
    # Trade: arrows strip
    d.rectangle([351, mid_y, 351 + mw, mid_y + 62], fill=(232, 222, 196))
    draw_trade_arrows(d, 351 + 156, mid_y + 2, 130, 58)
    d.text((351 + 14, mid_y + 18), "TRADE", font=font(SANS_B, 20), fill=INK)
    draw_panel(d, 351, mid_y + 62, mw, mid_h - 62, "TRADE",
               "CANADA & CHINA EXTEND TRADE DEALS",
               "Xi meets Carney as the two sides extend trade "
               "cooperation ahead of APEC.",
               head_size=25, body_size=18)
    # Britain: scales strip
    d.rectangle([686, mid_y, 686 + mw, mid_y + 62], fill=(232, 222, 196))
    draw_scales(d, 686 + mw - 66, mid_y + 31)
    d.text((686 + 14, mid_y + 18), "LONDON", font=font(SANS_B, 20),
           fill=INK)
    draw_panel(d, 686, mid_y + 62, mw, mid_h - 62, "BRITAIN",
               "UK SANCTIONS SETTLEMENT FIRMS",
               "Britain sanctions eight firms over illegal West "
               "Bank settlements.",
               head_size=25, body_size=18)

    # ---- also today strip ----
    ay = 778
    d.rectangle([16, ay, W - 16, ay + 40], fill=RED)
    d.text((W // 2, ay + 6), "A L S O   T O D A Y", font=font(SANS_B, 22),
           fill=CREAM, anchor="ma")
    items = [
        ("CYCLONE AKVAN", "Severe storm builds over the Bay of Bengal.",
         "cyclone"),
        ("NVIDIA", "Revenue up 103% as AI chip demand soars.", "chip"),
        ("DHONI", "Retires from the IPL; to mentor Chennai Super Kings.",
         "bat"),
        ("AMAZON", "$7bn for renewables in India.", "solar"),
    ]
    col_w = 244
    for i, (kick, txt, kind) in enumerate(items):
        cx = 16 + i * col_w
        d.rectangle([cx, ay + 40, cx + col_w - 8, ay + 150], outline=INK,
                    width=1)
        d.text((cx + 10, ay + 48), kick, font=font(SANS_B, 17), fill=RED)
        if kind == "cyclone":
            draw_cyclone(d, cx + 38, ay + 112)
        elif kind == "chip":
            draw_chip(d, cx + 14, ay + 94, 36)
        elif kind == "bat":
            draw_bat_ball(d, cx + 6, ay + 92)
        elif kind == "solar":
            draw_solar(d, cx + 10, ay + 100, 52, 32)
        bf = font(SANS, 17)
        for j, ln in enumerate(wrap(d, txt, bf, col_w - 88)):
            d.text((cx + 78, ay + 78 + j * 21), ln, font=bf,
                   fill=(60, 60, 60))
    # Gaza line
    gy = ay + 162
    d.rectangle([16, gy, W - 16, gy + 34], fill=(232, 222, 196))
    d.text((W // 2, gy + 6),
           "GAZA — Aid groups warn the ceasefire could collapse as food runs short.",
           font=font(SANS_B, 18), fill=INK, anchor="ma")

    # ---- footer ----
    d.line([16, 986, W - 16, 986], fill=INK, width=2)
    d.text((W // 2, 994), "THE WORLD TODAY  ·  WEDNESDAY 18 NOVEMBER 2026",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    print(build())
