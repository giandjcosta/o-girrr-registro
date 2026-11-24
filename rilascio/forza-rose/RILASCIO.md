# Forza della rosa: classifica delle rose sul server (proposta, 24 novembre 2026)

Regola di Gianluca: nella scheda della squadra (pagina Squadre, Lega e Stadio) si legge «**Xª rosa su 10** · Dopo la Nª giornata» e sotto «**Al completo: 94 su 100**».
- **Classifica delle rose**: fotografia calcolata sul server da `calcoli/forza_rose.py` → `girrr/dati/forza-rose.json`. Si rifà solo quando si chiude una giornata di Campionato o cambia una rosa (scambio). Per ogni giocatore: attesa di partenza (fantamedia dell'anno scorso pesata con le presenze e media del ruolo), fantavoti veri di quest'anno, giornate che mancano al voto atteso corretto dalla resa (sopra o sotto l'attesa). Le assenze non contano. Migliori undici nel modulo che rende di più.
- **Al completo**: la forza della rosa con tutti sani, quella della Carriera (`FZ` in `girrr/app.html`). Resta ferma.
- Niente frecce né «era 3ª».

## Passi del rilascio (con il «Vai» di Gianluca)
1. `main` del sito: copiare `calcoli/forza_rose.py` in `calcoli/` e aggiungere in `.github/workflows/dopo-giornata.yml`, prima di «Salvo i dati del sito», senza condizione:
   ```yaml
         - name: Classifica delle rose (dopo ogni giornata di Campionato o scambio)
           run: python3 code/calcoli/forza_rose.py site
   ```
   Il passo «Salvo i dati del sito» fa già `git add girrr/dati`.
2. `gh-pages`: `python3 rilascio/forza-rose/applica.py CARTELLA_GH_PAGES` (seconda volta «File cambiati: 0») e `python3 calcoli/forza_rose.py CARTELLA_GH_PAGES` per la prima fotografia.
3. Prove: pagina Squadre in Lega e Stadio a 320, 390 e 1280 px, console senza errori. Foto: `foto/scheda-forza-rosa.png`.

Per tornare indietro: `git revert` dei due commit. Senza `forza-rose.json` la scheda torna da sola al calcolo nella pagina.
La pagina Squadre non ha una sorgente in `ufficiale/src/sito/`: la modifica sta tutta in `applica.py`.
