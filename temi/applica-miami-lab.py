#!/usr/bin/env python3
"""17/11/2026 ChatGPT: applica lo stile Miami Nights alle copie REALI nel Lab.
L'operazione e' idempotente e limitata alle 4 pagine canoniche del Lab.
La sorgente del tema e' temi/miami-ui.css + temi/miami-nav.js.
Non tocca originale di Claude, sito pubblico, database, workflow e rilasci."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILENAMES = ('index.html', 'tabellone.html', 'app.html', 'totogirrr.html')

def main():
    count = 0
    for skin in ('girrr',):
        prefix = '../../../'
        for name in FILENAMES:
            p = ROOT / 'lab' / 'integrata-62' / skin / name
            if not p.is_file():
                raise FileNotFoundError(p)
            html = p.read_text(encoding='utf-8')
            if 'data-miami-ui' in html:
                continue
            if '</head>' not in html:
                raise RuntimeError('Manca </head>: ' + str(p))
            html = html.replace(
                '</head>',
                '<!-- Miami Nights (ChatGPT 17/11/2026): SOLO questa copia Lab, non produzione -->\n'
                '<link data-miami-ui rel="stylesheet" href="' + prefix + 'temi/miami-ui.css">\n'
                '<script defer data-miami-ui src="' + prefix + 'temi/miami-nav.js"></script>\n'
                '</head>', 1
            )
            p.write_text(html, encoding='utf-8')
            count += 1
    print('Miami Nights · pagine aggiornate:', count)

if __name__ == '__main__':
    main()
