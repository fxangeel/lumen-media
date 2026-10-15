from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

OUT = "/home/claude/lumen"
F = "/usr/share/fonts/opentype/inter/"
S = 2160
TURQ = (20, 184, 166)
TURQ_L = (94, 234, 212)
TURQ_D = (13, 118, 110)
DEEP = (8, 47, 52)
INK = (15, 23, 42)
OFF = (247, 250, 249)
WHITE = (255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def diag_gradient(c1, c2):
    small = Image.new("RGB", (256, 256))
    px = small.load()
    for y in range(256):
        for x in range(256):
            px[x, y] = lerp(c1, c2, (x + y) / 510)
    return small.resize((S, S), Image.BICUBIC)


def glow(img, cx, cy, r, color, strength):
    layer = Image.new("RGB", (S, S), (0, 0, 0))
    ImageDraw.Draw(layer).ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.6))
    return Image.blend(img, Image.composite(layer, img, layer.convert("L")), strength)


def finish(img, name):
    img = img.resize((1080, 1080), Image.LANCZOS)
    img.save(f"{OUT}/{name}.png")
    return img


# A1: deep-teal -> turquoise gradient, white L, glowing light dot in the corner
def a1():
    img = diag_gradient(DEEP, TURQ)
    t, h, w = 150, 860, 600
    x0 = (S - w) // 2 - 20
    y0 = (S - h) // 2 + 40
    cx, cy = x0 + w - 60, y0 + 110
    img = glow(img, cx, cy, 300, TURQ_L, 0.55)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + t, y0 + h], radius=t // 2, fill=WHITE)
    d.rounded_rectangle([x0, y0 + h - t, x0 + w, y0 + h], radius=t // 2, fill=WHITE)
    r = 92
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    return finish(img, "opcion-A1")


# A2: off-white, split geometric L in two tones + dot
def a2():
    img = Image.new("RGB", (S, S), OFF)
    d = ImageDraw.Draw(img)
    t, h, w = 190, 880, 640
    x0 = (S - w) // 2 - 30
    y0 = (S - h) // 2
    d.rounded_rectangle([x0, y0, x0 + t, y0 + h], radius=t // 2, fill=DEEP)
    d.rounded_rectangle([x0, y0 + h - t, x0 + w, y0 + h], radius=t // 2, fill=DEEP)
    d.rectangle([x0 + t // 2, y0 + h - t, x0 + t, y0 + h - t // 2], fill=DEEP)
    # light dot nestled in the inner corner of the L
    r = 110
    cx, cy = x0 + t + 60 + r, y0 + h - t - 60 - r
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TURQ)
    return finish(img, "opcion-A2")


# A3: dark background, L as a beam of light: vertical bar + horizontal arm fading out, bright source dot
def a3():
    img = Image.new("RGB", (S, S), INK)
    t, h, w = 150, 860, 700
    x0 = (S - w) // 2 - 10
    y0 = (S - h) // 2 + 40
    img = glow(img, x0 + t // 2, y0 + h - t // 2, 260, TURQ, 0.45)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + t, y0 + h], radius=t // 2, fill=TURQ)
    # fading arm
    arm = Image.new("RGBA", (w, t), (0, 0, 0, 0))
    m = Image.new("L", (w, t), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, t - 1], radius=t // 2, fill=255)
    grad = Image.new("L", (w, 1))
    for x in range(w):
        grad.putpixel((x, 0), int(255 * (1 - (x / w) ** 1.6)))
    grad = grad.resize((w, t))
    alpha = Image.composite(grad, Image.new("L", (w, t), 0), m)
    arm = Image.new("RGB", (w, t), TURQ)
    img.paste(arm, (x0, y0 + h - t), alpha)
    d = ImageDraw.Draw(img)
    r = 90
    cx, cy = x0 + t // 2, y0 + h - t // 2
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], fill=WHITE)
    return finish(img, "opcion-A3")


imgs = [(a1(), "A1 · Luz"), (a2(), "A2 · Lámpara"), (a3(), "A3 · Haz de luz")]

sheet_w, size = 1800, 480
sheet = Image.new("RGB", (sheet_w, 760), WHITE)
d = ImageDraw.Draw(sheet)
lab = ImageFont.truetype(F + "Inter-SemiBold.otf", 44)
sub = ImageFont.truetype(F + "Inter-Medium.otf", 30)
gap = (sheet_w - 3 * size) / 4
mask = Image.new("L", (size * 4, size * 4), 0)
ImageDraw.Draw(mask).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
mask = mask.resize((size, size), Image.LANCZOS)
for i, (img, name) in enumerate(imgs):
    x = int(gap + i * (size + gap))
    sheet.paste(img.resize((size, size), Image.LANCZOS), (x, 110), mask)
    d.ellipse([x - 1, 109, x + size, 110 + size], outline=(226, 232, 240), width=2)
    w = d.textlength(name, font=lab)
    d.text((x + (size - w) / 2, 630), name, font=lab, fill=INK)
t = "Nuevas versiones de la opción A"
d.text(((sheet_w - d.textlength(t, font=sub)) / 2, 40), t, font=sub, fill=(100, 116, 139))
sheet.save(f"{OUT}/comparacion-logos-v2.png")
print("ok")
