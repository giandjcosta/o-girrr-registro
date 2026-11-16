#!/usr/bin/env python3
"""6.2.1 · Home, «Oggi al Girrr»: i collegamenti portano alla giornata giusta in tutti i browser (Claude, 16 novembre 2026).

- I cerchi del «Cammino in classifica» sono collegamenti dentro un disegno (SVG). Nei browser senza transizioni
  native (Firefox, Safari meno recenti) la dissolvenza di ui.js leggeva `l.href`, che nei disegni non è un testo,
  e mandava a «[object SVGAnimatedString]» (pagina 404). Ora legge l'attributo href.
- Destinazioni (richiesta di Gianluca): i cerchi aprono la Classifica dopo quella giornata; Ultimo risultato,
  Le ultime cinque, Prossima sfida e Le prossime tre aprono i Risultati della giornata.

Uso: python3 rilascio/r621/applica.py COPIA_GH_PAGES   (si ferma se il file non è quello atteso; rieseguibile)
"""
import pathlib, sys

LAVORI = {
    'girrr/v55/ui.js': [
        ("var u;try{u=new URL(l.href,location.href)}catch(x){return}",
         "var u;try{u=new URL(l.getAttribute('href'),location.href)}catch(x){return}"),  # 6.2.1: anche i collegamenti dei disegni (SVG)
        ("dayLink:function(n){return href('tabellone')+'#lega-'+n}",
         "dayLink:function(n,sez){return href('tabellone')+'?sezione='+(sez||'risultati')+'#lega-'+n}"),  # 6.2.1: Risultati della giornata
    ],
    'girrr/v55/home55.js': [
        ("circleChart(series,'Posizioni nelle ultime giornate',o.dayLink,false)",
         "circleChart(series,'Posizioni nelle ultime giornate',function(n){return o.dayLink(n,'classifica')},false)"),  # 6.2.1: Classifica dopo la giornata
    ],
}


def applica(t, nome, coppie):
    for vecchio, nuovo in coppie:
        if nuovo in t:
            continue
        if t.count(vecchio) != 1:
            raise SystemExit('%s: atteso una volta «%s…», trovato %d volte' % (nome, vecchio[:60], t.count(vecchio)))
        t = t.replace(vecchio, nuovo)
    return t


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    base = pathlib.Path(argv[0])
    uscite = [(base / p, applica((base / p).read_text(encoding='utf-8'), p, c)) for p, c in LAVORI.items()]
    for dst, t in uscite:
        dst.write_text(t, encoding='utf-8')
        print('Scritto', dst)
    # Versione nell'indirizzo dei due file: senza, i telefoni tengono quelli vecchi in memoria.
    cambiate = 0
    for html in sorted(base.rglob('*.html')):
        t = html.read_text(encoding='utf-8')
        n = t.replace('v55/ui.js?v=55r10', 'v55/ui.js?v=621').replace('v55/home55.js?v=55r8', 'v55/home55.js?v=621')
        if n != t:
            html.write_text(n, encoding='utf-8'); cambiate += 1
    if not cambiate and not any('v55/ui.js?v=621' in h.read_text(encoding='utf-8') for h in base.rglob('*.html')):
        raise SystemExit('Nessuna pagina carica v55/ui.js?v=55r10: base diversa da quella attesa')
    print('Pagine con la versione 6.2.1 dei due file:', cambiate)


if __name__ == '__main__':
    main(sys.argv[1:])
