#!/usr/bin/env python3
"""THE WORLD TODAY - newspaper poster for 18 November 2026.

Draws a 1024x1024 PNG front page summarising the day's world news.
Standard library only: os, math, struct, zlib. No Pillow, no fonts
from disk, no network. Text is rendered with a small 5x7 bitmap
font defined in this file. Two runs write byte-identical PNGs.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

WHITE = (255, 255, 255)
BLACK = (22, 22, 22)
BODY = (64, 64, 64)
GRAY = (110, 110, 110)
RED = (176, 30, 30)
NAVY = (18, 38, 78)
STEEL = (120, 180, 220)
GREEN = (90, 200, 120)
LIGHT = (235, 235, 235)
SILVER = (215, 215, 215)

# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, '#' = ink. Authored here, no external font file.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
}


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def draw_line(self, x0, y0, x1, y1, color):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for s in range(steps + 1):
            t = s / steps
            x = round(x0 + (x1 - x0) * t)
            y = round(y0 + (y1 - y0) * t)
            self.set_pixel(x, y, color)
            self.set_pixel(x + 1, y, color)
            self.set_pixel(x, y + 1, color)

    def draw_circle(self, cx, cy, r, color):
        for deg in range(360):
            a = math.radians(deg)
            self.set_pixel(cx + round(r * math.cos(a)),
                           cy + round(r * math.sin(a)), color)
            self.set_pixel(cx + round(r * math.cos(a)) + 1,
                           cy + round(r * math.sin(a)), color)

    def draw_char(self, x, y, ch, scale, color):
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    self.fill_rect(x + col * scale, y + row * scale,
                                   scale, scale, color)

    def draw_text(self, x, y, text, scale, color):
        cx = x
        for ch in text:
            self.draw_char(cx, y, ch, scale, color)
            cx += 6 * scale
        return cx

    def text_width(self, text, scale):
        return len(text) * 6 * scale

    def draw_lines(self, x, y, lines, scale, color, line_h):
        for line in lines:
            self.draw_text(x, y, line, scale, color)
            y += line_h
        return y


def wrap(text, max_chars):
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= max_chars:
            cur += " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def story(c, x, y, width, headline, body, hscale=3, bscale=2):
    """One right-column story: headline + body + divider. Returns new y."""
    lines = wrap(headline, width // (6 * hscale))
    y = c.draw_lines(x, y, lines, hscale, BLACK, 7 * hscale + 7)
    y += 6
    blines = wrap(body, width // (6 * bscale))
    y = c.draw_lines(x, y, blines, bscale, BODY, 7 * bscale + 4)
    y += 10
    c.fill_rect(x, y, width, 2, LIGHT)
    return y + 16


# ---------------------------------------------------------------- png
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    data = (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


# ---------------------------------------------------------------- poster
def render():
    c = Canvas(W, H, WHITE)

    # Top red bar and masthead.
    c.fill_rect(0, 0, W, 10, RED)
    title = "THE WORLD TODAY"
    c.draw_text((W - c.text_width(title, 8)) // 2, 34, title, 8, BLACK)
    c.fill_rect(40, 118, 944, 3, BLACK)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    c.draw_text((W - c.text_width(date, 3)) // 2, 134, date, 3, BLACK)
    c.fill_rect(40, 168, 944, 6, RED)

    # ---- left column: lead story with a radar-screen graphic.
    px, pw = 40, 460
    c.fill_rect(px, 190, pw, 230, NAVY)
    cx, cy = px + 150, 305
    for r in (95, 65, 35):
        c.draw_circle(cx, cy, r, STEEL)
    c.draw_line(cx - 95, cy, cx + 95, cy, STEEL)
    c.draw_line(cx, cy - 95, cx, cy + 95, STEEL)
    c.draw_line(cx, cy, cx + 67, cy - 67, GREEN)
    for bx, by in ((cx + 52, cy - 28), (cx - 44, cy + 30), (cx + 18, cy + 52)):
        c.fill_rect(bx - 3, by - 3, 7, 7, GREEN)
    c.fill_rect(cx + 78, cy - 58, 7, 7, RED)
    # Small drone silhouette, top right of the panel.
    dx, dy = px + 330, 232
    c.fill_rect(dx, dy + 8, 52, 10, SILVER)
    c.fill_rect(dx + 22, dy, 8, 26, SILVER)
    c.fill_rect(dx - 12, dy, 30, 4, SILVER)
    c.fill_rect(dx + 34, dy, 30, 4, SILVER)
    c.fill_rect(dx - 12, dy + 22, 30, 4, SILVER)
    c.fill_rect(dx + 34, dy + 22, 30, 4, SILVER)
    # Legend for the radar blips, filling the empty right of the panel.
    c.fill_rect(dx + 4, dy + 76, 10, 10, GREEN)
    c.draw_text(dx + 20, dy + 76, "CONTACT", 2, STEEL)
    c.fill_rect(dx + 4, dy + 104, 10, 10, RED)
    c.draw_text(dx + 20, dy + 104, "HOSTILE", 2, STEEL)
    c.draw_text(px + 14, 386, "RADAR SCREEN: BAHRAIN", 2, STEEL)

    c.draw_text(px, 432, "A US RADAR SITE IN BAHRAIN", 2, GRAY)
    y = 458
    y = c.draw_lines(px, y, ["IRAN DRONE", "STRIKE HITS",
                             "US RADAR", "IN BAHRAIN"],
                     5, BLACK, 7 * 5 + 8)
    y += 10
    c.fill_rect(px, y, pw, 3, BLACK)
    y += 16
    body = ("IRAN LAUNCHED A DRONE STRIKE ON A US MILITARY RADAR "
            "SYSTEM IN BAHRAIN, ESCALATING TENSIONS ACROSS THE GULF.")
    y = c.draw_lines(px, y, wrap(body, pw // 12), 2, BODY, 18)
    y += 18

    # Left column, second story.
    y = c.draw_lines(px, y, ["UKRAINE HITS", "CRIMEA BRIDGE", "AGAIN"],
                     3, BLACK, 7 * 3 + 7)
    y += 6
    body2 = ("KYIV STRUCK THE CRIMEA BRIDGE FOR A SECOND DAY AS "
             "RUSSIA HIT A BRIDGE IN KYIV.")
    y = c.draw_lines(px, y, wrap(body2, pw // 12), 2, BODY, 18)

    # ---- right column: three stories, then a rising-chart panel.
    rx, rw = 544, 440
    y = 190
    y = story(c, rx, y, rw,
              "TRUMP LANDS IN MANILA FOR QUAD TALKS",
              "THE US PRESIDENT ARRIVED IN MANILA FOR QUAD TALKS "
              "WITH ALLIES ACROSS THE REGION.")
    y = story(c, rx, y, rw,
              "CANADA AND CHINA EXTEND TRADE DEALS",
              "XI MEETS CARNEY AHEAD OF APEC AS OTTAWA AND BEIJING "
              "EXTEND TRADE DEALS.")
    y = story(c, rx, y, rw,
              "BRITAIN SANCTIONS 8 FIRMS OVER WEST BANK SETTLEMENTS",
              "LONDON SANCTIONED EIGHT FIRMS OVER ILLEGAL "
              "SETTLEMENTS IN THE WEST BANK.")

    # Rising chart panel: Nvidia revenue up 103 percent.
    c.fill_rect(rx, y, rw, 186, LIGHT)
    c.draw_text(rx + 16, y + 14, "NVIDIA REVENUE +103%", 3, BLACK)
    pts = [(rx + 40, y + 158), (rx + 130, y + 138), (rx + 220, y + 118),
           (rx + 310, y + 88), (rx + 400, y + 52)]
    for a, b in zip(pts, pts[1:]):
        c.draw_line(a[0], a[1], b[0], b[1], RED)
    for (qx, qy) in pts:
        c.fill_rect(qx - 4, qy - 4, 9, 9, RED)
    c.draw_line(pts[-1][0], pts[-1][1], pts[-1][0] - 14, pts[-1][1] + 4, RED)
    c.draw_line(pts[-1][0], pts[-1][1], pts[-1][0] - 4, pts[-1][1] + 14, RED)

    # ---- bottom "Also today" strip.
    c.fill_rect(0, 936, W, 88, NAVY)
    strip = [
        "ALSO TODAY: CYCLONE AKVAN HITS COAST - NVIDIA REVENUE +103%",
        "DHONI RETIRES FROM IPL - AMAZON $7BN FOR INDIA RENEWABLES",
        "GAZA CEASEFIRE WARNING",
    ]
    yy = 948
    for line in strip:
        c.draw_text(40, yy, line, 2, WHITE)
        yy += 22

    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = render()
    write_png(os.path.join(out_dir, "entry.png"), canvas)


if __name__ == "__main__":
    main()
