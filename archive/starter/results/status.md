# Research evidence log — 2026-11-26

| Item | Status | Evidence / limitation |
| --- | --- | --- |
| Research question, scope | VERIFIED FROM BRIEF | `Research brief.md` in project root |
| Oblique-shock equations | VERIFIED AGAINST NASA GLENN | `theory/relations.md` and https://www.grc.nasa.gov/www/BGH/oblique.html |
| M=2, theta=10 numerical reference | TESTED | `pytest`; matches independent published numerical example to stated digits |
| Analytical code / edge cases | TESTED | `pytest`; actual output summarized in `results/test_results.txt` |
| Mesh generator & 3 meshes | GENERATED / STRUCTURAL TEST ONLY | `.su2` files created; SU2 mesh reader not available in the creation environment |
| SU2 solver execution | NOT EXECUTED | `SU2_CFD` not installed in creation environment |
| SU2 config syntax / runtime | UNVERIFIED | Must check with installed SU2 version |
| Residual plots | NOT EXECUTED | Need `history.csv` and solver logs |
| CFD-derived beta and property ratios | NOT EXECUTED | Template deliberately left blank |
| Mesh convergence / observed order | NOT EXECUTED | Requires three solved and converged grids |
| Conservation checks (CFD) | NOT EXECUTED | Compute boundary integrals from real CFD field data |
| Publication-quality conclusions | UNRESOLVED | Dependent on solver evidence and mentor review |

**Evidence classification:** analytical calculations have an independent numerical benchmark and physical invariant checks. No theoretical values are presented as CFD output.
