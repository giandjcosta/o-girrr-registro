"""Verifica elementi Carriera della 5.2 nel Lab e nelle due Anteprime."""
from pathlib import Path
for filename in ('lab/index.html', 'anteprima/index.html', 'anteprima/attuale.html'):
    s=Path(filename).read_text(encoding='utf8')
    expected=(
      'r="6" fill="#141d3d" stroke="#f1e8d8"',
      'id="fiducia-scala"',
      "function fiduciaColore(v)",
      'background:rgba(255,255,255,.24)',
      'aria-label="Progresso obiettivo"',
      ".ob>.pbar{grid-column:1/-1",
    )
    for check in expected:
        if check not in s:
            raise AssertionError(f'{filename}: missing {check}')
    assert "r=\"9\" fill=\"#fff\" stroke=\"#15234f\"" not in s
    print('PASS',filename)
