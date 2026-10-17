# Calcoli automatici (versione 5.0)

Script che leggono `data.json` della lega e producono file pronti per il sito. Non scrivono nel database.
Quando la 5.0 esce, vanno copiati in `scripts/` del repo della lega e agganciati all'Action "Aggiorna statistiche e voti".

| Script | Cosa fa | Stato |
|---|---|---|
| `fiducia.py` | Fiducia del presidente dopo ogni giornata (campionato, Coppa a peso ridotto, promesse in conferenza). Scrive `fiducia.json`. | Fatto, uguale al Laboratorio su 9 squadre su 10 (la decima differisce di 1 per la Coppa) |
| `probabilita.py` | Probabilità di scudetto, podio e ultimo posto dopo ogni giornata, con il motore di Totogirrr (`scripts/toto_quote.py` del repo della lega). Scrive `probabilita.json`. | Fatto |
| `borsino.py` | Valore dei giocatori giornata per giornata: parte dalla quotazione e sale o scende col fantavoto rispetto alla media del ruolo. Scrive `borsino.json`. | Fatto, regola da confermare |
| `aspettative.json` | Aspettative a inizio stagione (obiettivo del presidente, posto atteso). Fisse per tutta la stagione. | Generato dal Laboratorio |
| `conferenze.json` | Promesse fatte in conferenza stampa (squadra, giornata, testo, peso 1-3). Oggi vuoto: arriverà dalla tabella `conf_risposta` del database. | Da collegare |

Regola delle promesse (proposta, da confermare): mantenuta +1,5, pareggio -1, tradita -4, per il peso della promessa e per il peso della stagione.
