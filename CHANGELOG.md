# Changes

## v1.3.0

- Added native ParaView images for Mach, pressure and density, with fixed color ranges across meshes.
- Added a three-mesh pressure comparison, sampling-location picture and editable portable state.
- Extracted 801 valid line samples per mesh and compared pressure and Mach profiles with theory.
- Added plain-English instructions, source fingerprints, execution logs and a saved-state load check.
- Retained numerical overshoots and rendering messages with explanations. All 18 existing tests pass.
- Uses existing baseline flow files; no new solver runs or changes to the original measurements.

## v1.2.1

- Described the work consistently as AI- and computer-assisted numerical verification.
- Removed student explanation as a condition of the research checklist; learning exercises remain optional.
- Retained independent-review status, reproducibility limits and all numerical evidence.
- Documentation update only; no simulation results changed.

## v1.2.0

- Completed 12 fresh solver runs across all meshes, with matched CFL 5 and CFL 10 repeats.
- Added a pressure-gradient shock detector, midpoint/refined comparisons, and synthetic unit checks.
- Reported every sampling-area error and retained the non-monotonic detector result.
- Added a research-paper draft, evidence-linked checklist and an unsent teacher review packet.
- Full suite: 18 tests passed. Independent repeat and technical review remain open; learning exercises are separate from numerical verification.

## v1.1.0

- Added six converged medium-mesh CFD trials with two repeats per CFL setting.
- Added 21 labeled equation-only cases, 15 box measurements and 27 threshold fits.
- Shared and accelerated shock detection and cell averaging; the original reference measurements remain unchanged.
- Added five regression and edge-case checks (16 tests in the full package).
- Published timing samples and a plain-English expanded-study guide.
- Kept v1.0.0 available as the original research release.

## v1.0.0

- Published the recovered setup material and three actual SU2 runs.
- Added plain-English setup, student, results, methods and next-steps guides.
- Added a runner that protects the reference results by using new folders.
- Included the original attempts, raw logs, flow fields and both measurement boxes.
- Recorded software versions and file fingerprints.
- Removed personal computer paths from public text copies.

This is the first public research release. It is not a claim of peer review or physical validation.
