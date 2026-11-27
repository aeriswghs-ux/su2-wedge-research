# Where to find each piece of evidence

| Location | What it contains |
|---|---|
| `cfg/` | Final SU2 settings for each mesh. |
| `meshes/` | The three meshes actually used. |
| `wedgeverify/` | Equation solver, mesh generator, and comparison helpers. |
| `tests/` | The original 11 automated checks. |
| `scripts/run_study.py` | Runs new simulations in a separate folder. |
| `scripts/analyze_runs.py` | Reads flow fields and creates tables and figures. |
| `results/raw/coarse.log`, `medium.log`, `fine.log` | Complete final solver messages. |
| `results/raw/*_history.csv` | Residuals at each iteration. |
| `results/raw/*_flow.vtu` | Saved full flow fields. Open these in ParaView. |
| `results/raw/*_surface.vtu` | Saved lower-wall surface results. |
| `results/raw/*_restart.dat` | SU2 binary restart data. |
| `results/raw/*.exitcode` | Program exit status; zero means success, not automatically convergence. |
| `results/raw/initial_coarse/` | Original density-only stopping attempt. |
| `results/raw/strict_attempt/` | Earlier coarse and medium attempts with the stricter energy target. |
| `results/raw/strict_configs/` | Snapshots taken during the strict-target investigation; each run log is the authority for the settings actually loaded. |
| `results/verified_measurements.csv` | Main results, errors, alternate box values and conservation estimates. |
| `results/verified_measurements.json` | The same results plus theoretical values and boundary flux details. |
| `results/*_shock_points.csv` | Measured shock locations used in the line fit. |
| `results/paraview_readback.json` | Independent VTK-reader counts and field ranges. |
| `figures/verified_*.png` | Figures made from the saved runs. |
| `archive/starter/` | Recovered starting project, before this session's SU2 runs. |
| `runs/` | Your new runs; created locally and excluded from Git by default. |

## Reading the CSV

`shock_angle_deg`, `p2_p1`, `rho2_rho1`, and `mach_2` are the main results. Columns ending in `_abs_error` are absolute differences from theory. Columns ending in `_rel_error_pct` are percentage differences. `alternate_region_*` stores values from the second measurement box.

`h_m` is the square root of total mesh area divided by cell count. It is a representative cell size, not the width of every cell. `region_cells` tells you how many cells were used in the main average.

`boundary_mass_imbalance_pct` and `boundary_energy_imbalance_pct` are estimates from exported values. A value such as `9.14e-08` means 0.0000000914, not zero.

## Keep originals and new experiments separate

Do not edit the reference flow files to improve agreement. Run new cases under a new name, record exactly what you changed, and compare both results. Keep failed or non-converged attempts with honest labels.

The public text files replace personal machine paths with labels such as `[WORKSPACE]`. Solver numbers and binary flow data were not changed for that purpose. See [file history](PROVENANCE.md).
