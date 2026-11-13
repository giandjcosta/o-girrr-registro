# Rilascio della 6.0 — passi, controlli e ritorno indietro

Claude, 13 novembre 2026. Vale insieme a `COORDINAMENTO-6.0.md` (ChatGPT) e al ticket #57. Ogni passo che va online o tocca il database richiede il «Vai» esplicito di Gianluca.

## Prima di cominciare
- [ ] «Vai» di Gianluca al rilascio e conferma del numero **6.0** (aggiornamento grande).
- [ ] «Vai» di Gianluca alla SQL `sql/mvp-tifosi-60.sql` (senza lo schema MVP ogni pagina chiama `mvp_stato` e `mvp_derby`, che rispondono 404).
- [ ] `git pull` su tutti e due i rami 6.0 (registro e sito) e sui `main`/`gh-pages`: lavorano più assistenti e i workflow.
- [ ] Se nel frattempo è finita un'altra giornata: rifare la redazione dei tifosi (`redazione/tifosi.py`, `controlla` blocca il rilascio se è vecchia). Il video della nuova giornata lo fa il workflow dopo il rilascio.

## 1. Registro: Lab online per la certificazione
1. Unire `claude/o-girrr-versione-6-0-mjh4ut` nel `main` del registro (senza forzare, `git pull --rebase` prima). Il `main` si pubblica da solo: Lab, `lab/novita-6-0.html` e Ramificazioni vanno online su `giandjcosta.github.io/o-girrr-registro/`.
2. Effetti collaterali da sapere: la Radio del sito legge `voci-src/` dal `main` del registro, quindi i fischi nuovi valgono dalla prima puntata dopo; `ramificazioni.yml` parte ogni 15 minuti (lanciarlo una volta a mano).
3. Gianluca prova nel Lab online e certifica. Senza certificazione ci si ferma qui.

## 2. Database (solo dopo il «Vai» alla SQL)
1. Applicare `sql/mvp-tifosi-60.sql` al progetto `qmjqfgmvimsuxvghetgi`.
2. Advisors di Supabase (sicurezza e prestazioni): nessun avviso nuovo.
3. Letture vere: `mvp_stato` e `mvp_derby` con la chiave pubblica rispondono 200.

## 3. Sito: `gh-pages`
1. Copia NUOVA di `gh-pages` (`git archive origin/gh-pages | tar -x -C COPIA`).
2. `python3 rilascio/rilascio60.py COPIA` (**senza** `--lab`). Si ferma da solo se la copia è già preparata; alla fine stampa «Controllo finale: tutto a posto (copia per il sito vero)».
3. `bash rilascio/versioni/bozza-6-0.sh` per rileggere la voce, poi `bash rilascio/versioni/bozza-6-0.sh --file rilascio/versioni/versioni.json --file COPIA/versioni.json`.
4. Prove sulla copia servita in locale: `prove/prova_60.js` (Chromium, Firefox, WebKit × 16 schermi, **senza** `SENZA_MVP`), le prove di ChatGPT (`prove/prova_integrazione60_browser.py`) e le Curve (`prova_curva_os.js`, `prova_curva_ferma.js`). Scritture bloccate.
5. Copiare la copia preparata su `gh-pages`, commit «Claude: Rilascio 6.0, …», `git pull --rebase`, push. **Annotare l'hash.**
6. Sito vero: Home, Curva, Video, Giornale, Tabellone, Condividi la giornata, MVP, Derby, «La tua settimana» in Lega e Stadio; console senza errori nuovi. Foto PC e TV a Gianluca.

## 4. Sito: `main`
1. Unire `claude/o-girrr-versione-6-0-mjh4ut` nel `main` del sito (workflow `video-giornata.yml` e `tifosi-giornata.yml`, `calcoli/tifosi/`). **Annotare l'hash del merge.**
2. Lanciare a mano `tifosi-giornata.yml` e `video-giornata.yml`: il primo apre la votazione se la scadenza è futura; il secondo deve dire che non c'è un video da fare (la 7ª è già online) o fare quello della giornata nuova.
3. `AGENTS.md` del sito: «Sul sito: 6.0».

## 5. Registro, dopo
- `ufficiale/src/sito/` uguale ai file pubblicati; `AGENTS.md` con la 6.0 e gli hash; `STATO.md`.
- `registro-stato.json`, Anteprima, Changelog e Archivio li allinea il workflow (versione nuova: entro 6 ore, o a mano).

## Tornare indietro
- Pagine: `git revert HASH_GH_PAGES` su `gh-pages` (torna la 5.8.2 in un minuto).
- Workflow: `git revert -m 1 HASH_MERGE_MAIN` sul `main` del sito (si fermano video e MVP).
- Database (solo con il «Vai»): lo schema MVP è separato e non tocca dati esistenti. Per toglierlo: `drop function public.mvp_stato, public.mvp_mio, public.mvp_vota, public.mvp_prepara, public.mvp_derby, public.mvp_chiudi;` poi `drop schema mvp_private cascade;` (si perdono soltanto i voti MVP).
- Registro: `git revert -m 1 HASH_MERGE` sul `main` del registro (la Radio torna ai fischi di prima).
