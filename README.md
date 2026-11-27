# How well does SU2 predict a shock wave?

A high-school-friendly research project about air moving over a small ramp at **Mach 2**: twice the local speed of sound.

We compare a computer simulation with an answer calculated from established equations. We ask: **How close are the shock angle, pressure, density, and speed?**

**Status:** Three real simulations finished. The Python checks passed. These are saved computer results, not wind-tunnel measurements. The project is a supersonic benchmark, not a hypersonic experiment.

![Mach number from the actual fine-mesh simulation](figures/verified_fine_mach.png)

The red box is the main measurement area. The dashed line is the theoretical shock. The red dots show the measured shock position. See [how measurements work](docs/METHOD.md).

## New in v1.1.0

Six more CFD trials, 21 equation-only cases, five sampling areas, nine shock thresholds, and a faster shared measurement routine. Read the [expanded study](docs/EXPANDED_STUDY.md) for the data, timings and limits. The original baseline results remain unchanged.

## Start here

| What you want to do | Open this |
|---|---|
| Understand the project without coding | [Student guide](docs/STUDENT_GUIDE.md) |
| Install the tools and repeat the work | [Windows setup and reproduction](docs/SETUP.md) |
| See what was repeated before publication | [Reproducibility check](docs/REPRODUCIBILITY.md) |
| Read the results and limits | [Results explained](docs/RESULTS.md) |
| Check the exact settings and measurements | [Method](docs/METHOD.md) |
| Find the logs and data | [Data guide](docs/DATA_GUIDE.md) |
| Plan your next steps | [Next steps](docs/NEXT_STEPS.md) |
| Understand where the files came from | [File history](docs/PROVENANCE.md) |

## Download the two packages

Open the [v1.1.0 release](https://github.com/aeriswghs-ux/su2-wedge-research/releases/tag/v1.1.0).

- **SU2_Wedge_Setup_v1.1.0.zip:** current instructions, code, meshes, and settings. It also includes the recovered starter for reference. It does not include completed CFD flow files or the SU2/ParaView programs.
- **SU2_Wedge_Verified_Results_v1.1.0.zip:** everything in the setup package, plus completed runs, logs, tables, and figures.

The original starter ZIP was not found. The recovered starter came from its extracted folder. This is stated openly; we do not claim to have recovered the original ZIP byte for byte. The previously delivered verified-results ZIP was checked against all three published final flow files.

## What we found

| Quantity | Equation answer | Fine-mesh simulation | Relative error |
|---|---:|---:|---:|
| Shock angle | 39.313932° | 39.307805° | 0.015585% |
| Pressure after / before | 1.706579 | 1.706608 | 0.001730% |
| Density after / before | 1.458426 | 1.458484 | 0.004020% |
| Mach number after the shock | 1.640522 | 1.640550 | 0.001677% |

These averages come from a chosen area away from the ramp and shock. **Changing the area changes the answer.** A second area near the wall gives larger errors. We kept both sets of measurements. The result does not prove that SU2 is this accurate for every flow or everywhere in this flow.

## Quick check after setup

From the project folder, after following [SETUP.md](docs/SETUP.md):

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m wedgeverify.shock --mach 2 --theta 10
```

The original suite has 11 checks. It tests the equations and mesh code. Passing it does not replace running SU2.

## Tools and credit

The recorded simulation used Python 3.12.10, SU2 8.6.0, and ParaView 6.2.1. The Python package versions are recorded in [requirements-lock.txt](requirements-lock.txt). SU2 and ParaView are downloaded separately from their official sites.

This project used AI help to prepare code, run software, analyze results, and write documentation. It is a learning project, not a peer-reviewed paper. The student should explain and check the method before presenting it. See [sources](docs/REFERENCES.md) and [reuse notes](REUSE.md).

