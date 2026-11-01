# ChatGPT: cronache di classifica 5.5 — consegna del 1 novembre

La preparazione ora collega lo stesso evento a Girrr Sport, profilo Giornale,
commento della Curva, copione Radio e Giornale PDF. Il test integrato che falliva
su questa base è risolto. La selezione condivisa conserva priorità, soglie,
cooldown e chiave stagionale verificabile; nessuna rotazione obbligatoria dei canali.

## Revisione navigabile

- [Lab → Cronache di prova](https://giandjcosta.github.io/o-girrr-registro/lab/cronache-prova/).
- [Anteprima 5.5](https://giandjcosta.github.io/o-girrr-registro/anteprima/5.5/).
- [PR #44](https://github.com/giandjcosta/o-girrr-registro/pull/44).

Il dossier contiene un'edizione locale costruita dai dati pubblici della G5:
crisi di WOA, ultima per due giornate e attesa seconda. Gli input del Giornale
contengono titoli/commento minimi per la prova: non sono un'edizione ufficiale.
I tre testi social sono preparazioni, non interventi inviati dagli utenti.
Le schermate Home/Curva della 5.5 mantengono l'export condiviso `cronache.json`;
il dossier serve a verificare anche i canali che non si pubblicano in Anteprima.

## Comando di preparazione

```sh
python3 calcoli/prepara_cronache.py SITO_LOCALE EVENTI.json TESTI.json USCITA_SEPARATA --scripts-pdf SORGENTI_PDF_LOCALI
```

Il sito locale deve contenere `data.json` e `girrr/dati/lab-dati.json` allineati.
Il comando copia gli input in una cartella temporanea, prepara i testi e crea
un dossier HTML, JSON tracciabili e PDF. Non importa publisher, client database
o generatori vocali. Non modifica gli input, gli archivi Radio o il sito.
Richiede Playwright/Chromium solo con `--scripts-pdf`; senza, prepara i soli testi.
Rifiuta output dentro il sito sorgente o cartelle non vuote estranee alla prova.
Rieseguire gli stessi input conserva chiavi e testi; input diversi hanno cartelle
diverse e un indice corrente, evitando di presentare un vecchio contenuto come nuovo.
Con calcoli non allineati o Coppa ancora aperta il dossier indica l'attesa.

## Compatibilità e futura attivazione sul sito

**Il workflow Radio ufficiale legge già `voci-src` dal `main` del Registro.**
Verificato in sola lettura in `o-fant-a-girrr/main/.github/workflows/radio-giornata.yml`.
Per questo le nuove cronache richiedono esplicitamente `--cronache-classifica` in
`prepara_dati.py`, che marca i dati per il nuovo ramo del copione. Senza flag:
stessi testi e stessa sequenza casuale precedenti; eventuali marcatori vecchi nello
snapshot sono rimossi. Confermato con 32 copioni confrontati tramite SHA-256.
Il merge nel Registro non attiva la novità nella Radio ufficiale.

Anche `post_curva.py` richiede il flag e un `data.json` locale esplicito.
Le storie vengono ricalcolate: eventi importati vecchi, doppi o contraffatti non
sostituiscono quello selezionato. Mantiene gli altri tipi di post e la Moviola.
Se il modulo manca, la preparazione esplicita fallisce: non salta silenziosamente
il collegamento. Per un futuro rilascio servono insieme `zone_classifica.py`,
`aspettative.json` e `giornale_classifica.py`, oltre agli script chiamanti.

Il generatore PDF di riferimento è
`o-fant-a-girrr/gh-pages/scripts/pdf_giornale.py`, con `pdf_settimana.py` e
`toto_quote.py`. Le copie usate dal dossier hanno SHA-256 in `provenienza.json`.
`render_giornale_prova.py` esegue solo `costruisci` e il controllo dei margini:
non la CLI originale e non il workflow. La rete del browser è bloccata.
L'adattatore applica alle copie in memoria la chiusura condivisa delle giornate:
il generatore originale considerava giocato anche un turno con una sola gara finita.
Il test verifica quattro pagine, inclusione unica e allineamento al copione anche
con il turno successivo parziale. Nessun sorgente del sito è stato modificato.

**Prima della produzione resta necessario un rilascio esplicito autorizzato:**
aggiornare i chiamanti nel sito, passare il flag ai preparatori, integrare il testo
con `giornale_classifica.integra` prima del renderer ufficiale e portare la correzione
dei turni parziali nel generatore del sito. Nessun workflow pubblico è stato cambiato.
Nessun post inviato, database scritto o audio generato durante questa consegna.

## Verifiche

- PASS: Anteprima 5.2 statica, milestone Totogirrr, fiducia, Moviola, zone di classifica,
  cronache integrate, compatibilità Radio, pacchetto idempotente e casi limite Annuario.
- PASS: percorso Lab → dossier → PDF a 320/390/768/1280/1440, senza overflow o errori.
- PASS: Campo con formazioni vere/controllate (anche 10 + 11), ingresso dal Registro e
  percorsi completi Home/Tabellone/Campo/Albo/Curva/Notifiche nelle due grafiche.
- Il vecchio controllo dei Fantapunti bianchi è stato corretto: la grafica vigente
  li mostra azzurri come richiesto. DR e punti restano bianchi. Nessuna modifica UI
  introdotta per far passare il controllo.
- Browser usato: Chromium. Safari/iPhone fisico, invii reali, nuova giornata futura
  in produzione e audio non verificati e non eseguiti. Il collaudo non certifica
  l'approvazione estetica di Gianluca.

Screenshot del dossier, PDF e rapporti: `prove/risultati-cronache-55/`.
Screenshot delle due grafiche/legenda e rapporti precedenti nella stessa PR:
`prove/risultati-verifica-55/` e `prove/risultati-legenda-55/`.
