# Numerical Verification of Compressible Wedge Flow Using SU2 and Analytical Shock Relations

**Research stage: analytical benchmark completed; CFD NOT EXECUTED (2026-11-26).**

## Research question

How accurately does the open-source solver SU2 predict idealized supersonic
wedge flow, when compared with analytical oblique-shock theory?

## Abstract — PRELIMINARY: no CFD conclusions

This study investigates the accuracy of SU2 for idealized, steady,
two-dimensional inviscid supersonic flow over a 10-degree wedge at
upstream Mach number 2.0. The planned verification compares shock angle,
static pressure ratio, density ratio, and downstream Mach number against
analytical weak oblique-shock relations for a perfect gas with gamma=1.4.
An independent Python theory solver has been implemented and checked
against a published numerical example, with boundary cases and
conservation consistency tests. Three systematically refined structured
meshes have been created for subsequent SU2 runs. The CFD comparisons,
residual studies, conservation checks and grid-convergence conclusions
remain pending. No claim of numerical CFD accuracy is made at this stage.

## 1. Introduction

Wedge flow produces an oblique compression shock that admits an exact
ideal-gas analytical reference under appropriate attached-flow conditions.
It provides a controlled setting in which to measure how a discretized
Euler solver represents shock location and jumps in flow properties.
The project limits its claims to one idealized flow, one solver and a
three-level grid study, distinguishing solution verification from
physical validation (Roy 2005).

## 2. Literature review — VERIFIED STARTING REFERENCES

- Ames Research Staff, *Equations, Tables, and Charts for Compressible Flow*,
  NACA TR-1135 (1953). Governing analytical shock relations.
- NASA Glenn, *Oblique Shock Waves*. Accessible presentation of pressure,
  density, temperature and downstream Mach changes across an oblique shock.
- SU2 team, *Inviscid Supersonic Wedge*. Defines a tutorial case with
  M=2, 10-degree lower-wall wedge, T=300 K and p=100 kPa.
- Economon et al. (2016), *SU2: An Open-Source Suite for Multiphysics
  Simulation and Design*. General solver context (not evidence of accuracy
  for this newly generated mesh).
- Roy (2005), *Review of code and solution verification procedures for
  computational simulation*. Terminology for solution/code verification.

## 3. Theory — COMPLETE FOR ANALYTICAL BENCHMARK

Use the theta-beta-M relation, normal-shock jump relations and definition
of the downstream Mach number stated in `theory/relations.md`. The weak
root exists only for 0 <= theta <= theta_max. At M1=2.0, theta=10°,
gamma=1.4, theory gives shock angle **39.313931845°**, pressure ratio
**1.706578604**, density ratio **1.458425613**, and downstream Mach
**1.640522229**. The peak deflection is **22.973531761°**.

## 4. Numerical method — PRELIMINARY; not SU2-tested

The independent new meshes cover x in [0,1.5] m. The 10° lower-wall
ramp begins at x=0.5 m and the upper wall lies at y=1.0 m. Grid
resolutions are 60×40, 120×80 and 240×160 quadrilateral cells.
The proposed solver is SU2 Euler with HLLC flux. The boundary markers
are supersonic inlet, outlet, and upper/lower inviscid walls. The
candidate settings and their precise versions must be confirmed on a
real SU2 installation. Retain exact configs, mesh hashes and logs.

## 5. Verification — CFD NOT EXECUTED

TODO: record SU2 version, convergence histories, global and local
conservation checks and grid-refinement evidence. A residual plateau
is not by itself proof of spatial grid convergence.

## 6. Results — CFD NOT EXECUTED

Do not insert simulation values until original solver outputs exist.
The result table template is `results/mesh_errors.csv`.

## 7. Discussion — PENDING

Explain sources of discrepancy after inspecting real solution fields:
shock-capturing diffusion, grid spacing, gradient-based shock detection,
measurement-window sensitivity and boundary interactions.

## 8. Limitations

The study assumes steady, 2-D inviscid perfect-gas flow and investigates
a weak attached shock only. It is not an experiment, and it does not
establish accuracy for other SU2 solvers or hypersonic real-gas regimes.

## 9. Conclusion — NOT YET WRITABLE

A quantified CFD-versus-theory conclusion depends on completed runs.

## References

See source list with persistent URLs in `README.md`.
