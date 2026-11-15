#!/usr/bin/env python3
"""6.2 · Giornale: solo la rubrica «MVP dei tifosi» (Claude, 15 novembre 2026).

Decisione di Gianluca: il Giornale resta quello di oggi, con la sua grafica, i suoi caratteri e i suoi spazi.
Si aggiunge soltanto, in fondo alla pagina 2, la rubrica «MVP dei tifosi»: la vincitrice della giornata precedente
(storia più lunga, con il capolettera rosso, Campionato e Coppa insieme) e le tre candidate della giornata appena finita.
Vale dal prossimo Giornale: i numeri già usciti non si rigenerano. Il Coro della Curva non cambia.
Niente spazi compattati, niente Top/Flop su quattro colonne: se la pagina non basta, interviene il normale
controllo di impaginazione del generatore, come sulle altre pagine.

Uso:  python3 rilascio/r62/giornale_mvp.py COPIA_DI_GH_PAGES
Modifica scripts/pdf_giornale.py e aggiunge scripts/mvp_giornale62.py (candidati da girrr/dati/mvp-editoriale.json).
Si ferma se il generatore non è quello atteso; rieseguito non cambia niente.
"""
import pathlib, sys

QUI = pathlib.Path(__file__).resolve().parent
SEGNO = "data-rubrica-mvp"

DATI_OLD = "    # Cronache 5.5: arricchisce una copia prima della normale impaginazione."
DATI_NEW = ("    # 6.2: candidati MVP dei tifosi della giornata appena finita (solo se la votazione è aperta)\n"
            "    from mvp_giornale62 import integra as integra_mvp\n"
            "    dossier = ROOT / 'girrr/dati/mvp-editoriale.json'\n"
            "    if dossier.exists():\n"
            "        ultima = max((x['n'] for x in D['cal']['lega'] if giocata(x)), default=0)\n"
            "        t = integra_mvp(t, json.loads(dossier.read_text(encoding='utf-8')), ultima, D=D)\n" + DATI_OLD)
RUB_OLD = '    h.append(piede(2) + "</section>")'
RUB_NEW = '''    mvp = t.get('mvp_editoriale')
    if mvp and (mvp.get('candidati') or mvp.get('verdetto')):   # 6.2: rubrica MVP dei tifosi, stessi stili della pagina
        h.append('<div class="tab" data-rubrica-mvp><style>[data-rubrica-mvp] .txt:first-letter{color:var(--ink)}</style><h2>MVP <b>dei tifosi</b></h2>')   # capolettera nero: separa dai titoletti rossi (Gianluca)
        v = mvp.get('verdetto')
        if v:   # la vincitrice della giornata precedente, con il capolettera rosso
            h.append('<div class="gr">La vincitrice della ' + str(v['giornata']) + 'ª giornata</div>')
            h.append('<p class="txt">' + esc(v['testo']) + '</p>')
        if mvp.get('candidati'):
            h.append('<div class="gr"' + (' style="clear:both;margin-top:3mm;padding-top:2.2mm;border-top:.3mm solid var(--rule)"' if v else '') + '>Le candidate della ' + str(mvp['giornata']) + 'ª giornata</div>')
            h.append('<div style="clear:both;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4mm">')
            for c in mvp['candidati']:
                h.append('<div style="font-size:9.6pt;line-height:1.42"><b>' + esc(cap(c['squadra'])) + '</b><br>' + esc(c['testo']) + '</div>')
            h.append('</div>')
        h.append('</div>')
''' + RUB_OLD


def applica(base):
    p = base / "scripts" / "pdf_giornale.py"
    s = p.read_text(encoding="utf-8")
    if SEGNO not in s:
        for vecchio, nome in ((DATI_OLD, "lettura dei testi"), (RUB_OLD, "piede della pagina 2")):
            if s.count(vecchio) != 1:
                raise SystemExit(f"pdf_giornale.py diverso da quello atteso ({nome})")
        s = s.replace(DATI_OLD, DATI_NEW).replace(RUB_OLD, RUB_NEW)
        p.write_text(s, encoding="utf-8")
    (base / "scripts" / "mvp_giornale62.py").write_text((QUI / "editoriale" / "mvp_giornale62.py").read_text(encoding="utf-8"), encoding="utf-8")
    print("Giornale: rubrica MVP aggiunta in", p)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    applica(pathlib.Path(sys.argv[1]).resolve())
