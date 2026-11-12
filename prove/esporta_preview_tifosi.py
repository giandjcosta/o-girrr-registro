"""Esporta la preview locale in un HTML navigabile, senza commit o hosting.
La cornice risolve letture e asset da un archivio incorporato. Le pagine e il
blocco scritture sono quelli della preview; non è un pacchetto da pubblicare.
"""
from pathlib import Path
import base64,hashlib,json,re,mimetypes,html
R=Path(__file__).resolve().parents[1]
ROOT=R/'.preview-site';OUT=R/'consegna';OUT.mkdir(exist_ok=True)
files={}
for f in ROOT.rglob('*'):
 if not f.is_file() or f.suffix not in ['.html','.js','.css','.json','.png','.jpg','.svg','.woff2']:continue
 key='/'+str(f.relative_to(ROOT))
 if f.suffix=='.html' and not key.startswith('/lab/prova-tifosi/'):continue
 files[key]=[mimetypes.guess_type(f.name)[0] or 'application/octet-stream',base64.b64encode(f.read_bytes()).decode()]
# Incorpora anche i font già verificati dal bridge TLS del collaudo.
cache=Path('/tmp/girrr-browser-cache')
remote=set()
for path in (ROOT/'lab/prova-tifosi').rglob('*.html'):
 remote.update(html.unescape(u) for u in re.findall(r"https://fonts\.googleapis\.com/[^\"'\s<>)]+",path.read_text()))
for url in list(remote):
 f=cache/hashlib.sha256(url.encode()).hexdigest()
 if f.exists():remote.update(re.findall(r'https://fonts\.gstatic\.com/[^)"\s]+',f.read_text()))
for url in remote:
 f=cache/hashlib.sha256(url.encode()).hexdigest();meta=f.with_suffix('.json')
 if f.exists() and meta.exists():files[url]=[json.loads(meta.read_text())['content-type'],base64.b64encode(f.read_bytes()).decode()]
JS=r'''
const FILES=__FILES__,ORIGIN='https://girrr-preview.invalid',ENTRY='/lab/prova-tifosi/index.html';
let frame=document.querySelector('iframe'),current='';
function norm(u,base=ORIGIN+ENTRY){let x=new URL(u,base);let key=x.origin===ORIGIN?decodeURIComponent(x.pathname).replace(/^\/o-girrr-registro\//,'/'):x.href;if(key.endsWith('/'))key+='index.html';return key}
function get(u){return FILES[norm(u)]}
function bytes(v){return Uint8Array.from(atob(v[1]),c=>c.charCodeAt(0))}
function txt(v){return new TextDecoder().decode(bytes(v))}
function asset(u,base){if(!u||/^(data:|blob:|#)/.test(u))return u;let v=FILES[norm(u,base)];return v?'data:'+v[0]+';base64,'+v[1]:new URL(u,base).href}
function css(s,base){return s.replace(/url\(\s*(['"]?)([^)'"\s]+)\1\s*\)/g,(_,q,u)=>'url("'+asset(u,base)+'")')}
function js(s){return s.replace(/\b(?:window\.|document\.)?location\b/g,'window.__ptLocation')}
function bootstrap(virtualUrl){
 const src=String.raw`
(function(){
 let u=new URL(__URL__);const loc={toString:()=>u.href,assign:v=>nav(v),replace:v=>nav(v),reload:()=>nav(u.href,true)};
 function nav(v,force=false){parent.postMessage({girrr:'navigate',url:new URL(v,u).href,force},'*')}
 for(const k of ['href','hash','search','pathname','hostname','host','protocol','origin','port'])Object.defineProperty(loc,k,{get:()=>u[k],set:v=>{let n=new URL(u);n[k]=v;nav(n.href)}});
 window.__ptLocation=loc;
 history.replaceState=history.pushState=function(state,unused,value){if(value){u=new URL(value,u);parent.postMessage({girrr:'state',url:u.href},'*')}};
 window.fetch=function(input,init){let url=typeof input==='string'?input:(input.url||String(input));let v=parent.__girrrGet(new URL(url,document.baseURI).href);return new Promise(resolve=>{const ready=()=>setTimeout(()=>resolve(v?new Response(Uint8Array.from(atob(v[1]),c=>c.charCodeAt(0)),{status:200,headers:{'Content-Type':v[0]}}):new Response('File non presente nella prova',{status:404})),0);if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready,{once:true});else ready()})};
 // Le pagine native leggono anche il JSON con una XHR sincrona.
 class LocalXHR extends EventTarget{
  constructor(){super();this.readyState=0;this.status=0;this.responseType='';this.responseText='';this.response=null;this.withCredentials=false;this.timeout=0}
  event(name){this.dispatchEvent(new Event(name));if(typeof this['on'+name]==='function')this['on'+name](new Event(name))}
  open(method,url,async=true){this.method=method;this.url=new URL(url,document.baseURI).href;this.async=async;this.readyState=1;this.event('readystatechange')}
  setRequestHeader(){}
  getResponseHeader(key){return key.toLowerCase()==='content-type'?this.mime:null}
  getAllResponseHeaders(){return 'Content-Type: '+(this.mime||'text/plain')+'\r\n'}
  overrideMimeType(m){this.mime=m}
  abort(){this.status=0;this.event('abort');this.event('loadend')}
  send(){const run=()=>{const v=parent.__girrrGet(this.url);this.status=v?200:404;this.statusText=v?'OK':'Not Found';this.mime=v?.[0]||'text/plain';this.responseURL=this.url;const bytes=v?Uint8Array.from(atob(v[1]),c=>c.charCodeAt(0)):new Uint8Array();this.responseText=new TextDecoder().decode(bytes);this.response=this.responseType==='json'?JSON.parse(this.responseText):this.responseType==='arraybuffer'?bytes.buffer:this.responseText;this.readyState=4;this.event('readystatechange');this.event('load');this.event('loadend')};if(this.async)setTimeout(run,0);else run()}
 }
 Object.assign(LocalXHR,{UNSENT:0,OPENED:1,HEADERS_RECEIVED:2,LOADING:3,DONE:4});window.XMLHttpRequest=LocalXHR;
 const img=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype,'src');Object.defineProperty(HTMLImageElement.prototype,'src',{get:img.get,set(v){img.set.call(this,parent.__girrrAsset(v,document.baseURI))}});
 function repair(el){if(el.nodeType!==1)return;if(el.matches('img')){const a=el.getAttribute('src');if(a&&!a.startsWith('data:'))el.src=a;el.removeAttribute('srcset')}el.querySelectorAll('img').forEach(repair)}
 const set=Element.prototype.setAttribute;Element.prototype.setAttribute=function(k,v){if(this.tagName==='IMG'&&k.toLowerCase()==='src')v=parent.__girrrAsset(v,document.baseURI);return set.call(this,k,v)};
 new MutationObserver(ms=>ms.forEach(m=>m.type==='attributes'?repair(m.target):m.addedNodes.forEach(repair))).observe(document,{childList:true,subtree:true,attributes:true,attributeFilter:['src']});
 // Le pagine della prova si aprono prima dei gestori nativi di transizione.
 document.addEventListener('click',e=>{let a=e.target.closest('a[href]');if(!a||a.hasAttribute('download'))return;const href=a.getAttribute('href');if(/^(javascript:|mailto:|tel:|#)/.test(href))return;const target=new URL(href,document.baseURI);if(target.origin!==u.origin||!target.pathname.startsWith('/lab/prova-tifosi/'))return;const v=parent.__girrrGet(target.href);if(!v||!v[0].includes('html'))return;e.preventDefault();e.stopImmediatePropagation();nav(target.href)},true);
})();`.replace('__URL__',JSON.stringify(virtualUrl));
 return src;
}
window.__girrrGet=get;window.__girrrAsset=asset;
function remember(u){current=u;history.replaceState(null,'','#'+encodeURIComponent(new URL(u).pathname+new URL(u).search+new URL(u).hash))}
function navigate(url,force=false){
 let u=new URL(url,ORIGIN+ENTRY);if(u.origin!==ORIGIN)return;if(!force&&u.href===current)return;
 let file=get(u.href);if(!file||!file[0].includes('html'))return;
 remember(u.href);let d=new DOMParser().parseFromString(txt(file),'text/html');
 let b=d.querySelector('base');if(!b){b=d.createElement('base');d.head.prepend(b)}b.href=new URL(b.getAttribute('href')||u.href,u.href).href;let base=b.href;
 d.querySelectorAll('meta[http-equiv=refresh],link[rel=manifest],link[rel=preload]').forEach(e=>e.remove());
 d.querySelectorAll('link[rel=stylesheet]').forEach(el=>{let url=new URL(el.getAttribute('href'),base).href,v=get(url);if(v){let s=d.createElement('style');s.textContent=css(txt(v),url);el.replaceWith(s)}});
 d.querySelectorAll('style').forEach(el=>el.textContent=css(el.textContent,base));
 d.querySelectorAll('[style]').forEach(el=>el.setAttribute('style',css(el.getAttribute('style'),base)));
 d.querySelectorAll('img').forEach(el=>{if(el.hasAttribute('src'))el.src=asset(el.getAttribute('src'),base);el.removeAttribute('srcset')});
 d.querySelectorAll('link[rel=icon]').forEach(el=>el.href=asset(el.getAttribute('href'),base));
 d.querySelectorAll('script').forEach(el=>{if(el.type==='application/json')return;let url=el.getAttribute('src'),v=url&&get(new URL(url,base).href);if(url&&!v){el.remove();return}let code=v?txt(v):el.textContent;let deferred=el.hasAttribute('defer');el.removeAttribute('src');el.removeAttribute('defer');el.removeAttribute('async');el.textContent=(url?'Object.defineProperty(document.currentScript,"src",{configurable:true,value:'+JSON.stringify(new URL(url,base).href)+'});\n':'')+js(code);if(deferred)d.body.append(el)});
 let boot=d.createElement('script');boot.textContent=bootstrap(u.href);b.insertAdjacentElement('afterend',boot);
 // Chiusure script nel testo JS vengono evitate senza cambiare i sorgenti sul disco.
 // Un nuovo contesto per pagina esclude messaggi e caricamenti del documento precedente.
 const next=document.createElement('iframe');next.title='Anteprima navigabile O Girrr';next.srcdoc='<!doctype html>'+d.documentElement.outerHTML;const previous=frame;frame=next;previous.replaceWith(next);
}
addEventListener('message',e=>{if(e.source!==frame.contentWindow||!e.data?.girrr)return;if(e.data.girrr==='navigate')navigate(e.data.url,e.data.force);if(e.data.girrr==='state')remember(e.data.url)});
addEventListener('popstate',()=>navigate(decodeURIComponent(location.hash.slice(1))||ENTRY,true));
let initial=location.hash?decodeURIComponent(location.hash.slice(1)):ENTRY;navigate(initial);
'''.replace('__FILES__',json.dumps(files,separators=(',',':')))
# Tutti i dati sono base64: nessun delimitatore HTML dei sorgenti entra nello script.
page='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Revisione O Girrr · Lega e Stadio</title><style>html,body{margin:0;height:100%;background:#141d3d}iframe{border:0;width:100%;height:100%;display:block}</style><iframe title="Anteprima navigabile O Girrr"></iframe><script>'+JS.replace('</script','<\\/script')+'</script></html>'
(OUT/'revisione-girrr.html').write_text(page)
print('Esportata anteprima navigabile:',OUT/'revisione-girrr.html',round(len(page)/1e6,1),'MB')
