"""Estadísticas de los videos de Lumen (Instagram Reels y TikTok) tomadas de Metricool.

Guarda cada lectura en analisis/estadisticas.json y arma la tabla para comparar videos.
Los datos se piden a Metricool con su conector (getAnalyticsDataByMetrics) y se guardan
en un archivo JSON con esta forma, que es lo que lee el comando `importar`:

    {"red": "instagram", "metricas": ["IGRE02", "IGRE06", ...], "filas": [[...], [...]]}

Comandos:
    python3 estadisticas.py importar ARCHIVO.json      # Reels / videos (una fila por publicación)
    python3 estadisticas.py cuenta ARCHIVO.json        # evolución diaria de la cuenta (seguidores, perfil)
    python3 estadisticas.py lead --red instagram --video 3 --estado cotizó --nota "panadería de Maracay"
    python3 estadisticas.py pendientes                 # publicaciones que ya cumplieron 48 h o 7 días sin analizar
    python3 estadisticas.py analizado 3 instagram 48h  # marca un análisis como hecho
    python3 estadisticas.py tabla                      # tabla comparativa en Markdown
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
VIDEOS = os.path.join(RAIZ, "analisis", "videos.json")
DATOS = os.path.join(RAIZ, "analisis", "estadisticas.json")
VE = timezone(timedelta(hours=-4))  # hora de Venezuela

# Métricas que se piden a Metricool y el nombre con que se guardan.
CAMPOS = {
    "instagram": {
        "IGRE02": "publicado", "IGRE06": "url", "IGRE26": "duracion_s",
        "IGRE23": "vistas", "IGRE11": "alcance", "IGRE10": "me_gusta", "IGRE07": "comentarios",
        "IGRE12": "guardados", "IGRE21": "compartidos", "IGRE29": "reposts",
        "IGRE24": "tiempo_medio_s", "IGRE27": "retencion_pct", "IGRE28": "vio_3s_pct",
    },
    "tiktok": {
        "TKPO02": "publicado", "TKPO03": "url", "TKPO06": "duracion_s",
        "TKPO07": "vistas", "TKPO11": "alcance", "TKPO08": "me_gusta", "TKPO09": "comentarios",
        "TKPO10": "compartidos", "TKPO13": "vio_completo_pct", "TKPO14": "tiempo_total_s",
        "TKPO15": "tiempo_medio_s", "TKPO16": "pct_para_ti", "TKPO17": "pct_seguidores",
        "TKPO20": "pct_perfil", "TKPO21": "pct_busqueda",
    },
}
CUENTA = {
    "instagram": {"IGEV01": "seguidores", "IGEV43": "seguidores_ganados", "IGEV44": "seguidores_perdidos",
                  "IGEV42": "cuentas_interactuaron", "IGEV05": "vistas_perfil_y_posts"},
    "tiktok": {"TKEV07": "seguidores", "TKEV16": "seguidores_ganados", "TKEV17": "seguidores_perdidos",
               "TKEV09": "visitas_perfil"},
}
TEXTO = {"publicado", "url"}
ETAPAS = (("48h", 48), ("7d", 168))


def metricas_para(red, tipo="videos"):
    """Lista de IDs a pedir a Metricool, en el orden en que este programa los espera."""
    return list((CAMPOS if tipo == "videos" else CUENTA)[red].keys())


def cargar(path, vacio):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return vacio


def guardar(data):
    with open(DATOS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def datos_vacios():
    return {"_nota": "Lo escribe herramientas/analisis/estadisticas.py. No editar a mano salvo 'leads'.",
            "lecturas": [], "cuenta": {"instagram": {}, "tiktok": {}}, "leads": [], "analisis_hechos": []}


def num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def pct(v):
    """Metricool a veces da 0-1 y a veces 0-100. Todo se guarda en 0-100."""
    v = num(v)
    if v is None:
        return None
    return round(v * 100, 2) if v <= 1 else round(v, 2)


def fecha_de(v):
    """Saca la fecha (YYYY-MM-DD) de lo que Metricool ponga en 'publicado'."""
    s = str(v or "").strip()
    if len(s) >= 10 and s[4] == "-":
        return s[:10]
    if len(s) >= 8 and s[:8].isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return None


def ahora():
    return datetime.now(VE)


def video_por_fecha(videos, red, fecha):
    for v in videos:
        if v["publicacion"].get(red, "")[:10] == fecha:
            return v
    return None


def cmd_importar(args):
    raw = cargar(args.archivo, None)
    red = raw["red"]
    mapa = CAMPOS[red]
    videos = cargar(VIDEOS, {"videos": []})["videos"]
    data = cargar(DATOS, datos_vacios())
    leido = ahora().isoformat(timespec="minutes")
    hoy = leido[:10]
    sin = 0
    for fila in raw.get("filas", []):
        d = {}
        for mid, val in zip(raw["metricas"], fila):
            if mid not in mapa:
                continue
            campo = mapa[mid]
            if campo in TEXTO:
                d[campo] = val
            elif campo.endswith("_pct") or campo.startswith("pct_"):
                d[campo] = pct(val)
            else:
                d[campo] = num(val)
        v = video_por_fecha(videos, red, fecha_de(d.get("publicado")))
        if v is None:
            # Si la fecha no coincide, probar con el enlace guardado antes.
            for l in data["lecturas"]:
                if l["red"] == red and d.get("url") and l["datos"].get("url") == d.get("url"):
                    v = next((x for x in videos if x["n"] == l["video"]), None)
                    break
        if v is None:
            sin += 1
            print(f"AVISO: publicación de {red} sin video asignado: {d.get('publicado')} {d.get('url')}")
            continue
        pub = datetime.fromisoformat(v["publicacion"][red])
        horas = round((ahora() - pub).total_seconds() / 3600, 1)
        # Una lectura por publicación y por día: la del mismo día se reemplaza.
        data["lecturas"] = [l for l in data["lecturas"]
                            if not (l["video"] == v["n"] and l["red"] == red and l["leido"][:10] == hoy)]
        data["lecturas"].append({"video": v["n"], "red": red, "leido": leido,
                                 "horas_desde_publicacion": horas, "datos": d})
        print(f"ok: video {v['n']} en {red} ({horas} h publicado)")
    data["lecturas"].sort(key=lambda l: (l["video"], l["red"], l["leido"]))
    guardar(data)
    if not raw.get("filas"):
        print(f"Metricool no devolvió publicaciones de {red} para ese rango.")
    if sin:
        sys.exit(2)


def cmd_cuenta(args):
    raw = cargar(args.archivo, None)
    red = raw["red"]
    mapa = CUENTA[red]
    data = cargar(DATOS, datos_vacios())
    for fila in raw.get("filas", []):
        dia = fecha_de(fila[-1])
        if not dia:
            continue
        reg = {}
        for mid, val in zip(raw["metricas"], fila[:-1]):
            if mid in mapa and num(val) is not None:
                reg[mapa[mid]] = num(val)
        if reg:
            data["cuenta"][red][dia] = {**data["cuenta"][red].get(dia, {}), **reg}
    data["cuenta"][red] = dict(sorted(data["cuenta"][red].items()))
    guardar(data)
    print(f"ok: {len(raw.get('filas', []))} días de la cuenta de {red}")


def cmd_lead(args):
    data = cargar(DATOS, datos_vacios())
    data["leads"].append({"fecha": args.fecha or ahora().date().isoformat(), "red": args.red,
                          "video": args.video, "estado": args.estado, "nota": args.nota or ""})
    guardar(data)
    print("ok: lead guardado")


def ultimas(data):
    """Última lectura de cada publicación (video, red)."""
    u = {}
    for l in data["lecturas"]:
        k = (l["video"], l["red"])
        if k not in u or l["leido"] > u[k]["leido"]:
            u[k] = l
    return u


def derivadas(d, dur):
    alc = d.get("alcance") or 0
    inter = sum(d.get(k) or 0 for k in ("me_gusta", "comentarios", "guardados", "compartidos"))
    r = {"interacciones": inter}
    r["tasa_interaccion_pct"] = round(inter / alc * 100, 1) if alc else None
    r["guardar_compartir_pct"] = round(((d.get("guardados") or 0) + (d.get("compartidos") or 0)) / alc * 100, 1) if alc else None
    tm = d.get("tiempo_medio_s")
    if tm and dur:
        if tm > dur * 5:  # vino en milisegundos
            tm = tm / 1000
        r["tiempo_medio_s"] = round(tm, 1)
        r["pct_visto"] = round(min(tm / dur, 1.5) * 100, 1)
    else:
        r["tiempo_medio_s"] = None
        r["pct_visto"] = d.get("retencion_pct")
    return r


def seguidores_48h(data, red, inicio):
    """Seguidores ganados el día de la publicación y el siguiente."""
    dias = {inicio.date().isoformat(), (inicio + timedelta(days=1)).date().isoformat()}
    total = None
    for dia, reg in data["cuenta"].get(red, {}).items():
        if dia in dias and reg.get("seguidores_ganados") is not None:
            total = (total or 0) + reg["seguidores_ganados"]
    return total


def cmd_pendientes(args):
    videos = cargar(VIDEOS, {"videos": []})["videos"]
    data = cargar(DATOS, datos_vacios())
    hechos = {(a["video"], a["red"], a["etapa"]) for a in data["analisis_hechos"]}
    u = ultimas(data)
    hay = False
    for v in videos:
        for red, iso in v["publicacion"].items():
            horas = (ahora() - datetime.fromisoformat(iso)).total_seconds() / 3600
            for etapa, h in ETAPAS:
                if horas >= h and (v["n"], red, etapa) not in hechos:
                    tiene = (v["n"], red) in u
                    print(f"video {v['n']} · {red} · {etapa} · {'con datos' if tiene else 'SIN DATOS todavía'}")
                    hay = True
    if not hay:
        print("nada pendiente")


def cmd_analizado(args):
    data = cargar(DATOS, datos_vacios())
    k = {"video": args.video, "red": args.red, "etapa": args.etapa}
    if k not in [{x: a[x] for x in ("video", "red", "etapa")} for a in data["analisis_hechos"]]:
        data["analisis_hechos"].append({**k, "fecha": ahora().isoformat(timespec="minutes")})
    guardar(data)
    print("ok")


def fmt(v, suf=""):
    if v is None:
        return "–"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}".replace(",", ".") + suf if isinstance(v, int) else f"{v}{suf}"


def cmd_tabla(args):
    videos = {v["n"]: v for v in cargar(VIDEOS, {"videos": []})["videos"]}
    data = cargar(DATOS, datos_vacios())
    u = ultimas(data)
    leads = {}
    for l in data["leads"]:
        leads[(l.get("video"), l["red"])] = leads.get((l.get("video"), l["red"]), 0) + 1
    for red in ("instagram", "tiktok"):
        print(f"\n### {'Instagram' if red == 'instagram' else 'TikTok'}\n")
        if red == "instagram":
            cab = ["N°", "Tipo", "Gancho", "Dur.", "Horas", "Vistas", "Alcance", "Vio +3 s", "% visto",
                   "T. medio", "Me gusta", "Coment.", "Guard.", "Compart.", "Guard+Comp %", "Seg. 48 h", "Leads"]
        else:
            cab = ["N°", "Tipo", "Gancho", "Dur.", "Horas", "Vistas", "Alcance", "Vio completo", "% visto",
                   "T. medio", "Me gusta", "Coment.", "Compart.", "Para ti %", "Perfil %", "Seg. 48 h", "Leads"]
        print("| " + " | ".join(cab) + " |")
        print("|" + "---|" * len(cab))
        for n in sorted(videos):
            v = videos[n]
            l = u.get((n, red))
            if not l:
                continue
            d, x = l["datos"], derivadas(l["datos"], v["duracion_s"])
            seg = seguidores_48h(data, red, datetime.fromisoformat(v["publicacion"][red]))
            base = [str(n), v["tipo"], v["gancho"][:28], fmt(v["duracion_s"], " s"), fmt(l["horas_desde_publicacion"]),
                    fmt(d.get("vistas")), fmt(d.get("alcance"))]
            if red == "instagram":
                fila = base + [fmt(d.get("vio_3s_pct"), " %"), fmt(x["pct_visto"], " %"), fmt(x["tiempo_medio_s"], " s"),
                               fmt(d.get("me_gusta")), fmt(d.get("comentarios")), fmt(d.get("guardados")),
                               fmt(d.get("compartidos")), fmt(x["guardar_compartir_pct"], " %"), fmt(seg),
                               fmt(leads.get((n, red), 0))]
            else:
                fila = base + [fmt(d.get("vio_completo_pct"), " %"), fmt(x["pct_visto"], " %"), fmt(x["tiempo_medio_s"], " s"),
                               fmt(d.get("me_gusta")), fmt(d.get("comentarios")), fmt(d.get("compartidos")),
                               fmt(d.get("pct_para_ti"), " %"), fmt(d.get("pct_perfil"), " %"), fmt(seg),
                               fmt(leads.get((n, red), 0))]
            print("| " + " | ".join(fila) + " |")
    sin_video = [l for l in data["leads"] if not l.get("video")]
    if sin_video:
        print(f"\nLeads sin video identificado: {len(sin_video)}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("importar"); a.add_argument("archivo"); a.set_defaults(f=cmd_importar)
    a = s.add_parser("cuenta"); a.add_argument("archivo"); a.set_defaults(f=cmd_cuenta)
    a = s.add_parser("lead")
    a.add_argument("--red", required=True, choices=["instagram", "tiktok", "whatsapp", "otro"])
    a.add_argument("--video", type=int)
    a.add_argument("--estado", default="escribió", help="escribió, cotizó o compró")
    a.add_argument("--fecha"); a.add_argument("--nota"); a.set_defaults(f=cmd_lead)
    a = s.add_parser("pendientes"); a.set_defaults(f=cmd_pendientes)
    a = s.add_parser("analizado"); a.add_argument("video", type=int); a.add_argument("red")
    a.add_argument("etapa", choices=[e for e, _ in ETAPAS]); a.set_defaults(f=cmd_analizado)
    a = s.add_parser("tabla"); a.set_defaults(f=cmd_tabla)
    a = s.add_parser("metricas"); a.add_argument("red"); a.add_argument("--cuenta", action="store_true")
    a.set_defaults(f=lambda x: print(json.dumps(metricas_para(x.red, "cuenta" if x.cuenta else "videos"))))
    args = p.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
