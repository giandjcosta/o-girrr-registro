#!/usr/bin/env python3
"""Curva · Cuori e rilanci colorati anche sul telefono (Claude, 10 novembre 2026, segnalazione di Gianluca).

I colori di «già messo» (cuore rosa pieno, rilancio verde, risposta azzurra) stavano dentro @media (hover:hover):
valevano solo con il mouse. Sul telefono il cuore restava con il bordo grigio e il rilancio tutto grigio,
così non si vedeva a quali post si era già messo il cuore o fatto il rilancio. Ora valgono su ogni schermo,
e al tocco il cuore si colora subito (prima aspettava che la Curva si ricaricasse dal database).

Uso:
  python3 rilascio/curva563/cuori.py COPIA_GH_PAGES          scrive girrr/curva.html e stadio/girrr/curva.html (rilascio)
  python3 rilascio/curva563/cuori.py COPIA_GH_PAGES --lab    le scrive in rilascio/curva563/pagine/ (prova nel Lab)
Si può rilanciare: se la correzione c'è già non cambia niente.
"""
import pathlib, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0]); OUT = QUI / "pagine" if "--lab" in A else GH
PRIMA = ".acts .app.on svg{fill:var(--pk);animation:pop .35s ease}"
SEGNO = "/* Claude, 5.6.3: già messo"
DOPO = (PRIMA + "\n" + SEGNO + ", colori su ogni schermo (prima solo con il mouse) */"
        "\n.acts .rsp.on{color:var(--blu)}.acts .ril.on{color:var(--gr)}.acts .app.on{color:var(--pk)}")
# Al tocco il cuore (o il rilancio) si colora subito, senza aspettare che la Curva si ricarichi; se il database dice di no, torna com'era
R_PRIMA = " var key=k+'|'+kind,on=!MN[key];\n rpc('curva_reagisci',{p_team:me,p_code:code,p_k:k,p_kind:kind}).then(function(){ev1('curva/reazione','Curva: applauso o rilancio');return carica()}).then(function(){render()}).catch(function(e){toast(e.message)})}"
R_DOPO = (" var key=k+'|'+kind,on=!MN[key];\n"
          " /* Claude, 5.6.3: si colora subito al tocco */"
          "try{document.querySelectorAll('article.post[data-k=\"'+(window.CSS&&CSS.escape?CSS.escape(k):k)+'\"] .acts .'+(kind==='a'?'app':'ril')).forEach(function(b){b.classList.toggle('on',on)})}catch(e){}\n"
          " rpc('curva_reagisci',{p_team:me,p_code:code,p_k:k,p_kind:kind}).then(function(){ev1('curva/reazione','Curva: applauso o rilancio');return carica()}).then(function(){render()}).catch(function(e){render();toast(e.message)})}")
for rel in ("girrr/curva.html", "stadio/girrr/curva.html"):
    src = GH / rel
    t = src.read_text(encoding="utf-8")
    if SEGNO not in t:
        if t.count(PRIMA) != 1 or t.count(R_PRIMA) != 1:
            sys.exit(f"{rel}: lo stile o il tocco dei cuori è cambiato, controlla a mano")
        t = t.replace(PRIMA, DOPO).replace(R_PRIMA, R_DOPO)
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(t, encoding="utf-8")
    print("scritta", dest)
