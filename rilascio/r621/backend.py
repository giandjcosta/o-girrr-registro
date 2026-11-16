#!/usr/bin/env python3
"""6.2.1 · main del sito: undici personaggi votano l'MVP dei tifosi, ognuno con il suo criterio (Claude, 16 novembre 2026).
I sei nuovi sono personaggi della Curva. Valgono dalla votazione della 8ª giornata 2026/27: la 7ª è già aperta con
cinque personaggi e mvp_prepara non accetta di cambiare una votazione iniziata.
Uso: python3 rilascio/r621/backend.py COPIA_MAIN_SITO   (si ferma se il file non è quello atteso; rieseguibile)"""
import pathlib, sys

VECCHIO_CTX = " const giornate=rounds.map(g=>({giornata:g.n,sa:g.sa,"
NUOVO_CTX = " const giornate=rounds.map(g=>({giornata:g.n,sa:g.sa,stagione:d.stagione,"
VECCHIO = """  ['Telecronista Stanco',c=>c.gf*10+(c.away?1:0),'premia i gol della vincitrice, poi la trasferta']
 ];
 return rules.map("""
NUOVO = """  ['Telecronista Stanco',c=>c.gf*10+(c.away?1:0),'premia i gol della vincitrice, poi la trasferta'],
  /* 6.2.1 (Gianluca, 16 novembre 2026): altri personaggi della Curva, ognuno con il suo criterio, dalla 8ª giornata 2026/27 */
  ['Il Complottista',c=>-(c.gf-c.gs)*10+c.gs,'sospetta delle vittorie di misura, più sono sofferte e più ci crede'],
  ['Gufo Professionista',c=>-(c.opPos||99)*10+(c.gf-c.gs),'premia chi ha battuto l’avversaria più in alto in classifica'],
  ['Il Mago della Cabala',c=>(c.gf+c.gs)*10+c.gf,'segue i numeri: premia la partita con più gol'],
  ['Il Tassista',c=>(c.away?20:0)+(c.gf-c.gs),'premia la vittoria in trasferta, poi il margine'],
  ['Arbitro in Pensione',c=>(c.gf-c.gs)*10-c.gs,'premia il risultato più netto, poi la porta più pulita'],
  ['Klaus Pünktlich',c=>(c.away?0:20)-c.gs*2+c.gf,'premia l’ordine: vittoria in casa con pochi gol subiti']
 ];
 const tutti=!(week.stagione==='2026/27'&&week.giornata<8);   /* la 7ª, già aperta, resta con i cinque di prima */
 return (tutti?rules:rules.slice(0,5)).map("""


def main(argv):
    if len(argv) != 1:
        raise SystemExit(__doc__)
    f = pathlib.Path(argv[0]) / 'calcoli/tifosi/contesto.cjs'
    t = f.read_text(encoding='utf-8')
    for a, b in ((VECCHIO_CTX, NUOVO_CTX), (VECCHIO, NUOVO)):
        if b in t:
            continue
        if t.count(a) != 1:
            raise SystemExit('contesto.cjs diverso da quello atteso: ' + a[:60])
        t = t.replace(a, b)
    f.write_text(t, encoding='utf-8')
    print('Scritto', f)


if __name__ == '__main__':
    main(sys.argv[1:])
