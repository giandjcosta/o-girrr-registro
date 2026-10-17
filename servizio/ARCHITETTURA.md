# Architettura

## Com'è oggi
- Pagine statiche su GitHub Pages (`girrr/*.html`) che leggono `data.json`.
- Curva su Supabase (una tabella di post e funzioni RPC).
- I dati della lega arrivano da file aggiornati a mano o con script.

## Cosa serve per più leghe
1. **Configurazione per lega** (`leghe/<id>/config.json`): nome, stagione, squadre, allenatori, colori, loghi, regole (Totogirrr sì/no, Carriera sì/no).
2. **Dati per lega** (`leghe/<id>/data.json` o tabelle): classifica, calendario, risultati.
3. **Identità**: Supabase Auth con email e link magico. Ruoli: proprietario, allenatore, ospite.
4. **Curva condivisa**: un'unica tabella di post con `lega_id` e `autore`; il feed globale li mostra tutti, quello della lega solo i suoi.
5. **Permessi**: ogni tabella protetta da regole sulle righe (RLS), così nessuno legge o scrive dove non deve.

## Cosa va separato dal sito attuale
- Tutto il testo "O Fant A Girrr" scritto dentro le pagine (titoli, Albo, storia).
- I contenuti satirici e la storia della lega: restano nella lega, non nel motore.
- I dati personali degli allenatori.

## Come arrivano i dati di una lega (punto delicato)
Oggi li sappiamo prendere dal gestionale della lega. Per un servizio a più leghe non si può contare su leggere quel sito: ci sono condizioni d'uso e può cambiare senza preavviso. Opzioni da valutare:
- il proprietario carica un export o incolla i risultati;
- un modulo di inserimento semplice per giornata;
- un accordo con chi fornisce i dati, se esiste.
