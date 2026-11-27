# What was repeated before publication

The publication check used a new Python virtual environment on the same Windows computer. This is useful evidence that the setup works, but it is not a test by a different person on a different computer.

1. Installed the recorded versions in `requirements-lock.txt` into the new environment.
2. Ran `pip check`: no broken package requirements were reported.
3. Ran the original test suite: 11 passed.
4. Used the new `run_study` command to run coarse, medium and fine meshes in a separate folder.
5. Checked that all three runs returned exit code 0 and met both final stopping criteria.
6. Regenerated the measurement tables and figures from those new runs.
7. Compared the four main measurements with the recorded reference: every absolute difference was below 0.0000001 in its reported unit or ratio.
8. Checked the relative links in the current README and docs.

See [machine-readable comparison](reproduction_check.json) and [saved rerun evidence](../results/reproduction_check/). The repeat used the same SU2 binary and four threads. It does not establish identical behavior on every operating system, CPU, SU2 build, or Python version.

## How to check your own repeat

The v1.3.0 ParaView update also regenerated the field images and extracted 801 valid, finite line samples from each baseline file. Loading the saved state recovered 2,400, 9,600 and 38,400 cells. All 18 current Python tests passed. The [ParaView guide](PARAVIEW_GUIDE.md) links the scripts, logs, source fingerprints and known rendering messages. This was checked on the same computer, using ParaView 6.2.1; another-computer verification remains open.

Save your version list and new run folder. Compare your table with `results/verified_measurements.csv`. If differences are larger than expected, first check settings, mesh files, units, software versions, stopping messages, and measurement coordinates.

Do not change your data to force a match. Report differences and investigate them.
