/* I vecchi indirizzi continuano a funzionare e aprono lo stesso portale. */
(function(){'use strict';
  var script=document.currentScript;
  if(window.self!==window.top || new URLSearchParams(location.search).has('nel-registro'))return;
  var target=new URL('registro.html',script.src);
  target.hash=script.dataset.sezione||'changelog';
  location.replace(target.href);
})();
