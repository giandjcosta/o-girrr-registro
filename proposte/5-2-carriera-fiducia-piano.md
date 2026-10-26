# Carriera e Fiducia — evoluzione 5.2

Stato: **solo Anteprima**. La UI si può provare; la persistenza dei premi non è stata attivata in Supabase e nessun Fantacredito reale è stato attribuito.

## 1. Fiducia del presidente

- L'arco ha una track grigia da 0 a 100 e un tratto colorato che termina **esattamente al punteggio**. Il gradiente è fisso (rosso/arancio/giallo/verde/turchese/blu) e troncato via `stroke-dasharray`: a 52 non può comparire il tratto verde/blu della parte successiva.
- Senza pallino. Il numero al centro usa un breve flip stile cartellino; il valore e il riempimento si interpolano ~520 ms. Cambi rapidi di squadra cancellano l'animazione precedente. `prefers-reduced-motion: reduce` annulla le animazioni.
- La formula di fiducia temporanea attribuisce da giornata 23 a 34 bonus e malus simmetrici per tutte le squadre, fino a ±11 punti, proporzionati allo scarto rispetto alle attese iniziali e alla giornata. Per ogni squadra lo scarto è `(posizione attesa - posizione attuale)`, ponderato dalla giornata: un'outsider sopra le attese guadagna fiducia; una Big sotto le attese ne perde. Limite 98 invariato. Questo non è reputazione permanente: la fiducia può scendere quando cambiano i risultati.

## 2. Premi reputazione e sponsor

**Proposta economica:**
- Obiettivo del presidente verificato: +2 reputazione permanente, fino a +3 per traguardo eccezionale come il titolo finale (da definire esplicitamente per tipologia).
- Obiettivo sponsor verificato: +1 reputazione permanente e **50, 75, 100 o 125 Fantacrediti** secondo difficoltà, una sola volta.
- La sezione Carriera mostra una **simulazione** degli eventuali premi, etichettata come non accreditata. Non mostra saldo reale né dichiara di aver salvato reputazione.

**Dati reali verificati (sola lettura):**
- Supabase Girrr contiene `public.toto_conti` (crediti iniziali predefiniti 500) e `public.toto_movimenti`.
- Non esiste ancora una tabella dedicata ai punti reputazione/riconoscimenti.
- Il sito vero ha il workflow `riepilogo.yml` che parte da modifiche a `data.json` e da lancio manuale; un futuro controllo premi può agganciarsi a un evento dati ufficiali (o a uno scheduler), non al render della pagina.

**Schema backend preparato, NON eseguito:** `proposte/5-2-carriera-premi-schema.sql`.
- Registro privato dei premi con chiave univoca `(stagione, allenatore_id, obiettivo_key)`.
- `allenatore_id` dev'essere persistente anche cambiando squadra: non usare semplicemente il nome squadra.
- Routine transazionale: nuovo evento nel ledger → credito Totogirrr → movimento contabile. Se già esiste l'evento, nessuna seconda ricompensa; se manca il conto, rollback.
- Esecuzione solo server/amministratore dopo verifica dell'obiettivo sui risultati ufficiali alla giornata giusta. Mai credere a uno stato `Fatto` passato dal browser; niente credenziali privilegiate nel frontend.

### Lavori necessari prima dell'attivazione dei premi reali
1. Concordare identificativo allenatore stabile e i casi di trasferimento squadra / cambio allenatore.
2. Definire il momento preciso di consolidamento per ogni obiettivo (giornata 8/10/34 o fine stagione) e i casi in cui lo storico manca.
3. Definire gli importi per tipologia, cap annuale dei Fantacrediti, trattamento delle stagioni passate e verifica retroattiva.
4. Verificare il servizio affidabile che osserva `data.json` o il riepilogo (GitHub Actions server-side, oppure una Edge Function pianificata); custodire i segreti lato server.
5. Testare in transazione il doppio trigger, il rollback, il movimento contabile, il passaggio di stagione e la modifica del risultato.
6. Solo allora applicare la migrazione a Supabase e collegare la UI, con autorizzazione esplicita di rilascio.

Nessuna modifica al database è stata fatta durante questa attività.

### Revisione premi sponsor, 26 ottobre 2026
- Premio minimo **50 Fantacrediti** per obiettivo semplice su singola prestazione.
- **75** per obiettivi ripetuti di rendimento su più giornate.
- **100** per obiettivi di classifica con scadenza alla 10ª giornata.
- **125** per migliorare il piazzamento finale dell'anno precedente.
- Le cifre restano **simulate**, non effettuare accrediti finché il ledger privato non è approvato e testato.
