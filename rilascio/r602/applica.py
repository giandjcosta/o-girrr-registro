#!/usr/bin/env python3
"""6.0.2 su una copia di gh-pages che ha già la 6.0.1 (Claude, 13 novembre 2026). Richieste di Gianluca della stessa sera.

Uso: python3 rilascio/r601/applica.py COPIA && python3 rilascio/r602/applica.py COPIA
Non fa commit. Si ferma se una pagina non è quella attesa.

1. Ogni pezzo di «Condividi la giornata» si condivide anche da solo, nella sua pagina (condividi.js da rilascio/condividi/):
   - Tabellone: «Tabellone ufficiale» della giornata che stai guardando (Campionato o Champions Cup, la grafica della Curva),
     Risultati e Classifica come prima;
   - Girrr Sport › Radio: «Condividi la puntata» sotto ogni puntata; Girrr Sport › Video: «Condividi il video» sotto il video.
   Solo il file, senza testo né collegamento.
2. Nel Tabellone si sceglie la squadra, anche da ospite: «La partita», «Le ultime 5» (nuova immagine: le ultime cinque partite
   di Campionato con la forma) e il «Giro di boa» di qualsiasi squadra (dalla 17ª giornata, come prima).
"""
import os
import shutil
import sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def leggi(p):
    return open(p, encoding='utf-8').read()


def scrivi(p, t):
    open(p, 'w', encoding='utf-8').write(t)


def sost(t, a, b, rel, attese=1):
    n = t.count(a)
    if n != attese:
        sys.exit('%s: trovato %d volte «%s…»: la pagina non è quella attesa (serve la 6.0.1 già applicata).' % (rel, n, a[:70]))
    return t.replace(a, b)


def main(sito):
    shutil.copyfile(os.path.join(R, 'rilascio/condividi/condividi.js'), os.path.join(sito, 'condividi.js'))
    print('ok condividi.js')
    for nome in ('giro-di-boa.js', 'giro-di-boa.css'):
        shutil.copyfile(os.path.join(R, 'rilascio/r602', nome), os.path.join(sito, nome))
    for pre, su, voci in (('girrr/', '../', 'voci/'), ('stadio/girrr/', '../../', '../../girrr/voci/')):
        rel = pre + 'app.html'
        t = leggi(os.path.join(sito, rel))
        # condividi.js anche in app.html (prima di pillole.js)
        t = sost(t, '<script src="' + su + 'pillole.js?v=1" defer></script>',
                 '<script src="' + su + 'condividi.js?v=602" defer></script><script src="' + su + 'pillole.js?v=1" defer></script>', rel)
        t = sost(t, '</head>', '<script src="' + su + 'giro-di-boa.js?v=602" defer></script></head>', rel)
        t = sost(t, "['stag','Stagione']", "['stag','Stagione'],['boa','Giro di boa']", rel)
        # Anche gli ospiti possono leggere tutte le squadre senza autenticarsi.
        t = sost(t, "['pan','stag','ob','fid','prom','st','reg']", "['pan','stag','boa','ob','fid','prom','st','reg']", rel, attese=2)
        t = sost(t, "else if(S.ctab==='prom')", "else if(S.ctab==='boa')h+=(window.GirrrGiroDiBoa?window.GirrrGiroDiBoa(t):'');\n  else if(S.ctab==='prom')", rel)
        # Radio: «Condividi la puntata» sotto ogni puntata
        a = '<audio controls preload="none" src="' + voci + '\'+esc(x.file)+\'" style="width:100%;margin:8px 0"></audio>\''
        t = sost(t, a, a + '+\'<button type="button" class="cd-btn cd-sf" data-cd-file="' + voci + '\'+esc(x.file)+\'" '
                 'data-cd-nome="radio-girrr-\'+esc(String(x.file).replace(/^puntata-g?/,\'\'))+\'" '
                 'data-cd-tit="Radio Girrr · \'+esc(x.tag)+\'">Condividi la puntata</button>\'', rel)
        # Video: «Condividi il video» sotto il video scelto
        t = sost(t, "+' src=\"'+VB+esc(x.file)+'\"></video></div>';",
                 "+' src=\"'+VB+esc(x.file)+'\"></video>'"
                 "+'<button type=\"button\" class=\"cd-btn cd-sf\" data-cd-file=\"'+VB+esc(x.file)+'\"'+(x.img?' data-cd-img=\"'+VB+esc(x.img)+'\"':'')"
                 "+' data-cd-nome=\"o-girrr-video-'+(x.n<10?'0':'')+x.n+'.mp4\" data-cd-tit=\"Il video della '+x.n+'ª giornata\">Condividi il video</button></div>';", rel)
        scrivi(os.path.join(sito, rel), t)
        print('ok', rel)


if __name__ == '__main__':
    main(sys.argv[1])
