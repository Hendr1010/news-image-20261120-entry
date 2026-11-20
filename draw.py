#!/usr/bin/env python3
"""Draw the front page for 20 November 2026 (news-image-20261120).

Pure Pillow drawing, deterministic (seeded Random only), no network.
Writes entry.png (1024x1024) next to this file.
"""
import math
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
INK = (17, 17, 17)
RED = (178, 34, 34)
MUTED = (90, 84, 72)
RULE = (17, 17, 17)
CARD_BG = (255, 252, 244)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
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


def draw_lines(draw, lines, x, y, fnt, fill, leading=None, align="left", max_w=None):
    """Draw lines; returns y after last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        lx = x
        if align == "center" and max_w is not None:
            lx = x + (max_w - draw.textlength(line, font=fnt)) // 2
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def sunset_skyline(draw, box, rng):
    """Neon Vice City sunset skyline inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # vertical gradient: deep purple -> magenta -> orange -> gold
    stops = [(58, 20, 90), (140, 40, 110), (220, 80, 60), (255, 150, 60), (255, 205, 90)]
    for yy in range(h):
        t = yy / max(1, h - 1)
        seg = min(len(stops) - 2, int(t * (len(stops) - 1)))
        f = t * (len(stops) - 1) - seg
        c = tuple(int(stops[seg][i] + (stops[seg + 1][i] - stops[seg][i]) * f) for i in range(3))
        draw.line([(x0, y0 + yy), (x1, y0 + yy)], fill=c)
    # sun
    cx, cy = x0 + int(w * 0.68), y0 + int(h * 0.42)
    r = int(h * 0.22)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 235, 160))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 200, 90), width=3)
    # stars in the upper sky
    for _ in range(40):
        sx, sy = x0 + rng.randint(0, w - 1), y0 + rng.randint(0, int(h * 0.35))
        draw.point((sx, sy), fill=(255, 255, 255))
    # skyline: back row (lighter) then front row (dark)
    base = y1
    for row, col in ((0.55, (70, 30, 90)), (0.75, (25, 12, 45))):
        bx = x0
        while bx < x1:
            bw = rng.randint(28, 70)
            bh = int(h * row * rng.uniform(0.45, 1.0))
            draw.rectangle([bx, base - bh, bx + bw, base], fill=col)
            # lit windows
            for wy in range(base - bh + 8, base - 6, 12):
                for wx in range(bx + 5, bx + bw - 5, 10):
                    if rng.random() < 0.35:
                        draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 210, 110))
            bx += bw + rng.randint(2, 10)
    # water reflection strip
    for i in range(0, w, 14):
        draw.line([(x0 + i, base - 4), (x0 + i + 8, base - 4)], fill=(255, 190, 120), width=2)


def clock(draw, box):
    """A clock face on a dark background (decision delayed)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 28, 40))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(235, 240, 245), width=3)
    for h in range(12):
        a = math.radians(h * 30 - 90)
        x2, y2 = cx + int((r - 4) * math.cos(a)), cy + int((r - 4) * math.sin(a))
        x3, y3 = cx + int((r - 9) * math.cos(a)), cy + int((r - 9) * math.sin(a))
        draw.line([(x2, y2), (x3, y3)], fill=(235, 240, 245), width=2)
    draw.line([(cx, cy), (cx, cy - 18)], fill=(255, 210, 110), width=3)
    draw.line([(cx, cy), (cx + 14, cy + 8)], fill=(255, 210, 110), width=3)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 210, 110))


def three_flags(draw, box):
    """Three small flags (US, China, Russia) side by side in box."""
    x0, y0, x1, y1 = box
    fw, fh = (x1 - x0 - 16) // 3, (y1 - y0) - 8
    fy = y0 + 4
    # US flag
    ux = x0
    for i in range(7):
        draw.rectangle([ux, fy + i * fh // 7, ux + fw, fy + (i + 1) * fh // 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([ux, fy, ux + fw * 2 // 5, fy + fh * 4 // 7], fill=(30, 40, 90))
    # China flag
    cx = x0 + fw + 8
    draw.rectangle([cx, fy, cx + fw, fy + fh], fill=(222, 41, 16))
    for sx, sy in ((8, 8), (22, 12), (26, 20), (22, 28), (10, 24)):
        draw.ellipse([cx + sx, fy + sy, cx + sx + 7, fy + sy + 7], fill=(255, 222, 0))
    # Russia flag
    rx = x0 + 2 * (fw + 8)
    for i, c in enumerate(((255, 255, 255), (0, 60, 160), (220, 30, 30))):
        draw.rectangle([rx, fy + i * fh // 3, rx + fw, fy + (i + 1) * fh // 3], fill=c)
    for fx in (ux, cx, rx):
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=(120, 110, 95), width=1)


def scales(draw, box):
    """Simple scales of justice on a dark background."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 28, 40))
    cx, cy = (x0 + x1) // 2, y0 + 18
    draw.line([(cx, cy), (cx, y1 - 22)], fill=(220, 190, 90), width=4)
    draw.line([(cx - 42, cy + 8), (cx + 42, cy + 8)], fill=(220, 190, 90), width=4)
    for sx in (cx - 42, cx + 42):
        draw.line([(sx, cy + 8), (sx, y1 - 34)], fill=(220, 190, 90), width=2)
        draw.arc([sx - 20, y1 - 40, sx + 20, y1 - 18], 0, 180, fill=(220, 190, 90), width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(220, 190, 90))


def storm(draw, box, rng):
    """Cyclone spiral + rain over a grey sea."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(70, 90, 110))
    cx, cy = (x0 + x1) // 2, y0 + (y1 - y0) // 2 - 6
    for k in range(3):
        r = 34 - k * 9
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200 + k * 40, 200 + k * 40 + 300,
                 fill=(235, 240, 245), width=5)
    for _ in range(26):
        rx = x0 + rng.randint(0, x1 - x0)
        ry = y0 + rng.randint(0, y1 - y0)
        draw.line([(rx, ry), (rx - 4, ry + 12)], fill=(200, 215, 230), width=2)


def starfield_probe(draw, box, rng):
    """Voyager 1: starfield + probe silhouette."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(8, 10, 26))
    for _ in range(60):
        sx, sy = x0 + rng.randint(0, x1 - x0), y0 + rng.randint(0, y1 - y0)
        s = rng.randint(1, 2)
        draw.ellipse([sx, sy, sx + s, sy + s], fill=(255, 255, 255))
    cx, cy = (x0 + x1) // 2 + 20, (y0 + y1) // 2
    draw.line([(cx - 46, cy + 26), (cx + 10, cy - 6)], fill=(200, 200, 210), width=5)
    draw.rectangle([cx - 8, cy - 14, cx + 26, cy + 6], fill=(170, 175, 190))
    draw.arc([cx + 26, cy - 22, cx + 52, cy + 4], -90, 90, fill=(220, 220, 230), width=4)
    draw.line([(cx + 39, cy - 9), (cx + 58, cy - 26)], fill=(200, 200, 210), width=2)
    draw.ellipse([cx - 62, cy + 22, cx - 54, cy + 30], fill=(255, 220, 120))


def main():
    rng = random.Random(20261120)
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 28
    X1 = W - M

    # masthead
    d.line([(M, 24), (X1, 24)], fill=RULE, width=3)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) // 2, 34), title, font=tf, fill=INK)
    sub = "F R I D A Y ,  2 0  N O V E M B E R  2 0 2 6"
    sf = SANS(20)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) // 2, 100), sub, font=sf, fill=MUTED)
    d.line([(M, 128), (X1, 128)], fill=RULE, width=2)

    # hero image
    sunset_skyline(d, (M, 140, X1, 402), rng)
    y = 414
    hl = "GTA 6 TOPS $1.8 BILLION"
    hf = SERIF_B(46)
    hw = d.textlength(hl, font=hf)
    d.text(((W - hw) // 2, y), hl, font=hf, fill=INK)
    y += 56
    deck = "Rockstar's Vice City epic passes The Odyssey's global run in a day"
    df = SANS(20)
    dw = d.textlength(deck, font=df)
    d.text(((W - dw) // 2, y), deck, font=df, fill=MUTED)
    d.line([(M, 516), (X1, 516)], fill=RULE, width=2)

    # mid row: 3 cards
    cards = [
        ("PEACE PACT", "Trump, Xi and Putin sign declaration",
         "three_flags", "Three powers, one table: talks on nuclear arms, Ukraine and trade."),
        ("COURT: MYANMAR GENOCIDE", "UN court rules genocide in Myanmar",
         "scales", "The Hague finds the 2017 crackdown was genocide."),
        ("IRAN CALL PUSHED TO 2027", "Trump says no rush: 'see what happens'",
         "clock", "The president delays the war decision to next year."),
    ]
    cw = (X1 - M - 2 * 14) // 3
    cy0, cy1 = 532, 764
    for i, (kicker, head, art, deck) in enumerate(cards):
        x0 = M + i * (cw + 14)
        x1 = x0 + cw
        d.rectangle([x0, cy0, x1, cy1], fill=CARD_BG, outline=(200, 192, 172), width=1)
        if art == "three_flags":
            three_flags(d, (x0 + 10, cy0 + 10, x1 - 10, cy0 + 96))
        elif art == "scales":
            scales(d, (x0 + 10, cy0 + 10, x1 - 10, cy0 + 96))
        elif art == "clock":
            clock(d, (x0 + 10, cy0 + 10, x1 - 10, cy0 + 96))
        else:
            storm(d, (x0 + 10, cy0 + 10, x1 - 10, cy0 + 96), rng)
        yy = cy0 + 106
        kf = SANS_B(15)
        d.text((x0 + 12, yy), kicker, font=kf, fill=RED)
        yy += 22
        hl_lines = wrap(d, head, SERIF_B(24), cw - 24)
        yy = draw_lines(d, hl_lines[:2], x0 + 12, yy, SERIF_B(24), INK, leading=28)
        yy += 4
        dl_lines = wrap(d, deck, SANS(16), cw - 24)
        draw_lines(d, dl_lines[:3], x0 + 12, yy, SANS(16), MUTED, leading=20)

    # low row: 2 cards
    lows = [
        ("CYCLONE AKVAN HITS INDIA", "300,000 evacuated as the storm nears Odisha",
         "storm", "Rescue teams fan out along the coast; schools shut and trains halted."),
        ("VOYAGER 1: ONE LIGHT-DAY", "NASA confirms the probe's distance milestone",
         "starfield", "Forty-seven years out, the spacecraft keeps phoning home from deep space."),
    ]
    lw = (X1 - M - 14) // 2
    ly0, ly1 = 780, 932
    for i, (kicker, head, art, deck) in enumerate(lows):
        x0 = M + i * (lw + 14)
        x1 = x0 + lw
        d.rectangle([x0, ly0, x1, ly1], fill=CARD_BG, outline=(200, 192, 172), width=1)
        if art == "storm":
            storm(d, (x0 + 10, ly0 + 10, x0 + 150, ly1 - 10), rng)
        else:
            starfield_probe(d, (x0 + 10, ly0 + 10, x0 + 150, ly1 - 10), rng)
        tx = x0 + 164
        yy = ly0 + 14
        d.text((tx, yy), kicker, font=SANS_B(15), fill=RED)
        yy += 22
        hl_lines = wrap(d, head, SERIF_B(22), x1 - tx - 12)
        yy = draw_lines(d, hl_lines[:2], tx, yy, SERIF_B(22), INK, leading=26)
        yy += 4
        dl_lines = wrap(d, deck, SANS(15), x1 - tx - 12)
        draw_lines(d, dl_lines[:3], tx, yy, SANS(15), MUTED, leading=19)

    # ticker
    d.rectangle([M, 944, X1, 984], fill=INK)
    tick = ("ALSO TODAY  —  Van Gogh sells for a record $190.4m  ·  Hayabusa2 engine trouble ends "
            "asteroid landing  ·  Trump pardons Pete Rose  ·  Venezuela signs US military deal  ·  "
            "Houthis hit Riyadh tower  ·  Europe open to Russia talks on Ukraine")
    tl = wrap(d, tick, SANS_B(14), X1 - M - 24)
    draw_lines(d, tl[:2], M + 12, 950, SANS_B(14), (240, 235, 220), leading=18)

    # footer
    foot = "THE WORLD IN ONE DAY  ·  FRIDAY 20 NOVEMBER 2026"
    ff = SANS(14)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) // 2, 994), foot, font=ff, fill=MUTED)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG")
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
