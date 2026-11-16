# Rilascio 6.2 — scaletta operativa

Preparata da Claude il 16 novembre 2026 su richiesta di Gianluca («Risolvi tutti così da esser pronti per la release»). Si esegue **solo** dopo:

1. il «Vai» di Gianluca alla pubblicazione;
2. il «Vai» alla SQL, che comprende tre file: `votazioni-62-proposta.sql`, `finestre-62-proposta.sql` e `albo-62-proposta.sql`;
3. l'approvazione del testo dell'annuncio (`ANNUNCIO-APPROVAZIONE.json`, 24 voci, validato in `ANNUNCIO-VALIDAZIONE.txt`).

Regole: niente push forzati, `git pull --rebase` prima di ogni push, nessun audio, nessun dato inventato. Sicurezza e limiti della SQL sono in `SICUREZZA-SQL.md`.

## 0. Controlli prima di toccare qualcosa

- `main` del registro con la release candidate unita; `integrazione-62-qa.yml` verde nei tre motori sullo stesso commit.
- `git fetch` dei due repository; annotare gli hash di partenza di `gh-pages` e del `main` del sito.
- Copia di partenza di `gh-pages`: `git archive origin/gh-pages | tar -x -C BASE`.

## 1. Fotografia del database (sola lettura)

Con lo strumento SQL di Supabase (progetto `qmjqfgmvimsuxvghetgi`) salvare in `rilascio/r62/prima/`:

- le definizioni attuali di `mvp_vota`, `mvp_prepara`, `sondaggio_vota`, `curva_vota`: `select pg_get_functiondef(p.oid) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('mvp_vota','mvp_prepara','sondaggio_vota','curva_vota');`
- i conteggi dei voti: `sondaggio_private.voti` per giornata, `mvp_private.voti` per stagione e giornata, `curva_vote`;
- la scadenza della 7ª: `select chiude from mvp_private.giornate where stagione='2026/27' and giornata=7;` (atteso: 21 novembre 2026 alle 15:00, ora italiana).

Le definizioni salvate servono per tornare indietro.

## 2. SQL, in quest'ordine

1. `sql/votazioni-62-proposta.sql`
2. `sql/finestre-62-proposta.sql`
3. `sql/albo-62-proposta.sql`

Ognuno va applicato come migrazione con un nome, per esempio `claude_v62_votazioni`, `claude_v62_finestre` e `claude_v62_albo`.

Dopo ciascuno, solo letture:

- `select public.v62_sondaggi('2026/27',null,null);`
- `select public.v62_finestre('2026/27');`
- `select public.v62_albo('2026/27');`
- `select public.mvp_stato('2026/27',7);`

I conteggi dei voti devono restare quelli del punto 1. Il voto 6.1 delle sfide continua a funzionare anche senza catalogo, per il ramo di compatibilità di `sondaggio_vota`.

## 3. Catalogo dei sondaggi, prima delle pagine

In questo ambiente non c'è la chiave segreta del servizio, quindi il piano si genera in locale e si applica con lo strumento SQL.

1. Copia del backend: `python3 rilascio/r62/backend.py MAIN_SITO COPIA_BACKEND`.
2. Piano, senza rete: `cd COPIA_BACKEND && python3 calcoli/catalogo62.py BASE`.

   Il 16 novembre il piano ha un solo sondaggio: `sfida:2026/27:8`. Le scelte sono scritte come i 2 voti già presenti per l'8ª: «Mariana Coneja – Oranje VC» e «Apo team – Atletico ma non troppo». Chiude il 21 novembre alle 14:00 UTC.
3. Per ogni voce del piano: `select public.v62_prepara(p_id,p_stagione,p_origine,p_fonte,p_giornata,p_titolo,p_scelte::jsonb,p_aperto::timestamptz,p_chiude::timestamptz);`
4. Finestra della vigilia per la stessa giornata, con gli stessi orari: `select public.v62_finestre_prepara('2026/27','vigilia',8,APERTO,CHIUDE);`
5. Verifica, in sola lettura:
   - `v62_sondaggi` mostra l'8ª con i voti già dati;
   - i conteggi di `sondaggio_private.voti` sono invariati;
   - la 7ª MVP chiude ancora il 21 novembre alle 15:00, ora italiana.

Dal rilascio in poi il catalogo lo aggiorna il workflow `tifosi-giornata.yml` del sito, con la chiave nei segreti di GitHub.

## 4. Pagine: `gh-pages`

1. `python3 rilascio/r62/applica.py BASE --out USCITA`, su una copia nuova.
2. Copiare in un checkout di `gh-pages` solo i file che cambiano. L'elenco si ricava con `diff -rq BASE USCITA` e sono 23 file: pagine Lega e Stadio, `sondaggi62.js`, `albo62.js`, `scripts/pdf_giornale.py`, `scripts/mvp_giornale62.py`, `stagione.js` e gli altri moduli.
3. Aggiungere la 6.2 con `python3 rilascio/versioni/aggiungi.py`, con gli argomenti di `ANNUNCIO-APPROVAZIONE.json`, `--tipo medio --v 6.2` e senza `--prova`. Poi copiare `rilascio/versioni/versioni.json` nella radice di `gh-pages`.
4. Commit `Claude: …`, `git pull --rebase`, push. Annotare l'hash.
5. Sul sito vero, Lega e Stadio, a 320 px e su PC, la console non deve avere errori nuovi:
   - Home, con l'avviso 6.2;
   - Campo, Campionato e Coppa;
   - Tabellone;
   - Curva, con voto e «Cambia il mio voto» provati con una squadra di prova solo se Gianluca lo chiede;
   - Girrr Sport › Sondaggi;
   - Albo › Record;
   - Versioni.

## 5. `main` del sito

1. `python3 rilascio/r62/backend.py MAIN_SITO COPIA`. Lo script si ferma se il sito ha modifiche che il registro non conosce.
2. Copiare nel `main` del sito i file cambiati:
   - workflow `tifosi-giornata.yml` e `radio-giornata.yml`;
   - in `calcoli/`: `catalogo62.py`, `finestre62.py`, `giuria62.py`, `leggi_eventi.py`, `post_curva.py`, `tifosi/sincronizza.py`.
3. Commit, `git pull --rebase`, push. Annotare l'hash.
4. Nessun avvio manuale di Radio o TTS. Il primo giro ordinario usa il flag `--mvp-tifosi`, con al massimo due battute brevi.

## 6. Registro

- Allineare `ufficiale/src/sito/` alle pagine pubblicate.
- In `STATO.md` scrivere la versione, gli hash di `gh-pages` e del `main` del sito, le migrazioni applicate e come tornare indietro.
- Il workflow `sincronizza-registro.yml` aggiorna da solo Anteprima, Changelog e Archivio: non toccarli a mano.

## Tornare indietro

- **Pagine:** `git revert HASH_GH_PAGES` su `gh-pages`, poi `versioni.json` torna alla 6.1.
- **`main` del sito:** `git revert HASH_MAIN_SITO`.
- **Database:** ripristinare le definizioni salvate al punto 1 per `mvp_vota`, `mvp_prepara`, `sondaggio_vota` e `curva_vota`, e togliere i trigger `conf_finestre62` e `dopo_finestre62`. Le funzioni nuove `v62_*` e lo schema `votazioni62_private` possono restare: le pagine 6.1 non li usano. **Non cancellare voti, cataloghi o verdetti.**

## Dopo il rilascio, da fare ma non bloccante

- Voti delle sfide per stagione (`sondaggio_private.voti` senza stagione): proposta separata in `SICUREZZA-SQL.md`, prima della stagione 2027/28.
- Partita più seguita: dati veri solo quando la redazione carica le giurie con `calcoli/giuria62.py … --vai`. Fino ad allora «Dato non disponibile».
- Prove su Safari di un iPhone vero, Samsung Internet e TV fisiche: non disponibili qui.
