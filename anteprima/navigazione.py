"""Build delle pagine navigabili 5.3; nessuna scrittura nelle sorgenti ufficiali."""
import re
from pathlib import Path
from urllib.parse import urljoin
R = Path(__file__).resolve().parent.parent
SITO = 'https://giandjcosta.github.io/o-fant-a-girrr/'

def risorse(s, base, links):
    s = re.sub(r'<base\b[^>]*>', '', s)
    # Script che riscrivono link o avviano sessioni/telemetria non appartengono alla preview.
    s = re.sub(r'<script[^>]+src="[^"]*(?:ospite|transizioni|barra|grafica|auth-ingresso|novita-badge|novita-dati|novita)\.js[^\"]*"[^>]*></script>', '', s)
    def attr(m):
        key, u = m.groups()
        if key == 'href':
            for source, dest in links.items():
                if u == source or u.startswith(source+'#'):
                    return f'{key}="{dest}{u[len(source):]}"'
        if u.startswith(('#', 'data:', 'mailto:')):
            return m.group(0)
        return f'{key}="{urljoin(base,u)}"'
    return re.sub(r'\b(src|href)="([^"]+)"', attr, s)

def genera():
    for skin in ('lega','stadio'):
        app = 'attuale.html' if skin=='lega' else 'index.html'
        home, tab = f'home-{skin}.html', f'tabellone-{skin}.html'
        base = SITO+('girrr/' if skin=='lega' else 'stadio/girrr/')
        links = {'./':home, 'index.html':home, 'tabellone.html':tab,
                 'albo.html':app+'#oro', 'app.html':app,
                 '../../anteprima/'+app:app, 'giornale.html':app+'#sport',
                 'totogirrr.html':'totogirrr-52.html?skin='+skin,
                 SITO+'index.html':app+'#spog'}
        h = (R/f'anteprima/sorgenti/home-{skin}.html').read_text()
        h = risorse(h,base,links)
        # Le Home conservano card, ordine e struttura originale; logo e link restano nella preview.
        h = h.replace('sponsor-wegwezen.png','sponsor-wegwezen-reizen.png')
        h = h.replace('</body>', '<script src="home-preview.js"></script></body>')
        h = h.replace('<title>', '<title>Anteprima 5.3 · ',1)
        h = h.replace('</body>', f'<nav class="preview-skin" aria-label="Grafica"><a href="home-lega.html">Grafica Lega</a> · <a href="home-stadio.html">Grafica Stadio</a> · <a href="../lab/index.html">Laboratorio</a></nav><style>.preview-skin{{padding:24px;text-align:center}}.preview-skin a{{color:#ffd166}}</style></body>')
        (R/'anteprima'/home).write_text(h)
        t = (R/f'lab/prova-tabellone-{skin}.html').read_text()
        t = risorse(t,base,links)
        t = t.replace("location.href='index.html'", "location.href='"+home+"'")
        t = t.replace("fetch('../data.json'", "fetch('"+SITO+"data.json'")
        t = t.replace('<div class="sw" role="tablist">',f'<nav class="giornata-nav" aria-label="Giornata"><a aria-current="page" href="{tab}">Risultati e classifica</a><a id="campo-link" href="campo.html?skin={skin}">Campo · Centro della giornata ›</a></nav><div class="sw" role="tablist">')
        t = t.replace('function render(){',f'''function render(){{
  var campoLink=document.getElementById('campo-link');if(campoLink){{campoLink.href='campo.html?skin={skin}&giornata='+sel.lega;campoLink.hidden=mode==='coppa'}}''')
        t = t.replace('</style>', '''.giornata-nav [hidden]{display:none!important}.giornata-nav{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}.giornata-nav a{display:block;padding:12px;border:1px solid #7888a8;border-radius:10px;color:inherit;text-decoration:none;font-weight:800}.giornata-nav a[aria-current]{border-color:var(--acc)}.panel tr.me td.n{box-shadow:inset 0 -2px var(--acc)}.panel td.n{white-space:normal;overflow:visible;text-overflow:clip}.panel td.fp{white-space:nowrap}@media(min-width:1150px){.wrap{max-width:1420px}.grid{grid-template-columns:minmax(0,.7fr) minmax(0,1.5fr)}.panel th{font-size:14px}.panel td.n{font-size:15px}}@media(max-width:359px){.wrap{padding-left:9px;padding-right:9px}.panel{padding:10px}.panel th:last-child{white-space:normal;overflow-wrap:anywhere;max-width:65px}}
</style>''',1)
        (R/'anteprima'/tab).write_text(t)
        a = (R/'anteprima'/app).read_text()
        a = a.replace('../ufficiale/nuovo/girrr/index.html',home).replace('../ufficiale/girrr/index.html',home)
        a = re.sub(r"var dir=lab\?.*?;", "var dir='';", a, count=1)
        a = a.replace("else href=dir+pr+'.html';", f"else href=pr==='index'?'{home}':dir+pr+'.html';")
        a = a.replace("href=dir+'totogirrr.html'", f"href='totogirrr-52.html?skin={skin}'")
        # Niente script che sostituisca nuovamente i ritorni alla Home.
        a = a.replace('<script src="../ufficiale/girrr/barra.js"></script>','')
        (R/'anteprima'/app).write_text(a)
    c = (R/'lab/prova-dashboard-campo.html').read_text()
    c = c.replace('href="index.html">‹ Torna al Lab','id="ritorno-tabellone" href="tabellone-stadio.html">‹ Tabellone')
    c = c.replace('</body>', '''<script>function aggiornaRitorni(){var s=document.body.dataset.skin;document.getElementById('ritorno-tabellone').href='tabellone-'+s+'.html#lega-'+(new URLSearchParams(location.search).get('giornata')||1);document.querySelectorAll('[data-home]').forEach(function(a){a.href='home-'+s+'.html'})}aggiornaRitorni();document.addEventListener('click',function(){setTimeout(aggiornaRitorni,0)})</script></body>''')
    (R/'anteprima/campo.html').write_text(c)
