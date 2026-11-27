"""Build the checklist from completed trial records, never from planned counts."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'datasets/v12-checklist'
with (OUT/'trial_comparison.csv').open() as f: trials=list(csv.DictReader(f))
assert len(trials)==12 and all(r['exit_code']=='0' and r['converged']=='True' for r in trials)
reference=json.loads((ROOT/'results/verified_measurements.json').read_text())['meshes']
differences={key:max(abs(float(t[key])-next(r for r in reference if r['mesh']==t['mesh'])[key]) for t in trials)
             for key in ['shock_angle_deg','p2_p1','rho2_rho1','mach_2']}
(OUT/'repeat_differences.json').write_text(json.dumps(differences,indent=2))
with (OUT/'detector_comparison.csv').open() as f:detectors=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(8,5))
for method in ['pressure_half','gradient_midpoint','gradient_parabolic']:
    rows=[r for r in detectors if r['method']==method]
    ax.plot([r['mesh'] for r in rows],[float(r['absolute_error_deg']) for r in rows],'o-',label=method.replace('_',' '))
ax.set(yscale='log',ylabel='Absolute shock-angle error (degrees)',title='Detector choice changes the refinement trend')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'detector_errors.png',dpi=160)
lines=['# Checklist: completed work and remaining human steps','',
'Status: November 27, 2026. This records what was actually done, not just planned.','',
'- [x] Prepared plain-English explanations and a student worksheet.',
'- [x] Repeated the automated checks: 18 tests passed.',
'- [x] Completed four fresh three-mesh studies: 12 successful, converged simulations.',
'- [x] Compared all five measurement areas, including the larger errors.',
'- [x] Tested CFL 10 on coarse, medium and fine meshes, twice each, with matched CFL 5 controls.',
'- [x] Added a pressure-gradient detector and compared both midpoint and refined versions with the pressure-crossing method.',
'- [x] Prepared a research-paper draft with methods, data, sources, limits and AI disclosure.',
'- [x] Prepared a teacher/mentor review packet.',
'- [ ] Student explains the work independently, using their own words.',
'- [ ] Another person repeats the study on a different computer.',
'- [ ] A teacher or mentor reviews the paper and the student addresses their findings.','',
'The repeat runs used the same computer and software environment. They do not satisfy independent reproduction. The review packet has not been sent; no recipient was supplied and no review has occurred.','',
'## New solver results','',
'Every batch runs coarse, medium and fine meshes. The fixed CFL order was 5, 10, 10, 5. Four threads were used. Timing includes process startup and solver output writing. Two repeats per setting are not a statistical performance guarantee.','',
'| Mesh | CFL | Final iteration labels | Recorded times (seconds) |','|---|---:|---|---|']
for mesh in ['coarse','medium','fine']:
    for cfl in ['5.0','10.0']:
        rows=[r for r in trials if r['mesh']==mesh and r['cfl']==cfl]
        assert len(rows)==2
        lines.append(f"| {mesh} | {cfl} | {', '.join(r['last_iteration'] for r in rows)} | {', '.join(f'{float(r["seconds"]):.2f}' for r in rows)} |")
lines+=['','Maximum absolute change from the original reference across all 12 new runs:','']
for k,v in differences.items():lines.append(f'- {k}: {v:.10g}.')
lines+=['','CFL 10 met the convergence criteria in these cases. The baseline remains CFL 5 to keep the earlier work unchanged. This is evidence for these three meshes and settings, not a universal rule.','',
'## Measurement findings','',
'Across the five fine-mesh areas, pressure error is about 0.00153–0.00177%, density error is 0.00018–0.03002%, and Mach error is 0.00092–0.03803%. These are selected-area ranges, not confidence intervals.','',
'The parabolic gradient detector gives errors of 0.007786°, 0.002418°, and 0.004649° on coarse, medium and fine meshes. Its error is not monotonic. The raw midpoint detector is also retained; we did not discard the less accurate method.','',
'![Shock-detector errors](../datasets/v12-checklist/detector_errors.png)','',
'## Files to use next','',
'- [Research draft](../paper/research-draft.md)',
'- [Review packet and student worksheet](REVIEW_PACKET.md)',
'- [All trial records](../datasets/v12-checklist/trial_comparison.csv)',
'- [All sampling-area errors](../datasets/v12-checklist/all_box_errors.csv)',
'- [Detector comparison](../datasets/v12-checklist/detector_comparison.csv)','',
'## Repeat this checklist study','',
'Use the full results package and the environment in SETUP.md. Choose a new name:','',
'```powershell',
'.\\.venv\\Scripts\\python.exe -m scripts.checklist_trials --su2 "C:\\path\\to\\SU2\\bin\\SU2_CFD.exe" --name my-checklist',
'```','',
'This creates datasets/my-checklist and runs/my-checklist-1 through -4. Each run contains its own tables and figures. The checklist analysis/report helpers currently target the published datasets/v12-checklist folder; they regenerate its derived tables and checklist, not the raw simulations. Use a copy when experimenting with the report.','']
(ROOT/'docs/CHECKLIST.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(differences))
