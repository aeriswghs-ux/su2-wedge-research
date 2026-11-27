"""Build the two downloadable ZIPs and their file fingerprints."""
from pathlib import Path
import hashlib
import zipfile

ROOT=Path(__file__).resolve().parents[1]
VERSION='1.3.0'
DIST=ROOT/'dist'
DIST.mkdir(exist_ok=True)
EXCLUDED={'.git','.venv','__pycache__','.pytest_cache','dist','runs','tools'}
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(part in EXCLUDED for part in p.relative_to(ROOT).parts) and p.suffix!='.pyc')
for label in ['Setup','Verified_Results']:
    selected=[p for p in files if label=='Verified_Results' or not p.relative_to(ROOT).as_posix().startswith(('results/raw/', 'datasets/v1.1/trial_', 'datasets/v12-checklist/batch_'))]
    name=f'SU2_Wedge_{label}_v{VERSION}.zip'
    hashes=[]
    with zipfile.ZipFile(DIST/name,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in selected:
            relative=p.relative_to(ROOT).as_posix()
            payload=p.read_bytes()
            hashes.append(hashlib.sha256(payload).hexdigest()+'  '+relative)
            info=zipfile.ZipInfo('su2-wedge-research/'+relative,date_time=(2026,11,27,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,payload)
        info=zipfile.ZipInfo('su2-wedge-research/MANIFEST.sha256',date_time=(2026,11,27,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,'\n'.join(hashes)+'\n')
    print(name,(DIST/name).stat().st_size,'bytes')
(DIST/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(DIST.glob(f'*v{VERSION}.zip'))))




