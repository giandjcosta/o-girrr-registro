#!/usr/bin/env python3
"""Prepara una COPIA locale del main del sito. Non esegue workflow né pubblica."""
import argparse
import shutil
from pathlib import Path

REGISTRO = Path(__file__).resolve().parents[2]


def prepara(copia):
    workflow = copia / '.github/workflows/dopo-giornata.yml'
    testo = workflow.read_text()
    # Il primo JSON può essere generato dal ramo di prova, prima del merge sul main.
    # Per i calcoli ordinari resta sempre il main; l'ingresso dedicato non scrive sul DB.
    checkout = '          ref: main\n          path: code'
    riferimento = "          ref: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.solo_giro_di_boa == 'true' && github.ref_name || 'main' }}\n          path: code"
    if checkout in testo:
        testo = testo.replace(checkout, riferimento)
    elif riferimento not in testo:
        raise ValueError('Il checkout del codice è cambiato: confrontarlo prima del rilascio')
    if 'code/calcoli/giro_di_boa.py' not in testo:
        dispatch = '  workflow_dispatch:\n  push:'
        if dispatch not in testo:
            raise ValueError('Gli ingressi manuali del workflow sono cambiati: confrontarli prima del rilascio')
        testo = testo.replace(dispatch, "  workflow_dispatch:\n    inputs:\n      solo_giro_di_boa:\n        description: Aggiorna solo il bilancio, senza scritture nel database\n        type: boolean\n        default: false\n  push:")
        prima = '          if [ "${{ github.event_name }}" = "push" ]; then'
        if testo.count(prima) != 1:
            raise ValueError('Il controllo della giornata è cambiato')
        testo = testo.replace(prima, '          if [ "${{ github.event.inputs.solo_giro_di_boa }}" = "true" ]; then\n            echo "esegui=false" >> "$GITHUB_OUTPUT"\n          elif [ "${{ github.event_name }}" = "push" ]; then')
        punto = '      - name: Cronache della Home 5.5 (Oggi al Girrr)'
        if testo.count(punto) != 1:
            raise ValueError('Il workflow è cambiato: confrontarlo prima di applicare il Giro di boa')
        testo = testo.replace(punto, "      - name: Giro di boa per pagina, album e Radio\n        if: github.event_name != 'push'\n        run: python3 code/calcoli/giro_di_boa.py site --leggi-pubblico\n" + punto)
        salva = "      - name: Salvo i dati del sito\n        if: steps.c.outputs.esegui == 'true' || github.event_name == 'push'"
        if testo.count(salva) != 1:
            raise ValueError('Il salvataggio del sito è cambiato')
        # Aggiorna anche gli MVP conclusi senza una nuova giornata: firma identica = nessun commit.
        testo = testo.replace(salva, '      - name: Salvo i dati del sito')
        testo = testo.replace('      - name: Salvo la coda e i post già pubblicati\n        if: always()', "      - name: Salvo la coda e i post già pubblicati\n        if: always() && github.event.inputs.solo_giro_di_boa != 'true'")
    # Le sorgenti Radio rimangono nel Registro: radio-giornata.yml le legge da lì.
    if not (copia / 'calcoli/zone_classifica.py').is_file():
        raise ValueError('Manca zone_classifica.py nel main del sito: aggiornare la copia prima del rilascio')
    for rel in ('calcoli/giro_di_boa.py',):
        target = copia / rel;target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REGISTRO / rel, target)
    workflow.write_text(testo)
    print('Server preparato nella copia locale:', copia)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('copia',type=Path);prepara(p.parse_args().copia)
