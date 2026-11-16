# Rilascio 6.2.2 · «Carriera e Derby più fluidi»

- 16 novembre 2026, «Vai» di Gianluca. Tipo: minore. Messaggio: `ANNUNCIO-BOZZA.json`, approvato così com'è.
- `gh-pages` del sito: `64a243b` (da `19653ba`). `main` del sito e del registro: invariati dalla 6.2.2.
- Passi: `python3 rilascio/r622/applica.py COPIA_GH_PAGES` due volte (29 pagine, poi 0) · `rilascio/versioni/aggiungi.py --tipo minore` · `node --check` sui cinque `.js` toccati · commit su `gh-pages`, `git pull --rebase`, push.
- **Per tornare indietro: `git revert 64a243b` su `gh-pages`.**
- Niente SQL nella 6.2.2.
