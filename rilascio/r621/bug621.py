"""6.2.1, seconda parte (Claude, 16 novembre 2026): bug del sito vero segnalati da Gianluca. Usato da applica.py."""

APP_HOST = r"""    /* host62 */ if((a.hasAttribute('data-v62-precedenti')&&b.hasAttribute('data-v62-precedenti'))||(a.hasAttribute('data-v62-sondaggi')&&b.hasAttribute('data-v62-sondaggi')))continue;"""
APP_HOST_NEW = r"""    /* 6.2.1: un riquadro dei sondaggi o dei Precedenti non si trasforma in un'altra scheda (altrimenti i sondaggi ricomparivano nella Moviola) */ if(a.hasAttribute('data-v62-sondaggi')!==b.hasAttribute('data-v62-sondaggi')||a.hasAttribute('data-v62-precedenti')!==b.hasAttribute('data-v62-precedenti')){o.replaceChild(b.cloneNode(true),a);continue}
""" + APP_HOST

SEG = r"""var h='<div class="seg" role="group" aria-label="Sfide">'"""
SEG_NEW = r"""var h=sfCont()+'<div class="seg" role="group" aria-label="Sfide">'"""
HUB = "function sfidaHub(){var n=rxCount();"
SFCONT = r"""/* 6.2.1: quante sfide hai lanciato in questa stagione (due all'anno) */
function sfCont(){try{if(GUEST||!ME||typeof DBS==='undefined'||!DBS||!DBS.sfide)return '';var u=DBS.sfide.filter(function(s){return s.da===ME&&s.stagione===LV.stag}).length;return '<p class="sf-cont" style="display:inline-flex;align-items:center;gap:8px;margin:0 0 12px;padding:6px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.06);font-weight:700;font-size:13px"><b style="font-size:15px">'+Math.min(u,2)+'/2</b> sfide lanciate quest\'anno'+(u>=2?' · Nuove sfide dalla prossima stagione':'')+'</p>'}catch(e){return ''}}
"""

SOND_DRAW = "for(const h of hosts){if(h.isConnected)mount(h,h.dataset.v62Sondaggi);else hosts.delete(h)}"
SOND_DRAW_NEW = "for(const h of hosts){if(h.isConnected&&h.hasAttribute('data-v62-sondaggi'))mount(h,h.dataset.v62Sondaggi);else hosts.delete(h)}"
SOND_PREC = "async function precedenti(host){if(!host)return;"
SOND_PREC_NEW = "async function precedenti(host){if(!host)return;const era=host.hasAttribute('data-v62-precedenti');"
SOND_PREC2 = "conf={prima,dopo};"
SOND_PREC2_NEW = "if(!host.isConnected||(era&&!host.hasAttribute('data-v62-precedenti')))return;conf={prima,dopo};"
SOND_CAMBIA = ".v62-cambia{font:inherit;font-size:.85em;font-weight:600;background:none;border:0;padding:4px 2px;margin-left:6px;color:inherit;opacity:.8;text-decoration:underline;cursor:pointer;min-height:32px}.v62-cambia:hover{opacity:1}"
SOND_CAMBIA_NEW = (".v62-cambia{display:inline-flex;align-items:center;font:inherit;font-size:13px;font-weight:800;line-height:1;border:0;border-radius:999px;padding:9px 16px;margin:8px 0 0 8px;"
                   "'+(/\\/stadio\\//.test(location.pathname)?'background:#ffd166;color:#1d2a52':'background:#d62839;color:#fff')+';cursor:pointer;min-height:36px;text-decoration:none;opacity:1}"
                   ".v62-cambia:hover{filter:brightness(1.1)}.v62-cambia:focus-visible{outline:3px solid #89d9ff;outline-offset:2px}.v62-cambia[disabled]{opacity:.55;cursor:default}")

PILL_FILE = "  var FILE = '.seg,.at,.dtab,nav .nvi,.chips,.ptabs,#tabs,.pt-competition';"
PILL_FILE_NEW = PILL_FILE + "\n  /* 6.2.1 (Gianluca): menu dell'Albo e della Carriera (.oro-scroll), sottomenu dei Derby e pulsanti Campionato / Champions Cup dei Derby: il colore passa\n     dalla pillola di prima alla nuova senza scivolare; le pillole restano ferme (sul telefono la scelta resta in vista). */\n  var FERME = '.at,.dtab,.pt-competition,.oro-scroll';\n  try { var _fs = document.createElement('style'); _fs.textContent = FERME + '{scroll-snap-type:none!important}'; (document.head || document.documentElement).appendChild(_fs); } catch (e) {}   /* l'aggancio riportava indietro la fila e l'ultima voce restava tagliata */"
PILL_GHOST = "      /* il colore scivola dalla pillola di prima a quella nuova */"
PILL_GHOST_NEW = "      if (c2.matches && c2.matches(FERME)) return;\n" + PILL_GHOST

LATTA = "  b.innerHTML=h+(LS.p==='sempre'?latSempre():latAnno())}"
LATTA_NEW = r"""  /* 6.2.1: al tocco restano titolo e pulsanti; cambia solo il contenuto, in dissolvenza (prima si ricaricava tutto il riquadro) */
  var corpo=LS.p==='sempre'?latSempre():latAnno(),lb=b.querySelector('.lbody');
  if(lb&&b.querySelector('.lseg [data-lp]')){[].forEach.call(b.querySelectorAll('.lseg [data-lp]'),function(x){x.setAttribute('aria-pressed',String(x.getAttribute('data-lp')===LS.p))});lb.innerHTML=corpo;
   if(!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))try{lb.animate([{opacity:.3,transform:'translateY(4px)'},{opacity:1,transform:'none'}],{duration:260,easing:'cubic-bezier(.22,.61,.36,1)'})}catch(e){}return}
  b.innerHTML=h+'<div class="lbody">'+corpo+'</div>'}"""

DERBY_FINE = r"""
/* 6.2.1 (Gianluca): nei Derby la linea sotto la sezione scorre da una voce all'altra e il contenuto entra in dissolvenza,
   senza saltare in alto. Con «riduci movimento» cambia e basta. */
(function(){if(window.__dline)return;window.__dline=1;
var STA=/\/stadio\//.test(location.pathname),R=function(){try{return matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){return false}};
var st=document.createElement('style');st.textContent='.dtab{position:relative}.dtab>.dline{position:absolute;left:0;bottom:0;height:3px;border-radius:3px;background:'+(STA?'#ffd166':'var(--acc,#d62839)')+';pointer-events:none;transition:transform .38s cubic-bezier(.22,.61,.36,1),width .38s cubic-bezier(.22,.61,.36,1)}.dtab button[aria-selected=true]{border-bottom-color:transparent!important}';document.head.appendChild(st);
function linea(t,anim){var a=t.querySelector('[aria-selected=true]');if(!a)return;var l=t.querySelector('.dline');if(!l){l=document.createElement('i');l.className='dline';l.setAttribute('aria-hidden','true');t.appendChild(l);anim=false}
 if(!anim||R())l.style.transition='none';l.style.width=a.offsetWidth+'px';l.style.transform='translateX('+a.offsetLeft+'px)';if(!anim||R()){void l.offsetWidth;l.style.transition=''}}
var attesa=false;function tutte(){if(attesa)return;attesa=true;requestAnimationFrame(function(){attesa=false;[].forEach.call(document.querySelectorAll('.dtab'),function(t){linea(t,false)})})}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-dsez]');if(!b)return;var t=b.closest('.dtab'),top=t?t.getBoundingClientRect().top:0;
 requestAnimationFrame(function(){if(!t)return;linea(t,true);var d=t.getBoundingClientRect().top-top;if(Math.abs(d)>1)window.scrollBy(0,d);
  var p=document.querySelector('[data-dp="'+b.getAttribute('data-dsez')+'"]');if(p&&!R())try{p.animate([{opacity:0,transform:'translateY(6px)'},{opacity:1,transform:'none'}],{duration:280,easing:'cubic-bezier(.22,.61,.36,1)'})}catch(x){}})});
if(window.MutationObserver)new MutationObserver(tutte).observe(document.documentElement,{childList:true,subtree:true});window.addEventListener('resize',tutte);window.addEventListener('load',tutte);tutte();
})();
"""

ORO_SCROLL = """requestAnimationFrame(function(){var r=document.querySelector('.oro-scroll'),a=r&&r.querySelector('[aria-pressed="true"]');if(a)a.scrollIntoView({block:'nearest',inline:'center'})});"""
ORO_SCROLL_NEW = """requestAnimationFrame(function(){var r=document.querySelector('.oro-scroll'),a=r&&r.querySelector('[aria-pressed="true"]');/* 6.2.1: la fila si sposta solo se la voce scelta è fuori vista, e con calma; la pagina non si muove */if(a&&r.scrollWidth>r.clientWidth+1){var e=r.getBoundingClientRect(),q=a.getBoundingClientRect();if(q.left<e.left-1||q.right>e.right+1)r.scrollTo({left:Math.max(0,r.scrollLeft+(q.left-e.left)-(e.width-q.width)/2),behavior:(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)?'auto':'smooth'})}});"""

PILL_FILA = """      /* la fila non torna all'inizio */
      if (scorri(c2) && c2.scrollLeft < sl - 2) { var sb = c2.style.scrollBehavior; c2.style.scrollBehavior = 'auto'; c2.scrollLeft = sl; c2.style.scrollBehavior = sb; }
      centra(c2, n);"""
PILL_FILA_NEW = """      /* 6.2.1: nelle file ferme (Albo, Carriera, Derby) la fila non viene riportata indietro e si sposta solo se la voce scelta
         è fuori vista: prima tre scorrimenti insieme (questo, l'app e il ritorno indietro) la fermavano a metà, con l'ultima voce tagliata */
      var ferma = c2.matches && c2.matches(FERME);
      if (ferma) { var _r = n.getBoundingClientRect(), _e = c2.getBoundingClientRect(); if (_r.left < _e.left - 1 || _r.right > _e.right + 1) centra(c2, n); }
      else {
      /* la fila non torna all'inizio */
      if (scorri(c2) && c2.scrollLeft < sl - 2) { var sb = c2.style.scrollBehavior; c2.style.scrollBehavior = 'auto'; c2.scrollLeft = sl; c2.style.scrollBehavior = sb; }
      centra(c2, n);
      }"""

CURVA_LOGO = '<div class="logo" data-lega="1">'
CURVA_LOGO_NEW = '<div class="logo" aria-label="Curva">'  # 6.2.1 (da ChatGPT nel Lab): il simbolo C della Curva non apre più la Home della Lega
NOTIFICHE_HEAD = '</head>'
NOTIFICHE_NEW = ('<style>/* 6.2.1 (da ChatGPT nel Lab): logo della Lega senza alone, come nelle altre pagine; niente contorno al tocco */'
                 'body[data-v53="notifications"] .hero img{filter:none!important;animation:none!important}'
                 'body[data-v53="notifications"] .hero>a{background:transparent!important;box-shadow:none!important;border:0!important}'
                 'a[href]:focus:not(:focus-visible),button:focus:not(:focus-visible){outline:none!important;box-shadow:none!important}</style></head>')

WEEK_MORPH = "  morphDom(_vw,_nv);"
WEEK_MORPH_NEW = ("  /* 6.2.1: «La mia settimana» la aggiunge tifosi.js dopo il disegno: fuori dal confronto, poi di nuovo al suo posto, con la fila ferma.\n"
                  "     Prima il confronto la trasformava in «Regole» e cancellava l'ultimo pulsante: la fila saltava e i pulsanti cambiavano sotto il dito. */\n"
                  "  var _wk=_vw.querySelector('[data-pt-week]'),_wfr=_wk&&_wk.parentNode,_wsl=_wfr?_wfr.scrollLeft:0;if(_wk)_wk.remove();\n"
                  "  morphDom(_vw,_nv);\n"
                  "  if(_wk){var _rg=_vw.querySelector('[data-ctab=\"reg\"]');if(_rg&&_rg.parentNode){var _rf=_rg.parentNode,_rsb=_rf.style.scrollBehavior;_rf.insertBefore(_wk,_rg);_rf.style.scrollBehavior='auto';_rf.scrollLeft=_wsl;_rf.style.scrollBehavior=_rsb}}")

LAVORI = {
    'girrr/app.html': [(APP_HOST, APP_HOST_NEW), (SEG, SEG_NEW), (ORO_SCROLL, ORO_SCROLL_NEW), (WEEK_MORPH, WEEK_MORPH_NEW)],
    'stadio/girrr/app.html': [(APP_HOST, APP_HOST_NEW), (SEG, SEG_NEW), (ORO_SCROLL, ORO_SCROLL_NEW), (WEEK_MORPH, WEEK_MORPH_NEW)],
    'sondaggi62.js': [(SOND_DRAW, SOND_DRAW_NEW), (SOND_PREC, SOND_PREC_NEW), (SOND_PREC2, SOND_PREC2_NEW), (SOND_CAMBIA, SOND_CAMBIA_NEW)],
    'girrr/curva.html': [(CURVA_LOGO, CURVA_LOGO_NEW)],
    'stadio/girrr/curva.html': [(CURVA_LOGO, CURVA_LOGO_NEW)],
    'girrr/notifiche.html': [(NOTIFICHE_HEAD, NOTIFICHE_NEW)],
    'stadio/girrr/notifiche.html': [(NOTIFICHE_HEAD, NOTIFICHE_NEW)],
    'condividi.js': [("giro-di-boa.js?v=61-periodi1", "giro-di-boa.js?v=621")],
    'pillole.js': [(PILL_FILE, PILL_FILE_NEW), (PILL_GHOST, PILL_GHOST_NEW), (PILL_FILA, PILL_FILA_NEW)],
}


def copia(base):
    """6.2.1: file corretti da ChatGPT nel Lab (Derby, Albo di Latta, Giro di boa), presi così come sono.
    Si fermano se il file del sito non è più quello da cui sono partiti."""
    import hashlib, json, pathlib
    qui = pathlib.Path(__file__).resolve().parent / 'file'
    attesi = json.loads((qui / 'ORIGINALI.json').read_text())
    for rel, h in attesi.items():
        dst = base / rel; nuovo = (qui / rel).read_bytes()
        if dst.read_bytes() == nuovo:
            continue
        if hashlib.sha256(dst.read_bytes()).hexdigest() != h:
            raise SystemExit('Il sito ha cambiato ' + rel + ' dopo la prova nel Lab: riallineare prima di pubblicare')
        dst.write_bytes(nuovo)


def extra(base):
    """Funzioni aggiunte una volta sola (rieseguibile)."""
    for p in ('girrr/app.html', 'stadio/girrr/app.html'):
        f = base / p; t = f.read_text(encoding='utf-8')
        if 'function sfCont(' not in t:
            i = t.index(HUB)  # prima definizione: sfCont è visibile da entrambe
            t = t[:i] + SFCONT + t[i:]; f.write_text(t, encoding='utf-8')
    for p in ('girrr/derby.js', 'stadio/girrr/derby.js'):
        f = base / p; t = f.read_text(encoding='utf-8')
        if '__dline' not in t:
            f.write_text(t + DERBY_FINE, encoding='utf-8')


def versioni(t):
    import re
    t = t.replace('pillole.js?v=1"', 'pillole.js?v=621"')
    t = re.sub(r'derby\.js\?v=\d+', 'derby.js?v=621', t)
    t = re.sub(r'novita\.js\?v=\d+', 'novita.js?v=621', t)
    t = t.replace('giro-di-boa.js?v=611-1', 'giro-di-boa.js?v=621').replace('giro-di-boa.css?v=61-periodi1', 'giro-di-boa.css?v=621').replace('condividi.js?v=61-periodi1', 'condividi.js?v=621')
    return t
