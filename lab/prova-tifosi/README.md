# Prova: La mia settimana, MVP e Derby della stagione

Prototipo di revisione della PR #56, non nuova versione e non rilascio. Ingresso `index.html`; `?novita=1` mostra le evidenze temporanee e le differenze.

## Sistemazioni scelte da Gianluca

- **Carriera → Storia → La mia settimana**. Il componente appare soltanto nella scheda Storia, dopo i pulsanti nativi. Una tendina per ogni giornata completa: la più recente aperta, le precedenti chiuse. Ogni racconto mostra risultato nell'ordine casa/ospite, posizione e punti di allora, ultime partite, successiva avversaria e grafico facoltativo. Le schede storiche degli allenatori restano. Passando a Panoramica, la settimana scompare. Link diretto: `lega/app.html?novita=1&sezione=storia#carriera` (anche `stadio/`).
- **Albo → Record → Record 2026/27 → MVP della giornata**. Tendina stagionale distinta dagli altri record; il premio non è più in Stagioni né sopra la pagina Albo. Il link `albo.html?novita=1#pt-archivio` seleziona Record e apre la stagione. L'archivio mostra soltanto l'esempio della 7ª giornata: niente vincitori passati inventati.
- **Albo → Derby → Derby della stagione 2026/27**. Una voce di sottomenu apre la nuova pagina `derby-stagione.html`. Mostra Derby vinti, pareggi, sconfitte e giocati; niente punti classifica. Chi ha le stesse vittorie è a pari merito. Restano la pagina Derby originale e gli altri suoi contenuti. Collegamento di ritorno all'Albo/Derby, nessuna scorciatoia Home. Link al menu: `albo.html?novita=1#pt-derby-access`.
- **Home → Notifiche**. Una notifica MVP dopo la giornata completa apre direttamente il verdetto; lettura salvata solo nel namespace locale della prova. Nessun riepilogo personale aggiunto nella Home: Oggi al Girrr originale resta.
- **MVP**. Tre candidate; solo preferenze dimostrative della redazione e del pubblico rappresentato dai personaggi della Curva. Nessun bottone per votare, attesa degli allenatori o uso dei loro vecchi voti locali. Il verdetto precede il Giornale. La Curva mantiene tema chiaro/scuro e il sondaggio sulle partite separato.

Il Giornale conserva ancora la scheda di anteprima del verdetto: **l'impaginazione dentro il vero numero/PDF non è completata in questa revisione dei tre menu**. Non dichiararla già integrata. La collocazione scelta è dentro il numero della giornata, non sopra l'elenco delle uscite; richiede un passaggio successivo della prova.

## Dati, calcoli e limiti

Snapshot pubblico fino alla 7ª giornata completa. Il modello interrompe il conteggio a una giornata parziale, mancante o con squadre duplicate. I racconti storici usano soltanto le partite già concluse a quel punto; la citazione compare solo quando il dossier è allineato alla giornata. Per Oranje G7: WOA 1–2 Oranje, 11 punti e 5º posto; 4 punti nelle ultime due; successiva Mariana Coneja. La frase «Una partita alla volta, con umiltà» è dalla conferenza prima della G8, non attribuita alle settimane precedenti.

Derby: fonte corretta nel file `derby-ufficiali.json`, estratto il 12 novembre con soli SELECT da `derby_attivi` e sfide accettate con nome confermato. Otto coppie ufficiali attive, sette incontri conclusi, cinque club. Oranje: 0 V, 1 N, 1 P in 2 Derby; The Continental (1–1 Apo, G6), Derby dell'Emma (0–3 The Blues Brothers, G5). Le rivalità non determinano più l'ammissione. Il conteggio stagionale incrocia il registro attuale con il calendario completato; non ricostruisce l'intera storia dei cambi di ufficialità. `dal` è il momento registrato di attivazione nel sistema, non va spacciato per data d'origine storica dei sei Derby preesistenti. Il browser non interroga Supabase: anche la pagina Derby originale riceve uno snapshot locale dei Derby confermati. Nessun simulatore.

La voce del sottomenu ora riusa esattamente il componente nativo delle voci «I Derby della Lega» e «Le rivalità»: `a.card`, titolo e descrizione, stessa geometria e colori. Il collaudo confronta gli stili calcolati con un'altra voce originale.

MVP significa club. Fino a tre vincitrici candidate: criterio dimostrativo `10 × DR partita + gol + 2 se in trasferta + (numero squadre − posizione precedente avversaria)/10`. Senza vincitrici, scelta non disponibile. Preferenze di esempio: 2 della redazione alla prima candidata, 3 dei personaggi alle altre (2+1). Parità risolta dalla redazione; regola ancora da approvare. I voti umani precedenti non influiscono più. Non sono voti effettivamente espressi dalla redazione autonoma o premi realmente assegnati. Composizione, pesi, scadenza e archivio definitivo restano da approvare e integrare prima del sito.

## Struttura e isolamento

Quattordici copie native Lega/Stadio, comprese le due nuove pagine Derby della stagione. `build.py` le rigenera dal mirror senza modificarlo. `native-ui.js` conserva le funzioni originali, con sole costanti dei percorsi adattate alle URL di ramo. `prova.js` inserisce i moduli nelle schede selezionate; nessuna modifica alle sorgenti ufficiali o ai lavori di Claude.

`guard.js` è il primo script: nessuna RPC reale, GET/HEAD solo dello stesso sito della prova, XHR di scrittura/beacon/form/service worker esclusi, sessione vera non letta né modificata. Risposte locali vuote per feed e notifiche server; soltanto lo stato Derby riceve lo snapshot ufficiale locale, senza eseguire una RPC. Scritture localStorage solo nel namespace `og:prova-tifosi:`. Le pagine non installano l'app e non caricano il tracker originale. Nessuna modifica Supabase, post, audio, PDF reale o redazione programmata avviati.

## Riproduzione

```sh
python3 lab/prova-tifosi/build.py
python3 anteprima/build.py
node prove/prova_tifosi_model.js
# Servire la cartella che contiene o-girrr-registro su localhost:8765
python3 prove/prova_tifosi_browser.py
```

`TIFOSI_BASE` cambia origine; `TIFOSI_FOTO=1` ripete 320/390/1280 e le fotografie; `TIFOSI_SOLO_PERCORSI=1` ripete le interazioni conservando la matrice precedente e archiviando i tentativi dei percorsi. Rapporto in `collaudo.json`, 24 confronti prima/dopo e immagini delle tendine aperte/chiuse in `foto/`. I font Google già usati dal sito (Inter, Lobster, Lora) sono in una cache temporanea locale, non nel repository; senza cache il test usa il ripiego di sistema. I profili iOS/Android/TV sono emulazioni, non dispositivi o browser di marca reali. Firefox/WebKit locali assenti.

CI generale del Registro: nel primo commit della PR la matrice delle pagine correnti ha passato Chromium/WebKit/Firefox; `percorsi-e-cronache` falliva su `prove/prova_navigazione_53.py:49` (`#campo-link` atteso nascosto), fuori dalle pagine qui modificate. Non confondere quel collaudo con la nuova prova e non dichiarare tutta la CI verde. Vecchi tentativi ed esiti sono conservati in STATO e nel rapporto.

## Scrittura della settimana

Regola permanente per tutte le IA: `AGENTS.md` → `redazione/LA-MIA-SETTIMANA.md`. Titolo e tre paragrafi con un fatto centrale, un filo di stagione e il capitolo successivo; niente elenchi di risultati in prosa, scene inventate, sequenze dei gol dedotte o citazioni spostate nel tempo.

`racconti.js` contiene sette episodi dell'Oranje rivisti editorialmente e una composizione per gli altri club guidata da risultato, serie, posizione e Derby ufficiale. Le sette bozze curate sono riusate solo quando coincide l'impronta integrale del calendario fino a quella giornata; un dato corretto attiva la composizione dai nuovi fatti. Nessuna generazione a pagamento o scrittura nel sistema della redazione. I testi delle altre squadre restano da rivedere editorialmente prima del rilascio. Le citazioni vengono usate solo se la conferenza conservata è davvero quella prima della giornata successiva.
