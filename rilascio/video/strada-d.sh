#!/bin/bash
# Strada D: immagini già pronte del sito (copertina del Giornale, Tabellone di Campionato e di Champions Cup) montate con ffmpeg.
set -e
R=/tmp/claude-0/srv/o-fant-a-girrr/riepiloghi; O=/tmp/claude-0/prova/vd; mkdir -p $O
python3 - <<'PY'
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def card(nome, righe):
    im=Image.new('RGB',(720,1280),'#1d2a52'); d=ImageDraw.Draw(im)
    for y in range(1280):
        t=y/1280; d.line([(0,y),(720,y)],fill=(int(44-20*t),int(63-34*t),int(124-63*t)))
    lg=Image.open('/tmp/claude-0/srv/o-fant-a-girrr/assets/loghi/logo-lega-o-fant-a-girrr.png').convert('RGBA'); lg=lg.resize((260,int(260*lg.height/lg.width)))
    im.paste(lg,((720-lg.width)//2,330),lg); y=330+lg.height+50
    for testo,dim,col in righe:
        f=ImageFont.truetype(B,dim); w=d.textlength(testo,font=f); d.text(((720-w)/2,y),testo,font=f,fill=col); y+=dim+22
    im.save('/tmp/claude-0/prova/vd/'+nome)
card('a.png',[('7ª GIORNATA',64,'#fbf6ec'),('CAMPIONATO · RISULTATI',28,'#ffd166')])
card('z.png',[('Tutto su O Girrr',44,'#fbf6ec'),('Giornale, Tabellone e Curva',26,'#ffd166')])
PY
# ogni immagine in verticale: sfondo sfocato + immagine al centro con zoom lento
i=0
for f in $O/a.png $R/copertine/settimana-07.png $R/tabellone-lega-07.png $R/tabellone-coppa-04.png $O/z.png; do
  HH=$(python3 -c "from PIL import Image;i=Image.open('$f');print(min(1100,round(680*i.height/i.width/2)*2))")
  # una sola immagine in ingresso: lo zoom lento ne fa 100 fotogrammi (4 secondi a 25 al secondo)
  ffmpeg -loglevel error -y -i "$f" -filter_complex "[0]split[x][y];[x]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,boxblur=24:2,eq=brightness=-0.15,loop=99:1:0,setpts=N/25/TB[bg];[y]scale=680:-2,zoompan=z='min(zoom+0.0008,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=100:s=680x${HH}[fg0];[fg0]null[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p" -frames:v 100 -r 25 -c:v libx264 -crf 22 $O/s$i.mp4
  i=$((i+1))
done
# dissolvenze tra le scene
ffmpeg -loglevel error -y -i $O/s0.mp4 -i $O/s1.mp4 -i $O/s2.mp4 -i $O/s3.mp4 -i $O/s4.mp4 -filter_complex \
 "[0][1]xfade=transition=fade:duration=0.6:offset=3.4[a];[a][2]xfade=transition=slideleft:duration=0.6:offset=6.8[b];[b][3]xfade=transition=slideleft:duration=0.6:offset=10.2[c];[c][4]xfade=transition=fade:duration=0.6:offset=13.6,format=yuv420p" \
 -c:v libx264 -crf 23 /home/user/o-girrr-registro/lab/video-giornata/strada-d-immagini.mp4
echo fatto
