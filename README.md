# O Girrr · Repository di prova

**Questa è la repository di prova di O Fant A Girrr.** Qui si costruiscono e si provano le idee nuove prima di metterle nell'app vera. Niente di quello che c'è qui tocca il sito vero finché non arriva il "vai" di Gianluca.

- **Sito vero:** repository [o-fant-a-girrr](https://github.com/giandjcosta/o-fant-a-girrr), pubblicato su https://giandjcosta.github.io/o-fant-a-girrr/
- **Questa repository:** https://giandjcosta.github.io/o-girrr-registro/ (Registro, Laboratorio e Anteprima)

## Link utili

| Cosa | Link |
|---|---|
| **Sito vero** · grafica Lega | https://giandjcosta.github.io/o-fant-a-girrr/girrr/ |
| **Sito vero** · grafica Stadio | https://giandjcosta.github.io/o-fant-a-girrr/stadio/girrr/ |
| Sito vero in **modalità ospite** (sola lettura, da condividere) | https://giandjcosta.github.io/o-fant-a-girrr/girrr/?ospite=1 |
| **Registro** · Changelog (le modifiche giorno per giorno) | https://giandjcosta.github.io/o-girrr-registro/ |
| **Aggiornamenti** (cosa porta ogni versione) | https://giandjcosta.github.io/o-girrr-registro/aggiornamenti.html |
| **Laboratorio** (le prove nuove) | https://giandjcosta.github.io/o-girrr-registro/lab/ |
| **Novità 5.5** (tutte le novità con foto e link) | https://giandjcosta.github.io/o-girrr-registro/lab/novita-5-5.html |
| **Anteprima corrente** · ultima versione online, in sola lettura, con scelta della grafica | https://giandjcosta.github.io/o-girrr-registro/ufficiale/ |
| Archivio della prova 5.5 · pagine (Home, Notifiche, Tabellone, Campo, Albo, Curva) | https://giandjcosta.github.io/o-girrr-registro/anteprima/5.5/index.html |
| Anteprima storica dell'app 5.5 · Lega / Stadio | https://giandjcosta.github.io/o-girrr-registro/anteprima/attuale.html · https://giandjcosta.github.io/o-girrr-registro/anteprima/index.html |
| Archivio delle versioni uscite | https://giandjcosta.github.io/o-girrr-registro/archivio.html |
| Stato del progetto (cosa è online, cosa è in prova) | [STATO.md](STATO.md) |
| Collaudo automatico su telefono e PC, Chromium e WebKit (Safari) | https://github.com/giandjcosta/o-girrr-registro/actions/workflows/claude-collaudo-55.yml |

Versione online sul sito vero: **5.8.1**. Anteprima corrente: copia in sola lettura della stessa versione; i prototipi restano nel Laboratorio. Allineamento automatico dopo le modifiche al Lab e controllo dei rilasci ogni 30 minuti (gli orari GitHub possono slittare).

Per riprendere il lavoro in una chat nuova: "Leggi STATO.md nel repo o-girrr-registro e continuiamo da lì". In `STATO.md` c'è cosa è online, cosa è in prova e cosa resta da fare.

## Cosa c'è

| Cartella / file | A cosa serve |
|---|---|
| `index.html`, `aggiornamenti.html` | **Registro modifiche**: legge i commit pubblici di o-fant-a-girrr e li mostra giorno per giorno, con l'elenco delle attività automatiche (`automazioni.json`). Legge da solo le ultime 100 modifiche; la copia salvata del resto si rinfresca con `python3 changelog.py`. |
| `lab/` | **Laboratorio**: i prototipi delle idee nuove, da far provare agli amici. Si apre da `/lab/`. `lab/novita-5-5.html` mostra le novità della versione in prova; `lab/versione-5-3.html`, `-5-2`, `-5-1` e `versione-5.html` sono gli archivi delle versioni uscite. |
| `anteprima/` | **Anteprima**: il Laboratorio impaginato come l'app vera, in tutte e due le grafiche (`index.html` Stadio, `attuale.html` Lega), con database finto (salvo le notifiche personali). Le pagine nuove della 5.5 sono in `anteprima/5.5/`. Si genera con `python3 anteprima/build.py` e si apre da `/ufficiale/` o `/anteprima/`. |
| `calcoli/` | Calcoli automatici prima di passarli al sito: fiducia, probabilità, Borsino, Moviola, post della Curva, fine stagione. Spiegati in `calcoli/LEGGIMI.md`. |
| `ufficiale/` | Le sorgenti delle pagine del sito vero (Lega e Stadio) da cui si costruisce il rilascio (`ufficiale/build.py`). |
| `rilascio/` | Gli strumenti per portare le novità sul sito vero: `pacchetto.py` prepara i file, `applica.py` mostra le differenze e, con `--vai`, fa i commit. Procedura in `rilascio/LEGGIMI.md`. |
| `prove/` | Le prove automatiche (Moviola, collaudo nel browser con Playwright: `prove/collaudo_55_browser.js` prova tutte le pagine 5.5 a 320, 390, 768, 1280 e 1440 px). |
| `voci-src/` | La **Radio Girrr**: copioni, voci e montaggio delle puntate, con i workflow `voci-*.yml` che le generano. |
| `sql/` | Funzioni del database in prova (Derby, Sfide, quote dei Derby, conferenze). |
| `servizio/` | Idee e bozze per far diventare O Girrr un servizio per più leghe. Non c'è codice che gira. |
| `moviola-video.html` | Pagina di lavoro per aggiungere i video agli episodi della Moviola. |

## Dalla prova al sito vero

1. Si prova qui: Laboratorio, Anteprima e prove automatiche.
2. Si prepara il pacchetto con `rilascio/pacchetto.py` e si guarda cosa cambierebbe con `rilascio/applica.py`.
3. Solo con il "vai" di Gianluca si fa il push sui rami `gh-pages` e `main` di o-fant-a-girrr.

Ogni modifica destinata al sito, comprese le correzioni di testo, viene prima mostrata e provata nel Lab. Il sito vero aspetta la certificazione della prova e il "vai" esplicito di Gianluca.

L’allineamento automatico è eseguito da `.github/workflows/sincronizza-registro.yml`: rigenera Anteprima, Archivio e Changelog dopo le modifiche al Lab e controlla il sito ogni 30 minuti. La versione e il commit sincronizzati sono in `registro-stato.json`. Le modifiche sperimentali non ancora unite a `main` restano sui rami degli autori.
