# Carriera a tab: piano di lavoro (Claude, ChatGPT, Grok)

La Carriera passa da pagina unica a **4 tab** (decisione di Gianluca del 30 ottobre: la Cassa non va sotto Carriera). Ognuno vede **solo la propria squadra** (decisione di Gianluca): nell'Anteprima e nel sito vero non c'è selettore; il selettore resta solo nel Lab per le prove. Sopra i tab: nome della squadra e bolla del premio sponsor.

| Tab | Contenuto | Chi | Stato |
|---|---|---|---|
| **Panoramica** | Fiducia del presidente (arco), riassunto obiettivi (N su 4 raggiunti), Reputazione e sponsor | Claude | fatto |
| **Obiettivi** | Obiettivi della stagione con linea del tempo delle scadenze, obiettivi di Coppa, premio sponsor | ChatGPT | da fare |
| **Fiducia** | Come nasce l'aspettativa, Come cambia la fiducia con il calendario, grafico «Fiducia giornata per giornata», Fiducia in lega | Claude | fatto |
| **Storia** | Carriera dell'allenatore: stagioni, titoli, grafico delle posizioni, racconto | Grok | da fare (c'è una versione base) |

## Come si lavora
1. **Base comune:** il ramo `claude/review-ai-changes-test-ui9gjy` contiene già i tab, le correzioni 5.2 e due **zone riservate**: una per ChatGPT e una per Grok. Si parte da lì, **non** da `main`.
2. ChatGPT e Grok lavorano **in parallelo**, ognuno sul suo ramo, toccando **solo la propria zona** in `lab/index.html` e **solo il proprio paragrafo** in `STATO.md`. Così le unioni non vanno in conflitto.
3. Ognuno prova, aggiorna il suo paragrafo in STATO.md e apre una Pull Request **verso `claude/review-ai-changes-test-ui9gjy`**.
4. Claude unisce le due PR, rigenera l'Anteprima, prova tutto e lo segnala in STATO.md.
5. Gianluca prova nella preview del Lab. Col suo «vai»: unione a `main` del registro → rilascio 5.2 sul sito vero.

## Contratto delle zone
In `lab/index.html`:

```js
/* === TAB CARRIERA: OBIETTIVI (ChatGPT) === */
function vCarObiettivi(t,C){ ... }
/* === FINE TAB OBIETTIVI === */

/* === TAB CARRIERA: STORIA (Grok) === */
function vCarStoria(t){ ... }
/* === FINE TAB STORIA === */
```

- `t` è il nome della squadra selezionata. La funzione **restituisce una stringa HTML** e non tocca il DOM.
- Si scrive **solo tra i due commenti della propria zona**. Funzioni di aiuto dentro la zona, con prefisso `ob_` (ChatGPT) o `st_` (Grok).
- Eventi: `document.addEventListener('click'|'change', …)` dentro la zona, filtrando su attributi propri (`data-ob…` o `data-st…`), poi `render()`.
- Stato locale: `S.ob` (ChatGPT) e `S.st` (Grok), già creati come oggetti vuoti.
- CSS: stili inline o classi con prefisso `.ob-` / `.st-`, mai regole globali nuove.
- **Mai modificare a mano** `anteprima/index.html` e `anteprima/attuale.html`: si rigenerano con `python3 anteprima/build.py`. Il workflow «Anteprima Totogirrr 5.2 QA» fallisce se non corrispondono al Lab.

---

## Prompt per ChatGPT (incollalo così)

```
Lavora nel repository giandjcosta/o-girrr-registro.
Prima leggi AGENTS.md, STATO.md e proposte/carriera-tab-piano.md.

RAMO
- Parti dal ramo claude/review-ai-changes-test-ui9gjy (NON da main): git fetch origin && git checkout -b chatgpt/carriera-tab-obiettivi origin/claude/review-ai-changes-test-ui9gjy
- Ogni commit inizia con "ChatGPT:". Niente push forzati, niente push su main o su altri rami.

COMPITO: tab «Obiettivi» della Carriera
Riscrivi solo la funzione vCarObiettivi(t,C) in lab/index.html, tra
/* === TAB CARRIERA: OBIETTIVI (ChatGPT) === */ e /* === FINE TAB OBIETTIVI === */.
Non modificare nessun'altra riga del file.

Cosa ricevi:
- t = squadra selezionata
- C.o = 4 righe obiettivi [tipo, fonte, titolo, percentuale 0-100, stato]: 0) posizione finale, 1) vittorie entro l'8ª, 2) Coppa (OB[t].cp, stato «Da giocare»), 3) sponsor. tipo = 'P' per il presidente, null per lo sponsor; fonte = "Presidente" o nome dello sponsor
- C.e1, C.e2, C.e4 = esiti [percentuale, stato] (posizione finale, vittorie entro l'8ª, sponsor)
- C.sp = sponsorDi(t) {nome, testo, pct, stato, dl (giornata di scadenza), ok}
- C.wn = vittorie richieste entro l'8ª
- C.premio = premioSponsor(t) {sponsor, testo, crediti, ok}, C.riscosso = true se già riscosso
Funzioni utili già nel file: OB[t] (.cp e .ca = obiettivi di Coppa), gioc(), aGiornata(n,t), GTOT, CL, SPIMG, D.img.sp2, esc().

Cosa deve mostrare il tab, nell'ordine:
1. Card «Linea del tempo»: scadenze alle giornate 2, 6, 8, 10, 18, 26, 34. Pallino pieno = giornata già giocata (gioc() oppure CL con tutti i risultati), pallino vuoto = futura, evidenziata la prossima. Sotto ogni scadenza, i nomi brevi degli obiettivi che si decidono lì: vittorie entro l'8ª → 8; sponsor → C.sp.dl (10 o 34); posizione finale → 34. Su schermi stretti la linea scorre DENTRO la card (overflow-x:auto), mai la pagina.
2. Card «Obiettivi della stagione»: le righe 0, 1 e 3 di C.o, ognuna con logo (SPIMG[fonte] || D.img.sp2) oppure etichetta «Pres.», titolo, fonte, barra .pbar con la percentuale, etichetta di stato (.tag, classe "o" se Fatto) e scadenza («entro la 8ª», «alla 10ª», «a fine stagione»). Il titolo non deve mai andare a capo parola per parola: a ≤700 px l'etichetta va sotto il titolo (flex-wrap).
3. Card «Champions Cup»: la riga 2 di C.o (obiettivo del presidente, OB[t].cp) e OB[t].ca (obiettivo dell'allenatore), con lo stato della riga 2.
4. Card «Premio sponsor»: C.premio.sponsor, C.premio.testo, C.premio.crediti crediti Totogirrr, stato «Riscosso» (C.riscosso) / «Da riscuotere» (C.premio.ok) / «In corso». Se «Da riscuotere», metti un link con lo stesso indirizzo della bolla: toto52Url(t,(/\/lab\//.test(location.pathname)?'../lab/':'')+(location.pathname.split('/').pop()||'index.html')+'#carriera'). Non inventare altri premi o importi.

REGOLE
- Grafica: classi esistenti (.card, .ob, .pbar, .tag, .row, .grow, .sm, .mut, .num, .btn). Niente librerie, niente fetch nuovi, niente Supabase.
- Testi in italiano, come un campionato vero, maiuscola iniziale. Mai «fantacalcio», «fantapunti» o disclaimer tipo «simulazione/dati finti». Mai scommesse.
- Dopo ogni modifica: python3 anteprima/build.py, poi committa anche anteprima/index.html e anteprima/attuale.html generati.

PROVE (obbligatorie, prima della PR)
- node prove/collaudo_preview52_totogirrr_milestone.js
- node prove/collaudo_fiducia_universale52.js
- python3 prove/collaudo_anteprima_52.py
- python3 anteprima/build.py && git diff --exit-code anteprima/  (deve uscire senza differenze)
- Nel browser (python3 -m http.server dalla cartella del repo), a 320, 375 e 1280 px, su lab/index.html#carriera, anteprima/attuale.html#carriera e anteprima/index.html#carriera: apri il tab Obiettivi con almeno 3 squadre (Oranje VC, Grodah, The Blue brothers): nel Lab col selettore, nell'Anteprima aggiungendo ?come=Grodah all'indirizzo (ognuno vede solo la propria squadra, non c'è selettore). Nessuno scorrimento laterale della pagina (document.documentElement.scrollWidth ≤ larghezza), console senza errori. Prova anche ?premi=prova#carriera per vedere «Da riscuotere».

STATO.md
Scrivi SOLO sotto il titolo «### Tab Obiettivi (ChatGPT)», dentro la sezione «## Carriera a tab — resoconti», sostituendo la riga «In attesa.». Max 6 righe: cosa hai fatto, prove eseguite con esito, cosa non hai potuto provare. Non toccare altre parti di STATO.md.

CONSEGNA
Apri una Pull Request da chatgpt/carriera-tab-obiettivi verso claude/review-ai-changes-test-ui9gjy (NON verso main), titolo «ChatGPT: tab Obiettivi della Carriera», con le prove fatte e quelle non fatte.
```

## Prompt per Grok (incollalo così)

```
Lavora nel repository giandjcosta/o-girrr-registro.
Prima leggi AGENTS.md, STATO.md e proposte/carriera-tab-piano.md.

RAMO
- Parti dal ramo claude/review-ai-changes-test-ui9gjy (NON da main): git fetch origin && git checkout -b grok/carriera-tab-storia origin/claude/review-ai-changes-test-ui9gjy
- Ogni commit inizia con "Grok:". Niente push forzati, niente push su main o su altri rami.

COMPITO: tab «Storia» della Carriera
Riscrivi solo la funzione vCarStoria(t) in lab/index.html, tra
/* === TAB CARRIERA: STORIA (Grok) === */ e /* === FINE TAB STORIA === */.
Non modificare nessun'altra riga del file. Oggi c'è una versione base (elenco stagioni): sostituiscila.

Dati già nel file:
- mgrsOf(t) = elenco allenatori della squadra (di solito uno; «The Blue brothers» ne ha due: Leanzino e Mario, mostrali entrambi)
- HIST[allenatore] = righe [stagione, posizione, numero squadre], es. ["2024/25", 5, 10]
- PRE = righe [stagione, squadra vincitrice, allenatore] delle stagioni prima del 2021/22 (null = sconosciuto)
- fascia(t) → 'Big' | 'Emergente' | 'Outsider'; histScore(t) → punteggio storico 0-100; OB[t].pres = obiettivo di quest'anno
- esc() per il testo, var(--gold), var(--mute), var(--line), var(--ink) per i colori

Cosa deve mostrare il tab, nell'ordine (per ogni allenatore della squadra):
1. Card intestazione: nome allenatore, fascia attuale, «Storia: N su 100» (Math.round(histScore(t))), numero di stagioni, titoli e podi.
2. Card «Posizioni stagione per stagione»: grafico SVG inline con viewBox e style="width:100%;height:auto". Asse verticale rovesciato (1° in alto, ultimo in basso, scala sul numero di squadre di quella stagione), un punto per stagione con etichetta della stagione sotto, 🏆 o punto dorato per il 1° posto, linea che unisce i punti. Deve stare in 320 px senza scorrimento.
3. Card «Stagioni»: righe dalla più recente: «2024/25 · 5° su 10», con 🏆 per il 1°, 🥈 per il 2° e 🥉 per il 3°.
4. Card «Albo»: titoli da HIST (posizione 1) più quelli in PRE dove l'allenatore compare (confronto senza maiuscole/minuscole e spazi), con l'anno.
5. Un paragrafo di racconto generato dai dati, stile giornale sportivo (es. «Tre podi nelle ultime cinque stagioni e il titolo del 2023/24: Leanzino arriva da favorito.»). Niente frasi inventate che non dipendono dai dati.
Se un allenatore non ha HIST, mostra «Prima stagione in lega» senza errori.

REGOLE
- Grafica: classi esistenti (.card, .row, .grow, .tag, .sm, .mut, .num). Niente librerie, niente fetch nuovi, niente Supabase.
- Testi in italiano, come un campionato vero, maiuscola iniziale. Mai «fantacalcio», «fantapunti» o disclaimer. «Derby» con la D maiuscola se compare. Mai scommesse.
- Dopo ogni modifica: python3 anteprima/build.py, poi committa anche anteprima/index.html e anteprima/attuale.html generati.

PROVE (obbligatorie, prima della PR)
- node prove/collaudo_preview52_totogirrr_milestone.js
- python3 prove/collaudo_anteprima_52.py
- python3 anteprima/build.py && git diff --exit-code anteprima/  (deve uscire senza differenze)
- Nel browser (python3 -m http.server dalla cartella del repo), a 320, 375 e 1280 px, su lab/index.html#carriera, anteprima/attuale.html#carriera e anteprima/index.html#carriera: tab Storia con TUTTE le 10 squadre: nel Lab col selettore, nell'Anteprima aggiungendo ?come=NomeSquadra all'indirizzo (ognuno vede solo la propria squadra, non c'è selettore). Nessuno scorrimento laterale della pagina (document.documentElement.scrollWidth ≤ larghezza), console senza errori.

STATO.md
Scrivi SOLO sotto il titolo «### Tab Storia (Grok)», dentro la sezione «## Carriera a tab — resoconti», sostituendo la riga «In attesa.». Max 6 righe: cosa hai fatto, prove eseguite con esito, cosa non hai potuto provare. Non toccare altre parti di STATO.md.

CONSEGNA
Apri una Pull Request da grok/carriera-tab-storia verso claude/review-ai-changes-test-ui9gjy (NON verso main), titolo «Grok: tab Storia della Carriera», con le prove fatte e quelle non fatte.
```

## Lavoro di Claude
- **Fatto:** impalcatura dei tab, Panoramica, Fiducia (con il grafico «Fiducia giornata per giornata»), correzioni 5.2 (premi veri, Totogirrr legato alla squadra).
- **Dopo le due PR:** unione, `build.py`, prove (test automatici + browser a 320/375/1280 su Lab, Lega e Stadio), resoconto in STATO.md, poi richiesta del «vai» a Gianluca.
- **Rilascio 5.2 sul sito vero (dopo il «vai»):** unione a `main` del registro, poi pacchetto con `rilascio/pacchetto.py`; prima `gh-pages`, poi verifica sul sito vero, poi `main` del sito.
