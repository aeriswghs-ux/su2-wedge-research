# Research Brief: How Accurate Is SU2 for Supersonic Wedge Flow?

Nov 26, 2026 · @John

This brief states the research question, the learning goals, the tools, the expected results, and the paper plan for one project: checking the SU2 solver against oblique-shock theory.

## Research Question

**How accurately does the open-source solver SU2 predict idealized supersonic wedge flow, when we compare it with analytical oblique-shock theory?**

This is the only research question. The project measures "accurate" with four quantities: the shock angle β, the pressure ratio p₂/p₁, the density ratio ρ₂/ρ₁, and the downstream Mach number M₂. For each quantity, we calculate the absolute error and the relative error, and we study how the error changes when the mesh gets finer.

| In scope | Out of scope |
| --- | --- |
| 2D, steady, inviscid flow (Euler equations) | Wind tunnel or other physical tests |
| Perfect gas, γ = 1.4, SI units | Viscous flow, boundary layers, real-gas effects |
| Attached, weak oblique shock | Detached shocks as CFD cases (theory only: no attached solution) |
| SU2 and exact theory | Other solvers, 3D flow, new research questions |
| Three or more systematically refined meshes | Claims of formal order of accuracy without supporting data |

## Learning Objectives

After the project, the student can do the tasks below. Core is for high school students. Extension is for undergraduates or advanced high school students.

| # | The student can… | Track | How we check it |
| --- | --- | --- | --- |
| 1 | Explain why supersonic flow makes shock waves, and why Mach number falls across an oblique shock | Core | Written answers in the report |
| 2 | Use the θ–β–M relation to find β, and say when no attached solution exists | Core | Code passes its self-checks; a case with θ > θ\_max returns "no attached solution" |
| 3 | Calculate p₂/p₁, ρ₂/ρ₁, T₂/T₁, and M₂ from β | Core | Values match a reference table or calculator |
| 4 | Describe a CFD setup: geometry, mesh, boundary conditions, solver settings | Core | Configuration file and setup notes in the repository |
| 5 | Read a residual plot, and tell solver convergence from grid convergence | Core | Residual plot with a written explanation |
| 6 | Calculate absolute and relative error between CFD and theory | Core | Error table |
| 7 | Derive the oblique-shock relations from conservation of mass, momentum, and energy | Extension | Derivation in the `theory/` folder |
| 8 | Run three or more refined meshes, and estimate the observed order only if the data supports it | Extension | Grid-convergence plot with a statement on order |
| 9 | Explain how numerical diffusion and shock capturing change the error | Extension | Discussion section of the paper |
| 10 | Label each result as verified, numerically supported, preliminary, or unresolved | Both | Audit table |
| 11 | Package the project so another person can repeat it | Both | `README.md` and `requirements.txt` that work on a clean machine |

## Uses

The wedge is a simple shape with an exact answer. This makes it a standard first test for any compressible-flow solver.

| Use | Why the wedge case helps |
| --- | --- |
| Code verification | The exact answer shows if the solver solves its equations correctly. Engineers do this before they trust a solver on a complex shape. |
| Supersonic inlet design | Ramps in an inlet slow and compress the air with oblique shocks. The same relations apply. |
| Supersonic wing and fin design | Sharp leading edges make attached oblique shocks. The shock strength sets pressure loads and wave drag. |
| Teaching compressible flow | A few equations show shocks, flow turning, and the limit θ\_max. |
| Research training | Students practice reproducible work: write code, test it, log results, and report limits. |

## Tools

All tools below are free. Record the version of each tool in `requirements.txt` and in the paper.

| Tool | What it does here | Stage |
| --- | --- | --- |
| Python 3 with NumPy and SciPy | Analytical oblique-shock code; root finding for β; error calculations | Theory, analysis |
| pytest | Automatic tests for the analytical code | Theory |
| SU2 | Open-source solver for the 2D Euler wedge case | CFD |
| SU2 Inviscid Wedge tutorial | Verified starting configuration. Read its flow conditions; do not assume them | CFD set-up |
| Gmsh or a Python mesh script | Makes the coarse, medium, and fine meshes | CFD set-up |
| ParaView | Mach and pressure contours; lines through the shock; shock-angle measurement | Post-processing |
| Matplotlib | Residual, grid-convergence, and comparison plots | Analysis |
| Git and GitHub | Version control and the public repository | All stages |
| LaTeX (for example Overleaf) or Markdown | Writes the paper | Paper |
| Reference sources | A compressible-flow textbook, NACA Report 1135 tables, and the NASA Glenn oblique-shock calculator for independent checks | Theory, audit |

## Goal and Expected Results

The goal is to answer the research question with evidence for every claim. Success means honest, checked numbers. It does not mean a perfect match with theory.

### Deliverables

| Deliverable | Form | Evidence needed |
| --- | --- | --- |
| Analytical solver | Python code and tests | Passes its self-checks; matches an independent table or calculator |
| CFD runs | SU2 configuration files, meshes, logs, history files | Raw logs saved; any run not done is marked NOT EXECUTED |
| Comparison tables | CFD against theory, one table per mesh | Absolute and relative error for β, p₂/p₁, ρ₂/ρ₁, M₂ |
| Figures | Geometry and mesh, Mach contours, pressure contours, shock-angle comparison, grid-convergence plots, error summary | Made from real data; units, labels, captions, and data source on each |
| Research paper | PDF or Markdown | See Paper Plan below |
| Repository | Folder set up as in the project plan | Another person can repeat the work from the `README.md` |
| Learning guide | The student guide in the first tab | Core and Extension tasks are clear |

### Success tests

- The analytical code passes all self-checks, and it says "no attached solution" when θ > θ\_max.
- Residuals fall and then stay flat on every mesh, and the report says what this does and does not prove.
- Mass flow and total enthalpy are checked for conservation.
- The error is reported for at least three meshes, with a plot against cell size.
- Each result has an evidence label: verified, numerically supported, preliminary, or unresolved.

### What we expect to test

These are expectations, not results. The runs must confirm or reject each one.

- The errors get smaller on finer meshes.
- The shock is thin in theory, but the solver smears it over a few cells. This affects the shock angle and the values near the shock most.
- The values in the uniform area behind the shock, away from the wedge tip and the outlet, agree best with theory.

### Results table template

The analytical column holds hand-calculated test values for M₁ = 2.0, θ = 10°, γ = 1.4. They are approximate. The CFD column stays empty until a real run exists.

| Quantity | Analytical (approximate) | CFD, fine mesh |
| --- | --- | --- |
| Shock angle β (degrees) | 39.3 | NOT EXECUTED |
| Pressure ratio p₂/p₁ | 1.707 | NOT EXECUTED |
| Density ratio ρ₂/ρ₁ | 1.459 | NOT EXECUTED |
| Mach number after shock M₂ | 1.64 | NOT EXECUTED |

After the runs, add columns for the absolute error and the relative error.

## Paper Plan

Working title: *Numerical Verification of Compressible Wedge Flow Using SU2 and Analytical Shock Relations*. The full paper is about 10 to 15 pages. The Core track writes a short report of 5 to 8 pages with the same parts, in shorter form.

| Section | What it holds | Figures and tables | Approx. length |
| --- | --- | --- | --- |
| Abstract | Question, method, main numbers, main limit | None | 150 to 250 words |
| Introduction | Why wedge-flow verification matters; the research question | Wedge and shock sketch | 1 page |
| Literature review | What the sources say. Established theory is kept apart from numerical choices | Source table | 1 page |
| Theory | Governing equations, the θ–β–M relation, the shock relations, θ\_max, assumptions | θ–β–M curve | 1 to 2 pages |
| Numerical method | Geometry, mesh, boundary conditions, solver settings, software versions | Geometry and mesh figure; settings table | 1 to 2 pages |
| Verification | Residuals, conservation checks, grid study | Residual plot; grid-convergence plot | 1 to 2 pages |
| Results | CFD against theory for each mesh; shock angle; pressure and Mach fields | Mach and pressure contours; comparison and error tables | 2 to 3 pages |
| Discussion | Why CFD and theory differ: numerical diffusion, mesh size, boundaries, measurement method | Error summary | 1 page |
| Limitations | What the project does not show | None | Half a page |
| Conclusion | The answer to the research question, with the evidence | None | Half a page |
| References | Only sources the authors read, each with title, authors, date, and DOI or URL | None | 1 page |

### How to write it

1. Write the Theory, Numerical method, and Literature review parts first. They do not need CFD results.
2. Write the Results and Discussion parts only from real, saved solver output.
3. Run the audit: state each claim, check the equations, compare with an independent source, fix errors, and give each result its evidence label.
4. Ask a mentor to read the draft and check the numbers against the repository.
5. Share the paper with the repository. Check the rules of each venue first, for example a school or university research symposium.

## Limits and Sources

### Limits

- The study is 2D, steady, and inviscid. It does not show how SU2 behaves with friction, heat transfer, or real-gas effects.
- It checks one solver on one simple flow. The result does not prove that SU2 is accurate for other flows.
- This is verification, not validation. It tests the solution of the equations, not how well the equations match real flow.
- The shock angle depends on how we measure it. The paper must state the method and test other methods.
- No SU2 run has been done for this brief. Every CFD result stays NOT EXECUTED until a real run, with a saved log, exists.

### Starting sources

These sources are from memory. They were not opened for this brief. Open each one, confirm the title, authors, date, and DOI or URL, and then cite it.

- SU2 official documentation and tutorials, including the Inviscid Wedge tutorial.
- Economon, T. D., et al. "SU2: An Open-Source Suite for Multiphysics Simulation and Design." *AIAA Journal*, 2016.
- Anderson, J. D. *Modern Compressible Flow: With Historical Perspective.* McGraw-Hill.
- Ames Research Staff. *Equations, Tables, and Charts for Compressible Flow.* NACA Report 1135, 1953.
- NASA Glenn Research Center, Beginner's Guide to Aeronautics: oblique-shock pages and calculator.
- Roache, P. J. "Verification of Codes and Calculations." *AIAA Journal*, 1998.
- Roy, C. J. "Review of Code and Solution Verification Procedures for Computational Simulation." *Journal of Computational Physics*, 2005.
