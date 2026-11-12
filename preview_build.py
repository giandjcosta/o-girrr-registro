from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
out=R/'.preview-site'
out.mkdir(exist_ok=True)
for path in ['lab/prova-tifosi','anteprima/pubblicata']:
 shutil.copytree(R/path,out/path,dirs_exist_ok=True)
shutil.copy2(R/'anteprima/sola-lettura.js',out/'anteprima/sola-lettura.js')
(out/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=lab/prova-tifosi/">')
print(out)
