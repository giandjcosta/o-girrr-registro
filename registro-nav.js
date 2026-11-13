/* I collegamenti correnti del Lab seguono la versione pubblicata, non i prototipi storici. */
(function () {
  var root = new URL('./', document.currentScript.src);
  var nav=document.querySelector('.tabs');
  if(nav&&!nav.querySelector('[data-ramificazioni]')){var a=document.createElement('a');a.dataset.ramificazioni='';a.href=new URL('ramificazioni.html',root);a.textContent='Ramificazioni';nav.append(a);}
  fetch(new URL('registro-stato.json', root), {cache: 'no-cache'}).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function (state) {
    document.querySelectorAll('a').forEach(function (a) {
      var t = a.textContent.trim();
      if (/^Anteprima 5\.5$/.test(t)) { a.textContent = 'Anteprima ' + state.versione; a.href = new URL('ufficiale/', root); }
      if (/^Archivio 5\.3$/.test(t)) { a.textContent = 'Archivio'; a.href = new URL('archivio.html', root); }
    });
  }).catch(function () {});
})();
