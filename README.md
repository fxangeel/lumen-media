# Lumen Web Design · media

Videos (Reels/TikTok) e imágenes de la marca Lumen Web Design. Los archivos de `reels/` se usan como URL pública para que Metricool los publique.

- `reels/` — videos finales (1080x1920, 30 fps).
- `marca/` — foto de perfil (logo A2), calendario de publicaciones y `guia-videos.md` (lo que las estadísticas enseñan sobre qué funciona).
- `analisis/` — ficha de cada video (`videos.json`) y estadísticas de Metricool (`estadisticas.json`).
- `herramientas/` — scripts de Python (Pillow + ffmpeg) que generan cada video.
  - `video1/render.py` contiene las funciones base (colores, fuentes Inter, logo, fondo, CTA); `video2` y `video3` las importan.
  - `analisis/estadisticas.py` importa las estadísticas de Metricool y arma la tabla comparativa (ver `CLAUDE.md`).
  - Uso: `python3 render.py still 1.0 5.0` (fotogramas de prueba) o `python3 render.py video salida.mp4`, luego unir la voz con ffmpeg.

Paleta: fondo #F7FAF9 · verde oscuro #082F34 · turquesa #14B8A6 · turquesa claro #CCFBF1 · gris #64748B. Fuente: Inter.
