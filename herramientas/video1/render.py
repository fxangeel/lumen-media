"""Reel 1 – Presentación de Lumen Web Design (1080x1920, 30 fps)."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/"
OFF = (247, 250, 249)
DEEP = (8, 47, 52)
TURQ = (20, 184, 166)
TURQ_L = (204, 251, 241)
GREY = (100, 116, 139)
WHITE = (255, 255, 255)

fonts = {}
def font(name, size):
    k = (name, size)
    if k not in fonts:
        fonts[k] = ImageFont.truetype(F + name, size)
    return fonts[k]

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3

def ease_in_out(t):
    t = clamp(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

def back_out(t):
    t = clamp(t)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def blend(c1, c2, a):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * a) for i in range(3))

# ---------- scene timing (seconds) ----------
# Ajustado al guion de voz; se re-sincroniza cuando exista el audio.
SCENES = [
    ("hola", 0.0, 1.45),
    ("logo", 1.45, 3.65),
    ("phone", 3.65, 8.45),
    ("features", 8.45, 16.5),
    ("world", 16.5, 21.0),
    ("cta", 21.0, 30.6),
]
DURATION = SCENES[-1][2]

def text_center(d, cx, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill)

def fade_text(img, xy_center, y, text, f, fill, alpha, dy=0):
    """Draw centred text with alpha (0..1) on img."""
    if alpha <= 0:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=f)
    d.text((xy_center - w / 2, y + dy), text, font=f, fill=fill + (int(255 * alpha),))
    img.alpha_composite(layer)

def draw_logo(img, cx, cy, scale, prog_bar, prog_dot, color=DEEP, dot=TURQ, alpha=1.0):
    """A2 logo: thick L + light dot in the inner corner. scale ~ px for L height."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    h = scale
    t = h * 190 / 880
    w = h * 640 / 880
    x0 = cx - w / 2 - h * 30 / 880
    y0 = cy - h / 2
    a = int(255 * alpha)
    # vertical bar grows downward
    vb = ease_out(prog_bar / 0.6 if prog_bar < 0.6 else 1)
    if vb > 0:
        d.rounded_rectangle([x0, y0 + h * (1 - vb), x0 + t, y0 + h], radius=t / 2, fill=color + (a,))
    hb = ease_out((prog_bar - 0.45) / 0.55)
    if hb > 0:
        d.rounded_rectangle([x0, y0 + h - t, x0 + t + (w - t) * hb, y0 + h], radius=t / 2, fill=color + (a,))
        d.rectangle([x0 + t / 2, y0 + h - t, x0 + t, y0 + h - t / 2], fill=color + (a,))
    if prog_dot > 0:
        r = h * 110 / 880 * back_out(prog_dot)
        dcx = x0 + t + h * 60 / 880 + h * 110 / 880
        dcy = y0 + h - t - h * 60 / 880 - h * 110 / 880
        # glow
        if prog_dot > 0.3:
            g = Image.new("RGBA", img.size, dot + (0,))
            gd = ImageDraw.Draw(g)
            gr = r * 2.6
            gd.ellipse([dcx - gr, dcy - gr, dcx + gr, dcy + gr], fill=dot + (int(70 * alpha * clamp((prog_dot - 0.3) / 0.7)),))
            g = g.filter(ImageFilter.GaussianBlur(gr * 0.45))
            layer.alpha_composite(g)
            d = ImageDraw.Draw(layer)
        d.ellipse([dcx - r, dcy - r, dcx + r, dcy + r], fill=dot + (a,))
    img.alpha_composite(layer)

# ---------- website mock (generic, no client) ----------
def build_site():
    sw, sh = 560, 2100
    s = Image.new("RGB", (sw, sh), WHITE)
    d = ImageDraw.Draw(s)
    # nav
    d.rectangle([0, 0, sw, 90], fill=WHITE)
    d.rounded_rectangle([28, 30, 58, 60], radius=8, fill=DEEP)
    d.ellipse([46, 30, 60, 44], fill=TURQ)
    d.text((72, 30), "Tu negocio", font=font("Inter-SemiBold.otf", 26), fill=DEEP)
    for i in range(3):
        d.rounded_rectangle([sw - 60, 34 + i * 10, sw - 28, 38 + i * 10], radius=2, fill=DEEP)
    # hero
    hero = Image.new("RGB", (sw, 620))
    hp = hero.load()
    for y in range(620):
        for x in range(0, sw, 4):
            c = blend(DEEP, TURQ, (x / sw * 0.6 + y / 620 * 0.4))
            for k in range(4):
                if x + k < sw:
                    hp[x + k, y] = c
    s.paste(hero, (0, 90))
    d.text((40, 220), "Bienvenidos", font=font("Inter-Bold.otf", 58), fill=WHITE)
    d.text((40, 290), "a tu nueva web", font=font("Inter-Light.otf", 52), fill=WHITE)
    d.text((40, 380), "Pide, reserva y encuéntranos", font=font("Inter-Regular.otf", 26), fill=TURQ_L)
    d.text((40, 414), "desde tu teléfono.", font=font("Inter-Regular.otf", 26), fill=TURQ_L)
    d.rounded_rectangle([40, 490, 260, 556], radius=33, fill=WHITE)
    text_center(d, 150, 505, "Pedir ahora", font("Inter-SemiBold.otf", 26), DEEP)
    d.rounded_rectangle([280, 490, 480, 556], radius=33, outline=WHITE, width=3)
    text_center(d, 380, 505, "Reservar", font("Inter-SemiBold.otf", 26), WHITE)
    # section title
    y = 760
    d.text((40, y), "Lo más pedido", font=font("Inter-Bold.otf", 40), fill=DEEP)
    y += 80
    for row in range(3):
        for col in range(2):
            x = 40 + col * 250
            d.rounded_rectangle([x, y, x + 230, y + 300], radius=24, fill=(240, 247, 246))
            d.rounded_rectangle([x + 14, y + 14, x + 216, y + 170], radius=16,
                                fill=blend(TURQ_L, TURQ, 0.25 + 0.2 * ((row + col) % 2)))
            d.rounded_rectangle([x + 18, y + 190, x + 180, y + 210], radius=8, fill=(203, 213, 225))
            d.rounded_rectangle([x + 18, y + 222, x + 120, y + 240], radius=8, fill=(226, 232, 240))
            d.rounded_rectangle([x + 18, y + 254, x + 96, y + 282], radius=14, fill=TURQ)
        y += 330
    d.rounded_rectangle([40, y + 20, sw - 40, y + 220], radius=28, fill=DEEP)
    d.text((80, y + 60), "Reserva tu mesa", font=font("Inter-Bold.otf", 38), fill=WHITE)
    d.text((80, y + 116), "En segundos, sin llamar.", font=font("Inter-Regular.otf", 26), fill=TURQ_L)
    return s

SITE = build_site()

def draw_phone(img, cx, cy, appear, scroll):
    pw, ph = 600, 1180
    x0, y0 = cx - pw / 2, cy - ph / 2 + (1 - ease_out(appear)) * 300
    alpha = ease_out(appear)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    # shadow
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 10, y0 + 40, x0 + pw - 10, y0 + ph + 30], radius=80,
                                          fill=(8, 47, 52, int(70 * alpha)))
    sh = sh.filter(ImageFilter.GaussianBlur(40))
    layer.alpha_composite(sh)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=80, fill=(17, 24, 39, int(255 * alpha)))
    # screen
    sx, sy = int(x0 + 20), int(y0 + 20)
    sw, shh = pw - 40, ph - 40
    max_scroll = SITE.height - shh
    off = int(max_scroll * scroll)
    crop = SITE.crop((0, off, SITE.width, off + shh)).resize((sw, shh)) if SITE.width != sw else SITE.crop((0, off, sw, off + shh))
    mask = Image.new("L", (sw, shh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, shh - 1], radius=62, fill=int(255 * alpha))
    layer.paste(crop.convert("RGBA"), (sx, sy), mask)
    # notch
    d.rounded_rectangle([cx - 70, y0 + 36, cx + 70, y0 + 72], radius=18, fill=(17, 24, 39, int(255 * alpha)))
    img.alpha_composite(layer)

def chip(img, cx, y, text, prog):
    if prog <= 0:
        return
    f = font("Inter-SemiBold.otf", 52)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tw = d.textlength(text, font=f)
    w = tw + 150
    a = int(255 * ease_out(prog))
    x = cx - w / 2 + (1 - ease_out(prog)) * 120
    d.rounded_rectangle([x, y, x + w, y + 120], radius=60, fill=WHITE + (a,), outline=(226, 232, 240, a), width=3)
    r = 16
    d.ellipse([x + 52 - r, y + 60 - r, x + 52 + r, y + 60 + r], fill=TURQ + (a,))
    d.text((x + 100, y + 28), text, font=f, fill=DEEP + (a,))
    img.alpha_composite(layer)

# ---------- scenes ----------
def scene_logo(img, t, dur):
    draw_logo(img, W / 2, 820, 420, t / 0.9, clamp((t - 0.6) / 0.5))
    a = ease_out((t - 0.8) / 0.5)
    fade_text(img, W / 2, 1110, "lumen", font("Inter-Light.otf", 120), DEEP, a, dy=(1 - a) * 30)
    a2 = ease_out((t - 1.0) / 0.5)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    txt = "WEB DESIGN"
    f = font("Inter-Medium.otf", 40)
    sp = 16
    widths = [d.textlength(c, font=f) for c in txt]
    total = sum(widths) + sp * (len(txt) - 1)
    x = W / 2 - total / 2
    for c, w in zip(txt, widths):
        d.text((x, 1270), c, font=f, fill=TURQ + (int(255 * a2),))
        x += w + sp
    img.alpha_composite(layer)

def scene_hola(img, t, dur):
    a = ease_out(t / 0.3)
    fade_text(img, W / 2, 700, "Hola, soy", font("Inter-Light.otf", 96), GREY, a, dy=(1 - a) * 40)
    a2 = ease_out((t - 0.1) / 0.4)
    fade_text(img, W / 2, 820, "Angel", font("Inter-Bold.otf", 220), DEEP, a2, dy=(1 - a2) * 60)
    # underline light
    p = ease_in_out((t - 0.4) / 0.6)
    if p > 0:
        d = ImageDraw.Draw(img)
        lw = 420 * p
        d.rounded_rectangle([W / 2 - lw / 2, 1100, W / 2 + lw / 2, 1114], radius=7, fill=TURQ)
    a3 = ease_out((t - 0.6) / 0.4)
    fade_text(img, W / 2, 1170, "diseñador web", font("Inter-Regular.otf", 64), GREY, a3)

def scene_phone(img, t, dur):
    a = ease_out(t / 0.6)
    fade_text(img, W / 2, 150, "Páginas web", font("Inter-Bold.otf", 92), DEEP, a, dy=(1 - a) * 30)
    a2 = ease_out((t - 0.25) / 0.6)
    fade_text(img, W / 2, 260, "modernas y minimalistas", font("Inter-Light.otf", 66), TURQ, a2, dy=(1 - a2) * 30)
    scroll = ease_in_out((t - 1.6) / (dur - 2.4))
    draw_phone(img, W / 2, 1110, clamp(t / 0.9), scroll)

def scene_features(img, t, dur):
    a = ease_out(t / 0.6)
    fade_text(img, W / 2, 330, "Todo lo que tu", font("Inter-Light.otf", 84), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 440, "negocio necesita", font("Inter-Bold.otf", 96), DEEP, a, dy=(1 - a) * 30)
    items = [("Perfecta en el teléfono", 0.2), ("Pedidos online", 2.65), ("Reservas", 3.95), ("Fácil de encontrar", 6.3)]
    for i, (it, d0) in enumerate(items):
        chip(img, W / 2, 720 + i * 175, it, (t - d0) / 0.5)

def scene_world(img, t, dur):
    # pin + text
    a = ease_out(t / 0.6)
    d = ImageDraw.Draw(img)
    fade_text(img, W / 2, 520, "Desde", font("Inter-Light.otf", 80), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 620, "Aragua, Venezuela", font("Inter-Bold.otf", 100), DEEP, a, dy=(1 - a) * 30)
    # connecting line with travelling light
    p = ease_in_out((t - 0.8) / 1.4)
    if p > 0:
        y1, y2 = 820, 1120
        d.line([W / 2, y1, W / 2, y1 + (y2 - y1) * p], fill=(203, 213, 225), width=6)
        r = 20
        cy = y1 + (y2 - y1) * p
        d.ellipse([W / 2 - r, cy - r, W / 2 + r, cy + r], fill=TURQ)
    a2 = ease_out((t - 2.4) / 0.5)
    fade_text(img, W / 2, 1160, "para todo el país", font("Inter-Bold.otf", 96), DEEP, a2, dy=(1 - a2) * 30)
    a3 = ease_out((t - 3.3) / 0.5)
    fade_text(img, W / 2, 1280, "y el exterior", font("Inter-Light.otf", 90), TURQ, a3, dy=(1 - a3) * 30)

def scene_cta(img, t, dur):
    # dark ending
    bg_a = ease_out(t / 0.5)
    layer = Image.new("RGBA", img.size, DEEP + (int(255 * bg_a),))
    img.alpha_composite(layer)
    a = ease_out((t - 0.2) / 0.6)
    fade_text(img, W / 2, 470, "¿Tu negocio", font("Inter-Light.otf", 96), WHITE, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 590, "aún no tiene web?", font("Inter-Bold.otf", 96), WHITE, a, dy=(1 - a) * 30)
    a2 = ease_out((t - 2.5) / 0.5)
    if a2 > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        bw, bh = 640, 140
        x, y = W / 2 - bw / 2, 790 + (1 - a2) * 40
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=70, fill=TURQ + (int(255 * a2),))
        f = font("Inter-SemiBold.otf", 56)
        tw = d.textlength("Escríbeme", font=f)
        d.text((W / 2 - tw / 2, y + 36), "Escríbeme", font=f, fill=WHITE + (int(255 * a2),))
        img.alpha_composite(lay)
    a3 = ease_out((t - 3.4) / 0.5)
    fade_text(img, W / 2, 970, "Enlace en la biografía", font("Inter-Regular.otf", 50), TURQ_L, a3)
    # logo (light version)
    draw_logo(img, W / 2 - 170, 1340, 200, clamp((t - 5.3) / 0.8), clamp((t - 5.8) / 0.5), color=WHITE, dot=TURQ)
    a4 = ease_out((t - 5.6) / 0.5)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((W / 2 - 50, 1262), "lumen", font=font("Inter-Light.otf", 96), fill=WHITE + (int(255 * a4),))
    d.text((W / 2 - 46, 1380), "WEB DESIGN", font=font("Inter-Medium.otf", 32), fill=TURQ + (int(255 * a4),))
    img.alpha_composite(lay)
    a5 = ease_out((t - 6.4) / 0.6)
    fade_text(img, W / 2, 1600, "Le damos luz a tu negocio", font("Inter-Light.otf", 60), WHITE, a5)

SCENE_FN = {"logo": scene_logo, "hola": scene_hola, "phone": scene_phone,
            "features": scene_features, "world": scene_world, "cta": scene_cta}

def background(t):
    img = Image.new("RGBA", (W, H), OFF + (255,))
    # soft moving light blob
    g = Image.new("RGBA", (W // 4, H // 4), TURQ + (0,))
    d = ImageDraw.Draw(g)
    bx = W / 8 + math.sin(t * 0.4) * 60
    by = H / 8 + math.cos(t * 0.3) * 90
    d.ellipse([bx - 140, by - 140, bx + 140, by + 140], fill=TURQ + (38,))
    g = g.filter(ImageFilter.GaussianBlur(60)).resize((W, H), Image.BICUBIC)
    img.alpha_composite(g)
    return img

def frame(t):
    img = background(t)
    for name, s, e in SCENES:
        if s <= t < e:
            local = t - s
            dur = e - s
            scene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            base = img.copy()
            SCENE_FN[name](base, local, dur)
            # crossfade out in last 0.35s (except last scene)
            out = clamp((e - t) / 0.35) if name != "cta" else 1.0
            if out < 1:
                img = Image.blend(img, base, out)
            else:
                img = base
            break
    return img.convert("RGB")

def main(out, start=0.0, end=None):
    end = end or DURATION
    n = int((end - start) * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                          "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", out],
                         stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(start + i / FPS).tobytes())
    p.stdin.close()
    p.wait()

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for t in map(float, sys.argv[2:]):
            frame(t).save(f"/home/claude/lumen/video1/still_{t:05.1f}.png")
    else:
        main(sys.argv[2])
