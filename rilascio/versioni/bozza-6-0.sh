#!/bin/bash
# Bozza della voce 6.0 di versioni.json (Claude, 13 novembre 2026). Da rivedere con Gianluca prima del rilascio.
# Senza argomenti stampa soltanto la voce (--prova): non scrive niente.
# Al rilascio, dopo il «Vai» e la conferma del numero:
#   bash rilascio/versioni/bozza-6-0.sh --file rilascio/versioni/versioni.json --file COPIA_GH_PAGES/versioni.json
# Livello editoriale nel messaggio (niente fantapunti né scommesse), tecnico nel changelog.
cd "$(dirname "$0")/../.." || exit 1
[ $# -eq 0 ] && set -- --prova
python3 rilascio/versioni/aggiungi.py --tipo grande --titolo "La Curva del tuo telefono e il video della giornata" \
  --messaggio "🎬 **O Girrr 6.0 è online!** La Curva cambia faccia: su iPhone ha lo stile di iPhone, su Android quello di Android, e mentre leggete non salta più, perché i cori nuovi arrivano con la pillola «Nuovi cori». Dopo ogni giornata esce il video in mezzo minuto, nella scheda Video di Girrr Sport accanto alla Radio, con tutti quelli dalla 1ª giornata. Con «Condividi la giornata» mandate al gruppo video, Radio, Tabelloni e Giornale in un tocco. E poi la Squadra MVP dei tifosi, la classifica dei Derby e «La tua settimana», il racconto della vostra squadra. Buona giornata a tutti! ⚽" \
  --voce "Curva: Stile di iPhone (vetro e pillole) sugli iPhone e iPad, stile Android (Material 3) sui telefoni e tablet Android; PC e TV restano come prima" \
  --voce "Curva: La pagina non si ricrea più a ogni aggiornamento: cambiano solo i cori nuovi o modificati" \
  --voce "Curva: Pillola «Nuovi cori» con le facce di chi ha scritto; toccandola si torna su" \
  --voce "Curva: Notifiche divise in Attività (applausi, rilanci, visualizzazioni) e Menzioni" \
  --voce "Curva: Bozza del coro che resta se esci, link a ogni coro e Condividi con l'immagine e l'anteprima per WhatsApp" \
  --voce "Curva: Impostazioni con Aspetto (Automatico, Chiaro, Scuro), suono dell'applauso e colori della lega o della tua squadra" \
  --voce "Curva: 15 nuovi personaggi, tra cui Radio Girrr e VAR del Girrr verificati" \
  --voce "Girrr Sport: Scheda Video con il video della giornata (risultati, podio, classifica, Champions Cup, partite da non perdere) e l'archivio dalla 1ª giornata" \
  --voce "Girrr Sport: Il video esce da solo dopo i calcoli della giornata" \
  --voce "Girrr Sport: Squadra MVP dei tifosi: scelgono redazione e personaggi, gli allenatori possono votare, cambiare o ritirare il voto (uno per squadra)" \
  --voce "Radio: Fischio d'inizio e triplice fischio veri in apertura e chiusura" \
  --voce "Condividi: «Condividi la giornata» in Home e nel Giornale: video, puntata della Radio, Tabelloni ufficiali di Campionato e Champions Cup e copertina del Giornale, con la spunta per togliere quello che non serve" \
  --voce "Derby: Classifica dei Derby della stagione (3 punti la vittoria, 1 il pareggio), con Campionato e Champions Cup separati" \
  --voce "Home: «La tua settimana» in Oggi al Girrr, il racconto della giornata della tua squadra" \
  --voce "Carriera: Archivio delle settimane della tua squadra" \
  --voce "Albo d'oro: Archivio dei verdetti MVP nei Record della stagione" \
  "$@"
