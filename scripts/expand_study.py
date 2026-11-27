"""Create labeled theory and sensitivity datasets, then six real CFD trials."""
from pathlib import Path
import argparse, csv, hashlib, json, os, shutil, subprocess, time
import numpy as np
from scripts.inspect_flow import read_vtu
from wedgeverify.measure import pressure_crossings, cell_values, box_average
from wedgeverify.shock import solve_weak_shock, NoAttachedShock

ROOT=Path(__file__).resolve().parents[1]
BOXES={'main':(.85,1.15,.16,.22),'near_wall':(.8,1.2,.12,.20),
       'upstream_box':(.8,1.,.14,.19),'downstream_box':(1.,1.2,.20,.26),
       'higher_box':(.9,1.1,.22,.28)}

def write_csv(path, rows):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for row in rows for k in row)))
        writer.writeheader();writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--su2',required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'datasets/v1.1')
    args=parser.parse_args();exe=Path(args.su2).resolve();out=args.output.resolve()
    if not exe.is_file():parser.error('Solver executable not found')
    if out.exists():parser.error('Output already exists; choose a new folder to protect earlier work')
    out.mkdir(parents=True)
    plan={'date':'2026-11-27','theory_mach':[1.5,2.,3.], 'theory_angles_deg':[0,5,10,15,20,25,30],
          'boxes':BOXES,'pressure_thresholds':np.linspace(.3,.7,9).tolist(),
          'trial_cfl_order':[5,2,10,10,2,5],'mesh':'medium','threads':4,
          'purpose':'Measure sensitivity and repeatability; keep every trial, including failures.',
          'solver_sha256':hashlib.sha256(exe.read_bytes()).hexdigest()}
    (out/'plan.json').write_text(json.dumps(plan,indent=2))
    theory=[]
    for mach in plan['theory_mach']:
        for angle in plan['theory_angles_deg']:
            try:row=solve_weak_shock(mach,angle).as_dict()
            except NoAttachedShock:row={'mach_1':mach,'theta_deg':angle,'status':'NO_ATTACHED_SOLUTION'}
            theory.append({'data_kind':'ANALYTICAL_NOT_CFD',**row})
    write_csv(out/'theory_sweep.csv',theory)
    boxes=[];thresholds=[];truth=solve_weak_shock(2,10)
    for mesh in ['coarse','medium','fine']:
        d=read_vtu(ROOT/f'results/raw/{mesh}_flow.vtu')
        _,centers,area,fields=cell_values(d)
        for name,box in BOXES.items():
            means,count=box_average(centers,area,fields,box)
            boxes.append({'mesh':mesh,'box':name,'cells_sampled':count,'p2_p1':means['Pressure']/100000,
                          'rho2_rho1':means['Density']/(100000/(287.058*300)),'mach_2':means['Mach']})
        for fraction,fit in zip(plan['pressure_thresholds'],pressure_crossings(d,truth.p2_p1,plan['pressure_thresholds'])):
            thresholds.append({'mesh':mesh,'fraction':fraction,'shock_angle_deg':fit[0],'error_deg':abs(fit[0]-truth.shock_angle_deg)})
    write_csv(out/'box_sensitivity.csv',boxes);write_csv(out/'threshold_sensitivity.csv',thresholds)
    trials=[];env=os.environ.copy();env['OMP_NUM_THREADS']='4'
    for index,cfl in enumerate(plan['trial_cfl_order'],1):
        run=out/f'trial_{index:02d}';(run/'results/raw').mkdir(parents=True);(run/'meshes').mkdir()
        shutil.copy2(ROOT/'meshes/wedge_medium.su2',run/'meshes/wedge_medium.su2')
        cfg=(ROOT/'cfg/wedge_medium.cfg').read_text().replace('CFL_NUMBER= 5.0',f'CFL_NUMBER= {cfl}.0')
        (run/'case.cfg').write_text(cfg)
        started=time.perf_counter()
        with (run/'solver.log').open('w') as log:
            completed=subprocess.run([str(exe),'case.cfg'],cwd=run,env=env,stdout=log,stderr=subprocess.STDOUT)
        elapsed=time.perf_counter()-started
        text=(run/'solver.log').read_text(errors='replace');converged='All convergence criteria satisfied.' in text
        row={'trial':index,'cfl':cfl,'seconds':elapsed,'exit_code':completed.returncode,'converged':converged}
        if completed.returncode==0 and converged:
            d=read_vtu(run/'results/raw/medium_flow.vtu')
            _,centers,area,fields=cell_values(d);means,_=box_average(centers,area,fields,BOXES['main'])
            hist=np.genfromtxt(run/'results/raw/medium_history.csv',delimiter=',',names=True)
            row.update(last_iteration=int(hist['Inner_Iter'][-1]),shock_angle_deg=pressure_crossings(d,truth.p2_p1,[.5])[0][0],
                       p2_p1=means['Pressure']/100000,rho2_rho1=means['Density']/(100000/(287.058*300)),mach_2=means['Mach'])
        trials.append(row);write_csv(out/'cfd_trials.csv',trials)
        print(json.dumps(row),flush=True)

if __name__=='__main__':main()
