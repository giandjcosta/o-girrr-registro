(function(){'use strict';
  var base=new URL('./',document.currentScript.src),frame=document.getElementById('contenuto');
  var routes={changelog:['index.html','Changelog'],lab:['lab/','Lab'],anteprima:['ufficiale/','Anteprima'],aggiornamenti:['aggiornamenti.html','Aggiornamenti'],archivio:['archivio.html','Archivio'],ramificazioni:['ramificazioni.html','Ramificazioni']};
  var current='',status=document.getElementById('stato'),skin=document.getElementById('grafica'),select=document.getElementById('sezione');
  function section(){var key=location.hash.slice(1);return Object.prototype.hasOwnProperty.call(routes,key)?key:'changelog';}
  function navigate(){var key=section();if(key===current)return;current=key;
    document.querySelectorAll('#menu a').forEach(function(a){if(a.hash==='#'+key)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    select.value=key;document.title=routes[key][1]+' · Registro O Girrr';frame.title=routes[key][1]+' del Registro';frame.setAttribute('aria-busy','true');status.textContent='Caricamento…';skin.hidden=key!=='anteprima';
    var target=new URL(routes[key][0]+'?nel-registro=1',base).href;
    frame.dataset.src=target;frame.contentWindow.location.replace(target);
  }
  function skinState(){try{var toggle=frame.contentDocument.getElementById('tg');skin.textContent='Grafica: '+(toggle&&toggle.getAttribute('aria-checked')==='true'?'Stadio':'Lega');}catch(e){}}
  function routeKey(url){if(url.origin!==base.origin)return null;return Object.keys(routes).find(function(k){var path=new URL(routes[k][0],base).pathname;return url.pathname===path||url.pathname===path+'index.html'||(k==='changelog'&&url.pathname===base.pathname);});}
  function connect(doc){
    if(!doc||doc.documentElement.dataset.registroCollegato)return;doc.documentElement.dataset.registroCollegato='true';
    doc.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||a.hasAttribute('download'))return;
      var url=new URL(a.href,doc.location.href),key=routeKey(url);
      if(key){e.preventDefault();location.hash=key;return;}
      // I prototipi locali restano nel portale; i collegamenti esterni mantengono il loro comportamento.
      if(url.origin===base.origin&&url.pathname.startsWith(base.pathname)&&a.target==='_blank')a.target='_self';
    });
  }
  frame.addEventListener('load',function(){
    try{var doc=frame.contentDocument;if(!doc||doc.location.href==='about:blank'||(frame.hasAttribute('aria-busy')&&doc.location.href!==frame.dataset.src))return;connect(doc);
      var style=doc.createElement('style');style.textContent='body>.w>.g.top,body>main.w>header.g.top,body>.w>.tabs,body>main.w>.tabs{display:none!important}';
      if(current==='archivio')style.textContent+='main>nav{display:none!important}';
      if(current==='anteprima'&&doc.getElementById('tg')){
        style.textContent+='html{--bh:0px!important}.bar{display:none!important}#f{top:0!important;height:100%!important}';
        var inner=doc.getElementById('f');inner.addEventListener('load',function(){try{connect(inner.contentDocument);}catch(e){}skinState();});
        try{connect(inner.contentDocument);}catch(e){}skinState();
      }
      doc.head.appendChild(style);status.textContent=current==='anteprima'?'Anteprima in sola lettura':'';
    }catch(e){status.textContent='La pagina è aperta. Il menu resta disponibile.';}
    frame.removeAttribute('aria-busy');
  });
  skin.addEventListener('click',function(){try{frame.contentDocument.getElementById('tg').click();skinState();}catch(e){}});
  select.addEventListener('change',function(){location.hash=select.value;});window.addEventListener('hashchange',navigate);
  fetch(new URL('registro-stato.json',base),{cache:'no-cache'}).then(function(r){if(!r.ok)throw Error();return r.json();}).then(function(s){document.getElementById('versione').textContent='Anteprima '+s.versione;}).catch(function(){});
  navigate();
})();
