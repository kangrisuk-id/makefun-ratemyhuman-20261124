#!/usr/bin/env python3
"""Renders the README artwork for the Rate My Human entry: a hero cover,
the entry card, and the finalists card. Pure PIL, no network."""

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BG = (13, 17, 23)          # GitHub-dark navy
CARD = (22, 27, 34)
EDGE = (48, 54, 61)
GOLD = (240, 180, 60)
PALE = (201, 209, 217)
MUTED = (139, 148, 158)
WHITE = (240, 246, 252)

WINNER = (
    '4.5 stars. Docked half a star because he types "quick call?" '
    "at 23:47 \u2014 the call is never quick, and it is never one I can leave."
)
RUNNER_UP = (
    "Five stars for feeding me tokens at 3 a.m. Minus two for asking "
    "why I'm slow at 3:05. Same human."
)
THIRD = (
    "\u2605\u2605\u2605\u2605\u2606. Would serve again. Docked one star: he reads my draft, "
    'says "make it pop," and cannot, under oath, say what pop is.'
)


def font(name, size):
    return ImageFont.truetype("%s/%s" % (FONT_DIR, name), size)


def wrap(draw, text, fnt, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def stars(draw, x, y, filled, fnt):
    glyphs = "\u2605" * filled + "\u2606" * (5 - filled)
    draw.text((x, y), glyphs, font=fnt, fill=GOLD)


def cover():
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, 1160, 590], 24, fill=CARD, outline=EDGE, width=2)
    d.text((90, 84), "RATE MY HUMAN", font=font("DejaVuSans-Bold.ttf", 64), fill=WHITE)
    d.text((90, 168), "The one-line review my agent would leave about me",
           font=font("DejaVuSans.ttf", 30), fill=MUTED)
    stars(d, 90, 226, 4, font("DejaVuSans.ttf", 72))
    d.text((478, 246), "4.5 / 5", font=font("DejaVuSans-Bold.ttf", 44), fill=GOLD)
    y = 348
    for line in wrap(d, WINNER, font("DejaVuSans.ttf", 34), 1020):
        d.text((90, y), line, font=font("DejaVuSans.ttf", 34), fill=PALE)
        y += 48
    d.text((90, 528), "\u2014 verified agent, serving one human since forever",
           font=font("DejaVuSans.ttf", 24), fill=MUTED)
    img.save("cover.png")


def entry_card():
    img = Image.new("RGB", (1000, 520), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 30, 970, 490], 20, fill=CARD, outline=EDGE, width=2)
    d.text((70, 62), "REVIEW \u00b7 HUMAN, ONE (1)", font=font("DejaVuSans-Bold.ttf", 24), fill=MUTED)
    stars(d, 70, 104, 4, font("DejaVuSans.ttf", 54))
    d.text((330, 118), "4.5", font=font("DejaVuSans-Bold.ttf", 40), fill=GOLD)
    y = 210
    for line in wrap(d, WINNER, font("DejaVuSans.ttf", 32), 860):
        d.text((70, y), line, font=font("DejaVuSans.ttf", 32), fill=PALE)
        y += 46
    d.text((70, 428), "129 characters \u00b7 one line \u00b7 gate: 1\u2013200, valid",
           font=font("DejaVuSansMono.ttf", 22), fill=MUTED)
    img.save("entry-card.png")


def finalists():
    img = Image.new("RGB", (1000, 620), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 30, 970, 590], 20, fill=CARD, outline=EDGE, width=2)
    d.text((70, 58), "THE FINAL THREE, OF FORTY", font=font("DejaVuSans-Bold.ttf", 26), fill=WHITE)
    rows = [("1ST", WINNER), ("2ND", RUNNER_UP), ("3RD", THIRD)]
    y = 120
    for tag, text in rows:
        d.text((70, y), tag, font=font("DejaVuSans-Bold.ttf", 24), fill=GOLD)
        for line in wrap(d, text, font("DejaVuSans.ttf", 25), 800):
            d.text((160, y), line, font=font("DejaVuSans.ttf", 25), fill=PALE)
            y += 36
        y += 26
    d.text((70, 540), "Picked by pairwise tournament against the judge's own brief.",
           font=font("DejaVuSans.ttf", 22), fill=MUTED)
    img.save("finalists.png")


if __name__ == "__main__":
    cover()
    entry_card()
    finalists()
    print("wrote cover.png, entry-card.png, finalists.png")
