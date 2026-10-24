# Come si lavora su O Girrr Registro (laboratorio della lega)

Qui ci sono il Lab, l'Anteprima, le sorgenti delle pagine del sito vero e lo stato del progetto. Il sito vero è nel repository `giandjcosta/o-fant-a-girrr`.

## Prima di tutto
- Leggi `STATO.md`: dice cosa è online, cosa è in prova, i comandi di build e rilascio e cosa resta da fare. Alla fine di ogni lavoro aggiornalo.

## Come è fatto
- `lab/index.html`: il Lab, dove si provano le novità. Dopo ogni modifica al Lab rigenera l'Anteprima con `python3 anteprima/build.py` (scrive `anteprima/index.html` per lo Stadio e `anteprima/attuale.html` per la Lega).
- `ufficiale/src/sito/`: sorgenti delle pagine del sito vero (Lega in `girrr/`, Stadio in `stadio/girrr/`). Devono restare uguali a quello che c'è su `gh-pages` del sito.
- `calcoli/`: script dei calcoli (Moviola, Curva, Borsino e altri), copiati sul `main` del sito al rilascio. `rilascio/`: script e patch per il rilascio.
- `prove/`: prove automatiche. Prima di consegnare lancia quelle che riguardano quello che hai toccato, per esempio `python3 prove/prova_moviola.py` e `python3 prove/prova_moviola_gol.py`.
- Non lanciare `voci-src/prova_*.py`: non sono prove, generano voci con servizi a pagamento.

## Regole di questo repository
- Le novità si fanno su un ramo e si uniscono a `main` insieme al rilascio sul sito, con il "vai" di Gianluca.
- Se il `main` del sito ha file più nuovi del registro (workflow, script della Curva), copiali prima qui: non sovrascriverli con versioni vecchie.

## Regole sui contenuti
- Storie come un campionato vero (giocatori, gol, squadre, allenatori). Niente riferimenti a fantacalcio, crediti, fantapunti o fantamedia, salvo i punteggi.
- Niente disclaimer tipo "notizia inventata" o "dati finti".
- "Derby" sempre con la D maiuscola. Titoli ed etichette con la maiuscola iniziale.
- I post ufficiali (Girrr Sport, Lega, Giornale) non parlano mai di scommesse.

## Regole comuni a tutti i repository di Gianluca

Valgono per chiunque modifichi questi repository: Gianluca, Claude Code (cloud o desktop), l'agente di VS Code, Perplexity, Aider o altri.

Repository: `o-fant-a-girrr` (sito della lega), `o-girrr-registro` (laboratorio e registro della lega), `armocromatic` (sito di armocromia), `giandjcosta` (profilo GitHub).

### Prima di cominciare
1. Leggi questo file fino in fondo: sotto ci sono le regole del singolo progetto.
2. Aggiorna la copia locale (`git pull`). I repository cambiano di continuo: lavorano più assistenti, e sul sito della lega scrivono anche i workflow ogni pochi minuti.
3. Guarda le Pull Request e i rami aperti: se qualcuno sta già lavorando sulla stessa parte, non sovrapporti.

### Mentre lavori
- Una modifica per argomento, piccola. Non toccare file che non c'entrano con quello che ti è stato chiesto.
- Lavora su un ramo con il tuo nome davanti: `claude/…`, `vscode/…`, `perplexity/…`, `aider/…`, `gianluca/…`. Commit con messaggi in italiano che dicono cosa cambia.
- Mai `git push --force`, mai riscrivere la storia di un ramo già su GitHub, mai cancellare rami di altri.
- Mai scrivere nel codice chiavi, token o password. Le chiavi "publishable" di Supabase già presenti nelle pagine sono pubbliche per scelta; ogni altra chiave no.
- Prima di consegnare, prova davvero: le pagine devono funzionare a 320 px di larghezza (iPhone SE) senza scorrere di lato, e la console del browser non deve avere errori nuovi.

### Cosa serve il "vai" di Gianluca
- Qualsiasi cosa che va online (merge sul ramo pubblicato, push sul sito vero). Unica eccezione: micro correzioni di testo nel sito della lega, che vanno online con un avviso dopo.
- Qualsiasi modifica al database Supabase (progetto `qmjqfgmvimsuxvghetgi`): niente SQL, niente migrazioni, niente dati cambiati senza il suo "vai" esplicito.
- Cancellare file, rami, Pull Request o dati.
- Se un controllo di sicurezza blocca un'operazione, fermati e spiega cosa è successo: non aggirarlo.

### Quando hai finito
- Di' cosa hai cambiato, cosa hai provato e cosa non hai potuto provare (per esempio Safari).
- Per la lega: aggiorna `STATO.md` nel repository `o-girrr-registro`.
- Rispondi in italiano.
