#!/usr/bin/env python3
"""6.2 · Campo con Campionato e Champions Cup (Claude, 15 novembre 2026).

Aggiunge alla pagina Campo (Lega e Stadio) l'interruttore Campionato / Champions Cup:
- le partite della Coppa erano raggiungibili solo con ?coppa=1 dal Tabellone; ora si cambia nella pagina;
- Lega: l'indicatore scorre da rosso ad azzurro e le bande sfumano da rosso ad azzurro;
- Stadio: tutto resta oro anche in Coppa (regola di Gianluca, 15 novembre 2026);
- cerchio oro e stella al migliore in campo; simboli per tutti i bonus e malus delle pagelle;
- il contenuto esce e rientra con una dissolvenza breve; «Riduci movimento» toglie i movimenti;
- ogni competizione ricorda la sua giornata e la sua partita.

Uso:
  python3 rilascio/r62/campo_coppa.py COPIA_DI_GH_PAGES     modifica girrr/campo.html e stadio/girrr/campo.html
  python3 rilascio/r62/campo_coppa.py --lab                 scrive rilascio/r62/pagine/ dalle sorgenti ufficiali
Si ferma se una pagina non è quella attesa. Rieseguirlo sulla stessa copia non cambia niente.
"""
import pathlib
import sys

QUI = pathlib.Path(__file__).resolve().parent
REG = QUI.parent.parent
PAGINE = ('girrr/campo.html', 'stadio/girrr/campo.html')
SEGNO = '/* 6.2 · Campo con Campionato e Champions Cup */'

CSS = SEGNO + r'''
/* Regola di Gianluca (15 novembre 2026): la Lega tiene i colori (Campionato rosso, Coppa azzurra), lo Stadio tiene tutto oro anche in Coppa */
body[data-v53=campo][data-comp=coppa][data-skin=lega]{--g-acc:#3d93d6;--g-onacc:#fff;--accent:#3d93d6;--onaccent:#fff}
body[data-v53=campo][data-comp=coppa][data-skin=stadio]{--accent:#ffd166;--onaccent:#142449}
.comp-sw{position:relative;display:grid;grid-template-columns:1fr 1fr;align-self:center;width:min(100%,400px);padding:4px;border-radius:999px;background:rgba(20,29,61,.72);box-shadow:inset 0 0 0 1px var(--line)}
.comp-sw[hidden]{display:none}
.comp-sw i{position:absolute;top:4px;bottom:4px;left:4px;width:calc(50% - 4px);border-radius:999px;background:#d62839;box-shadow:0 4px 14px rgba(0,0,0,.28);transition:transform .55s cubic-bezier(.65,0,.25,1),background-color .55s ease;will-change:transform}
.comp-sw[data-on=coppa] i{transform:translateX(100%)}
body[data-skin=lega] .comp-sw[data-on=coppa] i{background:#3d93d6}
body[data-skin=stadio] .comp-sw i{background:#ffd166}
body[data-skin=stadio] .comp-sw button[aria-selected=true]{color:#1d2a52;transition:opacity .35s ease,color .3s ease .15s}
.comp-sw button{position:relative;z-index:1;border:0;background:none;color:#fbf6ec;font:800 13px/1.2 Inter,system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:10px 8px;min-height:44px;border-radius:999px;white-space:nowrap;transition:opacity .35s ease}
.comp-sw button[aria-selected=false]{opacity:.7}.comp-sw button[aria-selected=false]:hover{opacity:1}
/* Il colore sfuma solo dove serve. Bande delle schede: la banda di prima resta sopra come velo e svanisce (solo opacità, lavoro della scheda grafica) */
body[data-v53=campo] #board>.card{position:relative}
html.cc-pronto body[data-v53=campo] #board>.card::after{content:'';position:absolute;top:-1px;right:-1px;bottom:-1px;left:calc(-1*var(--g-band,8px));border:1px solid transparent;border-left:var(--g-band,8px) solid var(--cc-prima,transparent);border-radius:var(--g-card,14px);pointer-events:none;opacity:0;transition:opacity .65s cubic-bezier(.4,0,.2,1)}
html.cc-pronto body[data-v53=campo] #board.cc-da>.card::after{opacity:1;transition:none}
html.cc-pronto body[data-v53=campo] .sidebar nav a{transition:box-shadow .6s cubic-bezier(.4,0,.2,1),background-color .6s cubic-bezier(.4,0,.2,1),color .6s cubic-bezier(.4,0,.2,1)}
html.cc-pronto body[data-v53=campo] .gamebtn{transition:background-color .6s cubic-bezier(.4,0,.2,1),color .6s cubic-bezier(.4,0,.2,1)}
#board,#matches,#roundtitle{transition:opacity .34s cubic-bezier(.22,.61,.36,1),transform .34s cubic-bezier(.22,.61,.36,1)}
#board.cc-via,#matches.cc-via,#roundtitle.cc-via{opacity:0;transform:translateY(8px);transition-duration:.16s;transition-timing-function:ease-in;pointer-events:none}
/* Cerchio dei giocatori di casa sul campo, solo nella Lega: rosso in Campionato, azzurro in Coppa. Nello Stadio resta com'era (l'oro è del migliore in campo). Ospite sempre bianco */
body[data-v53=campo][data-skin=lega]{--casa:#ff5a6a}
body[data-v53=campo][data-skin=lega][data-comp=coppa]{--casa:#63bce9}
/* Cerchio oro: il migliore in campo, quello con la stella (al massimo uno per squadra, come nei dati di Fantacalcio) */
.pitch .pl.top b,.pitch .pl.away.top b{border-color:#ffd166;box-shadow:0 0 0 2px rgba(255,209,102,.35),0 2px 6px rgba(0,0,0,.35)}
@media(max-width:700px){.comp-sw{width:100%}}
@media(max-width:360px){.comp-sw button{font-size:11.5px;letter-spacing:.03em;padding:10px 4px}}
@media(prefers-reduced-motion:reduce){.comp-sw i,.comp-sw button,#board,#matches,#roundtitle,html.cc-pronto body[data-v53=campo] #board>.card::after,html.cc-pronto body[data-v53=campo] .sidebar nav a,html.cc-pronto body[data-v53=campo] .gamebtn{transition:none!important}}
'''

SW = ('<div class="comp-sw" id="comp-sw" role="tablist" aria-label="Competizione"><i aria-hidden="true"></i>'
      '<button role="tab" data-comp-choice="lega" aria-selected="true">Campionato</button>'
      '<button role="tab" data-comp-choice="coppa" aria-selected="false">Champions Cup</button></div>\n ')

JS_STATO = r'''var CAL={},STATO={},CAMBIO=0,FERMO=window.matchMedia('(prefers-reduced-motion: reduce)');document.body.dataset.comp=COPPA?'coppa':'lega';(document.getElementById('comp-sw')||{dataset:{}}).dataset.on=COPPA?'coppa':'lega';
/* 6.2: Campionato e Champions Cup nella stessa pagina. D.cal.lega è il calendario mostrato; CAL tiene i due, STATO giornata e partita di ognuno. */
function primo(){var i=D.cal.lega.findIndex(function(g){return !played(g)});return i<0?D.cal.lega.length-1:Math.max(0,i-1)}
function colori(){document.body.dataset.comp=COPPA?'coppa':'lega'}
function intestazione(){var c=COPPA?'coppa':'lega',sw=document.getElementById('comp-sw');if(sw)sw.dataset.on=c;
 document.querySelectorAll('[data-comp-choice]').forEach(function(b){var si=b.dataset.compChoice===c;b.setAttribute('aria-selected',String(si));b.tabIndex=si?0:-1});
 document.querySelectorAll('.campo-logo').forEach(function(i){i.src=COPPA?'https://giandjcosta.github.io/o-fant-a-girrr/assets/loghi/logo-cup-champions-cup.png':'https://giandjcosta.github.io/o-fant-a-girrr/assets/loghi/logo-lega-o-fant-a-girrr.png';i.alt=COPPA?'Champions Cup':'O Fant A Girrr'});
 var kk=document.querySelector('.campo-title .kicker');if(kk)kk.textContent=COPPA?'Campo · Champions Cup':'Campo · Centro della giornata';
 var sub=document.querySelector('.campo-title .sub');if(sub)sub.textContent='Partite, risultati, rendimento e andamento '+(COPPA?'della Champions Cup':'della Lega')+', aggiornati dal calendario.';
 var pie=document.getElementById('comp-foot');if(pie)pie.textContent=COPPA?'CHAMPIONS CUP':'CAMPIONATO'}
function setComp(c){
 if(!D||!CAL.coppa||!CAL.coppa.length||(c==='coppa')===COPPA)return;
 STATO[COPPA?'coppa':'lega']={round:round,game:game};
 COPPA=c==='coppa';D.cal.lega=CAL[c];
 var s=STATO[c];if(s){round=s.round;game=s.game}else{round=primo();game=partitaMia(round)}
 intestazione();
 var t=++CAMBIO,piani=['board','matches','roundtitle'].map(function(id){return document.getElementById(id)});
 function fine(){render();if(typeof aggiornaRitorni==='function')aggiornaRitorni()}
 if(FERMO.matches){colori();fine();return}
 piani.forEach(function(p){p.classList.add('cc-via')});
 setTimeout(function(){if(t!==CAMBIO)return;
  /* Le nuove schede nascono col colore di prima; poi il colore cambia una volta sola e le bande sfumano mentre la pagina rientra */
  var bd=document.getElementById('board'),bs=document.body.style;bs.setProperty('--cc-prima',getComputedStyle(document.body).getPropertyValue('--g-acc').trim()||'transparent');
  fine();bd.classList.add('cc-da');colori();var c=bd.querySelector('.card');if(c)getComputedStyle(c,'::after').opacity;
  bd.classList.remove('cc-da');piani.forEach(function(p){p.classList.remove('cc-via')})},170);
}
(function(){var sw=document.getElementById('comp-sw');if(!sw)return;
 sw.addEventListener('click',function(e){var b=e.target.closest('[data-comp-choice]');if(b)setComp(b.dataset.compChoice)});
 sw.addEventListener('keydown',function(e){if(!/^(ArrowLeft|ArrowRight|Home|End)$/.test(e.key))return;e.preventDefault();var c=e.key==='ArrowLeft'||e.key==='Home'?'lega':'coppa';setComp(c);var b=sw.querySelector('[data-comp-choice="'+c+'"]');if(b)b.focus()})})();
'''
GI_OLD = r''' function gioc(id,dentro){var p=D.P[id]||{},x=voto(id),b=(x&&x.b)||[],gol=0,ass=0,top=false;
  b.forEach(function(s){var n;if((n=/^(\d+) (gol|rigore segnato|rigori segnati)$/.exec(s)))gol+=+n[1];else if((n=/^(\d+) assist$/.exec(s)))ass+=+n[1];else if(s==='migliore in campo')top=true});
  return {n:p.n||'—',r:p.r||'C',v:x&&x.v!=null?x.v:null,gol:gol,ass:ass,top:top,dentro:dentro||null}}'''
GI_NEW = r''' function gioc(id,dentro){var p=D.P[id]||{},x=voto(id),b=(x&&x.b)||[],k={gol:0,rig:0,ass:0,ag:0,rs:0,rp:0,gs:0},top=false;
  b.forEach(function(s){var n=/^(\d+) (.+)$/.exec(s),q=n?+n[1]:0,w=n?n[2]:s;
   if(w==='gol')k.gol+=q;else if(/^rigor[ei] segnat[oi]$/.test(w))k.rig+=q;else if(w==='assist')k.ass+=q;else if(w==='autogol')k.ag+=q;else if(/^rigor[ei] sbagliat[oi]$/.test(w))k.rs+=q;else if(/^rigor[ei] parat[oi]$/.test(w))k.rp+=q;else if(/^gol subit[oi]$/.test(w))k.gs+=q;else if(s==='migliore in campo')top=true});
  var r=p.r||'C',v=x&&x.v!=null?x.v:null;
  return {n:p.n||'—',r:r,v:v,gol:k.gol,rig:k.rig,ass:k.ass,ag:k.ag,rs:k.rs,rp:k.rp,gs:k.gs,pi:r==='P'&&v!=null&&!k.gs,top:top,dentro:dentro||null}}'''
CH_OLD = r''' var ic=(g.gol?Array(g.gol+1).join('⚽'):'')+(g.ass?(g.ass>1?g.ass+'×':'')+'👟':'')+(g.dentro?'↑':'');
 var tit=g.n+(g.dentro?' (Entrato al posto di '+g.dentro+')':'')+' · Voto '+v+(g.gol?' · Gol: '+g.gol:'')+(g.ass?' · Assist: '+g.ass:'')+(g.top?' · ★ Migliore in campo':'');'''
CH_NEW = r''' function rip(n,s){return n?(n>2?n+'×'+s:Array(n+1).join(s)):''}
 var ic=rip(g.gol,'⚽')+rip(g.rig,'🎯')+rip(g.ass,'👟')+rip(g.rp,'🧤')+(g.pi?'🛡️':'')+(g.gs?g.gs+'🥅':'')+rip(g.rs,'❌')+rip(g.ag,'🔴')+(g.dentro?'↑':'');
 var tit=g.n+(g.dentro?' (Entrato al posto di '+g.dentro+')':'')+' · Voto '+v+(g.gol?' · Gol: '+g.gol:'')+(g.rig?' · Rigori segnati: '+g.rig:'')+(g.ass?' · Assist: '+g.ass:'')+(g.rp?' · Rigori parati: '+g.rp:'')+(g.pi?' · Porta inviolata':'')+(g.gs?' · Gol subiti: '+g.gs:'')+(g.rs?' · Rigori sbagliati: '+g.rs:'')+(g.ag?' · Autogol: '+g.ag:'')+(g.top?' · ★ Migliore in campo':'');'''
LE_OLD = '''<li><span class="legend-symbol leg-star" aria-hidden="true">★</span><span>Migliore in campo.</span></li><li><span class="legend-symbol" aria-hidden="true">⚽</span><span>Gol segnato.</span></li><li><span class="legend-symbol" aria-hidden="true">👟</span><span>Assist.</span></li>'''
LE_NEW = '''<li><span class="legend-symbol leg-star" aria-hidden="true">★</span><span>Migliore in campo: cerchio oro e stella.</span></li><li><span class="legend-symbol" aria-hidden="true">⚽</span><span>Gol segnato.</span></li><li><span class="legend-symbol" aria-hidden="true">🎯</span><span>Rigore segnato.</span></li><li><span class="legend-symbol" aria-hidden="true">👟</span><span>Assist.</span></li><li><span class="legend-symbol" aria-hidden="true">🧤</span><span>Rigore parato.</span></li><li><span class="legend-symbol" aria-hidden="true">🛡️</span><span>Porta inviolata: portiere senza gol subiti.</span></li><li><span class="legend-symbol" aria-hidden="true">🥅</span><span>Gol subiti dal portiere (il numero accanto).</span></li><li><span class="legend-symbol" aria-hidden="true">❌</span><span>Rigore sbagliato.</span></li><li><span class="legend-symbol" aria-hidden="true">🔴</span><span>Autogol.</span></li>'''


def sostituisci(t, vecchio, nuovo, nome):
    n = t.count(vecchio)
    if n != 1:
        raise SystemExit('%s: atteso una volta «%s…», trovato %d volte' % (nome, vecchio[:60], n))
    return t.replace(vecchio, nuovo)


def applica(t, nome):
    if SEGNO in t:
        return t
    t = sostituisci(t, '\n</style><link rel="icon"', '\n' + CSS + '</style><link rel="icon"', nome)
    t = sostituisci(t, '<div class="skin" role="group" aria-label="Grafica">', SW + '<div class="skin" role="group" aria-label="Grafica">', nome)
    t = sostituisci(t, '<div class="side-foot">CAMPIONATO<small>', '<div class="side-foot"><span id="comp-foot">CAMPIONATO</span><small>', nome)
    t = sostituisci(t, "var COPPA=new URLSearchParams(location.search).get('coppa')==='1',GIR={};\n",
                    "var COPPA=new URLSearchParams(location.search).get('coppa')==='1',GIR={};\n" + JS_STATO, nome)
    t = sostituisci(t, "u.searchParams.set('skin',document.body.dataset.skin);history.replaceState(null,'',u);\n}",
                    "u.searchParams.set('skin',document.body.dataset.skin);if(COPPA)u.searchParams.set('coppa','1');else u.searchParams.delete('coppa');history.replaceState(null,'',u);\n}", nome)
    vecchio = ("if(COPPA){D.cal.lega=(D.cal.cup||[]).map(function(g){g.m.forEach(function(m){GIR[m[1]]=GIR[m[4]]=m[0]});(g.rest||[]).forEach(function(z){GIR[z[1]]=z[0]});return {n:g.n,sa:g.sa,m:g.m.map(function(m){return [m[1],m[2],m[3],m[4],m[5],m[0]]})}});document.body.dataset.comp='coppa';document.querySelectorAll('.campo-logo').forEach(function(i){i.src='https://giandjcosta.github.io/o-fant-a-girrr/assets/loghi/logo-cup-champions-cup.png';i.alt='Champions Cup'});var kk=document.querySelector('.campo-title .kicker');if(kk)kk.textContent='Campo · Champions Cup'}var playedIdx=D.cal.lega.findIndex(function(g){return !played(g)});round=playedIdx<0?D.cal.lega.length-1:Math.max(0,playedIdx-1);")
    nuovo = ("CAL.lega=D.cal.lega;CAL.coppa=(D.cal.cup||[]).filter(function(g){return g&&g.m&&g.m.length}).map(function(g){g.m.forEach(function(m){GIR[m[1]]=GIR[m[4]]=m[0]});(g.rest||[]).forEach(function(z){GIR[z[1]]=z[0]});return {n:g.n,sa:g.sa,m:g.m.map(function(m){return [m[1],m[2],m[3],m[4],m[5],m[0]]})}});"
             "if(!CAL.coppa.length){COPPA=false;var sw=document.getElementById('comp-sw');if(sw)sw.hidden=true}D.cal.lega=COPPA?CAL.coppa:CAL.lega;intestazione();colori();round=primo();")
    t = sostituisci(t, vecchio, nuovo, nome)
    t = sostituisci(t, "Number(q.get('partita'))||0)):partitaMia(round);render()}",
                    "Number(q.get('partita'))||0)):partitaMia(round);render();requestAnimationFrame(function(){requestAnimationFrame(function(){document.documentElement.classList.add('cc-pronto')})})}", nome)
    t = sostituisci(t, "<span><b>Squadra di casa</b><small>Bordo azzurro.</small></span>",
                    "<span><b>Squadra di casa</b><small>'+(COPPA||document.body.dataset.skin!=='lega'?'Bordo azzurro.':'Bordo rosso.')+'</small></span>", nome)
    t = sostituisci(t, GI_OLD, GI_NEW, nome)
    t = sostituisci(t, CH_OLD, CH_NEW, nome)
    t = sostituisci(t, LE_OLD, LE_NEW, nome)
    return t


def main(argv):
    if argv == ['--lab']:
        coppie = [(REG / 'ufficiale/src/sito' / p, QUI / 'pagine' / p) for p in PAGINE]
    elif len(argv) == 1:
        base = pathlib.Path(argv[0])
        coppie = [(base / p, base / p) for p in PAGINE]
    else:
        raise SystemExit(__doc__)
    uscite = [(dst, applica(src.read_text(encoding='utf-8'), str(src))) for src, dst in coppie]
    for dst, t in uscite:  # scrive solo dopo aver preparato tutte le pagine
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(t, encoding='utf-8')
        print('Scritto', dst)


if __name__ == '__main__':
    main(sys.argv[1:])
