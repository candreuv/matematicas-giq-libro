#!/bin/bash
# usage: mkgif.sh file.py Scene outname
set -e
manim -qh --fps 15 -r 960,540 $1 $2 >/tmp/manim_$3.log 2>&1 || { tail -20 /tmp/manim_$3.log; exit 1; }
v=$(ls media/videos/${1%.py}/*/$2.mp4)
ffmpeg -y -loglevel error -sseof -0.1 -i $v -frames:v 1 last_$3.png
ffmpeg -y -loglevel error -ss 4 -i $v -frames:v 1 mid_$3.png
ffmpeg -y -loglevel error -i $v -vf "fps=10,scale=720:-1:flags=lanczos,palettegen=max_colors=64:stats_mode=full" pal_$3.png
ffmpeg -y -loglevel error -i $v -i pal_$3.png -lavfi "fps=10,scale=720:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=none" t_$3.gif
gifsicle -O3 t_$3.gif -o $3.gif
ls -la $3.gif
