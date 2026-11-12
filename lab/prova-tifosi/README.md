# Prova: MVP dei tifosi, Re dei Derby e La mia settimana

Solo proposta navigabile, non nuova versione e non rilascio. Ingresso: `index.html`.

Le dodici pagine sono copie delle sei pagine native per Lega/Stadio del mirror corrente 5.8.1. `build.py` le rigenera senza modificare il mirror, `ufficiale/` o le funzioni originali. Il modulo `native-ui.js` è la UI corrente con sole costanti dei percorsi adattate per funzionare anche nelle URL di ramo. `prova.js` aggiunge le proposte nei contenitori esistenti. Non è un'altra applicazione che sostituisce le funzioni originali.

## Percorsi da confrontare

- **Home → Notifiche**: una notifica MVP dopo la giornata completa, cliccabile per intero, apre il voto della Curva; la lettura si conserva solo nella prova. Tolti il racconto/riepilogo aggiunto e la scorciatoia ai Re dei Derby. Il riepilogo Oggi al Girrr originale resta.
- **Curva → Riquadro Il sondaggio della giornata**: MVP dei tifosi, prima del sondaggio sulle partite che resta disponibile. La Curva mantiene la grafica sociale chiara/scura; nessun nuovo menu principale.
- **Albo → Derby → Re dei Derby**: collegamento alla pagina Derby originale con classifica aggiunta e tendina delle partite conteggiate. Nessuna scorciatoia Home: accesso dall’Albo → Derby.
- **Carriera → La mia settimana**: tendina con due risultati, punti, posizione, cammino, prossima sfida e citazione registrata. Rimane soltanto nella Carriera, aperta e richiudibile nel dettaglio.
- **Giornale**: anteprima dell'articolo MVP con collegamento esatto al voto.
- **Albo → Stagioni → MVP dei tifosi**: archivio della stagione. La pagina nativa usa attualmente l'etichetta «Stagioni», non viene rinominata. Nessun vincitore storico inventato.

Solo per questa revisione, `?novita=1` mostra una targhetta **Novità rispetto a prima** con la differenza precisa in ogni nuovo modulo. Si può spegnere dalla cornice e non compare nelle visite normali. I collegamenti della mappa aprono direttamente la sezione, incluso il racconto Carriera, mantenendo il parametro nel cambio skin e nei ritorni.

Il comando esterno **Prima / Con proposte** lascia la stessa pagina e la stessa skin. Il selettore esterno della squadra è uno strumento di confronto della prova: non è una scelta dell'identità sul sito reale.

## Dati e regole provvisorie

- Snapshot pubblico del calendario, rivalità e `redazione/dossier.json`, fino alla 7ª giornata completa. Partite delle giornate parziali, buchi e partecipazioni duplicate interrompono il conteggio; niente anticipazioni dalla giornata 8.
- **MVP è un club**, non un singolo giocatore. Sono candidate fino a tre vincitrici. Criterio dimostrativo di selezione: `10 × differenza reti + gol fatti + 2 se in trasferta + (numero squadre − posizione precedente dell'avversaria)/10`. Tre candidature non vengono inventate se ci sono meno vincitrici; se nessuno ha vinto il voto rimane chiuso in attesa della redazione.
- Giuria dimostrativa: 2 preferenze della redazione alla prima candidata, 3 preferenze dei personaggi alle altre (2+1). Sono **preferenze di esempio**, non voti realmente espressi dai personaggi o dalla redazione autonoma. Riferimenti ai personaggi già esistenti: Nonno Cesare, Tifoso Arrabbiato e Statistico Folle; banca originale intatta.
- Ogni allenatore può aggiungere un voto facoltativo. Cambiare scelta sostituisce il voto precedente; ritirarlo annulla la preferenza. Tutte le squadre confrontate nello stesso browser contribuiscono al conteggio locale. Chiave: `og:prova-tifosi:mvp-club-2026-27-g7:SQUADRA`. Nessuna sincronizzazione tra persone/dispositivi. Nessuna scadenza o attribuzione reale in questa prova. Parità: preferenza della redazione, poi ordine alfabetico, entrambi da approvare.
- **Re dei Derby** comprende le sei rivalità storiche con indice ≥80 nel file del sito: 5 incontri conclusi, 4 club classificati, Grodah primo a 6 punti. Non è la classifica completa di tutti i Derby ufficiali: mancano lo storico verificato di accettazioni/veti e le relative date. La tendina elenca ogni incontro conteggiato. Punti, differenza reti, gol fatti; ordine alfabetico solo per visualizzare parità residue. Nessun simulatore.
- **La mia settimana** è calcolata dal calendario, con storico della posizione calcolato usando punti, DR e Fantapunti come il Tabellone. I Fantapunti non entrano nel racconto. La citazione compare soltanto se il dossier è allineato all'ultima giornata completa e viene attribuita alla conferenza corretta. Oranje: 1–1 Apo, 2–1 WOA, 11 punti e 5º posto; prossima Mariana Coneja; frase reale della conferenza G8.

## Isolamento

`guard.js` è il primo script, prima degli script nativi. Intercetta tutte le chiamate esterne e ogni metodo diverso da GET/HEAD; le RPC ricevono risposte vuote locali. Nessuna chiamata Supabase raggiunge la rete, nemmeno le RPC normalmente considerate di lettura. Blocca XHR di scrittura, beacon, invii di form e service worker; le copie non caricano gli script di installazione/tracciamento dell'app. L'identità `fg` nativa è sostituita soltanto in memoria; la sessione reale non è letta né alterata. Le scritture localStorage sono consentite solo nel namespace della prova. Le navigazioni native sono contenute nelle sei pagine della prova; le altre destinazioni vengono segnalate nella cornice senza aprirle.

Il feed Curva reale e le notifiche personali non vengono importati: la prova mantiene il rendering e i personaggi nativi, con risposte server locali vuote. Non sostituisce un collaudo della socialità o dell'autenticazione reali.

## Riproduzione e consegna

```sh
python3 lab/prova-tifosi/build.py
python3 anteprima/build.py
node prove/prova_tifosi_model.js
# Servire la directory che contiene o-girrr-registro su localhost:8765
python3 prove/prova_tifosi_browser.py
```

`TIFOSI_BASE` permette un'origine diversa. Il test cerca Chromium, Firefox e WebKit reali, dichiarando gli eseguibili assenti. Incrocia le due skin e sei pagine con 19 profili (i 16 del collaudo schermi più 390, 768 e 1440). Gli user-agent dei telefoni e TV sono emulazioni, non browser di marca o dispositivi fisici. Verifica assenza di overflow, errori JS, HTTP ≥400 e richieste Supabase. Prova voto/cambio/ritiro/persistenza, ritorni e tendine. `collaudo.json` registra gli esiti; 24 immagini affiancate sono nella cartella `foto/` e nella galleria.

Prima del sito reale: revisione estetica; approvazione delle regole del premio e dell'interpretazione club; identità verificata; voto unico/server e archivio idempotente; chiusura editoriale; storico dei Derby ufficiali; integrazione nelle sorgenti con i lavori di Claude; collaudo WebKit/Firefox e dispositivi fisici; certificazione del Lab e «Vai» di Gianluca. Il prototipo non scrive SQL, non avvia la redazione programmata e non produce audio/PDF/post reali.

Esito della prima bozza: **264 visite, 0 problemi, 24 confronti affiancati**. Matrice iniziale di 228 visite con font di sistema; 36 visite aggiuntive a 320/390/1280 e tutte le foto ripetute con i font originali Google già usati dal sito (Inter, Lobster, Lora), conservati solo in `/tmp/tifosi-font-cache`. La cache non viene aggiunta al repository. Se esiste, il test la usa; `TIFOSI_FOTO=1` ripete queste tre misure conservando il rapporto precedente, `TIFOSI_SOLO_PERCORSI=1` ripete solo le interazioni. I due motori assenti restano non collaudati. PR #56 aperta in bozza, non unita.

Verifica pubblica: Home di ramo caricata in Chromium attraverso il normale avviso «Open the page» di raw.githack, nessun errore JS/HTTP o richiesta Supabase. CI generale del Registro al commit `028f74e`: matrice Chromium/WebKit/Firefox superata sulle pagine correnti; `percorsi-e-cronache` fallito su `prove/prova_navigazione_53.py:49` (`#campo-link` atteso nascosto), fuori dalle pagine modificate. Non dichiarare tutta la CI verde e non confondere quella matrice con un test multipiattaforma del prototipo.

Revisione su indicazioni di Gianluca: notifica MVP nella lista Home; nessun riepilogo personale aggiunto e nessun link Home ai Derby; racconto solo in Carriera. La mappa ora include sei link diretti con `novita=1`. Il collaudo aggiornato comprende 228 visite su 19 profili, 24 foto rigenerate e riprova separata dei percorsi/lettura/link diretti nelle due skin; esiti effettivi in `collaudo.json`. Nel primo giro delle interazioni la verifica immediata della scritta «Letta» precedeva il caricamento: il controllo ora attende l’elemento e conserva il tentativo precedente nel rapporto.
