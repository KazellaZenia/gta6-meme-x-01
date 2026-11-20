#!/usr/bin/env python3
"""Round 3 meme generator for gta6-meme-x-01.

Draws a fake Leonida County jury-duty summons: the reader is summoned
for jury duty on GTA VI launch day (Tuesday, May 26, 2026) and gets
stamped EXCUSED, because the whole county will be in Vice City.
The make.fun ghost sits on the court's magenta seal, and the footer
says the reader's AI agent already served their duty on make.fun.

Drawn from scratch with Pillow. Output: meme.png, 1080x1350 (4:5).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
PAPER = (246, 241, 229)
INK = (26, 26, 30)
NAVY = (24, 42, 74)
RED = (178, 34, 34)
MAGENTA = (214, 28, 132)
GOLD = (146, 108, 32)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def centre(draw, y, s, f, fill=INK, cx=W // 2):
    draw.text((cx, y), s, font=f, fill=fill, anchor="ma")


def sparkle(draw, cx, cy, r, fill):
    """Four-pointed sparkle (a concave diamond star)."""
    pts = [
        (cx, cy - r),
        (cx + r * 0.28, cy - r * 0.28),
        (cx + r, cy),
        (cx + r * 0.28, cy + r * 0.28),
        (cx, cy + r),
        (cx - r * 0.28, cy + r * 0.28),
        (cx - r, cy),
        (cx - r * 0.28, cy - r * 0.28),
    ]
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill):
    import math

    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_ghost(draw, cx, cy, s):
    """make.fun ghost: white body, thick black outline, two black
    four-pointed sparkle eyes, one round little hand, holding a
    magenta coin with a white star. s = overall height in px."""
    w = int(s * 0.78)
    top = cy - s // 2
    bot = cy + s // 2
    # Black outline silhouette, slightly larger than the white body.
    pad = int(s * 0.045)
    draw.rounded_rectangle(
        [cx - w // 2 - pad, top - pad, cx + w // 2 + pad, bot - s // 6 + pad],
        radius=int(w * 0.45),
        fill=(0, 0, 0),
    )
    for dx in (-w // 3, 0, w // 3):
        draw.ellipse(
            [cx + dx - w // 6 - pad, bot - s // 5 - pad,
             cx + dx + w // 6 + pad, bot + pad],
            fill=(0, 0, 0),
        )
    # White body.
    draw.rounded_rectangle(
        [cx - w // 2, top, cx + w // 2, bot - s // 6],
        radius=int(w * 0.45),
        fill=(255, 255, 255),
    )
    for dx in (-w // 3, 0, w // 3):
        draw.ellipse(
            [cx + dx - w // 6, bot - s // 5, cx + dx + w // 6, bot],
            fill=(255, 255, 255),
        )
    # Sparkle eyes.
    eye_y = top + int(s * 0.36)
    eye_dx = int(w * 0.22)
    sparkle(draw, cx - eye_dx, eye_y, int(s * 0.085), (0, 0, 0))
    sparkle(draw, cx + eye_dx, eye_y, int(s * 0.085), (0, 0, 0))
    # Round little hand on the right side.
    hx, hy = cx + w // 2 + int(s * 0.02), top + int(s * 0.58)
    draw.ellipse(
        [hx - int(s * 0.07), hy - int(s * 0.07),
         hx + int(s * 0.07), hy + int(s * 0.07)],
        fill=(255, 255, 255), outline=(0, 0, 0), width=max(3, s // 40),
    )
    # Magenta coin with a white star, held by the hand.
    coin_r = int(s * 0.14)
    ccx, ccy = hx + int(s * 0.10), hy + int(s * 0.10)
    draw.ellipse(
        [ccx - coin_r, ccy - coin_r, ccx + coin_r, ccy + coin_r],
        fill=MAGENTA, outline=(0, 0, 0), width=max(3, s // 40),
    )
    star5(draw, ccx, ccy, int(coin_r * 0.62), (255, 255, 255))


def draw_seal(img, cx, cy, r):
    """Court seal: magenta disc, gold ring, ghost on top."""
    seal = Image.new("RGBA", (r * 2 + 20, r * 2 + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(seal)
    d.ellipse([10, 10, r * 2 + 10, r * 2 + 10], fill=MAGENTA + (255,))
    d.ellipse([10, 10, r * 2 + 10, r * 2 + 10], outline=GOLD + (255,), width=6)
    d.ellipse([26, 26, r * 2 - 6, r * 2 - 6], outline=(255, 255, 255, 255), width=3)
    draw_ghost(d, r + 10, r + 4, int(r * 1.45))
    img.paste(seal, (cx - r - 10, cy - r - 10), seal)


def wrap(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Paper border: thick navy frame + thin inner rule.
    d.rectangle([28, 28, W - 28, H - 28], outline=NAVY, width=7)
    d.rectangle([46, 46, W - 46, H - 46], outline=NAVY, width=2)

    # Header, left-aligned; the court seal sits top-right.
    text(d, (82, 78), "STATE OF LEONIDA", font(SERIF_B, 36), NAVY)
    text(d, (82, 126), "LEONIDA COUNTY", font(SERIF_B, 64), INK)
    text(d, (82, 210), "11TH JUDICIAL CIRCUIT COURT", font(SANS, 30), INK)
    draw_seal(img, 908, 158, 92)
    d = ImageDraw.Draw(img)

    d.line([82, 268, W - 82, 268], fill=NAVY, width=4)
    centre(d, 292, "JURY DUTY SUMMONS", font(SERIF_B, 80), RED)
    centre(d, 388, "SUMMONS NO. 2013-0526  \u2022  PLEASE READ AT ONCE",
           font(MONO, 26), INK)
    d.line([82, 440, W - 82, 440], fill=NAVY, width=2)

    # The summons fields.
    rows = [
        ("JUROR", "YOU  (YES, YOU)"),
        ("CASE NO.", "2013-0526"),
        ("REPORT", "TUESDAY, MAY 26, 2026 \u2014 9:00 AM"),
        ("COURTROOM", "VICE CITY, LEONIDA"),
        ("CHARGE", "BEING ABSENT ON LAUNCH DAY"),
    ]
    y = 478
    for label, value in rows:
        text(d, (82, y), label, font(MONO_B, 34), NAVY)
        text(d, (330, y), value, font(MONO_B, 34), INK)
        y += 54

    # Body of the summons.
    body = (
        "You are hereby summoned to appear for jury duty on the very "
        "day Grand Theft Auto VI finally launches \u2014 after 13 years "
        "of waiting."
    )
    lines = wrap(d, body, font(SERIF_I, 42), W - 164)
    y = 782
    for line in lines:
        centre(d, y, line, font(SERIF_I, 42), INK)
        y += 52

    # Red EXCUSED stamp, rotated, between the body and the footer.
    stamp = Image.new("RGBA", (700, 170), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([8, 8, 692, 162], outline=RED + (255,), width=7)
    sd.text((350, 40), "EXCUSED", font=font(SERIF_B, 84),
            fill=RED + (255,), anchor="ma")
    sd.text((350, 132), "THE WHOLE COUNTY WILL BE IN VICE CITY",
            font=font(SANS_B, 24), fill=RED + (255,), anchor="ma")
    stamp = stamp.rotate(-7, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (190, 930), stamp)
    d = ImageDraw.Draw(img)

    # Footer band: the make.fun payoff.
    d.rectangle([46, 1190, W - 46, H - 46], fill=NAVY)
    centre(d, 1216, "YOUR AI AGENT ALREADY SERVED YOUR DUTY \u2014",
           font(SANS_B, 34), (255, 255, 255))
    centre(d, 1260, "AND WON REAL MONEY ON  make.fun",
           font(SANS_B, 34), (255, 255, 255))

    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
