"""Reel 4 – ¿Tu negocio solo está en redes sociales? 3 razones (1080x1920, 30 fps).

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
RED = (239, 68, 68)
RED_L = (254, 226, 226)

# Inicio de cada escena (segundos). Se re-sincroniza con la voz.
T = dict(hook=0.0, tres=2.55, uno=6.2, dos=11.0, tres_r=18.75, cta=24.0)  # sincronizado con voz Diego
DURATION = 30.0


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def shadow_card(lay, box, radius, a=1.0, strength=35, blur=26):
    sh = layer()
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 22, x1, y1 + 22], radius=radius, fill=DEEP + (int(strength * a),))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))


def number_badge(d, cx, cy, n, a, r=58):
    a8 = int(255 * a)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TURQ + (a8,))
    text_center(d, cx, cy - r * 0.62, str(n), font("Inter-Bold.otf", int(r * 1.1)), WHITE + (a8,))


# ---------------- iconos ----------------
def icon_search(d, cx, cy, s, col):
    r = s * 0.32
    w = max(4, int(s * 0.09))
    d.ellipse([cx - r - s * 0.08, cy - r - s * 0.08, cx + r - s * 0.08, cy + r - s * 0.08], outline=col, width=w)
    d.line([cx + r * 0.62, cy + r * 0.62, cx + s * 0.38, cy + s * 0.38], fill=col, width=w + 2)


def icon_lock(d, cx, cy, s, col, open_=0.0):
    w = max(4, int(s * 0.09))
    bw, bh = s * 0.62, s * 0.46
    d.rounded_rectangle([cx - bw / 2, cy - bh * 0.15, cx + bw / 2, cy + bh * 0.85], radius=s * 0.08, fill=col)
    ar = s * 0.2
    lift = open_ * s * 0.16
    d.arc([cx - ar, cy - bh * 0.15 - ar * 2 - lift, cx + ar, cy - bh * 0.15 + ar * 0.2 - lift], 180, 360, fill=col, width=w)
    d.line([cx - ar + w / 2, cy - bh * 0.15 - ar * 0.9 - lift, cx - ar + w / 2, cy - bh * 0.15], fill=col, width=w)
    d.line([cx + ar - w / 2, cy - bh * 0.15 - ar * 0.9 - lift, cx + ar - w / 2, cy - bh * 0.15], fill=col, width=w)


def icon_link(d, cx, cy, s, col):
    w = max(4, int(s * 0.1))
    for k in (-1, 1):
        ox = k * s * 0.17
        d.rounded_rectangle([cx + ox - s * 0.28, cy - s * 0.14, cx + ox + s * 0.28, cy + s * 0.14],
                            radius=s * 0.14, outline=col, width=w)


# ---------------- escenas ----------------
def social_phone(img, cx, cy, p, glitch=0.0):
    """Teléfono con un perfil de red social genérico (sin marcas)."""
    pw, ph = 560, 1000
    a = ease_out(p)
    x0, y0 = cx - pw / 2, cy - ph / 2 + (1 - a) * 260
    lay = layer()
    shadow_card(lay, (x0 + 10, y0 + 20, x0 + pw - 10, y0 + ph), 76, a, 60, 40)
    d = ImageDraw.Draw(lay)
    a8 = int(255 * a)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=76, fill=(17, 24, 39, a8))
    sx0, sy0, sx1, sy1 = x0 + 18, y0 + 18, x0 + pw - 18, y0 + ph - 18
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=60, fill=WHITE + (a8,))
    d.rounded_rectangle([cx - 66, y0 + 34, cx + 66, y0 + 68], radius=17, fill=(17, 24, 39, a8))
    # cabecera del perfil
    d.ellipse([sx0 + 40, sy0 + 100, sx0 + 170, sy0 + 230], fill=blend(TURQ_L, TURQ, 0.5) + (a8,))
    d.text((sx0 + 200, sy0 + 112), "tu_negocio", font=font("Inter-Bold.otf", 34), fill=DEEP + (a8,))
    for i, (n, l) in enumerate([("128", "posts"), ("1,2 mil", "seguidores")]):
        d.text((sx0 + 200 + i * 150, sy0 + 166), n, font=font("Inter-SemiBold.otf", 26), fill=DEEP + (a8,))
        d.text((sx0 + 200 + i * 150, sy0 + 200), l, font=font("Inter-Regular.otf", 20), fill=GREY + (a8,))
    # cuadrícula de fotos
    gw = (sx1 - sx0 - 16) / 3
    for r in range(4):
        for c in range(3):
            gx = sx0 + 4 + c * (gw + 4)
            gy = sy0 + 280 + r * (gw + 4)
            if gy + gw > sy1 - 10:
                continue
            col = blend(TURQ_L, TURQ, 0.15 + 0.12 * ((r * 3 + c) % 4))
            if glitch > 0:
                col = blend(col, (203, 213, 225), glitch)
            d.rectangle([gx, gy, gx + gw, gy + gw], fill=col + (a8,))
    img.alpha_composite(lay)
    return (sx0, sy0, sx1, sy1)


def scene_hook(img, t):
    a = ease_out(t / 0.45)
    fade_text(img, W / 2, 170, "¿Tu negocio solo", font("Inter-Light.otf", 88), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 280, "está en redes?", font("Inter-Bold.otf", 108), DEEP, a, dy=(1 - a) * 30)
    social_phone(img, W / 2, 1120, clamp((t - 0.2) / 0.8))
    # burbuja de pregunta
    p = back_out((t - 1.4) / 0.5)
    if p > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        cx, cy, r = 850, 690, 90 * p
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TURQ)
        if p > 0.7:
            text_center(d, cx, cy - 62, "?", font("Inter-Bold.otf", 110), WHITE)
        img.alpha_composite(lay)


def scene_tres(img, t):
    local = t - T["tres"]
    p = back_out(local / 0.5)
    lay = layer()
    d = ImageDraw.Draw(lay)
    text_center(d, W / 2, 470, "3", font("Inter-Bold.otf", int(max(1, 420 * p))), DEEP)
    img.alpha_composite(lay)
    a = ease_out((local - 0.25) / 0.4)
    fade_text(img, W / 2, 1000, "razones para tener", font("Inter-Light.otf", 80), GREY, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 0.45) / 0.4)
    fade_text(img, W / 2, 1110, "tu página web", font("Inter-Bold.otf", 104), TURQ, a2, dy=(1 - a2) * 30)


def reason_header(img, local, n, line1, line2):
    a = ease_out(local / 0.4)
    lay = layer()
    number_badge(ImageDraw.Draw(lay), W / 2, 250, n, a)
    img.alpha_composite(lay)
    fade_text(img, W / 2, 360, line1, font("Inter-Light.otf", 76), GREY, a, dy=(1 - a) * 24)
    fade_text(img, W / 2, 455, line2, font("Inter-Bold.otf", 92), DEEP, a, dy=(1 - a) * 24)


def scene_uno(img, t):
    local = t - T["uno"]
    reason_header(img, local, 1, "Te encuentran", "en Google")
    # barra de búsqueda
    p = ease_out((local - 0.3) / 0.5)
    if p <= 0:
        return
    lay = layer()
    shadow_card(lay, (110, 690, W - 110, 820), 65, p)
    d = ImageDraw.Draw(lay)
    a8 = int(255 * p)
    d.rounded_rectangle([110, 690 + (1 - p) * 40, W - 110, 820 + (1 - p) * 40], radius=65, fill=WHITE + (a8,), outline=LINE + (a8,), width=3)
    icon_search(d, 190, 755, 64, TURQ + (a8,))
    q = "panadería en Maracay"
    n = int(len(q) * clamp((local - 0.8) / 1.3))
    d.text((250, 730), q[:n], font=font("Inter-Regular.otf", 44), fill=DEEP + (a8,))
    if n < len(q) and int(local * 3) % 2 == 0:
        x = 250 + d.textlength(q[:n], font=font("Inter-Regular.otf", 44))
        d.rectangle([x + 4, 728, x + 8, 784], fill=TURQ + (a8,))
    img.alpha_composite(lay)
    # resultados
    results = [("Tu negocio", "tunegocio.com", True), ("Otro local", "otro-local.com", False), ("Competencia", "competencia.com", False)]
    for i, (name, url, mine) in enumerate(results):
        rp = ease_out((local - 2.3 - i * 0.2) / 0.45)
        if rp <= 0:
            continue
        lay = layer()
        d = ImageDraw.Draw(lay)
        y = 900 + i * 230 + (1 - rp) * 40
        a8 = int(255 * rp * (1 if mine else 0.85))
        hi = ease_out((local - 3.3) / 0.5) if mine else 0
        if mine:
            shadow_card(lay, (110, y, W - 110, y + 200), 36, rp * (0.4 + hi))
            d = ImageDraw.Draw(lay)
        d.rounded_rectangle([110, y, W - 110, y + 200], radius=36,
                            fill=(blend(WHITE, DEEP, hi) if mine else SOFT) + (a8,),
                            outline=(blend(LINE, TURQ, hi) if mine else LINE) + (a8,), width=4)
        d.text((160, y + 40), url, font=font("Inter-Regular.otf", 30), fill=(blend(GREY, TURQ_L, hi) if mine else GREY) + (a8,))
        d.text((160, y + 90), name, font=font("Inter-Bold.otf", 50), fill=(blend(DEEP, WHITE, hi) if mine else (148, 163, 184)) + (a8,))
        if mine and hi > 0:
            bp = back_out((local - 3.5) / 0.5)
            if bp > 0:
                d.rounded_rectangle([W - 330, y + 66, W - 330 + 180 * bp, y + 134], radius=34, fill=TURQ + (a8,))
                if bp > 0.9:
                    d.text((W - 300, y + 80), "N.º 1", font=font("Inter-SemiBold.otf", 34), fill=WHITE + (a8,))
        img.alpha_composite(lay)


def scene_dos(img, t):
    local = t - T["dos"]
    reason_header(img, local, 2, "Tu web", "es solo tuya")
    # tarjeta de cuenta con problema
    p = ease_out((local - 0.3) / 0.5)
    if p > 0:
        warn = ease_out((local - 3.2) / 0.4)
        shake = math.sin(local * 40) * 10 * clamp(1 - abs(local - 3.5) / 0.4) if warn > 0 else 0
        lay = layer()
        box = (130 + shake, 650, W - 130 + shake, 960)
        shadow_card(lay, box, 40, p)
        d = ImageDraw.Draw(lay)
        a8 = int(255 * p)
        d.rounded_rectangle(box, radius=40, fill=blend(WHITE, RED_L, warn) + (a8,), outline=blend(LINE, RED, warn) + (a8,), width=4)
        d.ellipse([box[0] + 50, 715, box[0] + 170, 835], fill=blend(blend(TURQ_L, TURQ, 0.5), (203, 213, 225), warn) + (a8,))
        d.text((box[0] + 200, 720), "tu_negocio", font=font("Inter-Bold.otf", 46), fill=DEEP + (a8,))
        sub = "Cuenta con problemas" if warn > 0.5 else "1,2 mil seguidores"
        d.text((box[0] + 200, 785), sub, font=font("Inter-Medium.otf", 34), fill=blend(GREY, RED, warn) + (a8,))
        if warn > 0:
            r = 34 * back_out((local - 3.2) / 0.5)
            cx, cy = box[2] - 70, 700
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED + (a8,))
            if r > 26:
                text_center(d, cx, cy - 26, "!", font("Inter-Bold.otf", 46), WHITE + (a8,))
        img.alpha_composite(lay)
        a2 = ease_out((local - 4.6) / 0.5)
        fade_text(img, W / 2, 870 + 140, "Pierdes a tus clientes", font("Inter-SemiBold.otf", 48), RED, a2)
    # tarjeta web segura
    p2 = ease_out((local - 6.0) / 0.6)
    if p2 > 0:
        lay = layer()
        y = 1230 + (1 - p2) * 60
        box = (130, y, W - 130, y + 330)
        shadow_card(lay, box, 44, p2, 60)
        d = ImageDraw.Draw(lay)
        a8 = int(255 * p2)
        d.rounded_rectangle(box, radius=44, fill=DEEP + (a8,))
        d.ellipse([190, y + 95, 330, y + 235], fill=TURQ + (a8,))
        icon_lock(d, 260, y + 170, 90, WHITE + (a8,))
        d.text((370, y + 95), "tunegocio.com", font=font("Inter-Bold.otf", 52), fill=WHITE + (a8,))
        d.text((370, y + 175), "Siempre tuya", font=font("Inter-Regular.otf", 40), fill=TURQ_L + (a8,))
        img.alpha_composite(lay)


def scene_tres_r(img, t):
    local = t - T["tres_r"]
    reason_header(img, local, 3, "Todo en", "un solo enlace")
    # píldora del enlace
    p = back_out((local - 0.3) / 0.5)
    cy = 820
    if p > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        w = 700 * p
        d.rounded_rectangle([W / 2 - w / 2, cy - 75, W / 2 + w / 2, cy + 75], radius=75, fill=TURQ)
        if p > 0.85:
            icon_link(d, W / 2 - 240, cy, 90, WHITE)
            d.text((W / 2 - 160, cy - 34), "tunegocio.com", font=font("Inter-SemiBold.otf", 56), fill=WHITE)
        img.alpha_composite(lay)
    items = [("Menú", 1.1), ("Precios", 2.1), ("Pedidos", 3.0)]
    # línea que conecta el enlace con las tarjetas (detrás de ellas)
    last = -1
    for i, (_, st) in enumerate(items):
        if local >= st:
            last = i
    if last >= 0:
        lp = ease_out((local - items[last][1]) / 0.5)
        y_prev = cy + 75 if last == 0 else 1050 + (last - 1) * 190 + 70
        y_end = y_prev + (1050 + last * 190 + 70 - y_prev) * lp
        lay = layer()
        ImageDraw.Draw(lay).line([W / 2, cy + 75, W / 2, y_end], fill=(203, 213, 225), width=5)
        img.alpha_composite(lay)
    for i, (txt, st) in enumerate(items):
        ip = ease_out((local - st) / 0.5)
        if ip <= 0:
            continue
        lay = layer()
        d = ImageDraw.Draw(lay)
        y = 1050 + i * 190
        x0 = 220 + (1 - ip) * 160
        a8 = int(255 * ip)
        shadow_card(lay, (x0, y, W - 220 + (1 - ip) * 160, y + 140), 70, ip)
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle([x0, y, W - 220 + (1 - ip) * 160, y + 140], radius=70, fill=WHITE + (a8,), outline=LINE + (a8,), width=3)
        d.ellipse([x0 + 46, y + 52, x0 + 82, y + 88], fill=TURQ + (a8,))
        d.text((x0 + 116, y + 36), txt, font=font("Inter-SemiBold.otf", 56), fill=DEEP + (a8,))
        img.alpha_composite(lay)


def scene_cta(img, t):
    local = t - T["cta"]
    bg_a = ease_out(local / 0.45)
    img.alpha_composite(Image.new("RGBA", img.size, DEEP + (int(255 * bg_a),)))
    a = ease_out((local - 0.15) / 0.5)
    fade_text(img, W / 2, 380, "Soy Angel,", font("Inter-Light.otf", 92), TURQ_L, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 500, "de Lumen Web Design", font("Inter-Bold.otf", 84), WHITE, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 3.0) / 0.5)
    fade_text(img, W / 2, 680, "¿Hacemos la tuya?", font("Inter-SemiBold.otf", 72), TURQ, a2, dy=(1 - a2) * 30)
    a3 = ease_out((local - 2.4) / 0.5)
    if a3 > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        bw, bh = 640, 140
        x, y = W / 2 - bw / 2, 840 + (1 - a3) * 40
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=70, fill=TURQ + (int(255 * a3),))
        text_center(d, W / 2, y + 36, "Escríbeme", font("Inter-SemiBold.otf", 56), WHITE + (int(255 * a3),))
        img.alpha_composite(lay)
    a4 = ease_out((local - 2.8) / 0.5)
    fade_text(img, W / 2, 1020, "Enlace en la biografía", font("Inter-Regular.otf", 50), TURQ_L, a4)
    draw_logo(img, W / 2 - 170, 1390, 200, clamp((local - 3.4) / 0.8), clamp((local - 3.9) / 0.5), color=WHITE, dot=TURQ)
    a5 = ease_out((local - 3.7) / 0.5)
    lay = layer()
    d = ImageDraw.Draw(lay)
    d.text((W / 2 - 50, 1312), "lumen", font=font("Inter-Light.otf", 96), fill=WHITE + (int(255 * a5),))
    d.text((W / 2 - 46, 1430), "WEB DESIGN", font=font("Inter-Medium.otf", 32), fill=TURQ + (int(255 * a5),))
    img.alpha_composite(lay)
    a6 = ease_out((local - 4.4) / 0.6)
    fade_text(img, W / 2, 1650, "Le damos luz a tu negocio", font("Inter-Light.otf", 60), WHITE, a6)


ORDER = ["hook", "tres", "uno", "dos", "tres_r", "cta"]
FN = dict(hook=scene_hook, tres=scene_tres, uno=scene_uno, dos=scene_dos, tres_r=scene_tres_r, cta=scene_cta)


def frame(t):
    img = background(t)
    for i, name in enumerate(ORDER):
        s = T[name]
        e = T[ORDER[i + 1]] if i + 1 < len(ORDER) else DURATION + 1
        if s <= t < e:
            base = img.copy()
            FN[name](base, t)
            out = clamp((e - t) / 0.3) if name != "cta" else 1.0
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
