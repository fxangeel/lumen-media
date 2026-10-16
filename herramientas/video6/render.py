"""Reel 6 – 3 errores que espantan clientes (1080x1920, 30 fps).

Uso: python3 render.py still 1 6 12 ...   |   python3 render.py video salida.mp4 [instagram|tiktok]
Tiempos sincronizados con la voz Diego (voz6.mp3, 23,7 s).
"""
import importlib.util, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "video1"))
from PIL import Image, ImageDraw
from render import (W, H, FPS, DEEP, TURQ, TURQ_L, GREY, WHITE, font, clamp, ease_out,
                    back_out, blend, fade_text, draw_logo, background, text_center)

_spec = importlib.util.spec_from_file_location("v4", os.path.join(HERE, "..", "video4", "render.py"))
v4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v4)
layer, shadow_card, number_badge, reason_header = v4.layer, v4.shadow_card, v4.number_badge, v4.reason_header
LINE, SOFT, RED, RED_L = v4.LINE, v4.SOFT, v4.RED, v4.RED_L
SKEL = (226, 232, 240)


def bo(x):
    """back_out que vale 0 exacto antes de empezar (evita líneas fantasma)."""
    return 0.0 if x <= 0 else back_out(x)
GREEN = (37, 211, 102)

T = dict(hook=0.0, tres=2.7, uno=6.2, dos=11.55, tres_r=15.85, cta=20.6)  # sincronizado con voz Diego
DURATION = 27.0
RED_NET = "instagram"


def phone(img, cx, cy, p, pw=520, ph=900, tilt=0.0):
    """Teléfono vacío; devuelve el área de la pantalla y la capa para dibujar encima."""
    a = ease_out(p)
    x0, y0 = cx - pw / 2, cy - ph / 2 + (1 - a) * 240
    lay = layer()
    shadow_card(lay, (x0 + 10, y0 + 20, x0 + pw - 10, y0 + ph), 72, a, 60, 40)
    d = ImageDraw.Draw(lay)
    a8 = int(255 * a)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=72, fill=(17, 24, 39, a8))
    s = (x0 + 18, y0 + 18, x0 + pw - 18, y0 + ph - 18)
    d.rounded_rectangle(s, radius=56, fill=WHITE + (a8,))
    d.rounded_rectangle([cx - 62, y0 + 32, cx + 62, y0 + 64], radius=16, fill=(17, 24, 39, a8))
    return lay, d, s, a8


def web_skeleton(d, s, a8, y_start=110, scale=1.0, dx=0):
    x0, y0, x1, y1 = s
    x0 += dx
    w = (x1 - s[0]) * scale
    d.rounded_rectangle([x0 + 30, y0 + y_start, x0 + 30 + w * 0.35, y0 + y_start + 34], radius=12, fill=TURQ + (a8,))
    d.rounded_rectangle([x0 + 30, y0 + y_start + 70, x0 + 30 + (w - 60), y0 + y_start + 330], radius=26, fill=blend(TURQ_L, TURQ, 0.25) + (a8,))
    for i in range(3):
        yy = y0 + y_start + 370 + i * 50
        d.rounded_rectangle([x0 + 30, yy, x0 + 30 + (w - 60) * (0.9 - i * 0.2), yy + 26], radius=13, fill=SKEL + (a8,))


# ---------------- escenas ----------------
def scene_hook(img, t):
    a = ease_out(t / 0.45)
    fade_text(img, W / 2, 170, "¿Tu página web", font("Inter-Light.otf", 88), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 280, "espanta clientes?", font("Inter-Bold.otf", 104), DEEP, a, dy=(1 - a) * 30)
    lay, d, s, a8 = phone(img, W / 2 - 60, 1130, clamp((t - 0.15) / 0.7))
    web_skeleton(d, s, a8)
    img.alpha_composite(lay)
    # clientes que se van
    for i in range(3):
        p = ease_out((t - 0.9 - i * 0.25) / 0.9)
        if p <= 0:
            continue
        lay = layer()
        d = ImageDraw.Draw(lay)
        cx = 800 + p * 260 + i * 10
        cy = 900 + i * 210
        al = int(255 * clamp(1.4 - p))
        d.ellipse([cx - 34, cy - 90, cx + 34, cy - 22], fill=DEEP + (al,))
        d.rounded_rectangle([cx - 58, cy - 12, cx + 58, cy + 90], radius=50, fill=DEEP + (al,))
        img.alpha_composite(lay)
    p = bo(clamp((t - 1.5) / 0.5))
    if p > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        cx, cy, r = 850, 620, 86 * p
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        if p > 0.7:
            text_center(d, cx, cy - 60, "!", font("Inter-Bold.otf", 104), WHITE)
        img.alpha_composite(lay)


def scene_tres(img, t):
    local = t - T["tres"]
    p = bo(local / 0.5)
    lay = layer()
    text_center(ImageDraw.Draw(lay), W / 2, 470, "3", font("Inter-Bold.otf", int(max(1, 420 * p))), DEEP)
    img.alpha_composite(lay)
    a = ease_out((local - 0.25) / 0.4)
    fade_text(img, W / 2, 1000, "errores muy", font("Inter-Light.otf", 80), GREY, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 0.45) / 0.4)
    fade_text(img, W / 2, 1110, "comunes", font("Inter-Bold.otf", 110), RED, a2, dy=(1 - a2) * 30)


def scene_uno(img, t):
    local = t - T["uno"]
    reason_header(img, local, 1, "Tarda en", "cargar")
    lay, d, s, a8 = phone(img, W / 2, 1180, clamp((local - 0.2) / 0.6), pw=500, ph=820)
    x0, y0, x1, y1 = s
    cx, cy = (x0 + x1) / 2, y0 + 300
    # rueda de carga
    ang = local * 300
    for k in range(10):
        th = math.radians(ang + k * 36)
        al = int(a8 * (0.15 + 0.85 * k / 9))
        px, py = cx + math.cos(th) * 70, cy + math.sin(th) * 70
        d.ellipse([px - 13, py - 13, px + 13, py + 13], fill=TURQ + (al,))
    # contador de segundos
    secs = clamp((local - 0.6) / 4.0) * 5.0
    col = RED if secs >= 3 else DEEP
    text_center(d, cx, cy + 140, f"{secs:.1f} s", font("Inter-Bold.otf", 76), col + (a8,))
    bw = (x1 - x0) - 100
    d.rounded_rectangle([x0 + 50, cy + 270, x0 + 50 + bw, cy + 296], radius=13, fill=SKEL + (a8,))
    d.rounded_rectangle([x0 + 50, cy + 270, x0 + 50 + bw * min(1, secs / 5) + 1, cy + 296], radius=13, fill=col + (a8,))
    img.alpha_composite(lay)
    a2 = ease_out((local - 2.6) / 0.5)
    if a2 > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        y = 1650 + (1 - a2) * 30
        d.rounded_rectangle([W / 2 - 330, y, W / 2 + 330, y + 120], radius=60, fill=RED + (int(255 * a2),))
        text_center(d, W / 2, y + 30, "El cliente se va", font("Inter-SemiBold.otf", 54), WHITE + (int(255 * a2),))
        img.alpha_composite(lay)


def scene_dos(img, t):
    local = t - T["dos"]
    reason_header(img, local, 2, "No se ve bien", "en el teléfono")
    lay, d, s, a8 = phone(img, W / 2, 1150, clamp((local - 0.2) / 0.6), pw=500, ph=880)
    x0, y0, x1, y1 = s
    # web de computadora metida a la fuerza: se sale de la pantalla
    off = clamp((local - 0.9) / 0.8)
    clip = layer()
    cd = ImageDraw.Draw(clip)
    web_skeleton(cd, (x0, y0, x1, y1), a8, y_start=90, scale=1.0 + 0.7 * off, dx=-20 * off)
    mtxt = "Bienvenidos a nuestro negocio"
    cd.text((x0 + 30, y0 + 660), mtxt, font=font("Inter-Bold.otf", int(34 + 14 * off)), fill=DEEP + (a8,))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle(s, radius=56, fill=255)
    lay.paste(clip, (0, 0), Image.composite(clip, Image.new("RGBA", (W, H)), mask).split()[3])
    img.alpha_composite(lay)
    p = bo(clamp((local - 2.0) / 0.5))
    if p > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        cx, cy, r = x1 - 10, y0 + 40, 60 * p
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        if p > 0.7:
            d.line([cx - 22, cy - 22, cx + 22, cy + 22], fill=WHITE, width=10)
            d.line([cx - 22, cy + 22, cx + 22, cy - 22], fill=WHITE, width=10)
        img.alpha_composite(lay)


def chat_icon(d, cx, cy, s, col):
    d.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], outline=col, width=max(4, int(s * 0.1)))
    d.polygon([(cx - s * 0.42, cy + s * 0.2), (cx - s * 0.5, cy + s * 0.52), (cx - s * 0.15, cy + s * 0.42)], fill=col)


def scene_tres_r(img, t):
    local = t - T["tres_r"]
    reason_header(img, local, 3, "Sin botón de", "WhatsApp")
    # número para copiar a mano
    p = ease_out((local - 0.3) / 0.5)
    if p > 0:
        lay = layer()
        box = (150, 680, W - 150, 900)
        shadow_card(lay, box, 40, p)
        d = ImageDraw.Draw(lay)
        a8 = int(255 * p)
        d.rounded_rectangle(box, radius=40, fill=SOFT + (a8,), outline=LINE + (a8,), width=3)
        d.text((210, 715), "Llámanos al", font=font("Inter-Regular.otf", 40), fill=GREY + (a8,))
        d.text((210, 775), "0412-000-0000", font=font("Inter-Bold.otf", 70), fill=DEEP + (a8,))
        st = clamp((local - 1.6) / 0.5)
        if st > 0:
            d.line([200, 815, 200 + (W - 400) * st, 815], fill=RED + (a8,), width=10)
        img.alpha_composite(lay)
    a2 = ease_out((local - 1.9) / 0.4)
    fade_text(img, W / 2, 930, "Nadie lo copia a mano", font("Inter-SemiBold.otf", 50), RED, a2)
    # botón correcto
    p2 = bo(clamp((local - 2.9) / 0.6))
    if p2 > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        bw, bh = 760 * p2, 170
        y = 1250
        shadow_card(lay, (W / 2 - bw / 2, y, W / 2 + bw / 2, y + bh), 85, 1, 50)
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle([W / 2 - bw / 2, y, W / 2 + bw / 2, y + bh], radius=85, fill=GREEN)
        if p2 > 0.85:
            chat_icon(d, W / 2 - 250, y + bh / 2, 70, WHITE)
            d.text((W / 2 - 180, y + 50), "Escríbenos ya", font=font("Inter-Bold.otf", 64), fill=WHITE)
        img.alpha_composite(lay)
        a3 = ease_out((local - 3.6) / 0.4)
        fade_text(img, W / 2, 1480, "Un toque y te escriben", font("Inter-Medium.otf", 50), TURQ, a3)


def scene_cta(img, t):
    local = t - T["cta"]
    bg_a = ease_out(local / 0.45)
    img.alpha_composite(Image.new("RGBA", img.size, DEEP + (int(255 * bg_a),)))
    a = ease_out((local - 0.15) / 0.5)
    fade_text(img, W / 2, 380, "¿Tu web tiene", font("Inter-Light.otf", 92), TURQ_L, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 500, "alguno?", font("Inter-Bold.otf", 104), WHITE, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 1.4) / 0.5)
    if a2 > 0:
        lay = layer()
        d = ImageDraw.Draw(lay)
        bw, bh = 640, 140
        x, y = W / 2 - bw / 2, 720 + (1 - a2) * 40
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=70, fill=TURQ + (int(255 * a2),))
        text_center(d, W / 2, y + 36, "Escríbeme", font("Inter-SemiBold.otf", 56), WHITE + (int(255 * a2),))
        img.alpha_composite(lay)
    a3 = ease_out((local - 1.9) / 0.5)
    sub = "Enlace en la biografía" if RED_NET == "instagram" else "Escríbeme por mensaje directo"
    fade_text(img, W / 2, 900, sub, font("Inter-Regular.otf", 50), TURQ_L, a3)
    a4 = ease_out((local - 2.3) / 0.5)
    fade_text(img, W / 2, 1010, "Soy Angel, de Lumen", font("Inter-Light.otf", 46), WHITE, a4)
    draw_logo(img, W / 2 - 170, 1390, 200, clamp((local - 2.6) / 0.8), clamp((local - 3.1) / 0.5), color=WHITE, dot=TURQ)
    a5 = ease_out((local - 2.9) / 0.5)
    lay = layer()
    d = ImageDraw.Draw(lay)
    d.text((W / 2 - 50, 1312), "lumen", font=font("Inter-Light.otf", 96), fill=WHITE + (int(255 * a5),))
    d.text((W / 2 - 46, 1430), "WEB DESIGN", font=font("Inter-Medium.otf", 32), fill=TURQ + (int(255 * a5),))
    img.alpha_composite(lay)
    a6 = ease_out((local - 3.6) / 0.6)
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


def main(out, start=0, end=None):
    end = end or int(DURATION * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                          "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", out], stdin=subprocess.PIPE)
    for i in range(start, end):
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
        if len(sys.argv) > 3:
            RED_NET = sys.argv[3]
        a = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        b = int(sys.argv[5]) if len(sys.argv) > 5 else None
        main(sys.argv[2], a, b)
