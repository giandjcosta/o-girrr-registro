# Per ChatGPT · il tuo lavoro entra nella 6.5 (non nella 6.5.1) · Claude, 18 novembre 2026

```
Cambio di Gianluca: quello che stai facendo (animazioni d'ingresso e il resto del prompt PROMPT-CHATGPT-651.md) entra nella 6.5, insieme al lavoro di Claude. La 6.5 è già pronta nella PR #23 del sito (ramo claude/65-pubblicazione), NON ancora unita: Gianluca la unisce solo quando ha provato tutto, ingresso compreso.

Come consegnare, esattamente:
1. Parti dal ramo del registro claude/65-uscita (ultimo commit): git fetch origin claude/65-uscita && git checkout -b chatgpt/65-entrata origin/claude/65-uscita
2. Tutto il tuo lavoro sta in file NUOVI dentro temi/notte-tropicale/ (entrata.css, entrata.js, la locandina .webp) più UNA riga in fondo a temi/notte-tropicale/notte-tropicale.js che carica entrata.js solo nella Home con la skin accesa, e i nomi dei file aggiunti all'elenco FILE di rilascio/r65/evento.py e di temi/notte-tropicale/lab.py. Non riscrivere notte-tropicale.css, non toccare temi/evento-loader.js (contiene la regola fissa dell'avviso in cima alla Home e le date 19/11 00:00 → 28/11 00:00).
3. Le correzioni alle pagine del sito (Condividi in Coppa, titolo della classifica, Giro di boa) vanno in rilascio/r65/ritocchi-patches.json, come nuove coppie [testo esatto prima, testo esatto dopo], perché ritocchi.py le applica già sopra la 6.5. Prova sempre: due esecuzioni di fila, la seconda dice «File cambiati: 0».
4. Prova sulla copia (comandi nel prompt 6.5.1, sezione 1 e 4): copia di gh-pages → applica.py → evento.py → ritocchi.py → prove. Copertina: visibile entro 0,5 s, sparita entro 3 s, una volta al giorno, tocco per chiuderla, «riduci movimento» rispettato, mai appesa, niente scorrimento laterale a 320 px, nessun errore in console.
5. Push del ramo chatgpt/65-entrata e scrivi a Gianluca: «pronto per Claude». NON aprire PR verso gh-pages e non toccare claude/65-pubblicazione: l'unione nella PR #23 la fa Claude, che rilancia gli script sulla copia del sito, riprova tutto e aggiorna il link di prova.
Gli altri compiti (Radio e video della giornata 8) restano una PR separata verso main del registro, come scritto nel prompt 6.5.1.
```
