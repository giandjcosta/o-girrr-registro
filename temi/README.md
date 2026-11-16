# O Girrr — infrastruttura permanente dei temi evento

16 novembre 2026 · prototipo, **non pubblicato**.

Le due grafiche permanenti restano **Lega** e **Stadio**, con le loro attuali regole e preferenze. Un tema evento è un **livello indipendente** applicato sopra una qualsiasi delle due grafiche, senza modificare l'identità della skin selezionata.

- `data-skin="girrr"` / `data-skin="stadio"`: restano proprietà dell'app esistente.
- `data-event-theme="vice-city"`: selettore separato, gestito da `theme-engine.js`.
- Le variabili CSS dell'evento, gli asset e le componenti decorative sono isolate.
- Nessun accesso a Supabase, sessione, account, calcoli o dati della lega.
- Nessuna pubblicazione, attivazione automatica o modifica del sito vero da questa cartella.
- Un futuro evento si registra nel catalogo con ID univoco; si aggiungono foglio CSS e asset specifici.
- Spegnere il tema elimina l'attributo evento; Lega/Stadio restano inalterate.
- Anteprima manuale: `OGirrrTheme.preview("vice-city")` e `OGirrrTheme.clearPreview()`.
- `OGirrrTheme.activateScheduled()` è intenzionalmente separato: non chiamarlo nella produzione senza approvazione e collaudo dell'evento.
- Se JavaScript fallisce, nessun attributo evento viene applicato e rimane l'interfaccia standard.
- Prima di ogni rilascio: confronto Lega/Stadio × evento on/off, Chromium/WebKit/Firefox, telefono/tablet/desktop, dati e autenticazione invariati, `prefers-reduced-motion`, contrasto, navigazione e rollback.
- Utilizzare asset originali ispirati all'estetica tropicale/neon: evitare loghi e artwork ufficiali non autorizzati.

**Nota importante:** questa cartella contiene soltanto le fondamenta. Non è un restyling completo, non è ancora collegata alle pagine dell'app e non costituisce una preview navigabile certificata.
