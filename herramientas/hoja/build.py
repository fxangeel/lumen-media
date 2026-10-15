from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

DEEP = "082F34"
TURQ = "14B8A6"
TURQ_L = "CCFBF1"
GREY = "64748B"
INPUT = "FFF9C4"
F = "Arial"

thin = Side(style="thin", color="E2E8F0")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def hdr(ws, row, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(name=F, bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=DEEP)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30

def title(ws, text, sub):
    ws["A1"] = text
    ws["A1"].font = Font(name=F, bold=True, size=16, color=DEEP)
    ws["A2"] = sub
    ws["A2"].font = Font(name=F, italic=True, size=9, color=GREY)

def body(c, wrap=False, center=False, color="0F172A", bold=False):
    c.font = Font(name=F, size=10, color=color, bold=bold)
    c.alignment = Alignment(vertical="top", wrap_text=wrap, horizontal="center" if center else None)
    c.border = border

IG1 = "Hola, soy Angel 👋 y esto es Lumen Web Design.\n\nCreo páginas web modernas y minimalistas para negocios que quieren crecer: pedidos online, reservas y un diseño perfecto para el teléfono.\n\n📍 Desde Aragua, Venezuela, para todo el país y el exterior.\n\n¿Tu negocio aún no tiene web? Escríbeme por WhatsApp, el enlace está en mi biografía 💬\n\nLumen: le damos luz a tu negocio ✨"
IG2 = "Si tu negocio no se ve bien en el teléfono, ese cliente se va con la competencia en dos segundos 📉\n\nEl café del video es solo un ejemplo: tu web lleva tu logo, tus colores, tus fotos y tus productos reales 🎨\n\n¿Qué te gustaría que tuviera la web de tu negocio? Te leo en los comentarios 👇 o escríbeme por WhatsApp desde el enlace de mi biografía."
IG3 = "Todos los paquetes incluyen ✨\n📱 Diseño que se ve perfecto en celular, tablet y computadora\n💬 Botón de WhatsApp para que te escriban al instante\n🔎 Optimización básica para aparecer en Google\n🎓 Te enseño a manejar tu página\n🎁 2 semanas de mantenimiento gratis\n\n¿Cuál paquete le vendría mejor a tu negocio? Cuéntame en los comentarios 👇 o escríbeme por WhatsApp desde el enlace de mi biografía."
TK1 = "Hola, soy Angel 👋 Diseño páginas web para negocios de Venezuela y del exterior. Si tu negocio aún no tiene web, escríbeme por mensaje directo y te ayudo 💬"
TK2 = "El café del video es solo un ejemplo: tu web lleva tu logo, tus colores y tus productos reales 🎨 ¿Qué te gustaría que tuviera la web de tu negocio? Cuéntame en los comentarios o por mensaje directo 👇"
TK3 = "Todos los paquetes incluyen diseño para celular y computadora, botón de WhatsApp, optimización para Google, capacitación y 2 semanas de mantenimiento gratis ✨ ¿Cuál le vendría mejor a tu negocio? Escríbeme por mensaje directo y te hago tu cotización 💬"
IG4 = "Las redes sociales sirven para que te descubran, pero tu página web es donde te eligen 💡\n\nTu web le da a tu negocio una dirección propia que puedes poner en tu perfil, en tu tarjeta, en Google Maps y en tu estado de WhatsApp. Y trabaja las 24 horas, aunque no estés respondiendo mensajes 🕐\n\n¿Tu negocio ya tiene web o todavía vende solo por redes? Cuéntame en los comentarios 👇 o escríbeme por WhatsApp desde el enlace de mi biografía."
IG5 = "Lo que necesito para empezar tu web 📝\n📸 Tu logo y fotos de tus productos o de tu local\n🎨 Tus colores\n📋 Tu menú, servicios o lista de precios\n📍 Tu dirección, horario y número de WhatsApp\n\nSi algo te falta, no pasa nada: lo vemos juntos en la primera conversación 🤝\n\n¿Qué es lo que más te frena para tener la página web de tu negocio? Te leo en los comentarios 👇 o escríbeme por WhatsApp desde el enlace de mi biografía."
TK4 = "Tu web le da a tu negocio una dirección propia que puedes poner en tu perfil, en tu tarjeta y en Google Maps, y trabaja las 24 horas aunque no estés respondiendo mensajes 🕐 ¿Tu negocio ya tiene web o vende solo por redes? Cuéntame en los comentarios o escríbeme por mensaje directo 💬"
TK5 = "Para empezar tu web solo necesito tu logo, fotos de tus productos, tu menú o lista de precios y tu WhatsApp 📝 Si algo te falta, lo vemos juntos 🤝 ¿Qué es lo que más te frena para tener tu página web? Cuéntame en los comentarios o escríbeme por mensaje directo 💬"
HT_IG ="#diseñoweb #paginasweb #webdesign #emprendedoresvenezolanos #aragua #maracay #venezuela #negociosvenezuela #marketingdigital #emprendimiento"

ROWS = [
    # n, video, fecha, hora, red, estado, enlace, descripcion, hashtags, archivo, portada
    (1, "Presentación de Lumen", "jue 15/10/2026", "1:50 pm", "Instagram", "Publicado",
     "https://www.instagram.com/reel/DehiSD7DYrn/", IG1, HT_IG, "lumen-reel-01-presentacion.mp4", "Logo (seg. 3)"),
    (1, "Presentación de Lumen", "jue 15/10/2026", "3:46 pm", "TikTok", "Publicado",
     "https://www.tiktok.com/@Lumen Web Design/video/7696983331849686293", TK1,
     "#diseñoweb #paginasweb #emprendedoresvenezolanos #aragua #venezuela", "lumen-reel-01-presentacion.mp4", "Primer fotograma"),
    (2, "Web moderna en el teléfono", "sáb 17/10/2026", "11:00 am", "Instagram", "Programado",
     "", IG2, HT_IG, "lumen-reel-02-web-en-el-telefono.mp4", "\"Así se ve una web moderna\""),
    (2, "Web moderna en el teléfono", "sáb 17/10/2026", "11:00 am", "TikTok", "Programado",
     "", TK2, "#diseñoweb #paginasweb #emprendedoresvenezolanos #venezuela #negocios",
     "lumen-reel-02-web-en-el-telefono.mp4", "Primer fotograma"),
    (3, "¿Cuánto cuesta una página web?", "lun 19/10/2026", "11:00 am", "Instagram", "Programado",
     "", IG3, HT_IG, "lumen-reel-03-cuanto-cuesta-una-web.mp4", "Tarjeta paquete Completo"),
    (3, "¿Cuánto cuesta una página web?", "lun 19/10/2026", "11:00 am", "TikTok", "Programado",
     "", TK3, "#diseñoweb #paginasweb #emprendedoresvenezolanos #venezuela #emprendimiento",
     "lumen-reel-03-cuanto-cuesta-una-web.mp4", "Primer fotograma"),
    (4, "¿Tu negocio solo está en redes?", "mié 21/10/2026", "11:00 am", "Instagram", "Programado",
     "", IG4, HT_IG, "lumen-reel-04-solo-en-redes.mp4", "Título (seg. 1,5)"),
    (4, "¿Tu negocio solo está en redes?", "mié 21/10/2026", "11:00 am", "TikTok", "Programado",
     "", TK4, "#diseñoweb #paginasweb #emprendedoresvenezolanos #venezuela #negocios",
     "lumen-reel-04-solo-en-redes.mp4", "Primer fotograma"),
    (5, "Así hago tu web en 4 pasos", "vie 23/10/2026", "11:00 am", "Instagram", "Programado",
     "", IG5, HT_IG, "lumen-reel-05-proceso-4-pasos.mp4", "Título (seg. 1,8)"),
    (5, "Así hago tu web en 4 pasos", "vie 23/10/2026", "11:00 am", "TikTok", "Programado",
     "", TK5, "#diseñoweb #paginasweb #emprendedoresvenezolanos #venezuela #emprendimiento",
     "lumen-reel-05-proceso-4-pasos.mp4", "Primer fotograma"),
]

wb = Workbook()

# ---------------- Calendario ----------------
ws = wb.active
ws.title = "Calendario"
title(ws, "Lumen Web Design · Calendario de publicaciones",
      "Horas en hora de Venezuela. Publicación automática con Metricool. Todos los videos van marcados como contenido hecho con IA.")
H = ["N°", "Video", "Fecha", "Hora", "Red", "Estado", "Enlace", "Descripción", "Hashtags", "Archivo (Videos\\Lumen)", "Portada"]
hdr(ws, 4, H, [5, 26, 15, 10, 11, 13, 30, 60, 34, 34, 22])
for r, row in enumerate(ROWS, start=5):
    for col, v in enumerate(row, start=1):
        c = ws.cell(row=r, column=col, value=v if v != "" else None)
        body(c, wrap=col in (2, 7, 8, 9, 10, 11), center=col in (1, 3, 4, 5, 6))
        if col == 7 and v:
            c.hyperlink = v.replace(" ", "%20")
            c.value = "Ver publicación"
            c.font = Font(name=F, size=10, color="0563C1", underline="single")
        if col == 7 and not v:
            c.value = "Se genera al publicarse"
            c.font = Font(name=F, size=9, italic=True, color=GREY)
        if col == 5:
            c.font = Font(name=F, size=10, bold=True, color=DEEP)
    ws.row_dimensions[r].height = 150 if row[4] == "Instagram" else 80
last = 4 + len(ROWS)
dv = DataValidation(type="list", formula1='"Publicado,Programado,Pendiente,Borrador"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"F5:F{last}")
ws.conditional_formatting.add(f"F5:F{last}", FormulaRule(formula=['$F5="Publicado"'],
                              fill=PatternFill("solid", fgColor=TURQ_L), font=Font(name=F, bold=True, color="0F766E")))
ws.conditional_formatting.add(f"F5:F{last}", FormulaRule(formula=['$F5="Programado"'],
                              fill=PatternFill("solid", fgColor="E0F2FE"), font=Font(name=F, bold=True, color="075985")))
ws.freeze_panes = "C5"
ws.auto_filter.ref = f"A4:K{last}"

# ---------------- Resultados ----------------
rs = wb.create_sheet("Resultados")
title(rs, "Resultados por publicación",
      "Celdas amarillas: escribe los números de Metricool o de la app. Las columnas grises se calculan solas.")
RH = ["N°", "Video", "Red", "Estado", "Vistas", "Alcance", "Me gusta", "Comentarios", "Guardados",
      "Compartidos", "Interacciones", "Tasa de interacción", "Mensajes recibidos", "Clientes que cotizaron"]
hdr(rs, 4, RH, [5, 30, 11, 13, 10, 10, 10, 12, 11, 12, 13, 13, 12, 13])
for i, row in enumerate(ROWS):
    r = 5 + i
    vals = [f"=Calendario!A{r}", f"=Calendario!B{r}", f"=Calendario!E{r}", f"=Calendario!F{r}"]
    for col, v in enumerate(vals, start=1):
        c = rs.cell(row=r, column=col, value=v)
        body(c, center=col != 2, wrap=col == 2)
        c.font = Font(name=F, size=10, color="008000")
    for col in range(5, 11):
        c = rs.cell(row=r, column=col)
        body(c, center=True)
        c.fill = PatternFill("solid", fgColor=INPUT)
        c.font = Font(name=F, size=10, color="0000FF")
        c.number_format = "#,##0"
    if row[4] == "TikTok":
        rs.cell(row=r, column=9).value = None
        rs.cell(row=r, column=9).fill = PatternFill("solid", fgColor="F1F5F9")
    c = rs.cell(row=r, column=11, value=f"=IF(COUNT(G{r}:J{r})=0,\"\",SUM(G{r}:J{r}))")
    body(c, center=True); c.fill = PatternFill("solid", fgColor="F1F5F9"); c.number_format = "#,##0"
    c = rs.cell(row=r, column=12, value=f"=IFERROR(IF(F{r}=\"\",\"\",K{r}/F{r}),\"\")")
    body(c, center=True); c.fill = PatternFill("solid", fgColor="F1F5F9"); c.number_format = "0.0%"
    for col in (13, 14):
        c = rs.cell(row=r, column=col)
        body(c, center=True)
        c.fill = PatternFill("solid", fgColor=INPUT)
        c.font = Font(name=F, size=10, color="0000FF")
    rs.row_dimensions[r].height = 30
tr = 5 + len(ROWS)
rs.cell(row=tr, column=2, value="Total")
body(rs.cell(row=tr, column=2), bold=True)
for col in range(5, 15):
    L = get_column_letter(col)
    if col == 12:
        f = f"=IFERROR(IF(F{tr}=0,\"\",K{tr}/F{tr}),\"\")"
        fmt = "0.0%"
    else:
        f = f"=SUM({L}5:{L}{tr-1})"
        fmt = "#,##0"
    c = rs.cell(row=tr, column=col, value=f)
    body(c, center=True, bold=True)
    c.number_format = fmt
    c.fill = PatternFill("solid", fgColor=TURQ_L)
note_r = tr + 2
notes = [
    "Notas:",
    "• Metricool todavía no muestra estadísticas (cuenta conectada hoy); suelen aparecer en unas 24 horas.",
    "• Interacciones = Me gusta + Comentarios + Guardados + Compartidos. Tasa de interacción = Interacciones ÷ Alcance.",
    "• TikTok no informa 'Guardados' por Metricool, por eso esa celda está en gris.",
    "• Mensajes recibidos y Clientes que cotizaron: llévalos tú a mano; son los números que de verdad importan para vender.",
]
for i, n in enumerate(notes):
    c = rs.cell(row=note_r + i, column=2, value=n)
    c.font = Font(name=F, size=9, bold=(i == 0), color=GREY)
rs.freeze_panes = "C5"

# ---------------- Resumen ----------------
sm = wb.create_sheet("Resumen")
title(sm, "Resumen", "Se actualiza solo con lo que pongas en Calendario y Resultados.")
items = [
    ("Videos creados", "=MAX(Calendario!A5:A100)", "0"),
    ("Publicaciones totales", "=COUNTA(Calendario!E5:E100)", "0"),
    ("Publicadas", "=COUNTIF(Calendario!F5:F100,\"Publicado\")", "0"),
    ("Programadas", "=COUNTIF(Calendario!F5:F100,\"Programado\")", "0"),
    ("En Instagram", "=COUNTIF(Calendario!E5:E100,\"Instagram\")", "0"),
    ("En TikTok", "=COUNTIF(Calendario!E5:E100,\"TikTok\")", "0"),
    ("Vistas totales", f"=Resultados!E{tr}", "#,##0"),
    ("Mensajes recibidos", f"=Resultados!M{tr}", "#,##0"),
    ("Clientes que cotizaron", f"=Resultados!N{tr}", "#,##0"),
]
sm.column_dimensions["A"].width = 28
sm.column_dimensions["B"].width = 16
for i, (k, f, fmt) in enumerate(items):
    r = 4 + i
    a = sm.cell(row=r, column=1, value=k); body(a, bold=True, color=DEEP)
    b = sm.cell(row=r, column=2, value=f); body(b, center=True, bold=True); b.number_format = fmt
    b.fill = PatternFill("solid", fgColor=TURQ_L)
r = 4 + len(items) + 1
sm.cell(row=r, column=1, value="Créditos de voz (ElevenLabs Starter)").font = Font(name=F, bold=True, size=11, color=DEEP)
rows2 = [
    ("Créditos disponibles", 38848, "#,##0", True),
    ("Costo por video (aprox.)", 400, "#,##0", True),
    ("Videos que alcanzan", f"=IFERROR(INT(B{r+1}/B{r+2}),0)", "0", False),
]
for i, (k, v, fmt, is_input) in enumerate(rows2):
    rr = r + 1 + i
    a = sm.cell(row=rr, column=1, value=k); body(a)
    b = sm.cell(row=rr, column=2, value=v); body(b, center=True); b.number_format = fmt
    if is_input:
        b.fill = PatternFill("solid", fgColor=INPUT); b.font = Font(name=F, size=10, color="0000FF")
    else:
        b.fill = PatternFill("solid", fgColor=TURQ_L); b.font = Font(name=F, size=10, bold=True)
sm.cell(row=r + 5, column=1,
        value="Fuente: tu cuenta de ElevenLabs (15/10/2026). Voz: Diego (desde el video 4). Los créditos se renuevan cada mes.").font = Font(name=F, size=9, italic=True, color=GREY)

wb.move_sheet("Resumen", offset=-2)
wb.active = 0
import os
wb.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "marca", "lumen-calendario-publicaciones.xlsx"))
print("ok")
