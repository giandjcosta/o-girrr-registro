"""Prepara una copia separata del main del sito; non esegue alcun workflow."""
import argparse,difflib,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def sost(s,a,b):
    if s.count(a)!=1:raise ValueError('Automazione diversa dalla base attesa: '+a[:90])
    return s.replace(a,b)
def prepara(sorgente,uscita):
    sorgente=sorgente.resolve();uscita=uscita.resolve()
    if uscita.exists() or uscita.is_relative_to(sorgente) or sorgente.is_relative_to(uscita):raise ValueError('Serve una destinazione nuova e separata')
    shutil.copytree(sorgente,uscita,ignore=shutil.ignore_patterns('.git'))
    for src,dst in [('calcoli/finestre62.py','calcoli/finestre62.py'),('rilascio/r62/server/catalogo62.py','calcoli/catalogo62.py'),('rilascio/r62/server/giuria62.py','calcoli/giuria62.py')]:
        (uscita/dst).write_text((R/src).read_text())

    # Verdetto MVP nella Curva: le sorgenti del Registro aggiungono soltanto
    # funzionalità 6.2. Se il main del sito è cambiato, NON sovrascriverlo.
    for rel in ('calcoli/leggi_eventi.py','calcoli/post_curva.py'):
        corrente=(sorgente/rel).read_text(encoding='utf-8')
        aggiornato=(R/rel).read_text(encoding='utf-8')
        controllo=corrente
        if rel.endswith('leggi_eventi.py'):
            sostituzioni=(
              ('    cal = calendario_lega() if (conf or dopo) else None',
               '    cal = calendario_lega() if (conf or dopo or mvp) else None'),
              ('    ev = eventi(rpc("derby_stato", {}), prom) + eventi_conferenza(conf, cal) + eventi_dopo(dopo, cal)',
               '    ev = eventi(rpc("derby_stato", {}), prom) + eventi_conferenza(conf, cal) + eventi_dopo(dopo, cal) + eventi_mvp(mvp, cal)'),
            )
            for prima,dopo in sostituzioni:
                if controllo.count(prima)!=1:raise ValueError('La base del sito è cambiata: '+rel)
                controllo=controllo.replace(prima,dopo)
        differenze=difflib.SequenceMatcher(None,controllo.splitlines(),aggiornato.splitlines(),autojunk=False).get_opcodes()
        if any(op not in ('equal','insert') for op,*_ in differenze):
            raise ValueError('Il sito contiene modifiche non presenti nel Registro: '+rel)
        (uscita/rel).write_text(aggiornato,encoding='utf-8')
    p=uscita/'calcoli/tifosi/sincronizza.py';s=p.read_text()
    s=sost(s,"    result=rpc('mvp_prepara',plan)","    if tuple(map(int,version.split('.')[:2]))>=(6,2):\n        from finestre62 import scadenza\n        presente=rpc('mvp_stato',{'p_stagione':season,'p_giornata':plan['p_giornata']}).get('votazione')\n        corrente=dt.datetime.fromisoformat(presente['chiude'].replace('Z','+00:00')) if presente else None\n        limite=dt.datetime.fromisoformat(plan['p_chiude'].replace('Z','+00:00'))\n        plan['p_chiude']=scadenza('mvp',apertura=dt.datetime.now(dt.timezone.utc),inizio=limite,esistente=corrente).isoformat()\n    result=rpc('mvp_prepara',plan)")
    s=sost(s,'from fatti import context,deadline','from fatti import context,deadline\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[1]))')
    p.write_text(s)
    p=uscita/'.github/workflows/tifosi-giornata.yml';s=p.read_text().replace('  contents: read','  contents: write').replace('          persist-credentials: false','          persist-credentials: true')
    s+='''\n      - name: Catalogo e dossier 6.2 nel giro ordinario, senza audio
        env:
          SUPABASE_SECRET_KEY: ${{ secrets.SUPABASE_SECRET_KEY }}
          SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
        run: |
          python3 code/calcoli/catalogo62.py site --vai
          cd site
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          if [ -f girrr/dati/mvp-editoriale.json ]; then
            git add girrr/dati/mvp-editoriale.json
            if ! git diff --cached --quiet; then
              git commit -m "Aggiorna il dossier MVP per i canali ordinari"
              git pull --rebase origin gh-pages
              git push origin gh-pages
            fi
          fi
''';p.write_text(s)
    p=uscita/'.github/workflows/radio-giornata.yml';s=p.read_text()
    # Il flag opera solo nella normale preparazione: restano archivio, cadenza e guardie esistenti.
    if s.count('reg/voci-src/prepara_dati.py site code/calcoli/eventi.json --cronache-classifica')!=2:raise ValueError('Ingressi Radio diversi dalla base attesa')
    s=s.replace('reg/voci-src/prepara_dati.py site code/calcoli/eventi.json --cronache-classifica','reg/voci-src/prepara_dati.py site code/calcoli/eventi.json --cronache-classifica --mvp-tifosi');p.write_text(s)
    print('Backend preparato soltanto nella copia',uscita)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('sorgente',type=Path);p.add_argument('uscita',type=Path);a=p.parse_args();prepara(a.sorgente,a.uscita)
