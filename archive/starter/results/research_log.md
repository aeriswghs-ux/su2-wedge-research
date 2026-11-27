# Research log — 26 November 2026

## Completed

1. Parsed the provided research brief and preserved its single question and boundaries.
2. Verified the primary analytical formulas against NASA Glenn and bibliographic details for NACA Report 1135 using UNT's archival record.
3. Verified the official SU2 tutorial's flow conditions: M1=2, p=100,000 Pa, T=300 K, 10° wedge; it is a 2D steady Euler, HLLC example.
4. Implemented an attached weak-branch analytical solver and computed a numerical reference for the benchmark case.
5. Checked numerical results against a separate published oblique-shock worked example, and tested conservation of normal mass flux and total enthalpy.
6. Generated three structured quadrilateral meshes with exact geometric refinement ratio two and candidate SU2 input configs.
7. Created theory plots, an explicit empty CFD measurement table, a comparison calculator and initial paper sections.

## Findings

- For M1=2, theta=10°, gamma=1.4: beta=39.313931845°, p2/p1=1.706578604, rho2/rho1=1.458425613, M2=1.640522229.
- Maximum attached turning angle at M1=2: theta_max=22.973531761°.
- Official SU2 test configuration inlet velocity (695.429076 m/s) corresponds to R≈287.87 J/(kg K) if gamma=1.4, T=300 K. The standard-air template specifies R=287.058, so the generated configs use 694.447579 m/s, calculated consistently from M=2 and the gas model. Confirm behavior with the installed version before using any CFD values.
- The source tutorial notes a 75×50 grid of nodes (3,626 quadrilateral elements); the research mesh series here is an independently generated geometry, not that CGNS file.

## Remaining, and what evidence will close each gap

| Step | Current status | Evidence to collect |
| --- | --- | --- |
| Install and version-check SU2_CFD | NOT EXECUTED | SU2 version, full config parse and startup log |
| Confirm mesh-reader accepts all levels | NOT EXECUTED | SU2 geometry report; no inverted cells |
| Obtain steady flow and residual convergence | NOT EXECUTED | Full logs, `*_history.csv`, stable fields |
| Check numerical conservation | NOT EXECUTED | Boundary-integrated mass and total enthalpy flux, controlled tolerances |
| Measure the 4 CFD quantities | NOT EXECUTED | Saved sampling windows, exported field values, shock fits |
| Convergence sensitivity and grid uncertainty | NOT EXECUTED | Errors on all three mesh levels, checks for asymptotic trends |
| Peer/mentor review | PENDING | Independently reviewed draft and reproducibility audit |

Do not fill pending cells from the exact theoretical solution. Residual convergence is not grid convergence; a good match on one mesh does not establish global code accuracy.
