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

## Regole sui contenuti — TRE LIVELLI UFFICIALI (decisione di Gianluca, 31 ottobre 2026)

**Principio vincolante per ogni AI, nuova pagina, testo, bot e statistica: O Girrr è raccontato come un campionato vero, ma usa i dati ufficiali di Leghe Fantacalcio. Realismo nel racconto, precisione nei dati. Non cancellare il lessico Fantacalcio dove indica una metrica reale.**

1. **SPORTIVO — identità del campionato.** Home personale, Tabellone dei risultati, classifica, titoli, rivalità e presentazioni delle partite: usare squadre, allenatori, gol, vittorie, sconfitte, pareggi, punti in classifica, giornata, Campionato, Champions Cup, Derby. Esempio illustrativo: «Squadra A batte Squadra B 3–1 e sale al secondo posto». Non scambiare i **gol** con i **Fantapunti**.
2. **TECNICO/UFFICIALE — fonte e calcolo, senza ambiguità.** Tabellone di dettaglio, Regole, Statistiche, schede e Annuario: mostrare esplicitamente i **Fantapunti** dei due team, i voti/bonus/malus, eventuale modificatore difensivo, soglie per la conversione in gol, i **punti in classifica** e, quando pertinente, fantacrediti e costo delle rose. «Leghe Fantacalcio» resta il nome corretto del servizio sorgente. Esempio esclusivamente dimostrativo: «Fantapunti 77,5–68; risultato 3–1; 3 punti in classifica alla squadra vincente». La conversione segue sempre il regolamento effettivamente vigente; non inventare criteri.
3. **EDITORIALE/NARRATIVO — cronaca e vita della Lega.** Giornale, Radio, Curva e bot raccontano come media sportivi: «Tre reti, tre punti e una serata da ricordare», usando solo risultati o fatti verificabili. Possono nominare i Fantapunti quando commentano un voto, uno scarto, una decisione o una controversia tecnica. Personaggi e tifosi possono essere ironici, polemici o provocatori, ma sono opinioni narrative, **non dichiarazioni attribuite come fatti reali agli allenatori**.

**Regole trasversali:**
- **Non confondere:** gol del risultato ≠ Fantapunti ≠ punti della classifica ≠ fantacrediti; le statistiche e l'Annuario dichiarano chiaramente unità, competizione e giornata. I pareggi restano pareggi.
- Le etichette *Fantapunti*, *Fantamedia*, *Modificatore*, *Bonus/Malus* restano dove tecnicamente corrette: non fare sostituzioni indiscriminate con «Punteggio» o «Punti».
- Conservare tutte le informazioni, tab e sottomenu esistenti. Una nuova Home o un Annuario espandibile sono **aggiunte**, non scorciatoie che nascondono dati.
- Dove mancano dati storici scrivere «Dato non conservato», non ricostruire statistiche non disponibili.
- Nelle cronache non aggiungere disclaimer superflui che rovinino l'immersione; **nelle anteprime e nei contenuti non verificati** indicare chiaramente lo stato di prova senza far passare esempi come fatti.
- **Derby** sempre con D maiuscola, regole Derby aggiornate dall'utente senza ripristinare soglie precedenti. Titoli ed etichette con maiuscola iniziale.
- I post ufficiali (Girrr Sport, Lega, Giornale) non parlano mai di scommesse. La Curva automatica mantiene le personalità e le regole già presenti in `curva-banca.js` e `calcoli/post_curva.py`.


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
