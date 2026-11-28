# Elenco delle prove

Regole in `REGOLE-LAVORO.md`, sezione 12 (Gianluca, 28 novembre 2026). Una riga per prova: file · cosa controlla · versione · stato.
Stati: **In uso** (si lancia per la versione in corso o prima dei rilasci che toccano quelle pagine) · **Da verificare** (prima stesura automatica del 28 novembre: va controllata e passata a «In uso» o «Archivio») · **Archivio** (spostata in `prove/archivio/`, si cancella alla versione grande con il «Vai» di Gianluca).
Chi aggiunge una prova aggiunge la sua riga. Prima stesura generata dai commenti in testa ai file: dove la descrizione manca va scritta.

| File | Cosa controlla | Versione | Stato |
|---|---|---|---|
| `blocca_scritture.js` | Blocco delle scritture nel database per le prove automatiche (Claude, 12 novembre 2026). |  | Da verificare |
| `browser_certificato.js` | Firefox usa un profilo NSS con la CA del proxy, senza disattivare TLS. |  | Da verificare |
| `collaudo_55_browser.js` | !/usr/bin/env node | 5.5 | Da verificare |
| `collaudo_anteprima_52.py` | Verifica elementi Carriera della 5.2 nel Lab e nelle due Anteprime. | 5.2 | Da verificare |
| `collaudo_anteprima_53_browser.py` | Anteprima 5.5: controlla le due grafiche su pagine reali, senza scrivere al sito. | 5.3 | Da verificare |
| `collaudo_chatgpt_31_browser.py` | Browser 320px e prova della bio Curva su un turno aggiunto soltanto in memoria. |  | Da verificare |
| `collaudo_fiducia52_browser.py` | Nell'app si può vedere solo la propria squadra; il cambio è uno strumento di prova. |  | Da verificare |
| `collaudo_fiducia_universale52.js` | Verifica formule universali Fiducia e premi sponsor, senza DB writes. |  | Da verificare |
| `collaudo_milestone_ufficiali52.js` | Verifica che la milestone rispetti solo i risultati con cinque incontri conclusi e consecutivi. |  | Da verificare |
| `collaudo_preview52_totogirrr_milestone.js` | Totogirrr finto dell'anteprima: squadra e premi dalla Carriera, niente login, niente database |  | Da verificare |
| `collaudo_produzione52_browser.py` |  |  | Da verificare |
| `collaudo_tabellone_annuario_browser.py` | Collaudo di Tabellone (Lega/Stadio) e Annuario (Lab), senza scritture remote. |  | Da verificare |
| `esporta_preview_tifosi.py` | Esporta la preview locale in un HTML navigabile, senza commit o hosting. |  | Da verificare |
| `esporta_ramificazioni.py` | Copia di revisione autonoma della mappa; non è il file da pubblicare sul sito. |  | Da verificare |
| `foto_giro_di_boa.js` | Foto esportate dall'interfaccia reale del Lab, senza condividere verso applicazioni esterne. |  | Da verificare |
| `galleria_tifosi.py` | Raccoglie le foto effettive del collaudo per la revisione, senza modificarle. |  | Da verificare |
| `prova-562-schermi.js` |  |  | Da verificare |
| `prova_53_casi_limite.py` | Casi controllati per giorni parziali, record e sicurezza delle metriche. | 5.3 | Da verificare |
| `prova_53_completa.py` | Percorsi e regressioni della 5.5 completa: dati pubblici, RPC isolate, cinque viewport. | 5.3 | Da verificare |
| `prova_60.js` | Prova completa della 6.0 sulla copia di rilascio (Claude, 12 novembre 2026). | 6.0 | Da verificare |
| `prova_601.js` | Prova della 6.0.1 (Claude, 13 novembre 2026) sulla copia di gh-pages con rilascio/r601/applica.py, servita su localhost:8771. | 6.01 | Da verificare |
| `prova_602.js` | Prova della 6.0.2 (Claude, 13 novembre 2026): condivisione singola nelle pagine e scelta della squadra nel Tabellone. | 6.02 | Da verificare |
| `prova_611.js` | 6.1.1 · Copie locali, tre motori reali, nessuna scrittura o invio. | 6.11 | Da verificare |
| `prova_cambio_versione_registro.py` | Un nuovo rilascio aggiorna tutti gli ingressi senza modificare il Laboratorio. |  | Da verificare |
| `prova_campo_62.js` | ChatGPT 6.2: QA della COPIA locale, mai del database vero. | 6.2 | Da verificare |
| `prova_campo_contenuti.py` | Campo: risultato, partite da giocare, identità Lega/Stadio della pagina e Curva chiara/scura. |  | Da verificare |
| `prova_cartellini_602.js` | Prima apertura reale, ripetizione, riduzione del movimento e G1 visibile. | 6.02 | Da verificare |
| `prova_cerca_pubblica.js` | Forza Cerca a montarsi dopo il render: nessuna quarta scheda pubblica per errore. |  | Da verificare |
| `prova_chiave_premi.py` | Nessun contatto con Supabase: chiavi finte e trasporto HTTP simulato. |  | Da verificare |
| `prova_condividi_radio_602.js` | Radio 6.0.2: centratura rispetto al lettore e condivisione simulata, senza invii o scritture reali. | 6.02 | Da verificare |
| `prova_conferenze.js` | Prova delle novità delle conferenze (Claude, 10 novembre 2026): conferenza bloccata dopo la pubblicazione, conferenza dell'avversario |  | Da verificare |
| `prova_cornice_archivio.py` | Versione leggibile, interruttore su più pagine e schede dell’Archivio. |  | Da verificare |
| `prova_cronache_compatibilita.py` | La Radio attuale, letta dal Registro, non cambia senza attivazione esplicita. |  | Da verificare |
| `prova_cronache_integrate.py` | Pipeline preparatoria locale: post/commenti, testo Radio e adattatore PDF. |  | Da verificare |
| `prova_cronache_lab_browser.py` | Dal Lab al dossier e al PDF: sola lettura locale, cinque larghezze. |  | Da verificare |
| `prova_cronache_pacchetto.py` | Prova offline del pacchetto: ripetibilità, attesa e protezione degli input. |  | Da verificare |
| `prova_curva_banca.js` | Curva · Nuovi personaggi, frasi e immagini (Claude, 12 novembre 2026). |  | Da verificare |
| `prova_curva_condividi.js` |  |  | Da verificare |
| `prova_curva_cuori.js` |  |  | Da verificare |
| `prova_curva_ferma.js` | Curva aggiornata pezzo per pezzo e Notifiche divise (Claude, 12 novembre 2026). |  | Da verificare |
| `prova_curva_os.js` | Curva · Stile e movimenti di iPhone e di Android (Claude, 12 novembre 2026). |  | Da verificare |
| `prova_curva_performance_611.js` | Confronto locale ripetibile: PRIMA=f619634 per la 6.1, senza PRIMA per la proposta. DB simulato. | 6.11 | Da verificare |
| `prova_derby_schede.js` | Derby in tre schede (6.0.1, Claude, 13 novembre 2026): Derby della Lega, Le rivalità, Classifica dei Derby. |  | Da verificare |
| `prova_emoji_versioni.js` | Versioni: nessuna emoji da sola su una riga, su 16 schermi (Claude, 9 novembre 2026). Serve la copia di gh-pages con rilascio56.py su http://localhost:8771/o-fa |  | Da verificare |
| `prova_filtri_panorama.py` | Filtri combinati, date di Roma e panoramica completa nel portale del Registro. |  | Da verificare |
| `prova_fluido_lette.js` | Versioni: cambio Messaggio/Changelog fluido; Notifiche: lette rimpicciolite (Claude, 9 novembre 2026). Serve una copia di gh-pages con versioni.js e notifiche-l |  | Da verificare |
| `prova_giornale_cronaca_pdf.py` | Prova completa: calendario → post/commento → copione → testi → PDF locale. |  | Da verificare |
| `prova_giro_di_boa.py` | Prove dei fatti del bilancio e del testo Radio, senza rete né voci a pagamento. |  | Da verificare |
| `prova_giro_di_boa_browser.js` | Matrice reale 16 schermi × Chromium/WebKit/Firefox. Solo copie locali. |  | Da verificare |
| `prova_giro_di_boa_filtri_61.js` | Periodi, competizione e contenuti coerenti: motori reali, schermi emulati, nessuna scrittura. | 6.1 | Da verificare |
| `prova_giro_di_boa_grafica.js` | Verifica la grafica effettivamente disegnata: centratura dei glifi e palette separate dalle bande. |  | Da verificare |
| `prova_giro_di_boa_lab.js` | Lab navigabile, specchio con service worker e riapertura senza rete. Nessuna voce generata. |  | Da verificare |
| `prova_giro_di_boa_tabellone_61.js` | Il bilancio aperto dal Tabellone conserva la competizione vista, anche per l'ospite. | 6.1 | Da verificare |
| `prova_giro_di_boa_tv.js` | Identità Tizen e schermo TV emulati; non equivale a Samsung Internet su dispositivo. |  | Da verificare |
| `prova_home_notifiche55.py` | Home reale, notifiche e navigazione: fonti pubbliche/risposte personali controllate. |  | Da verificare |
| `prova_home_unica55.py` | Due bozze, due skin, cinque larghezze: dati del calendario e nessun database. |  | Da verificare |
| `prova_infortuni_spogliatoio.py` | Prova: infortuni e squalifiche nello Spogliatoio (Chi scambiare, Mercato Scambi). |  | Da verificare |
| `prova_ingresso_anteprima_53.py` | Regressione della cornice storica 5.5; l'ingresso corrente è provato da prova_registro_corrente.py. | 5.3 | Da verificare |
| `prova_integrazione60_browser.py` | 6.0 di Claude + modulo tifosi + Ramificazioni. RPC simulate, nessuna richiesta al DB vero. |  | Da verificare |
| `prova_link_anteprima.py` | I collegamenti ereditati dal Lab puntano al Registro, senza cambiare le pagine reali. |  | Da verificare |
| `prova_moviola.py` | Prova con dati finti del post Moviola di Girrr Sport (passo 4). Non tocca il database né il sito: lavora in una cartella temporanea |  | In uso |
| `prova_moviola_browser.js` | Uso: servire il sito di oggi su :8001, il candidato al rilascio su :8002 (cartelle con dentro o-fant-a-girrr/) e il registro su :8003, poi |  | In uso |
| `prova_moviola_gol.py` | Prova con dati finti degli episodi nuovi della Moviola: gol decisivo, assist decisivo, decisivo dalla panchina, limite di 4 |  | In uso |
| `prova_mvp60_db.py` | Prova lo schema soltanto su Postgres locale o su un contenitore di test esplicito. |  | Da verificare |
| `prova_navigazione_53.py` | Home → Tabellone → Campo → Home → Albo, nelle due skin e cinque viewport. | 5.3 | Da verificare |
| `prova_nomi.js` |  |  | Da verificare |
| `prova_notifiche_destinazioni55.py` | Clic su tutta la scheda → contenuto preciso; RPC controllate, nessuna scrittura. |  | Da verificare |
| `prova_pillola_home.js` |  |  | Da verificare |
| `prova_portale_registro.py` | Portale completo: vecchi indirizzi, menu persistente, grafica e sola lettura. |  | Da verificare |
| `prova_rami_interattivi.js` | Prova di lab/prove-grafiche/rami-alternative.html (Claude, 13 novembre 2026): in ogni vista tocca un pallino e controlla zoom, dettagli e link ai commit. Uso: s |  | Da verificare |
| `prova_rami_tre_viste.js` | Ramificazioni (Claude, 14-15 novembre 2026): la pagina principale è rami.html, a tutta larghezza nel portale del Registro; |  | Da verificare |
| `prova_ramificazioni.py` | Prova la ricostruzione su veri repository temporanei, senza rete. |  | Da verificare |
| `prova_ramificazioni_browser.py` | Ramificazioni: tutti i rami, selezione collettiva e leggibilità senza scorrimento laterale. |  | Da verificare |
| `prova_redazione.js` | Prova della redazione di Girrr Sport nella Conferenza (Claude, 11 novembre 2026, versione 5.8). |  | Da verificare |
| `prova_redazione.py` | Prova della redazione di Girrr Sport (Claude, 11 novembre 2026, versione 5.8): controllo dei testi e giudizi nei calcoli. |  | Da verificare |
| `prova_registro_corrente.py` | Versione corrente, archivio, navigazione Lega/Stadio e blocco scritture. |  | Da verificare |
| `prova_rilascio_cronache55.py` | Collegamenti reali del pacchetto, eseguiti solo su copie senza publisher/audio. |  | Da verificare |
| `prova_schermi_56.js` | Prova della 5.6 su 16 schermi (Claude, 9 novembre 2026). Uso: servire una copia di gh-pages con rilascio56.py applicato su http://localhost:8771/o-fant-a-girrr/ | 5.6 | In uso |
| `prova_schermi_conferenze.js` | Novità delle conferenze su 16 schermi (Claude, 10 novembre 2026): Conferenza (con l'avversario), Promesse, Testa a testa, Curva con ?scrivi=. |  | In uso |
| `prova_settimana_ospite.js` | Carriera (Claude, 13 novembre 2026): con la squadra «La mia settimana» prima di «Regole» (ultima voce); da ospite «La settimana delle squadre» con le 10 squadre |  | Da verificare |
| `prova_sincronizzazione.py` | Controlla versione unica, archivio completo e protezione della copia pubblicata. |  | Da verificare |
| `prova_spogliatoio_lazy.js` | Test isolati del wrapper lazy (nessuna dipendenza npm). |  | Da verificare |
| `prova_tabellone_campo_browser.py` | Prove visuali 320 / 768 / 1280 per Tabellone, Campo e Albo. Nessuna scrittura al sito. |  | Da verificare |
| `prova_tifosi60.py` | Regole server/editoriali su dati reali conservati; nessun servizio remoto. |  | Da verificare |
| `prova_tifosi_browser.py` | Preview integrata: tre motori reali, sedici profili e interazioni locali. |  | Da verificare |
| `prova_tifosi_esportazione.py` | Collauda la copia monofile effettivamente consegnata, separatamente dal server. |  | Da verificare |
| `prova_tifosi_model.js` |  |  | Da verificare |
| `prova_zone_classifica.py` | Risultati completi, scelte editoriali, priorità e assenza di duplicazioni. |  | Da verificare |
| `rete_browser.py` | Rete browser verificata con CA del runtime; cache solo per letture pubbliche. |  | Da verificare |
| `server_range.py` | Server locale delle prove: supporta anche i Range di audio e video. |  | Da verificare |
| `v62/albo-browser.cjs` | Browser Albo 6.2: stesso contratto della RPC v62_albo, nessuna rete Supabase. | 6.2 | Da verificare |
| `v62/attendi.cjs` | Attende soltanto un server locale; non invia scritture. | 6.2 | Da verificare |
| `v62/check621.py` | 6.2.1: verifiche statiche su checkout temporanei, mai su produzione/Supabase. | 6.2 | Da verificare |
| `v62/foto.cjs` |  | 6.2 | Da verificare |
| `v62/funzioni.cjs` |  | 6.2 | Da verificare |
| `v62/native-browser.cjs` |  | 6.2 | Da verificare |
| `v62/native-network.cjs` |  | 6.2 | Da verificare |
| `v62/native-server.cjs` | Server dei collaudi: soltanto file locali e Postgres WASM locale, mai Supabase. | 6.2 | Da verificare |
| `v62/pdf-originale.py` | PDF su copie isolate di giornate reali, confronto con renderer originale a quattro pagine. | 6.2 | Da verificare |
| `v62/portieri.cjs` |  | 6.2 | Da verificare |
| `v62/postgres.py` | Test su PostgreSQL locale con sessioni distinte; nessuna connessione a Supabase. | 6.2 | In uso |
| `v62/postgres_albo.py` | Albo 6.2: prove SQL su PostgreSQL LOCALE, mai su Supabase. | 6.2 | In uso |
| `v62/postgres_cambio.py` | Claude, 15 novembre 2026: «Cambia il mio voto» su PostgreSQL locale (mai Supabase). | 6.2 | In uso |
| `v62/postgres_personaggi.py` | Claude, 16 novembre 2026: voti dei personaggi dell'MVP che arrivano durante la settimana (sql/mvp-personaggi-621.sql). | 6.2 | In uso |
| `v62/preview.cjs` | Collaudo della preview esportata: le preferenze vere del browser non cambiano. | 6.2 | Da verificare |
| `v62/render-originale.py` |  | 6.2 | Da verificare |
| `v62/server.cjs` | ')[1].split(' | 6.2 | Da verificare |
| `v62/sql.cjs` |  | 6.2 | Da verificare |
| `v62/testi.py` |  | 6.2 | Da verificare |
| `v623/prova_esci623.js` | 6.2.3 · Pillola «Esci» in fondo alla Home (Claude, 16 novembre 2026). | 6.2 | Da verificare |
| `v623/prova_toto623.js` | 6.2.3 · Totogirrr su 16 schermi, Lega e Stadio (Claude, 16 novembre 2026). | 6.2 | Da verificare |
| `v624/prova_624.js` | 6.2.4 · Prova delle correzioni (Claude, 17 novembre 2026). Uso: node prove/v624/prova_624.js URL_DEL_LAB_INTEGRATA | 6.2 | Da verificare |
| `v65/prova_fiducia_65.js` | Fiducia del presidente in Carriera (iPhone 13): opacità massima del numero nascosto durante il giro e foto della sequenza. | 6.5 | In uso |
| `v65/prova_fluidita_65.js` | Dettaglio: Conferenze stampa (salto) e opacità solo dei blocchi grandi e visibili, con il valore di partenza. | 6.5 | In uso |
| `v65/prova_radio_speciale.py` | Collaudo puramente testuale della Radio 6.5: NON genera voci o audio. | 6.5 | In uso |
| `v65/prova_schermi_65.js` | 6.5 nel Lab: pagine principali su tutti gli schermi, con e senza tema. Controlla errori nuovi e scorrimento laterale. | 6.5 | In uso |
| `v66/prova_scambi_app.py` | Claude, 24 novembre 2026: prove di calcoli/scambi_app.py (scambi nell'app, 6.6) senza database (--prova) e senza toccare il sito. | 6.6 | In uso |
| `v66/prova_scambi_sql.py` | Claude, 24 novembre 2026: prove di sql/scambi-66.sql (scambi nell'app, 6.6). | 6.6 | In uso |
| `v66/prova_schermi_66.js` | Prova della 6.6 su 16 schermi (Claude, 24 novembre 2026), sul Lab: Spogliatoio › Mercato Scambi con le richieste, | 6.6 | In uso |

Totale: 119 prove (16 in uso, 103 da verificare). Gli altri file di `prove/` sono dati di prova, risultati e registri.
