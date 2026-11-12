# Video della giornata, strada B (Remotion)

Prova del 12 novembre 2026 (Claude). Installazione in una cartella a parte:
`npm i remotion@4.0.300 @remotion/cli@4.0.300 @remotion/renderer@4.0.300 @remotion/bundler@4.0.300 react@18.3.1 react-dom@18.3.1`

I caratteri (Inter e Lobster, licenza libera OFL) vanno scaricati in `public/font/` e il logo in `public/logo.png` (lo fa `render.mjs` per il logo).
Poi `node render.mjs PERCORSO_DI_CHROME_HEADLESS_SHELL`: legge `data.json` del sito e scrive il video.
