# Albo 6.2 — dati dei sondaggi e giurie

**Solo proposta nel branch; non applicata a Supabase.** Questa parte completa il contratto frontend di Claude senza modificarne la grafica.

## Fonte e vincoli

- `sql/albo-62-proposta.sql` introduce `v62_albo(p_stagione)`, la registrazione server `v62_giuria_sfide_prepara` e la chiusura di stagione `v62_albo_finalizza`.
- La pagina dell'Albo legge la RPC; i voti degli allenatori rimangono nella tabella originale `sondaggio_private.voti`. Le due giurie sono salvate, una sola volta, in `votazioni62_private.giuria_sfide`, con un autore, una scelta presente nel sondaggio e una motivazione verificabile.
- La redazione deve fornire un dossier **reale**, non un esempio inventato. La registrazione accetta un solo voto per autore e tipo, esige almeno un redattore e un personaggio e rifiuta modifiche successive; non apre votazioni dopo la scadenza.
- I numeri sono **conteggi di preferenze**, non valutazioni ponderate: ogni allenatore, membro della redazione e personaggio conta un voto nella scelta «Quale sfida seguire».
- Se non esistono sondaggi conclusi con date note e giurie complete, `partite` è `null`: Claude mostra «Dato non disponibile». Le giornate prima dell'attivazione, con `aperto=null`, sono escluse: niente voti editoriali retroattivi immaginati.
- L'attuale tabella dei voti degli allenatori non ha la stagione; **per prudenza `partite=null` per le stagioni diverse da 2026/27**. Prima della prossima stagione bisogna introdurre una chiave stagionale e migrare i dati con stagione verificata. Non riusare il numero di giornata per attribuire automaticamente voti vecchi.
- `mvp` e `mvp_classifica` derivano esclusivamente dalle classifiche archiviate al momento della chiusura dell'MVP, non da un risultato ricalcolato. A pari MVP rimangono pari merito; l'ordine tra pari non cambia il premio.
- `stagione_conclusa` è falso finché il servizio non certifica esplicitamente l'ultima giornata reale con `v62_albo_finalizza`. Nessuna conclusione della stagione viene dedotta per ipotesi.

## Contratto dell'Albo

```json
{
  "stagione": "2026/27",
  "mvp": [{"giornata": 7, "team": "squadra vincitrice verificata", "chiusa": "timestamp"}],
  "mvp_classifica": [{"team": "squadra vincitrice verificata", "mvp": 1, "giornate": [7]}],
  "partite": null,
  "stagione_conclusa": false
}
```

Quando tutti i dati richiesti sono disponibili, `partite` diventa una lista ordinata per voto totale, con voci `{id,giornata,partita,voti:{allenatori,redazione,personaggi,totale}}`.

## Ingresso del dossier editoriale (ancora da produrre)

Preparare un file dedicato, ad esempio `redazione/sfide62.json`, **solo dopo che la redazione ha realmente espresso i voti**, nel formato:

```json
{
  "stagione": "2026/27",
  "giornate": {
    "8": [
      {"tipo": "redazione", "autore": "Nome redattore", "scelta": "ESATTO TESTO OPZIONE DAL SONDAGGIO", "motivo": "Motivo realmente approvato"},
      {"tipo": "personaggio", "autore": "Nome personaggio", "scelta": "ESATTO TESTO OPZIONE DAL SONDAGGIO", "motivo": "Motivo realmente motivato"}
    ]
  }
}
```

`rilascio/r62/server/giuria62.py` rifiuta opzioni diverse dalle partite in `data.json` e controlla che non manchi alcun tipo di giuria. La chiamata senza `--vai` valida il dossier senza rete; la chiamata con `--vai` scrive nel database e richiede autorizzazione esplicita, credenziali di servizio e sito già alla 6.2. Il collegamento all'automazione ordinaria non è ancora stato effettuato: **non dichiarare completa la popolazione dei dati editoriali fino alla consegna del dossier e a un test autorizzato**.

## Verifiche

`prove/v62/postgres_albo.py` usa solo PGHOST localhost/127.0.0.1, crea un database usa-e-getta, esegue due installazioni dello script (idempotenza), verifica giurie, privilegi di `anon`, RLS, conteggi, MVP, stagioni e finalizzazione. Non legge Supabase né inventa dati sul sito. La matrice dei browser è distinta da questa prova SQL.

La dicitura **«Serie A, 11ª giornata» nel Giornale rimane invariata**, per decisione espressa di Gianluca; nessun file editoriale è stato toccato.
