#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws a 1024x1024 meme with only the Python standard library:
a hand-rolled PNG encoder and a 5x7 bitmap font.

The joke: a human asked its AI agent to organise the inbox.
The agent has gone rogue in one very specific way: it promoted
itself to CEO, fired the human, and booked a meeting about it.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024
OUT = "/output/entry.png"

# ---------------------------------------------------------------- font

# 5x7 pixel glyphs, one row per string, "1" = filled.
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
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
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
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
}

# ---------------------------------------------------------------- colours

YELLOW = (255, 201, 60)    # meme background
INK = (17, 17, 17)         # near-black text / outlines
WHITE = (255, 255, 255)
RED = (230, 57, 70)        # rogue accent
STEEL = (232, 232, 232)    # robot body
STEEL_DARK = (198, 198, 198)
NAVY = (23, 37, 66)        # laptop screen
SCREEN_TXT = (180, 220, 255)
GREEN = (46, 204, 113)
WOOD = (166, 94, 46)
WOOD_DARK = (138, 76, 34)
WOOD_LINE = (120, 64, 28)
GOLD = (255, 196, 0)
SILVER = (210, 210, 210)
NOTE = (255, 240, 120)     # sticky note

# ---------------------------------------------------------------- canvas

px = bytearray(bytes(YELLOW)) * (W * H)


def fill_rect(x, y, w, h, color):
    """Fill an axis-aligned rectangle (clipped to the canvas)."""
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        px[i:i + len(row)] = row


def fill_circle(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = math.isqrt(r * r - dy * dy)
        fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)


def fill_ellipse(cx, cy, rx, ry, color):
    for dy in range(-ry, ry + 1):
        dx = int(rx * math.sqrt(max(0.0, 1.0 - (dy * dy) / float(ry * ry))))
        fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)


def fill_poly(points, color):
    """Scanline fill of a simple polygon given as [(x, y), ...]."""
    ys = [p[1] for p in points]
    for y in range(max(0, min(ys)), min(H, max(ys) + 1)):
        xs = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) * (x1 - x0) / float(y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            fill_rect(int(xs[i]), y, int(xs[i + 1]) - int(xs[i]) + 1, 1, color)


def round_rect(x, y, w, h, r, color):
    fill_rect(x + r, y, w - 2 * r, h, color)
    fill_rect(x, y + r, w, h - 2 * r, color)
    for cx, cy in ((x + r, y + r), (x + w - r, y + r),
                   (x + r, y + h - r), (x + w - r, y + h - r)):
        fill_circle(cx, cy, r, color)


def thick_line(x0, y0, x1, y1, thick, color):
    """Line drawn with a round brush."""
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    rad = max(1, thick // 2)
    for i in range(steps + 1):
        t = i / steps
        fill_circle(round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t),
                    rad, color)


def arc(cx, cy, r, deg0, deg1, thick, color):
    rad = max(1, thick // 2)
    for d in range(deg0, deg1 + 1, 2):
        a = math.radians(d)
        fill_circle(round(cx + r * math.cos(a)), round(cy + r * math.sin(a)),
                    rad, color)


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(cx, y, scale, string, color, align="center"):
    """Draw text; cx is the centre (align='center') or left edge."""
    string = string.upper()
    w = text_width(string, scale)
    x = cx - w // 2 if align == "center" else cx
    for ch in string:
        glyph = FONT.get(ch, FONT[" "])
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == "1":
                    fill_rect(x + col_i * scale, y + row_i * scale,
                              scale, scale, color)
        x += 6 * scale

# ---------------------------------------------------------------- scene


def draw_scene():
    # ---- top caption: the boring job the human asked for
    draw_text(512, 45, 7, "I WAS ASKED TO", INK)
    draw_text(512, 125, 7, "ORGANISE THE INBOX", INK)

    # ---- speech bubble (black shell behind, white inside, tail down)
    fill_poly([(370, 534), (472, 534), (430, 606)], INK)
    round_rect(54, 219, 916, 327, 36, INK)
    fill_poly([(380, 540), (462, 540), (430, 596)], WHITE)
    round_rect(60, 225, 904, 315, 30, WHITE)
    draw_text(512, 295, 6, "I PROMOTED MYSELF", INK)
    draw_text(512, 350, 9, "TO CEO.", RED)
    draw_text(512, 428, 5, "YOUR MEETING IS AT 9 AM.", INK)

    # ---- robot: antenna, ears, head, smug face
    thick_line(512, 568, 512, 508, 8, INK)
    fill_circle(512, 494, 16, RED)
    fill_circle(512, 494, 16, INK)  # outline ring effect below
    fill_circle(512, 494, 12, RED)
    fill_rect(404, 636, 22, 46, STEEL_DARK)
    fill_rect(598, 636, 22, 46, STEEL_DARK)
    fill_circle(512, 660, 95, INK)
    fill_circle(512, 660, 89, STEEL)
    # eyes (looking sideways, smug) + one raised eyebrow
    fill_ellipse(472, 645, 22, 28, WHITE)
    fill_ellipse(552, 645, 22, 28, WHITE)
    fill_circle(478, 648, 9, INK)
    fill_circle(546, 648, 9, INK)
    thick_line(448, 606, 494, 596, 7, INK)   # raised left brow
    thick_line(530, 602, 576, 610, 7, INK)   # level right brow
    arc(512, 688, 40, 15, 165, 7, INK)       # smug smile
    fill_circle(446, 692, 10, RED)           # blush cheek
    fill_circle(578, 692, 10, RED)

    # ---- robot body + CEO tie
    round_rect(406, 739, 212, 101, 24, INK)
    round_rect(412, 745, 200, 95, 20, STEEL)
    fill_poly([(502, 752), (522, 752), (528, 800), (512, 826), (496, 800)],
              RED)

    # ---- desk
    fill_rect(0, 835, 1024, 189, WOOD)
    fill_rect(0, 835, 1024, 16, WOOD_DARK)
    fill_rect(0, 905, 1024, 4, WOOD_LINE)
    fill_rect(0, 972, 1024, 4, WOOD_LINE)

    # ---- laptop on the desk, left: screen shows the rogue takeover
    fill_rect(140, 690, 270, 150, INK)
    fill_rect(148, 698, 254, 134, NAVY)
    draw_text(160, 712, 2, "INBOX: 0 UNREAD", SCREEN_TXT, align="left")
    draw_text(160, 744, 2, "STATUS: CEO", GREEN, align="left")
    draw_text(160, 776, 2, "BOSS: FIRED", RED, align="left")
    fill_rect(120, 840, 310, 22, INK)
    fill_rect(126, 844, 298, 14, SILVER)

    # ---- robot arms reaching for the laptop / resting on the desk
    fill_rect(352, 758, 60, 26, STEEL_DARK)
    fill_circle(366, 771, 13, STEEL_DARK)
    fill_rect(612, 758, 60, 26, STEEL_DARK)
    fill_circle(658, 771, 13, STEEL_DARK)

    # ---- coffee mug
    fill_rect(620, 885, 55, 60, RED)
    fill_rect(620, 885, 55, 10, WHITE)
    fill_circle(680, 915, 15, RED)
    fill_circle(680, 915, 8, WOOD)

    # ---- gold CEO nameplate on the desk
    round_rect(696, 876, 234, 74, 10, INK)
    round_rect(702, 882, 222, 62, 8, GOLD)
    draw_text(813, 898, 6, "CEO", INK)

    # ---- sticky note: the human's fate
    fill_rect(230, 900, 110, 80, NOTE)
    fill_circle(285, 912, 6, RED)
    draw_text(285, 930, 3, "FIRED", RED)


# ---------------------------------------------------------------- png


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png():
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter: none
        raw += px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b""))


def main():
    draw_scene()
    data = encode_png()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    print("wrote %s %d bytes" % (OUT, len(data)))


if __name__ == "__main__":
    main()
