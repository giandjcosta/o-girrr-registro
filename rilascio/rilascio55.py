"""Rilascio 5.5 sul sito vero: trasforma le pagine dell'Anteprima 5.5 nelle pagine di gh-pages.

Uso: python3 rilascio/rilascio55.py CARTELLA_GH_PAGES
Scrive soltanto dentro CARTELLA_GH_PAGES (una copia di gh-pages del sito, aggiornata): niente commit, niente push.
Poi: controllare `git diff`, provare la copia servita su /o-fant-a-girrr/ e solo dopo il «vai» fare commit e push.

Cosa fa (Lega in girrr/, Stadio in stadio/girrr/):
  index.html, curva.html      dalla pagina del sito + blocchi 5.5 (modelli in anteprima/sorgenti/53/), senza parti dell'Anteprima
  notifiche.html (nuova)      dal modello delle notifiche 5.5
  tabellone.html              dal Tabellone del Lab (lab/prova-tabellone-*.html) con schede, Campo e approfondimenti
  campo.html (nuova)          dal Campo del Lab (lab/prova-dashboard-campo.html)
  app.html                    dal Lab (build in modalità rilascio) con il foglio e gli script 5.5
  girrr/v55/                  ui.js, ui.css, home55.js, destinazioni55.js, allenatori.json
  girrr/dati/cronache.json    cronache della Home (poi le rinnova il workflow dopo ogni giornata)
  ospite.js, curva-banca.js   modalità ospite e banca dei personaggi ampliata
  index.html (Spogliatoio)    grafica Stadio e menu delle grafiche (rilascio/spogliatoio55.py)
"""
import json, os, re, subprocess, sys, tempfile, shutil
from pathlib import Path

R = Path(__file__).resolve().parent.parent
A5 = R / 'anteprima' / '5.5'
SORG = R / 'anteprima' / 'sorgenti' / '53'
V = '55r1'  # versione dei file comuni (svuota la cache dei browser)
sys.path.insert(0, str(R / 'rilascio'))
sys.path.insert(0, str(R / 'anteprima'))

DIR = {'lega': 'girrr', 'stadio': 'stadio/girrr'}
V55 = {'lega': 'v55/', 'stadio': '../../girrr/v55/'}
PAGINE = {'index': 'index.html', 'tabellone': 'tabellone.html', 'campo': 'campo.html', 'curva': 'curva.html',
          'notifiche': 'notifiche.html', 'albo': 'app.html#oro'}
ATTESA = '<script>document.documentElement.classList.add("v55-attesa");setTimeout(function(){document.documentElement.classList.remove("v55-attesa")},3000)</script>'


def asset_head(skin, home=False):
    v = V55[skin]
    return (f'<link rel="stylesheet" href="{v}ui.css?v={V}">' + (f'<script src="{v}home55.js?v={V}" defer></script>' if home else '') +
            f'<script src="{v}destinazioni55.js?v={V}" defer></script><script src="{v}ui.js?v={V}" defer></script>')


def goat(sito):
    m = re.search(r'<script>window\.goatcounter=.*?</script>\s*<script data-goatcounter=[^>]*>\s*</script>', sito, re.S)
    return m.group(0) if m else ''


def pulisci(s, skin):
    """Toglie tutto ciò che è solo dell'Anteprima e rimette i collegamenti del sito."""
    s = re.sub(r'<base\b[^>]*>', '', s)
    s = re.sub(r'<link\b[^>]*raw\.githack\.com[^>]*>', '', s)
    s = re.sub(r'<script src="https://raw\.githack\.com[^"]*"[^>]*>\s*</script>', '', s)
    s = re.sub(r'<script>/\* Anteprima 5\.[35]: protezione.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<script src="(?:\.\./)*preview-guard\.js"></script>', '', s)
    s = re.sub(r'<div class="v53-banner">.*?</div>', '', s, flags=re.S)
    s = s.replace('Anteprima 5.5 · ', '').replace(' · Anteprima 5.5', '')
    def link(m):
        return PAGINE.get(m.group(1), m.group(1) + '.html')
    s = re.sub(r'https://raw\.githack\.com/giandjcosta/o-girrr-registro/[^"\']*?/anteprima/5\.5/(\w+)-(?:lega|stadio)\.html', link, s)
    return s


def aggiungi_head(s, skin, home=False, attesa=False, sito=''):
    g = goat(sito)
    if g and 'data-goatcounter=' not in s:
        s = s.replace('</head>', g + '</head>', 1)
    if attesa:
        s = s.replace('<head>', '<head>' + ATTESA, 1)
    return s.replace('</head>', asset_head(skin, home) + '</head>', 1)


def da_modello(nome, skin, sito):
    s = pulisci((SORG / f'{nome}-{skin}.html').read_text(encoding='utf-8'), skin)
    if nome == 'curva':
        hook = "var sel={e:undefined,h:null},aimg=null;"
        assert hook in s
        s = s.replace(hook, (R / 'anteprima/sorgenti/53/curva-destinazioni.js').read_text() + '\n' + hook, 1)
        s = s.replace('caricaImg();osserva();', "caricaImg();osserva();if(new URLSearchParams(location.search).has('notifica'))setTimeout(function(){document.dispatchEvent(new Event('og:curva-render'))},0);", 1)
        s = s.replace("return '<div class=\"rp\">'+AV(ra", "return '<div class=\"rp\"'+(r.real?' data-risposta=\"'+esc(r.id)+'\"':'')+'>'+AV(ra", 1)
        s = s.replace('<div class="v53-kicker">LA CURVA · 5.5</div>', '<div class="v53-kicker">LA CURVA</div>')
        s = s.replace('Vota, leggi i personaggi e commenta nello stesso spazio. Solo prova locale.', 'Vota la sfida della prossima giornata, leggi i personaggi e commenta.')
    if nome == 'notifiche':
        s = s.replace('CENTRO NOTIFICHE · 5.5', 'CENTRO NOTIFICHE')
        vecchio = '<h3>Notifiche push</h3><p>Questa è soltanto un’anteprima del centro notifiche. L’invio push reale richiede consenso, salvataggio autenticato e un servizio di recapito: non è attivo e non viene simulato come vero.</p>'
        assert vecchio in s
        s = s.replace(vecchio, '<h3>Notifiche sul telefono</h3><p>Gli avvisi sul telefono arriveranno con una prossima versione. Intanto le novità della Lega e della tua squadra le trovi qui e nella Home.</p>')
    return aggiungi_head(s, skin, home=True, sito=sito)


def tabellone(skin, sito):
    t = (R / f'lab/prova-tabellone-{skin}.html').read_text(encoding='utf-8')
    t = re.sub(r'<base\b[^>]*>', '', t)
    t = t.replace('<div class="sw" role="tablist">', '<nav class="giornata-nav" aria-label="Giornata"><a aria-current="page" href="tabellone.html">Risultati e classifica</a><a id="campo-link" href="campo.html">Campo · Centro della giornata ›</a></nav><div class="sw" role="tablist">', 1)
    hook = 'function render(){'
    assert t.count(hook) == 1
    t = t.replace(hook, """function render(){
  document.querySelectorAll('.sw button').forEach(function(b){b.setAttribute('aria-selected',String(b.dataset.m===mode))});
  var campoLink=document.getElementById('campo-link');if(campoLink){campoLink.href=mode==='coppa'?'campo.html?coppa=1&giornata='+Math.min(sel.coppa,D?D.cal.cup.length:10):'campo.html?giornata='+sel.lega;campoLink.hidden=false}""", 1)
    t = t.replace('</style>', '.giornata-nav [hidden]{display:none!important}.giornata-nav{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}.giornata-nav a{display:block;padding:12px;border:1px solid #7888a8;border-radius:10px;color:inherit;text-decoration:none;font-weight:800}.giornata-nav a[aria-current]{border-color:var(--acc)}.panel td.n{white-space:normal;overflow:visible;text-overflow:clip}.panel td.fp{white-space:nowrap}@media(min-width:1150px){.wrap{max-width:1420px}.grid{grid-template-columns:minmax(0,1fr) minmax(0,1.5fr)}.m{gap:10px;padding:14px}.m .t{font-size:16px;overflow-wrap:normal;word-break:normal}.m .sc b{width:44px;height:58px;font-size:40px}.panel th{font-size:14px}.panel td.n{font-size:15px}}@media(max-width:359px){.wrap{padding-left:9px;padding-right:9px}.panel{padding:10px}.panel th:last-child{white-space:normal;overflow-wrap:anywhere;max-width:65px}}\n</style>', 1)
    assert '<body data-mode="lega">' in t
    t = t.replace('<body data-mode="lega">', f'<body data-mode="lega" data-v53="board" data-v53-skin="{skin}">', 1)
    t = t.replace('<div class="swap" id="board"></div>', '<div class="swap" id="board"></div>' + (SORG / 'approfondimenti.html').read_text(encoding='utf-8'), 1)
    return aggiungi_head(t, skin, attesa=True, sito=sito)


def campo(skin, sito):
    c = (R / 'lab/prova-dashboard-campo.html').read_text(encoding='utf-8')
    c = c.replace('href="index.html">‹ Torna al Lab', 'id="ritorno-tabellone" href="tabellone.html">‹ Tabellone')
    c = c.replace('<title>Campo · Centro della giornata · Lab O Girrr</title>', '<title>Campo · Centro della giornata · O Girrr</title>')
    c = c.replace('</body>', """<script>function aggiornaRitorni(){var q=new URLSearchParams(location.search);document.getElementById('ritorno-tabellone').href='tabellone.html#'+(q.get('coppa')==='1'?'coppa-':'lega-')+(q.get('giornata')||1);document.querySelectorAll('[data-home]').forEach(function(a){a.href='index.html'})}aggiornaRitorni();document.addEventListener('click',function(){setTimeout(aggiornaRitorni,0)})</script></body>""")
    assert '<body data-skin="stadio">' in c
    c = c.replace('<body data-skin="stadio">', f'<body data-skin="{skin}" data-v53="campo" data-v53-skin="{skin}">', 1)
    # la grafica la decide la cartella (Lega o Stadio), non il parametro skin
    c = c.replace("var q=new URLSearchParams(location.search),skin=q.get('skin');if(skin==='lega')document.body.dataset.skin='lega';", "var q=new URLSearchParams(location.search);")
    ic = re.search(r'<link rel="icon"[^>]*>', sito)
    if ic:
        c = c.replace('</head>', ic.group(0) + '</head>', 1)
    return aggiungi_head(c, skin, attesa=True, sito=sito)


def app(skin, sito):
    tmp = Path(tempfile.mkdtemp())
    base = dict(os.environ, APP_MODO='reale', APP_RIL='1')
    if skin == 'lega':
        env = dict(base, APP_DATI='dati/lab-dati.json', APP_VOCI='voci/', APP_MOV='dati/moviola.json', APP_OUT_LEGA=str(tmp / 'a.html'), APP_OUT_STADIO=str(tmp / 'x.html'))
        out = tmp / 'a.html'
    else:
        env = dict(base, APP_DATI='../../girrr/dati/lab-dati.json', APP_VOCI='../../girrr/voci/', APP_MOV='../../girrr/dati/moviola.json', APP_OUT_LEGA=str(tmp / 'y.html'), APP_OUT_STADIO=str(tmp / 'a.html'))
        out = tmp / 'a.html'
    subprocess.check_call([sys.executable, 'anteprima/build.py'], cwd=R, env=env, stdout=subprocess.DEVNULL)
    a = out.read_text(encoding='utf-8')
    import sfondo
    a, _ = sfondo.applica(a)
    assert 'src="../lab/annuario.js"' in a
    a = a.replace('src="../lab/annuario.js"', f'src="{V55[skin]}annuario.js?v={V}"')
    a = re.sub(r'<title>O Girrr · Anteprima 5\.\d+(?: \(grafica attuale\))?</title>', '<title>O Girrr</title>', a)
    # la Cassa resta fuori dalla Carriera del sito, come oggi (decisione di Gianluca)
    a, k = re.subn(r"function vCarr\(\)\{return '<button class=\"btn o\" data-cr=.*?\}\n", 'function vCarr(){return vCar0()}\n', a, count=1, flags=re.S)
    assert k == 1, 'Cassa: definizione di vCarr non trovata'
    assert a.count('<div class="col">') == 1
    a = a.replace('<div class="col">', f'</head><body data-v53="albo" data-v53-skin="{skin}"><div class="col">', 1)
    a = a.replace('<!doctype html>', '<!doctype html><html lang="it"><head>', 1)
    a = aggiungi_head(a, skin, sito=sito) + '</body></html>'
    return a


def main(gh):
    gh = Path(gh)
    scritti = []
    def scrivi(rel, testo):
        p = gh / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(testo, encoding='utf-8')
        scritti.append(rel)
    for skin, d in DIR.items():
        sito_index = (gh / d / 'index.html').read_text(encoding='utf-8')
        sito_tab = (gh / d / 'tabellone.html').read_text(encoding='utf-8')
        scrivi(f'{d}/index.html', da_modello('index', skin, sito_index))
        scrivi(f'{d}/curva.html', da_modello('curva', skin, (gh / d / 'curva.html').read_text(encoding='utf-8')))
        scrivi(f'{d}/notifiche.html', da_modello('notifiche', skin, sito_index))
        scrivi(f'{d}/tabellone.html', tabellone(skin, sito_tab))
        scrivi(f'{d}/campo.html', campo(skin, sito_tab))
        scrivi(f'{d}/app.html', app(skin, (gh / d / 'app.html').read_text(encoding='utf-8')))
        scrivi(f'{d}/ospite.js', (R / f'lab/ospite-prova-{skin}.js').read_text(encoding='utf-8'))
        scrivi(f'{d}/curva-banca.js', (R / 'lab/curva-banca-ampliata.js').read_text(encoding='utf-8'))
    for f in ('ui.js', 'ui.css', 'home55.js', 'destinazioni55.js', 'allenatori.json'):
        scrivi(f'girrr/v55/{f}', (A5 / f).read_text(encoding='utf-8'))
    ann = (R / 'lab/annuario.js').read_text(encoding='utf-8')
    assert "fetch('../ufficiale/src/annuario.json'" in ann
    scrivi('girrr/v55/annuario.js', ann.replace("fetch('../ufficiale/src/annuario.json'", "fetch(new URL('/o-fant-a-girrr/girrr/v55/annuario.json',location.href).href"))
    scrivi('girrr/v55/annuario.json', (R / 'ufficiale/src/annuario.json').read_text(encoding='utf-8'))
    # cronache della Home dai dati veri del sito
    subprocess.check_call([sys.executable, str(R / 'calcoli/cronache_home.py'), str(gh / 'data.json'), str(R / 'calcoli/aspettative.json'), str(gh / 'girrr/dati/cronache.json')])
    scritti.append('girrr/dati/cronache.json')
    # Spogliatoio: grafica Stadio e menu delle grafiche
    subprocess.check_call([sys.executable, str(R / 'rilascio/spogliatoio55.py'), str(gh / 'index.html'), '--sito', str(gh / 'index.html')])
    scritti.append('index.html')
    # nessuna traccia dell'Anteprima nelle pagine pubblicate
    for rel in scritti:
        if rel.endswith('.html'):
            t = (gh / rel).read_text(encoding='utf-8')
            for vietato in ('raw.githack.com', 'preview-guard', 'v53-banner"', 'o-girrr-registro/anteprima'):
                assert vietato not in t, f'{rel}: contiene {vietato}'
    print('Scritti', len(scritti), 'file:')
    for r in scritti:
        print(' ', r)


if __name__ == '__main__':
    main(sys.argv[1])
