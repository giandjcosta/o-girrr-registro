#!/usr/bin/env python3
"""Curva · Condividi con l'immagine del post (Claude, 9 novembre 2026, segnalazione di Gianluca).

Il pulsante Condividi della Curva disegnava l'immagine da mandare su WhatsApp con il testo del post, ma prendeva solo
le foto caricate dagli utenti: i post dei risultati (Lega e Champions Cup, con il Tabellone della giornata) e le
immagini dei personaggi uscivano senza immagine. Ora, se il post ha un'immagine visibile nella Curva, si usa quella.

Uso:
  python3 rilascio/curva562/condividi_img.py COPIA_GH_PAGES          scrive girrr/curva.html e stadio/girrr/curva.html (rilascio)
  python3 rilascio/curva562/condividi_img.py COPIA_GH_PAGES --lab    le scrive in rilascio/curva562/pagine/ (prova nel Lab)
Si può rilanciare: se la correzione c'è già non cambia niente.
"""
import pathlib, sys

QUI = pathlib.Path(__file__).resolve().parent
A = sys.argv[1:]
if not A:
    sys.exit(__doc__)
GH = pathlib.Path(A[0]); OUT = QUI / "pagine" if "--lab" in A else GH
PRIMA = "var ph=p.hi&&IM[p.id]?IM[p.id]:null;"
DOPO = (PRIMA + "\n /* Claude, 5.6.2: anche l'immagine che il post mostra nella Curva (Tabellone dei risultati, immagini dei personaggi) */"
        "\n if(!ph){var sel='article.post[data-k=\"'+(window.CSS&&CSS.escape?CSS.escape(k):k)+'\"] .pimg img',vis=Array.prototype.filter.call(document.querySelectorAll(sel),function(x){return x.complete&&x.naturalWidth>0&&x.offsetParent!==null})[0];if(vis)ph=vis.currentSrc||vis.src}")
for rel in ("girrr/curva.html", "stadio/girrr/curva.html"):
    t = (GH / rel).read_text(encoding="utf-8")
    if "Claude, 5.6.2: anche l'immagine" not in t:
        if t.count(PRIMA) != 1:
            sys.exit(f"{rel}: il Condividi della Curva è cambiato, controlla a mano")
        t = t.replace(PRIMA, DOPO)
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(t, encoding="utf-8")
    print("scritta", dest)
