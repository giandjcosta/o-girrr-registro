# O Girrr — Vice City Edition · Brief operativo

Data: 16 novembre 2026. Stato: concept e fondamenta, **non integrato**, **non collaudato**, **non pubblicato**.

## Obiettivo
Edizione grafica temporanea per il 18–20 novembre 2026, con tema tropicale, tramonti cinematografici, rosa/viola, nightlife e azzurro turchese. Asset e illustrazioni originali, non artwork o loghi Rockstar copiati.

## Separazione permanente
- Lega e Stadio restano le due esperienze permanenti, con stili e preferenze invariate.
- Gli eventi speciali costituiscono overlay visuali indipendenti, applicabili a entrambe le grafiche.
- Nessuna modifica ai dati, calcoli, autenticazione o Supabase.
- Tema evento disattivabile e reversibile; senza tema l'app deve comportarsi esattamente come prima.
- Il catalogo dei temi resta riutilizzabile dopo l'evento.

## Direzione visiva iniziale (da validare in anteprima)
- Sfondo: skyline tropicale originale al tramonto, silhouette di palme, gradienti profondi e luci notturne.
- Palette: #FF91BB, #EE6599, #8D59BB, #25214A, #FFB878, #67D6CF.
- Home: hero illustrato, grande titolo O Girrr, etichetta Special Event, scorciatoie principali e attualità della lega.
- Componenti: schede leggibili in vetro scuro, bordi neon delicati, pulsanti con feedback, classifica ad alta densità informativa.
- Transizioni non invasive; supporto prefers-reduced-motion; no movimento continuo su superfici informative.
- Accessibilità: contrasto, focus da tastiera, 320 px senza overflow, aree touch grandi.

## Priorità implementazione
1. Home Lega/Stadio e navigazione globale
2. Tabellone, Totogirrr, Carriera, Spogliatoio
3. Curva, Giornale, Derby, Notifiche e sezioni rimanenti
4. Overlay, stati vuoti, modali, responsive, riduzione del movimento
5. Ripristino della grafica originale, scadenza e rollback

## Metodo di lavoro
- Usare il branch chatgpt/theme-engine-vice-city-event del solo laboratorio.
- Prima costruire una homepage **navigabile** in anteprima.
- Rispettare la fonte unica degli script di rilascio e la generazione Lab definita in REGOLE-LAVORO.md prima di integrare nel sito.
- Non cambiare main/gh-pages del sito vero, non toccare Supabase, non usare servizi a pagamento.
- Raccogliere feedback su homepage PC e mobile prima dell'integrazione estesa.
- Nessuna pubblicazione senza il comando esplicito «Vai, pubblica».
