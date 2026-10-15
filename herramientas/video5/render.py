"""Reel 5 – Así hago tu página web en 4 pasos (1080x1920, 30 fps).

Uso: python3 render.py still 1 6 12 ...   |   python3 render.py video salida.mp4
Los tiempos de T se ajustan a la voz final.
"""
import math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "video1"))
from PIL import Image, ImageDraw, ImageFilter
from render import (W, H, FPS, OFF, DEEP, TURQ, TURQ_L, GREY, WHITE, font, clamp, ease_out,
                    ease_in_out, back_out, blend, fade_text, draw_logo, background, text_center)

LINE = (226, 232, 240)
SOFT = (240, 247, 246)
MUTED = (203, 213, 225)
CREAM = (250, 243, 232)
COFFEE = (120, 82, 58)

# Inicio de cada escena (segundos). Se re-sincroniza con la voz.
T = dict(hook=0.0, cuatro=2.6, p1=4.25, p2=9.5, p3=12.8, p4=16.05, facil=22.0, cta=23.2)  # sincronizado con voz Diego
DURATION = 28.0
STEPS = [("p1", "Conversamos", "por WhatsApp"), ("p2", "Primer diseño", "de tu web"),
         ("p3", "Lo ajustamos", "juntos"), ("p4", "La publico", "y te acompaño")]


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def shadow(lay, box, radius, a=1.0, strength=35, blur=26):
    sh = layer()
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 22, x1, y1 + 22], radius=radius, fill=DEEP + (int(strength * a),))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))


def check(d, cx, cy, s, col, w=None):
    w = w or max(4, int(s * 0.14))
    d.line([cx - s * 0.32, cy + s * 0.02, cx - s * 0.08, cy + s * 0.26, cx + s * 0.36, cy - s * 0.24], fill=col, width=w, joint="curve")


# ---------- barra de progreso de 4 pasos ----------
def progress(img, t, alpha):
    if alpha <= 0:
        return
    lay = layer()
    d = ImageDraw.Draw(lay)
    a8 = int(255 * alpha)
    xs = [W / 2 - 330 + i * 220 for i in range(4)]
    y = 200
    d.line([xs[0], y, xs[-1], y], fill=LINE + (a8,), width=8)
    cur = -1
    for i, (k, _, _) in enumerate(STEPS):
        if t >= T[k]:
            cur = i
    if cur >= 0:
        # relleno animado de la línea
        fill_p = ease_in_out((t - T[STEPS[cur][0]]) / 0.6)
        x_end = xs[max(0, cur - 1)] + (xs[cur] - xs[max(0, cur - 1)]) * fill_p
        d.line([xs[0], y, x_end, y], fill=TURQ + (a8,), width=8)
    for i, x in enumerate(xs):
        on = 0.0
        if i < cur:
            on = 1.0
        elif i == cur:
            on = ease_out((t - T[STEPS[i][0]] - 0.3) / 0.4)
        r = 40 + 8 * (on if i == cur else 0)
        d.ellipse([x - r, y - r, x + r, y + r], fill=blend(WHITE, TURQ, on) + (a8,), outline=blend(MUTED, TURQ, on) + (a8,), width=5)
        if i < cur:
            check(d, x, y, 44, WHITE + (a8,))
        else:
            text_center(d, x, y - 24, str(i + 1), font("Inter-Bold.otf", 40), blend(GREY, WHITE, on) + (a8,))
    img.alpha_composite(lay)


def step_title(img, local, line1, line2):
    a = ease_out((local - 0.2) / 0.45)
    fade_text(img, W / 2, 320, line1, font("Inter-Bold.otf", 96), DEEP, a, dy=(1 - a) * 26)
    fade_text(img, W / 2, 432, line2, font("Inter-Light.otf", 80), TURQ, a, dy=(1 - a) * 26)


# ---------- maqueta del sitio inventado "Café Aurora" ----------
def site_mock(img, cx, top, p, build=1.0, tune=0.0, url=0.0, scale=1.0):
    """build: 0..1 bloques que aparecen; tune: 0..1 colores finales; url: barra con dirección."""
    a = ease_out(p)
    if a <= 0:
        return
    w, h = 720 * scale, 900 * scale
    x0, y0 = cx - w / 2, top + (1 - a) * 80
    lay = layer()
    shadow(lay, (x0, y0, x0 + w, y0 + h), 40 * scale, a, 45, 34)
    d = ImageDraw.Draw(lay)
    a8 = int(255 * a)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=40 * scale, fill=WHITE + (a8,), outline=LINE + (a8,), width=3)
    # barra del navegador
    d.rounded_rectangle([x0, y0, x0 + w, y0 + 80 * scale], radius=40 * scale, fill=SOFT + (a8,))
    d.rectangle([x0, y0 + 40 * scale, x0 + w, y0 + 80 * scale], fill=SOFT + (a8,))
    for i, c in enumerate([(248, 113, 113), (251, 191, 36), (74, 222, 128)]):
        d.ellipse([x0 + (30 + i * 34) * scale, y0 + 28 * scale, x0 + (52 + i * 34) * scale, y0 + 50 * scale], fill=c + (a8,))
    ub = (x0 + 150 * scale, y0 + 18 * scale, x0 + w - 30 * scale, y0 + 62 * scale)
    d.rounded_rectangle(ub, radius=22 * scale, fill=WHITE + (a8,))
    if url > 0:
        ua = int(255 * a * url)
        d.ellipse([ub[0] + 18 * scale, ub[1] + 14 * scale, ub[0] + 34 * scale, ub[1] + 30 * scale], fill=(34, 197, 94) + (ua,))
        d.text((ub[0] + 46 * scale, ub[1] + 6 * scale), "cafeaurora.com", font=font("Inter-Medium.otf", int(26 * scale)), fill=DEEP + (ua,))

    def blk(k):  # progreso de cada bloque al construirse
        return ease_out(clamp(build * 5 - k))

    hero_col = blend((214, 205, 192), DEEP, tune)
    accent = blend(COFFEE, TURQ, tune)
    # menú
    b = blk(0)
    if b > 0:
        ba = int(a8 * b)
        d.text((x0 + 40 * scale, y0 + 104 * scale), "Café Aurora", font=font("Inter-Bold.otf", int(34 * scale)), fill=DEEP + (ba,))
        for i in range(3):
            d.rounded_rectangle([x0 + w - 70 * scale, y0 + (110 + i * 11) * scale, x0 + w - 36 * scale, y0 + (114 + i * 11) * scale], radius=2, fill=DEEP + (ba,))
    # portada
    b = blk(1)
    if b > 0:
        ba = int(a8 * b)
        hy = y0 + 170 * scale
        d.rounded_rectangle([x0 + 30 * scale, hy, x0 + w - 30 * scale, hy + 330 * scale * b], radius=28 * scale, fill=hero_col + (ba,))
        if b > 0.9:
            tc = blend(DEEP, WHITE, tune)
            d.text((x0 + 70 * scale, hy + 70 * scale), "Café de especialidad", font=font("Inter-Bold.otf", int(44 * scale)), fill=tc + (ba,))
            d.text((x0 + 70 * scale, hy + 134 * scale), "y postres caseros", font=font("Inter-Light.otf", int(40 * scale)), fill=tc + (ba,))
            d.rounded_rectangle([x0 + 70 * scale, hy + 220 * scale, x0 + 300 * scale, hy + 280 * scale], radius=30 * scale, fill=accent + (ba,))
            text_center(d, x0 + 185 * scale, hy + 234 * scale, "Pedir ahora", font("Inter-SemiBold.otf", int(26 * scale)), WHITE + (ba,))
    # productos
    for i in range(3):
        b = blk(2 + i * 0.6)
        if b <= 0:
            continue
        ba = int(a8 * b)
        cw = (w - 60 * scale - 40 * scale) / 3
        px = x0 + 30 * scale + i * (cw + 20 * scale)
        py = y0 + 540 * scale + (1 - b) * 30
        d.rounded_rectangle([px, py, px + cw, py + 300 * scale], radius=22 * scale, fill=SOFT + (ba,))
        d.rounded_rectangle([px + 14 * scale, py + 14 * scale, px + cw - 14 * scale, py + 160 * scale], radius=16 * scale,
                            fill=blend(blend(CREAM, (226, 205, 180), 0.3 + 0.2 * i), blend(TURQ_L, TURQ, 0.2 + 0.15 * i), tune) + (ba,))
        d.rounded_rectangle([px + 16 * scale, py + 184 * scale, px + cw - 40 * scale, py + 204 * scale], radius=8, fill=MUTED + (ba,))
        d.rounded_rectangle([px + 16 * scale, py + 236 * scale, px + 100 * scale, py + 272 * scale], radius=18 * scale, fill=accent + (ba,))
    img.alpha_composite(lay)


# ---------- escenas ----------
def scene_hook(img, t):
    a = ease_out(t / 0.45)
    fade_text(img, W / 2, 520, "¿Cómo se hace", font("Inter-Light.otf", 92), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 640, "una página web", font("Inter-Bold.otf", 110), DEEP, a, dy=(1 - a) * 30)
    a2 = ease_out((t - 0.5) / 0.45)
    fade_text(img, W / 2, 770, "con Lumen?", font("Inter-Bold.otf", 110), TURQ, a2, dy=(1 - a2) * 30)
    # cursor y bloques que se arman
    for i in range(3):
        bp = ease_out((t - 1.0 - i * 0.25) / 0.45)
        if bp <= 0:
            continue
        lay = layer()
        d = ImageDraw.Draw(lay)
        y = 1050 + i * 150 + (1 - bp) * 60
        wv = [760, 560, 660][i] * bp
        d.rounded_rectangle([W / 2 - wv / 2, y, W / 2 + wv / 2, y + 110], radius=30,
                            fill=[DEEP, TURQ, TURQ_L][i] + (int(255 * bp),))
        img.alpha_composite(lay)


def scene_cuatro(img, t):
    local = t - T["cuatro"]
    progress(img, t, ease_out(local / 0.5))
    p = back_out(local / 0.5)
    lay = layer()
    text_center(ImageDraw.Draw(lay), W / 2, 560, "4", font("Inter-Bold.otf", int(max(1, 440 * p))), DEEP)
    img.alpha_composite(lay)
    a = ease_out((local - 0.25) / 0.4)
    fade_text(img, W / 2, 1110, "pasos", font("Inter-Light.otf", 120), TURQ, a, dy=(1 - a) * 30)


def bubble(img, text_lines, side, y, p):
    if p <= 0:
        return 0
    f = font("Inter-Medium.otf", 42)
    lay = layer()
    d = ImageDraw.Draw(lay)
    tw = max(d.textlength(s, font=f) for s in text_lines)
    bw, bh = tw + 80, 60 * len(text_lines) + 50
    a = ease_out(p)
    a8 = int(255 * a)
    if side == "l":
        x0 = 100 - (1 - a) * 60
        fill, col = WHITE, DEEP
    else:
        x0 = W - 100 - bw + (1 - a) * 60
        fill, col = TURQ, WHITE
    shadow(lay, (x0, y, x0 + bw, y + bh), 36, a * 0.7)
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=36, fill=fill + (a8,), outline=(LINE if side == "l" else TURQ) + (a8,), width=2)
    for i, s in enumerate(text_lines):
        d.text((x0 + 40, y + 24 + i * 60), s, font=f, fill=col + (a8,))
    img.alpha_composite(lay)
    return bh


def scene_p1(img, t):
    local = t - T["p1"]
    progress(img, t, 1)
    step_title(img, local, *STEPS[0][1:])
    msgs = [(["Hola, quiero una web", "para mi café"], "l", 0.7),
            (["¡Claro! ¿Qué vendes?"], "r", 1.5),
            (["Café y postres.", "Mis colores: crema y café"], "l", 2.4),
            (["¿Y qué necesitas?"], "r", 3.5),
            (["Que me hagan pedidos", "desde la web"], "l", 4.2)]
    y = 640
    for lines, side, st in msgs:
        h = bubble(img, lines, side, y, (local - st) / 0.4)
        y += (h or (60 * len(lines) + 50)) + 36


def scene_p2(img, t):
    local = t - T["p2"]
    progress(img, t, 1)
    step_title(img, local, *STEPS[1][1:])
    site_mock(img, W / 2, 620, (local - 0.2) / 0.5, build=clamp((local - 0.5) / 2.2))


def scene_p3(img, t):
    local = t - T["p3"]
    progress(img, t, 1)
    step_title(img, local, *STEPS[2][1:])
    tune = ease_in_out((local - 0.9) / 1.4)
    site_mock(img, W / 2, 620, 1.0, build=1.0, tune=tune)
    # muestras de color
    sw = ease_out((local - 0.3) / 0.4)
    if sw > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        cols = [DEEP, TURQ, TURQ_L, WHITE]
        bx = W / 2 - (len(cols) * 110 - 20) / 2
        d.rounded_rectangle([bx - 30, 1560, bx + len(cols) * 110 + 10, 1700], radius=70, fill=WHITE + (int(255 * sw),), outline=LINE + (int(255 * sw),), width=3)
        for i, c in enumerate(cols):
            x = bx + i * 110
            d.ellipse([x + 10, 1590, x + 90, 1670], fill=c + (int(255 * sw),), outline=MUTED + (int(255 * sw),), width=2)
        # anillo de selección
        sel = 1 if tune > 0.5 else 0
        x = bx + sel * 110
        d.ellipse([x + 2, 1582, x + 98, 1678], outline=TURQ + (int(255 * sw),), width=6)
        img.alpha_composite(lay)
    # sello "¡Me gusta!"
    sp = back_out((local - 2.6) / 0.5)
    if sp > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        cx, cy = W - 200, 690
        r = 90 * sp
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TURQ)
        if sp > 0.6:
            check(d, cx, cy, 100 * sp, WHITE)
        img.alpha_composite(lay)


def scene_p4(img, t):
    local = t - T["p4"]
    progress(img, t, 1)
    step_title(img, local, *STEPS[3][1:])
    # la web se publica: se encoge y aparece la dirección
    pub = ease_in_out((local - 0.3) / 0.8)
    site_mock(img, W / 2, 600, 1.0, build=1.0, tune=1.0, url=ease_out((local - 0.9) / 0.5), scale=1 - 0.28 * pub)
    lp = back_out((local - 1.1) / 0.5)
    if lp > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        cx, cy = W / 2 + 230, 640
        bw = 250 * lp
        d.rounded_rectangle([cx - bw / 2, cy - 40, cx + bw / 2, cy + 40], radius=40, fill=(34, 197, 94))
        if lp > 0.85:
            text_center(d, cx, cy - 20, "En línea", font("Inter-SemiBold.otf", 34), WHITE)
        img.alpha_composite(lay)
    items = [("Te enseño a usarla", 1.8), ("2 semanas de", 3.3)]
    for i, (txt, st) in enumerate(items):
        ip = ease_out((local - st) / 0.5)
        if ip <= 0:
            continue
        lay = layer()
        y = 1330 + i * 190 + (1 - ip) * 40
        box = (130, y, W - 130, y + 160)
        dark = i == 1
        shadow(lay, box, 80, ip)
        d = ImageDraw.Draw(lay)
        a8 = int(255 * ip)
        d.rounded_rectangle(box, radius=80, fill=(DEEP if dark else WHITE) + (a8,), outline=(DEEP if dark else LINE) + (a8,), width=3)
        d.ellipse([190, y + 45, 260, y + 115], fill=TURQ + (a8,))
        check(d, 225, y + 80, 44, WHITE + (a8,))
        if dark:
            d.text((300, y + 22), "2 semanas de mantenimiento", font=font("Inter-SemiBold.otf", 42), fill=WHITE + (a8,))
            d.text((300, y + 82), "gratis", font=font("Inter-Bold.otf", 42), fill=TURQ + (a8,))
        else:
            d.text((300, y + 50), txt, font=font("Inter-SemiBold.otf", 50), fill=DEEP + (a8,))
        img.alpha_composite(lay)


def scene_facil(img, t):
    local = t - T["facil"]
    progress(img, T["facil"] + 1, 1)  # los 4 pasos completos
    lay = layer()
    d = ImageDraw.Draw(lay)
    xs = [W / 2 - 330 + i * 220 for i in range(4)]
    for i, x in enumerate(xs):  # último paso marcado
        if i == 3:
            d.ellipse([x - 40, 160, x + 40, 240], fill=TURQ)
            check(d, x, 200, 44, WHITE)
    img.alpha_composite(lay)
    a = ease_out(local / 0.4)
    fade_text(img, W / 2, 760, "Así de", font("Inter-Light.otf", 110), GREY, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 0.2) / 0.4)
    fade_text(img, W / 2, 890, "fácil", font("Inter-Bold.otf", 200), TURQ, a2, dy=(1 - a2) * 40)


def scene_cta(img, t):
    local = t - T["cta"]
    bg_a = ease_out(local / 0.45)
    img.alpha_composite(Image.new("RGBA", img.size, DEEP + (int(255 * bg_a),)))
    a = ease_out((local - 0.15) / 0.5)
    fade_text(img, W / 2, 470, "¿Empezamos", font("Inter-Light.otf", 100), WHITE, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 590, "con la tuya?", font("Inter-Bold.otf", 110), TURQ, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 0.7) / 0.5)
    if a2 > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        bw, bh = 640, 140
        x, y = W / 2 - bw / 2, 800 + (1 - a2) * 40
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=70, fill=TURQ + (int(255 * a2),))
        text_center(d, W / 2, y + 36, "Escríbeme", font("Inter-SemiBold.otf", 56), WHITE + (int(255 * a2),))
        img.alpha_composite(lay)
    a3 = ease_out((local - 1.2) / 0.5)
    fade_text(img, W / 2, 980, "Enlace en la biografía", font("Inter-Regular.otf", 50), TURQ_L, a3)
    draw_logo(img, W / 2 - 170, 1340, 200, clamp((local - 1.8) / 0.8), clamp((local - 2.3) / 0.5), color=WHITE, dot=TURQ)
    a4 = ease_out((local - 2.1) / 0.5)
    lay = layer()
    d = ImageDraw.Draw(lay)
    d.text((W / 2 - 50, 1262), "lumen", font=font("Inter-Light.otf", 96), fill=WHITE + (int(255 * a4),))
    d.text((W / 2 - 46, 1380), "WEB DESIGN", font=font("Inter-Medium.otf", 32), fill=TURQ + (int(255 * a4),))
    img.alpha_composite(lay)
    a5 = ease_out((local - 2.8) / 0.6)
    fade_text(img, W / 2, 1600, "Le damos luz a tu negocio", font("Inter-Light.otf", 60), WHITE, a5)


ORDER = ["hook", "cuatro", "p1", "p2", "p3", "p4", "facil", "cta"]
FN = dict(hook=scene_hook, cuatro=scene_cuatro, p1=scene_p1, p2=scene_p2, p3=scene_p3,
          p4=scene_p4, facil=scene_facil, cta=scene_cta)
NO_FADE = {"cta", "p1", "p2", "p3"}  # p2→p3 comparten maqueta: corte limpio


def frame(t):
    img = background(t)
    for i, name in enumerate(ORDER):
        s = T[name]
        e = T[ORDER[i + 1]] if i + 1 < len(ORDER) else DURATION + 1
        if s <= t < e:
            base = img.copy()
            FN[name](base, t)
            out = clamp((e - t) / 0.3) if name not in NO_FADE else 1.0
            img = Image.blend(img, base, out) if out < 1 else base
            break
    return img.convert("RGB")


def main(out):
    n = int(DURATION * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                          "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", out], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    p.wait()


if __name__ == "__main__":
    if sys.argv[1] == "still":
        ts = list(map(float, sys.argv[2:]))
        ims = [frame(t).resize((360, 640)) for t in ts]
        s = Image.new("RGB", (370 * len(ims), 640), "white")
        for i, im in enumerate(ims):
            s.paste(im, (i * 370, 0))
        s.save(os.path.join(HERE, "check.png"))
    else:
        main(sys.argv[2])
