# Come si lavora su O Girrr Registro (laboratorio della lega)

Qui ci sono il Lab, l'Anteprima, le sorgenti delle pagine del sito vero e lo stato del progetto. Il sito vero è nel repository `giandjcosta/o-fant-a-girrr`.

## Prima di tutto
- Leggi `STATO.md`: dice cosa è online, cosa è in prova, i comandi di build e rilascio e cosa resta da fare. Alla fine di ogni lavoro aggiornalo. La cronologia raggruppata è in `STATO-storico.md`; la pagina Registro mostra i commit.

## Come è fatto
- `lab/index.html`: il Lab, dove si provano le novità. Dopo ogni modifica al Lab rigenera l'Anteprima con `python3 anteprima/build.py` (scrive `anteprima/index.html` per lo Stadio e `anteprima/attuale.html` per la Lega).
- `ufficiale/src/sito/`: sorgenti delle pagine del sito vero (Lega in `girrr/`, Stadio in `stadio/girrr/`). Devono restare uguali a quello che c'è su `gh-pages` del sito.
- `calcoli/`: script dei calcoli (Moviola, Curva, Borsino e altri), copiati sul `main` del sito al rilascio. `rilascio/`: script e patch per il rilascio.
- `prove/`: prove automatiche. Prima di consegnare lancia quelle che riguardano quello che hai toccato, per esempio `python3 prove/prova_moviola.py` e `python3 prove/prova_moviola_gol.py`.
- Non lanciare `voci-src/prova_*.py`: non sono prove, generano voci con servizi a pagamento.

## Regole di questo repository
- Le novità si fanno su un ramo e si uniscono a `main` insieme al rilascio sul sito, con il "vai" di Gianluca.
- Ogni modifica destinata al sito, comprese le correzioni di testo, deve prima essere mostrata e provata nella preview navigabile del Laboratorio: `https://giandjcosta.github.io/o-girrr-registro/lab/`. Un branch Git o un file isolato non sostituiscono la preview.
- Il sito vero resta invariato finché Gianluca non certifica la prova nel Lab e dà il suo «Vai» esplicito. Le modifiche documentali o agli strumenti interni che non cambiano il comportamento del sito non richiedono un prototipo nel Lab.
- Se il `main` del sito ha file più nuovi del registro (workflow, script della Curva), copiali prima qui: non sovrascriverli con versioni vecchie.

## Regole grafiche — Lega e Stadio (decisione di Gianluca, 1° novembre 2026)
Le due grafiche devono essere davvero diverse, e ognuna uguale su tutte le pagine, menu, sottomenu, schede e riquadri:
- **Lega** (grafica «normale», più statica): riquadri dritti come le partite del Tabellone, banda laterale dritta (8 px, rossa) e angoli appena arrotondati (4 px a sinistra, 14 px a destra); schede e pillole squadrate.
- **Stadio** (grafica col corsivo Lobster): riquadri arrotondati (12 px) con la banda laterale curva, come le righe della classifica Stadio; schede e pillole tonde.
- Colori ufficiali in tutte e due: il rosso della Lega (#d62839) è l'accento (interruttori, bande delle partite, scheda attiva del Tabellone); l'oro (#ffd166) solo dove è oro anche sul sito vero (giornata selezionata, schede dell'Albo nello Stadio, primo posto). Prima di cambiare un colore, confrontalo con la pagina vera.

## Regole sui contenuti — tre livelli di scrittura (decisione di Gianluca, 1° novembre 2026)
O Girrr si racconta come un campionato vero, ma i dati sono quelli ufficiali di Leghe Fantacalcio. Realismo nel racconto, precisione nei dati.
1. **Sportivo** (Home, risultati, classifica, titoli, rivalità, presentazioni delle partite): squadre, allenatori, gol, vittorie, pareggi, sconfitte, punti in classifica, giornata, Campionato, Champions Cup, Derby.
2. **Tecnico** (Tabellone di dettaglio, Regole, Statistiche, Campo, schede, Annuario, Totogirrr): Fantapunti, voti, bonus e malus, modificatore della difesa e fantacrediti dove sono il dato vero, sempre con l'unità chiara.
3. **Editoriale** (Giornale, Radio, Curva, personaggi): raccontano come i media sportivi, con risultati e fatti veri. **Radio e Giornale non parlano di Fantapunti**, tranne: le vittorie decise da pochissimi fantapunti; il Cucchiaio di legno (il punteggio più basso della giornata); le statistiche del Giornale (miglior punteggio, record e simili).
- Non confondere gol del risultato, Fantapunti, punti in classifica e fantacrediti. I pareggi restano pareggi.
- Dove mancano dati storici scrivere «Dato non conservato»: niente statistiche ricostruite per ipotesi.
- Niente disclaimer tipo "notizia inventata" o "dati finti".
- Le frasi iniziano con la maiuscola, anche dopo un punto. Nelle legende usare etichette con iniziale maiuscola e separare chiaramente i significati.
- "Derby" sempre con la D maiuscola. Titoli ed etichette con la maiuscola iniziale.
- I post ufficiali (Girrr Sport, Lega, Giornale) non parlano mai di scommesse.

## Regole comuni a tutti i repository di Gianluca

Valgono per chiunque modifichi questi repository: Gianluca, Claude Code (cloud o desktop), l'agente di VS Code, Perplexity, Aider, **Grok** o altri.

Repository: `o-fant-a-girrr` (sito della lega), `o-girrr-registro` (laboratorio e registro della lega), `armocromatic` (sito di armocromia), `giandjcosta` (profilo GitHub).

### Prima di cominciare
1. Leggi questo file fino in fondo: sotto ci sono le regole del singolo progetto.
2. Aggiorna la copia locale (`git pull`). I repository cambiano di continuo: lavorano più assistenti, e sul sito della lega scrivono anche i workflow ogni pochi minuti.
3. Guarda le Pull Request e i rami aperti: se qualcuno sta già lavorando sulla stessa parte, non sovrapporti.

### Mentre lavori
- Una modifica per argomento, piccola. Non toccare file che non c'entrano con quello che ti è stato chiesto.
- Lavora su un ramo con il tuo nome davanti: `claude/…`, `vscode/…`, `perplexity/…`, `aider/…`, `grok/…`, `gianluca/…`. Commit con messaggi in italiano che dicono cosa cambia.
- **Identificazione obbligatoria dell'autore (vale per TUTTI gli assistenti e collaboratori):** ogni nuovo ramo deve iniziare con il prefisso dell'agente che lo crea e ogni messaggio di commit e titolo di Pull Request deve iniziare con il nome dello stesso autore seguito da due punti. Esempi: `chatgpt/nome-attivita` → `ChatGPT: descrizione`; `grok/nome-attivita` → `Grok: descrizione`; `claude/nome-attivita` → `Claude: descrizione`; `vscode/nome-attivita` → `VSCode: descrizione`; `perplexity/nome-attivita` → `Perplexity: descrizione`; `aider/nome-attivita` → `Aider: descrizione`; `gianluca/nome-attivita` → `Gianluca: descrizione`. Il prefisso identifica chi ha realmente effettuato la modifica: non usare il nome di un altro assistente. Anche i commit successivi sullo stesso ramo mantengono il prefisso del loro effettivo autore. Non rinominare rami o riscrivere commit già esistenti per adeguarli retroattivamente.
- Mai `git push --force`, mai riscrivere la storia di un ramo già su GitHub, mai cancellare rami di altri.
- Mai scrivere nel codice chiavi, token o password. Le chiavi "publishable" di Supabase già presenti nelle pagine sono pubbliche per scelta; ogni altra chiave no.
- Cambi di pagina, schede e aperture di tendine e menu devono essere fluidi (dissolvenze e scorrimenti morbidi, niente di scattante), rispettando «riduci movimento».
- Prima di consegnare, prova davvero: le pagine devono funzionare a 320 px di larghezza (iPhone SE) senza scorrere di lato, e la console del browser non deve avere errori nuovi.

### Cosa serve il "vai" di Gianluca
- Qualsiasi modifica al sito vero, anche una correzione di testo: prima preview nel Lab, poi certificazione e «Vai» esplicito di Gianluca.
- Qualsiasi modifica al database Supabase (progetto `qmjqfgmvimsuxvghetgi`): niente SQL, niente migrazioni, niente dati cambiati senza il suo "vai" esplicito.
- Cancellare file, rami, Pull Request o dati.
- Se un controllo di sicurezza blocca un'operazione, fermati e spiega cosa è successo: non aggirarlo.

### Quando hai finito
- Di' cosa hai cambiato, cosa hai provato e cosa non hai potuto provare (per esempio Safari).
- Per la lega: aggiorna `STATO.md` nel repository `o-girrr-registro`.
- Rispondi in italiano.
