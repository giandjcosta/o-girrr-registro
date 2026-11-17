# Vice City Edition — revisione fotografica del 17 novembre 2026

## Feedback ricevuto
- Sfondo SVG a rettangoli troppo generico: sostituire con fotografie autentiche.
- Riferimenti UI: liste partita con grandi numeri e griglie cromatiche; scoreboard viola con dati chiari.
- Tipografia: il titolo decorativo deve avere un corsivo neon Vice City, non soltanto condensato.

## Modifiche effettivamente fatte
- File `temi/anteprima-home.html`: rimosso skyline SVG; background fotografico con selettore Tramonto / Ocean Drive notte; corsivo Yellowtail per il titolo Vice City, Barlow Condensed per la parte sportiva; attribuzioni e gradiente per leggibilità.
- **Sorgente tramonto**: Denys Kostyuchenko, Miami Beach, Unsplash License, https://unsplash.com/photos/silhouette-of-palm-trees-near-body-of-water-during-sunset-FQjUaIMQF3Q
- **Sorgente notturna**: Luis Erives, Ocean Drive, Pexels License, https://www.pexels.com/photo/people-on-street-near-illuminated-nightclubs-11457824/
- Licenze: https://unsplash.com/license e https://www.pexels.com/license/ . Entrambe autorizzano l'utilizzo e le modifiche, ma non implicano affiliazione ai brand ritratti.
- Le immagini vengono temporaneamente caricate dai CDN esterni, non ancora archiviate in asset locali. Prima di un eventuale rilascio verificare performance, CORS/hotlink e fallback.

## Regole per i prossimi passi
1. Pinterest solo come moodboard: non presume una licenza per riutilizzare i file.
2. Artwork e screenshot GTA VI originali restano di Rockstar: non trattarli come immagini royalty-free. Solo ispirazione per la direzione artistica o altro uso previa verifica dei permessi.
3. Il corsivo decorativo serve per il titolo 'Vice City'; pulsanti, numeri, partite e statistica restano in font bold ad alta leggibilità.
4. Applicare al Tabellone le griglie colorate ispirate al riferimento rosa, con scoreboard compatto e fondo viola in vista dei dati del secondo esempio.
5. Proseguire esclusivamente nel branch sperimentale. Lega e Stadio permanenti invariati. Nessun merge/deploy o Supabase senza approvazione.

## Verifiche
- Controllo statico della homepage GitHub: SVG rimosso, due URL immagine, import font, selettori sfondo, listener JS, crediti e theme engine presenti.
- **Non eseguiti in questa sessione**: caricamento effettivo foto su browser, screenshot reali, test mobile, Playwright, compatibilità accessibilità, confronto in Lab.
- Preview nel browser possibile tramite visualizzatore statico di branch: https://raw.githack.com/giandjcosta/o-girrr-registro/ec88c9d0f6840c94d17a7554d4720564353e990d/temi/anteprima-home.html (non verificato qui).
