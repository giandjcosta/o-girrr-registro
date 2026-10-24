# O Girrr · Repository di prova

**Questa è la repository di prova di O Fant A Girrr.** Qui si costruiscono e si provano le idee nuove prima di metterle nell'app vera. Niente di quello che c'è qui tocca il sito vero finché non arriva il "vai" di Gianluca.

- **Sito vero:** repository [o-fant-a-girrr](https://github.com/giandjcosta/o-fant-a-girrr), pubblicato su https://giandjcosta.github.io/o-fant-a-girrr/
- **Questa repository:** https://giandjcosta.github.io/o-girrr-registro/ (Registro, Laboratorio e Anteprima)

Per riprendere il lavoro in una chat nuova: "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì". In `STATO.md` c'è cosa è online, cosa è in prova e cosa resta da fare.

## Cosa c'è

| Cartella / file | A cosa serve |
|---|---|
| `index.html`, `aggiornamenti.html` | **Registro modifiche**: legge i commit pubblici di o-fant-a-girrr e li mostra giorno per giorno, con l'elenco delle attività automatiche (`automazioni.json`). Si aggiorna da solo (`aggiorna.py`). |
| `lab/` | **Laboratorio**: i prototipi delle idee nuove, da far provare agli amici. Si apre da `/lab/`. `lab/versione-5.html` elenca cosa è pronto e cosa manca per la 5.0. |
| `anteprima/` | **Anteprima**: il Laboratorio impaginato come l'app vera, in tutte e due le grafiche (`index.html` Stadio, `attuale.html` Lega), con database finto. Si genera con `python3 anteprima/build.py` e si apre da `/anteprima/`. |
| `calcoli/` | Calcoli automatici prima di passarli al sito: fiducia, probabilità, Borsino, Moviola, post della Curva, fine stagione. Spiegati in `calcoli/LEGGIMI.md`. |
| `ufficiale/` | Le sorgenti delle pagine del sito vero (Lega e Stadio) da cui si costruisce il rilascio (`ufficiale/build.py`). |
| `rilascio/` | Gli strumenti per portare le novità sul sito vero: `pacchetto.py` prepara i file, `applica.py` mostra le differenze e, con `--vai`, fa i commit. Procedura in `rilascio/LEGGIMI.md`. |
| `prove/` | Le prove automatiche (Moviola, prova nel browser con Playwright). |
| `voci-src/` | La **Radio Girrr**: copioni, voci e montaggio delle puntate, con i workflow `voci-*.yml` che le generano. |
| `sql/` | Funzioni del database in prova (Derby, Sfide, quote dei Derby, conferenze). |
| `servizio/` | Idee e bozze per far diventare O Girrr un servizio per più leghe. Non c'è codice che gira. |
| `moviola-video.html` | Pagina di lavoro per aggiungere i video agli episodi della Moviola. |

## Dalla prova al sito vero

1. Si prova qui: Laboratorio, Anteprima e prove automatiche.
2. Si prepara il pacchetto con `rilascio/pacchetto.py` e si guarda cosa cambierebbe con `rilascio/applica.py`.
3. Solo con il "vai" di Gianluca si fa il push sui rami `gh-pages` e `main` di o-fant-a-girrr.

Le micro correzioni di testo vanno online in automatico, con avviso dopo; tutto il resto aspetta il "vai".
