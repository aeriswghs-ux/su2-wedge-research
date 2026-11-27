# SU2 Supersonic Wedge: Analytical Benchmark and Grid Study

> **Research question:** How accurately does the open-source solver SU2 predict idealized supersonic wedge flow, compared with analytical oblique-shock theory?

This student research starter follows the attached original `Research brief.md`.
The main verification case is **M1=2, theta=10°, gamma=1.4**, idealized
steady, 2-D, inviscid Euler flow. The scope is deliberately **supersonic**;
we do not claim that this experiment models hypersonic real-gas physics.

**State as of 2026-11-26:** the analytic solver and unit tests ran. Three
structured SU2 meshes and starter SU2 configs were generated. **No SU2 CFD
run was executed**, so numerical-simulation and mesh-convergence results
remain **NOT EXECUTED**. See `results/status.md`.

## Run the theory calculation and tests

Using Python 3.11+ from the top-level project folder:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m wedgeverify.shock --mach 2 --theta 10 --output results/analytical_M2_theta10.json
python -m wedgeverify.shock --mach 2 --theta 24
```

The second example must report `NO_ATTACHED_SOLUTION`, rather than
returning a fictitious attached shock. The main test yields approximately:

| Reference quantity | Analytical output |
| --- | ---: |
| Shock angle beta | 39.313932 degrees |
| p2/p1 | 1.706578604 |
| rho2/rho1 | 1.458425613 |
| T2/T1 | 1.170151284 |
| M2 | 1.640522229 |
| theta max | 22.973531761 degrees |

Independent printed example: https://kursatkara.github.io/MAE3293_Fundamentals_of_Aerodynamics/calculators/oblique-shock.html ; NASA theory:
https://www.grc.nasa.gov/www/BGH/oblique.html . The independent check
is limited to a published numerical example and conservation invariants;
it is not proof of a complete implementation for all inputs.

## Set up a repeatable three-mesh CFD study

```bash
python -m wedgeverify.mesh --out-dir meshes
python -m scripts.make_configs
python -m scripts.make_figures
```

All three meshes have the same geometry and a factor-of-two resolution
refinement in both directions:

| Level | nx × ny | Quadrilateral cells | h=sqrt(A/N), m |
| --- | --- | ---: | --- |
| Coarse | 60 × 40 | 2,400 | see measurements CSV |
| Medium | 120 × 80 | 9,600 | see measurements CSV |
| Fine | 240 × 160 | 38,400 | see measurements CSV |

The channel spans x=0..1.5 m and y=0..1.0 m before wedge displacement.
The 10° wedge begins at x=0.5 m and remains a lower-wall ramp to the
outlet. The mesh is **new, not the SU2 tutorial CGNS mesh**; so do not
compare our outputs directly against tutorial fields without accounting
for the geometry and mesh differences. The upper wall boundary may affect
flow farther downstream; sample only where the field is approximately
uniform and insensitive to the outlet/upper wall.

Once `SU2_CFD` is installed and functional, inspect each config and run
from the project root, saving logs and the exact solver version:

```bash
SU2_CFD cfg/wedge_coarse.cfg > results/raw/coarse.log 2>&1
SU2_CFD cfg/wedge_medium.cfg > results/raw/medium.log 2>&1
SU2_CFD cfg/wedge_fine.cfg > results/raw/fine.log 2>&1
```

**Important:** These configs have not been executed. Treat SU2 outputs
as unverified until you check boundary markers, mesh orientation, solver
convergence, gas properties, and physically plausible field contours.
The official tutorial is at https://su2code.github.io/tutorials/Inviscid_Wedge/ .

## CFD measurement protocol (to implement after first successful run)

1. Save residual histories and full field files for each mesh. Use
   convergence of pressure and shock location as well as residuals;
   a flat residual alone does not prove mesh convergence.
2. Export cell or point data from ParaView, including x,y, p, rho and Mach.
3. At multiple streamwise x stations inside 0.7–1.1 m, find the main
   shock pressure-gradient ridge; fit a line **with the tip fixed or free**
   and compare the resulting beta. Document ridge threshold and exclude
   near-tip and reflected-shock regions. Repeat with another threshold.
4. For downstream p, rho and Mach, use a stable uniform region **behind
   the main shock and above the wedge surface**, excluding the shock layer,
   outlet and boundaries. State the x/y ranges and sample counts.
5. Record the measured properties (not theory) in
   `results/measurements_template.csv`. Do not leave any values inferred
   from expected theoretical values.
6. Compute error tables with:

```bash
python -m wedgeverify.comparison --input results/measurements_template.csv --output results/mesh_errors.csv
```

Blank CFD input fields stay explicitly `NOT_EXECUTED` and yield no fake
error values. The nominal grid-size h is computed as sqrt(domain area / N).
After real CFD output, plot error vs h; no observed order will be reported
without supporting convergence data and model assumptions.

## Inlet consistency note

The official SU2 wedge config specifies an inlet velocity of
695.429076 m/s. If gamma=1.4 and T=300 K, this corresponds to a gas
constant R about 287.87 J/(kg K). In contrast, SU2's config template
shows STANDARD_AIR with R=287.058 J/(kg K), implying M=2 speed
**694.447579 m/s**. Our three configs use the latter self-consistent
choice, with an explicit R and gamma. Log actual gas settings from SU2.

## Project structure

- `wedgeverify/shock.py`: theta–beta–Mach weak-root and property jump model.
- `wedgeverify/mesh.py`: structured SU2 quadrilateral mesh generator.
- `wedgeverify/comparison.py`: measurement-only CFD/theory comparison.
- `tests/`: regression, invariants, and mesh structure tests.
- `cfg/`: generated candidate SU2 config files; not run-tested.
- `meshes/`: three generated `.su2` meshes.
- `theory/`: equations, assumptions, verification notes.
- `results/`: analytical output, status log, and empty CFD template.
- `figures/`: theory/geometry figures **not** CFD visualizations.
- `paper/`: paper draft; no fabricated CFD conclusions.
- `Research brief.md`: original user-provided project brief.

## Scientific caution

We use "verification" in the limited sense of comparing a numerical
solution to a known theoretical benchmark, not a claim of full general
SU2 code verification. A single shock test, even with grid refinement,
cannot verify all features of the solver. No physical experiments are
included, so there is no experimental validation. See `theory/verification.md`.

## Sources

- SU2 team, [Inviscid Supersonic Wedge tutorial](https://su2code.github.io/tutorials/Inviscid_Wedge/).
- NASA Glenn, [Oblique Shock Waves](https://www.grc.nasa.gov/www/BGH/oblique.html).
- Ames Research Staff (1953), [NACA Report 1135](https://digital.library.unt.edu/ark:/67531/metadc65650/).
- Christopher J. Roy (2005), *Review of code and solution verification procedures for computational simulation*, [DOI:10.1016/j.jcp.2004.10.036](https://doi.org/10.1016/j.jcp.2004.10.036).
- T. D. Economon et al. (2016), *SU2: An Open-Source Suite for Multiphysics Simulation and Design*, *AIAA Journal* 54(3), 828–846, [DOI:10.2514/1.J053813](https://doi.org/10.2514/1.J053813).
