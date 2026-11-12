# Come si lavora su O Girrr Registro (laboratorio della lega)

Qui ci sono il Lab, l'Anteprima, le sorgenti delle pagine del sito vero e lo stato del progetto. Il sito vero è nel repository `giandjcosta/o-fant-a-girrr`.

## Prima di tutto
- Leggi `STATO.md`: dice cosa è online, cosa è in prova, i comandi di build e rilascio e cosa resta da fare. Alla fine di ogni lavoro aggiornalo. La cronologia raggruppata è in `STATO-storico.md`; la pagina Registro mostra i commit.
- **Regola permanente di Gianluca (12 novembre 2026):** Changelog, Archivio e Anteprima devono seguire automaticamente l'ultima versione pubblicata. La fonte delle versioni è `versioni.json` su `gh-pages` del sito; `registro-stato.json` conserva versione e commit sincronizzati. `sincronizza.py --sito CHECKOUT_GH_PAGES`, `changelog.py` e `anteprima/build.py` vengono eseguiti dal workflow `sincronizza-registro.yml` dopo le modifiche al Lab e ogni 30 minuti per i rilasci esterni (con i possibili ritardi di GitHub). L'ingresso corrente è `ufficiale/`, in sola lettura; i prototipi restano nel Lab e le copie storiche non vanno rinominate come se fossero correnti. Non modificare a mano `anteprima/pubblicata/`, `archivio.html` o `registro-stato.json`.

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

## Ogni nuova versione (dalla 5.6 in poi, decisione di Gianluca, 1° novembre 2026)
- Oltre a `STATO.md`, al registro delle modifiche e alle prove nel Lab, ogni versione ha la sua **pagina delle novità** `lab/novita-X-Y.html`, fatta come `lab/novita-5-5.html`: una scheda per novità, con foto, «Dove» e i bottoni per aprirla in Lega e Stadio. Collegala dal Lab.
- Le novità sono **integrate anche nell'Anteprima** (`anteprima/`), così Gianluca vede come si muove tutto insieme, non solo la scheda singola.
- Transizioni sempre fluide (vedi «Mentre lavori»).

## Numeri di versione e pagina Versioni (decisione di Gianluca, 9 novembre 2026)
- **Prima di rilasciare qualcosa sul sito vero chiedi a Gianluca che tipo di aggiornamento è:**
  - correzione minore → cambia la terza cifra: 5.6.1, 5.6.2, …;
  - aggiornamento medio → cambia la seconda cifra: 5.7 (cioè 5.7.0), 5.8, …;
  - aggiornamento grande → cambia la prima cifra: 6.0, 7.0, ….
- La versione online corrente e il commit sincronizzato si leggono in `registro-stato.json`. Cronologia: **5.8** (11 novembre 2026, `gh-pages` `6897f71`, `main` `e4465da`: Claude in redazione, domande della conferenza su misura e giudizio delle risposte scritte a mano; la redazione lavora da sola con l'attività programmata «Redazione di Girrr Sport», vedi `redazione/ISTRUZIONI.md`). Prima: 5.7 (`ddf30fc`, `c05cf9f`, migrazioni `v57_push_menzioni` e `v57_conf_dopo`: Sala stampa, dopo partita, Promesse, Testa a testa, menzioni sul telefono, testo grande sulla TV, cuori della Curva sul telefono, Giro di boa in Condividi), 5.6.2 (`414a959`, nome «The Blues Brothers» mostrato ovunque con `nomi.js`, Condividi della Curva con l'immagine del post), 5.6.1 (`4694f35`, notifiche lette rimpicciolite, Versioni fluide, pillola della versione nella Home), 5.6 (`caa13c6`, notifiche sul telefono, Cerca, Condividi, La mia stagione, Versioni) e 5.5.1 (`e06cbe2`, copia offline e scorciatoie). Il prossimo numero lo calcola `aggiungi.py` dalla fonte delle versioni aggiornata.
- A ogni rilascio aggiungi la versione in cima a `versioni.json` con `python3 rilascio/versioni/aggiungi.py --tipo minore|medio|grande …` (il numero lo calcola da solo): un **messaggio** per il gruppo, nel tono dei messaggi di prima (livello editoriale, niente fantapunti né scommesse), e il **changelog** diviso per area (livello tecnico). Poi copia `versioni.json` nella radice di `gh-pages`: la pagina Versioni (`girrr/versioni.html`, `stadio/girrr/versioni.html`) e l'avviso in Home si aggiornano da soli.
- Dalla 1.0 alla 4.4 la divisione in versioni non è conservata («Dato non conservato»): se Gianluca ritrova i messaggi, vanno aggiunti a `versioni.json`.

## Regole grafiche — Lega e Stadio (decisione di Gianluca, 1° novembre 2026)
Le due grafiche devono essere davvero diverse, e ognuna uguale su tutte le pagine, menu, sottomenu, schede e riquadri:
- **Lega** (grafica «normale», più statica): riquadri grandi dritti come le partite del Tabellone, banda laterale dritta (8 px, rossa) e angoli appena arrotondati (4 px a sinistra, 14 px a destra). Pillole, schede e cerchi delle giornate restano tondi: la Lega non va resa tutta squadrata (Gianluca, 1° novembre).
- **Stadio** (grafica col corsivo Lobster): riquadri arrotondati (12 px) con la banda laterale curva, come le righe della classifica Stadio; schede e pillole tonde.
- Colori: nella **Lega** l'accento è il rosso (#d62839): interruttori, bande, scheda attiva. Nello **Stadio** più oro che rosso (Gianluca, 1° novembre): bande, scheda attiva, interruttore e pillole selezionate in oro (#ffd166). **Regola fissa in tutte e due le grafiche:** Campionato rosso e Champions Cup azzurra (interruttore Campionato/Champions Cup, scheda attiva del Tabellone, bande delle partite); rossi anche retrocessione ed eliminate. Prima di cambiare un colore, confrontalo con la pagina vera.

## Regole sui contenuti — tre livelli di scrittura (decisione di Gianluca, 1° novembre 2026)
O Girrr si racconta come un campionato vero, ma i dati sono quelli ufficiali di Leghe Fantacalcio. Realismo nel racconto, precisione nei dati.
1. **Sportivo** (Home, risultati, classifica, titoli, rivalità, presentazioni delle partite): squadre, allenatori, gol, vittorie, pareggi, sconfitte, punti in classifica, giornata, Campionato, Champions Cup, Derby.
2. **Tecnico** (Tabellone di dettaglio, Regole, Statistiche, Campo, schede, Annuario, Totogirrr): Fantapunti, voti, bonus e malus, modificatore della difesa e fantacrediti dove sono il dato vero, sempre con l'unità chiara.
3. **Editoriale** (Giornale, Radio, Curva, personaggi): raccontano come i media sportivi, con risultati e fatti veri. **Radio e Giornale non parlano di Fantapunti**, tranne: le vittorie decise da pochissimi fantapunti; il Cucchiaio di legno (il punteggio più basso della giornata); le statistiche del Giornale (miglior punteggio, record e simili).
- Non confondere gol del risultato, Fantapunti, punti in classifica e fantacrediti. I pareggi restano pareggi.
- Dove mancano dati storici scrivere «Dato non conservato»: niente statistiche ricostruite per ipotesi.
- Niente disclaimer tipo "notizia inventata" o "dati finti".
- Le frasi iniziano con la maiuscola, anche dopo un punto. Nelle legende usare etichette con iniziale maiuscola e separare chiaramente i significati.
- **Dopo il punto mediano «·» la parola comincia sempre con la maiuscola** (decisione di Gianluca, ribadita il 9 novembre 2026): «Offline · Copia delle 15:46», «Roma · Attaccante», «Campionato · Risultati della 7ª giornata». Mai «· copia», «· pagato». Vale per testi, pulsanti, avvisi, notifiche, immagini e commenti nel codice. I numeri restano numeri («· 9 novembre»).
- "Derby" sempre con la D maiuscola. Titoli ed etichette con la maiuscola iniziale.
- I post ufficiali (Girrr Sport, Lega, Giornale) non parlano mai di scommesse.

## La mia settimana — regola editoriale permanente (Gianluca, 12 novembre 2026)

Chiunque modifichi i racconti, i generatori o i prompt di **Carriera → Storia → La mia settimana** deve leggere e applicare [redazione/LA-MIA-SETTIMANA.md](redazione/LA-MIA-SETTIMANA.md).

- È una breve cronaca giornalistica con un filo di stagione: titolo specifico, apertura sulla notizia, sviluppo e aggancio al capitolo successivo. Normalmente tre paragrafi, circa 100–180 parole; meno se i fatti sono pochi.
- Non basta elencare risultato, punti e posizione in prosa. I numeri devono dare significato al racconto, mentre il riepilogo resta nei riquadri tecnici.
- Varietà tra giornate e squadre; niente aperture o frasi identiche a prescindere dagli eventi. Ogni episodio considera il cammino precedente senza anticipare il futuro.
- Soltanto fatti verificati: nessuna scena, sequenza dei gol, emozione personale o dichiarazione inventata. Citazioni attribuite al momento corretto; Derby soltanto se ufficiali, non dedotti dalle rivalità.
- Una bozza già scritta vale solo finché coincidono i fatti di origine. Verificare cronologia e dati prima di riusarla. Nessuna pubblicazione o generazione a pagamento è autorizzata da questa regola.

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
- **Prove su tutti gli schermi (Gianluca, 9 novembre 2026):** ogni novità e ogni versione si prova su telefono piccolo e grande (iPhone SE, iPhone recente, Android piccolo e grande), iPad e tablet Android in verticale e orizzontale, PC (1280, 1920), monitor grande (2560) e smart TV (1920×1080 a densità doppia), con l'identità di iOS e di Android. A Gianluca si mandano le foto su PC e TV. Script pronto nel registro: `prove/prova_schermi_56.js`. Se un motore non è disponibile (per esempio WebKit/Safari) va detto.
- **Browser e manutenzione del Registro (Gianluca, 12 novembre 2026):** incrociare le grandezze degli schermi con Chromium, WebKit e Firefox reali (`registro-browser-qa.yml`, 3 motori × 16 profili). Samsung Internet, Safari su dispositivo, Chrome/Edge di marca e altri browser richiedono una prova separata quando disponibili: cambiare user-agent non vale come collaudo di quel browser. Indicare sempre eseguito, simulato o non disponibile. La manutenzione di Anteprima/Changelog/Archivio nella repo di prova non crea una nuova versione dell'app e non aggiunge annunci in `versioni.json`.

### Cosa serve il "vai" di Gianluca
- Qualsiasi modifica al sito vero, anche una correzione di testo: prima preview nel Lab, poi certificazione e «Vai» esplicito di Gianluca.
- Qualsiasi modifica al database Supabase (progetto `qmjqfgmvimsuxvghetgi`): niente SQL, niente migrazioni, niente dati cambiati senza il suo "vai" esplicito.
- Cancellare file, rami, Pull Request o dati.
- Se un controllo di sicurezza blocca un'operazione, fermati e spiega cosa è successo: non aggirarlo.

### Quando hai finito
- Di' cosa hai cambiato, cosa hai provato e cosa non hai potuto provare (per esempio Safari).
- Per la lega: aggiorna `STATO.md` nel repository `o-girrr-registro`.
- Rispondi in italiano.
