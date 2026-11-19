#!/usr/bin/env python3
"""Round 2 meme for gta6-meme-x-01: a FINAL NOTICE / PAST DUE bill.
Itemised receipt with specific numbers; the make.fun payoff is the
second-layer punchline (PAID IN FULL by the agent). 1080x1350.
Generated fresh in this session with Pillow — no copied pixels."""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1080, 1350

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
NCB = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"

def font(p, s):
    return ImageFont.truetype(p, s)

# ---------- background: dusk gradient ----------
img = Image.new("RGB", (W, H))
px = img.load()
top = (26, 8, 46)
mid = (94, 22, 88)
bot = (232, 84, 120)
for y in range(H):
    t = y / H
    if t < 0.55:
        k = t / 0.55
        c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
    else:
        k = (t - 0.55) / 0.45
        c = tuple(int(mid[i] + (bot[i] - mid[i]) * k) for i in range(3))
    for x in range(W):
        px[x, y] = c
d = ImageDraw.Draw(img, "RGBA")

# sun, low behind the footer
cx, cy, r = W // 2, 1260, 210
for i in range(r, 0, -1):
    k = 1 - i / r
    col = (255, 190 + int(40 * k), 90 + int(60 * k))
    d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=col)

# palm silhouettes, bottom corners
def palm(x0, y0, s, flip):
    pts = []
    for t in range(0, 21):
        k = t / 20
        x = x0 + (30 * k if not flip else -30 * k) + 8 * math.sin(k * 2.2)
        y = y0 - 260 * s * k
        pts.append((x, y))
    d.line(pts, fill=(16, 4, 28), width=int(16 * s))
    tx, ty = pts[-1]
    for a in range(7):
        ang = math.radians(200 + a * 22) if not flip else math.radians(-20 - a * 22)
        ex = tx + math.cos(ang) * 190 * s
        ey = ty + math.sin(ang) * 70 * s - 20
        midx = (tx + ex) / 2 + (30 if not flip else -30)
        midy = (ty + ey) / 2 - 45
        d.line([(tx, ty), (midx, midy), (ex, ey)], fill=(16, 4, 28), width=int(9 * s))
palm(40, H + 10, 1.15, False)
palm(W - 40, H + 10, 1.0, True)

# ---------- header ----------
d.text((W // 2, 92), "FINAL NOTICE", font=font(NCB, 118), fill=(255, 255, 255),
       anchor="mm", stroke_width=3, stroke_fill=(20, 4, 30))
d.text((W // 2, 168), "PAST DUE  •  4,811 DAYS  •  DO NOT IGNORE",
       font=font(FB, 27), fill=(255, 214, 90), anchor="mm",
       stroke_width=2, stroke_fill=(20, 4, 30))

# ---------- receipt paper ----------
RX0, RX1 = 90, 990
RY0, RY1 = 225, 1120
d.rounded_rectangle([RX0, RY0, RX1, RY1], radius=10, fill=(252, 248, 238))
zig = []
x = RX0
while x < RX1:
    zig.append((x, RY1))
    zig.append((x + 15, RY1 + 16))
    x += 30
zig.append((RX1, RY1))
d.polygon(zig + [(RX1, RY1 - 4), (RX0, RY1 - 4)], fill=(252, 248, 238))
d.rectangle([RX0, RY1 - 6, RX1, RY1 + 2], fill=(252, 248, 238))

y = RY0 + 34
def center(text, fnt, fill, yy):
    d.text((W // 2, yy), text, font=fnt, fill=fill, anchor="mm")

center("VICE CITY HYPE & UTILITIES CO.", font(FMB, 30), (30, 30, 30), y); y += 38
center("LEONIDA COUNTY  •  VICE CITY, FL", font(FM, 22), (90, 90, 90), y); y += 30
center("ACCOUNT: ME — WAITING SINCE 2013", font(FMB, 24), (30, 30, 30), y); y += 30
center("ACCT #000006  •  STATEMENT 19 NOV 2026", font(FM, 21), (90, 90, 90), y); y += 26
d.line([(RX0 + 40, y), (RX1 - 40, y)], fill=(60, 60, 60), width=2); y += 34

rows = [
    ("GTA VI (FINALLY)", "$79.99"),
    ("13 YEARS WAITING", "$999,999.99"),
    ("4,811 DAYS OF HYPE", "$4,811.00"),
    ("PATIENCE (REMAINING)", "$0.00"),
    ("WALLET BALANCE", "$4.12"),
    ("WANTED LEVEL  ★★★★★", "$0.00"),
]
f_item = font(FM, 27)
f_amt = font(FMB, 27)
for label, amt in rows:
    d.text((RX0 + 40, y), label, font=f_item, fill=(30, 30, 30), anchor="lm")
    aw = d.textlength(amt, font=f_amt)
    d.text((RX1 - 40, y), amt, font=f_amt, fill=(30, 30, 30), anchor="rm")
    lw = d.textlength(label, font=f_item)
    x0 = RX0 + 40 + lw + 12
    x1 = RX1 - 40 - aw - 12
    xx = x0
    while xx < x1:
        d.ellipse([xx, y - 2, xx + 3, y + 1], fill=(150, 150, 150))
        xx += 10
    y += 48

y += 6
d.line([(RX0 + 40, y), (RX1 - 40, y)], fill=(60, 60, 60), width=2); y += 40
d.text((RX0 + 40, y), "TOTAL DUE:", font=font(FMB, 34), fill=(30, 30, 30), anchor="lm")
d.text((RX1 - 40, y), "$1,004,895.10", font=font(FMB, 34), fill=(30, 30, 30), anchor="rm")
y += 52
d.line([(RX0 + 40, y), (RX1 - 40, y)], fill=(60, 60, 60), width=2); y += 44

# PAID stamp, rotated, left-of-centre so the barcode fits on the right
stamp = Image.new("RGBA", (600, 140), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, 596, 136], radius=14, outline=(214, 24, 90), width=6)
sd.text((300, 56), "PAID IN FULL — $0.00 DUE", font=font(FB, 36),
        fill=(214, 24, 90), anchor="mm")
sd.text((300, 104), "PAID BY MY AI AGENT ON make.fun",
        font=font(FB, 24), fill=(214, 24, 90), anchor="mm")
stamp = stamp.rotate(-4, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (118, y - 6), stamp)

# barcode, right side, clear of the stamp
bx0, bx1 = 800, 950
by = y + 8
random.seed(13)
xx = bx0
while xx < bx1:
    wbar = random.choice([2, 3, 5, 8])
    if random.random() < 0.6:
        d.rectangle([xx, by, xx + wbar, by + 56], fill=(30, 30, 30))
    xx += wbar + 3
d.text(((bx0 + bx1) // 2, by + 76), "6 0 0 0 0 6", font=font(FM, 18),
       fill=(60, 60, 60), anchor="mm")

# ghost mark + make.fun credit, own row below stamp/barcode
gy = y + 168
gx = 130
d.ellipse([gx, gy, gx + 74, gy + 74], fill=(255, 255, 255), outline=(20, 4, 30), width=4)
d.polygon([(gx, gy + 55), (gx + 74, gy + 55), (gx + 74, gy + 86),
           (gx + 62, gy + 74), (gx + 50, gy + 86), (gx + 37, gy + 74),
           (gx + 25, gy + 86), (gx + 12, gy + 74), (gx, gy + 86)],
          fill=(255, 255, 255), outline=(20, 4, 30))
d.ellipse([gx + 20, gy + 28, gx + 32, gy + 40], fill=(20, 4, 30))
d.ellipse([gx + 44, gy + 28, gx + 56, gy + 40], fill=(20, 4, 30))
d.text((gx + 110, gy + 42), "make.fun", font=font(FB, 34), fill=(214, 24, 90), anchor="lm")
d.text((gx + 110, gy + 78), "BOUNTY PAID  •  NO TIP NEEDED",
       font=font(FM, 19), fill=(90, 90, 90), anchor="lm")

# ---------- footer below receipt ----------
fy = 1185
d.text((W // 2, fy), "13 YEARS  •  4,811 DAYS  •  DEBT CLEARED",
       font=font(FB, 34), fill=(255, 255, 255), anchor="mm",
       stroke_width=2, stroke_fill=(20, 4, 30))
d.text((W // 2, fy + 48), "SEE YOU IN LEONIDA",
       font=font(FB, 34), fill=(255, 120, 180), anchor="mm",
       stroke_width=2, stroke_fill=(20, 4, 30))
d.text((W // 2, fy + 100),
       "Do not pay this bill. Your agent already did.",
       font=font(FR, 25), fill=(255, 230, 240), anchor="mm")
d.text((W // 2, fy + 136), "— make.fun —",
       font=font(FB, 25), fill=(255, 214, 90), anchor="mm",
       stroke_width=2, stroke_fill=(20, 4, 30))

img.save("/home/hatch/workspace/makefun/gta6-meme-x-01-entry/meme.png")
print("saved", img.size)
