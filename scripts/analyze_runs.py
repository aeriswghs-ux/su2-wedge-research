"""Reproducible measurements from actual SU2 fields; no synthetic CFD data."""
from pathlib import Path
import json, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scripts.inspect_flow import read_vtu
from wedgeverify.measure import pressure_crossings, cell_values, box_average
from wedgeverify.shock import solve_weak_shock

import argparse
parser=argparse.ArgumentParser(description="Measure real SU2 results and draw the figures.")
parser.add_argument('--run-dir', type=Path, help="Folder containing results/raw from a new run")
args=parser.parse_args()
ROOT=args.run_dir.resolve() if args.run_dir else Path(__file__).resolve().parents[1]
RAW=ROOT/'results/raw'
OUT=ROOT/'results'
FIG=ROOT/'figures'
FIG.mkdir(parents=True,exist_ok=True)
theory=solve_weak_shock(2,10).as_dict()
rho1=100000/(287.058*300)
rows=[]
figres, axres=plt.subplots(figsize=(8,5))

for level in ['coarse','medium','fine']:
    d=read_vtu(RAW/f'{level}_flow.vtu')
    xy=d['Points'][:,:2].astype(float)
    cells=d['connectivity'].reshape(-1,4)
    poly, centers, area, fields = cell_values(d)
    means, region_count = box_average(centers, area, fields, (.85, 1.15, .16, .22))
    region=(centers[:,0]>=.85)&(centers[:,0]<=1.15)&(centers[:,1]>=.16)&(centers[:,1]<=.22)
    fit40, (beta, intercept, points), fit60 = pressure_crossings(d, theory['p2_p1'])
    row={'mesh':level,'cells':len(cells),'h_m':float(np.sqrt(area.sum()/len(cells))),
         'shock_angle_deg':beta,'p2_p1':means['Pressure']/100000,'rho2_rho1':means['Density']/rho1,'mach_2':means['Mach'],
         'shock_intercept_m':intercept,'beta_threshold40_deg':fit40[0],'beta_threshold60_deg':fit60[0],
         'region_cells':int(region.sum())}
    for key in ['shock_angle_deg','p2_p1','rho2_rho1','mach_2']:
        row[key+'_abs_error']=abs(row[key]-theory[key])
        row[key+'_rel_error_pct']=100*abs(row[key]-theory[key])/abs(theory[key])
    alternate, _ = box_average(centers, area, fields, (.8, 1.2, .12, .20))
    for field,key,scale in [('Pressure','p2_p1',100000),('Density','rho2_rho1',rho1),('Mach','mach_2',1)]:
        row['alternate_region_'+key] = alternate[field]/scale
    x,y=xy.T
    # Boundary trapezoidal quadrature on exported nodal fields (not solver face fluxes).
    rho=d['Density'].astype(float); mom=d['Momentum'].astype(float)
    h0=(d['Energy'].astype(float)+d['Pressure'])/rho
    fluxes={}; hfluxes={}
    boundary_ids={
       'inlet':np.flatnonzero(np.isclose(x,0)),
       'outlet':np.flatnonzero(np.isclose(x,1.5)),
       'upper':np.flatnonzero(np.isclose(y,1)),
       'lower':np.flatnonzero(np.isclose(y,np.maximum(x-.5,0)*np.tan(np.deg2rad(10)),atol=1e-7))}
    for name,ids in boundary_ids.items():
        ids=ids[np.argsort(y[ids] if name in ['inlet','outlet'] else x[ids])]
        a,b=ids[:-1],ids[1:]
        tangent=xy[b]-xy[a]
        normal=np.column_stack((tangent[:,1],-tangent[:,0]))
        if name in ['inlet','upper']: normal=-normal
        fluxes[name]=float(np.sum(.5*(mom[a,:2]+mom[b,:2])*normal))
        hfluxes[name]=float(np.sum(.5*(mom[a,:2]*h0[a,None]+mom[b,:2]*h0[b,None])*normal))
    row['boundary_mass_imbalance_pct']=100*abs(sum(fluxes.values()))/abs(fluxes['inlet'])
    row['boundary_energy_imbalance_pct']=100*abs(sum(hfluxes.values()))/abs(hfluxes['inlet'])
    row['h0_region_mean_error_pct']=100*abs(float(np.average(h0[cells].mean(axis=1)[region],weights=area[region]))/(1.4/.4*287.058*300+.5*(2*np.sqrt(1.4*287.058*300))**2)-1)
    row['mass_flux_kg_s_per_m']=fluxes
    row['pressure_min_pa']=float(d['Pressure'].min())
    row['mach_min']=float(d['Mach'].min())
    hist=np.genfromtxt(RAW/f'{level}_history.csv',delimiter=',',names=True)
    row['last_iteration']=int(hist['Inner_Iter'][-1])
    row['final_log10_rms_density']=float(hist['rmsRho'][-1])
    row['final_log10_rms_energy']=float(hist['rmsRhoE'][-1])
    row['density_residual_drop_orders']=float(hist['rmsRho'][0]-hist['rmsRho'][-1])
    row['energy_residual_drop_orders']=float(hist['rmsRhoE'][0]-hist['rmsRhoE'][-1])
    axres.plot(hist['Inner_Iter'],hist['rmsRho']-hist['rmsRho'][0],label=level+' density')
    axres.plot(hist['Inner_Iter'],hist['rmsRhoE']-hist['rmsRhoE'][0],ls='--',label=level+' energy')
    rows.append(row)
    np.savetxt(OUT/f'{level}_shock_points.csv',points,delimiter=',',header='x_m,y_m',comments='')
    if level=='fine':
        for field,label in [('Mach','Mach number'),('Pressure','Pressure (Pa)')]:
            fig,ax=plt.subplots(figsize=(10,5))
            collection=PolyCollection(poly,array=fields[field],cmap='viridis',edgecolors='none',antialiased=False)
            ax.add_collection(collection); ax.autoscale(); ax.set_aspect('equal')
            xx=np.array([.5,1.5]); ax.plot(xx,(xx-.5)*np.tan(np.deg2rad(theory['shock_angle_deg'])),'w--',lw=1,label='Analytical shock')
            ax.plot(points[:,0],points[:,1],'r.',ms=2,label='Measured half-pressure crossing')
            ax.add_patch(plt.Rectangle((.85,.16),.3,.06,fill=False,edgecolor='red',lw=1))
            ax.set(xlabel='x (m)',ylabel='y (m)',title=f'SU2 8.6.0 — fine mesh ({len(cells):,} cells)')
            ax.legend(fontsize=8,loc='upper left'); fig.colorbar(collection,ax=ax,label=label)
            fig.tight_layout(); fig.savefig(FIG/f'verified_fine_{field.lower()}.png',dpi=180); plt.close(fig)

axres.set(xlabel='Iteration',ylabel='log10 residual / initial residual',title='Actual SU2 residual reduction')
axres.legend(ncol=2,fontsize=8); axres.grid(alpha=.2); figres.tight_layout(); figres.savefig(FIG/'verified_residuals.png',dpi=180)
(OUT/'verified_measurements.json').write_text(json.dumps({'theory':theory,'meshes':rows},indent=2))
flat=[{k:v for k,v in r.items() if not isinstance(v,dict)} for r in rows]
with (OUT/'verified_measurements.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=flat[0].keys()); writer.writeheader(); writer.writerows(flat)
fig,axes=plt.subplots(2,2,figsize=(9,7))
for ax,key in zip(axes.flat,['shock_angle_deg','p2_p1','rho2_rho1','mach_2']):
    ax.loglog([r['h_m'] for r in rows],[r[key+'_rel_error_pct'] for r in rows],'o-')
    ax.set(title=key,xlabel='Nominal cell size (m)',ylabel='Absolute relative error (%)');ax.grid(alpha=.2)
fig.suptitle('Measured errors — three SU2 meshes (no formal order claim)');fig.tight_layout();fig.savefig(FIG/'verified_grid_errors.png',dpi=180)
print(json.dumps(rows,indent=2))


