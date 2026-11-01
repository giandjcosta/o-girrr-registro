# Prompt per la prossima chat — completare integrazione UI, Campo e cronache (31 ottobre 2026)

Sei l'assistente incaricato di **completare e integrare**, non reinventare, i lavori già sviluppati per la Lega O Girrr. Gianluca ha aperto l'Anteprima 5.3 su iPhone e **non vede la nuova grafica del Tabellone**, pur vedendo alcune novità dell'Albo d'oro. La richiesta è correggere questo problema, migliorare la dashboard Campo in modo molto più simile al mockup mostrato dall'utente **soprattutto su PC**, e completare con criterio le cronache sulle zone di classifica.

## 0. Repository, responsabilità e confini invalicabili
- Lavorare soltanto nel repository **`giandjcosta/o-girrr-registro`**.
- Leggere **tutto `AGENTS.md` e `STATO.md`** prima di modificare codice; leggere l'ultima sezione **«31 ottobre — Verifica integrazione e consegna alla prossima chat»**.
- Base di lavoro: **`chatgpt/lavori-31-ottobre`**, che contiene i prototipi esistenti. La PR **#39** è aperta verso **`claude/coppe-simboli-ere-descrizioni-4jn4ss`**. Controllarne stato e merge conflicts; l'API GitHub ha segnalato `mergeable=false / dirty` alla verifica del 31 ottobre: **NON presumere che sia unibile**.
- **Crea un nuovo ramo dal ramo esistente**, con prefisso del *tuo* autore (`claude/...`, `chatgpt/...`, `grok/...` ecc.). Niente commit senza prefisso corrispondente, niente force-push, niente modifiche a rami di altri. Apri una PR contro `chatgpt/lavori-31-ottobre` o concorda prima una strategia di integrazione sicura.
- Il sito reale è `giandjcosta/o-fant-a-girrr`: **SOLO LETTURA**, mai modificarne `main`, `gh-pages` o GitHub Actions. Non modificare database Supabase, non generare nuove radio/audio a pagamento e non eseguire `voci-src/prova_*.py`. **Non eseguire `ufficiale/build.py`**: può svuotare la directory di output.
- Regole editoriali: tutto in italiano, «Derby» con la D maiuscola, no riferimenti a fantacalcio/crediti nelle narrazioni della Lega, no scommesse nei post ufficiali, nessun disclaimer che rovini l'immersione. La retrocessione è una **zona narrativa**: non aggiungere un meccanismo reale di retrocessione.

## 1. Diagnosi confermata: perché non vede le modifiche
- Le nuove classifica e fasce colorate sono in **`lab/prova-tabellone-lega.html`** e **`lab/prova-tabellone-stadio.html`**, **non nella pagina Tabellone principale integrata nelle Anteprime**.
- Le anteprime **`anteprima/index.html`** (Stadio) e **`anteprima/attuale.html`** (Lega) sono generate da **`lab/index.html`** e **`anteprima/build.py`**, e in esse le card `.proto-only` sono nascoste con CSS `display:none!important`. Quindi la card «Tabellone · Più dati in classifica» e quella «Campo · Centro della giornata» non sono visibili nell'Anteprima 5.3.
- I link nei prototipi copiati nell'Anteprima sono relativi `href="prova-tabellone-...html"`, e da `anteprima/` non puntano a `lab/prova-tabellone-...html`. Non basta togliere `.proto-only` senza correggere **routing, posizione nel menu e path**.
- Le sorgenti congelate del Tabellone, da ispezionare senza alterarle: **`ufficiale/src/sito/girrr/tabellone.html`** (Lega) e **`ufficiale/src/sito/stadio/girrr/tabellone.html`** (Stadio). La patch preparatoria `rilascio/tabellone_dati.py` NON include ancora tutta la nuova grafica della classifica. Non confondere queste sorgenti con le pagine prototipo.
- I test precedenti a 320/768/1280 px erano **positivi sulle pagine isolate**, non dimostravano che l'utente arrivasse alle nuove schermate tramite i veri menu. La nuova verifica deve seguire i click reali dall'Home.

## 2. PRIORITÀ MASSIMA — Tabellone integrato nella vera navigazione dell'Anteprima
1. Individua nel sito di sola lettura il posto originale della pagina **Tabellone** e come vi arriva l'utente da Home/menu. Riproduci esattamente quel percorso navigabile nelle **due Anteprime 5.3**, non un menu inventato o una card lasciata in alto a caso.
2. Porta nella pagina finale **il lavoro già presente nelle due pagine `lab/prova-tabellone-*.html`**, conservando tutte le funzioni precedenti (giornate, risultati, classifiche, dati, Derby, regole).
3. Colonne «Squadra», «DR», «Pt», «Fantapunti» più leggibili, anche su iPhone; per PC mostra anche G/V/N/P/GF/GS e usa spazio e font da desktop. NON tagliare nomi o numeri.
4. Colora **solo la sottile barra laterale della riga**, non l'intero sfondo. Numeri della posizione: **1 oro, 2 argento, 3 bronzo, 4–penultimo bianco, ultimo rosso**. Numeri DR/Pt/totale **sempre bianchi**. Freccia ▲/▼ **affiancata** al numero di posizione, non sotto. Rispetta anche l'evidenza della squadra dell'utente, senza compromettere la semantica dei colori.
5. Legenda «Scudetto», «Podio» e «Retrocessione» (ultimo). Lascia «Sfida retrocessione» come elemento sportivo narrativo e **non cambiare i regolamenti reali**.
6. Crea percorsi chiari dalla Home fino alla classifica e ritorno; tutte le due skin devono funzionare e usare il design corretto. Non introdurre nuovi tab arbitrari.

## 3. Albo d'oro: tab orizzontali da telefono **e** PC
- Già esiste `.seg.oro-scroll` dentro `lab/index.html`, e i CSS sono nelle due Anteprime: **non duplicare**.
- Verifica tramite click nell'Anteprima reale che «La storia della Lega», «L'Era Contemporanea», «L'Era dei Titani», «I Derby», «Annuario», «Albo di Latta», «Gli allenatori», «Regole» stiano **su una sola fila scorrevole** senza andare a capo. Su PC usa abbastanza spazio e comandi chiaramente selezionati; su mobile scorrimento fluido e tasti almeno 44px. L'attivo deve rimanere visibile dopo lo scroll e la navigazione.

## 4. Campo · Centro della giornata — redesign **più fedele al mockup**, soprattutto desktop
- Il prototipo attuale **`lab/prova-dashboard-campo.html`** è funzionale ma **troppo semplice** rispetto all'immagine mostrata da Gianluca nella chat. Chiedigli di ri-allegare lo screenshot se la nuova chat non può vederlo: è una **dashboard calcistica futuristica blu notte**, con **menu laterale verticale**, **campo verde centrale**, **pannelli di numeri a destra**, **grafici circolari / strumenti**, **grafici andamento sotto**, gerarchie visive e icone curate. NON basta ingrandire il semplice SVG esistente.
- **PC (priorità estetica)**: progettare un vero cockpit sportivo con sidebar di navigazione utile, header con giornata e partita selezionata, grande campo come focus, pannelli KPI laterali e grafici in basso. Usa CSS Grid, proporzioni curate, pannelli nitidi, linee sottili, gerarchie chiare, interazioni consistenti e colori della skin (rosso Lega / oro Stadio), senza un'interfaccia tutta rossa.
- **Tablet**: due colonne dove c'è spazio, poi stacking ordinato. **Telefono**: campo ben leggibile, pannelli verticali, navigazione compressa in selettore/menu o scorrimento orizzontale, nessun overflow.
- Mantieni interazione tra giornata e partita e cambio Lega/Stadio, con URL coerenti; collega il Campo dal **sottomenu pertinente al Tabellone / Giornata** delle Anteprime, non come top-level sconnesso né solo card nascosta.
- I dati validi arrivano da `data.json` del sito in sola lettura: risultati, punti, posizione, GF/GS/DR, vittorie/pareggi/sconfitte, forma, risultati recenti, andamento. Indicatori circolari ammessi se rappresentano **metriche vere e definite** (ad esempio percentuale vittorie o andamento), non «possesso», «tiri», heatmap o posizioni reali di giocatori che non sono registrate. Non copiare asset di terzi da pagine casuali.
- Inserisci un titolo/azione reale per i pannelli, evita etichette inglesi casuali e demo con numeri inventati. Dimostra il desktop con screenshot **1280 e 1440 px**, più 320/390 e 768 px.

## 5. Notizie sulla vetta, il podio e la zona retrocessione: **completare** l'integrazione
Esiste una prima implementazione:
- `calcoli/zone_classifica.py` → conta 3 giornate consecutive in vetta, sul podio o all'ultimo posto; reminder ogni 4; crisi anticipata per favorita top 3 ultima da 2 giornate; sceglie al massimo una storia e alterna Radio/Curva/profilo Giornale.
- `calcoli/post_curva.py` → prepara potenziali post, ma il percorso che usa un file temporaneo per la prova Moviola **salta il modulo se non è disponibile**: verificare il **workflow reale** e il caricamento del modulo.
- `voci-src/prepara_dati.py` e `voci-src/copione.py` → preparano la notizia per la futura Radio senza generare audio.
- `calcoli/aspettative.json` → aspettative pre-stagione reali per identificare le favorite. Non dedurre da nome o simpatia.

Da completare:
1. Valutare casi interessanti, non solo leader fisso o ultimo: **big in crisi**, squadra rivelazione sul podio, risalita dalla zona retrocessione, ingresso/uscita dal podio, lotta scudetto, permanenza prolungata in fondo, sorpassi significativi; eventi derivati dal calendario completato e da aspettative verificabili.
2. Evitare ogni giornata la solita «X è primo»: soglie, finestre editoriali e cooldown. Controllare che un evento importante **non venga perso** solo per la semplice rotazione deterministica `giornata % 3`. Priorità proporzionata alla notizia, massimo un fatto principale per canale/giornata, ma lascia spazio a post/commenti pertinenti.
3. Integrare la cronaca anche nei **commenti della Curva**, nei post di Girrr Sport, nel profilo Giornale e nel **Giornale PDF** (quest'ultimo **manca completamente**). Individuare e documentare il generatore in sola lettura nel sito (`scripts/pdf_giornale.py`) e preparare una soluzione compatibile **nel registro**, senza scrivere nel sito. Qualsiasi preparazione di post per produzione deve attendere «Vai».
4. Radio: testare il **copione testuale**, la sequenza dopo la chiusura della giornata, nessuna duplicazione con altro contenuto su distacchi/podio e la corretta inclusione della storia; **non produrre audio**.
5. Tutti gli eventi devono essere verificabili a posteriori, con chiave idempotente per evitare doppioni. Nessun post inviato, nessun database scritto e nessuna pubblicazione durante la prova.

## 6. Test obbligatori: percorso reale, non soltanto pagine isolate
- Esegui `python3 anteprima/build.py` dopo ogni modifica al Lab e **committa `anteprima/index.html` e `anteprima/attuale.html`** insieme alle modifiche.
- Usa Chromium o Playwright per aprire il **Lab**, poi la **Home della vera Anteprima**, e da lì **cliccare il menu reale** fino a Tabellone, Campo, Albo d'oro, e tornare alla Home. Testa grafica Lega e Stadio.
- Prova 320, **390**, 768, **1280 e 1440** px, senza overflow orizzontale, navigazione rotta, errori JS o richieste 404; verifica che le differenze siano **effettivamente visibili nel percorso che apre Gianluca**, senza dipendere da card `proto-only`.
- Riesegui `python3 prove/collaudo_anteprima_52.py`, `node prove/collaudo_preview52_totogirrr_milestone.js`, `node prove/collaudo_fiducia_universale52.js`, `python3 prove/prova_moviola.py`, `python3 prove/prova_zone_classifica.py` e `python3 prove/prova_tabellone_campo_browser.py`. Aggiungi prove integrate delle cronache con casi limite e giornate parziali.
- Includi **screenshot non solo dei prototipi isolati**, ma del Tabellone e del Campo raggiunti **tramite i menu** a 390 e 1280/1440 px.
- Se il browser non è disponibile, scrivilo: non dichiarare «pronto» sulla sola base di build o test statici. Valuta cache raw.githack, ma verifica **prima** che i file/link puntino davvero ai contenuti aggiornati.

## 7. Deliverable e stop di sicurezza
- Commit piccoli con il prefisso corretto e **PR NON unita**, con screenshot, screenshot desktop aderenti al mockup, URL anteprima Lega/Stadio, checklist dei percorsi provati, cosa manca e cosa non è stato verificato.
- Aggiorna `STATO.md`: marca «INTEGRATO» solo ciò che compare davvero nel menu dell'Anteprima e «PROTOTIPO» il resto. Documenta anche eventuali workflow già in errore o conflitti della PR precedente, senza nasconderli.
- Se una parte si rivela grande, documenta il blocco, passa alle altre; nessun intervento distruttivo né deploy di produzione senza approvazione esplicita di Gianluca.

**Criterio di accettazione fondamentale:** Gianluca apre il link dell'**Anteprima 5.3**, raggiunge **Tabellone** e **Campo** nei sottomenu corretti, vede le nuove grafiche su iPhone **e soprattutto su PC**, e può confrontare Lega/Stadio. Non basta aggiungere un'altra pagina `prova-*.html` che nessuno raggiunge.