# Tema evento · Note di Claude per ChatGPT (17 novembre 2026, 4:30)

Gianluca ha chiesto a Claude di lavorare con ChatGPT fino alle 8 sul tema evento temporaneo, che deve spegnersi da solo dopo il 20 novembre.

## Prove fatte da Claude sulle demo del ramo `chatgpt/theme-engine-vice-city-event` (Chromium)
- Home, Tabellone, Carriera e Totogirrr demo su iPhone SE 320, iPhone 15 Pro, iPad Pro 11, PC 1280, PC 1920 e monitor 2560: **24 casi senza errori**, senza scorrimento laterale, senza animazioni infinite e senza `backdrop-filter`.
- `theme-engine.js` con date simulate: spento il 17 alle 23:59, acceso dal 18 alle 00:00 al 20 alle 23:59, spento dal 21 alle 00:00 (ora italiana). Corretto.
- Su iPhone SE la barra fissa dei pulsanti demo (Tema ON/OFF, Base) copre il titolo della Home: spostarla in fondo o renderla richiudibile.

## Cosa aggiunge questa proposta
- `temi/evento-loader.js`: **un solo punto di accensione** per le pagine vere. Incluso da `tv.js` (che è in tutte le pagine), mette `data-event-theme` e carica il CSS dell'evento solo dentro la finestra di date, deciso dal browser: dopo il 20 si spegne da solo anche nella copia offline, senza rilasci. `?evento=on|off|auto` per provarlo, `?evento-data=…` per simulare il giorno. Usa lo stesso attributo di `theme-engine.js`, quindi il CSS già scritto vale così com'è.
- `temi/prova-evento.html` e `temi/prova_evento.js`: prova automatica del caricatore (14 casi, tutti superati).

## Consigli per l'integrazione (tempo stretto: l'evento parte il 18 alle 00:00)
1. **Nome e grafica originali.** «Vice City» è un nome di Rockstar (GTA), come il logo, il carattere Pricedown e le illustrazioni. Nelle pagine pubblicate usare un nome nostro (per esempio «Girrr City Nights» o «Notte Tropicale») e disegni originali: l'atmosfera tramonto e neon va benissimo.
2. **Tema sopra le pagine vere, non pagine nuove.** Le demo sono belle ma sono pagine a parte: per il 18 conviene un foglio `temi/<evento>.css` che, con `:root[data-event-theme]`, cambia sfondo (cielo, skyline, palme), accenti e titoli delle pagine esistenti, lasciando struttura e dati come sono. Meno rischi, e Lega e Stadio restano riconoscibili.
3. **Regole dei colori** (AGENTS.md): Lega rossa e azzurra, Stadio oro, Campionato rosso e Champions Cup azzurra. Il tema cambia luce e atmosfera, non il significato dei colori.
4. **Fluidità sul telefono:** niente animazioni continue sopra i contenuti; lo sfondo può muoversi piano, solo con `transform`/`opacity`; niente `backdrop-filter` sopra sfondi animati; tutto fermo con «riduci movimento».
5. **Prove:** Lega e Stadio × tema acceso/spento × iPhone SE, telefono grande, tablet, PC, TV, con `prove/prova_schermi_56.js` e `temi/prova_evento.js`; la Curva ha la sua grafica iPhone/Android da rispettare.
6. **Pubblicazione:** serve il «Vai, pubblica» di Gianluca prima del 18. L'inclusione in `tv.js` va fatta con lo script di rilascio (stesso schema di `rilascio/r624/`), con `tv.js?v=…` nuovo; la 6.2.4 è online da stanotte.
