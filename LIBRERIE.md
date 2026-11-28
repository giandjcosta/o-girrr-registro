# Librerie esterne

Regole in `REGOLE-LAVORO.md`, sezione 8 (Gianluca, 28 novembre 2026): solo se servono davvero, versione fissata, licenza libera, copia nel sito in `assets/lib/nome-versione/` con la licenza, caricata solo dove serve, e la pagina resta usabile se non si carica.

Una riga per libreria: nome · versione · licenza · dove si usa · perché · chi l'ha aggiunta e quando.

| Libreria | Versione | Licenza | Dove | Perché | Aggiunta |
|---|---|---|---|---|---|

## Già in uso prima della regola (da tenere d'occhio)
- **Playwright e Chromium**: solo per le prove e per i PDF del Giornale (`scripts/pdf_giornale.py`), non nelle pagine.
- **Caratteri Google Fonts** (Inter, Lobster e altri): presi dal sito di Google nelle pagine; Lobster copiato in `scripts/font/` per il Giornale.
- **Workflow della Radio**: `edge-tts`, `numpy`, `scipy`, `google-genai<3`, `google-auth`, `requests` (`radio-giornata.yml` del sito), da fissare con le versioni esatte alla prima occasione.
