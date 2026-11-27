"""Draw a simple view of the measured sensitivity datasets."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wedgeverify.shock import solve_weak_shock

root=Path(__file__).resolve().parents[1]/'datasets/v1.1'
with (root/'threshold_sensitivity.csv').open() as f: rows=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(8,5))
for mesh in ['coarse','medium','fine']:
    selected=[r for r in rows if r['mesh']==mesh]
    ax.plot([100*float(r['fraction']) for r in selected],[float(r['shock_angle_deg']) for r in selected],'o-',label=mesh)
ax.axhline(solve_weak_shock(2,10).shock_angle_deg,color='black',ls='--',label='Equation answer')
ax.set(xlabel='Pressure threshold (% of theoretical jump)',ylabel='Measured shock angle (degrees)',title='The measurement rule changes the answer')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(root/'thresholds.png',dpi=160)
