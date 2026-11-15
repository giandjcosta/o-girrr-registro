"""Rubrica MVP autonoma nel Giornale a quattro pagine, senza ridurre i caratteri."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def prepara(base):
    p=base/'scripts/pdf_giornale.py';s=p.read_text()
    marker='    # Cronache 5.5: arricchisce una copia prima della normale impaginazione.'
    if 'from mvp_giornale62 import integra as integra_mvp' not in s:
        if s.count(marker)!=1:raise ValueError('Generatore PDF diverso dalla base certificata')
        s=s.replace(marker,"    from mvp_giornale62 import integra as integra_mvp\n    dossier = ROOT / 'girrr/dati/mvp-editoriale.json'\n    if dossier.exists():\n        ultima = max((x['n'] for x in D['cal']['lega'] if giocata(x)), default=0)\n        t = integra_mvp(t, json.loads(dossier.read_text()), ultima)\n"+marker)
    anchor='    h.append(piede(2) + "</section>")'
    if 'data-rubrica-mvp' not in s:
        if s.count(anchor)!=1:raise ValueError('Pagina delle classifiche diversa dalla base attesa')
        s=s.replace(anchor,'''    mvp = t.get('mvp_editoriale')
    if mvp:
        h.append('<div class="tab" data-rubrica-mvp><h2>MVP <b>dei tifosi</b></h2>')
        if mvp.get('verdetto'):h.append('<p class="txt">'+esc(mvp['verdetto'])+'</p>')
        if mvp.get('candidati'):
            h.append('<div class="gr">'+str(mvp['giornata'])+'ª giornata · Tre candidature, premio ancora da assegnare</div>')
            h.append('<div class="cols" style="grid-template-columns:repeat(3,minmax(0,1fr));gap:4mm">')
            for c in mvp['candidati']:h.append('<div class="mvp-candidato" style="font-size:9.6pt;line-height:1.42"><strong>'+esc(cap(c['squadra']))+'</strong><br>'+esc(c['testo'])+'</div>')
            h.append('</div>')
        h.append('</div>')
'''+anchor)
    if 'mvp-griglia' not in s:
        s=s.replace("'<div class=\"gr\" style=\"margin-top:0\">I top</div>'", "('<div class=\"mvp-griglia\" style=\"display:grid;grid-template-columns:1fr 1fr;gap:0 3mm\"><div class=\"gr\" style=\"margin-top:0;grid-column:1/-1\">I top</div>' if t.get('mvp_editoriale') else '<div class=\"gr\" style=\"margin-top:0\">I top</div>')")
        s=s.replace('        h.append("</div><div>")\n        if flop:', '        h.append(("</div>" if t.get("mvp_editoriale") else "")+"</div><div>")\n        if flop:')
        s=s.replace("'<div class=\"gr\" style=\"margin-top:0\">I flop</div>'", "('<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:0 3mm\"><div class=\"gr\" style=\"margin-top:0;grid-column:1/-1\">I flop</div>' if t.get('mvp_editoriale') else '<div class=\"gr\" style=\"margin-top:0\">I flop</div>')")
        s=s.replace('        h.append("</div></div></div>")\n    mvp =', '        h.append(("</div>" if t.get("mvp_editoriale") else "")+"</div></div></div>")\n    mvp =')
    if 'mvp-spazi' not in s:
        a="    # ---------- pagina 2: classifiche e migliori"
        s=s.replace(a,a+"\n    if t.get('mvp_editoriale'):h.append('<style id=\"mvp-spazi\">.pg:nth-of-type(2) .tab{margin-top:2mm}.pg:nth-of-type(2) .tab h2{margin:.8mm 0}.pg:nth-of-type(2) td{padding-top:.55mm;padding-bottom:.55mm}</style>')")
    p.write_text(s);(base/'scripts/mvp_giornale62.py').write_text((R/'rilascio/r62/editoriale/mvp_giornale62.py').read_text())
if __name__=='__main__':
    import sys
    prepara(Path(sys.argv[1]).resolve())
