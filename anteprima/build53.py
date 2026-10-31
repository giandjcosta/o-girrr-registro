"""Costruzione della 5.3 dalle pagine conservate, dal Lab e dal Tabellone completo."""
import re, json, sys
from pathlib import Path
from urllib.parse import urljoin
R=Path(__file__).resolve().parent.parent
SITO='https://giandjcosta.github.io/o-fant-a-girrr/'
OLD='https://raw.githack.com/giandjcosta/o-girrr-registro/chatgpt/anteprima-53-integrata/anteprima/5.3/'

def converti(s,skin):
    base=SITO+('girrr/' if skin=='lega' else 'stadio/girrr/')
    s=s.replace(OLD,'')
    s=re.sub(r'<base\b[^>]*>','',s)
    s=re.sub(r'<script>\/\* Anteprima 5\.3: protezione.*?</script>','',s,flags=re.S)
    s=re.sub(r'<script[^>]*src="[^"]*(?:ospite|transizioni|barra|grafica|auth-ingresso|goatcounter|app)\.js[^\"]*"[^>]*></script>','',s)
    local={'index.html':'index-'+skin+'.html','tabellone.html':'tabellone-'+skin+'.html',
           'albo.html':'albo-'+skin+'.html','curva.html':'curva-'+skin+'.html',
           'notifiche.html':'notifiche-'+skin+'.html'}
    def attr(m):
        key,u=m.groups()
        if u.startswith(('#','data:','mailto:',"'+",'"+')):return m[0]
        if u.startswith(('ui.js','ui.css','../preview-guard.js')) or re.match(r'(index|tabellone|albo|curva|notifiche|campo)-(lega|stadio)\.html',u):return m[0]
        file=u.split('?')[0].split('#')[0]
        if key=='href' and file in local:return key+'="'+u.replace(file,local[file],1)+'"'
        return key+'="'+urljoin(base,u)+'"'
    s=re.sub(r'\b(src|href)="([^"]+)"',attr,s)
    s=re.sub(r"fetch\('([^']+)'",lambda m:"fetch('"+urljoin(base,m[1])+"'" if not m[1].startswith(('http','#','data:')) else m[0],s)
    s=s.replace('<head>','<head><script src="../preview-guard.js"></script>',1)
    # Native return links are handled locally before the original page listeners.
    s=s.replace('</head>','<link rel="stylesheet" href="ui.css?v=53d"><script src="ui.js?v=53d" defer></script></head>',1)
    # Drop the old tail script; the single deferred script sees currentScript at execution.
    s=re.sub(r'<script src="ui.js\?v=53c"></script>','',s)
    s=re.sub(r"\.src='(?:\.\./)+'\+", ".src='"+SITO+"'+", s)
    s=re.sub(r"'(?:\.\./)+assets/", "'"+SITO+"assets/", s)
    return s.replace('sponsor-wegwezen.png','sponsor-wegwezen-reizen.png')

def genera53():
    out=R/'anteprima/5.3';templates=R/'anteprima/sorgenti/53'
    sys.path.insert(0,str(R/'calcoli'))
    from zone_classifica import eventi, _giornate
    dati=json.loads((R/'anteprima/dati/calendario-stagione.json').read_text())
    att=json.loads((R/'calcoli/aspettative.json').read_text())
    def numero_js(x):
        if isinstance(x,float) and x.is_integer():return int(x)
        if isinstance(x,list):return [numero_js(v) for v in x]
        if isinstance(x,dict):return {k:numero_js(v) for k,v in x.items()}
        return x
    firma=json.dumps(numero_js([{'n':g['n'],'m':g['m']} for g in _giornate(dati)]),ensure_ascii=False,separators=(',',':'))
    (out/'cronache.json').write_text(json.dumps({'firma':firma,'eventi':eventi(dati,att),'aggiornato':dati.get('updated')},ensure_ascii=False,indent=2))
    for skin in ('lega','stadio'):
        for page in ('index','curva','notifiche'):
            s=converti((templates/f'{page}-{skin}.html').read_text(),skin)
            (out/f'{page}-{skin}.html').write_text(s)
        t=(R/f'anteprima/tabellone-{skin}.html').read_text()
        t=t.replace('<body data-mode="lega">',f'<body data-mode="lega" data-v53="board" data-v53-skin="{skin}">')
        t=t.replace('<div class="swap" id="board"></div>','<div class="swap" id="board"></div>'+(templates/'approfondimenti.html').read_text())
        t=t.replace('home-'+skin+'.html','index-'+skin+'.html').replace('href="campo.html?', 'href="campo-'+skin+'.html?').replace("'campo.html?","'campo-"+skin+".html?")
        t=converti(t,skin)
        (out/f'tabellone-{skin}.html').write_text(t)
        # L'Albo completo proviene dalla stessa build del Lab: tutte le tab e i record conservati.
        a=(R/('anteprima/attuale.html' if skin=='lega' else 'anteprima/index.html')).read_text()
        a=a.replace('<!doctype html>',f'<!doctype html><html lang="it"><head><base href="../"><script src="preview-guard.js"></script><link rel="stylesheet" href="5.3/ui.css?v=53d"><script src="5.3/ui.js?v=53d" defer></script>',1)
        a=a.replace('<div class="col">',f'</head><body data-v53="albo" data-v53-skin="{skin}"><div class="col">',1)
        a+='</body></html>'
        a=a.replace('home-'+skin+'.html','5.3/index-'+skin+'.html')
        # This dedicated page opens Albo even without a hash, like the original Albo page.
        a=a.replace("var hh=(location.hash||'').slice(1);","var hh=(location.hash||'#oro').slice(1);")
        (out/f'albo-{skin}.html').write_text(a)
        c=(R/'anteprima/campo.html').read_text()
        c=c.replace('<body data-skin="stadio">',f'<body data-skin="{skin}" data-v53="campo" data-v53-skin="{skin}">')
        c=c.replace('home-'+skin+'.html','index-'+skin+'.html')
        c=c.replace("'home-'+s+'.html'","'index-'+s+'.html'")
        c=c.replace('href="tabellone-stadio.html"',f'href="tabellone-{skin}.html"')
        (out/f'campo-{skin}.html').write_text(c)
