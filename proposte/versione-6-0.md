# Prossima versione: 5.9 o 6.0? · 12 novembre 2026 (Claude)

Sul sito c'è la 5.8.1. Qui l'elenco di tutto quello che è pronto o in prova, di Claude e di ChatGPT, e le proposte per Radio, video e «Condividi la giornata».

## 1. Cosa porterebbe la nuova versione

### Claude · ramo `claude/liquid-glass-lab-prototype-qslq3e` (nel Lab, non online)

**Curva (il cambiamento più grande)**
- Grafica diversa per sistema: su iPhone stile Liquid Glass (vetro, pillole, molle di iOS), su Android stile Material 3 (indicatore a pillola, onde al tocco, molle più elastiche). Animazioni vere su tutta la Curva: cambio scheda, ricarica, aperture.
- Intestazione e barra in basso fisse: non si ricaricano più a ogni cambio, la Curva aggiorna solo i post cambiati (come lo Spogliatoio).
- Notifiche divise in «Attività» (cuori, rilanci, visualizzazioni) e «Menzioni».
- Pillola «Nuovi cori»: compare solo se ci sono cori nuovi, toccandola si torna su e si aggiorna.
- Bozza del coro (non si perde se esci), link a ogni coro (`?coro=`) con evidenza breve.
- Condividi con l'immagine del coro e anteprima per WhatsApp.
- Impostazioni: Aspetto (Automatico, Chiaro, Scuro), suono dell'applauso (tace in silenzioso), colori «Della lega» o «Della tua squadra».
- 15 nuovi personaggi (Radio Girrr e VAR del Girrr verificati, Pizzeria Fuorigioco no), più frasi, immagini disegnate con dati veri (lavagna del bar, foto d'epoca, cartolina e altre). La storia dei giorni passati resta identica.
- Reazioni (prototipo): cuore per primo, altre tenendo premuto, nomi propri e numeri. **Per essere vere serve una modifica al database** (con il «vai»).

**Altro**
- Video della giornata (Remotion): versione «B senza folla» scelta da Gianluca, musica ed effetti, partite da non perdere con i criteri decisi (Derby, 1ª-2ª, 3ª-4ª, ultima all'inseguimento, lunga storia).
- Piccole correzioni, pronte da sole: niente «· bot» nei commenti della Curva, pallino Live che lampeggia solo durante le partite, Carriera con il numero a cartellini e la pillola «Panoramica» centrata.

### ChatGPT

- **Già su `main` del registro, senza nuova versione dell'app (deciso da Gianluca):** allineamento automatico di Anteprima, Changelog e Archivio; controllo della chiave dei premi (serve `SUPABASE_SECRET_KEY` nei segreti); collaudi su Chromium, WebKit e Firefox con 16 schermi.
- **In prova nel Lab, ramo `chatgpt/prova-mvp-derby-settimana`:** Squadra MVP dei tifosi (notifiche), Classifica dei Derby, «La settimana della tua squadra».
- **Proposte conservate** (`proposte/roadmap-discussa-12-novembre.md`): promemoria del mercato scambi, accessibilità.
- I due lavori toccano file diversi (in comune solo `STATO.md` e il menu del Lab): si possono unire senza conflitti veri.

### Proposta sul numero

- **5.8.2 subito (correzione minore):** le tre piccole correzioni (bot, pallino Live, Carriera). Non serve aspettare il resto.
- **6.0 (aggiornamento grande):** Curva nuova per iPhone e Android, video della giornata, «Condividi la giornata», suoni nuovi della Radio. Cambia l'aspetto di una sezione intera e aggiunge un nuovo tipo di contenuto (il video): è la prima cifra.
- Le prove di ChatGPT (MVP dei tifosi, Classifica dei Derby, settimana della squadra) possono entrare nella 6.0 se sono pronte e approvate, altrimenti nella 6.1.
- Le reazioni vere solo dopo il «vai» al database: 6.0 se arriva in tempo, altrimenti 6.1.

## 2. Radio: cosa si può fare con i suoni nuovi

Oggi `voci-src/monta.py` mette sigla (folla, fischio, jingle) all'inizio e alla fine, con un triplice fischio fatto ripetendo tre volte lo stesso fischio. In `RADIO-REGOLE.md` resta da fare «esultanza del pubblico nel mix».

Proposte (nessuna chiamata a Gemini in più: si lavora sul montaggio):
- **Stesso marchio del video:** la base calma del Campionato come sigla, così Radio e video si riconoscono.
- **Triplice fischio vero** in chiusura (`triplice-fischio.mp3`) al posto del fischio ripetuto.
- **Stacchi tra le parti** (risultati → classifica → Champions Cup → conferenze → Curva): whoosh basso, e lo stinger della Coppa quando parte la Champions Cup. Serve che `puntata.py` scriva dove inizia ogni parte (oggi unisce le battute in un file solo).
- **Esultanza** quando Beppe urla un gol o una vittoria larga (le battute con «!!!»), bassa e breve.
- **Tamburi da curva** quando si annuncia un Derby; **«dun»** per il Cucchiaio di legno.
- Il brusio di stadio solo sotto apertura e chiusura, non sotto tutta la puntata (stanca).

Si prova senza costi rimontando l'ultima puntata già pubblicata.

## 3. Il video della giornata: dove, come, per cosa

- **Come:** dopo ogni giornata, il workflow che già calcola tutto (`dopo-giornata.yml`) lancia `rilascio/video/fai_video.sh`: Remotion disegna il video con i dati veri, poi musica ed effetti. Gratis, circa 2-3 minuti su GitHub Actions. Remotion è gratuito per persone e piccoli gruppi (da confermare per noi).
- **Dove sta:** un file per giornata su `gh-pages` (`girrr/video/giornata-N.mp4`, circa 3 MB). Per non far crescere troppo il sito si tengono gli ultimi, oppure si mettono nelle Release di GitHub.
- **Dove si vede:**
  - Home: riquadro «Il video della giornata» accanto a Tabellone e Giornale;
  - Giornale: in cima all'ultimo numero;
  - Curva: post di Girrr Sport con il video;
  - Instagram: lo pubblica Gianluca a mano. Farlo in automatico richiede un profilo aziendale Meta e la loro API: si valuta dopo.
- **Per cosa:** il riassunto da 35 secondi per il gruppo e per Instagram, la porta d'ingresso al sito («Tutto su O Girrr»).

## 4. «Condividi la giornata»: il pacchetto

Un solo pulsante che prepara tutto insieme:
1. l'ultimo video della giornata;
2. l'ultima puntata della Radio (`girrr/voci/puntata-gNN.mp3`);
3. le grafiche ufficiali: Risultati e Classifica del Campionato (già disegnate da «Condividi» del Tabellone) e, nuove, Risultati e Gironi della Champions Cup;
4. il Giornale: la copertina dell'ultimo numero (già disegnata da «Condividi l'ultimo numero») e il link.

- **Dove:** pulsante in Home sotto «Giornata conclusa» e nel Giornale; una scheda mostra il pacchetto con le caselle per togliere quello che non si vuole mandare.
- **Come:** il menu Condividi del telefono con più file insieme (WhatsApp li accetta). Dove non c'è (PC) si scaricano. Se un pezzo non c'è ancora (per esempio la Radio non è uscita, o la Coppa non ha giocato), non compare.
- Livello sportivo nei testi: niente fantapunti e niente scommesse.
- Da provare su iPhone vero: la condivisione di più file insieme, video e audio compresi.
