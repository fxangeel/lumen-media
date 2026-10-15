"""Reel 3 – ¿Cuánto cuesta una página web? (1080x1920, 30 fps)."""
import math, subprocess, sys, random
sys.path.insert(0, "/home/claude/lumen/video1")
from PIL import Image, ImageDraw, ImageFilter
from render import (W, H, FPS, OFF, DEEP, TURQ, TURQ_L, GREY, WHITE, font, clamp, ease_out,
                    ease_in_out, back_out, blend, fade_text, draw_logo, background, text_center)

LINE = (226, 232, 240)
SOFT = (240, 247, 246)

T_INTRO, T_CARDS, T_CUSTOM, T_CTA = 3.4, 4.9, 24.2, 28.4
DURATION = 33.0

def layer_new():
    return Image.new("RGBA", (W, H), DEEP + (0,))

def scene_hook(img, t):
    a = ease_out(t / 0.4)
    fade_text(img, W / 2, 360, "¿Cuánto cuesta", font("Inter-Light.otf", 96), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 480, "una página web?", font("Inter-Bold.otf", 110), DEEP, a, dy=(1 - a) * 30)
    # price tag with rolling digits
    p = back_out((t - 0.3) / 0.5)
    if p > 0:
        lay = layer_new()
        d = ImageDraw.Draw(lay)
        cx, cy = W / 2, 900
        w, h = 520 * p, 230 * p
        d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=40 * p, fill=TURQ)
        d.ellipse([cx - w / 2 + 34 * p, cy - 18 * p, cx - w / 2 + 70 * p, cy + 18 * p], fill=OFF)
        if p > 0.8:
            random.seed(int(t * 14))
            txt = "$" + "".join(random.choice("0123456789") for _ in range(3)) if t < 1.9 else "$ ?"
            text_center(d, cx + 20, cy - 70, txt, font("Inter-Bold.otf", 120), WHITE)
        img.alpha_composite(lay)
    a2 = ease_out((t - 2.05) / 0.45)
    fade_text(img, W / 2, 1120, "Menos de lo", font("Inter-Light.otf", 84), GREY, a2, dy=(1 - a2) * 30)
    fade_text(img, W / 2, 1220, "que piensas", font("Inter-Bold.otf", 96), TURQ, a2, dy=(1 - a2) * 30)

def scene_intro(img, t):
    local = t - T_INTRO
    p = back_out(local / 0.5)
    lay = layer_new()
    d = ImageDraw.Draw(lay)
    f = font("Inter-Bold.otf", int(max(1, 420 * p)))
    text_center(d, W / 2, 600, "3", f, DEEP)
    img.alpha_composite(lay)
    a = ease_out((local - 0.25) / 0.4)
    fade_text(img, W / 2, 1100, "paquetes", font("Inter-Light.otf", 110), TURQ, a, dy=(1 - a) * 30)

CARDS = [  # name, price, start, lines(start offset), badge
    ("Básico", "65", 5.0, [("Página informativa", 7.6), ("Todo tu negocio en un lugar", 8.4)], None),
    ("Intermedio", "85", 10.8, [("Todo lo del Básico", 11.6), ("+ Pedidos o reservas", 13.15)], None),
    ("Completo", "135", 16.1, [("Reservas con calendario", 19.05), ("Panel de control", 20.2)], ("Dominio gratis 1er año", 21.55)),
]
CARD_Y = [430, 830, 1230]
CARD_H = 360

def active_index(t):
    idx = -1
    for i, c in enumerate(CARDS):
        if t >= c[2]:
            idx = i
    return idx

def scene_cards(img, t):
    local = t - T_CARDS
    a = ease_out(local / 0.4)
    fade_text(img, W / 2, 230, "Paquetes", font("Inter-Light.otf", 72), GREY, a)
    fade_text(img, W / 2, 310, "Lumen Web Design", font("Inter-Bold.otf", 64), DEEP, a)
    act = active_index(t)
    for i, (name, price, st, lines, badge) in enumerate(CARDS):
        p = ease_out((t - st) / 0.5)
        if p <= 0:
            continue
        hi = 1.0 if i == act else 0.0
        # smooth highlight transitions
        if i == act and i > 0:
            hi = ease_out((t - st) / 0.4)
        elif i < act:
            hi = 1 - ease_out((t - CARDS[act][2]) / 0.4)
        lay = layer_new()
        d = ImageDraw.Draw(lay)
        x0, x1 = 90 + (1 - p) * 140, W - 90 + (1 - p) * 140
        y0 = CARD_Y[i]
        a8 = int(255 * p)
        bg = blend(WHITE, DEEP, hi)
        sh = layer_new()
        ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 24, x1, y0 + CARD_H + 24], radius=44, fill=DEEP + (int(35 * p),))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle([x0, y0, x1, y0 + CARD_H], radius=44, fill=bg + (a8,),
                            outline=blend(LINE, DEEP, hi) + (a8,), width=3)
        tc = blend(DEEP, WHITE, hi)
        sc = blend(GREY, TURQ_L, hi)
        d.text((x0 + 60, y0 + 50), name, font=font("Inter-Bold.otf", 64), fill=tc + (a8,))
        # price block right
        pf = font("Inter-Bold.otf", 96)
        pw = d.textlength(price + " $", font=pf)
        d.text((x1 - 60 - pw, y0 + 34), price + " $", font=pf, fill=blend(TURQ, TURQ, hi) + (a8,))
        df = font("Inter-Regular.otf", 34)
        dw = d.textlength("desde", font=df)
        d.text((x1 - 60 - pw - dw - 18, y0 + 84), "desde", font=df, fill=sc + (a8,))
        # feature lines
        for j, (ln, ls) in enumerate(lines):
            lp = ease_out((t - ls) / 0.4)
            if lp <= 0:
                continue
            la = int(255 * lp * p)
            yy = y0 + 170 + j * 70 + (1 - lp) * 20
            d.ellipse([x0 + 62, yy + 14, x0 + 84, yy + 36], fill=TURQ + (la,))
            d.text((x0 + 106, yy), ln, font=font("Inter-Medium.otf", 42), fill=tc + (la,))
        if badge:
            bp = back_out((t - badge[1]) / 0.5)
            if bp > 0:
                bf = font("Inter-SemiBold.otf", 34)
                bw = d.textlength(badge[0], font=bf) + 70
                bx, by = x1 - 40 - bw, y0 - 30
                d.rounded_rectangle([bx, by, bx + bw * bp, by + 70], radius=35, fill=TURQ + (a8,))
                if bp > 0.9:
                    d.text((bx + 35, by + 14), badge[0], font=bf, fill=WHITE + (a8,))
        img.alpha_composite(lay)

def scene_custom(img, t):
    local = t - T_CUSTOM
    a = ease_out(local / 0.45)
    fade_text(img, W / 2, 470, "Cada negocio", font("Inter-Light.otf", 96), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 585, "es distinto", font("Inter-Bold.otf", 110), DEEP, a, dy=(1 - a) * 30)
    # sliders
    labels = ["Secciones", "Funciones", "Diseño"]
    targets = [0.62, 0.38, 0.8]
    for i, (lb, tg) in enumerate(zip(labels, targets)):
        sp = ease_out((local - 0.3 - i * 0.15) / 0.4)
        if sp <= 0:
            continue
        lay = layer_new()
        d = ImageDraw.Draw(lay)
        a8 = int(255 * sp)
        y = 860 + i * 150
        x0, x1 = 180, W - 180
        d.text((x0, y - 60), lb, font=font("Inter-Medium.otf", 40), fill=GREY + (a8,))
        d.rounded_rectangle([x0, y, x1, y + 16], radius=8, fill=LINE + (a8,))
        v = 0.15 + (tg - 0.15) * ease_in_out((local - 0.6 - i * 0.2) / 1.2) + 0.04 * math.sin(local * 2 + i)
        xv = x0 + (x1 - x0) * clamp(v)
        d.rounded_rectangle([x0, y, xv, y + 16], radius=8, fill=TURQ + (a8,))
        d.ellipse([xv - 26, y - 18, xv + 26, y + 34], fill=WHITE + (a8,), outline=TURQ + (a8,), width=6)
        img.alpha_composite(lay)
    a2 = ease_out((local - 1.8) / 0.5)
    fade_text(img, W / 2, 1330, "Precio final", font("Inter-Light.otf", 80), GREY, a2, dy=(1 - a2) * 30)
    fade_text(img, W / 2, 1430, "a tu medida", font("Inter-Bold.otf", 96), TURQ, a2, dy=(1 - a2) * 30)

def scene_cta(img, t):
    local = t - T_CTA
    bg_a = ease_out(local / 0.45)
    img.alpha_composite(Image.new("RGBA", img.size, DEEP + (int(255 * bg_a),)))
    a = ease_out((local - 0.15) / 0.5)
    fade_text(img, W / 2, 470, "Cotización", font("Inter-Bold.otf", 110), WHITE, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 600, "sin compromiso", font("Inter-Light.otf", 92), TURQ_L, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 0.3) / 0.5)
    if a2 > 0:
        lay = layer_new()
        d = ImageDraw.Draw(lay)
        bw, bh = 640, 140
        x, y = W / 2 - bw / 2, 790 + (1 - a2) * 40
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=70, fill=TURQ + (int(255 * a2),))
        text_center(d, W / 2, y + 36, "Escríbeme", font("Inter-SemiBold.otf", 56), WHITE + (int(255 * a2),))
        img.alpha_composite(lay)
    a3 = ease_out((local - 0.8) / 0.5)
    fade_text(img, W / 2, 970, "Enlace en la biografía", font("Inter-Regular.otf", 50), TURQ_L, a3)
    draw_logo(img, W / 2 - 170, 1340, 200, clamp((local - 1.6) / 0.8), clamp((local - 2.1) / 0.5), color=WHITE, dot=TURQ)
    a4 = ease_out((local - 1.9) / 0.5)
    lay = layer_new()
    d = ImageDraw.Draw(lay)
    d.text((W / 2 - 50, 1262), "lumen", font=font("Inter-Light.otf", 96), fill=WHITE + (int(255 * a4),))
    d.text((W / 2 - 46, 1380), "WEB DESIGN", font=font("Inter-Medium.otf", 32), fill=TURQ + (int(255 * a4),))
    img.alpha_composite(lay)
    a5 = ease_out((local - 2.6) / 0.6)
    fade_text(img, W / 2, 1600, "Le damos luz a tu negocio", font("Inter-Light.otf", 60), WHITE, a5)

SCENES = [(0, T_INTRO, scene_hook), (T_INTRO, T_CARDS, scene_intro), (T_CARDS, T_CUSTOM, scene_cards),
          (T_CUSTOM, T_CTA, scene_custom), (T_CTA, DURATION + 1, scene_cta)]

def frame(t):
    img = background(t)
    for s, e, fn in SCENES:
        if s <= t < e:
            base = img.copy()
            fn(base, t)
            out = clamp((e - t) / 0.3) if fn is not scene_cta and fn is not scene_custom else 1.0
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
        ims = [frame(t).resize((270, 480)) for t in ts]
        s = Image.new("RGB", (280 * len(ims), 480), "white")
        for i, im in enumerate(ims):
            s.paste(im, (i * 280, 0))
        s.save("/home/claude/lumen/video3/check.png")
    else:
        main(sys.argv[2])
