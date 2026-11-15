#!/usr/bin/env python3
"""6.2 · Due ritocchi chiesti da Gianluca (Claude, 15 novembre 2026).

- Tabellone › Dentro la partita (girrr/v55/ui.js, usato da Lega e Stadio): «= Stessa posizione» con la maiuscola
  dopo il simbolo, e «1 posizione» al singolare (prima «↑ 1 posizioni»).
- Albo › La Storia (girrr/novita.js e stadio/girrr/novita.js): i Padri Fondatori solo con il nome, tutti in fila,
  senza la squadra di oggi. Il testo della Storia non cambia.
- Tabellone › Risultati: la tua partita al suo posto, con un leggero velo oro e «La tua partita», senza contorno.
- Tabellone dello Stadio: tutto oro (interruttore, giornata scelta, bande, podio), in Campionato e in Coppa; sfondi azzurrati e rosati invariati.

Uso come campo_coppa.py:  python3 rilascio/r62/testi.py COPIA_DI_GH_PAGES   oppure   --lab
"""
import pathlib
import sys

QUI = pathlib.Path(__file__).resolve().parent
REG = QUI.parent.parent

POS_OLD = "(d>0?'↑ '+d+' posizioni':d<0?'↓ '+(-d)+' posizioni':'= stessa posizione')"
POS_NEW = "(d>0?'↑ '+d+(d===1?' posizione':' posizioni'):d<0?'↓ '+(-d)+(d===-1?' posizione':' posizioni'):'= Stessa posizione')"
PF_OLD = "STORIA.f.map(function(x){return '<div><b>'+esc(x[0])+'</b><small>'+esc(x[1])+'</small></div>'})"
PF_NEW = "STORIA.f.map(function(x){return '<div><b>'+esc(x[0])+'</b></div>'})"
CSS_OLD = ".sto-f{display:grid;grid-template-columns:repeat(auto-fill,minmax(105px,1fr));gap:8px;margin:10px 0 14px}"
CSS_NEW = ".sto-f{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:8px;margin:10px 0 14px}.sto-f div{text-align:center}"

# Tabellone › Risultati: la partita di chi entra col codice resta al suo posto, con un leggero velo oro e «La tua partita» (niente contorno). Albo e Derby restano senza oro.
TAB_M_OLD = "b+='<div class=\"m'+(cup?' cp':'')+(tg.length?' dby':'')+'\""
TAB_M_NEW = "b+='<div class=\"m'+(cup?' cp':'')+(tg.length?' dby':'')+(ME&&(casa===ME||fuori===ME)?' tua':'')+'\""
TAB_CSS_OLD = "</head>"
TAB_CSS_NEW = ("<style>/* 6.2: la tua partita con un leggero velo oro */"
               "#board>.m.tua{position:relative;background-image:linear-gradient(90deg,rgba(255,209,102,.17),rgba(255,209,102,.05))!important}"
               "#board>.m.tua::before{content:'La tua partita';position:absolute;top:6px;left:18px;font:900 9px/1 Inter,system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#ffd166}"
               "</style></head>")
SW_OLD = "background:var(--acc);transition:transform .55s"
SW_NEW = "background:#ffd166;transition:transform .55s"  # 6.2: nello Stadio l'interruttore è oro in Campionato e in Coppa (regola di Gianluca, 15 novembre)
SWT_OLD = "</head>"
SWT_NEW = ("<style>/* 6.2 · Stadio tutto oro (Gianluca, 15 novembre): accento oro in Campionato e Coppa, sfondi azzurrati e rosati invariati; testo scuro sull'oro */"
           "body,body[data-mode]{--acc:#ffd166;--hi:#ffd166}"
           ".sw button[aria-selected=true],.chips button.sel,tr.pod td.p{color:#1d2a52;transition:color .3s ease .15s}"
           "body .v55-schede>button[aria-selected=true],body[data-mode=coppa] .v55-schede>button[aria-selected=true]{background:#ffd166;color:#1d2a52}</style></head>")
LAVORI = {
    'girrr/v55/ui.js': [(POS_OLD, POS_NEW)],
    'girrr/novita.js': [(PF_OLD, PF_NEW), (CSS_OLD, CSS_NEW)],
    'stadio/girrr/novita.js': [(PF_OLD, PF_NEW), (CSS_OLD, CSS_NEW)],
    'girrr/tabellone.html': [(TAB_M_OLD, TAB_M_NEW), (TAB_CSS_OLD, TAB_CSS_NEW)],
    'stadio/girrr/tabellone.html': [(TAB_M_OLD, TAB_M_NEW), (TAB_CSS_OLD, TAB_CSS_NEW), (SW_OLD, SW_NEW), (SWT_OLD, SWT_NEW)],
}


def applica(t, nome, coppie):
    for vecchio, nuovo in coppie:
        if nuovo in t:
            continue
        if t.count(vecchio) != 1:
            raise SystemExit('%s: atteso una volta «%s…», trovato %d volte' % (nome, vecchio[:50], t.count(vecchio)))
        t = t.replace(vecchio, nuovo)
    return t


def main(argv):
    if argv == ['--lab']:
        coppie = [(REG / 'ufficiale/src/sito' / p, QUI / 'pagine' / p, p) for p in LAVORI]
    elif len(argv) == 1:
        coppie = [(pathlib.Path(argv[0]) / p, pathlib.Path(argv[0]) / p, p) for p in LAVORI]
    else:
        raise SystemExit(__doc__)
    uscite = [(dst, applica(src.read_text(encoding='utf-8'), str(src), LAVORI[p])) for src, dst, p in coppie]
    for dst, t in uscite:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(t, encoding='utf-8')
        print('Scritto', dst)


if __name__ == '__main__':
    main(sys.argv[1:])
