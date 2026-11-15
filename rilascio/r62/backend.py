"""Prepara una copia separata del main del sito; non esegue alcun workflow."""
import argparse,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def prepara(sorgente,uscita):
    sorgente=sorgente.resolve();uscita=uscita.resolve()
    if uscita.exists() or uscita.is_relative_to(sorgente) or sorgente.is_relative_to(uscita):raise ValueError('Serve una destinazione nuova e separata')
    shutil.copytree(sorgente,uscita,ignore=shutil.ignore_patterns('.git'))
    for src,dst in [('calcoli/finestre62.py','calcoli/finestre62.py'),('rilascio/r62/server/catalogo62.py','calcoli/catalogo62.py')]:
        (uscita/dst).write_text((R/src).read_text())
    p=uscita/'calcoli/tifosi/sincronizza.py';s=p.read_text()
    s=s.replace("    result=rpc('mvp_prepara',plan)","    if tuple(map(int,version.split('.')[:2]))>=(6,2):\n        from finestre62 import scadenza\n        presente=rpc('mvp_stato',{'p_stagione':season,'p_giornata':plan['p_giornata']}).get('votazione')\n        corrente=dt.datetime.fromisoformat(presente['chiude'].replace('Z','+00:00')) if presente else None\n        limite=dt.datetime.fromisoformat(plan['p_chiude'].replace('Z','+00:00'))\n        plan['p_chiude']=scadenza('mvp',apertura=dt.datetime.now(dt.timezone.utc),inizio=limite,esistente=corrente).isoformat()\n    result=rpc('mvp_prepara',plan)")
    s=s.replace('from fatti import context,deadline','from fatti import context,deadline\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[1]))')
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
    s=s.replace('reg/voci-src/prepara_dati.py site code/calcoli/eventi.json --cronache-classifica','reg/voci-src/prepara_dati.py site code/calcoli/eventi.json --cronache-classifica --mvp-tifosi');p.write_text(s)
    print('Backend preparato soltanto nella copia',uscita)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('sorgente',type=Path);p.add_argument('uscita',type=Path);a=p.parse_args();prepara(a.sorgente,a.uscita)
