#!/bin/sh
# Pone la portada como primeros 3 fotogramas (0,1 s) del video, para que TikTok
# (cuenta personal: Metricool no puede asignarle portada) la use en el perfil.
# Uso: sh con_portada.sh PORTADA.png VIDEO.mp4 SALIDA.mp4
D=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$2")
T=$(python3 -c "print(round($D + 0.1, 3))")
ffmpeg -y -loglevel error -loop 1 -framerate 30 -t 0.1 -i "$1" -i "$2" \
  -filter_complex "[0:v]scale=1080:1920,format=yuv420p,setsar=1[c];[1:v]format=yuv420p,setsar=1[v];[c][v]concat=n=2:v=1:a=0[vo];[1:a]adelay=100:all=1[ao]" \
  -map "[vo]" -map "[ao]" -t "$T" -c:v libx264 -crf 18 -preset medium -r 30 -c:a aac -b:a 192k "$3"
