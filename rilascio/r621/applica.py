#!/usr/bin/env python3
"""6.2.1 · Home, «Oggi al Girrr»: i collegamenti portano alla giornata giusta in tutti i browser (Claude, 16 novembre 2026).

- I cerchi del «Cammino in classifica» sono collegamenti dentro un disegno (SVG). Nei browser senza transizioni
  native (Firefox, Safari meno recenti) la dissolvenza di ui.js leggeva `l.href`, che nei disegni non è un testo,
  e mandava a «[object SVGAnimatedString]» (pagina 404). Ora legge l'attributo href.
- Albo › Record: la «Serie di vittorie più lunga» senza il numero in oro (niente oro nell'Albo).
- MVP dei tifosi: «Giurie e criteri» resta aperta durante gli aggiornamenti; testo sui personaggi che votano durante
  la settimana e quanti hanno votato (con sql/mvp-personaggi-621.sql).
- Girrr Sport › Sondaggi: risultati con barre e percentuali staccate (prima solo testo, perché gli stili erano nella Curva).
- Destinazioni (richiesta di Gianluca): i cerchi aprono la Classifica dopo quella giornata; Ultimo risultato,
  Le ultime cinque, Prossima sfida e Le prossime tre aprono i Risultati della giornata.

Uso: python3 rilascio/r621/applica.py COPIA_GH_PAGES   (si ferma se il file non è quello atteso; rieseguibile)
"""
import pathlib, re, sys

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
    'sondaggi62.js': [
        # 6.2.1: in Girrr Sport i risultati del sondaggio avevano solo gli stili della Curva (barre e percentuali assenti).
        # Stili propri, solo dentro i riquadri di Girrr Sport: barre rosse nella Lega e oro nello Stadio.
        ("st.id='v62-cambia-css';st.textContent='",
         "st.id='v62-cambia-css';st.textContent=(function(){var c=/\\/stadio\\//.test(location.pathname)?'#ffd166':'#d62839';return '.v62-card .poll{margin:10px 0 4px}.v62-card .po-r{position:relative;display:flex;justify-content:space-between;align-items:center;gap:10px;border:1px solid rgba(255,255,255,.22);border-radius:12px;padding:11px 14px;margin:6px 0;overflow:hidden;font-size:15px}.v62-card .po-r i{position:absolute;left:0;top:0;bottom:0;background:'+c+';opacity:.3}.v62-card .po-r.me{border-color:'+c+'}.v62-card .po-r.me i{opacity:.5}.v62-card .po-r span{position:relative;min-width:0}.v62-card .po-r b{font-weight:900}.v62-card .pom{font-size:13px;opacity:.75;margin-top:4px}'})()+'"),
    ],
    'girrr/albo.html': [
        ("row('🔥','Serie di vittorie più lunga',se.best.t,'tra campionato e coppa',se.best.n,true)",
         "row('🔥','Serie di vittorie più lunga',se.best.t,'tra campionato e coppa',se.best.n)"),  # 6.2.1: niente oro nell'Albo (Gianluca)
    ],
    'stadio/girrr/albo.html': [
        ("row('🔥','Serie di vittorie più lunga',se.best.t,'tra campionato e coppa',se.best.n,true)",
         "row('🔥','Serie di vittorie più lunga',se.best.t,'tra campionato e coppa',se.best.n)"),
    ],
    'girrr/v60/tifosi.js': [
        # «Giurie e criteri» resta aperta quando la scheda si aggiorna da sola (ogni 15 secondi)
        ("<details><summary>Giurie e criteri</summary>",
         "<details data-pt-giurie'+(window.ptGiurieAperte?' open':'')+'><summary>Giurie e criteri</summary>"),
        # personaggi che votano durante la settimana (Gianluca, 16 novembre)
        ("<p>Le candidature considerano vittorie, risultato, trasferta e avversario. Ogni personaggio applica un criterio riconoscibile; le preferenze sono normalizzate, così il loro numero non decide da solo il premio.</p>",
         "<p>Votano la redazione e più personaggi della Curva. La redazione vota all’apertura; i personaggi arrivano uno alla volta durante la settimana, fino alla chiusura, e la classifica provvisoria si aggiorna a ogni nuovo voto.</p>'+(week.personaggi_totali&&!week.chiusa?'<p>Personaggi che hanno votato: '+(week.personaggi||[]).length+' su '+week.personaggi_totali+'.</p>':'')+'<p>Le candidature considerano vittorie, risultato, trasferta e avversario. Ogni personaggio applica un criterio riconoscibile; le preferenze sono normalizzate, così il loro numero non decide da solo il premio.</p>"),
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
    # «Giurie e criteri»: ricorda se è aperta (l'evento toggle non risale, si ascolta in cattura)
    t = (base / 'girrr/v60/tifosi.js').read_text(encoding='utf-8')
    if 'ptGiurieAperte=d.open' not in t:
        t += "\n/* 6.2.1: «Giurie e criteri» resta aperta durante gli aggiornamenti automatici */document.addEventListener('toggle',function(e){var d=e.target;if(d&&d.matches&&d.matches('[data-pt-giurie]'))window.ptGiurieAperte=d.open},true);\n"
        (base / 'girrr/v60/tifosi.js').write_text(t, encoding='utf-8')
    # Versione nell'indirizzo dei due file: senza, i telefoni tengono quelli vecchi in memoria.
    cambiate = 0
    for html in sorted(base.rglob('*.html')):
        t = html.read_text(encoding='utf-8')
        n = t.replace('v55/ui.js?v=55r10', 'v55/ui.js?v=621').replace('v55/home55.js?v=55r8', 'v55/home55.js?v=621')
        n = re.sub(r'v60/tifosi\.js(?=["\'])', 'v60/tifosi.js?v=621', n)
        n = n.replace('sondaggi62.js?v=62-nativa1', 'sondaggi62.js?v=621')
        if n != t:
            html.write_text(n, encoding='utf-8'); cambiate += 1
    if not cambiate and not any('v55/ui.js?v=621' in h.read_text(encoding='utf-8') for h in base.rglob('*.html')):
        raise SystemExit('Nessuna pagina carica v55/ui.js?v=55r10: base diversa da quella attesa')
    print('Pagine con la versione 6.2.1 dei due file:', cambiate)


if __name__ == '__main__':
    main(sys.argv[1:])
