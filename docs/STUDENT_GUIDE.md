# The idea in simple words

Imagine air moving very fast toward a ramp. The air must turn to follow the ramp. At twice the speed of sound, it cannot gently warn the air far upstream. A thin region forms where pressure, density, and temperature rise quickly. That region is a **shock wave**.

Our ramp turns the air by 10 degrees. The shock itself sits at about 39.3 degrees to the incoming flow. Those are different angles.

## Why compare two answers?

For this simple case, established equations give an answer. SU2 gives another answer by dividing the space into small pieces and solving equations on those pieces. Comparing the two helps us find mistakes and measure numerical error.

This is **verification**: checking how well the computer solves the chosen equations. **Validation** would compare the model with a real experiment. We have not done that.

## Words you will see

| Word | Meaning here |
|---|---|
| CFD | Computational fluid dynamics: using a computer to calculate flow. |
| Mach number | Flow speed divided by the local speed of sound. Mach 2 means twice that sound speed. |
| Pressure | Force per unit area. It is measured in pascals (Pa). |
| Density | Mass per unit volume, measured in kilograms per cubic metre. |
| Mesh or grid | The small pieces into which the flow area is divided. |
| Coarse / fine | Fewer, larger pieces / more, smaller pieces. |
| Residual | A measure of how much the current numerical solution still fails to balance an equation. |
| Solver convergence | The calculation settles sufficiently on one mesh. |
| Grid convergence | Results become steadier as the mesh is refined. This is a different check. |
| Inviscid | The model leaves out viscosity, so it does not model friction or a boundary layer. |
| Euler equations | Conservation equations for an inviscid fluid. |
| Perfect gas | A simplified gas model relating pressure, density and temperature. |
| Weak attached shock | The lower-strength shock solution that starts at the ramp corner. |
| Total enthalpy | An energy quantity combining thermal energy with flow speed. It should stay constant in this ideal case. |
| Reproducible | Someone else can follow the instructions and obtain comparable results. |

## Read a ratio

`p2/p1 = 1.7066` means the pressure after the shock is about 1.7066 times the pressure before it: about 70.66% higher. The `1` means before the shock; `2` means after it.

`rho2/rho1` is the same idea for density. `M2` is the Mach number after the shock.

## Calculate error

```text
absolute error = |simulation answer - equation answer|
relative error (%) = 100 × absolute error / |equation answer|
```

For the fine mesh, the shock-angle difference is about 0.00613 degrees. Divide that by 39.31393 degrees and multiply by 100 to get about 0.0156%.

Small error is useful evidence, but it does not mean every part of the flow is correct. The result also depends on where and how we measure it.

## Check your understanding

1. Why are the ramp angle and shock angle different?
2. What does a pressure ratio of 1.7066 mean?
3. Why can a simulation finish without being converged?
4. Why do we use three meshes?
5. Why is this verification rather than validation?
6. Which finding changes when the measurement box moves?

Try answering in your own words before reading the technical files.
