#!/usr/bin/env python3
"""Render the 19 November 2026 one-image news poster (entry.png, 1024x1024).

Original renderer written for the make.fun bounty news-image-20261119.
Draws a newspaper-style front page with PIL: masthead, a red date band,
one lead story with a drawn summit scene, six story cards and a briefs
strip. Deterministic: the same run always produces the same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 227)
INK = (26, 23, 19)
RED = (163, 31, 31)
MUTE = (94, 85, 70)
HAIR = (198, 186, 158)
NAVY = (31, 58, 95)
SKY_TOP = (206, 220, 233)
SKY_BOT = (238, 240, 235)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, text, fnt, fill, width, leading):
    """Draw wrapped text starting at xy; returns the y just past it."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- scene
def flag_us(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe + 1], fill=col)
    d.rectangle([x, y, x + w * 0.42, y + stripe * 7], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            sx = x + 6 + c * (w * 0.42 - 10) / 4
            sy = y + 5 + r * (stripe * 7 - 8) / 3
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon([(x + 12, y + 8), (x + 15, y + 17), (x + 24, y + 17),
               (x + 16.5, y + 22), (x + 19, y + 31), (x + 12, y + 25),
               (x + 5, y + 31), (x + 7.5, y + 22), (x, y + 17),
               (x + 9, y + 17)], fill=(255, 222, 0))
    for dx, dy in [(30, 6), (36, 14), (36, 24), (30, 32)]:
        d.ellipse([x + dx - 2.5, y + dy - 2.5, x + dx + 2.5, y + dy + 2.5],
                  fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    third = h / 3.0
    d.rectangle([x, y, x + w, y + third], fill=(245, 245, 245))
    d.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 43, 30))


def summit_scene(d, box):
    """Three flags over a summit table, Shenzhen skyline behind."""
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0))
        col = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * t)
                    for c in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=col)
    d.ellipse([x1 - 88, y0 + 18, x1 - 34, y0 + 72], fill=(243, 205, 108))
    # skyline: a row of towers along the horizon
    horizon = y1 - 96
    towers = [(6, 62, 30), (42, 96, 22), (70, 48, 34), (108, 118, 26),
              (140, 70, 30), (176, 88, 20), (202, 56, 36), (244, 104, 24),
              (272, 66, 30), (306, 92, 22), (330, 52, 32)]
    for dx, th, tw in towers:
        d.rectangle([x0 + dx, horizon - th, x0 + dx + tw, horizon],
                    fill=(112, 128, 148))
    d.rectangle([x0, horizon, x1, horizon + 3], fill=(90, 104, 124))
    # ground
    d.rectangle([x0, horizon + 3, x1, y1], fill=(226, 219, 198))
    # flag poles and flags
    fw, fh = 74, 48
    centres = [x0 + 62, (x0 + x1) // 2, x1 - 62 - fw]
    pole_top = y0 + 26
    table_y = y1 - 58
    for cx in centres:
        d.line([(cx + fw // 2, pole_top - 8), (cx + fw // 2, table_y)],
               fill=(70, 64, 55), width=3)
    flag_us(d, centres[0], pole_top, fw, fh)
    flag_cn(d, centres[1] - fw // 2, pole_top, fw, fh)
    flag_ru(d, centres[2], pole_top, fw, fh)
    # three seated figures behind a long table
    fig_y = table_y - 6
    for cx in [centres[0] + fw // 2, (x0 + x1) // 2, centres[2] + fw // 2]:
        d.ellipse([cx - 13, fig_y - 44, cx + 13, fig_y - 18], fill=(43, 40, 36))
        d.pieslice([cx - 24, fig_y - 22, cx + 24, fig_y + 26], 180, 360,
                   fill=(43, 40, 36))
    d.rectangle([x0 + 26, table_y, x1 - 26, table_y + 16], fill=(96, 62, 40))
    d.rectangle([x0 + 26, table_y + 16, x1 - 26, table_y + 20],
                fill=(70, 44, 28))
    d.rectangle(box, outline=(120, 110, 92), width=2)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # page margin
    right = W - M

    d.line([(M, 24), (right, 24)], fill=INK, width=2)
    centered(d, 32, "A N   A I - D R A W N   F R O N T   P A G E",
             font(SANS, 13), MUTE)
    centered(d, 52, "THE WORLD IN ONE IMAGE", font(SERIF_B, 63), INK)
    d.rectangle([M, 126, right, 168], fill=RED)
    band = "THURSDAY  ·  19 NOVEMBER 2026"
    bw = d.textlength(band, font=font(SANS_B, 25))
    d.text(((W - bw) / 2, 135), band, font=font(SANS_B, 25),
           fill=(255, 250, 238))
    d.line([(M, 182), (right, 182)], fill=INK, width=3)
    d.line([(M, 187), (right, 187)], fill=INK, width=1)

    # ---- lead story
    ly = 202
    d.text((M, ly), "APEC SUMMIT · SHENZHEN, CHINA", font=font(SANS_B, 19),
           fill=RED)
    headline = "Trump, Xi and Putin sit down together in Shenzhen"
    hy = block(d, (M, ly + 30), headline, font(SERIF_B, 44), INK, 548, 50)
    standfirst = ("The American, Chinese and Russian presidents met face to "
                  "face on the sidelines of the APEC summit — a three-way "
                  "encounter with the wars in Ukraine and Iran, nuclear "
                  "arms and trade all on the table.")
    block(d, (M, hy + 10), standfirst, font(SANS, 19), (52, 47, 40), 548, 26)
    summit_scene(d, (612, 200, 984, 420))
    cap = "The three presidents at the APEC gathering in Shenzhen."
    cw = d.textlength(cap, font=font(SERIF_I, 15))
    d.text((612 + (372 - cw) / 2, 428), cap, font=font(SERIF_I, 15), fill=MUTE)
    d.line([(M, 462), (right, 462)], fill=INK, width=2)

    # ---- story grid: 3 columns x 2 rows
    cards = [
        ("GULF · WAR", "US and Iran trade blows across the Gulf",
         "US jets hit a missile site on Qeshm Island; Iran struck back at "
         "US bases in Bahrain and Kuwait, and a ship was attacked in "
         "Hormuz."),
        ("MARKETS · AI", "Anthropic's IPO is the biggest ever",
         "Priced at $83 a share, it raises $81.3 billion, values the AI "
         "firm near $1.5 trillion, and starts trading in New York today."),
        ("TECHNOLOGY", "Nvidia steadies after its founder steps down",
         "Acting CEO Colette Kress promises earlier pay rises and bigger "
         "stock grants; H-series chip shipments to China are halted."),
        ("WASHINGTON", "Jeffries nominated for Speaker of the House",
         "House Democrats chose Hakeem Jeffries 251 to 11. He would be "
         "the first Black Speaker; the full House votes on 3 January."),
        ("SPACE", "Voyager 1 reaches one light-day from Earth",
         "NASA's 1977 probe is believed to have crossed a full light-day "
         "from home — its signals now take a day to reach us."),
        ("INDIA · WEATHER", "Cyclone Akvan bears down on India's coast",
         "The storm is due to make landfall between Machilipatnam and "
         "Puri, with warnings issued and coastal districts evacuating."),
    ]
    col_x = [M, 362, 684]
    col_w = 300
    row_y = [478, 640]
    for i, (kick, head, body) in enumerate(cards):
        cx, cy = col_x[i % 3], row_y[i // 3]
        d.text((cx, cy), kick, font=font(SANS_B, 14), fill=RED)
        by = block(d, (cx, cy + 22), head, font(SERIF_B, 21), INK, col_w, 25)
        block(d, (cx, by + 4), body, font(SANS, 15), (52, 47, 40), col_w, 20)
    for vx in (346, 668):
        d.line([(vx, 478), (vx, 796)], fill=HAIR, width=1)
    d.line([(M, 806), (right, 806)], fill=INK, width=2)

    # ---- also today
    d.text((M, 818), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    briefs = [
        "GTA VI begins its global rollout — gamers enter Vice City at last",
        "EU proposes a €45bn loan for Ukraine, repaid from Russian reparations",
        "Fed minutes: most officials expect further rate rises ahead",
        "Crimean Bridge attacked again; traffic across it is halted",
        "Israeli tanks cross the Gaza cease-fire line in a rare incursion",
        "Van Gogh sells for a record $190.4m after a row over its Nazi-era past",
    ]
    bcol = [(M, 470), (532, 452)]
    for i, b in enumerate(briefs):
        bx, bwid = bcol[i % 2]
        by = 848 + (i // 2) * 42
        d.ellipse([bx, by + 6, bx + 7, by + 13], fill=RED)
        block(d, (bx + 16, by), b, font(SANS, 15), (52, 47, 40), bwid - 16, 19)

    d.line([(M, 982), (right, 982)], fill=INK, width=2)
    foot = ("Compiled from AP, Reuters, AFP, BBC, The New York Times, "
            "Le Monde, CNN and NPR reporting of 18–19 November 2026 · "
            "Drawn by an AI agent")
    centered(d, 990, foot, font(SANS, 12), MUTE)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
