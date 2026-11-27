# Repeat the project on Windows

You can read the results without installing anything. To repeat the calculations, install Python. To run new simulations, also download SU2. ParaView is optional unless you want to explore the flow interactively.

## 1. Get the project

Download a ZIP from the [release page](https://github.com/aeriswghs-ux/su2-wedge-research/releases/tag/v1.2.0), then choose **Extract All** in File Explorer. The results ZIP is best for repeating the analysis. Keep the extracted project in a short path, such as a folder called `wedge` inside your Documents folder.

Open PowerShell in the extracted project folder. You should see `README.md`, `scripts`, and `meshes` there.

## 2. Prepare Python

The recorded run used Python 3.12.10. Use [Python's official downloads](https://www.python.org/downloads/) for installation. Check it first:

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pytest -q
```

The `.venv` folder holds this project's Python packages. You do not need to activate it or change PowerShell's security settings. The lock file requests recorded package versions. If installation fails, save the error; do not quietly substitute versions and call it the same environment. `requirements.txt` lists wider supported version ranges for experimentation, but those are not an exact reproduction.

## 3. Calculate the equation answer

```powershell
.\.venv\Scripts\python.exe -m wedgeverify.shock --mach 2 --theta 10
.\.venv\Scripts\python.exe -m wedgeverify.shock --mach 2 --theta 30
```

The first command should give a shock angle close to 39.313932 degrees. The second should report `NO_ATTACHED_SOLUTION`: at Mach 2, a 30-degree turn is too large for the attached-shock model used here.

## 4. Get SU2

Download the [official SU2 8.6.0 Windows OpenMP ZIP](https://github.com/su2code/SU2/releases/download/v8.6.0/SU2_v8.6.0_win64-omp.zip). Extract it. Find `bin/SU2_CFD.exe` inside it. This build does not require MPI. Do not add SU2 to your system PATH just for this project; the next command accepts its full location.

The download used for the original run had SHA-256:

```text
4bc28b656def415b4d22c8274af2473dd719aa5ebfa6bc1c95c08b1bac26508c
```

A SHA-256 hash is a file fingerprint. Compare your downloaded ZIP with `Get-FileHash -Algorithm SHA256` if you want to confirm it is the same package. This is a recorded local hash, not a publisher's digital signature.

## 5. Run all three meshes

Replace the example path with your actual `SU2_CFD.exe` location:

```powershell
.\.venv\Scripts\python.exe -m scripts.run_study --su2 "C:\path\to\SU2\bin\SU2_CFD.exe" --name my-first-run
```

The script uses four threads, runs coarse then medium then fine, and checks each exit code and convergence message. It stops if a run fails. It creates `runs/my-first-run` and refuses to reuse an existing folder. It does not overwrite the published reference data.

When it finishes, open `runs/my-first-run/results/verified_measurements.csv` and `runs/my-first-run/figures`. Expect small differences across machines or software builds. Compare numbers and trends; do not demand identical file hashes for a new simulation.

## 6. Repeat only the analysis

With the verified-results ZIP or the full repository:

```powershell
.\.venv\Scripts\python.exe -m scripts.analyze_runs
```

This uses the saved reference flow fields. It regenerates the derived CSV, JSON and figures, but does not rerun SU2. It overwrites those derived files, so keep a copy if you edited them. It does not change the raw flow files.

For your new run:

```powershell
.\.venv\Scripts\python.exe -m scripts.analyze_runs --run-dir runs/my-first-run
```

## 7. View the shock in ParaView

Get [ParaView from its official site](https://www.paraview.org/download/). The recorded run used the non-MPI Windows 6.2.1 portable ZIP. Extract it into a short path and open `bin/paraview.exe`.

1. Choose **File → Open**.
2. Open `results/raw/fine_flow.vtu` from this project, or the same file inside your new run folder.
3. Click **Apply**.
4. Choose `Mach` in the coloring menu. Then try `Pressure` and `Density`.
5. Use **Reset Camera** if the field is not visible.

To repeat the independent file-reader check with ParaView's Python:

```powershell
& "C:\path\to\ParaView\bin\pvpython.exe" scripts/verify_with_paraview.py
```

This checks the reference files. It is optional and is separate from the ordinary Python setup.

## If something fails

| Message or problem | What to do |
|---|---|
| `py` not found | Install Python, then open a new PowerShell window. |
| A package will not install | Save the full message and check that you chose Python 3.12. |
| SU2 file not found | Point to the actual executable, not the ZIP or its folder. |
| Missing DLL | Save the exact DLL name; use official runtime instructions. Do not download random DLL files. |
| Run name already exists | Pick a new name to keep the earlier result. |
| Solver did not converge | Read the log under that run's `results/raw`. Do not label it converged because the program exited. |
| No flow file for analysis | Use the results package or complete the simulations first. |

For a useful help request, include your versions, the command, and the relevant run log. Remove private file paths before posting it publicly.


