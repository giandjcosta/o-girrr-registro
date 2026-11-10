#!/usr/bin/env python3
"""Conferenze stampa, Testa a testa e testo grande sulla TV (Claude, 10 novembre 2026, richiesta di Gianluca: «Farei le prime 6 più la 10»).

Cosa cambia nelle pagine del sito (copia di gh-pages):
  girrr/app.html, stadio/girrr/app.html
    - Conferenza: dopo la pubblicazione è bloccata («Pubblicata · Non si cambia più»); prima del bottone l'avviso che poi non si cambia.
    - Conferenza: riquadro «Cosa ha detto …» con la conferenza dell'avversario e il bottone «Rispondi in Curva».
    - Carriera: nuova scheda «Promesse» (tutte le promesse della stagione, esito e peso sulla fiducia).
    - Derby: riquadro «Testa a testa» in fondo alla pagina.
    - Includono conferenze.js (radice del sito).
  girrr/curva.html, stadio/girrr/curva.html
    - ?scrivi=… apre la Curva con il testo già scritto (il «Rispondi in Curva» della conferenza: «@squadra »).
  Tutte le pagine .html di girrr/ e stadio/girrr/ e lo Spogliatoio (index.html): includono tv.js (testo più grande solo sulla TV).
  Radice: copia conferenze.js e tv.js.
I calcoli (calcoli/post_curva.py, leggi_eventi.py, fiducia.py) si copiano a parte sul main del sito.

Uso:
  python3 rilascio/conferenze/applica.py COPIA_GH_PAGES          scrive nella copia (rilascio)
  python3 rilascio/conferenze/applica.py COPIA_GH_PAGES --lab    scrive in rilascio/conferenze/pagine/ (prova nel Lab); la Curva parte
                                                                 da rilascio/curva563/pagine/ se c'è (correzione 5.6.3 non ancora online)
Si può rilanciare: se una modifica c'è già non la rifà.
"""
import pathlib, re, shutil, sys

QUI = pathlib.Path(__file__).resolve().parent
REG = QUI.parent.parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0]); LAB = "--lab" in A
OUT = QUI / "pagine" if LAB else GH
SEGNO = "Claude, conferenze 10/11"


def sostituisci(t, rel, prima, dopo):
    if t.count(prima) != 1:
        sys.exit(f"{rel}: non trovo (o trovo più volte) il punto da cambiare: {prima[:70]!r}")
    return t.replace(prima, dopo)


def app(t, rel):
    if SEGNO in t:
        return t
    # script del modulo, accanto a stagione.js (stesso percorso relativo)
    m = re.search(r'<script src="((?:\.\./)+)stagione\.js" defer></script>', t)
    if not m:
        sys.exit(f"{rel}: non trovo stagione.js")
    t = t.replace(m.group(0), m.group(0) + f'\n<script src="{m.group(1)}conferenze.js" defer></script><!-- {SEGNO} -->', 1)
    # Carriera: scheda Promesse
    t = sostituisci(t, rel, "['fid','Fiducia'],", "['fid','Fiducia'],['prom','Promesse'],")
    t = sostituisci(t, rel, "else if(S.ctab==='stag')h+=(window.GirrrStagione?window.GirrrStagione(t):'');",
                    "else if(S.ctab==='stag')h+=(window.GirrrStagione?window.GirrrStagione(t):'');\n"
                    "  else if(S.ctab==='prom')h+=(window.GirrrPromesse?window.GirrrPromesse(t):'');")
    # Conferenza bloccata dopo la pubblicazione
    t = sostituisci(t, rel, "function vConfL(){\n  var t=ME,o=nextOpp(t),Q=confQs(t),cf=S.cf,ch=confChosen(t),done=ch.every(function(c){return c});",
                    "/* " + SEGNO + ": la conferenza della giornata, una volta nel database, non si cambia più */\n"
                    "function confBloccata(){var G=D.cal[0]&&D.cal[0].n;return DBS.conf.some(function(c){return c.giornata===G&&Array.isArray(c.risposte)&&c.risposte.length})}\n"
                    "/* le funzioni che servono a conferenze.js (questo script è chiuso: da fuori non si vedono) */\n"
                    "window.GirrrApp={render:function(){render()},gsPost:gsPost,isDer:isDer,rvInfo:rvInfo,rvWord:rvWord,derName:derName,mg:mg,me:function(){return GUEST?null:ME},toast:lvToast};\n"
                    "function vConfL(){\n  var t=ME,o=nextOpp(t),Q=confQs(t),cf=S.cf,ch=confChosen(t),done=ch.every(function(c){return c}),lk=confBloccata(),dis=lk?' disabled':'';")
    t = sostituisci(t, rel, """'<button data-cq="'+i+'" data-ca="'+j+'" aria-pressed="'+(cf.a[i]===j)+'">'""",
                    """'<button data-cq="'+i+'" data-ca="'+j+'" aria-pressed="'+(cf.a[i]===j)+'"'+dis+'>'""")
    t = sostituisci(t, rel, """'<input class="cfree" data-cf="'+i+'" maxlength="'+CFMAX+'" value="'+esc(cf.free[i])+'" placeholder="Scrivi la tua risposta" autocomplete="off" enterkeyhint="done">'""",
                    """'<input class="cfree" data-cf="'+i+'" maxlength="'+CFMAX+'" value="'+esc(cf.free[i])+'" placeholder="Scrivi la tua risposta" autocomplete="off" enterkeyhint="done"'+dis+'>'""")
    t = sostituisci(t, rel, """'<button data-cq="'+i+'" data-ca="free" aria-pressed="false">Rispondo a modo mio…</button>'""",
                    """'<button data-cq="'+i+'" data-ca="free" aria-pressed="false"'+dis+'>Rispondo a modo mio…</button>'""")
    t = sostituisci(t, rel, """  h+='<button class="btn" id="cpub" '+(done?'':'disabled style="opacity:.45;cursor:not-allowed"')+'>Pubblica su Curva</button></div>';""",
                    """  h+=lk?'<button class="btn" id="cpub" disabled style="opacity:.6;cursor:default">Pubblicata · Non si cambia più</button><p class="sm mut" style="margin-top:8px">La conferenza è uscita in Curva: le parole dette restano quelle.</p></div>'
    :'<button class="btn" id="cpub" '+(done?'':'disabled style="opacity:.45;cursor:not-allowed"')+'>Pubblica su Curva</button><p class="sm mut" style="margin-top:8px">Una volta pubblicata, la conferenza non si può più cambiare.</p></div>';""")
    t = sostituisci(t, rel, """    h+=lvDopo(t,ch,ch.filter(function(c){return c.w}).length)}
  return h+'<p class="note">Le dichiarazioni""",
                    """    h+=lvDopo(t,ch,ch.filter(function(c){return c.w}).length)}
  h+=(window.GirrrConfAvv?window.GirrrConfAvv(t,o,D.cal[0]&&D.cal[0].n):'');
  return h+'<p class="note">Le dichiarazioni""")
    t = sostituisci(t, rel, "function lvConfPubblica(){\n  var ch=confChosen(ME);",
                    "function lvConfPubblica(){\n  if(confBloccata()){lvToast('La conferenza è già pubblicata');return}\n  var ch=confChosen(ME);")
    # Derby: Testa a testa
    t = sostituisci(t, rel, """  h+='<p class="note">Le storie vengono dall\\'Albo d\\'oro e compariranno anche lì, una per ogni Derby. I voti sono quelli degli amici della lega.</p>';\n  return h;""",
                    """  h+=(window.GirrrTesta?window.GirrrTesta(GUEST?'':ME,GUEST?'':nextOpp(ME)):'');
  h+='<p class="note">Le storie vengono dall\\'Albo d\\'oro e compariranno anche lì, una per ogni Derby. I voti sono quelli degli amici della lega.</p>';\n  return h;""")
    return t


def curva(t, rel):
    if SEGNO in t:
        return t
    t = sostituisci(t, rel, " var tx=document.getElementById('tx');if(tx){tx.addEventListener('input',conta);conta()}",
                    " var tx=document.getElementById('tx');if(tx){tx.addEventListener('input',conta);conta()}\n"
                    " /* " + SEGNO + ": ?scrivi=… apre la Curva con il testo già scritto (Rispondi in Curva dalla conferenza) */\n"
                    " if(tx&&window.__scrivi){if(!tx.value){tx.value=window.__scrivi;conta()}tx.addEventListener('input',function(){window.__scrivi=tx.value||null});"
                    "if(!window.__scrivi0){window.__scrivi0=1;try{tx.focus();tx.setSelectionRange(tx.value.length,tx.value.length)}catch(e){}}"
                    "var g0=document.getElementById('go');if(g0)g0.addEventListener('click',function(){window.__scrivi=null})}")
    # il testo arriva una volta sola: si legge e si toglie dall'indirizzo
    t = sostituisci(t, rel, "function calcola(d){",
                    "(function(){try{var s=new URLSearchParams(location.search).get('scrivi');if(s){window.__scrivi=s.slice(0,300);"
                    "var r=location.search.replace(/([?&])scrivi=[^&]*&?/,'$1').replace(/[?&]$/,'');history.replaceState(null,'',location.pathname+r+location.hash)}}catch(e){}})();\n"
                    "function calcola(d){")
    return t


def tv(t, rel, prefisso):
    if "tv.js" in t:
        return t
    tag = f'<script src="{prefisso}tv.js"></script>'
    if re.search(r"<head[^>]*>", t, re.I):   # il prima possibile, così la pagina nasce già grande
        return re.sub(r"(<head[^>]*>)", lambda m: m.group(1) + tag, t, count=1, flags=re.I)
    if "<meta charset" in t:
        return t.replace("<meta charset", tag + "<meta charset", 1)
    return tag + t


def scrivi(rel, t):
    d = OUT / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    d.write_text(t, encoding="utf-8")
    print("scritta", d)


cambiate = {}
for rel in ("girrr/app.html", "stadio/girrr/app.html"):
    cambiate[rel] = app((GH / rel).read_text(encoding="utf-8"), rel)
for rel in ("girrr/curva.html", "stadio/girrr/curva.html"):
    base = REG / "rilascio/curva563/pagine" / rel if LAB and (REG / "rilascio/curva563/pagine" / rel).exists() else GH / rel
    cambiate[rel] = curva(base.read_text(encoding="utf-8"), rel)

if LAB:
    # nel Lab tv.js lo aggiunge lo specchio a ogni pagina: qui si scrivono solo le pagine cambiate, già con tv.js
    for rel, t in cambiate.items():
        scrivi(rel, tv(t, rel, "../../" if rel.startswith("stadio/") else "../"))
else:
    pagine = sorted(set([p.relative_to(GH).as_posix() for p in (GH / "girrr").glob("*.html")]
                        + [p.relative_to(GH).as_posix() for p in (GH / "stadio/girrr").glob("*.html")] + ["index.html"]))
    for rel in pagine:
        t = cambiate.get(rel) or (GH / rel).read_text(encoding="utf-8")
        prefisso = "../" * rel.count("/")
        nuovo = tv(t, rel, prefisso)
        if nuovo != (GH / rel).read_text(encoding="utf-8"):
            scrivi(rel, nuovo)
    for f in ("conferenze.js", "tv.js"):
        shutil.copy(QUI / f, GH / f)
        print("copiato", GH / f)
