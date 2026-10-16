"""Portadas de los Reels de Lumen (1080x1920 PNG).

Todo lo importante va dentro de la zona central 3:4 (y de 240 a 1680), que es lo que
Instagram y TikTok muestran en la cuadrícula del perfil.

Uso: python3 portadas.py            -> genera todas en marca/portadas/
     python3 portadas.py 6           -> solo la del video 6
Para un video nuevo: agregar su entrada en PORTADAS.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "video1"))
from PIL import Image, ImageDraw, ImageFilter
from render import W, H, OFF, DEEP, TURQ, TURQ_L, GREY, WHITE, font, draw_logo

OUT = os.path.join(HERE, "..", "..", "marca", "portadas")

# n: (etiqueta, fondo "claro"/"oscuro", líneas). Cada línea: lista de (texto, acento?)
PORTADAS = {
    1: ("Presentación", "oscuro", [[("Hola,", False)], [("soy ", False), ("Angel", True)], [("y diseño", False)], [("tu web", True)]]),
    2: ("Tip", "claro", [[("Así se ve", False)], [("una web", False)], [("moderna en", False)], [("tu ", False), ("teléfono", True)]]),
    3: ("Precios", "oscuro", [[("¿Cuánto", False)], [("cuesta una", False)], [("página ", False), ("web?", True)]]),
    4: ("Tip", "claro", [[("¿Tu negocio", False)], [("solo está", False)], [("en ", False), ("redes?", True)]]),
    5: ("Proceso", "oscuro", [[("Tu web", False)], [("en ", False), ("4 pasos", True)]]),
    6: ("Tip", "claro", [[("3 errores", True)], [("que espantan", False)], [("clientes", False)]]),
}


def fondo(oscuro):
    img = Image.new("RGBA", (W, H), (DEEP if oscuro else OFF) + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    if oscuro:
        d.ellipse([W - 620, 200, W + 380, 1200], fill=TURQ + (255,))
        d.ellipse([-420, 1150, 520, 2090], fill=TURQ + (255,))
    else:
        d.ellipse([W - 620, 200, W + 380, 1200], fill=TURQ_L + (255,))
        d.ellipse([-420, 1150, 520, 2090], fill=TURQ_L + (255,))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    # mezcla controlada (evita bordes grises del desenfoque sobre fondo claro)
    a = glow.split()[3].point(lambda v: int(v * (0.28 if oscuro else 0.85)))
    tinte = Image.new("RGBA", (W, H), (TURQ if oscuro else TURQ_L) + (255,))
    tinte.putalpha(a)
    img.alpha_composite(tinte)
    return img


def portada(n):
    etiqueta, tono, lineas = PORTADAS[n]
    oscuro = tono == "oscuro"
    img = fondo(oscuro)
    d = ImageDraw.Draw(img)
    base, acento = (WHITE, TURQ) if oscuro else (DEEP, TURQ)
    x = 100
    # etiqueta: "TIP · 06"
    tag = f"{etiqueta.upper()}  ·  {n:02d}"
    ft = font("Inter-SemiBold.otf", 38)
    tw = d.textlength(tag, font=ft)
    d.rounded_rectangle([x, 330, x + tw + 64, 402], radius=36, fill=(TURQ if oscuro else TURQ_L))
    d.text((x + 32, 345), tag, font=ft, fill=(DEEP if oscuro else (15, 118, 110)))
    # título: el tamaño se ajusta a la línea más larga y a la cantidad de líneas
    size = 150 if len(lineas) <= 3 else 132
    fb = font("Inter-Bold.otf", size)
    while max(sum(d.textlength(t, font=fb) for t, _ in l) for l in lineas) > W - 2 * x and size > 80:
        size -= 6
        fb = font("Inter-Bold.otf", size)
    y = 540
    for linea in lineas:
        cx = x
        for texto, ac in linea:
            d.text((cx, y), texto, font=fb, fill=acento if ac else base)
            cx += d.textlength(texto, font=fb)
        y += int(size * 1.12)
    # barra de acento bajo el título
    d.rounded_rectangle([x, y + 40, x + 140, y + 56], radius=8, fill=TURQ)
    # marca abajo (dentro de la zona 3:4)
    draw_logo(img, x + 52, 1560, 110, 1.0, 1.0, color=(WHITE if oscuro else DEEP), dot=TURQ)
    d = ImageDraw.Draw(img)
    d.text((x + 140, 1505), "lumen", font=font("Inter-Light.otf", 60), fill=(WHITE if oscuro else DEEP))
    d.text((x + 143, 1578), "WEB DESIGN", font=font("Inter-Medium.otf", 22), fill=TURQ)
    return img.convert("RGB")


def guardar(n):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f"lumen-portada-{n:02d}.png")
    portada(n).save(p)
    return p


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or sorted(PORTADAS)
    for n in ns:
        print(guardar(n))
