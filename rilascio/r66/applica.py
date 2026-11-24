#!/usr/bin/env python3
"""6.6 «Scambi nell'app» (Claude, 24 novembre 2026, decisioni di Gianluca): applica le pagine della 6.6 a una copia di gh-pages.

- Spogliatoio (index.html): in «Mercato Scambi» l'elenco «Richieste di scambio» e, in «Valuta uno scambio», il pulsante
  «Effettua lo scambio» quando lo scambio è valido (stessi ruoli, stesso numero, niente crediti). Codice in assets/scambi66.js.
- Notifiche (Lega e Stadio): le notifiche degli scambi portano alla richiesta nello Spogliatoio; filtro «Scambi»;
  sul telefono la nuova voce «Scambi» (accesa di base).
- Loghi: rilascio/loghi-66/applica.py (scudi per sempre, simboli della stagione 2026 · 27).
- Icona dell'app: rilascio/r66/icona.py (scudo o simbolo, a scelta nella pagina Notifiche).

Il database serve per gli scambi veri: sql/scambi-66.sql, da applicare solo con il «Vai» di Gianluca. Senza, la pagina dice
che gli scambi si attivano con la 6.6 e non manda niente.

Uso: python3 rilascio/r66/applica.py CARTELLA_GH_PAGES   (idempotente: la seconda volta «File cambiati: 0»)
"""
import json
import pathlib
import runpy
import shutil
import sys

R = pathlib.Path(__file__).resolve().parents[2]
QUI = pathlib.Path(__file__).resolve().parent

SPOGLIATOIO = [
    # pulsante sotto la valutazione, solo quando lo scambio è valido
    ("mkCard({G:G.map(function(i){return Ab.filter(function(v){return v.id===i})[0]}),R:R.map(function(i){return Bb.filter(function(v){return v.id===i})[0]}),k:G.length,gA:cur.gA,gB:cur.gB,o:oth},mkT)+'</div>';",
     "mkCard({G:G.map(function(i){return Ab.filter(function(v){return v.id===i})[0]}),R:R.map(function(i){return Bb.filter(function(v){return v.id===i})[0]}),k:G.length,gA:cur.gA,gB:cur.gB,o:oth},mkT)+'</div>'+(window.SC66btn?window.SC66btn(mkT,G,R):'')/* 6.6 */;"),
    # elenco delle richieste in cima a Mercato Scambi
    ("  h+='<div class=\"seg\">'+[['c','Consigliati']",
     "  if(window.SC66box)h+=window.SC66box();/* 6.6: Richieste di scambio */\n  h+='<div class=\"seg\">'+[['c','Consigliati']"),
    # quello che serve a assets/scambi66.js, senza esporre altro
    ("byHash();render();\n",
     "/* 6.6: scambi nell'app (assets/scambi66.js) */window.SC66={ctx:function(){return {team:team,code:LS.code||'',authed:authed(),D:D}},apri:function(){tab='mkt';mkV='c';render()},fatto:function(){mkSG=[];mkSR=[];mkV='c';render()}};\nbyHash();render();\n"),
    ('<script src="assets/app.js"></script>', '<script src="assets/scambi66.js?v=66"></script>\n<script src="assets/app.js"></script>'),
]

DEST = [(" }else if(/^sfida-(r-)?\\d+$/.test(k)){u=new URL(OG55.pagina('app',s,base));if(!OG55.sito)u.searchParams.set('skin',s);u.hash='sport'}\n",
         " }else if(/^sfida-(r-)?\\d+$/.test(k)){u=new URL(OG55.pagina('app',s,base));if(!OG55.sito)u.searchParams.set('skin',s);u.hash='sport'}\n"
         " else if(/^sc-(ok-|no-)?\\d+$/.test(k)){u=new URL('../index.html',OG55.dir('lega'));u.searchParams.set('scambio',k.replace(/\\D+/g,''))}/* 6.6: richiesta di scambio nello Spogliatoio */\n")]
UI = [("['totogirrr','Totogirrr'],['albo','Albo']", "['totogirrr','Totogirrr'],['scambi','Scambi'],['albo','Albo']"),
      ("risposte, applausi, sfide, prestiti e Totogirrr", "risposte, applausi, sfide, scambi, prestiti e Totogirrr")]
PUSH = [("    ['totogirrr', 'Totogirrr', 'Prestiti da approvare e movimenti', true]\n",
         "    ['totogirrr', 'Totogirrr', 'Prestiti da approvare e movimenti', true],\n    ['scambi', 'Scambi', 'Richieste di scambio da confermare e scambi ufficiali', true] /* 6.6: sql/scambi-66.sql */\n")]
# Giornale: piccolo riquadro «Mercato» a pagina 3, prima della Bufala. Testo da testi.json («mercato»: righe) oppure, se manca,
# dagli scambi ufficiali arrivati dopo la giornata precedente (girrr/dati/mercato.json, scritto da calcoli/scambi_app.py).
GIORNALE = [
    (".bufala{border:.5mm solid var(--rule);",
     ".merc66{border:.5mm solid var(--rule);border-left:2.2mm solid var(--red);padding:2mm 3.4mm 2.4mm;margin-top:3.4mm}"
     ".merc66 .bk{font-family:var(--hd);font-weight:700;text-transform:uppercase;font-size:8.2pt;letter-spacing:.16em;color:var(--red)}"
     ".merc66 p{font-size:9.4pt;line-height:1.38;margin:1mm 0 0}\n.bufala{border:.5mm solid var(--rule);"),
    ("""        if t.get("bufala"):
            b = t["bufala"]""",
     """        merc = mercato66(t, n)   # 6.6: riquadro Mercato, solo se ci sono scambi ufficiali
        if merc:
            h.append('<div class="merc66"><div class="bk">Mercato · Ufficiale</div>' + "".join(f'<p>{esc(x)}</p>' for x in merc) + '</div>')
        if t.get("bufala"):
            b = t["bufala"]"""),
    ("def costruisci(t, tema=\"classico\"):",
     """def mercato66(t, n):
    \"\"\"6.6: righe del riquadro Mercato. testi.json «mercato» (lista di frasi) se c'è, altrimenti gli scambi ufficiali
    arrivati dopo la giornata precedente (girrr/dati/mercato.json, scritto da calcoli/scambi_app.py). Livello editoriale.\"\"\"
    if t.get("mercato") is not None:
        return [str(x) for x in t["mercato"] if str(x).strip()]
    f = ROOT / "girrr" / "dati" / "mercato.json"
    if not f.exists():
        return []
    righe = []
    for s in json.loads(f.read_text(encoding="utf-8")).get("scambi") or []:
        if s.get("dopo_giornata") != n - 1:
            continue
        da, a = (x.replace("The Blue brothers", "The Blues Brothers") for x in (s["da"], s["a"]))
        e = lambda l: l[0] if len(l) == 1 else ", ".join(l[:-1]) + " e " + l[-1]
        righe.append(f"{da} e {a} si scambiano {e(s['da_cede'])} e {e(s['a_cede'])}: {e(s['a_cede'])} "
                     f"{'va' if len(s['a_cede']) == 1 else 'vanno'} a {da}, {e(s['da_cede'])} a {a}.")
    return righe


def costruisci(t, tema=\"classico\"):"""),
]
# Il primo scambio della stagione (24 novembre 2026, registrato a mano) entra nel riquadro del Giornale n° 9
MERCATO_INIZIO = {"scambi": [{"id": 0, "dopo_giornata": 8, "quando": "2026-11-24T15:01:27+00:00", "da": "The Blue brothers", "a": "Real Madrink",
                              "da_cede": ["Colpani", "Adams C."], "a_cede": ["Baldanzi", "Kean"], "fonte": "mercato-manuale.json"}]}
VERSIONI = [('destinazioni55.js?v=65n"', 'destinazioni55.js?v=66"'), ('v55/ui.js?v=65"', 'v55/ui.js?v=66"'), ('v55/ui.js?v=65s"', 'v55/ui.js?v=66s"'),
            ('src="../push.js"', 'src="../push.js?v=66"'), ('src="../../push.js"', 'src="../../push.js?v=66"')]


def sostituisci(f, coppie, cambiati, tutte=False):
    t = f.read_text(encoding='utf-8')
    n = t
    for a, b in coppie:
        if b in n:
            continue
        c = n.count(a)
        if c == 0 or (c > 1 and not tutte):
            raise SystemExit('%s: testo atteso trovato %d volte: %s' % (f, c, a[:70]))
        n = n.replace(a, b)
    if n != t:
        f.write_text(n, encoding='utf-8')
        cambiati.add(str(f))


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    sito = pathlib.Path(argv[0]).resolve()
    cambiati = set()
    a = sito / 'assets/scambi66.js'
    if not a.exists() or a.read_bytes() != (QUI / 'scambi66.js').read_bytes():
        shutil.copyfile(QUI / 'scambi66.js', a); cambiati.add(str(a))
    sostituisci(sito / 'index.html', SPOGLIATOIO, cambiati)
    sostituisci(sito / 'girrr/v55/destinazioni55.js', DEST, cambiati)
    sostituisci(sito / 'girrr/v55/ui.js', UI, cambiati)
    sostituisci(sito / 'push.js', PUSH, cambiati)
    sostituisci(sito / 'scripts/pdf_giornale.py', GIORNALE, cambiati)
    m = sito / 'girrr/dati/mercato.json'
    if not m.exists():
        m.write_text(json.dumps(MERCATO_INIZIO, ensure_ascii=False, indent=1) + '\n', encoding='utf-8'); cambiati.add(str(m))
    for rel in ['girrr', 'stadio/girrr']:
        for p in sorted((sito / rel).glob('*.html')):
            t = p.read_text(encoding='utf-8')
            if any(x[0] in t for x in VERSIONI):
                sostituisci(p, [x for x in VERSIONI if x[0] in t], cambiati, tutte=True)
    print('Scambi: file cambiati:', len(cambiati))
    for x in ('rilascio/loghi-66/applica.py', 'rilascio/r66/icona.py'):
        if (R / x).exists():
            sys.argv = [x, str(sito)]
            runpy.run_path(str(R / x), run_name='__main__')


if __name__ == '__main__':
    main(sys.argv[1:])
