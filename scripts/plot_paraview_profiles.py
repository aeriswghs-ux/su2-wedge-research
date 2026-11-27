"""Plot ParaView-extracted values; interpolation adds samples, not mesh resolution."""
from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wedgeverify.shock import solve_weak_shock
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'paraview'
truth=solve_weak_shock(2,10);shock_y=.5*np.tan(np.deg2rad(truth.shock_angle_deg))
fig,axes=plt.subplots(1,2,figsize=(12,4.5));summary=[]
for mesh in ['coarse','medium','fine']:
    data=np.genfromtxt(OUT/f'{mesh}_profile.csv',delimiter=',',names=True)
    assert len(data)==801 and all(np.isfinite(data[n]).all() for n in data.dtype.names)
    assert np.allclose(data['x_m'],1) and np.all(np.diff(data['y_m'])>0)
    for ax,field,label,scale in [(axes[0],'pressure_pa','Pressure (kPa)',1000),(axes[1],'mach','Mach number',1)]:
        ax.plot(data['y_m'],data[field]/scale,label=mesh,lw=1.6)
        ax.set(xlim=(.32,.50),xlabel='Height y (m), at x = 1 m',ylabel=label)
        ax.axvline(shock_y,color='.5',ls=':',lw=.7)
    p=data['pressure_pa'];y=data['y_m']
    threshold=100000*(1+.5*(truth.p2_p1-1))
    ids=np.flatnonzero((p[:-1]>=threshold)&(p[1:]<threshold))
    assert len(ids)==1
    k=ids[0];cross=y[k]+(threshold-p[k])*(y[k+1]-y[k])/(p[k+1]-p[k])
    summary.append({'mesh':mesh,'samples':len(data),'half_pressure_y_m':float(cross),
                    'theoretical_y_m':float(shock_y),'location_difference_m':float(cross-shock_y)})
yy=np.array([.32,shock_y,shock_y,.50])
axes[0].plot(yy,[100*truth.p2_p1,100*truth.p2_p1,100,100],'k--',label='Ideal shock',lw=1)
axes[1].plot(yy,[truth.mach_2,truth.mach_2,2,2],'k--',label='Ideal shock',lw=1)
for ax in axes:ax.grid(alpha=.2);ax.legend(fontsize=9)
fig.suptitle('Across the shock: ParaView line samples from real SU2 fields')
fig.tight_layout();fig.savefig(OUT/'shock_profiles.png',dpi=180)
(OUT/'profile_checks.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
