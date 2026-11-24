# Fine giornata: cosa si aggiorna e chi lo aggiorna

Elenco completo, per non dimenticare niente (Gianluca, 24 novembre 2026). L'ordine dei passi resta quello della skill «Chiudere una giornata di O Girrr» e di `scripts/PROCEDURA.md` su `gh-pages`. Qui sotto c'è **tutto quello che cambia** dopo una giornata: per la pagina e per ogni allenatore.

## 0. Il via
Quando Gianluca scrive «giornata finita / da calcolare / posta la giornata» parte tutta la sequenza. Restano separati il «Vai» per il database Supabase e quello per cancellare file o rami.

## 1. Risultati da Leghe (a mano, con Claude)
| Cosa | Chi | Come si controlla |
|---|---|---|
| Punteggi e risultati di Campionato e Coppa in `data.json` (`cal`, `calcTs`) | Claude, dal Chrome di Gianluca loggato su Leghe (`scripts/PROCEDURA.md`, passi 1-3), oppure l'attività «Fanta lega: risultati di lega dal PC» | `leghe_importa.py` si ferma se i totali non tornano |
| Voti e statistiche di Serie A (`votiTs`, `formazioni.json`) | Workflow «Aggiorna statistiche e voti» (da solo, più volte al giorno) | `votiTs` della giornata presente |

Serve il computer di Gianluca acceso con Chrome: da una sessione nel cloud Leghe non si legge.

## 2. Automatico, appena i risultati sono in `data.json`
Workflow «Calcoli dopo la giornata» (ogni 2 ore, o lanciato a mano):
| Cosa | File | Dove si vede |
|---|---|---|
| Promesse delle conferenze chiuse | database | Sala stampa |
| Sfide 1 contro 1 del Totogirrr chiuse | database | Totogirrr |
| Fiducia, probabilità, Borsino | `girrr/dati/fiducia.json`, `probabilita.json`, `borsino.json`, `lab-dati.json` | Tabellone, Carriera, Borsino |
| Giro di boa e bilanci della stagione | `girrr/dati/giro-di-boa.json` | Bilanci, album, Radio |
| **Oggi al Girrr** (cronache della Home) | `girrr/dati/cronache.json` | Home |
| Moviola della giornata | `girrr/dati/moviola.json` | Girrr Sport |
| Post della Curva (in scaletta) | database | Curva |

Subito dopo, il workflow «Video della giornata» prepara `girrr/video/giornata-NN.mp4`.

## 3. Calcolato dalla pagina, per ogni allenatore (non c'è un file da aggiornare)
Queste parti si rifanno da sole dentro il browser appena `data.json` ha la giornata, per la squadra di chi è entrato:
- **La tua settimana** (Home): `girrr/v60/tifosi.js`, dall'ultima giornata completa.
- **Carriera**, **Statistiche** personali, **Spogliatoio** (rosa e giornata), **Classifica dei Derby**, **Albo d'oro** e record.
- **Notifiche** («Risultati della giornata», «Classifica aggiornata», «Il podio sfugge»…).

Se una di queste non cambia, il problema è quasi sempre in `data.json` (giornata non importata o non completa), non nella pagina.

## 4. A mano, con Claude
| Cosa | Note |
|---|---|
| **Giornale** (`testi.json`, PDF di 4 pagine, archivio, tabellone grafico di Lega e di Coppa) | Skill, passo 3. Le pagine del PDF si guardano una per una |
| **Moviola manuale** | Solo se Gianluca manda episodi con link (`calcoli/moviola-manuale.json`) |
| **Post vero della Curva della settimana** per la Radio | Chiedere a Gianluca, una volta a settimana |

## 5. Automatico, più tardi
| Cosa | Chi | Quando |
|---|---|---|
| **Radio** (`girrr/voci/puntata-gNN.mp3`) | Workflow «Radio della giornata» | Circa 70 minuti dopo il Giornale, se Gemini risponde |
| **Squadra della settimana (MVP)**: votazione e verdetto | Workflow «MVP dei tifosi» | Ogni 15 minuti, `girrr/dati/mvp-editoriale.json` |
| **Premi sponsor** | Workflow «Premi sponsor della giornata» | Ogni notte |
| **Domande della prossima conferenza** | Attività «Redazione di Girrr Sport» | `girrr/dati/redazione.json` |
| Totogirrr: quote, risultati e pagamenti | Workflow «Aggiorna statistiche e voti» | Più volte al giorno |

## 6. Controllo finale (obbligatorio)
Dalla radice di `gh-pages`: `python3 -I scripts/controllo_giornata.py N`.
- Dal 24 novembre 2026 controlla anche fiducia e probabilità, Moviola, Oggi al Girrr, giro di boa, settimane dei tifosi, MVP, Radio, video, domande della conferenza e tabellone della Coppa. Nuova versione in `rilascio/fine-giornata/controllo_giornata.py`: va copiata in `scripts/` di `gh-pages` con il «Vai» di Gianluca.
- **ERRORE** = la giornata non è finita. **AVVISO** = cosa che arriva più tardi (Radio, video, MVP) o da guardare a mano.
- Poi si apre il sito vero (Home con «La tua settimana» e «Oggi al Girrr», Curva, Girrr Sport, Tabellone, Giornale), con la console senza errori nuovi.
- Alla fine si aggiorna `STATO.md`.
