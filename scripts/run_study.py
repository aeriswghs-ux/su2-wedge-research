"""Run SU2 in a new folder, keeping the published results safe."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--su2',required=True,help='Full path to SU2_CFD.exe')
    parser.add_argument('--name',required=True,help='A new folder name, for example my-first-run')
    parser.add_argument('--threads',type=int,default=4)
    args=parser.parse_args()
    if not args.name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.name):
        parser.error('Use only letters, numbers, hyphens and underscores in the run name.')
    if args.threads<1: parser.error('Threads must be at least 1.')
    executable=Path(args.su2).resolve()
    if not executable.is_file(): parser.error('SU2_CFD.exe was not found at that path.')
    root=Path(__file__).resolve().parents[1]
    run=root/'runs'/args.name
    if run.exists(): parser.error('That run already exists. Choose a new name to protect its files.')
    (run/'results/raw').mkdir(parents=True)
    for folder in ['cfg','meshes']: shutil.copytree(root/folder,run/folder)
    manifest={'started_utc':datetime.now(timezone.utc).isoformat(),'threads':args.threads,
              'solver_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),
              'python':sys.version,'runs':[]}
    env=os.environ.copy();env['OMP_NUM_THREADS']=str(args.threads)
    for level in ['coarse','medium','fine']:
        command=[str(executable),f'cfg/wedge_{level}.cfg']
        print(f'Running {level}. Log: runs/{args.name}/results/raw/{level}.log',flush=True)
        with (run/f'results/raw/{level}.log').open('w',encoding='utf-8') as log:
            result=subprocess.run(command,cwd=run,env=env,stdout=log,stderr=subprocess.STDOUT)
        (run/f'results/raw/{level}.exitcode').write_text(str(result.returncode)+'\n')
        text=(run/f'results/raw/{level}.log').read_text(errors='replace')
        converged='All convergence criteria satisfied.' in text
        manifest['runs'].append({'mesh':level,'exit_code':result.returncode,'converged':converged})
        (run/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        if result.returncode!=0 or not converged:
            raise SystemExit(f'{level} did not meet the checks. Read its log before continuing.')
    subprocess.run([sys.executable,'-m','scripts.analyze_runs','--run-dir',str(run)],cwd=root,check=True)
    print(f'Done. New measurements: runs/{args.name}/results/verified_measurements.csv')

if __name__=='__main__': main()
