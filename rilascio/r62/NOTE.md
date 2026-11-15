# ChatGPT: coordinamento 6.2 — proposta nel Lab

Richiesta di Gianluca del 15 novembre 2026, con rettifica Radio che prevale sul punto 5 del testo iniziale.

## Scelte ricevute

- Numero 6.2 scelto, 6.1.1 preservata.
- Mostrare entrambe le alternative A e B prima della scelta definitiva.
- Approvate per **aperture future**: vigilia fino all’inizio; dopo partita 48 ore dalla pubblicazione dei risultati; MVP 48 ore dalla prima apertura, entro il turno seguente; sfida fino all’inizio; post 24 ore. Non spostare scadenze già annunciate.
- Giornale con commento autentico pertinente quando disponibile.
- Radio: una sola frase aggiunta subito prima della chiusura integrale. Nessuna sostituzione, nessun audio, nessuna nuova puntata o rigenerazione alla chiusura del voto.

## Cosa si può rivedere

`lab/novita-6-2.html` apre la proposta navigabile unica, con Curva, Girrr Sport, Precedenti, Albo, Giornale, Radio, Lega/Stadio e alternative A/B. Ingressi da `lab/index.html` e dalle due Anteprime rigenerate. La 6.1.1 e le sue pagine dello specchio non sono state toccate.

Le preferenze del Lab sono **dimostrative**: IndexedDB in un service worker, condiviso fra schede dello stesso browser. Non fornisce protezione fra dispositivi reali e non è presentato come database della Lega. Il collaudo con due contesti separati usa invece un server locale e PostgreSQL 17.5 WASM/PGlite. Non legge codici reali e non invia voti alla Lega.

Il server locale esegue la SQL della proposta, con autenticazione a codice fittizio. PGlite serializza su una connessione: la prova non sostituisce un collaudo di contesa con più sessioni PostgreSQL native. Il protocollo usa lock della votazione e vincoli unici, e non aggiorna il primo voto.

## Dati reali letti, mai modificati

Letture pubbliche del 15 novembre: `mvp_stato`, `conf_pubbliche`, `conf_dopo_pubbliche`, `curva_feed`; lettura del catalogo delle funzioni PostgreSQL per verificare i vecchi ingressi. Nessuna SQL di modifica sul progetto reale.

- MVP della **7ª** ancora aperto; chiusura conservata **21 novembre 2026 alle 15:00 italiane**. Archivio senza verdetti. Non si proclama la squadra provvisoriamente prima.
- Conferenze effettivamente pubblicate, con squadra/giornata; dove assenti, «Dato non conservato».
- Giornale: tre A4 reali (`lab/coordinamento-62/giornale.pdf`). Voto aperto della 7ª e commento dell’Apo team sulla sconfitta 3-2 con Mariana Coneja; testo integrale e fonte nel `commento-reale.json` (post pubblico 38). Non è presentato come preferenza MVP. Il vecchio coro editoriale è sostituito dalla dichiarazione autentica; le metriche social inventate sono eliminate. Restano i testi delle notizie sportive, classifica, tabellini, pagelle, formazione e programma, con nuova disposizione.
- Radio: `radio-copione.txt` mostra prima/dopo e copione completo. 26 → 27 battute nel caso di prova; tutte le 26 originarie restano identiche. La sola aggiunta è evidenziata.

Il PDF usa il generatore corrente in una copia locale e reimpagina in colonne bilanciate: stessi caratteri, niente `FIT_JS` o riduzione in scala. Le tre finestre di stampa contengono complessivamente ogni carattere una volta sola, verificato con DOM Range oltre al numero reale di pagine del PDF. Il renderer rifiuta contenuti troppo lunghi: non taglia, non scala e non genera una quarta pagina. Non è una garanzia automatica per qualunque futura edizione.

## SQL pronta per revisione, non applicata

`sql/votazioni-62-proposta.sql` aggiunge il catalogo unico (fonte/identificativo, prima apertura, scadenza) e RPC personali/autenticate. Non duplica i voti: i sondaggi della sfida continuano a usare `sondaggio_private.voti`, i post `curva_poll/curva_vote`, l’MVP `mvp_private`. Si aggiornano anche i vecchi ingressi affinché non sovrascrivano il primo voto; scelta e conteggi sono riletti dal server. Il catalogo limita centralmente i risultati agli ultimi due, ordinati per chiusura/ID. Nessun dato storico viene eliminato.

Le aperture server MVP conservano la scadenza già stabilita, anche senza voti umani; nuove aperture al massimo 48 ore. I post devono mantenere fonte, scelte e creazione originali. Le giurie 40/40/20 e 50/50 restano quelle della 6.0. La chiusura definitiva e l’archivio rimangono nel normale giro `mvp_chiudi`, senza audio.

`calcoli/finestre62.py` prepara le finestre approvate: prima apertura persistente, orari con fuso, ore effettive anche al cambio dell’ora. Scadenze precedenti hanno sempre precedenza. I metadati mostrati dalla UI provengono dal server, senza ricomputare la finestra all’apertura della pagina.

**Prima di un eventuale rilascio vero**: completare/validare il catalogo delle sfide dal calendario reale e quello dei post già creati, confrontare le scelte con i voti esistenti, integrare l’adapter nelle pagine pubblicate e nei loro vecchi moduli, collegare il pianificatore alle automazioni attuali e il dossier editoriale alla preparazione normale di Radio/Giornale. Non sostituire le pagine reali con il simulatore del Lab e non applicare questa SQL senza «Vai» esplicito. L’integrazione nel frontend di produzione e nelle automazioni non è distribuita da questa proposta.

## Come ripetere le prove

- `npm ci --prefix prove/v62`
- `python3 prove/v62/testi.py`
- `python3 prove/v62/prepara_radio.py COPIA_LOCALE_GH_PAGES`
- `node prove/v62/sql.cjs`
- `PORT=8863 node prove/v62/server.cjs`
- `BASE=http://127.0.0.1:8863/lab/coordinamento-62/ MOTORE=chromium node prove/v62/browser.cjs`
- Ripetere con `MOTORE=webkit` e `MOTORE=firefox`. `WEBKIT_PATH` può indicare il browser compatibile dell’ambiente. Firefox richiede `FIREFOX_CERT_PROFILE` con la CA del proxy; non si disattiva TLS.
- `python3 prove/v62/prepara_pdf.py COPIA_LOCALE_GH_PAGES`; `node prove/v62/pdf.cjs`

I browser devono essere installati con le loro librerie. Qui Chromium e WebKit reali: 16 profili × 2 grafiche ciascuno, zero problemi finali, alternative A/B, ingressi, ospite, due contesti separati e pagina servita da SW. Rete esterna bloccata anche dentro `fetch` delle pagine; nessuna scrittura possibile alla Lega. Firefox non disponibile per timeout di avvio/SWGL/sandbox nel container, anche su Xvfb; profilo NSS preparato, TLS preservato. Dispositivi fisici non disponibili. Rapporti in `prove/v62/risultati-*.json`.

## Autorizzazioni

Nessun merge o pubblicazione del sito vero, modifica Supabase o servizio vocale. Nessuna nuova voce in `versioni.json`. Gianluca ha dato il «Vai al solo Lab» il 15 novembre 2026, autorizzando il merge della PR #92 nel Registro. Il sito vero, Supabase e le voci restano esclusi. I test generali di Filtri/Panorama presentano la stessa anomalia già presente sul main precedente (`e9da729`, run `43722387690`), documentata in STATO.md; non sono dichiarati superati.
