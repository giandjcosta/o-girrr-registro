"""Sfondo delle pagine su un livello fisso a parte.

Le pagine avevano il gradiente sul body con background-attachment:fixed. Safari (iPhone e Mac) non lo rispetta bene e stira il
gradiente sull'altezza della pagina: così lo sfondo cambiava colore tra una pagina o una scheda corta e una lunga.
Qui ogni regola `body{... background-attachment:fixed ...}` viene riscritta: i gradienti passano su html::before (a schermo
intero, fisso, dietro a tutto), il body resta trasparente e l'html prende il colore pieno che aveva il body. Vale per la Lega e per lo Stadio.
"""
import re

# regola body{...} che contiene background-attachment:fixed (anche multilinea; dentro le graffe non ci sono altre graffe)
RULE = re.compile(r"(?<![\w.#:>,\-])body\{([^{}]*background-attachment:fixed[^{}]*)\}")
LAYER = "html::before{content:'';position:fixed;top:0;left:0;right:0;bottom:0;z-index:-2;pointer-events:none;%s}"
FINE = "body{background:transparent!important}"


def _dichiarazioni(s):
    """Divide per ';' solo fuori dalle parentesi (i gradienti ne hanno dentro)."""
    out, prof, cur = [], 0, ""
    for ch in s:
        prof += (ch == "(") - (ch == ")")
        if ch == ";" and prof == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [d.strip() for d in out if d.strip()]


def _riscrivi(m):
    resto, sfondo = [], []
    for d in _dichiarazioni(m.group(1)):
        nome = d.split(":", 1)[0].strip().lower()
        if nome == "background-attachment":
            continue
        if nome in ("background", "background-image") and "gradient(" in d:
            sfondo.append(d)
        else:
            resto.append(d)
    if not sfondo:   # nessun gradiente: si toglie solo il fixed
        return "body{%s}" % ";".join(resto)
    # colore pieno dell'html (anche sotto la barra di scorrimento): quello che il body aveva già, se c'era; altrimenti resta quello dell'html
    pieno = [d.split(":", 1)[1].strip() for d in resto if d.split(":", 1)[0].strip().lower() in ("background", "background-color")]
    html = "html{background-color:%s}" % pieno[-1] if pieno else ""
    return "body{%s}%s%s%s" % (";".join(resto), LAYER % ";".join(sfondo), html, FINE)


def applica(testo):
    """Ritorna (testo nuovo, quante regole riscritte)."""
    return RULE.subn(_riscrivi, testo)
