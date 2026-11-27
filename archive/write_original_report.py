from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'results/verified_measurements.json').read_text())
rows=data['meshes']; theory=data['theory']
lines=['# Verified Windows execution report','', 'Run date: November 26, 2026 (America/Chicago).','',
'## Scope and provenance','',
'This is a Mach 2 supersonic, two-dimensional, steady Euler wedge benchmark with a 10-degree turn and a perfect gas (gamma 1.4). It is not a hypersonic, viscous, heat-transfer, or physical-validation study.', '',
'The connected Windows desktop was accessible. The source project and Research brief.md were inspected at `[DOWNLOADS]/su2-wedge-verification` and copied into this folder. The exact named starter ZIP was not found in the searched user directory. Therefore archive integrity and identity cannot be verified. Original source-file hashes are saved in results/raw/source_hashes.csv. No prior conversation result was treated as a new measurement.','',
'## Software and prerequisites','',
'Python 3.12.10 and all four required packages were already present; all 11 tests passed locally. Exact package versions are in results/software_versions_verified.txt. SU2 8.6.0 Windows OpenMP and ParaView 6.2.1 Windows non-MPI portable packages were downloaded from official servers and extracted under the parent tools directory. SU2 executed with OMP_NUM_THREADS=4. No MPI installation is required for these selected builds. ParaView GUI startup and pvpython version were verified; its VTK reader independently read the result files. No system PATH modification was needed.','',
'Download URLs:', '',
'- https://github.com/su2code/SU2/releases/download/v8.6.0/SU2_v8.6.0_win64-omp.zip',
'- https://www.paraview.org/files/v6.2/ParaView-6.2.1-Windows-Python3.12-msvc2017-AMD64.zip','',
'Local download SHA-256 hashes are in results/raw/download_sha256.txt. These establish local artifact identity, not independent publisher signature verification. A Windows CIM inventory query was access-denied; successful execution establishes the needed runtime availability, but does not constitute a complete system inventory.','',
'## Configuration diagnosis','',
'The starter configuration parsed and ran without a fatal configuration error. Mesh orientations were accepted. The original coarse run stopped at iteration 177 using only density residuals. Those outputs remain in results/raw/initial_coarse. A stricter trial required both density and energy below 1e-9; coarse and medium reached 4000 iterations with energy plateauing near log10 residual -8.4 and -8.7. Those attempts are preserved in results/raw/strict_attempt and their configs in results/raw/strict_configs. The final common criterion requires both fields below 1e-8. All three final runs satisfy it. A solver success exit alone is not the convergence evidence; the final convergence tables and history files are.','',
'The starter uses dimensional residuals, so absolute density and energy values cannot be compared as equivalent relative tolerances. Residual-reduction plots normalize each field by its own initial value. Nonfatal warnings about surface pressure-drop output and inactive time-convergence monitoring do not invalidate this steady run. No pressure-drop result is claimed.','',
'## Measurements','',
'Shock angle: on mesh columns between x=0.8 and 1.25 m, linearly interpolate the downward pressure crossing at half the analytical pressure jump, then fit y=a(x-0.5)+b with a free intercept. Repeat at 40% and 60% of the pressure jump for measurement sensitivity. The threshold uses the analytical pressure jump explicitly; this is not a fully theory-independent shock detector.','',
'Downstream properties: area-weighted mean of four-node cell averages for cell centers within x=0.85–1.15 m and y=0.16–0.22 m. The same physical region is used on all meshes. Its boundary includes slightly different cells at different resolutions. Raw VTU point values are float32.','',
'| Mesh | Cells | Shock angle (deg) | p2/p1 | rho2/rho1 | M2 |', '|---|---:|---:|---:|---:|---:|',
f"| Analytical | — | {theory['shock_angle_deg']:.6f} | {theory['p2_p1']:.6f} | {theory['rho2_rho1']:.6f} | {theory['mach_2']:.6f} |"]
for r in rows:
    lines.append(f"| {r['mesh']} | {r['cells']} | {r['shock_angle_deg']:.6f} | {r['p2_p1']:.6f} | {r['rho2_rho1']:.6f} | {r['mach_2']:.6f} |")
lines+=['','### Absolute relative errors (%)','','| Mesh | Shock angle | Pressure ratio | Density ratio | Downstream Mach |','|---|---:|---:|---:|---:|']
for r in rows:
    lines.append('| '+r['mesh']+' | '+' | '.join(f"{r[k+'_rel_error_pct']:.6f}" for k in ['shock_angle_deg','p2_p1','rho2_rho1','mach_2'])+' |')
lines+=['','### Convergence and conservation','','| Mesh | Last iteration (zero based) | log10 RMS density | log10 RMS energy | Boundary mass imbalance (%) | Boundary energy imbalance (%) | Regional total enthalpy error (%) |','|---|---:|---:|---:|---:|---:|---:|']
for r in rows:
    lines.append(f"| {r['mesh']} | {r['last_iteration']} | {r['final_log10_rms_density']:.4f} | {r['final_log10_rms_energy']:.4f} | {r['boundary_mass_imbalance_pct']:.6f} | {r['boundary_energy_imbalance_pct']:.6f} | {r['h0_region_mean_error_pct']:.6f} |")
lines+=['','Boundary checks use trapezoidal integration of exported nodal momentum and enthalpy flux on all four boundaries, per unit depth. They are post-processing consistency checks, not exact SU2 numerical face-flux balances. Interpolation, shock smearing and float32 export affect these estimates.','', '### Grid trend and measurement sensitivity','']
for k in ['shock_angle_deg','p2_p1','rho2_rho1','mach_2']:
    errors=[r[k+'_abs_error'] for r in rows]
    trend='decreases on each refinement' if errors[0]>errors[1]>errors[2] else 'does not decrease monotonically'
    lines.append(f'- {k}: absolute error {trend}.')
for r in rows:
    vals=[r['beta_threshold40_deg'],r['shock_angle_deg'],r['beta_threshold60_deg']]
    lines.append(f"- {r['mesh']} shock angles for 40–60% thresholds span {min(vals):.6f} to {max(vals):.6f} degrees.")
lines+=['','No formal order of accuracy or grid-independent solution is claimed. Three grids, a captured discontinuity, a fixed sampling window and threshold sensitivity are insufficient by themselves to establish asymptotic order. The unlimited second-order reconstruction produces small upstream/downstream overshoots near the shock; these are numerical artifacts, not new physical phenomena.','',
'## Evidence labels','',
'- **Verified:** executable versions, 11 passing tests, actual solver executions, saved outputs, final stopping criteria, and independent ParaView readback.',
'- **Numerically supported:** tabulated agreement with analytical shock relations for this setup and measurement method.',
'- **Preliminary:** shock-position extraction and exported-field conservation estimates; inspect sensitivity before making stronger claims.',
'- **Unresolved:** original ZIP identity, systematic domain-boundary and sampling-window sensitivity, exact numerical face-flux balances, formal convergence order, and mentor review.','',
'## Figures','',
'![Fine Mach field](../figures/verified_fine_mach.png)','',
'![Fine pressure field](../figures/verified_fine_pressure.png)','',
'![Residual reduction](../figures/verified_residuals.png)','',
'![Grid errors](../figures/verified_grid_errors.png)','',
'## Sources actually consulted','',
'- SU2, Inviscid Supersonic Wedge tutorial: https://su2code.github.io/tutorials/Inviscid_Wedge/ — Euler/HLLC setup and boundary behavior.',
'- NASA Glenn, Oblique Shock Waves: https://www.grc.nasa.gov/www/k-12/airplane/oblique.html — shock relations and conservation assumptions.',
'- SU2 downloads: https://su2code.github.io/download.html',
'- ParaView downloads: https://www.paraview.org/download/',
'- The old SU2 Windows-Installation page explicitly applies only to version 6.2.0 and lower; it was not used as current-version runtime evidence.','']
(root/'results/VERIFIED_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
print('Wrote results/VERIFIED_REPORT.md')

