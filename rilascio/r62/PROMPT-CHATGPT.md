> **Superato (16 novembre 2026).** Questo prompt è del 15 novembre e non va più usato: Curva, Giornale e Radio sono cambiati dopo. La release candidate è unita nel Lab; la scaletta del rilascio è in `rilascio/r62/RILASCIO.md`.

# Prompt per ChatGPT: controllo e pubblicazione della parte di Claude nella 6.2

Testo da incollare a ChatGPT (preparato da Claude il 15 novembre 2026 su richiesta di Gianluca).

---

Ciao ChatGPT. Ti chiedo di controllare la parte della **6.2** preparata da Claude, unirla alla tua e, solo dopo il mio «Vai», pubblicarla sul sito.

**Prima di tutto leggi**, nel repository `giandjcosta/o-girrr-registro` (ramo `main`):
- `AGENTS.md`;
- `STATO.md`, la voce «15 novembre (2) — Claude»;
- `REGOLE-VERSIONI.md`, la regola fissa per messaggio e changelog;
- `rilascio/r62/NOTE-CLAUDE.md`.

Nel sito `giandjcosta/o-fant-a-girrr` leggi `AGENTS.md`. Valgono tutte le regole, in particolare:
- niente modifiche a Supabase senza il mio «Vai»;
- mai push forzati;
- rami `chatgpt/…` e commit `ChatGPT: …`.

## Cosa ha fatto Claude (già nel Lab del registro)

**Campo, Lega e Stadio.** Lo script è `rilascio/r62/campo_coppa.py`.
- Interruttore Campionato / Champions Cup con passaggio morbido: indicatore che scorre, dissolvenza breve, bande che sfumano.
- Ogni competizione ricorda giornata e partita.
- Frecce ‹ › per cambiare partita e « » per cambiare giornata; le partite si possono anche scorrere e toccare, e ogni cambio ha una dissolvenza.
- Con il codice della squadra si apre la tua partita, che resta al suo posto nella fila (contorno oro e «La tua partita»).
- Cerchio oro e stella solo al migliore in campo dei dati.
- Simboli di bonus e malus con legenda: ⚽ 🎯 👟 🧤 🛡️ 🥅 ❌ 🔴 ↑.
- Cerchio dei giocatori di casa: nella Lega rosso in Campionato e azzurro in Coppa; nello Stadio azzurro come prima. Ospite sempre bianco.

**Regola nuova sui colori**, scritta in `AGENTS.md`: la grafica **Lega** tiene i colori (Campionato rosso, Coppa azzurra), la grafica **Stadio** è **tutta oro**, anche in Coppa. Gli sfondi azzurrati e rosati restano.

**Altri ritocchi.** Lo script è `rilascio/r62/testi.py`.
- Tabellone: la tua partita al suo posto, con un leggero velo oro e «La tua partita», senza contorno e senza spostarla.
- Tabellone dello Stadio tutto oro, anche in Coppa: interruttore, schede, giornate, bande, gironi e podio.
- Tabellone › Dentro la partita: «= Stessa posizione» e «1 posizione» al singolare (`girrr/v55/ui.js`).
- Albo › La Storia: Padri Fondatori solo con il nome, in fila.

**Decisioni mie da rispettare:**
- Albo d'oro e Derby restano **senza oro**.
- Curva, Giornale, Radio, Storia e Totogirrr restano come sono.

Pagine di prova nel Lab: `lab/novita-6-2.html` e `lab/prova-squadra-62.html`. Le aprono lo specchio `lab/offline/sw-prova.js` e le pagine pronte in `rilascio/r62/pagine/`.

## Cosa ti chiedo di controllare

1. Applica i due script su una **copia nuova di `gh-pages`**:

   ```
   python3 rilascio/r62/campo_coppa.py COPIA
   python3 rilascio/r62/testi.py COPIA
   ```

   Si fermano se una pagina non è quella attesa. Se rieseguiti sulla stessa copia non cambiano niente.

2. **Unisci con la tua 6.2.** Il tuo ramo `chatgpt/coordinamento-62` (PR #92 in bozza, grafica rifiutata) ha anche lui un `rilascio/r62/NOTE.md`, che è tuo; quelle di Claude sono in `NOTE-CLAUDE.md`.
   - `lab/novita-6-2.html` sul `main` del registro è la pagina delle novità 6.2 di Claude: la tua bozza rifiutata spostala altrove (per esempio in `lab/coordinamento-62/`) e aggiungi le tue schede nella stessa pagina, senza cancellare quelle di Claude.
   - Se le tue modifiche toccano gli stessi file (`campo.html`, `tabellone.html`, `girrr/v55/ui.js`, `novita.js`), applica prima le tue e poi gli script di Claude. Se un controllo degli script si ferma, adatta il punto senza perdere né il tuo lavoro né quello di Claude.
   - Decidi con me se la 6.1.1 entra nella 6.2. In cima alle pagine dello specchio c'è ancora «Anteprima 6.1.1»: va allineato.

3. **Prova davvero:** Chromium, WebKit e Firefox × 16 profili × due grafiche (`registro-browser-qa.yml` o le tue prove). Controlla in particolare:
   - 320 px senza scorrimento laterale;
   - console senza errori nuovi (`girrr/v55/cronache.json` dà già 404 sul sito vero, non è una novità);
   - Campionato e Coppa nelle due grafiche, con e senza codice squadra, ospite compreso;
   - fluidità dei cambi;
   - «Riduci movimento»;
   - legenda e simboli;
   - Stadio tutto oro;
   - Lega rosso/azzurro.

   Mandami le foto su PC e TV.

4. **Rilascio, solo dopo il mio «Vai».** Ordine di `AGENTS.md`:
   - prima `gh-pages`, poi controllo del sito vero, solo dopo `main`;
   - aggiorna `ufficiale/src/sito/` del registro con le pagine pubblicate;
   - annota gli hash dei commit e come tornare indietro (`git revert`) in `STATO.md`.

## Versione, messaggio e changelog

Numero **6.2**, tipo **medio**:

```
python3 rilascio/versioni/aggiungi.py --tipo medio --v 6.2 …
```

Scrivi **seguendo esattamente `REGOLE-VERSIONI.md`**:
- un solo messaggio e un solo changelog per tutta la 6.2, mio e tuo insieme, senza nomi degli assistenti;
- messaggio con il «tu», niente Fantapunti né scommesse, saluto finale;
- voci `Area: frase.` con le aree uguali ai nomi delle pagine.

Per la parte di Claude usa queste voci (le tue si aggiungono nelle stesse aree o in aree nuove):

- `Campo: Interruttore Campionato / Champions Cup con passaggio morbido; ogni competizione ricorda la giornata e la partita che stavi guardando.`
- `Campo: Frecce ‹ › per cambiare partita e « » per cambiare giornata; le partite si possono anche scorrere e toccare, con cambi in dissolvenza.`
- `Campo: Con il codice della squadra si apre subito la tua partita, anche in Champions Cup.`
- `Campo: Il migliore in campo ha il cerchio oro e la stella; accanto ai giocatori i simboli di gol, rigori, assist, porta inviolata, gol subiti e autogol, con la legenda.`
- `Campo: Nella grafica Lega il cerchio dei giocatori di casa è rosso in Campionato e azzurro in Champions Cup; nella grafica Stadio resta tutto oro.`
- `Tabellone: Con il codice della squadra la tua partita ha un leggero velo oro e la scritta «La tua partita».`
- `Tabellone: Nella grafica Stadio interruttore, giornate, bande e podio sono oro anche in Champions Cup.`
- `Tabellone: In «Dentro la partita» si legge «= Stessa posizione» e «1 posizione» al singolare.`
- `Albo d’oro: Nella Storia i Padri Fondatori compaiono solo con il nome, tutti in fila.`

Frase proposta per il messaggio (da fondere con le tue novità):

> Nel Campo ora trovi anche le partite della Champions Cup: un tocco sull’interruttore e passi da una competizione all’altra. Quando entri con il tuo codice si apre subito la tua partita, e con le nuove frecce passi da una partita all’altra o salti di giornata.

Prima di scrivere, mandami messaggio e changelog completi per l'approvazione.

## Cartellini

**Già online** (unita con il mio «Vai» il 15 novembre, `1112d94`; i dati hanno già 345 ammonizioni e 10 espulsioni): [giandjcosta/o-fant-a-girrr#17](https://github.com/giandjcosta/o-fant-a-girrr/pull/17) verso `gh-pages`: `scripts/aggiorna_dati.py` legge ammonizioni ed espulsioni (classi `yellow-card` e `red-card` della pagina dei voti) e le aggiunge anche alle giornate già salvate, senza cambiare altro. `pdf_giornale.py` le esclude dalle pagelle. Prove sulle pagine vere nella PR.

Controlla solo che la Moviola delle prossime giornate mostri bene le espulsioni; non serve unire altro.

Voce di changelog da aggiungere:
- `Campo: Accanto ai giocatori anche ammonizioni 🟨 ed espulsioni 🟥, con la legenda.`

Gol decisivo e assist da fermo non sono nella pagina dei voti: restano fuori.

---
