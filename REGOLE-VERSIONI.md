# Regole fisse per messaggi e changelog delle versioni

Valgono per tutti (Gianluca, Claude, ChatGPT, Grok e altri) a ogni rilascio sul sito. Decisione di Gianluca del 15 novembre 2026: una regola sola, così ogni versione si scrive allo stesso modo. Si basano su `AGENTS.md` (tre livelli di scrittura) e sulle versioni già pubblicate.

## 1. Numero e tipo

- Prima del rilascio si chiede a Gianluca il tipo: **minore** (6.2.1), **medio** (6.3), **grande** (7.0). Il numero lo calcola `rilascio/versioni/aggiungi.py`, con `--v` solo se Gianluca ha già scelto il numero.
- Una versione per rilascio vero. Lab, Registro, Ramificazioni, Anteprima e prove non sono versioni dell’app e non vanno in `versioni.json`.
- Se la versione unisce lavori di più assistenti (per esempio Claude e ChatGPT), si scrive **un solo** messaggio e **un solo** changelog: le aree si uniscono, senza dire chi ha fatto cosa.

## 2. Titolo

- Da 3 a 8 parole, dice la novità più importante con parole da tifoso: «Il Campo della Champions Cup», «La stagione da raccontare».
- Maiuscola iniziale, niente punto finale, niente numero di versione.

## 3. Messaggio per il gruppo (livello editoriale)

- Comincia sempre così: emoji + `**O Girrr X.Y è online!**`. Emoji: ⚽ per medie e grandi, 🔧 per le minori; 🎬 o 🏆 solo se la novità principale è un video o un trofeo.
- Da 3 a 6 frasi brevi, al massimo due paragrafi. Prima la novità più importante, poi le altre in ordine di interesse.
- Si parla al lettore con il **tu** («scegli la tua squadra», «trovi la tua partita»).
- Si nominano le pagine come nell’app: Home, Tabellone, Campo, Curva, Carriera, Albo d’oro, Girrr Sport, Radio, Giornale, Totogirrr, Spogliatoio, Versioni. Campionato e Champions Cup per esteso; «Derby» sempre con la D maiuscola.
- **Mai**: Fantapunti, voti numerici, bonus e malus, scommesse, quote; parole tecniche (file, JSON, workflow, cache, database, script, commit, codice); nomi degli assistenti; disclaimer tipo «dati finti».
- Dopo «·» sempre la maiuscola. Le frasi iniziano con la maiuscola.
- Chiude con un saluto breve, una sola emoji: «Buona giornata a tutti! ⚽», «Buona settimana a tutti! ⚽».

## 4. Changelog (livello tecnico)

- Ogni voce si passa ad `aggiungi.py` come `--voce "Area: testo"`. Le voci con la stessa area finiscono nello stesso gruppo.
- **Aree ammesse**, cioè i nomi delle pagine: Home, Tabellone, Campo, Curva, Carriera, Albo d’oro, Girrr Sport, Radio, Giornale, Totogirrr, Spogliatoio, Condividi, Notifiche, Versioni, Ospite, App (per ciò che vale ovunque). Una pagina nuova usa il suo nome nell’app.
- Ordine delle aree: prima quella della novità principale, poi le altre in ordine di importanza.
- Ogni voce: **una frase**, maiuscola iniziale, **punto finale**, al massimo circa 30 parole. Dice cosa vede o può fare chi usa l’app, non come è fatto.
- Se una cosa cambia solo in una grafica si scrive «nella grafica Lega» o «nella grafica Stadio».
- Qui sono ammessi i termini tecnici del gioco con l’unità chiara (Fantapunti, voto, bonus, malus), come nel livello tecnico di `AGENTS.md`.
- **Mai**: nomi di file, funzioni, hash, numeri di PR, nomi degli assistenti, scommesse.

## 5. Dopo la scrittura

- Prova: `python3 rilascio/versioni/aggiungi.py --tipo … --titolo … --messaggio … --voce … --prova`.
- Poi la versione va in `rilascio/versioni/versioni.json` e in `versioni.json` alla radice di `gh-pages`; la pagina Versioni e l’avviso in Home si aggiornano da soli. Controllare la pagina Versioni nelle due grafiche.
- Annotare in `STATO.md` del registro versione, hash dei commit e come tornare indietro (`git revert`).

## Esempio (stile corretto)

Titolo: `Il Campo della Champions Cup`

Messaggio:
> ⚽ **O Girrr 6.2 è online!** Nel Campo ora trovi anche le partite della Champions Cup: un tocco sull’interruttore e passi da una competizione all’altra. Quando entri con il tuo codice si apre subito la tua partita. Con le nuove frecce passi da una partita all’altra o salti di giornata, tutto più fluido. Buona giornata a tutti! ⚽

Voci:
- `Campo: Interruttore Campionato / Champions Cup con passaggio morbido; ogni competizione ricorda la giornata e la partita che stavi guardando.`
- `Campo: Frecce ‹ › per cambiare partita e « » per cambiare giornata; le partite si possono anche scorrere e toccare.`
