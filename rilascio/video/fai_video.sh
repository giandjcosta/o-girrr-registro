#!/bin/bash
# Video della giornata, versione scelta da Gianluca il 12 novembre 2026 («B senza folla»):
# base calma del Campionato (MakeBestMusic), «Victory» sulla Champions Cup, ritorno al Campionato per la chiusura, effetti a tempo.
# Uso: rilascio/video/fai_video.sh CARTELLA_DEL_SITO USCITA.mp4   (CARTELLA_DEL_SITO: una copia di gh-pages)
# Serve Remotion installato in rilascio/video/remotion (vedi LEGGIMI.md) e Chrome headless (primo argomento di render.mjs).
set -e
QUI=$(cd "$(dirname "$0")" && pwd)
SITO=$(cd "$1" && pwd)/; USCITA=$2
# Chrome headless: quello indicato in CHROME, se no quello di Playwright se c'è, se no lo scarica Remotion (sul workflow).
if [ -z "$CHROME" ]; then D=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/*/ 2>/dev/null | head -1); [ -n "$D" ] && CHROME=${D}chrome-headless-shell; fi
cd "$QUI/remotion"
MUTO=$(mktemp --suffix=.mp4)
SITO=$SITO USCITA=$MUTO node render.mjs "$CHROME"
# Il passaggio alla Coppa e il ritorno al Campionato seguono la scaletta: logo della Coppa e chiusura da scene.json
read -r COPPA FINE < <(python3 -c "import json;S=json.load(open('scene.json'));t=0;d={}
for k,n in S['scene']:d[k]=t;t+=n/S['fps']
print('%.2f %.2f'%(d['introCoppa']+0.5,t-6.83))")
# 6.5 · Edizione speciale Notte Tropicale (giornata 8, Gianluca 19 novembre 2026): «Welcome to Vice City» (brano libero).
# Campionato: il brano da 0:08 (il tema entra a 0:10,5, sui risultati); sul logo della Coppa l'assolo di chitarra di 2:30
# (il riff esplode a 2:30,5); in chiusura il finale vero del brano.
SKIN=$(python3 -c "import json;print(json.load(open('scene.json')).get('skin') or '')")
if [ "$SKIN" = "notte-tropicale" ] && [ -f "$QUI/musica/vice-city.mp3" ]; then
  python3 "$QUI/monta_musica.py" "$QUI/musica/vice-city.mp3" "$MUTO" "$USCITA" --inizio 8 \
    --dopo "$QUI/musica/vice-city.mp3:150.0:170.0@$COPPA:1.0" \
    --dopo "$QUI/musica/vice-city.mp3:305.0:315.0@$FINE:1.0" \
    --coda 7 --effetti scene.json
  rm -f "$MUTO"; exit 0
fi
python3 "$QUI/monta_musica.py" "$QUI/musica/campionato.mp3" "$MUTO" "$USCITA" \
  --dopo "$QUI/musica/coppa-victory.mp3:19.46:126.7@$COPPA:1.0" \
  --dopo "$QUI/musica/campionato.mp3:64.77:72.6@$FINE:1.0" \
  --coda 7 --effetti scene.json
rm -f "$MUTO"
