"""Reel 2 – Así se ve una web moderna en el teléfono (1080x1920, 30 fps)."""
import math, subprocess, sys
sys.path.insert(0, "/home/claude/lumen/video1")
from PIL import Image, ImageDraw, ImageFilter
import render as base
from render import (W, H, FPS, OFF, DEEP, TURQ, TURQ_L, GREY, WHITE, font, clamp, ease_out,
                    ease_in_out, back_out, blend, fade_text, draw_logo, background, text_center)

GREEN = (37, 211, 102)
LINE = (226, 232, 240)
SOFT = (240, 247, 246)

# ---------------- website (fictional café) ----------------
SW = 560
SEC = {"hero": 0, "menu": 720, "map": 1500, "order": 2160}

def build_site():
    s = Image.new("RGB", (SW, 2900), WHITE)
    d = ImageDraw.Draw(s)
    # nav
    d.rounded_rectangle([28, 30, 58, 60], radius=8, fill=DEEP)
    d.ellipse([46, 30, 60, 44], fill=TURQ)
    d.text((72, 30), "Café Aurora", font=font("Inter-SemiBold.otf", 26), fill=DEEP)
    for i in range(3):
        d.rounded_rectangle([SW - 60, 34 + i * 10, SW - 28, 38 + i * 10], radius=2, fill=DEEP)
    # hero gradient
    hero = Image.new("RGB", (SW, 620))
    hp = hero.load()
    for y in range(620):
        for x in range(0, SW, 4):
            c = blend(DEEP, TURQ, x / SW * 0.6 + y / 620 * 0.4)
            for k in range(4):
                if x + k < SW:
                    hp[x + k, y] = c
    s.paste(hero, (0, 90))
    d.text((40, 230), "Café Aurora", font=font("Inter-Bold.otf", 62), fill=WHITE)
    d.text((40, 312), "Café de especialidad", font=font("Inter-Light.otf", 40), fill=WHITE)
    d.text((40, 360), "y pan recién hecho", font=font("Inter-Light.otf", 40), fill=WHITE)
    d.rounded_rectangle([40, 470, 250, 536], radius=33, fill=WHITE)
    text_center(d, 145, 485, "Ver menú", font("Inter-SemiBold.otf", 26), DEEP)
    d.rounded_rectangle([270, 470, 470, 536], radius=33, outline=WHITE, width=3)
    text_center(d, 370, 485, "Reservar", font("Inter-SemiBold.otf", 26), WHITE)
    # menu
    y = SEC["menu"] + 30
    d.text((40, y), "Menú", font=font("Inter-Bold.otf", 44), fill=DEEP)
    d.rounded_rectangle([SW - 190, y + 6, SW - 40, y + 50], radius=22, fill=SOFT)
    text_center(d, SW - 115, y + 14, "Actualizado", font("Inter-Medium.otf", 20), TURQ)
    items = [("Cappuccino", "2,50 $"), ("Latte de vainilla", "3,00 $"), ("Croissant", "1,80 $"),
             ("Pan de guayaba", "1,50 $"), ("Torta de chocolate", "3,20 $"), ("Jugo natural", "2,00 $")]
    y += 90
    for i, (n, p) in enumerate(items):
        d.rounded_rectangle([40, y, SW - 40, y + 96], radius=20, fill=SOFT)
        d.rounded_rectangle([54, y + 14, 122, y + 82], radius=14, fill=blend(TURQ_L, TURQ, 0.2 + 0.15 * (i % 3)))
        d.text((142, y + 20), n, font=font("Inter-SemiBold.otf", 26), fill=DEEP)
        d.text((142, y + 54), "Ver detalles", font=font("Inter-Regular.otf", 18), fill=GREY)
        pw = d.textlength(p, font=font("Inter-Bold.otf", 26))
        d.text((SW - 60 - pw, y + 34), p, font=font("Inter-Bold.otf", 26), fill=TURQ)
        y += 110
    # map
    y = SEC["map"] + 30
    d.text((40, y), "Encuéntranos", font=font("Inter-Bold.otf", 44), fill=DEEP)
    my = y + 80
    m = Image.new("RGB", (SW - 80, 420), (233, 240, 238))
    md = ImageDraw.Draw(m)
    md.rectangle([0, 0, SW - 80, 90], fill=(206, 236, 241))          # sea
    md.rectangle([300, 230, 470, 330], fill=(214, 238, 222))         # park
    for (a, b) in [((0, 180), (480, 160)), ((150, 90), (170, 420)), ((0, 330), (480, 360)), ((330, 90), (300, 420))]:
        md.line([a, b], fill=WHITE, width=22)
    md.line([(0, 250), (480, 270)], fill=WHITE, width=12)
    mask = Image.new("L", m.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, m.width - 1, m.height - 1], radius=24, fill=255)
    s.paste(m, (40, my), mask)
    d.text((40, my + 440), "Calle Principal #12", font=font("Inter-SemiBold.otf", 26), fill=DEEP)
    d.text((40, my + 476), "Abierto hoy · 7:00 am – 8:00 pm", font=font("Inter-Regular.otf", 22), fill=GREY)
    # order
    y = SEC["order"] + 30
    d.text((40, y), "Haz tu pedido", font=font("Inter-Bold.otf", 44), fill=DEEP)
    y += 90
    d.rounded_rectangle([40, y, SW - 40, y + 400], radius=24, fill=SOFT)
    rows = [("Cappuccino", "x2", "5,00 $"), ("Croissant", "x1", "1,80 $")]
    yy = y + 30
    for n, q, p in rows:
        d.text((70, yy), n, font=font("Inter-SemiBold.otf", 28), fill=DEEP)
        d.text((330, yy), q, font=font("Inter-Medium.otf", 28), fill=GREY)
        pw = d.textlength(p, font=font("Inter-SemiBold.otf", 28))
        d.text((SW - 70 - pw, yy), p, font=font("Inter-SemiBold.otf", 28), fill=DEEP)
        yy += 64
    d.line([70, yy + 6, SW - 70, yy + 6], fill=LINE, width=2)
    d.text((70, yy + 26), "Total", font=font("Inter-Bold.otf", 30), fill=DEEP)
    pw = d.textlength("6,80 $", font=font("Inter-Bold.otf", 30))
    d.text((SW - 70 - pw, yy + 26), "6,80 $", font=font("Inter-Bold.otf", 30), fill=TURQ)
    ORDER_BTN = (70, y + 290, SW - 70, y + 366)
    d.rounded_rectangle(ORDER_BTN, radius=38, fill=DEEP)
    text_center(d, SW / 2, y + 310, "Enviar pedido", font("Inter-SemiBold.otf", 30), WHITE)
    return s, {"map_pin": (40 + 225, my + 205), "order_btn": ORDER_BTN}

SITE, SPOTS = build_site()

# ---------------- phone ----------------
PW, PH = 600, 1160
SCR_W, SCR_H = PW - 40, PH - 40

def phone_frame(img, cx, cy, alpha, scale=1.0):
    """Draws phone body; returns screen origin (sx, sy) and scale."""
    pw, ph = PW * scale, PH * scale
    x0, y0 = cx - pw / 2, cy - ph / 2
    sh = Image.new("RGBA", img.size, DEEP + (0,))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 10, y0 + 40, x0 + pw - 10, y0 + ph + 30], radius=80 * scale,
                                          fill=DEEP + (int(70 * alpha),))
    sh = sh.filter(ImageFilter.GaussianBlur(40))
    img.alpha_composite(sh)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=80 * scale, fill=(17, 24, 39, int(255 * alpha)))
    return x0 + 20 * scale, y0 + 20 * scale

def screen_image(scroll_px):
    off = int(clamp(scroll_px, 0, SITE.height - SCR_H))
    return SITE.crop((0, off, SW, off + SCR_H)).convert("RGBA"), off

def place_screen(img, scr, sx, sy, alpha, scale=1.0):
    if scale != 1.0:
        scr = scr.resize((int(SCR_W * scale), int(SCR_H * scale)), Image.LANCZOS)
    mask = Image.new("L", scr.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, scr.width - 1, scr.height - 1], radius=int(62 * scale),
                                           fill=int(255 * alpha))
    img.paste(scr, (int(sx), int(sy)), mask)

def notch(img, cx, top, alpha, scale=1.0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - 70 * scale, top + 36 * scale, cx + 70 * scale, top + 72 * scale],
                        radius=18 * scale, fill=(17, 24, 39, int(255 * alpha)))

def ripple(layer, x, y, p):
    if 0 < p < 1:
        d = ImageDraw.Draw(layer)
        r = 20 + 70 * ease_out(p)
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE + (int(110 * (1 - p)),))
        d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(255, 255, 255, int(160 * (1 - p))))

def chat_icon(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=max(3, r // 6))
    d.polygon([(cx - r * 0.75, cy + r * 0.55), (cx - r * 0.95, cy + r * 1.05), (cx - r * 0.3, cy + r * 0.85)], fill=color)

def check(d, cx, cy, s, color, w=6):
    d.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.6)], fill=color, width=w, joint="curve")

# ---------------- timeline (s) ----------------
T_HOOK_END = 4.0
T_PHONE = 4.0
T_MENU, T_WA, T_MAP, T_ORDER = 8.2, 11.15, 14.55, 17.75
T_MODERN = 20.3
T_CTA = 22.2
DURATION = 28.2

HEADLINES = [  # (start, top line, bottom line)
    (T_PHONE, "Perfecta en", "pantalla pequeña"),
    (T_MENU, "Menú o catálogo", "siempre actualizado"),
    (T_WA, "WhatsApp", "en un solo toque"),
    (T_MAP, "Tu ubicación", "en el mapa"),
    (T_ORDER, "Pedidos y reservas", "en segundos"),
]

def scroll_at(t):
    keys = [(T_PHONE, 0), (T_MENU - 0.1, 0), (T_MENU + 0.7, SEC["menu"]), (T_WA - 0.1, SEC["menu"]),
            (T_WA + 0.6, SEC["menu"] + 120), (T_MAP - 0.1, SEC["menu"] + 120), (T_MAP + 0.6, SEC["map"]),
            (T_ORDER - 0.1, SEC["map"]), (T_ORDER + 0.7, SEC["order"] - 120), (T_MODERN, SEC["order"] - 120)]
    if t <= keys[0][0]:
        return 0
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * ease_in_out((t - t0) / max(0.001, t1 - t0))
    return keys[-1][1]

def headline(img, t):
    for i, (s, a, b) in enumerate(HEADLINES):
        e = HEADLINES[i + 1][0] if i + 1 < len(HEADLINES) else T_MODERN
        if s - 0.05 <= t < e:
            local = t - s
            fin = ease_out(local / 0.45)
            fout = clamp((e - t) / 0.25)
            al = fin * fout
            fade_text(img, W / 2, 175, a, font("Inter-Light.otf", 78), GREY, al, dy=(1 - fin) * 30)
            fade_text(img, W / 2, 270, b, font("Inter-Bold.otf", 92), DEEP, al, dy=(1 - fin) * 30)

# ---------------- scenes ----------------
def scene_hook(img, t):
    a = ease_out(t / 0.4)
    fade_text(img, W / 2, 380, "¿Tus clientes te buscan", font("Inter-Light.otf", 74), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 470, "desde el teléfono?", font("Inter-Bold.otf", 98), DEEP, a, dy=(1 - a) * 30)
    # search bar
    p = ease_out((t - 0.4) / 0.5)
    if p <= 0:
        return
    layer = Image.new("RGBA", img.size, DEEP + (0,))
    d = ImageDraw.Draw(layer)
    bw, bh = 860, 130
    x0, y0 = W / 2 - bw / 2, 760 + (1 - p) * 40
    sh = Image.new("RGBA", img.size, DEEP + (0,))
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 20, x0 + bw, y0 + bh + 20], radius=65, fill=DEEP + (int(40 * p),))
    layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=65, fill=WHITE + (int(255 * p),))
    # magnifier
    cx, cy = x0 + 75, y0 + bh / 2 - 6
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=TURQ + (int(255 * p),), width=7)
    d.line([cx + 15, cy + 15, cx + 34, cy + 34], fill=TURQ + (int(255 * p),), width=8)
    q = "panadería cerca de mí"
    n = int(len(q) * clamp((t - 0.9) / 1.4))
    f = font("Inter-Regular.otf", 52)
    d.text((x0 + 130, y0 + 34), q[:n], font=f, fill=DEEP + (int(255 * p),))
    if int(t * 2.5) % 2 == 0 or n < len(q):
        cxp = x0 + 132 + d.textlength(q[:n], font=f)
        d.rectangle([cxp, y0 + 36, cxp + 4, y0 + 96], fill=TURQ + (int(255 * p),))
    img.alpha_composite(layer)
    # results skeleton
    for i in range(3):
        rp = ease_out((t - 2.5 - i * 0.22) / 0.4)
        if rp <= 0:
            continue
        lay = Image.new("RGBA", img.size, DEEP + (0,))
        dd = ImageDraw.Draw(lay)
        ry = 960 + i * 190 + (1 - rp) * 40
        a8 = int(255 * rp)
        dd.rounded_rectangle([x0, ry, x0 + bw, ry + 160], radius=32, fill=WHITE + (a8,), outline=LINE + (a8,), width=2)
        dd.rounded_rectangle([x0 + 30, ry + 30, x0 + 130, ry + 130], radius=20,
                             fill=(blend(TURQ_L, TURQ, 0.3) if i == 0 else SOFT) + (a8,))
        dd.rounded_rectangle([x0 + 160, ry + 42, x0 + 160 + (420 if i == 0 else 360), ry + 66], radius=12,
                             fill=(DEEP if i == 0 else (203, 213, 225)) + (a8,))
        dd.rounded_rectangle([x0 + 160, ry + 90, x0 + 160 + 260, ry + 110], radius=10, fill=(226, 232, 240, a8))
        if i == 0:
            dd.rounded_rectangle([x0 + bw - 190, ry + 50, x0 + bw - 30, ry + 110], radius=30, fill=TURQ + (a8,))
            text_center(dd, x0 + bw - 110, ry + 62, "Tu web", font("Inter-SemiBold.otf", 30), WHITE + (a8,))
        img.alpha_composite(lay)

def scene_phone(img, t):
    local = t - T_PHONE
    appear = ease_out(local / 0.8)
    cx, cy = W / 2, 1150 + (1 - appear) * 380
    headline(img, t)
    layer = Image.new("RGBA", img.size, DEEP + (0,))
    sx, sy = phone_frame(layer, cx, cy, appear)
    scr, off = screen_image(scroll_at(t))
    sd = ImageDraw.Draw(scr)
    # --- overlays on the screen (screen coords) ---
    # WhatsApp-style floating button
    if t >= T_WA - 0.1:
        p = back_out((t - T_WA) / 0.5)
        r = 52 * p
        fx, fy = SCR_W - 90, SCR_H - 110
        if r > 0:
            sd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=GREEN)
            if p > 0.6:
                chat_icon(sd, fx, fy - 4, int(24 * p), WHITE)
        tp = (t - (T_WA + 1.1)) / 0.6
        ripple(scr, fx, fy, tp)
        cp = ease_out((t - (T_WA + 1.5)) / 0.5) * clamp((T_MAP + 0.1 - t) / 0.3)
        if cp > 0:
            card = Image.new("RGBA", scr.size, DEEP + (0,))
            cd = ImageDraw.Draw(card)
            by = SCR_H - 330 + (1 - cp) * 40
            cd.rounded_rectangle([40, by, SCR_W - 40, by + 170], radius=28, fill=WHITE + (int(250 * cp),),
                                 outline=LINE + (int(255 * cp),), width=2)
            cd.ellipse([66, by + 30, 126, by + 90], fill=GREEN + (int(255 * cp),))
            chat_icon(cd, 96, by + 57, 16, WHITE + (int(255 * cp),))
            cd.text((146, by + 30), "Café Aurora", font=font("Inter-SemiBold.otf", 26), fill=DEEP + (int(255 * cp),))
            cd.text((146, by + 64), "en línea", font=font("Inter-Regular.otf", 20), fill=GREEN + (int(255 * cp),))
            cd.rounded_rectangle([66, by + 106, SCR_W - 66, by + 150], radius=18, fill=(220, 248, 198, int(255 * cp)))
            cd.text((86, by + 114), "Hola, quiero hacer un pedido", font=font("Inter-Regular.otf", 22),
                    fill=DEEP + (int(255 * cp),))
            scr.alpha_composite(card)
    # map pin drop
    if t >= T_MAP + 0.6:
        p = clamp((t - (T_MAP + 0.6)) / 0.5)
        px, py = SPOTS["map_pin"]
        py = py - off - (1 - ease_out(p)) * 160
        sd.ellipse([px - 46, py - 120, px + 46, py - 28], fill=DEEP)
        sd.polygon([(px - 34, py - 54), (px + 34, py - 54), (px, py)], fill=DEEP)
        sd.ellipse([px - 18, py - 92, px + 18, py - 56], fill=TURQ)
        if p >= 1:
            pr = clamp((t - (T_MAP + 1.1)) / 0.9)
            rr = 20 + 60 * pr
            sd.ellipse([px - rr, py - rr * 0.35, px + rr, py + rr * 0.35], outline=TURQ + (int(200 * (1 - pr)),), width=4)
    # order tap + toast
    if t >= T_ORDER + 1.0:
        bx0, by0, bx1, by1 = SPOTS["order_btn"]
        tp = (t - (T_ORDER + 1.0)) / 0.6
        ripple(scr, (bx0 + bx1) / 2, (by0 + by1) / 2 - off, tp)
        tt = ease_out((t - (T_ORDER + 1.35)) / 0.45)
        if tt > 0:
            card = Image.new("RGBA", scr.size, DEEP + (0,))
            cd = ImageDraw.Draw(card)
            ty = 110 + (1 - tt) * -60
            a8 = int(255 * tt)
            cd.rounded_rectangle([40, ty, SCR_W - 40, ty + 120], radius=30, fill=DEEP + (a8,))
            cd.ellipse([66, ty + 28, 130, ty + 92], fill=TURQ + (a8,))
            check(cd, 98, ty + 62, 16, WHITE + (a8,), 6)
            cd.text((150, ty + 24), "¡Pedido enviado!", font=font("Inter-SemiBold.otf", 30), fill=WHITE + (a8,))
            cd.text((150, ty + 66), "Listo en 15 minutos", font=font("Inter-Regular.otf", 22), fill=TURQ_L + (a8,))
            scr.alpha_composite(card)
    place_screen(layer, scr, sx, sy, appear)
    notch(layer, cx, cy - PH / 2, appear)
    img.alpha_composite(layer)

def scene_modern(img, t):
    local = t - T_MODERN
    # phone shrinks & moves down while headline appears
    s = 1 - 0.18 * ease_in_out(local / 0.8)
    cx, cy = W / 2, 1150 + 90 * ease_in_out(local / 0.8)
    layer = Image.new("RGBA", img.size, DEEP + (0,))
    sx, sy = phone_frame(layer, cx, cy, 1.0, s)
    scr, off = screen_image(0)
    place_screen(layer, scr, sx, sy, 1.0, s)
    notch(layer, cx, cy - PH * s / 2, 1.0, s)
    img.alpha_composite(layer)
    a = ease_out(local / 0.45)
    fade_text(img, W / 2, 175, "Así se ve una", font("Inter-Light.otf", 78), GREY, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 270, "web moderna", font("Inter-Bold.otf", 104), DEEP, a, dy=(1 - a) * 30)
    p = ease_in_out((local - 0.4) / 0.6)
    if p > 0:
        d = ImageDraw.Draw(img)
        lw = 460 * p
        d.rounded_rectangle([W / 2 - lw / 2, 410, W / 2 + lw / 2, 424], radius=7, fill=TURQ)

def scene_cta(img, t):
    local = t - T_CTA
    bg_a = ease_out(local / 0.45)
    img.alpha_composite(Image.new("RGBA", img.size, DEEP + (int(255 * bg_a),)))
    a = ease_out((local - 0.15) / 0.5)
    fade_text(img, W / 2, 470, "¿Quieres una así", font("Inter-Light.otf", 92), WHITE, a, dy=(1 - a) * 30)
    fade_text(img, W / 2, 585, "para tu negocio?", font("Inter-Bold.otf", 96), WHITE, a, dy=(1 - a) * 30)
    a2 = ease_out((local - 2.3) / 0.5)
    if a2 > 0:
        lay = Image.new("RGBA", img.size, DEEP + (0,))
        d = ImageDraw.Draw(lay)
        bw, bh = 640, 140
        x, y = W / 2 - bw / 2, 790 + (1 - a2) * 40
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=70, fill=TURQ + (int(255 * a2),))
        text_center(d, W / 2, y + 36, "Escríbeme", font("Inter-SemiBold.otf", 56), WHITE + (int(255 * a2),))
        img.alpha_composite(lay)
    a3 = ease_out((local - 2.8) / 0.5)
    fade_text(img, W / 2, 970, "Enlace en la biografía", font("Inter-Regular.otf", 50), TURQ_L, a3)
    draw_logo(img, W / 2 - 170, 1340, 200, clamp((local - 3.6) / 0.8), clamp((local - 4.1) / 0.5), color=WHITE, dot=TURQ)
    a4 = ease_out((local - 3.9) / 0.5)
    lay = Image.new("RGBA", img.size, DEEP + (0,))
    d = ImageDraw.Draw(lay)
    d.text((W / 2 - 50, 1262), "lumen", font=font("Inter-Light.otf", 96), fill=WHITE + (int(255 * a4),))
    d.text((W / 2 - 46, 1380), "WEB DESIGN", font=font("Inter-Medium.otf", 32), fill=TURQ + (int(255 * a4),))
    img.alpha_composite(lay)
    a5 = ease_out((local - 4.6) / 0.6)
    fade_text(img, W / 2, 1600, "Le damos luz a tu negocio", font("Inter-Light.otf", 60), WHITE, a5)

def frame(t):
    img = background(t)
    if t < T_HOOK_END:
        scene_hook(img, t)
        out = clamp((T_HOOK_END - t) / 0.3)
        if out < 1:
            img = Image.blend(background(t), img, out)
    elif t < T_MODERN:
        scene_phone(img, t)
    elif t < T_CTA:
        scene_modern(img, t)
    else:
        scene_modern(img, t)
        scene_cta(img, t)
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
        s.save("/home/claude/lumen/video2/check.png")
    else:
        main(sys.argv[2])
