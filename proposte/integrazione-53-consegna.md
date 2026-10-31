# Anteprima 5.3: percorsi integrati e cronache

Ramo `chatgpt/integrazione-ui-campo-cronache`, derivato da `chatgpt/lavori-31-ottobre` (`3fd7e40`). PR verso quel ramo; nessuna unione. La PR #39 verso `claude/coppe-simboli-ere-descrizioni-4jn4ss` resta conflittuale (`mergeable=false`, `dirty`, verificato il 31 ottobre). Nessun tentativo di sovrascrivere o risolvere i lavori altrui.

## Dove provare

- [Home Lega](https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/integrazione-ui-campo-cronache/anteprima/home-lega.html)
- [Home Stadio](https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/integrazione-ui-campo-cronache/anteprima/home-stadio.html)
- [Laboratorio con i due ingressi](https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/integrazione-ui-campo-cronache/lab/index.html)

Dalla Home, usare la card **Tabellone**, poi **Campo · Centro della giornata**. Il ritorno riapre la giornata scelta nella medesima skin. L'Albo d'oro parte dalla sua card Home. Anche gli ingressi `anteprima/index.html` e `attuale.html` senza hash portano ora alle nuove Home. Le URL della PR #41 appartengono a un altro ramo e non vengono modificate.

## Cosa è integrato

`anteprima/build.py` genera le due app dal Lab e chiama `anteprima/navigazione.py` solo in modalità preview (mai con `APP_RIL`). Questo modulo genera Home, Tabelloni e Campo. Le Home conservano struttura, card e ordine originali, da copie locali in `anteprima/sorgenti/`; non si scrive in `ufficiale/src/sito/`, `ufficiale/girrr/` o `ufficiale/nuovo/`.

Il Tabellone deriva dai prototipi completi: risultati, giornate, classifiche, Coppa, Derby e Regole preservati. Solo fasce laterali, colori delle posizioni, numeri bianchi, frecce affiancate e segno discreto per la squadra entrata. Su PC i risultati hanno font proporzionati alla colonna, senza spezzare le parole dei nomi. Campo è una sottosezione del Tabellone Campionato; la Coppa conserva le sue funzioni. I link JavaScript di ritorno, oltre agli `href`, sono corretti: la precedente logica riscriveva gli `href` verso la vecchia Home.

Il Campo ha sidebar con ancore funzionanti, campo centrale, confronto KPI, percentuale vittorie definita come vittorie/gare concluse, forma recente, due grafici di punti cumulati alla stessa scala, risultati recenti. Giorno/partita/skin sono nell'URL. Dati da `data.json` pubblico, nessuna posizione dei giocatori o statistica di gioco inventata. Nessun asset copiato da terzi. L'immagine originale del mockup non è stata ancora allegata in questa chat: la struttura segue la descrizione, **la fedeltà al mockup non è certificata**.

L'Albo usa la `.seg.oro-scroll` già esistente: singola riga, pulsanti almeno 44 px, scheda attiva riportata in vista. Nessuna seconda implementazione.

## Cronache e percorso preparatorio

`calcoli/zone_classifica.py` ricostruisce solo turni completi consecutivi, ogni squadra esattamente una volta. Parità ordinate come il Tabellone: Pt, totale, DR, GF, ordine canonico. Verifica aspettative pre-stagione, serie, posizioni e distacchi; seleziona crisi di favorite, rivelazioni, permanenze in vetta/podio/fondo, sorpassi, risalite, ingressi/uscite dal podio, lotta scudetto riaperta. Priorità della notizia, cooldown di quattro turni per tema/squadra, nessuna rotazione per `giornata % 3`. Una storia principale al massimo per giornata, resa disponibile a ciascuna redazione. Candidati stabili non selezionati rimangono eleggibili. Le transizioni meno prioritarie possono cedere a una notizia più importante nella stessa giornata.

Ogni evento espone stagione, chiave idempotente `zona:2026/27:Gn:tipo:squadra`, giornata, squadra, tipo, posizione, durata, attesa e prova. Il commento sotto il post è una riflessione del profilo Giornale, mai una falsa frase attribuita a un allenatore.

Il workflow originale `o-fant-a-girrr/main/.github/workflows/dopo-giornata.yml`, letto senza modificarlo, passa già `site/data.json` a `post_curva.py` come quarto argomento. Con dati reali e modulo mancante ora il processo fallisce esplicitamente; non salta la cronaca in silenzio. In un futuro rilascio andranno portati insieme modulo e aspettative. La prova Moviola ridotta a sei squadre non introduce dipendenze spurie.

`post_curva.py` prepara GS, profilo Giornale e un commento collegato al post GS con chiavi e parent compatibili col publisher esistente. **Nessun publisher invocato contro il sito**. Gli altri post di conferenze e Moviola restano disponibili.

`prepara_dati.py` aspetta turni consecutivi, calcoli della stessa giornata e chiusura dell'eventuale Coppa; controlla l'archivio delle puntate. `copione.py` include una sola cronaca principale; limita i ritornelli su distacchi e ultimo posto e tiene il saluto dell'inviata alla fine del collegamento. Collaudato solo il testo, nessun audio.

### PDF del Giornale

Fonte letta: `o-fant-a-girrr/gh-pages/scripts/pdf_giornale.py` (non nel `main`), con `pdf_settimana.py` e `toto_quote.py`. Il generatore originale rende `testi.json.classifiche` nella seconda pagina. L'adattatore del Registro `calcoli/giornale_classifica.py` aggiunge la cronaca a **una nuova copia** di quei testi, conserva il commento precedente e registra chiave e prova. Un secondo passaggio non duplica il testo.

Preparazione futura, **solo dopo l'approvazione del rilascio**:

```bash
python3 calcoli/giornale_classifica.py COPIA/testi.json COPIA/data.json COPIA/testi-con-cronaca.json
# Nel processo di generazione approvato, passare testi-con-cronaca.json a scripts/pdf_giornale.py.
```

Il generatore del sito e le sue Actions sono invariati. `prove/prova_giornale_cronaca_pdf.py` legge via HTTPS i tre script pubblici in una cartella isolata, costruisce il documento con l'adattatore, verifica la presenza della storia nella pagina 2 e usa il controllo di impaginazione originale. Il PDF prodotto è un artefatto locale di prova, non il Giornale pubblicato.

## Verifiche e limiti

- Build ripetuta identica per tutte le pagine generate; collaudi storici Carriera, milestone/premi, fiducia, Moviola.
- Test delle cronache con giornate parziali, saltate, squadre duplicate/mancanti, priorità, cooldown, chiavi, commenti, Coppa non conclusa, snapshot Radio disallineato, archivio e quattro semi del copione.
- Chromium: Lab → Home → Tabellone → Campionato/Coppa → Campo → cambio partita/giornata/skin → Tabellone → Home → Albo (tutte le schede) → Home, Lega e Stadio a 320/390/768/1280/1440 px. Screenshot salvati dopo click reali. Nessun overflow, eccezione JS, errore console o risposta HTTP 404 nei percorsi provati.
- Prove isolate originali di Tabellone/Campo/Albo rieseguite a 320/768/1280.
- Le letture pubbliche nei browser passano attraverso urllib con TLS verificato perché Chromium di sistema non usa il bundle CA del proxy. La cache è solo di risorse pubbliche. Le RPC sono simulate e mai inoltrate. Questo collaudo non verifica autenticazione o stato reale dei Derby nel database.
- Il workflow legacy `anteprima52-toto-milestone.yml` falliva **prima di avviare i job** (run 41226126988): `run:` conteneva un `:` in una stringa YAML non quotata. Corretto con blocco multilinea solo nel nostro ramo. Gli altri workflow precedenti non vengono dichiarati verdi.
- Non verificati: Safari/iPhone fisico, confronto con il mockup mancante, giornata futura reale, accesso squadra reale e pubblicazione. Nessun merge, sito pubblico, database o audio a pagamento.

Screenshot e rapporto dei percorsi: `prove/risultati-53/`. Il workflow nuovo del Registro è di sola lettura del repository e non rigenera commit automaticamente.
