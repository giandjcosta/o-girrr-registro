# Prova integrata: settimana, MVP dei tifosi e Derby

Preview locale da rivedere prima del commit. Non assegna una versione, non pubblica e non cambia database, premi, video o attività di Claude.

## Percorsi da provare

- **Girrr Sport → Squadra della settimana**: candidatura dei club della giornata, preferenze dimostrative della redazione e dei personaggi, voto degli allenatori facoltativo. Il voto locale si può cambiare o ritirare. La proposta di pesi è 40/40/20 con allenatori e 50/50 senza. Richiamo nelle notifiche Home, votazione anche in Curva → Per te, archivio predisposto in Albo → Record. Nessun vincitore storico attribuito senza una vera votazione.
- **Albo → Derby → Classifica dei Derby**: punti 3/1/0, giocate, vittorie, pareggi e sconfitte. Campionato e Champions Cup separati, con elenco verificabile degli incontri conteggiati. Il resto della pagina Derby originale rimane accessibile.
- **Home → Oggi al Girrr → La tua settimana**: racconto chiuso inizialmente. Archivio in **Carriera → La mia settimana**, una scheda distinta dalle funzioni già esistenti. Ultima giornata aperta, precedenti chiuse. Il comando squadra consente di leggere dieci testi diversi della settimana attuale.

Le due grafiche mantengono i menu nativi: Lega rossa e riquadri con banda dritta; Stadio oro, Lobster e angoli curvi. Le competizioni conservano rosso e azzurro. Il selettore «Prima / Con proposte» confronta le pagine.

## Fonti e limiti

Dati conservati fino alla settima giornata di Campionato e quarta di Champions Cup. Gli incontri della stessa settimana si collegano tramite la giornata di Serie A (`sa`); il riposo non conta come incontro. Il registro dei Derby usa uno snapshot pubblico già presente nel ramo di riferimento, verificato il 12 novembre: otto coppie, sette incontri in Campionato e due in coppa. Non ricostruisce eventuali cambi di ufficialità storici non conservati.

`editoriale.json` contiene dieci testi della G7 scritti sui fatti, compresa la Coppa. L’impronta comprende tutti i risultati precedenti e le giornate di Coppa rilevanti: una correzione dei dati invalida il testo conservato. `racconti.js` conserva sette episodi distinti dell’Oranje e compone un riepilogo dai fatti per gli altri casi. Prima del rilascio occorrerà collegare la produzione e revisione settimanale dei testi alla redazione: questa preview non avvia servizi o generazioni a pagamento. Seguire `redazione/LA-MIA-SETTIMANA.md`.

Le preferenze delle giurie e i voti sono dimostrativi. Non esistono ancora un’assegnazione reale, una scadenza server o un salvataggio condiviso del nuovo premio. Servono una successiva implementazione e un collaudo dedicato; l’archivio resta vuoto finché non esistono premi realmente assegnati.

## Isolamento

`guard.js` precede gli script nativi: blocca invii, autenticazione, RPC e service worker; risolve i Derby da un file locale e mantiene l’identità della preview separata dalla sessione reale. Le sole scritture locali consentite usano `og:prova-tifosi:`. Nessuna modifica al mirror generato o ai sorgenti del sito pubblicato.

Le quattordici copie HTML si rigenerano con:

```sh
python3 lab/prova-tifosi/build.py
python3 anteprima/build.py
node prove/prova_tifosi_model.js
python3 preview_build.py
python3 -m http.server 8899 --directory .preview-site
# In un altro terminale con Playwright e i tre browser disponibili:
python3 prove/prova_tifosi_browser.py
python3 prove/esporta_preview_tifosi.py
```

`TIFOSI_BASE` cambia l’indirizzo della preview; `MOTORI`, `TIFOSI_SCHERMI`, `TIFOSI_OUT` selezionano i collaudi. `WEBKIT_PATH` può indicare un lanciatore locale quando mancano le librerie di sistema. Rapporto e foto in `qa_artifacts/tifosi/` (oppure `TIFOSI_OUT`).

L’esportazione `consegna/revisione-girrr.html` è un unico HTML navigabile che incorpora le risorse per la revisione prima del commit. La cornice adatta letture e navigazione alle risorse incorporate; non va distribuita come sorgente del sito. I collaudi della preview e dell’esportazione sono distinti. Profili iOS/Android/TV emulati; Samsung Internet e Safari su dispositivi reali non sono disponibili in questo ambiente.
