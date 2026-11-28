# Proposta · Regole comuni, parte 2 (Claude, 28 novembre 2026)

**Stato: proposta, da approvare da Gianluca.** Finché non è approvata valgono solo `AGENTS.md` e `REGOLE-LAVORO.md`. Quando è approvata, le sezioni sotto entrano in `REGOLE-LAVORO.md` (dalla 7 alla 12) e questo file si cancella.

Perché (Gianluca, 28 novembre): «Non ci sono basi su come scrivere e revisionare il codice, come fare i test e ogni quanto aggiornare o eliminare quelli superflui, come dividere i repository, come fare commit, merge e PR. Finché era piccolo andava bene, ma ora sta diventando più serio.»

Cosa c'è già (`REGOLE-LAVORO.md`, 16 novembre): una fonte sola per le correzioni, script di rilascio rieseguibili, Lega e Stadio insieme, `?v=` nei file, prove nel browser e sugli schermi, ordine del rilascio, ricerca dei guasti, passaggio di consegne. Le parti sotto **si aggiungono**, non cambiano quelle.

Com'è oggi, misurato il 28 novembre: 117 file in `prove/` senza un elenco di cosa controllano; 28 workflow nel registro, una decina sono collaudi di versioni passate (5.2, 5.3, 6.0, 6.1); nessun modello di Pull Request; rami e commit con regole sui nomi ma non sulla dimensione e sul modo di unire.

---

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
- **JavaScript delle pagine**: un file per novità (`girrr/home-cruscotto.js`), dentro una funzione `(function(){ 'use strict'; … })()`, senza librerie esterne né passaggi di compilazione. Classi CSS con un prefisso della novità (`c67-…`) per non toccare quelle degli altri. Funziona anche se il database o un file non risponde: in quel caso il riquadro non compare, la pagina resta intera.
- **Python**: Python 3 con la sola libreria standard dove si può. In testa un commento con cosa fa, la decisione di Gianluca con la data e la riga «Uso: …». Argomenti con `argparse`.
- **SQL**: tutto passa da funzioni che controllano il codice della squadra; tabelle senza accesso diretto; in testa al file il ritorno indietro.
- **Nomi e testi** in italiano, come il resto del progetto. Commenti con data e motivo (già in `REGOLE-LAVORO.md`).
- **Misura**: un file sopra le 600 righe scritte a mano, o una funzione sopra le 80, va divisa alla prima occasione (non serve rifare quelli vecchi, ma non si allungano).
- **Niente codice morto**: quello che non si usa più si toglie nel rilascio dopo, non si lascia commentato.

## 9. Revisione del codice (review)
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
- **Dopo il merge** il ramo si cancella. Proposta: attivare su GitHub «Automatically delete head branches» nei due repository (lo attiva Gianluca dalle impostazioni). I rami degli altri non si cancellano mai a mano.

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

---

## Le scelte che servono da Gianluca
1. **Revisione obbligatoria da un altro assistente per ogni PR del sito?** Proposta: sì, tranne le micro correzioni di testo.
2. **Merge**: «Squash and merge» per le PR normali e «merge commit» per i rilasci?
3. **Limiti**: 14 giorni per un ramo, circa 400 righe per una PR, 600 righe per un file?
4. **Cancellazione automatica dei rami uniti** su GitHub: la attivi tu?
5. **Pulizia delle prove**: archivio a ogni versione media, cancellazione alla versione grande con il tuo «Vai»?

Dopo il sì: queste sezioni entrano in `REGOLE-LAVORO.md`, aggiungo il modello di PR nei due repository, preparo `prove/ELENCO.md` con le 117 prove di oggi (quali sono vive, quali da archiviare) e lo segnalo in `AGENTS.md` dei due repository, così vale per tutti gli assistenti.
