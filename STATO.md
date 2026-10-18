# Stato del progetto O Girrr (aggiornato 18 ottobre 2026)

Per aprire una chat nuova: incolla "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì".

## Dove vive tutto
- Sito vero: repo `giandjcosta/o-fant-a-girrr`, ramo `gh-pages` (pagine) e `main` (workflow e calcoli). Sito: https://giandjcosta.github.io/o-fant-a-girrr/
- Laboratorio e registro: repo `giandjcosta/o-girrr-registro`, ramo `main`.
- Database: Supabase, progetto `qmjqfgmvimsuxvghetgi`.
- Build: `export SORGENTE_GIRRR=/tmp/orig/girrr` (worktree del commit 1e2506f), poi `python3 aggiorna.py`, `python3 rilascio/pacchetto.py`, `python3 rilascio/applica.py --gh-pages /home/claude/o-fant-a-girrr --main /tmp/wm [--vai]`, push `origin HEAD:gh-pages`.

## Regole di pubblicazione
- Micro correzioni di testo: online in automatico, avviso dopo. Tutto il resto: serve il "vai" di Gianluca.
- Niente disclaimer "notizia inventata" o "dati finti". Storie come un campionato vero (giocatori, gol, squadre, allenatori), niente riferimenti a fantacalcio, crediti, fantapunti o fantamedia, salvo punteggi. "Derby" sempre con la D maiuscola. Titoli ed etichette con la maiuscola iniziale. Post ufficiali mai sulle scommesse.

## Fatto e online (18 ottobre)
5.0 completa; Carriera con tre fasce e sette sponsor; Albo di Latta e Derby nell'Albo; storie di tutti gli allenatori dal 2016/17; logo della Lega in Curva porta alla Home della Lega (la casa alla Curva); tab deselezionata torna neutra subito; Curva con workflow "post quasi subito" ogni mezz'ora; quote Derby di Totogirrr accese (+15% per esito, +10% sulla schedina con un Derby, cashback 20%).

## Database (Supabase) già applicato
- Quote Derby (`sql/derby-quote-6.sql`) e interruttore acceso.
- `3-frase-sfida.sql`: colonna `frase_testo` e `derby_sfida_lancia` con `p_testo`. Da fare: `4-pulizia.sql` (drop della vecchia versione a 6 argomenti, altrimenti due funzioni con lo stesso nome).

## Da fare, in ordine
1. Applicare `4-pulizia.sql`.
2. App (rilascio/live.js, chiamata `derby_sfida_lancia`): mandare `p_testo` con la frase vera; poi `calcoli/leggi_eventi.py` legge `frase_testo` e `post_curva.py` la usa per l'Intervista speciale di tutte le coppie (ora solo Oranje VC–Apo). Serve il "vai".
3. Post "Conferenza pre partita giornata X" su Girrr con il riassunto delle risposte (le risposte sono già salvate con il testo in `conf_risposta.risposte`); verificare che `conf_promesse` le restituisca, altrimenti nuova funzione.
4. Derby "The Continental" (Oranje VC–Apo): Apo deve ancora confermare il nome nell'app (`nome_ok` falso).
5. Lanciare da Actions "Calcoli dopo la giornata" la prima volta e controllare il log.
6. Aperti: decidere se aggiungere il post della sfida anche sul profilo della squadra (per ora solo Girrr Sport), unificare le statistiche di Riccardo e Nobile, verificare su iPhone/Firefox/PWA.

## Note
- Il workflow Curva salva lo stato in `calcoli/pubblicati.json` su `main`; l'opzione `solo_segna` segna i post attuali come già usciti senza inviarli.
- Le storie degli allenatori stanno in `ufficiale/src/storie.json`.
