"""Integra le funzioni 6.2 nei componenti esistenti, conservandone i fogli di stile."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[2]
def sost(s,a,b):
    if s.count(a)!=1: raise ValueError('Pagina diversa da quella attesa: '+a[:100])
    return s.replace(a,b)
def prepara(base):
    out={base/'sondaggi62.js':(R/'rilascio/r62/sondaggi.js').read_text()}
    p=base/'girrr/v55/ui.js';s=p.read_text()
    if 'GirrrSondaggi62.mount(host)' not in s:
        s=sost(s,"var Sg=sondaggi(),reale=SITO55", "if(window.GirrrSondaggi62){window.GirrrSondaggi62.mount(host);SEC55.dataset.vuoto='';posizionaSondaggio();var vv=el('vista');if(vv)new MutationObserver(posizionaSondaggio).observe(vv,{childList:true});return}\nvar Sg=sondaggi(),reale=SITO55")
    out[p]=s
    p=base/'girrr/v60/tifosi.js';s=p.read_text()
    if 'readyVote=false' not in s:
        s=sost(s,"myVote=null,pollError=''", "myVote=null,readyVote=false,pollError=''")
        s=sost(s,"function identity(){try{", "function identity(){try{if(sessionStorage.getItem('ospite')==='1')return null;")
        s=s.replace("!closed&&id?'<button", "!closed&&id&&readyVote&&!myVote?'<button")
        s=sost(s,"const status=closed?", "const status=!readyVote?'Caricamento dello stato personale…':closed?")
        s=s.replace("'Hai votato '+N(mine[id.team])+'. Puoi cambiare o ritirare il voto.'", "'Hai già votato: '+N(mine[id.team])")
        s=sost(s,"(!closed&&id&&mine[id.team]?", "(false?")
        s=s.replace("knownLogin=login;myVote=null;", "knownLogin=login;myVote=null;readyVote=false;")
        s=s.replace("myVote=choice}catch", "myVote=choice;readyVote=true}catch")
        s=s.replace("pollError='La votazione non si è aggiornata.", "readyVote=false;pollError='La votazione non si è aggiornata.")
        s=s.replace("busyVote=false;redrawPoll()", "busyVote=false;readyVote=!!myVote;redrawPoll();window.dispatchEvent(new Event('og:voto62'));await refresh()")
        s=s.replace("myVote=null;mount();refresh()", "myVote=null;readyVote=false;mount();refresh()")
        marker='async function start(){'
        hooks="const votoCanale=typeof BroadcastChannel==='function'?new BroadcastChannel('girrr-voti62'):null;\nwindow.addEventListener('og:voto62',()=>votoCanale?.postMessage('rileggi'));if(votoCanale)votoCanale.onmessage=()=>{readyVote=false;redrawPoll();refresh()};\nfunction rileggiVoto(){readyVote=false;redrawPoll();refresh()}window.addEventListener('focus',rileggiVoto);window.addEventListener('pageshow',rileggiVoto);document.addEventListener('visibilitychange',()=>{if(!document.hidden)rileggiVoto()});setInterval(()=>{if(!document.hidden)refresh()},15000);\n"
        s=sost(s,marker,hooks+marker)
    out[p]=s
    for skin in ('girrr','stadio/girrr'):
        prefix='../' if skin=='girrr' else '../../'
        for name in ('app.html','curva.html'):
            p=base/skin/name;s=p.read_text()
            if 'sondaggi62.js' not in s:s=sost(s,'</head>',f'<script src="{prefix}sondaggi62.js?v=62-nativa1"></script></head>')
            if name=='app.html' and "['sondaggi','Sondaggi']" not in s:
                s=sost(s,"['conf','Conferenze stampa'],['radio','Radio']", "['conf','Conferenze stampa'],['sondaggi','Sondaggi'],['radio','Radio']")
                s=sost(s,"sp==='conf'?spConf():sp==='radio'?", "sp==='conf'?spConf():sp==='sondaggi'?'<div class=\"v53\" data-v62-sondaggi=\"sport\">'+(window.GirrrSondaggi62?GirrrSondaggi62.html('sport'):'Caricamento…')+'</div>':sp==='radio'?")
                s=sost(s,"function spConf(){var x=vConf();", "function spConf(){var x=vConf();x+='<div data-v62-precedenti></div>';")
                # L'app possiede già la navigazione; il nuovo ingresso usa la stessa S.sp.
                s=sost(s,"var sp=S.sp,tabs=", "var sp=S.sp,tabs=")
                s=sost(s,"window.GirrrApp={render:function(){render()},", "window.GirrrApp={render:function(){render()},")
                # Accoglie il link dalla Curva prima del primo disegno.
                s=sost(s,"function vSport(){\n  var sp=S.sp,", "function vSport(){\n  if(new URLSearchParams(location.search).get('sezione')==='sondaggi'){S.sp='sondaggi';var su=new URL(location.href);su.searchParams.delete('sezione');history.replaceState(null,'',su)}\n  var sp=S.sp,")
                hook="<script>(function(){let pending=false;function monta(){document.querySelectorAll('[data-v62-sondaggi]').forEach(h=>window.GirrrSondaggi62?.mount(h,h.dataset.v62Sondaggi));document.querySelectorAll('[data-v62-precedenti]').forEach(h=>{if(!h.dataset.avviato){h.dataset.avviato='1';window.GirrrSondaggi62?.precedenti(h)}})}new MutationObserver(()=>{if(!pending){pending=true;requestAnimationFrame(()=>{pending=false;monta()})}}).observe(document.getElementById('view'),{childList:true,subtree:true});monta()})();</script>"
                s=sost(s,'</body>',hook+'</body>')
            if name=='app.html' and '/* host62 */' not in s:
                s=sost(s,"    if(a.nodeType!==1)continue;", "    if(a.nodeType!==1)continue;\n    /* host62 */ if((a.hasAttribute('data-v62-precedenti')&&b.hasAttribute('data-v62-precedenti'))||(a.hasAttribute('data-v62-sondaggi')&&b.hasAttribute('data-v62-sondaggi')))continue;")
                s=s.replace("{childList:true});monta()", "{childList:true,subtree:true});monta()")
            if name=='app.html' and 'var cfW62=' not in s:
                s=sost(s,'function vConfL(){',"function vConfL(){\n  var cfW62=window.GirrrFinestre62?GirrrFinestre62('vigilia',D.cal[0]&&D.cal[0].n):{aperta:false,testo:'Caricamento della scadenza…'};")
                s=sost(s,'done=ch.every(function(c){return c}),lk=confBloccata(),dis=lk?', 'done=cfW62.aperta&&ch.every(function(c){return c}),lk=confBloccata(),dis=(lk||!cfW62.aperta)?')
                s=sost(s,"  Q.forEach(function(q,i){h+=", "  h+='<p class=\"sm mut\">'+esc(cfW62.testo)+'</p>';\n  Q.forEach(function(q,i){h+=")
            out[p]=s
    p=base/'conferenze.js';s=p.read_text()
    if 'var cfD62=' not in s:
        s=sost(s,"var g = ultimaGiocata(t); if (!g) return '';", "var g = ultimaGiocata(t); if (!g) return '';\n    var cfD62=window.GirrrFinestre62?GirrrFinestre62('dopo',g.n):{aperta:false,testo:'Caricamento della scadenza…'};")
        s=sost(s,"(scelta && !dsInvio ? '' : ' disabled')", "(scelta && !dsInvio && cfD62.aperta ? '' : ' disabled')")
        s=sost(s,"    if (dopoAttivo === false) h +=", "    h+='<p class=\"sm mut\">'+E(cfD62.testo)+'</p>';\n    if (dopoAttivo === false) h +=")
    out[p]=s
    for p,s in out.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)

if __name__=='__main__':
    import sys
    prepara(Path(sys.argv[1]).resolve())
