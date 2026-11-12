#!/bin/bash
# Video della giornata, versione scelta da Gianluca il 12 novembre 2026 («B senza folla»):
# base calma del Campionato (MakeBestMusic), «Victory» sulla Champions Cup, ritorno al Campionato per la chiusura, effetti a tempo.
# Uso: rilascio/video/fai_video.sh CARTELLA_DEL_SITO USCITA.mp4   (CARTELLA_DEL_SITO: una copia di gh-pages)
# Serve Remotion installato in rilascio/video/remotion (vedi LEGGIMI.md) e Chrome headless (primo argomento di render.mjs).
set -e
QUI=$(cd "$(dirname "$0")" && pwd)
SITO=$(cd "$1" && pwd)/; USCITA=$2
CHROME=${CHROME:-$(ls -d /opt/pw-browsers/chromium_headless_shell-*/*/ 2>/dev/null | head -1)chrome-headless-shell}
cd "$QUI/remotion"
SITO=$SITO USCITA=/tmp/video-muto.mp4 node render.mjs "$CHROME"
# Il passaggio alla Coppa e il ritorno al Campionato seguono la scaletta: logo della Coppa e chiusura da scene.json
read -r COPPA FINE < <(python3 -c "import json;S=json.load(open('scene.json'));t=0;d={}
for k,n in S['scene']:d[k]=t;t+=n/S['fps']
print('%.2f %.2f'%(d['introCoppa']+0.5,t-6.83))")
python3 "$QUI/monta_musica.py" "$QUI/musica/campionato.mp3" /tmp/video-muto.mp4 "$USCITA" \
  --dopo "$QUI/musica/coppa-victory.mp3:19.46:126.7@$COPPA:1.0" \
  --dopo "$QUI/musica/campionato.mp3:64.77:72.6@$FINE:1.0" \
  --coda 7 --effetti scene.json
