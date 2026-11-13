#!/usr/bin/env python3
"""6.0.1 su una copia di gh-pages (Claude, 13 novembre 2026). Richieste di Gianluca dello stesso giorno.

Uso: python3 rilascio/r601/applica.py CARTELLA_GH_PAGES
Non fa commit. Si ferma se una pagina non è quella attesa (copia già preparata o sito cambiato).

1. Carriera (girrr/app.html, stadio/girrr/app.html):
   - l'ospite (o chi non è entrato) sceglie una squadra e vede, in sola lettura, Panoramica, Stagione, Obiettivi, Fiducia
     e «La mia settimana»; niente Promesse, Storia, Regole, premi da riscuotere né «Vai a Totogirrr»;
   - Obiettivi › Linea del tempo dalla 1ª giornata, «L'inizio»;
   - Obiettivi › Premi sponsor con il logo dello sponsor (le stesse immagini SPIMG di Panoramica);
   - spazio della barra di scorrimento sempre riservato (scrollbar-gutter): il riquadro della fiducia non si sposta
     più quando arrivano i dati e compare la barra.
2. «La mia settimana» prima di «Regole» (Regole è sempre l'ultima): girrr/v60/tifosi.js e .css da rilascio/tifosi60/.
3. Spogliatoio (index.html) senza codice: schede pubbliche Infortunati, Svincolati e Calendario, più «Entra» con il codice
   (da ospite niente «Entra»). Statistiche resta solo per Oranje VC. ospite.js non nasconde più lo Spogliatoio.
4. Home della Lega (girrr/index.html): i riquadri grandi uno sotto l'altro, dritti come le partite del Tabellone
   (regola della Lega del 1° novembre); lo Stadio resta in griglia.
5. Derby: in Albo › Derby direttamente tre schede, «Derby della Lega», «Le rivalità» e «Classifica dei Derby»
   (il lavoro lasciato a metà da ChatGPT, rifatto da Claude), senza cambiare pagina (derby.js dentro albo.html).
   derby.html e rivalita.html portano lì, sulla scheda giusta (derby.html#pt-derby apre la Classifica).
6. Condividi la giornata (condividi.js da rilascio/condividi/): foto e video insieme, senza testo, così WhatsApp li mostra
   con l'anteprima in un album; poi, con un secondo tocco, Radio e Giornale. Il Giornale è il PDF intero (tutte le pagine,
   nitido) e non più la copertina sgranata; lo stesso per «Condividi l'ultimo numero».
7. Pillole fluide (pillole.js da rilascio/pillole/, nella radice): in app.html, Albo d'oro e Totogirrr il colore scivola dalla
   pillola di prima alla nuova, la fila non torna indietro, il contenuto entra con una dissolvenza. Girrr Sport: «Squadra della
   settimana» nel menu fin dall'inizio (la fila non salta più). Totogirrr: niente salto in cima né pagina che sparisce.
"""
import os
import shutil
import sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def leggi(p):
    return open(p, encoding='utf-8').read()


def scrivi(p, t):
    open(p, 'w', encoding='utf-8').write(t)


def sost(t, a, b, rel):
    n = t.count(a)
    if n != 1:
        sys.exit('%s: trovato %d volte «%s…»: la pagina non è quella attesa, niente scritto per questo file.' % (rel, n, a[:70]))
    return t.replace(a, b)


PUBBLICHE = "['pan','stag','ob','fid']"

APP = [
    # ospite: la Carriera c'è, con la scelta della squadra
    ("function vCar(){return GUEST?lvGate('La Carriera'):vCarL()}", "function vCar(){return vCarL()}"),
    ("var t=CARSCELTA?S.cteam:ME,",
     "if(GUEST&&!S.cteamOsp){S.cteamOsp=1;S.cteam=D.teams.slice().sort(function(a,b){return row(a).pos-row(b).pos})[0]}"
     "if(GUEST&&" + PUBBLICHE + ".indexOf(S.ctab)<0)S.ctab='pan';"
     "var t=(CARSCELTA||GUEST)?S.cteam:ME,"),
    ("h+=(CARSCELTA?'<select id=\"cteam\"",
     "h+=(GUEST?'<p class=\"sm mut\" style=\"margin:0 0 8px\">Modalità ospite: scegli una squadra e guarda la sua Carriera.</p>':'')+((CARSCELTA||GUEST)?'<select id=\"cteam\""),
    ("+'</p>')+bolla52(t)+carTabs();", "+'</p>')+(GUEST?'':bolla52(t))+carTabs();"),
    ("[['pan','Panoramica'],['stag','Stagione'],['ob','Obiettivi'],['fid','Fiducia'],['prom','Promesse'],['st','Storia'],['reg','Regole']].map(",
     "[['pan','Panoramica'],['stag','Stagione'],['ob','Obiettivi'],['fid','Fiducia'],['prom','Promesse'],['st','Storia'],['reg','Regole']].filter(function(x){return !GUEST||" + PUBBLICHE + ".indexOf(x[0])>=0}).map("),
    ("document.addEventListener('click',function(e){var b=e.target.closest('[data-ctab]');if(!b)return;S.ctab=b.dataset.ctab;render()});",
     "document.addEventListener('click',function(e){var b=e.target.closest('[data-ctab]');if(!b)return;S.ctab=b.dataset.ctab;render()});"
     "document.addEventListener('change',function(e){if(e.target&&e.target.id==='cteam'){S.cteam=e.target.value;render()}});"),
    ("(daRisc?'<a class=\"btn\" href=\"'+esc(torna)+'\"", "(daRisc&&!GUEST?'<a class=\"btn\" href=\"'+esc(torna)+'\""),
    # Linea del tempo dalla 1ª giornata
    ("var scadenze=[2,6,8,10,18,26,34]", "var scadenze=[1,2,6,8,10,18,26,34]"),
    ("var nomi=function(n){var a=[];if(n===8)", "var nomi=function(n){var a=[];if(n===1)a.push('L\\'inizio');if(n===8)"),
    ("display:flex;min-width:630px;width:100%;align-items:flex-start", "display:flex;min-width:500px;width:100%;align-items:flex-start"),
    # Premi sponsor con il logo
    ("return '<div class=\"row\" style=\"align-items:flex-start;gap:10px;flex-wrap:wrap;padding:9px 0;border-top:1px solid var(--line)\"><div class=\"grow\" style=\"min-width:0;flex:1 1 160px\"><b style=\"display:block\">'+esc(premio.sponsor)+'</b>",
     "return '<div class=\"row\" style=\"align-items:flex-start;gap:10px;flex-wrap:wrap;padding:9px 0;border-top:1px solid var(--line)\"><img class=\"sp-logo\" src=\"'+esc(SPIMG[premio.sponsor]||SPIMG._neutro)+'\" alt=\"'+esc(premio.sponsor)+'\"><div class=\"grow\" style=\"min-width:0;flex:1 1 160px\"><b style=\"display:block\">'+esc(premio.sponsor)+'</b>"),
    # la barra di scorrimento non sposta la pagina quando arrivano i dati
    ("</head>", "<style>html{scrollbar-gutter:stable}</style></head>"),
    # Girrr Sport: «Squadra della settimana» nel menu fin dall'inizio. Prima la aggiungeva tifosi.js dopo il disegno: a ogni tocco
    # la pagina ridisegnava le schede spostate di un posto, la toglieva e la rimetteva, e la fila saltava indietro.
    ("h+='<div class=\"seg\" role=\"group\" aria-label=\"Sezioni di Girrr Sport\">'+tabs.map(function(t){return '<button data-sp=\"'+t[0]+'\" aria-pressed=\"'+(sp===t[0])+'\">'+t[1]+'</button>'}).join('')+'</div>';",
     "var MVP=!!(window.GirrrSportMvp&&window.GirrrSportMvp());"
     "h+='<div class=\"seg\" role=\"group\" aria-label=\"Sezioni di Girrr Sport\">'+tabs.map(function(t){return '<button data-sp=\"'+t[0]+'\" aria-pressed=\"'+(sp===t[0]&&!MVP)+'\">'+t[1]+'</button>'+(t[0]==='giornale'?'<button type=\"button\" data-pt-sport=\"mvp\" aria-pressed=\"'+MVP+'\">Squadra della settimana</button>':'')}).join('')+'</div>';"),
    # e le pillole di Girrr Sport tornano a sfumare (questa regola serviva solo per il menu ridisegnato)
    ("#view .seg button[data-sp][aria-pressed=false]{transition:none}", ""),
]

TOTO = [
    # cambio di menu senza salti: niente salto in cima (solo fino al menu, con calma) e altezza tenuta mentre arrivano i dati
    ("tab=b.getAttribute('data-tab');render();window.scrollTo(0,0);",
     "var pv=document.querySelector('.pane'),ph=pv?pv.offsetHeight:0;tab=b.getAttribute('data-tab');render();cambioTab(ph);"),
    ("function navPre(){",
     "/* 6.0.1 · Cambio di menu senza salti (Gianluca, 13 novembre 2026): prima la pagina saltava in cima e il contenuto cambiava di colpo,\n"
     "   due volte per Prestiti, Movimenti e Probabilità (prima «Carico…», poi i dati). Ora si sale solo fino al menu, con calma, e la\n"
     "   pagina tiene l'altezza finché arrivano i dati; la dissolvenza del contenuto la fa pillole.js. */\n"
     "var MINT=0;function cambioTab(ph){var pn=document.querySelector('.pane'),nv=document.querySelector('nav');"
     "if(pn&&ph){pn.style.minHeight=Math.min(ph,innerHeight)+'px';clearTimeout(MINT);MINT=setTimeout(function(){var p2=document.querySelector('.pane');if(p2)p2.style.minHeight=''},1500)}"
     # il menu resta attaccato in alto: si riporta all'inizio del contenuto nuovo, appena sotto il menu, solo se è più su
     "if(pn){var nh=nv?nv.offsetHeight:0,y=pn.getBoundingClientRect().top+scrollY-nh-12;if(scrollY>y+1){var rid=false;try{rid=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}window.scrollTo({top:Math.max(0,y),behavior:rid?'auto':'smooth'})}}}\n"
     "function navPre(){"),
]

SPOGLIATOIO = [
    ('<button role="tab" data-t="rosa" aria-selected="true">Rosa</button>',
     '<button role="tab" data-t="entra" aria-selected="false" hidden>Entra</button>\n<button role="tab" data-t="rosa" aria-selected="true">Rosa</button>'),
    ("var ok=authed();document.getElementById('tabs').hidden=!ok;",
     "var ok=authed(),PUB={inj:1,fa:1,lega:1},OSP=false;try{OSP=sessionStorage.getItem('ospite')==='1'||/[?&]ospite\\b/.test(location.search)}catch(e){}document.getElementById('tabs').hidden=false;"),
    ("if(!ok){app.innerHTML=vGate();return}",
     "if(!ok){/* senza codice: Infortunati, Svincolati e Calendario sono pubblici (Gianluca, 13 novembre 2026) */"
     "if(!PUB[tab]&&!(tab==='entra'&&!OSP))tab=OSP?'inj':'entra';"
     "[].forEach.call(document.querySelectorAll('#tabs button'),function(b){b.hidden=!(PUB[b.dataset.t]||(b.dataset.t==='entra'&&!OSP));b.setAttribute('aria-selected',b.dataset.t===tab)});"
     "app.innerHTML=tab==='entra'?vGate():tab==='inj'?vInj():tab==='fa'?vFa():vLega();enter=false;return}"
     "if(tab==='entra')tab='rosa';"),
    ("if(b.dataset.t==='stat')b.hidden=team!=='Oranje VC'", "b.hidden=b.dataset.t==='entra'||(b.dataset.t==='stat'&&team!=='Oranje VC')"),
    ("D.teams.forEach(function(t){t.pl.forEach(function(x){own[x.id]=1;if(t.name===team)mine[x.id]=1})});",
     "var io=authed();D.teams.forEach(function(t){t.pl.forEach(function(x){own[x.id]=1;if(io&&t.name===team)mine[x.id]=1})});"),
    ("ogni giocatore.</div><h2 class=\"sec\">I tuoi</h2><div class=\"card\">'+rows(a)+'</div>';",
     "ogni giocatore.</div>'+(io?'<h2 class=\"sec\">I tuoi</h2><div class=\"card\">'+rows(a)+'</div>':'');"),
    ("h+='<h2 class=\"sec\">Altri giocatori nelle rose della lega</h2>",
     "h+='<h2 class=\"sec\">'+(io?'Altri giocatori nelle rose della lega':'Giocatori nelle rose della lega')+'</h2>"),
    ("var me=team,CN={lega:'Classic League',cup:'Champions Cup'};", "var me=authed()?team:'',CN={lega:'Classic League',cup:'Champions Cup'};"),
]

HOME_LEGA = """<style>/* 6.0.1 · Lega: i riquadri grandi uno sotto l'altro, dritti come le partite del Tabellone (Gianluca, 13 novembre 2026) */
html body .wrap .cards{grid-template-columns:1fr!important;gap:12px}
@media(min-width:600px){html body .wrap .cards>.c{display:grid;grid-template-columns:210px minmax(0,1fr) auto;grid-template-areas:"ic t go" "ic p go";align-items:center;column-gap:24px;min-height:0;padding:18px 26px}
html body .wrap .cards>.c .ic{grid-area:ic;margin:0;height:74px;justify-content:center}
html body .wrap .cards>.c .ic img,html body .wrap .cards>.c .ic .recw{max-width:100%;max-height:70px;width:auto!important;height:auto!important;object-fit:contain}html body .wrap .cards>.c .ic .recw img{max-height:70px}
html body .wrap .cards>.c h2{grid-area:t;margin:0;align-self:end}
html body .wrap .cards>.c p{grid-area:p;margin:6px 0 0;align-self:start;flex:none}
html body .wrap .cards>.c .go{grid-area:go;margin:0;white-space:nowrap}}
</style></head>"""


DERBY_JS = [
    ("var TAB=null;",
     "var TAB=null;\n"
     "/* 6.0.1 · Tre schede: Derby della Lega, Le rivalità, Classifica dei Derby (Gianluca, 13 novembre 2026) */\n"
     "var SEZ=[['lega','Derby della Lega'],['rivalita','Le rivalità'],['classifica','Classifica dei Derby']],SZ=null,STA=/\\/stadio\\//.test(location.pathname),ALBO=/\\/albo\\.html$/.test(location.pathname);\n"
     "/* In Albo › Derby le tre schede stanno dentro il riquadro #der-root (novita.js): niente cambio di pagina */\n"
     "function ROOT(){return document.getElementById('der-root')||document.getElementById('al')}\n"
     "function pronto(f){if(!ALBO||document.getElementById('der-root'))return f();var mo=new MutationObserver(function(){if(document.getElementById('der-root')){mo.disconnect();f()}});mo.observe(document.body,{childList:true,subtree:true})}\n"
     "var stT=document.createElement('style');stT.textContent='.dtab{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding:2px;margin:0 0 12px}.dtab::-webkit-scrollbar{display:none}.dtab button:first-child{margin-left:auto}.dtab button:last-child{margin-right:auto}.dtab button{flex:none;height:34px;padding:0 14px;border-radius:17px;border:2px solid transparent;background:rgba(255,255,255,.08);color:inherit;font:800 13px Inter,system-ui,sans-serif;cursor:pointer;opacity:.6;transition:background .25s,opacity .25s,color .25s}.dtab button[aria-selected=true]{background:'+(STA?'#ffd166;color:#1d2a52':'var(--acc,#d62839);color:#fff')+';opacity:1}.dtab button:focus-visible{outline:2px solid var(--hi);outline-offset:2px}.dpan{animation:dIn .35s ease}@keyframes dIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}#der-cls:empty::before{content:\"Carico la Classifica dei Derby…\";display:block;padding:16px;color:var(--sub);font-weight:700}@media (prefers-reduced-motion:reduce){.dpan{animation:none}.dtab button{transition:none}}';document.head.appendChild(stT);\n"
     "function sezIniziale(){var q=new URLSearchParams(location.search).get('sez'),h=ALBO?(q||''):(location.hash||'').slice(1);if(h==='pt-derby')return 'classifica';if(SEZ.some(function(x){return x[0]===h}))return h;return window.PAGINA==='rivalita'?'rivalita':'lega'}\n"
     "function sezioni(HL,HR){if(!SZ)SZ=sezIniziale();var al=ROOT(),box=document.getElementById('pt-derby');\n"
     "  al.innerHTML='<div class=\"dtab\" role=\"tablist\" aria-label=\"Sezioni dei Derby\">'+SEZ.map(function(x){return '<button type=\"button\" role=\"tab\" data-dsez=\"'+x[0]+'\" aria-selected=\"'+(SZ===x[0])+'\">'+x[1]+'</button>'}).join('')+'</div>'\n"
     "   +'<div class=\"dpan\" role=\"tabpanel\" data-dp=\"lega\"'+(SZ==='lega'?'':' hidden')+'>'+HL+'</div><div class=\"dpan\" role=\"tabpanel\" data-dp=\"rivalita\"'+(SZ==='rivalita'?'':' hidden')+'>'+HR+'</div><div class=\"dpan\" role=\"tabpanel\" data-dp=\"classifica\" id=\"der-cls\"'+(SZ==='classifica'?'':' hidden')+'></div>';\n"
     "  if(box)document.getElementById('der-cls').appendChild(box)}\n"
     "document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-dsez]');if(!b)return;SZ=b.getAttribute('data-dsez');\n"
     "  document.querySelectorAll('[data-dsez]').forEach(function(z){z.setAttribute('aria-selected',z===b)});document.querySelectorAll('[data-dp]').forEach(function(z){z.hidden=z.getAttribute('data-dp')!==SZ});\n"
     "  try{history.replaceState(null,'',ALBO?'?sez='+SZ+'#derby':'#'+SZ)}catch(_){}b.scrollIntoView({block:'nearest',inline:'center',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'})});\n"
     "window.addEventListener('hashchange',function(){if(ALBO)return;var k=sezIniziale(),b=document.querySelector('[data-dsez=\"'+k+'\"]');if(b&&k!==SZ)b.click()});"),
    ("var RIV=window.PAGINA==='rivalita',r=prossima(),h='';\n  if(!RIV){", "var r=prossima(),h='',HL;\n  {"),
    ("  }else{\n    h+='<div class=\"card\"><h3>Giornata '+r.n+'</h3><p class=\"nt\" style=\"margin:0 0 6px\">Le rivalità",
     "  }HL=h;h='';{\n    h+='<div class=\"card\"><h3>Giornata '+r.n+'</h3><p class=\"nt\" style=\"margin:0 0 6px\">Le rivalità"),
    ("  document.getElementById('al').innerHTML=h;\n}", "  sezioni(HL,h);\n}"),
    ("document.getElementById('lg').onclick=function(){location.href='index.html'};", "if(!ALBO)document.getElementById('lg').onclick=function(){location.href='index.html'};"),
    ("D=d;classifica();render();caricaDb().then(render);document.getElementById('foot').textContent=",
     "D=d;classifica();pronto(render);caricaDb().then(function(){pronto(render)});if(!ALBO)document.getElementById('foot').textContent="),
    (".catch(function(e){document.getElementById('al').innerHTML=", ".catch(function(e){ROOT().innerHTML="),
]

NOVITA_DERBY = (
    "h+='<a class=\"card\" href=\"derby.html\" style=\"display:block;text-decoration:none;color:inherit\"><h3>I Derby della Lega<span class=\"nt-nv\">NOVITÀ</span></h3><div style=\"font-weight:700;font-size:14px\">I Derby con il loro nome, la storia e il Derby della giornata →</div></a><a class=\"card\" href=\"rivalita.html\" style=\"display:block;text-decoration:none;color:inherit\"><h3>Le rivalità<span class=\"nt-nv\">NOVITÀ</span></h3><div style=\"font-weight:700;font-size:14px\">Le rivalità forti e le sfide decisive →</div></a>';",
    "h+='<div id=\"der-root\"><div class=\"vuoto\">Carico i Derby…</div></div>';")


def rinvio(sez):
    """derby.html e rivalita.html portano in Albo › Derby, sulla scheda giusta (i vecchi collegamenti restano buoni)."""
    return ('<head><script>(function(){var h=(location.hash||"").slice(1),s=' + sez + ';'
            'location.replace("albo.html?sez="+s+"#derby")})()</script>')


def main(sito):
    for rel in ('girrr/app.html', 'stadio/girrr/app.html'):
        t = leggi(os.path.join(sito, rel))
        for a, b in APP:
            t = sost(t, a, b, rel)
        scrivi(os.path.join(sito, rel), t)
        print('ok', rel)
    # 7. Pillole fluide (pillole.js nella radice) su app, Albo d'oro e Totogirrr; Totogirrr senza salti
    shutil.copyfile(os.path.join(R, 'rilascio/pillole/pillole.js'), os.path.join(sito, 'pillole.js'))
    for pre, su in (('girrr/', '../'), ('stadio/girrr/', '../../')):
        for pag in ('app.html', 'albo.html', 'totogirrr.html'):
            t = leggi(os.path.join(sito, pre + pag))
            if pag == 'totogirrr.html':
                for a, b in TOTO:
                    t = sost(t, a, b, pre + pag)
            off = '<script src="' + su + 'offline.js" defer></script>'
            t = sost(t, off, '<script src="' + su + 'pillole.js?v=1" defer></script>' + off, pre + pag)
            scrivi(os.path.join(sito, pre + pag), t)
        print('ok', pre + 'app.html, albo.html, totogirrr.html con pillole.js')
    print('ok pillole.js')
    # 6. Condividi la giornata: foto e video in un album (anteprime su WhatsApp), poi Radio e Giornale; Giornale in PDF intero
    shutil.copyfile(os.path.join(R, 'rilascio/condividi/condividi.js'), os.path.join(sito, 'condividi.js'))
    print('ok condividi.js')
    for f in ('tifosi.js', 'tifosi.css'):
        shutil.copyfile(os.path.join(R, 'rilascio/tifosi60', f), os.path.join(sito, 'girrr/v60', f))
        print('ok girrr/v60/' + f)
    t = leggi(os.path.join(sito, 'index.html'))
    for a, b in SPOGLIATOIO:
        t = sost(t, a, b, 'index.html')
    scrivi(os.path.join(sito, 'index.html'), t)
    print('ok index.html')
    for rel, sel in (('girrr/ospite.js', 'a[href="../index.html"],'), ('stadio/girrr/ospite.js', 'a[href="../../index.html"],')):
        t = sost(leggi(os.path.join(sito, rel)), sel, '', rel)
        t = t.replace('Sola lettura: niente Spogliatoio, scambi e Totogirrr.', 'Sola lettura: dello Spogliatoio solo le schede pubbliche; niente scambi né Totogirrr.')
        scrivi(os.path.join(sito, rel), t)
        print('ok', rel)
    t = leggi(os.path.join(sito, 'girrr/index.html'))
    if '6.0.1 · Lega: i riquadri grandi' not in t:
        t = sost(t, '</head>', HOME_LEGA, 'girrr/index.html')
    scrivi(os.path.join(sito, 'girrr/index.html'), t)
    print('ok girrr/index.html')
    # 5. Derby in tre schede, direttamente in Albo › Derby
    for pre in ('girrr/', 'stadio/girrr/'):
        t = leggi(os.path.join(sito, pre + 'derby.js'))
        for a, b in DERBY_JS:
            t = sost(t, a, b, pre + 'derby.js')
        scrivi(os.path.join(sito, pre + 'derby.js'), t)
        t = sost(leggi(os.path.join(sito, pre + 'novita.js')), NOVITA_DERBY[0], NOVITA_DERBY[1], pre + 'novita.js')
        scrivi(os.path.join(sito, pre + 'novita.js'), t)
        t = leggi(os.path.join(sito, pre + 'albo.html'))
        t = sost(t, 'novita.js?v=1793700000', 'novita.js?v=1793800000', pre + 'albo.html')
        t = sost(t, '</body>', '<script src="derby.js?v=1793800000"></script></body>', pre + 'albo.html')
        scrivi(os.path.join(sito, pre + 'albo.html'), t)
        t = leggi(os.path.join(sito, pre + 'derby.html'))
        t = sost(t, '<title>I derby · O Girrr</title>', '<title>I Derby · O Girrr</title>', pre + 'derby.html')
        t = sost(t, '<head>', rinvio('h==="pt-derby"||h==="classifica"?"classifica":h==="rivalita"?"rivalita":"lega"'), pre + 'derby.html')
        scrivi(os.path.join(sito, pre + 'derby.html'), t)
        t = sost(leggi(os.path.join(sito, pre + 'rivalita.html')), '<head>', rinvio('"rivalita"'), pre + 'rivalita.html')
        scrivi(os.path.join(sito, pre + 'rivalita.html'), t)
        print('ok', pre + 'derby.js, novita.js, albo.html, derby.html, rivalita.html')

if __name__ == '__main__':
    main(sys.argv[1])
