"""Home: la striscia (classifica, ultima giornata, prossimo turno) dice cosa sta succedendo.
Mentre carica: "Aggiorno i dati…"; se data.json non arriva: messaggio e "Riprova"; sotto la striscia: "Dati aggiornati al …" da data.json (campo updated).
Lo usa ufficiale/build.py (anteprima e rilascio); si può lanciare anche da solo sulle pagine già fatte: python3 ufficiale/src/home_stato.py <index.html>..."""
import sys

CSS = ("<style>.st0{grid-column:1/-1;display:flex;align-items:center;gap:12px;flex-wrap:wrap}.st0 span{margin:0!important}"
       ".st0 .gir{width:14px;height:14px;flex:none;border-radius:50%;border:2px solid var(--sub);border-top-color:var(--hi);animation:stgir .9s linear infinite}"
       "@keyframes stgir{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.st0 .gir{animation:none}}"
       ".st0 button{margin-left:auto;font:800 12px Inter,system-ui,sans-serif;letter-spacing:.08em;padding:8px 14px;border-radius:99px;border:0;background:var(--hi);color:#1d2a52;cursor:pointer}"
       ".agg{margin:-18px 0 26px;font-size:12px;font-weight:600;color:var(--sub);text-align:right}.agg:empty{display:none}</style>\n</head>")

STRIP_A = '<section class="strip" id="strip"></section>'
STRIP_B = ('<section class="strip" id="strip" aria-live="polite"><div class="st st0"><i class="gir" aria-hidden="true"></i><span>Aggiorno i dati…</span></div></section>\n'
           '  <p class="agg" id="agg"></p>')

DATA_A = "  var L=d.cal.lega,pl=L.filter("
DATA_B = ("  try{var _u=new Date(d.updated+'T12:00:00'),_o=new Date();document.getElementById('agg').textContent=isNaN(_u)?'':"
          "(_u.toDateString()===_o.toDateString()?'Dati aggiornati oggi':'Dati aggiornati a '+_u.toLocaleDateString('it-IT',{weekday:'long',day:'numeric',month:'long'}))}catch(e){}\n"
          "  var L=d.cal.lega,pl=L.filter(")

VUOTA_A = "  document.getElementById('strip').innerHTML=h;"
VUOTA_B = "  document.getElementById('strip').innerHTML=h||'<div class=\"st st0\"><span>Il campionato non è ancora cominciato: qui arrivano classifica e risultati.</span></div>';"

ERR_A = "}).catch(function(){});\nfunction cdTxt("
ERR_B = ("}).catch(function(){var s=document.getElementById('strip');if(s&&s.querySelector('.gir'))s.innerHTML="
         "'<div class=\"st st0\"><span>I dati della lega non si sono caricati. Controlla la connessione.</span><button type=\"button\" onclick=\"location.reload()\">RIPROVA</button></div>'});\nfunction cdTxt(")


def applica(ix):
    for a, b in ((STRIP_A, STRIP_B), (DATA_A, DATA_B), (VUOTA_A, VUOTA_B), (ERR_A, ERR_B), ("</head>", CSS)):
        assert ix.count(a) == 1, ("home_stato", a[:60])
        ix = ix.replace(a, b, 1)
    return ix


if __name__ == "__main__":
    for p in sys.argv[1:]:
        with open(p, encoding="utf-8") as f: t = f.read()
        with open(p, "w", encoding="utf-8", newline="") as f: f.write(applica(t))
        print("home_stato:", p)
