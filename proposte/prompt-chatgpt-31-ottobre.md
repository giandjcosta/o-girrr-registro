# Prompt per ChatGPT — 31 ottobre 2026

Due prompt da incollare in due chat diverse di ChatGPT. Il primo è il lavoro da fare, il secondo chiede un parere sull'app.

---

## Prompt 1 — Lavori (copia da qui)

Lavori sul repository GitHub `giandjcosta/o-girrr-registro` (Lab e registro della lega O Fant A Girrr). Il sito vero è `giandjcosta/o-fant-a-girrr`: **non lo tocchi mai** (né `gh-pages` né `main`) e non tocchi il database Supabase.

### Prima di iniziare
1. Leggi `AGENTS.md` fino in fondo e segui le sue regole: messaggi di commit che iniziano con `ChatGPT:`, testi in italiano, "Derby" con la D maiuscola, niente riferimenti a fantacalcio/fantacrediti/fantapunti nei testi della lega (salvo i punteggi), niente scommesse nei post ufficiali, niente disclaimer tipo "dati finti".
2. Leggi `STATO.md`, in particolare la sezione «Lavori aperti al 31 ottobre».
3. Crea il ramo `chatgpt/lavori-31-ottobre` **partendo da `claude/coppe-simboli-ere-descrizioni-4jn4ss`** (non da `main`: lì ci sono modifiche al Lab non ancora unite, così non andiamo in conflitto).
4. Non lanciare mai `voci-src/prova_*.py` (generano audio con servizi a pagamento) e non lanciare `ufficiale/build.py` (oggi si ferma e svuota `ufficiale/girrr/`).

### Come rendere tutto controllabile da Gianluca (obbligatorio)
- Ogni novità che si vede deve stare nel Lab (`lab/index.html`) o in una pagina `lab/prova-*.html` collegata da una card del Lab con classe `proto-only`, titolo «Nome · Cosa cambia», una frase su cosa guardare e i pulsanti «Grafica Lega» / «Grafica Stadio» quando serve. Copia lo stile della card «Tabellone · Più dati in classifica».
- Dopo ogni modifica al Lab lancia `python3 anteprima/build.py` e committa anche `anteprima/index.html` e `anteprima/attuale.html`.
- Dopo ogni push scrivi a Gianluca i link di anteprima del ramo, nella forma
  `https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/lavori-31-ottobre/lab/index.html`
  (e lo stesso con `anteprima/attuale.html` per la grafica Lega e `anteprima/index.html` per lo Stadio). Così Gianluca vede tutto prima che si unisca qualcosa.
- Un commit per compito, piccolo. Alla fine apri **una** Pull Request verso `claude/coppe-simboli-ere-descrizioni-4jn4ss` con titolo `ChatGPT: lavori del 31 ottobre`, con per ogni compito: cosa hai cambiato, il link di anteprima, cosa hai provato e cosa no. Non unirla tu.
- Prove prima di consegnare: le pagine devono funzionare a 320 px di larghezza senza scorrere di lato e la console del browser non deve avere errori nuovi. Lancia `python3 prove/collaudo_anteprima_52.py`, `node prove/collaudo_preview52_totogirrr_milestone.js`, `node prove/collaudo_fiducia_universale52.js`, `python3 prove/prova_moviola.py`. Se non puoi aprire un browser, dillo chiaramente.
- Alla fine aggiorna `STATO.md` con un paragrafo «31 ottobre — ChatGPT: …» (cosa è fatto, cosa no) e togli dalla lista «Per ChatGPT» ciò che hai completato.

### Compiti, in quest'ordine
1. **Storia di 17peppe17** (`ufficiale/src/storie.json`): «vince il campionato e lo fa con 34 punti sul secondo» è sbagliato. Nel 2024/25 il PornHub FC fa 70 punti, lo Stif dc 67: sono 3 punti sul secondo (34 era il distacco dal Wakanda di apo, ultimo). Correggi solo quella frase, mantenendo lo stile.
2. **Pagina Derby: rivalità sotto soglia.** Nell'elenco della pagina Derby (Lab, sezione Albo d'oro → I Derby, e `ufficiale/src/derby.js`) compaiono anche coppie con un nome ma rivalità sotto 80 e senza voto né sfida accettata. Devono comparire solo i Derby veri: rivalità da 80 in su, oppure votati, oppure nati da una sfida accettata. Le altre restano nella pagina Rivalità.
3. **Anteprima: la Cassa non si raggiunge.** In `lab/index.html` la funzione `vCarr` ignora `S.cr`, quindi nell'Anteprima la Cassa della Carriera non si apre. Rendila raggiungibile come nel Lab (senza cambiare i 5 tab della Carriera: va dove era prima).
4. **Anteprima: Totogirrr sempre in grafica Lega.** Da `anteprima/index.html` (Stadio) il link al Totogirrr (`anteprima/totogirrr-52.html`) apre la grafica Lega. Passa `?skin=stadio` e fai in modo che la pagina usi i colori dello Stadio (prendi le differenze da `stadio/girrr/totogirrr.html` del sito, solo lettura).
5. **Pulsanti dello Stadio in oro.** Nella grafica Stadio dell'Anteprima i pulsanti principali devono essere oro (come la Lega li ha rossi). Elenca nella PR quali hai cambiato.
6. **Annuario nell'Albo d'oro** (nuovo, richiesto dai giocatori): una sezione «Annuario» nell'Albo d'oro del Lab, una riga per stagione, da riempire ogni anno. Per la 2026/27 calcola dai dati del sito (`data.json`: `teams[].pl[].c` è il prezzo d'acquisto, `P[id].n` il nome):
   - il giocatore più pagato (oggi Lautaro Martinez, 210 milioni, Oranje VC; scrivi «milioni», non «crediti»);
   - la rosa più costosa e quella più economica;
   - capocannoniere della squadra e della lega (gol del calendario), miglior e peggior punteggio di giornata, la vittoria più larga, la serie di vittorie più lunga;
   - il campione, il podio e l'ultimo (quando la stagione finisce; prima «In corso»).

   Le stagioni passate restano vuote («Dato non conservato») finché Gianluca non manda i dati. I numeri si calcolano dai dati, non vanno scritti a mano. Prepara anche un file `ufficiale/src/annuario.json` dove a fine stagione si salva la riga definitiva.
7. **Testi di annuncio della 5.1 e della 5.2** in `proposte/annunci-5-1-5-2.md`: un post per la Curva (profilo Lega) e un messaggio WhatsApp per ciascuna versione, brevi, con le novità vere (vedi `lab/versione-5-1.html` e `lab/versione-5-2.html`). Niente scommesse.
8. **Bio della Curva**: verifica nel browser che follower e posizione in classifica nelle bio dei profili della Curva si aggiornino da soli dopo una giornata (pagina Curva del Lab o del sito in sola lettura). Scrivi in `STATO.md` cosa hai visto, con uno screenshot nella PR se puoi.

Se un compito è più grande del previsto, fermati, scrivilo nella PR e passa al successivo.

---

## Prompt 2 — Parere sull'app (copia da qui)

Sei un esperto di prodotto per app sportive e di community. Leggi il repository GitHub `giandjcosta/o-girrr-registro` (soprattutto `STATO.md`, `STATO-storico.md`, `lab/index.html`) e guarda il sito della lega: https://giandjcosta.github.io/o-fant-a-girrr/girrr/ (Lega) e https://giandjcosta.github.io/o-fant-a-girrr/stadio/girrr/ (Stadio).

È l'app di una lega di dieci amici raccontata come un campionato vero: Giornale, Tabellone, Curva (social interno con profili e bot), Radio settimanale, Albo d'oro con le Ere e i Derby, Carriera con fiducia del presidente e sponsor, Totogirrr (pronostici con crediti), Spogliatoio, conferenze stampa.

Non scrivere codice e non modificare niente. Rispondi in italiano con:
1. Le 5 cose che aggiungeresti, in ordine di valore per il gruppo (cosa farebbe tornare gli amici nell'app ogni giorno), ognuna con: cosa è, perché funziona, quanto è grande (piccola/media/grande) e quali dati usa che esistono già.
2. Statistiche da conservare anno dopo anno nell'Albo d'oro (oltre al giocatore più pagato), indicando quali si possono calcolare dai dati di oggi.
3. Idee per il Tabellone.
4. Le 3 cose che toglieresti o semplificheresti.
5. Rischi che vedi (cose che possono rompersi, confondere o creare litigi nel gruppo).

Regole del contenuto: tutto raccontato come un campionato vero (giocatori, gol, squadre, allenatori), niente riferimenti a fantacalcio o fantacrediti nei testi pubblici, "Derby" con la D maiuscola, i post ufficiali non parlano mai di scommesse.
