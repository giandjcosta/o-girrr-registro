# Regole comuni di lavoro · O Girrr

Valgono per tutti: Claude, ChatGPT, Grok, Copilot, Perplexity, Aider, VS Code e Gianluca (decisione di Gianluca, 16 novembre 2026).
Ognuno può usare i suoi metodi: per esempio ChatGPT è molto bravo nella grafica e nel front end. Queste sono le **basi comuni**, perché chi riprende il lavoro di un altro trovi tutto in ordine.
Le regole di progetto restano in `AGENTS.md` (contenuti, grafiche Lega e Stadio, versioni, «Vai» di Gianluca). Questo file dice **come** si lavora.

## 0. Prima di toccare qualcosa
1. Leggi `AGENTS.md`, `STATO.md` e **`LAVORI-IN-CORSO.md`**. Se qualcuno ha lasciato un lavoro a metà, riparti da lì e non rifarlo da capo.
2. `git pull` su tutti e due i repository. Guarda Pull Request e rami aperti.
3. Scrivi in `LAVORI-IN-CORSO.md` cosa stai per fare (vedi il punto 6), così se la chat si interrompe chi arriva dopo lo sa.

## 1. Scrivere il codice
- **Una fonte sola.** Una correzione destinata al sito va nello script del rilascio (`rilascio/rXYZ/…`). Il Lab si rigenera da lì (per la 6.2.1: `rilascio/r621/applica.py` poi `rilascio/r621/lab.py`). Mai correggere a mano solo la copia nel Lab e solo il rilascio: le due versioni si separano e quello che si prova non è quello che va online.
- **Sostituzioni che si fermano se il file è cambiato.** Gli script di rilascio cercano il testo esatto da sostituire e si fermano se non lo trovano (oppure confrontano l'impronta sha256 in `ORIGINALI.json`). Non togliere questi controlli: sono quelli che evitano di pubblicare sopra una modifica di un altro.
- **Rieseguibili.** Lanciare due volte uno script di rilascio deve dare lo stesso risultato (alla seconda volta: «0 file cambiati»).
- **Lega e Stadio insieme.** Quasi ogni modifica va nelle due copie (`girrr/` e `stadio/girrr/`). Attenzione ai percorsi relativi.
- **Versione nell'indirizzo dei file.** Se cambi un `.js` o un `.css`, cambia anche il `?v=` nelle pagine che lo caricano, altrimenti i telefoni tengono quello vecchio.
- **Un solo responsabile per ogni movimento.** Uno scorrimento, un'animazione o un ridisegno deve avere un solo codice che lo comanda. Nella Carriera la fila delle pillole era mossa da tre codici insieme e sul telefono si fermava a metà.
- **Animazioni.** Sempre fluide e sempre con `prefers-reduced-motion`. Al tocco niente alone del browser: `-webkit-tap-highlight-color:transparent`, con un segnale proprio, per esempio `:active{opacity:.7}`.
- **Commenti nel codice** in italiano, con data e motivo («6.2.1 (Gianluca): …»). Sono il diario di chi arriva dopo.
- **Niente segreti** nel codice. Le chiavi «publishable» di Supabase già presenti sono pubbliche per scelta.

## 2. Provare
- **Sempre nel browser vero, non solo leggendo il codice.** Playwright con Chromium: `require('playwright')` funziona da qualsiasi cartella nell'ambiente di Claude. Su GitHub i workflow provano Chromium, WebKit e Firefox.
- **Telefono = tocco vero.** Su telefono usa `page.touchscreen.tap(x, y)` su un punto **visibile** dell'elemento. `locator.tap()` e `click()` prima fanno scorrere la pagina fino all'elemento: nascondono proprio i difetti di posizione e di scorrimento.
- **Misura, non indovinare.** Per le animazioni registra la posizione fotogramma per fotogramma (`requestAnimationFrame`) e intercetta chi muove cosa (`scrollTo`, `scrollLeft`, `scrollIntoView`). Così si vede subito se due codici si contendono lo stesso movimento.
- **Schermi:** 320 px (iPhone SE) senza scorrimento laterale, telefono grande, tablet, PC 1280 e 1920, monitor 2560 e TV (`prove/prova_schermi_56.js`). A Gianluca le foto su PC e TV.
- **Console senza errori nuovi.** Se un errore c'era già, confrontalo con la versione pubblicata e dillo.
- **Controlli di GitHub** (Gianluca, 16 novembre 2026): sulle PR partono da soli solo quelli della versione in corso e del Registro (`integrazione-62-qa`, `registro-browser-qa`). I collaudi delle versioni passate restano nei file e si lanciano a mano (Actions › Run workflow) quando serve. Una versione nuova aggiunge il suo controllo e rende «solo a mano» quello vecchio.
- **Prove automatiche del registro** (`prove/`): lancia quelle di quello che hai toccato. Non lanciare `voci-src/prova_*.py`, che usano servizi a pagamento.
- **Database:** le prove SQL solo su PostgreSQL locale (`prove/v62/postgres_*.py`), mai su Supabase.
- **Di' sempre cosa hai provato davvero e cosa no**: per esempio «Safari su iPhone non disponibile qui» oppure «solo Chromium». Cambiare user-agent non vale come prova di un altro browser.

## 3. Rilasciare (deploy)
1. **Prima la prova nel Lab** (`https://giandjcosta.github.io/o-girrr-registro/lab/`), poi la certificazione e il **«Vai» esplicito di Gianluca**. Senza «Vai» non va online niente.
2. **Proponi tu il tipo di versione** (Gianluca, 28 novembre 2026: «da ora in poi qualsiasi agente propone se è una versione piccola, grande o media»): correzione minore, aggiornamento medio o aggiornamento grande, con il motivo in una riga. Gianluca conferma o cambia. Poi scrivi messaggio e changelog seguendo `REGOLE-VERSIONI.md` e aggiungili con `rilascio/versioni/aggiungi.py`.
3. **Ordine fisso:** prima `gh-pages` del sito, poi la controlli sul sito vero (pagina aperta, console pulita), solo dopo `main` del sito e del registro. `git pull --rebase` prima di ogni push: i workflow scrivono ogni pochi minuti.
4. **Annota gli hash** dei commit e come tornare indietro (`git revert <hash>` sul ramo giusto) in `STATO.md` e nella cartella del rilascio (`rilascio/rXYZ/RILASCIO.md`).
5. **SQL:** solo con il «Vai». Gianluca lo applica dall'SQL Editor di Supabase (la conferma dello strumento di Claude spesso non gli arriva). Prepara sempre anche le funzioni di prima, per tornare indietro.
6. **Unire una Pull Request** solo quando i controlli di GitHub sono finiti e verdi. Se un controllo era rosso già prima, spiegalo nella PR invece di ignorarlo.
7. Dopo il rilascio: allinea `ufficiale/src/sito/` con `gh-pages` e aggiorna `STATO.md` e `LAVORI-IN-CORSO.md`.

## 4. Cercare un guasto (troubleshooting)
1. **Riproducilo** nel browser, con la stessa grafica (Lega o Stadio), lo stesso schermo e lo stesso modo di toccare di Gianluca.
2. **Pubblicato o in prova?** Confronta il sito vero, il Lab e la copia locale. Spesso il guasto è solo in una delle tre.
3. **Guarda la storia:** `git log -S"testo" -- file` dice chi ha introdotto una riga e perché.
4. **Un controllo di GitHub rosso:** leggi il log (`get_job_logs`) e verifica se era rosso anche su `main` prima della tua modifica. «Instabile» non è una causa.
5. **Cache:** se il sito vero «non cambia», di solito manca il `?v=` nuovo oppure il service worker (`offline.js`) tiene la copia di prima.
6. **Workflow che scrivono da soli** (Curva, voti, calcoli, Ramificazioni, Allineamento del Registro): non modificare a mano i file che generano. Correggi lo script che li genera e rilancia il workflow.
7. **Se un controllo di sicurezza ti blocca, fermati e spiegalo.** Non aggirarlo.

## 5. Scrivere per Gianluca
- In italiano, semplice. Cosa è cambiato, cosa hai provato, cosa no, cosa serve da lui (un «Vai», una scelta).
- Le domande vanno fatte una volta sola e chiare, con le opzioni e la tua raccomandazione.

## 6. Passaggio di consegne
- `LAVORI-IN-CORSO.md` è il quaderno comune: ogni voce dice **cosa**, **chi**, **stato**, **dove** (rami, file, PR) e **prossimo passo**.
- Aggiornalo **quando cominci** e **quando ti fermi**, anche se ti fermi a metà: soprattutto se ti fermi a metà.
- Quando una voce è finita e pubblicata, spostala in «Fatto di recente». Dopo una settimana la cronologia vive in `STATO.md` e `STATO-storico.md`.

<!-- Parte 2 approvata da Gianluca il 28 novembre 2026 («mi va bene tutto»): sezioni 7-12. -->
## 7. Cosa va in quale repository
| Repository | Cosa contiene | Cosa **non** contiene |
|---|---|---|
| `o-fant-a-girrr` (sito) | `gh-pages`: solo quello che è online (pagine, dati, immagini usate). `main`: workflow e script che girano da soli (`calcoli/`, `.github/workflows/`). | Prove, bozze, foto delle prove, Lab, copie di sicurezza, documenti di lavoro. |
| `o-girrr-registro` (laboratorio) | Lab e Anteprima, script di rilascio (`rilascio/rXY/`), sorgenti ufficiali delle pagine (`ufficiale/src/sito/`), prove (`prove/`), SQL (`sql/`), Radio (`voci-src/`), documenti (`STATO.md`, `LAVORI-IN-CORSO.md`, regole). | File pesanti che non servono più (video, PDF di prova): restano solo quelli citati da una pagina delle novità. |

- **Un file nuovo nel posto giusto la prima volta.** Uno script che girerà sul sito nasce nel registro (`calcoli/`) e va sul `main` del sito solo al rilascio.
- **Cartelle**: nomi in italiano, minuscoli, con trattini (`rilascio/r67/`, `prove/v66/`). Una cartella nuova ha un `LEGGIMI.md` di poche righe: a cosa serve, chi l'ha creata, quando si può cancellare.
- **File generati e file scritti a mano non si mescolano** nello stesso commit. L'elenco dei file generati (che non si toccano a mano) resta in `AGENTS.md` di ogni repository.
- **Repository nuovi** solo con il «Vai» di Gianluca e solo se il progetto è davvero un'altra cosa (come `armocromatic`), non per una funzione della lega.

## 8. Come si scrive il codice
- **JavaScript delle pagine**: un file per novità (`girrr/home-cruscotto.js`), dentro una funzione `(function(){ 'use strict'; … })()`, senza passaggi di compilazione. Classi CSS con un prefisso della novità (`c67-…`) per non toccare quelle degli altri. Funziona anche se il database o un file non risponde: in quel caso il riquadro non compare, la pagina resta intera.
- **Librerie esterne** (Gianluca, 28 novembre 2026: «se si possono usare librerie esterne lo farei, se ci aiutano solamente e se non rompono e si possono integrare»). Sì, a queste condizioni:
  1. **servono davvero**: fanno meglio o più in fretta una cosa che a mano sarebbe lunga o fragile (grafici, PDF, date, animazioni complesse), non per due righe di codice;
  2. **non rompono**: versione fissata (mai «ultima»), libreria mantenuta e diffusa, licenza libera (MIT, BSD, Apache, ISC) annotata nella PR;
  3. **si integrano**: la copia della libreria sta nel sito (`assets/lib/nome-versione/`, con il file della licenza), non presa ogni volta da un sito esterno, così funziona anche offline e se quel sito si ferma; si carica solo nelle pagine che la usano;
  4. **leggere**: niente pacchetti enormi per una funzione sola; se serve un passaggio di compilazione (npm, bundler) si chiede prima a Gianluca;
  5. **se non si carica**, la pagina resta usabile (il riquadro non compare, oppure c'è una versione semplice).
  Ogni libreria nuova si scrive in `LIBRERIE.md` del registro: nome, versione, licenza, dove si usa, perché. Per gli script Python dei workflow vale lo stesso, con la versione fissata in `requirements.txt`.
- **Python**: Python 3; librerie esterne alle condizioni qui sopra. In testa un commento con cosa fa, la decisione di Gianluca con la data e la riga «Uso: …». Argomenti con `argparse`.
- **SQL**: tutto passa da funzioni che controllano il codice della squadra; tabelle senza accesso diretto; in testa al file il ritorno indietro.
- **Nomi e testi** in italiano, come il resto del progetto. Commenti con data e motivo (già in `REGOLE-LAVORO.md`).
- **Misura**: un file sopra le 600 righe scritte a mano, o una funzione sopra le 80, va divisa alla prima occasione (non serve rifare quelli vecchi, ma non si allungano).
- **Niente codice morto**: quello che non si usa più si toglie nel rilascio dopo, non si lascia commentato.

## 9. Revisione del codice (review)
- Decisione di Gianluca (28 novembre 2026): **revisione obbligatoria** di ogni PR del sito da parte di un altro assistente, tranne le micro correzioni di testo.
- **Ogni modifica destinata al sito passa da una Pull Request**, anche quella di Claude. Fanno eccezione le micro correzioni di testo (regola già esistente) e i file scritti dai workflow.
- **La PR la rivede qualcuno che non l'ha scritta**: un altro assistente (per esempio ChatGPT rivede Claude e viceversa) oppure Gianluca. Chi rivede scrive un commento con l'esito: «Approvata», oppure l'elenco di cosa cambiare.
- **Cosa si guarda**, sempre nello stesso ordine:
  1. fa quello che ha chiesto Gianluca, e niente di più;
  2. regole dei contenuti (`AGENTS.md`: tre livelli di scrittura, maiuscole, Derby, niente scommesse);
  3. Lega e Stadio tutte e due, ognuna con la sua grafica;
  4. `?v=` aggiornati, script di rilascio rieseguibile, ritorno indietro scritto;
  5. prove lanciate e risultati nella PR (con foto per le modifiche che si vedono);
  6. niente segreti, niente file generati toccati a mano.
- **Chi rivede non riscrive**: segnala. Le correzioni le fa chi ha aperto la PR.

## 10. Commit
- **Un commit, un argomento.** Messaggio in italiano: `Autore: cosa cambia` (regola già esistente), al presente, che si capisca senza aprire i file.
- **Mai «prova», «wip», «fix» da soli** nei messaggi.
- **Push diretto su `main`** solo per: file scritti dai workflow, `STATO.md` e `LAVORI-IN-CORSO.md` e correzioni di testo nei documenti. Tutto il resto passa da un ramo e da una PR.

## 11. Rami, Pull Request e merge
- **Ramo**: `autore/argomento-breve` (regola già esistente), uno per argomento. Un ramo vive al massimo **14 giorni**: dopo si unisce o si chiude, scrivendolo in `LAVORI-IN-CORSO.md`.
- **PR piccola**: al massimo circa **400 righe scritte a mano** (non contano i file generati, la copia del Lab e le foto). Se è più grande, si divide.
- **Modello di PR** (in `.github/pull_request_template.md` dei due repository): Cosa cambia · Perché (decisione di Gianluca e data) · Come l'ho provato · Cosa non ho potuto provare · Come tornare indietro · Serve un «Vai»? (sito, database).
- **PR in bozza** finché non è provata nel Lab; «pronta» solo con le prove fatte.
- **Come si unisce**:
  - PR normali: **«Squash and merge»**, cioè un commit solo su `main` per ogni novità, con il titolo della PR;
  - PR di rilascio sul sito: **«Create a merge commit»**, così si torna indietro con un solo `git revert -m 1 <hash>`;
  - mai con controlli di GitHub rossi o in corso; i conflitti li risolve chi ha aperto la PR.
- **Dopo il merge** il ramo si cancella: su GitHub «Automatically delete head branches» nei due repository (lo attiva Gianluca dalle impostazioni). I rami degli altri non si cancellano mai a mano.

## 12. Prove: come si fanno, quando si aggiornano, quando si tolgono
- **Ogni novità ha la sua prova** in `prove/vXY/` (per esempio `prove/v66/`): stampa una riga `ok · …` per ogni controllo, si ferma alla prima che fallisce ed esce con un errore. Una prova che non può fallire non è una prova.
- **Elenco delle prove**: `prove/ELENCO.md`, una riga per prova (file · cosa controlla · quando lanciarla · ultima volta che è passata). Chi aggiunge una prova aggiunge la riga.
- **Quando si aggiornano**: nello stesso commit in cui cambia il comportamento che controllano. Se una prova fallisce, si corregge il codice oppure, se è cambiata la regola, la prova; mai disattivarla o cambiare il controllo perché passi.
- **Pulizia a ogni versione media** (6.7, 6.8…):
  - le prove della versione appena pubblicata diventano «di regressione» (si lanciano prima di ogni rilascio che tocca quelle pagine);
  - le prove di una funzione che non esiste più si spostano in `prove/archivio/` con una riga nell'elenco;
  - dall'archivio si cancellano, con il «Vai» di Gianluca, dopo una versione grande (7.0).
- **Workflow di collaudo**: sulle PR partono solo quelli della versione in corso e del Registro (regola già esistente). Quelli delle versioni passate (5.2, 5.3, 6.0…) passano a «solo a mano» alla versione dopo e si archiviano alla versione grande successiva.
- **Foto delle prove**: non nei repository, salvo quelle usate nelle pagine delle novità. Quelle per Gianluca si mandano in chat o restano negli artefatti dei workflow.
