"""Run four complete three-mesh studies in a fixed, balanced CFL order."""
from pathlib import Path
import argparse, json, subprocess, sys, shutil
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--su2',required=True)
    parser.add_argument('--name',default='v12-checklist')
    args=parser.parse_args()
    if not args.name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.name):
        parser.error('Use letters, numbers, hyphens or underscores for the name')
    exe=Path(args.su2).resolve()
    if not exe.is_file():parser.error('SU2 executable not found')
    out=ROOT/'datasets'/args.name
    if out.exists() or any((ROOT/'runs'/f'{args.name}-{i}').exists() for i in range(1,5)):
        parser.error('Study already exists. Use a new name.')
    out.mkdir(parents=True)
    plan={'cfl_order':[5,10,10,5],'meshes':['coarse','medium','fine'],'threads':4,
          'purpose':'Fresh full repeats and matched CFL controls; preserve all attempts; do not change baseline defaults.'}
    (out/'plan.json').write_text(json.dumps(plan,indent=2))
    statuses=[]
    for i,cfl in enumerate(plan['cfl_order'],1):
        name=f'{args.name}-{i}'
        with (out/f'batch_{i}.log').open('w') as log:
            result=subprocess.run([sys.executable,'-m','scripts.run_study','--su2',str(exe),'--name',name,'--cfl',str(cfl)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
        shutil.copytree(ROOT/'runs'/name,out/f'batch_{i}')
        statuses.append({'batch':i,'cfl':cfl,'exit_code':result.returncode})
        (out/'status.json').write_text(json.dumps(statuses,indent=2))
        print(statuses[-1],flush=True)

if __name__=='__main__':main()
