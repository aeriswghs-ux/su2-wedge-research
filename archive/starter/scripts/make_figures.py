"""Theory-only figures: no simulated CFD fields or curves are included."""
from pathlib import Path
from math import asin, degrees, pi, tan, radians
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wedgeverify.shock import _turn_angle, _theta_peak, solve_weak_shock
from wedgeverify.mesh import bottom_y

ROOT = Path(__file__).resolve().parents[1]
figs = ROOT / 'figures'
figs.mkdir(exist_ok=True)

M, gamma = 2.0, 1.4
mu = asin(1/M)
peak_b, peak_theta = _theta_peak(M, gamma)
beta = np.linspace(mu, pi/2, 1000)
theta = np.array([degrees(_turn_angle(float(b), M, gamma)) for b in beta])
fig, ax=plt.subplots(figsize=(8,5))
ax.plot(np.degrees(beta[beta<=peak_b]),theta[beta<=peak_b], label='Weak attached branch')
ax.plot(np.degrees(beta[beta>=peak_b]),theta[beta>=peak_b], linestyle='--', label='Strong attached branch (context only)')
ref = solve_weak_shock(2,10)
ax.scatter([ref.shock_angle_deg],[10],marker='o',zorder=4,label=f'Test: theta=10°, beta={ref.shock_angle_deg:.3f}°')
ax.axhline(degrees(peak_theta),linestyle=':', alpha=.7, label=f'theta max={degrees(peak_theta):.3f}°')
ax.set(xlabel='Shock angle beta (degrees)', ylabel='Deflection angle theta (degrees)',title='Analytical theta–beta–Mach relation: M1=2.0, gamma=1.4')
ax.grid(alpha=.25); ax.legend(fontsize=8); fig.tight_layout()
fig.savefig(figs/'theta_beta_m2.png',dpi=180)
plt.close(fig)

fig, ax=plt.subplots(figsize=(9,5))
x=np.linspace(0,1.5,1000)
y=np.array([bottom_y(xv) for xv in x]); ax.plot(x,y,lw=2,label='Wedge/channel lower wall')
ax.plot([0,1.5],[1,1],lw=2,label='Upper wall')
ax.plot([0.5,1.5],[0,tan(radians(ref.shock_angle_deg))],linestyle='--',label='Analytical shock ray (not CFD)')
ax.axvspan(.7,1.1,alpha=.12,label='Proposed sampling x-range')
ax.set(xlabel='x (m)',ylabel='y (m)',title='Illustrative wedge domain and analytical shock location')
ax.set_aspect('equal',adjustable='box'); ax.set_xlim(0,1.5); ax.set_ylim(-0.04,1.04)
ax.grid(alpha=.2); ax.legend(loc='upper left',fontsize=8); fig.tight_layout()
fig.savefig(figs/'geometry_theory.png',dpi=180)
plt.close(fig)

fig, ax=plt.subplots(figsize=(9,5))
nx,ny=60,40
for i in range(nx+1):
    xv=1.5*i/nx
    ax.plot([xv,xv],[bottom_y(xv),1],linewidth=0.25)
for j in range(ny+1):
    frac=j/ny
    yy=np.array([bottom_y(xv)+frac*(1-bottom_y(xv)) for xv in x])
    ax.plot(x,yy,linewidth=.25)
ax.set(xlabel='x (m)',ylabel='y (m)',title='Generated coarse mesh: 60 × 40 quads, not SU2-validated')
ax.set_xlim(0,1.5); ax.set_ylim(-.02,1.02); ax.set_aspect('equal', adjustable='box'); fig.tight_layout()
fig.savefig(figs/'mesh_coarse.png',dpi=180)
plt.close(fig)
print('Generated figures (analytical or input geometry ONLY):')
for item in sorted(figs.glob('*.png')): print(' -', item.name)
