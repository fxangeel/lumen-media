# Lumen Web Design · instrucciones para Claude

Repositorio de los videos de Lumen Web Design (marca de diseño web de Angel). Todo se escribe en español.

## Antes de crear un video nuevo
1. Leer `marca/guia-videos.md` completa y aplicar sus "Reglas vigentes".
2. Si hay una hipótesis "Por probar" que este video pueda probar, cambiar solo esa variable y decirlo a Angel.
3. Portada: agregar el video a `PORTADAS` en `herramientas/portadas/portadas.py` (etiqueta, fondo alternando claro/oscuro con el video anterior, título corto con una palabra en acento), correr `python3 portadas.py N` y luego `sh con_portada.sh marca/portadas/lumen-portada-NN.png VIDEO.mp4 VIDEO-portada.mp4` en las dos versiones (Instagram y TikTok). Se programa siempre el archivo `-portada.mp4`. En Instagram además se pasa `videoThumbnailUrl` con la URL raw de la portada PNG. En TikTok (cuenta personal) Metricool no puede poner portada: por eso va como primer fotograma.
4. El mismo día que se programa, agregar el video a `analisis/videos.json` (tipo, gancho, tipo de gancho, duración, segundos del cierre, voz, si muestra precios, negocio de ejemplo, fecha y hora de cada red).

## Análisis de estadísticas (Metricool, marca 7447240, zona horaria America/New_York = hora de Venezuela)
1. `python3 herramientas/analisis/estadisticas.py pendientes` muestra qué publicaciones cumplieron 48 h o 7 días sin analizar.
2. Pedir a Metricool con `getAnalyticsDataByMetrics` (desde 2 días antes del primer video hasta hoy):
   - Reels de Instagram: los IDs de `estadisticas.py metricas instagram`.
   - Videos de TikTok: los IDs de `estadisticas.py metricas tiktok`.
   - Cuenta: `estadisticas.py metricas instagram --cuenta` y `estadisticas.py metricas tiktok --cuenta`.
   Guardar cada respuesta como `{"red": ..., "metricas": [IDs en el mismo orden], "filas": rows}` en un archivo temporal y correr `estadisticas.py importar ARCHIVO` (videos) o `estadisticas.py cuenta ARCHIVO` (cuenta).
3. La primera vez que lleguen datos reales, revisar que las unidades tengan sentido (porcentajes entre 0 y 100, tiempo medio menor que la duración) y corregir el programa si no.
4. `estadisticas.py tabla` da la comparación. Analizar con las reglas de la sección 2 de la guía, actualizar hipótesis, registro y, si se confirma algo en 3 o más videos, las reglas vigentes.
5. Marcar cada análisis con `estadisticas.py analizado N RED 48h|7d`. Nunca marcar como analizada una publicación que todavía no tiene datos ("SIN DATOS todavía" en `pendientes`): se vuelve a intentar al día siguiente.
6. Reconstruir el Excel: `python3 herramientas/hoja/build.py` (llena la pestaña Resultados con `analisis/estadisticas.json`).
7. Subir a GitHub con un mensaje claro y avisar a Angel en pocas líneas: qué funcionó, qué no y qué cambia en el próximo video.

## Leads (lo más importante)
Cuando Angel cuente que le escribió o cotizó alguien, registrarlo:
`estadisticas.py lead --red instagram|tiktok|whatsapp --video N --estado escribió|cotizó|compró --nota "..."`

## No cambiar sin preguntar a Angel
Marca, voz, precios, la regla de no decir plazos, usar negocios inventados y el formato de las descripciones. Si los números sugieren cambiar algo de esto, proponérselo con la evidencia.
