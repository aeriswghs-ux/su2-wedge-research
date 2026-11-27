"""Compare every sampling area and two independently defined shock detectors."""
from pathlib import Path
import csv,json
import numpy as np
from scripts.inspect_flow import read_vtu
from scripts.expand_study import write_csv
from wedgeverify.measure import gradient_shock,pressure_crossings
from wedgeverify.shock import solve_weak_shock
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'datasets/v12-checklist'

def main():
    truth=solve_weak_shock(2,10).as_dict();rows=[]
    for mesh in ['coarse','medium','fine']:
        data=read_vtu(ROOT/f'results/raw/{mesh}_flow.vtu')
        for method,fit in [('pressure_half',pressure_crossings(data,truth['p2_p1'],[.5])[0]),
                           ('gradient_midpoint',gradient_shock(data,False)),('gradient_parabolic',gradient_shock(data))]:
            rows.append({'mesh':mesh,'method':method,'angle_deg':fit[0],'absolute_error_deg':abs(fit[0]-truth['shock_angle_deg']),
                         'intercept_m':fit[1],'points':len(fit[2])})
            np.savetxt(OUT/f'{mesh}_{method}_points.csv',fit[2],delimiter=',',header='x_m,y_m',comments='')
    write_csv(OUT/'detector_comparison.csv',rows)
    with (ROOT/'datasets/v1.1/box_sensitivity.csv').open() as f: boxes=list(csv.DictReader(f))
    for row in boxes:
        for key in ['p2_p1','rho2_rho1','mach_2']:
            row[key+'_error_pct']=100*abs(float(row[key])-truth[key])/abs(truth[key])
    write_csv(OUT/'all_box_errors.csv',boxes)
    summary={}
    for mesh in ['coarse','medium','fine']:
        summary[mesh]={}
        for key in ['p2_p1','rho2_rho1','mach_2']:
            vals=[r[key+'_error_pct'] for r in boxes if r['mesh']==mesh]
            summary[mesh][key]={'min_error_pct':min(vals),'max_error_pct':max(vals)}
    (OUT/'box_error_ranges.json').write_text(json.dumps(summary,indent=2))
    trials=[]
    for folder in sorted(OUT.glob('batch_*')):
        if not folder.is_dir():continue
        manifest=json.loads((folder/'run_manifest.json').read_text())
        measured=folder/'results/verified_measurements.json'
        measurements=json.loads(measured.read_text())['meshes'] if measured.exists() else []
        for run in manifest['runs']:
            row={'batch':folder.name,'cfl':manifest['cfl'],**run}
            for result in measurements:
                if result['mesh']==run['mesh']:
                    row.update({k:result[k] for k in ['last_iteration','shock_angle_deg','p2_p1','rho2_rho1','mach_2']})
            trials.append(row)
    write_csv(OUT/'trial_comparison.csv',trials)
    print(json.dumps({'detectors':rows,'box_ranges':summary,'recorded_trials':len(trials)},indent=2))

if __name__=='__main__':main()
