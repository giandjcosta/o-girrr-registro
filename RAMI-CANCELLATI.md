# Rami da cancellare (19 novembre 2026)

**Stato:** da questa sessione di Claude la cancellazione è bloccata (GitHub risponde 403 a ogni `git push --delete`). Per farla: lancia `bash strumenti/cancella-rami.sh` da un computer con git e accesso a GitHub, oppure cancella i rami dalla pagina *Branches* di ogni repository. Aggiornato il 19 novembre (mattina): dopo le unioni (PR #27, #28, #135-#140) sono superflui anche `claude/65-entrata-pc`, `chatgpt/65-edizione-speciale` (presa la parte buona nella PR #137), `chatgpt/65-tab-uniche-curva-separata` (non serve: la TV si legge già bene), `claude/65-uscita`, `claude/readme-home`, `claude/65-radio-video` e `claude/sincronizza-65`. Restano solo `main` e `gh-pages`.

Pulizia chiesta da Gianluca («Vai» del 19 novembre). Restano: sito `main`, `gh-pages` (e la PR aperta `claude/65-entrata-pc`); registro `main` e `chatgpt/65-edizione-speciale` (PR #129, Radio e video della giornata 8).

Per ricreare un ramo: `git push origin <commit>:refs/heads/<nome>` nel repository giusto.

## o-fant-a-girrr

| Ramo | Ultimo commit | Data | Messaggio |
|---|---|---|---|
| `probe` | `7637d12bb94013c8254b5b5778b2a858ec1510c1` | 2026-10-08 | Esito probe |
| `curva-tieni-post` | `9a7f0e7ba34eada32dde2e4825897cc962e54a05` | 2026-10-22 | Curva: MVP, moviola, sala stampa, record, big match e voti restano per ogni giornata |
| `curva-accettata` | `043e902ba2d5042881462faa9b4f900e8fc9751a` | 2026-10-22 | Curva: controllo dei post nuovi ogni 5 minuti |
| `claude/infortuni` | `f1263a02f330f2f26c78ad27d3f5993bb528cdb4` | 2026-10-25 | Infortuni: aggiornamento da giornali |
| `grok/spogliatoio-lazy` | `d489f8748d4c646e6639e6a321e009c807fb0506` | 2026-10-25 | Grok: lazy loading tab pesanti Spogliatoio (spogliatoio-lazy.js) |
| `chatgpt/regola-autori-commit` | `44a4aecefaf3f06a848a4fea33be7baf2994aad9` | 2026-10-25 | ChatGPT: rende obbligatoria l'identificazione dell'autore nei rami, commit e PR |
| `claude/uscita-g4` | `ddd468889fe8c937b164c08b3a68d8ca972c81a7` | 2026-10-26 | Giornata 4: uscita anticipata di Risultati, Giornale e Coppa su richiesta di Gianluca |
| `chatgpt/staging-20261026-lazy-curva-carriera` | `5105c0bf6d235602d873a2135842034233b20eab` | 2026-10-26 | ChatGPT: integra Curva infinite scroll con paginazione e refresh sicuro |
| `chatgpt/fix-sponsor-card-grid-20261026` | `85f0ca0b048b008841c1f6e99c0fce4e76cc3843` | 2026-10-26 | ChatGPT: corregge markup sponsor e barra obiettivi full width su mobile |
| `chatgpt/fiducia-colori-20261026` | `519a2740097ddb9fbb3cea936f2adf4ebbe95471` | 2026-10-26 | ChatGPT: rende multicolore il semicerchio Fiducia con indicatore del valore |
| `chatgpt/release52-carriera-rewards-milestones` | `e3b5faca57cf0d8b768c38cba949b3fc0e178ee0` | 2026-10-27 | ChatGPT: browser QA Carriera milestone WebKit Chromium |
| `claude/giornata-5` | `7eb00646de6f7433865782d5e267f1b630f36232` | 2026-10-30 | Claude: Giornale n° 5, tabellone e archivio della quinta giornata |
| `claude/radio-automatica` | `341cf945a9286d28c32373003536c2ae3ffba415` | 2026-10-30 | Claude: radio automatica, non parte se manca GEMINI_API_KEY |
| `claude/coppe-simboli-ere-descrizioni-4jn4ss` | `2fce571af90daa2988f0d9617b170863a9c9ced6` | 2026-10-31 | Claude: premi sponsor automatici dopo ogni giornata (ogni due ore, con registro su main) |
| `claude/premi-giornata` | `aba24067efe17f2a4ba4c0714031f8192a63a3aa` | 2026-10-31 | Claude: premi sponsor controllati una volta al giorno invece che ogni due ore |
| `claude/offline-mode-sync-5vmvdd` | `618d6753a9bd22e133eb74ba641511818c52580f` | 2026-11-09 | Claude: AGENTS.md, sul sito la 5.6.1 |
| `claude/curva-sondaggi-chiusi` | `23ff55995da705343cd0e529993dc22464afd1d1` | 2026-11-12 | Claude: Curva, tolte le linee a tutta larghezza sopra e sotto Sondaggi chiusi |
| `chatgpt/controllo-chiave-premi` | `e721990ab0828b6e6a5c1f064327b8c892ebf121` | 2026-11-12 | ChatGPT: permette la diagnosi manuale della chiave senza registrare premi |
| `chatgpt/backend-tifosi-6-0` | `2b927517412587c5ad1fad3d00773c176f84b436` | 2026-11-13 | ChatGPT: esclude la cache Python dagli artefatti server |
| `claude/o-girrr-versione-6-0-mjh4ut` | `bc34e95f3dee82cbc05303ee1175f8007bf596b2` | 2026-11-13 | Claude: AGENTS.md, sul sito la 6.0 |
| `chatgpt/messaggio-60-approvato` | `df52e20a883c0fddaf42c24fd5c3f4cb310989e4` | 2026-11-13 | ChatGPT: aggiorna il messaggio 6.0 approvato da Gianluca |
| `claude/sito-601` | `6a9d187a00de0c82d186037e84a460fff35acd1c` | 2026-11-14 | Claude: AGENTS.md, sul sito la 6.0.1 |
| `chatgpt/rilascio-6-1` | `2536af28e788d3b299e8c7625294099b50a84a1d` | 2026-11-14 | ChatGPT: aggiorna il modulo condiviso anche nelle pagine del Giornale |
| `claude/avvisa-ramificazioni` | `39df3fb2ce79f625074f410435e9122929ce228a` | 2026-11-14 | Claude: avvisa le Ramificazioni del Registro a ogni push, ramo e Pull Request del sito |
| `chatgpt/giro-boa-calcoli-602` | `0873dcc7ca30e8916632b5ac7f8cbcbdaa291985` | 2026-11-14 | ChatGPT: registra la 6.1 pubblicata nelle istruzioni del sito |
| `claude/fervent-thompson-rwlwrh` | `7aaac184331889d76a77b42729c44897fb102712` | 2026-11-15 | Claude: prova della lettura dei cartellini su una copia di data.json (solo log, ramo di prova) |
| `claude/cartellini-voti` | `a44a4bc6954e4f65192b0e13d17bfdaa27a42ccb` | 2026-11-15 | Claude: i voti leggono anche ammonizioni ed espulsioni (data.json), il Giornale non le mostra |
| `chatgpt/r62-rilascio-sicuro` | `432505d542177c2b158225640e584f4bc0c39ecd` | 2026-11-15 | ChatGPT: blocca lo staging se la CI sullo SHA non è completamente verde |
| `release/621-ready` | `93ad1a6e0a9c445dace42a8e8638376227e362df` | 2026-11-16 | O Girrr 6.2.1: cache pagine Stadio |
| `release/621-backend` | `326fea4716a0170b16d7acde3b585364511cba65` | 2026-11-16 | O Girrr 6.2.1: 11 personaggi MVP dalla ottava giornata |
| `claude/totogirrr-ui-responsive-b2pgee` | `f80874037e7966e247ccca719135b6433539d515` | 2026-11-17 | Claude: rilascio 6.2.4 «Spogliatoio e Totogirrr più fluidi», versioni.json · «Vai» di Gianluca |
| `claude/65-pubblicazione` | `547d0382de09ea7e6a3989d3b475794efbea7e09` | 2026-11-18 | ChatGPT: conserva la quarta scheda Numeri nel Tabellone 6.5 |
| `chatgpt/65-1-fix-home-campo` | `c297a732606cbd25baa8966375e7003821c1fc62` | 2026-11-18 | ChatGPT: conferma spostamento punteggi di 18px nelle sezioni Squadre |
| `claude/65-numeri` | `5e7d22d2f3f907c1ac6ddec9e840d15994e859d7` | 2026-11-19 | Claude: regole di Numeri accanto a quelle della fila del Tabellone, senza conflitti con le altre PR |
| `claude/65-versioni-schede` | `fe52d072aad46b3793d6647a04caed6c59577ac2` | 2026-11-18 | ChatGPT: integra ritocchi Campo, Versioni e punteggi Squadre nella PR Claude #24 |
| `claude/65-niente-doppio-ingresso` | `ebf629c1b11cf2ea6aa4192d50327e40fc8acb14` | 2026-11-19 | Claude: chiave della prima visita rinnovata, copertina e nuvola tornano una volta su ogni dispositivo |

## o-girrr-registro

| Ramo | Ultimo commit | Data | Messaggio |
|---|---|---|---|
| `moviola-lab` | `1c57cf3458d03831116eb833c560abd05d0ef742` | 2026-10-23 | Lab: tab Moviola di Girrr Sport attiva (episodi veri per giornata, archivio, verdetto) |
| `moviola-json` | `603567ac2f55e7147540fb9b7b285f351b9b1c49` | 2026-10-23 | Moviola: episodi decisi una volta sola da calcoli/moviola.py, il Lab legge moviola.json |
| `claude/moviola-passo-4-girrr-kss5r2` | `b73e961ffb3c2f802ea74d8147294e36ce5d53ca` | 2026-10-23 | Moviola passo 4: post Moviola di Girrr Sport dalla Curva (solo ramo, non online) |
| `moviola-verdetti` | `061bc0b4ff7a6a7b9137faa0c140bef93a96c876` | 2026-10-23 | Moviola: barretta laterale del colore del verdetto su tutte le card |
| `claude/moviola-manuale-step-3-7qapus` | `4dac3bb3a2e2fc34e5b2a0fa85c079cc1e024de7` | 2026-10-23 | Moviola passo 3: voci a mano, video nelle card e pagina di ricerca dei video, dentro calcoli/moviola.py |
| `moviola-curva` | `52858cb8f3ab6050547148a25525b719da6ac26c` | 2026-10-24 | Moviola passo 4: online sul sito (gh-pages a8ae5c0, main c505036), patch gh-pages rifatta sopra 0ccac01 |
| `moviola-gol` | `d42f65679d515bf736918d91473683d66b98c1bc` | 2026-10-24 | Moviola gol: online sul sito (gh-pages a2e611a, main 6ef4017), prova nel browser con il numero di episodi da moviola.json |
| `claude/sfondo-selettore` | `163052db082243e3d601ce9f39ca5268c01d1da9` | 2026-10-24 | Selettore Lega/Stadio: fondo scuro solo sullo Stadio, tornano le strisce della Lega |
| `claude/stato-rilascio-selettore` | `42092071983c4035de32753a652965375c9a600b` | 2026-10-24 | STATO: selettore Lega/Stadio online sul sito (gh-pages 27487c0) |
| `claude/allenatore-squadra` | `6ac2d97dc2fe2c14873518b4ce35fd16dc1b26b9` | 2026-10-24 | Unisce main: STATO con la storia della Lega (VS Code) e la card dell'allenatore |
| `claude/storia-emma` | `614981e7c16242e5786e691ea0dfc3e9f0a5bf79` | 2026-10-24 | STATO: storia del Derby dell'Emma online (gh-pages a489393) |
| `claude/storia-lega-correzioni` | `6e377448e7ab1b6e7cd9a3d29bf350e9a5968bed` | 2026-10-24 | Storia della Lega (bozza): nomi come su Leghe, anni del sito, Grande Silenzio corretto |
| `claude/derby-senza-in-palio` | `c4180b3903decb3e1d81303bf17f9ca6fc1291b4` | 2026-10-24 | Derby: tolta la riga "In palio" dal riquadro del Lab (Anteprima rigenerata) |
| `claude/storia-apo-oranje` | `4b2fe61f1c6fd04d3d40cd1a8cd907fbe12cd7b1` | 2026-10-24 | Unisce main nel ramo della correzione apo-DJ Cst Brazil |
| `claude/derby-tabellone` | `bdd86c607138e4cb048fa9e0bb5332c1e99f698d` | 2026-10-25 | Derby da 80 in su ovunque; etichette Sfida scudetto, podio e salvezza nelle ultime 10 giornate |
| `claude/scheda-storia` | `775b29b6f0d4b3906f576540d2a0261ce5082ada` | 2026-10-25 | Unisce main nel ramo della scheda La Storia (note di STATO tenute tutte) |
| `claude/gracious-meitner-lmt0ny` | `cfe57ce5a1a6e94d82c88cfe937d3bb234398fde` | 2026-10-25 | STATO: Totogirrr a 320 px online (gh-pages d8ce210) |
| `claude/ere-pallino` | `588cb3ab0cc1ec92366fe7a882ee4ed7ef27e012` | 2026-10-25 | Le Ere: nome con punto mediano (L'Era dei Titani · La scintilla, ...) nell'Anteprima e nella bozza |
| `vscode/anteprima-storia-lega` | `91f29336a4a598b32de126bc96403598b9fe87e1` | 2026-10-25 | Intreccia le descrizioni nei racconti delle Ere |
| `claude/tabellone-punteggi` | `2260367fd551829381abbbbaf509c6728dbd9399` | 2026-10-25 | Tabellone: tornano i punteggi (l'etichetta di classifica sovrascriveva la variabile del punteggio) |
| `claude/stato-rilascio-5-1` | `2e1fadb741e6a2b9550ccb13872c90d53a4f0909` | 2026-10-25 | STATO: rilascio 5.1 online (gh-pages eb886da) |
| `claude/ere-intrecci` | `0e90462bbfc8d43af713bd413fe5c85fc8c6ca45` | 2026-10-25 | Unisce i testi intrecciati delle Ere di VS Code (titoli col punto mediano tenuti) |
| `claude/stato-infortuni` | `8ae57b1eddf14b4db7709ae1a616a67dcc59541d` | 2026-10-25 | Stato: controllo infortuni del 25 ottobre |
| `claude/ere-leggenda` | `518505a798f45238c22af7a58717291596eff505` | 2026-10-25 | Ere: sopra il racconto leggendario, sotto i capitoli descrittivi; la storia del nome rimanda a La Storia |
| `claude/stato-ere-online` | `6a4d2af20f34b4ae8a78b161b0c16b8a9d010d8a` | 2026-10-25 | STATO: Ere con racconto e descrizione online (gh-pages 85a9415) |
| `vscode/sposta-stagioni-silenzio` | `940d2d374df403507576bed7c47283b010c56f00` | 2026-10-25 | Sposta le stagioni non assegnate nel Grande Silenzio |
| `claude/obiettivi-scadenza` | `463eefb322be78e404e3dc2fa63bcb9ad64500e2` | 2026-10-25 | Carriera: gli obiettivi con scadenza non sono Fatto prima del tempo; dopo, Fatto o Mancato secondo la classifica |
| `claude/changelog-archivio-5-1` | `f15cfce63d9537251e5e3899f90dae8b9bdff680` | 2026-10-25 | Unisce main (STATO: Lab e SQL curva_feed) nel ramo del changelog |
| `grok/curva-infinite-scroll` | `f972444462b336bc0dffba5e8072399e3dee78ae` | 2026-10-25 | Curva: infinite scroll (20 post + scroll) — patch e file pronti |
| `claude/stato-curva-ripristino` | `e7dd42d384fc08b5be0afab158956896c9487650` | 2026-10-25 | STATO: Curva ripristinata sul sito vero dopo il push errato |
| `claude/curva-320` | `fee1eedb60877310e51fc92b181ada98cb706e25` | 2026-10-25 | Curva: riga dei pulsanti dentro lo schermo a 320 px (sorgenti del sito, Anteprima, STATO) |
| `grok/spogliatoio-lazy` | `78935a1d1b10976d9d2bbeb8087c71c4e4e98fab` | 2026-10-25 | Grok: sincronizza il lazy loading completo nel Laboratorio |
| `chatgpt/regola-autori-commit` | `4ed5a67bbb6fed77d67995133af8aa6dbd302979` | 2026-10-25 | ChatGPT: rende obbligatoria l'identificazione dell'autore nei rami, commit e PR |
| `chatgpt/lab-lazy-grafica-lega` | `30f65a7bb27792a9b04aaddaa9eba029aa1c554a` | 2026-10-26 | ChatGPT: documenta la prova dello Spogliatoio integrale nel Lab |
| `chatgpt/collaudo-curva-infinite` | `46dc0b4b67c18cc821733e62c1ca7f02e17bec2d` | 2026-10-26 | ChatGPT: risolve conflitto STATO preservando Lazy e Infinite Scroll |
| `chatgpt/collaudo-carriera-storico` | `d8454ebcbabed1670af9fc857aae552dbc903189` | 2026-10-26 | ChatGPT: risolve conflitto STATO e mantiene i collaudi Lazy, Curva e Carriera |
| `claude/stato-giornata-4` | `258543194aeb5520f8819cd2e750a60ea3e60b3d` | 2026-10-26 | Stato: giornata 4 entrata, Radio ancora da collegare |
| `claude/radio-giornata-4` | `998ed46d2d7f9819e31ec117becae31123cd93db` | 2026-10-26 | Puntata di prova della Radio |
| `chatgpt/fix-carriera-responsive-rilascio` | `8d1d1688e981ed8ae9346e8e448b6c2a1148e437` | 2026-10-26 | ChatGPT: documenta fix UI Carriera, collaudi e staging del sito |
| `chatgpt/ci-collaudo-rilascio` | `c58d7793ee1978a663696a3ecb030df863dca6b9` | 2026-10-26 | ChatGPT: normalizza colori RGB CSS nel test Chromium e WebKit |
| `chatgpt/anteprima-52-fiducia-pallino` | `3882a8307db2911e3a8c6a30ad080a443f16ba31` | 2026-10-26 | ChatGPT: esegue build e verifica Anteprima 5.2 su GitHub Actions |
| `chatgpt/anteprima52-anim-fiducia-reputazione` | `f1d48d6bd4b2207b8d64cea43b0c0b9db7c76191` | 2026-10-26 | ChatGPT: anima anche le barre Fiducia in lega con rispetto reduced motion |
| `chatgpt/anteprima52-fiducia-tutte-squadre` | `17950d290cb72d2edc7b578ff8b9309d50389c71` | 2026-10-26 | ChatGPT: aggiunge CI formula Fiducia universale 5.2 |
| `chatgpt/preview52-milestone-toto-premi` | `4eaf766f1e04926c0d69dd02b89c158be6ad433d` | 2026-10-26 | ChatGPT: expect correct official ranking for synthetic G8 test |
| `chatgpt/anteprima52-riscatto-milestone` | `a27fe47684d98767d189305bd5e55eed03467b24` | 2026-10-27 | ChatGPT: diagnostica controlli QA Carriera 5.2 per browser |
| `chatgpt/regola-anteprima-integrata-52` | `e234b50eb5290536b8012185128322d52f2b844f` | 2026-10-27 | ChatGPT: definisce anteprima integrata, laboratorio e aggiornamento changelog |
| `claude/gifted-wozniak-vhwhnb` | `a5105ac8736d72bc8d97fddfe6e7cb1a11c7b4fb` | 2026-10-27 | Claude: STATO.md, infortuni a orario fisso e prova da cancellare rinominata |
| `chatgpt/carriera-tab-obiettivi` | `bc3abb79972337cf16529545cca1a46f5a8fcea3` | 2026-10-30 | ChatGPT: documenta tab Obiettivi, collaudi e limiti di verifica |
| `grok/carriera-tab-storia` | `972dc62cb8512458e3cf0da8bd268084c2ae0674` | 2026-10-30 | Grok: vCarStoria tab Storia della Carriera |
| `chatgpt/recupero-tab-storia-grok` | `6c4c231846c5bdbb95f2a27c28de1879419f7bb6` | 2026-10-30 | ChatGPT: documenta ricostruzione tab Storia e corruzione del ramo Grok |
| `claude/review-ai-changes-test-ui9gjy` | `67c97f812e606f8d437f2a27614e241af18243d5` | 2026-10-30 | Claude: rilascio 5.2 sul sito vero, sorgenti allineate e STATO |
| `chatgpt/tabellone-annuario` | `0556f4870ff36548a60ca7492e8a1b3dcba2c028` | 2026-10-31 | ChatGPT: registra in STATO i collaudi riusciti a 320 e 1280 px |
| `chatgpt/home-notifiche-centro-partita` | `d54620cb530b4b0fa03157ad3e8a296a3d866000` | 2026-10-31 | ChatGPT: ufficializza i tre livelli editoriali e documenta il redesign necessario |
| `claude/premi-giornata` | `665ecb15abca1b3f906764bda54015e900f2ce01` | 2026-10-31 | Claude: sponsor dei Big in Champions Cup, 4 vittorie nel girone invece di 5 |
| `chatgpt/anteprima-53-integrata` | `03a2a9f4be64243f6e3ec811851e74052ae4038d` | 2026-10-31 | ChatGPT: documenta in STATO.md la QA 5.3 verde e i limiti UX |
| `chatgpt/lavori-31-ottobre` | `3fd7e40be46b39cc32c9c2ba2713d3196fac602f` | 2026-10-31 | ChatGPT: documenta integrazioni mancanti e prepara il prompt per la prossima chat |
| `chatgpt/integrazione-ui-campo-cronache` | `70a0b58da875957a633d72895a03f332feafb1ae` | 2026-10-31 | ChatGPT: collega la PR e documenta il limite della verifica pubblica |
| `claude/coppe-simboli-ere-descrizioni-4jn4ss` | `bc37f08ee7cc79f34a0938edc946b1da88f0a08e` | 2026-10-31 | Claude: numerazione, la 5.3 è online e la prossima sarà la 5.5; archivio 5.3 e anteprima rigenerata |
| `claude/anteprima-55` | `8fc383681d045b444b853f6ebebf0d98bfa3b4e3` | 2026-10-31 | Claude: porta il lavoro di ChatGPT del 31 ottobre (PR 38, 39, 41, 42, 43) sopra main, Anteprima rinominata 5.5 |
| `chatgpt/completamento-53-campo` | `9137c1f6ccc4f55455d950117a5fa104ea614fe4` | 2026-11-01 | ChatGPT: documenta e collauda Campo con contenuti, due skin e casi limite |
| `claude/campo-unione-chatgpt` | `4a0720883998b354292b1103077479a3c525058a` | 2026-11-01 | Claude: unisce il Campo di ChatGPT (stile Lega/Stadio del sito, stemma, ui.css unico) tenendo le formazioni nel campo |
| `claude/notifiche-supabase` | `54a952e4b6255ffbd39d7370d30a93296aea073d` | 2026-11-01 | Claude: notifiche personali da Supabase nell'Anteprima 5.5 e puntini della Home sistemati |
| `claude/campo-grafico-maiuscole` | `5d12cdc2da10a69afdfaa2b13696ec62730544ae` | 2026-11-01 | Claude: Campo, grafico dei punti con scala, valori e giornate; maiuscole nelle etichette |
| `chatgpt/verifica-55-claude` | `bddbdf67edd3ead0cd52167070fc8a5eebb6892c` | 2026-11-01 | ChatGPT: rende consultabili cronache e PDF nel Lab e documenta la consegna |
| `chatgpt/cronache-55-complete` | `ab9cbdadd848874c0209cc8bc12b60922f18aa92` | 2026-11-01 | ChatGPT: documenta il collaudo superato e collega le cronache dalle Novità 5.5 |
| `claude/squadra-evidenziata` | `6a1d7f4bc960d319b0fc165dfc062e1ce97f3ac6` | 2026-11-01 | Claude: la squadra entrata in evidenza in Campo, grafico del Tabellone e Annuario |
| `chatgpt/cronache-55-rilascio` | `a10a4e253f2ba7accd198781bd3cde10300cc979` | 2026-11-01 | ChatGPT: include i collegamenti delle cronache nel futuro rilascio 5.5 |
| `claude/collaudo-55` | `500e201aa43726deca9dcb9562b7f725d86b95ef` | 2026-11-01 | Claude: collaudo 5.5 su telefono, tablet e PC con Chromium e WebKit (prova e workflow) |
| `chatgpt/home-unica-55-bozze` | `becd43cd9977bf24447aeaeca80a47897cdee5dd` | 2026-11-01 | ChatGPT: allinea le bozze Home al Registro aggiornato |
| `claude/frasi-regole-readme` | `adbada2d18f6ecf277b18250561193d3e5442a4b` | 2026-11-01 | Claude: frasi dei personaggi dalla PR 40 (solo dal 2 novembre), tre livelli di scrittura, README con i link, menu leggibili nelle sorgenti |
| `chatgpt/home-notifiche-navigazione-55` | `4a14139d168bc771015520b4fcf533d4fb809295` | 2026-11-01 | ChatGPT: documenta i collaudi finali della Home e i limiti aperti |
| `chatgpt/home-richiudibile-squadra55` | `ee434432d35ec0ad3942b3b5763a3e9897ee4ccb` | 2026-11-01 | ChatGPT: consegna screenshot ed esiti della Home richiudibile |
| `chatgpt/notifiche-destinazioni55` | `1f3e5dfa709ce8bb1d055eca3c37e5f7404f2767` | 2026-11-01 | ChatGPT: preserva impaginazione e transizioni di Claude nelle notifiche |
| `claude/unione-pr50` | `46eb6eb39080d8321b1af523323e675c11c1bc93` | 2026-11-01 | Claude: unisce la PR 50 di ChatGPT (notifiche compatte e collegamenti al contenuto preciso) |
| `claude/regole-grafiche-prompt` | `4a59ccff5ac4921dfedcf35e0cdcd49d1a3863f6` | 2026-11-01 | Claude: regola grafica Lega/Stadio in AGENTS.md e prompt per ChatGPT e prossima chat |
| `claude/sharp-cori-ypgc7o` | `523857eed6c12d811b3c04b6cde0faca7c352264` | 2026-11-01 | Claude: Tabellone C con Campo anche in Coppa, schede uguali e azzurre in coppa, fase finale a tabellone di tennis |
| `claude/grafiche-lega-stadio-55` | `b2d2baf0ffca1dd9829559661861d4894163af6c` | 2026-11-01 | Claude: grafiche Lega e Stadio su tutta la 5.5, Stadio più oro, Spogliatoio con grafica Stadio e menu delle grafiche |
| `claude/risultati-tre-due` | `0257260ae7afa8b3e8f80a14eda5242f3310f6cd` | 2026-11-01 | Claude: Tabellone C definitivo, cinque partite tre a sinistra e due a destra su PC, regola della pagina novità per ogni versione |
| `claude/campo-fluido` | `ea816987a6fa7e5b184f2ad2618fab3b9c9624dc` | 2026-11-01 | Claude: Campo senza scelta della grafica, entrata in dissolvenza di Campo e Tabellone quando sono pronti |
| `claude/campo-telefono` | `42a464e8c2a3e08948c639ed93885acc42c90828` | 2026-11-01 | Claude: Campo sul telefono senza doppioni, fila delle partite che scorre col dito |
| `claude/fiducia-grafico` | `eaacf8e3d9a41b20ae1d302b1361ddd6d6b140d9` | 2026-11-01 | Claude: Carriera, grafico della fiducia con scala, valori, giornate e tabella dei risultati; «E se…» spiegato |
| `claude/rilascio-55` | `8f71c88733e0a48b56374e7a5bc53e7e39ee51a1` | 2026-11-01 | Claude: rilascio 5.5 sul sito vero — script di rilascio, modalità sito in ui.js, sondaggio della Curva nel database, cronache della Home, sorgenti ufficiali allineate a gh-pages |
| `claude/home-testata` | `f4d61ee68447f21b23c88c154b80c8cf22021594` | 2026-11-02 | Claude: Home con la testata di prima (logo grande, interruttore Lega/Stadio), online su gh-pages 42f271a |
| `claude/curva-barre` | `6b4cad15c9e1b51c8335e7ea6e288f6b403d5af2` | 2026-11-02 | Claude: Curva con il sondaggio come post e senza barra, commenti che si chiudono, barra con solo logo e indietro, tiro giù per aggiornare; online su gh-pages 064a207 |
| `claude/home-riquadri` | `83bfe66dc55f37ede470d9281f837ae2c0e663fb` | 2026-11-02 | Claude: Home con i riquadri di prima nell'Anteprima e Totogirrr su una riga; rilascio sul sito in attesa del permesso |
| `claude/home-stadio-oro` | `50a7d41ab665f2726321ee9d2df2b459c842f6db` | 2026-11-02 | Claude: Home Stadio con i riquadri di informazioni più tondi e più oro (Anteprima e sorgenti pronte) |
| `claude/tira-giu-dritto` | `97f9669f5edfe2cbe01dde0324a34911c3b98914` | 2026-11-02 | Claude: «Tira per aggiornare» resta dritto, gira solo la freccina (Anteprima; sito in attesa del vai) |
| `claude/campo-icone` | `415e52bb88aa538c3a8964e1e6566e71db808675` | 2026-11-02 | Claude: Campo con il simbolo della scheda attiva visibile e pillola di aggiornamento trasparente (Anteprima; sito in attesa del vai) |
| `claude/prima-apertura` | `a395c81b5b6a8a9f85fd946dd21ddff685129be6` | 2026-11-02 | Claude: prima apertura più veloce delle pagine 5.5 (script velocita55.py, attesa massima 1,5 s); sito in attesa del vai |
| `claude/confident-babbage-1993x1` | `c094c13ce15efa1f4a832a262e7239ac51ec0b93` | 2026-11-03 | Claude: punti del 2022/23 online nell'Albo d'oro (gh-pages 3135e60), sorgenti allineate |
| `claude/offline-mode-sync-5vmvdd` | `db73fbd04e60f73016f37beb1b10ce50efd7e676` | 2026-11-10 | Claude: Lab, collegamenti alla Curva per provare cuori e rilanci (5.6.3) |
| `claude/conferenze-stampa-punteggio-pe4qga` | `e29eea7931dbd4bffef94813c82a1e59d47d0669` | 2026-11-11 | Claude: STATO, sezione della 5.8 riscritta (testo perso per un comando sbagliato, nessun danno) |
| `chatgpt/controllo-chiave-premi` | `e3ca2305ffc0a00e530ff2a6418b6da51a89ab7e` | 2026-11-12 | ChatGPT: controlla la chiave server dei premi e supporta le nuove chiavi Supabase |
| `chatgpt/allineamento-automatico` | `81799e3278ffe258c04d15eb8c40637e134e53df` | 2026-11-12 | ChatGPT: registra il via e i collaudi sui tre motori senza nuova versione |
| `chatgpt/verifica-pubblicazione-registro` | `90a7f7ce800931ea93b7a41e78aacc56bfabe087` | 2026-11-12 | ChatGPT: verifica la ripubblicazione del Registro e abilita la lettura dei sondaggi |
| `chatgpt/fiducia-anteprima-squadra` | `51e0d8e1c0ba8c4fd72e3fffc6828b22f8a8088c` | 2026-11-12 | ChatGPT: completa il deploy Pages e corregge la Fiducia della squadra nell’Anteprima |
| `chatgpt/decisioni-mvp-derby-12-novembre` | `0ef3c5ceed16c5fa88c9faf4bdb5ca5df47d8796` | 2026-11-12 | ChatGPT: registra la verifica e distingue idee e funzioni presenti |
| `claude/liquid-glass-lab-prototype-qslq3e` | `dd3ba22e64ed1f60613abf73cafa716b6258ed80` | 2026-11-12 | Claude: scheda Video in Girrr Sport con tutti i video della giornata (Lab), video dalla 1ª alla 7ª, fischi nuovi della Radio |
| `chatgpt/prova-mvp-derby-settimana` | `c90eb656cd97c095f759cd568fb7f42b3402d0d9` | 2026-11-12 | ChatGPT: documenta la regola editoriale e il collaudo dei Derby ufficiali |
| `chatgpt/integrazione-6-0` | `3a35e4d6144ec8e3e119827aedede5f349747f7d` | 2026-11-13 | ChatGPT: certifica i collaudi e consegna la preparazione 6.0 a Claude |
| `chatgpt/ramificazioni-leggibili` | `c60b0ea3614a14f81415e3065683cc2601b94f89` | 2026-11-13 | ChatGPT: certifica la vista compatta richiesta con Claude |
| `chatgpt/esito-schema-mvp-60` | `024ab26a580c942e1fa0deacf2c87601d6bb0150` | 2026-11-13 | ChatGPT: registra lo schema MVP applicato e le verifiche live |
| `chatgpt/registro-ingresso-unico` | `fc5117ba11e1ccb12bb155e81947666ece9b8d00` | 2026-11-13 | ChatGPT: attende la sezione corretta nei cambi di pagina |
| `chatgpt/registro-attesa-browser` | `c8a52c648bde6c3201a9d25780d5927263af7d36` | 2026-11-13 | ChatGPT: attende anche la nuova grafica prima del collaudo |
| `chatgpt/prove-lab-portale` | `9ef37aba765ea0ce23e0494bed78323ed885037d` | 2026-11-13 | ChatGPT: apre il Lab fuori dal portale nelle prove browser |
| `chatgpt/changelog-filtri-compatti` | `a44673dc8a4b0f152691aadcd7fcc8ca2744287b` | 2026-11-13 | ChatGPT: verifica filtri e panorama sui tre motori e sedici formati |
| `chatgpt/anteprima-avvio-404` | `0f7b58cc79f9d6d9cb2bf049919f976055636810` | 2026-11-13 | ChatGPT: recupera l’Anteprima da un ultimo indirizzo non valido |
| `chatgpt/anteprima-versione-grafica` | `e2090373143f7b2998b704be725355fb219b39aa` | 2026-11-13 | ChatGPT: carica insieme la nuova cornice e i suoi controlli aggiornati |
| `chatgpt/registro-workflow-e-verifiche` | `7eb6a3a5b9ae9fe9e541af490e48c18f4300246d` | 2026-11-13 | ChatGPT: conserva i collaudi sulle notifiche e sui menu attuali |
| `chatgpt/esito-registro-60` | `0e1d3ce5fd1dca8073e99942d80eb799a80100e7` | 2026-11-13 | ChatGPT: registra gli esiti del main e il lavoro completato da Claude |
| `chatgpt/rami-eventi-pr` | `a915ffd81ebe388757f2416f23f48a9a78757148` | 2026-11-13 | ChatGPT: aggiorna la mappa a ogni cambio di PR e ramo |
| `chatgpt/602-giro-di-boa` | `f7d3f637b9df6e214a1369807bddef9f72fb71c0` | 2026-11-13 | ChatGPT: registra per la 6.0.2 le due condivisioni del Giro di boa |
| `claude/o-girrr-versione-6-0-mjh4ut` | `a87c8ebd748cbca584dc84c35a12f2205672938f` | 2026-11-14 | Claude: 6.0.2, Le ultime 5 senza la sigla della forma: vittorie, pareggi e sconfitte a parole |
| `chatgpt/lab-claude-601-602` | `566399b7f52a714965a65548d16ba0b556f4b793` | 2026-11-14 | ChatGPT: riprende la 6.0.2 di Claude conservando lo stato del main |
| `claude/rilascio-601` | `882e6e73b98483c3084888bbd4960f3001772f5e` | 2026-11-14 | Claude: Rilascio 6.0.1 online (gh-pages e9124d9), versioni.json, sorgenti del sito allineate, AGENTS.md e STATO.md |
| `claude/rilascio-601-esiti` | `10dac318bab8882065b1c28104b565e304a64558` | 2026-11-14 | Claude: STATO.md, esiti delle prove della 6.0.1 sul sito vero |
| `chatgpt/giro-boa-completo-602` | `450fb6adc4d61ea0b430f45bea354278a90fa034` | 2026-11-14 | ChatGPT: certifica le nuove anteprime e prepara la 6.0.2 sopra la 6.0.1 online |
| `chatgpt/esito-anteprime-602` | `bc60af9f9cab744a0ea256ba0dda7b27d446699f` | 2026-11-14 | ChatGPT: registra i collaudi conclusi e le anteprime 6.0.2 verificate online |
| `chatgpt/giro-boa-colori-602` | `229dc4f12dd8c5267741f328200cb3dd343f6822` | 2026-11-14 | ChatGPT: centra V N P e distingue i colori delle scritte nel Giro di boa |
| `chatgpt/radio-condividi-centrato-602` | `b6a85d4b5a56f2cbcac79819cf04d508f0759b7a` | 2026-11-14 | ChatGPT: centra Condividi la puntata sotto il lettore della Radio |
| `chatgpt/giro-boa-periodi-sbloccabili-602` | `c9e01e4abbb2d9de507035db92910d7f5eabdb62` | 2026-11-14 | ChatGPT: annota il blocco del merge Lab in attesa del Vai 6.1 |
| `claude/ramificazioni-tre-viste` | `8fd79f58fdd73719cbd1b2e34c0cd006eab61aae` | 2026-11-14 | Claude: Ramificazioni con i tre disegni dei rami in cima (Albero, Linea del tempo, Ventaglio), dati aggiornati dal workflow ogni 15 minuti |
| `claude/ramificazioni-aggiornamento-immediato` | `49df58ac714da05dfa6cdc85b1f0a1b822657dc8` | 2026-11-14 | Merge remote-tracking branch 'origin/main' into claude/ramificazioni-aggiornamento-immediato |
| `chatgpt/esito-lab-61` | `a03eefd4f5d79deb4508c07427675b6ed87f956c` | 2026-11-14 | ChatGPT: conserva sorgenti e verifica della 6.1 pubblicata |
| `chatgpt/nome-competizioni-61` | `f5b83f426f3de44ea9eb1a9db7304fd4330e2373` | 2026-11-14 | ChatGPT: rifinisce il nome delle due competizioni nel Lab |
| `chatgpt/carriera-curva-611` | `ccc1f5df20ad898dfd4dc91094b1d5102c525340` | 2026-11-14 | ChatGPT: rende bianchi e più leggibili i dettagli della Stagione |
| `chatgpt/esito-611-lab` | `804a36e950b4bd200d6ad5361b6ac21ac82b2864` | 2026-11-14 | ChatGPT: registra CI e verifica pubblica dell’anteprima 6.1.1 |
| `chatgpt/posizione-riga-unica-611` | `88362fa6b33985355e0b72d064f69b82bc066827` | 2026-11-14 | ChatGPT: tiene unita sul PC la frase della posizione peggiore |
| `claude/ramificazioni-pagina-piena` | `16207d19503d8f0aedaf87ab0a30ef3caac92e83` | 2026-11-15 | Claude: Ramificazioni a tutta pagina, unioni dei rami in tutte e tre le viste, vista bloccata all'inizio, Linea del tempo con nomi e date fissi, Ventaglio a blocchi |
| `claude/stato-61` | `4e3c3b444adb5f54f6a989ae96a9b3a6e30950f3` | 2026-11-15 | Claude: STATO.md, voce del 15 novembre in cima e la 6.0.2 confluita nella 6.1 |
| `chatgpt/coordinamento-62` | `05419a859eb8d138713ca95627641fad4a3849b9` | 2026-11-15 | ChatGPT: ferma la pubblicazione delle bozze grafiche rifiutate |
| `chatgpt/integrazione-62-completa` | `13b722368a7df8ebf15afb47dcec73caffa9a419` | 2026-11-15 | ChatGPT: separa i candidati MVP dal Coro e rende laterali i simboli dei portieri |
| `chatgpt/albo-62` | `a31fab6d0b4b40f3849930d6c6ee273fccf82e0e` | 2026-11-15 | ChatGPT: registra esiti e limiti della revisione 6.2 |
| `chatgpt/controllo-62` | `a5480da1a2298aa53fcedd386c7fb9a8c0b0074a` | 2026-11-15 | ChatGPT: registra QA e copia protetta del post MVP |
| `chatgpt/rc-62-verifica` | `7c5fbaa216a67018974a4790edf497d6d3014daf` | 2026-11-15 | ChatGPT: apri la scheda Record prima delle verifiche Albo 6.2 |
| `chatgpt/fix-62-portale-ramificazioni` | `3e4e2d48d3574d2bfc463f8b7e67ccdc663888bc` | 2026-11-15 | ChatGPT: collega Ramificazioni moderna al portale 6.2 |
| `chatgpt/621-completamento` | `6573411415cdf16c9ad9e350d83c3490d1b13d9b` | 2026-11-16 | ChatGPT: includi modulo MVP 6.2 nel PDF di prova cronache |
| `chatgpt/dati-ramificazioni` | `bfe3d93f837a033e2b2b23647ce3e5e08545665a` | 2026-11-16 | ChatGPT: aggiorna le ramificazioni alla nuova versione |
| `claude/fervent-thompson-rwlwrh` | `d6280d5176d7096059ef6bdc650593ec339f35b8` | 2026-11-16 | Claude: prove allineate all'Archivio con l'anteprima storica e al ripristino dell'Anteprima |
| `claude/rilascio-622-registro` | `341faf909c4fce25302b72874f2f6338b30f743e` | 2026-11-16 | Claude: lascio l'allineamento di versioni.json del registro al workflow |
| `giandjcosta/prima-pr` | `19bf67994fe808369fa4e161e146aa3b8ad52463` | 2026-11-16 | Gianluca : First Pull Request, nota nel quaderno dei lavori |
| `chatgpt/miami-nights-fusione-lab` | `74f527adf98d82cd2622ef91037f20aea1e9ed91` | 2026-11-17 | ChatGPT: annota ingresso unico senza scelta Lega/Stadio nel quaderno |
| `chatgpt/theme-engine-vice-city-event` | `cb33e3bde651ad672068ee2f4126c761610f09b7` | 2026-11-17 | ChatGPT: crea anteprima navigabile delle pagine reali 6.2.x con nuovo UI Miami |
| `chatgpt/miami-ux-claude-base` | `ccdd8544b49bffc905024f10a769172e3efef9a5` | 2026-11-17 | ChatGPT: ridisegna anche tab native del Lab con gradiente evento unico |
| `grok/palette-notte-tropicale` | `4549a14b861fd9b05c716b425a0c676bb144541d` | 2026-11-17 | Grok: spiega la licenza di Pricedown, il file non entra nel ramo |
| `chatgpt/651-tabellone` | `048d55be5f8ca6e713b403007621f2e2304a8ae3` | 2026-11-17 | Claude: 6.5, Curva senza «vince» per i pareggi; scaletta con la skin |
| `chatgpt/65-tabellone-curva` | `4cc63aa20c30672e2d00cb8bffa2fb4d809ec0ae` | 2026-11-17 | ChatGPT: registra il link di anteprima 6.5 senza deploy |
| `chatgpt/notte-tropicale-pagine` | `3563361301bb1b81896dea8f1fdba0c0550b121d` | 2026-11-18 | ChatGPT: prova anche le due ancore Classifica e Risultati |
| `chatgpt/65-qa-base` | `4764de7cbb347b1ff3768afd4eecb1f34eb1a967` | 2026-11-18 | ChatGPT: prepara collaudo screenshot separato dal rilascio |
| `chatgpt/65-qa-screenshots` | `9f6cb598b4e97b21a28d324f27c228cd3112fc94` | 2026-11-18 | ChatGPT: risolve regressione 2×2 nel Tabellone e ripristina griglia Home |
| `chatgpt/65-tab-uniche-curva-separata` | `ccddbb81aeebd8073f9c0d490f997af85714cecb` | 2026-11-18 | ChatGPT: aggiorna la bozza annuncio per finestra 19–27, fine 28 senza promettere skin già attiva |
| `chatgpt/65-due-ingressi-preview` | `76fc39c512f2ca721652645db8f920c44228f8d0` | 2026-11-18 | ChatGPT: testa durata visibile della copertina e nuova dissolvenza senza toccare B |
| `chatgpt/65-transizione-b-sfumata-60fps` | `3346bed2992a1b32abafb2ad9e020b45191485ca` | 2026-11-18 | ChatGPT: anima B a dissolvenza morbida solo opacity/transform per migliore fluidità |
| `claude/totogirrr-ui-responsive-b2pgee` | `de00cd8231ee12cc05df87c5c5c1d18db65f3b02` | 2026-11-18 | Claude: prompt di uscita aggiornato al nuovo commit |
| `chatgpt/65-rifiniture-prima-del-rilascio` | `9c5caad020f6a0e83438e62861dd2ea0e8f00b03` | 2026-11-18 | ChatGPT: registra rifiniture della 6.5 prima della pubblicazione, non 6.5.1 |
| `chatgpt/65-entrata` | `6e3ebe2863801b2056a378073659a7b84e306b6f` | 2026-11-18 | ChatGPT: aggiorna la certificazione statica delle 61 patch della 6.5 |
| `claude/girrr-transition-effects-zpfofz` | `ba5aa08c39fea5d7d20da9b97073d24d6e4ec80c` | 2026-11-18 | Claude: fondo a strisce della Lega senza fascia vuota a sinistra sull'iPhone; nota per l'integrazione della nuvola |


## Aggiunti il 19 novembre (mattina)

| Ramo | Ultimo commit | Data | Messaggio |
|---|---|---|---|
| o-fant-a-girrr · `claude/65-entrata-pc` | `63d3dbe23724ed5cde727c95a4234b13fd127982` | 2026-11-19 | Claude: README, il link apre la Home della lega invece dello Spogliatoio |
| o-fant-a-girrr · `claude/readme-home` | `605a1a0f64ae94d2d98f133f2b10075941a9262f` | 2026-11-19 | Claude: README, il link apre la Home della lega invece dello Spogliatoio |
| o-girrr-registro · `chatgpt/65-edizione-speciale` | `f5deec153715fef2998d5558aaadce4b540322dd` | 2026-11-17 | ChatGPT: allinea banca Curva del Lab alla versione collaudata e alla scadenza |
| o-girrr-registro · `chatgpt/65-tab-uniche-curva-separata` | `ccddbb81aeebd8073f9c0d490f997af85714cecb` | 2026-11-18 | ChatGPT: aggiorna la bozza annuncio per finestra 19–27, fine 28 senza promettere skin già attiva |
| o-girrr-registro · `claude/65-uscita` | `a0383dd0afe795bcd023e2785d0b69a5254485ac` | 2026-11-19 | Claude: STATO aggiornato dopo la copertina su PC e la Radio/video della giornata 8 |
| o-girrr-registro · `claude/65-radio-video` | `4486f33cd98fc19c9e4c6d96cdc05a1dd7fb8481` | 2026-11-19 | Claude: Radio e video della giornata 8 in edizione Notte Tropicale, dalla PR 129 di ChatGPT senza i post della Curva già online, caratteri in locale |
| o-girrr-registro · `claude/sincronizza-65` | `eb6ff5e1333e484b3bc47c5db7a512c331b7cb33` | 2026-11-19 | Claude: sincronizzazione del registro compatibile con destinazioni55.js della 6.5 |
