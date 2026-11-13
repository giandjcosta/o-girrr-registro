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


def main(sito):
    for rel in ('girrr/app.html', 'stadio/girrr/app.html'):
        t = leggi(os.path.join(sito, rel))
        for a, b in APP:
            t = sost(t, a, b, rel)
        scrivi(os.path.join(sito, rel), t)
        print('ok', rel)
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


if __name__ == '__main__':
    main(sys.argv[1])
