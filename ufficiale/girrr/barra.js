/* Barra di navigazione dell'anteprima: compare solo quando la pagina è aperta da sola (fuori dal contenitore con l'interruttore). */
(function(){
if(window.top!==window.self||window._barra)return;window._barra=1;
var p=location.pathname,i=p.indexOf('/ufficiale/'),j=p.indexOf('/anteprima/'),k=i>=0?i:j;if(k<0)return;
var base=p.slice(0,k+1),nuova=(p.indexOf('/ufficiale/nuovo/')>=0||/\/anteprima\/(index\.html)?$/.test(p));
function a(h,t,on){return '<a href="'+h+'"'+(on?' class="on"':'')+'>'+t+'</a>'}
var st=document.createElement('style');
st.textContent='#barra{position:sticky;top:0;z-index:9999;display:flex;gap:4px;justify-content:center;flex-wrap:wrap;padding:6px 8px;background:#0f1630;border-bottom:1px solid rgba(255,255,255,.14);font-family:Inter,system-ui,sans-serif}#barra a{color:#fbf6ec;opacity:.75;text-decoration:none;font-weight:800;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:6px 10px;border-radius:99px;white-space:nowrap}#barra a.on{background:#d62839;opacity:1}';
function go(){var d=document.createElement('div');d.id='barra';
d.innerHTML=a(base,'Changelog')+a(base+'aggiornamenti.html','Aggiornamenti')+a(base+'ufficiale/#'+(nuova?'nuova':'attuale'),'Anteprima 5.0',1)+a(base+'lab/','Laboratorio');
document.head.appendChild(st);document.body.insertBefore(d,document.body.firstChild)}
if(document.body)go();else document.addEventListener('DOMContentLoaded',go);
})();
