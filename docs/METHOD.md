# Exactly what we did

This page keeps the details needed to repeat the work. Use the [student guide](STUDENT_GUIDE.md) for unfamiliar terms.

## The flow and mesh

| Setting | Value |
|---|---|
| Upstream Mach number | 2.0 |
| Ramp angle | 10 degrees |
| Pressure before the shock | 100,000 Pa |
| Temperature before the shock | 300 K |
| Ratio of specific heats, gamma | 1.4 |
| Gas constant | 287.058 J/(kg K) |
| Geometry | 2D channel, 1.5 m long and 1 m high |
| Ramp start | x = 0.5 m |
| Ramp surface | y = max(x - 0.5, 0) × tan(10 degrees) |
| Meshes | 60 × 40, 120 × 80, 240 × 160 quadrilateral cells |

Mesh coordinates are in metres. The code checks cell orientation and makes the ramp corner fall on a mesh vertex. The original logs also show SU2 accepting the cell and boundary orientations.

## Boundary conditions

- **Inlet:** specified supersonic incoming air. The speed is computed from Mach number, gamma, gas constant and temperature: about 694.447579 m/s.
- **Upper and lower walls:** slip walls in an inviscid model. Air cannot pass through them, but no wall friction is modeled.
- **Outlet:** SU2's outlet condition. A low back pressure is supplied, as in the official wedge tutorial. For a supersonic exit, the flow is extrapolated from inside the domain.

The predicted shock reaches y ≈ 0.819 m at the exit, below the top wall. That geometric check does not replace a boundary-location sensitivity study.

## Numerical settings

SU2 8.6.0 solves the steady Euler equations. The configuration uses HLLC for the inviscid flux, second-order MUSCL reconstruction, no slope limiter, weighted least-squares gradients, implicit Euler stepping, CFL 5, no multigrid, and BCGSTAB with up to 10 inner linear iterations. The complete settings are in `cfg/`.

These are numerical choices, not new physical laws. The no-limiter setting can create small overshoots close to the shock. They appear in the raw fields and were not deleted.

The final stop requires density and energy RMS residuals below 10^-8, with a maximum of 4,000 iterations. Earlier attempts are preserved: the starter checked only density, while a later 10^-9 energy target reached a plateau above that target. See `results/raw/initial_coarse` and `results/raw/strict_attempt`.

## Equation answer

`wedgeverify/shock.py` solves the theta–beta–Mach relation for the weak attached shock. It finds the highest turning angle that permits an attached shock and then finds the weak root. It uses normal-shock relations for the pressure, density and temperature jumps and downstream Mach number.

The tests cover a published example, the zero-turn limit, invalid inputs, the attached-shock limit, and conservation relations. The [NASA source](REFERENCES.md) gives the underlying equations. The numerical benchmark test uses rounded values from an educational example; it is a check, not a replacement for reviewing the equations.

## Shock-angle measurement

1. Use vertical mesh columns with x between 0.8 and 1.25 m.
2. Find the downward crossing of a pressure threshold on each column.
3. Interpolate between the two points around each crossing.
4. Fit a straight line `y = a(x - 0.5) + b`, allowing `b` to be nonzero.
5. Convert the slope with `beta = arctan(a)` and report degrees.

The main threshold is halfway between upstream pressure and the theoretical downstream pressure. We also use 40% and 60% of that jump. Because the threshold uses theory, this detector is not independent of the theoretical pressure jump. A detector based only on the computed pressure gradient is a useful next check.

## Pressure, density and Mach measurements

Use cells whose centers lie in the stated rectangular region. Average the four corner values of each cell. Then average those cell values with weights proportional to cell area. Divide pressure by 100,000 Pa and density by `100000/(287.058 × 300)` kg/m³. Mach is already a ratio.

This is a consistent quadrature rule, not an exact average over the geometric rectangle. Different grids include slightly different cells along the box edges. The primary and alternate boxes are both retained.

## Conservation estimates

Integrate nodal momentum and total-enthalpy flux along the four boundaries using the trapezoidal rule and outward normals. Divide the net imbalance by the inlet magnitude. The result is per metre of depth because the model is two dimensional.

These estimates use exported float32 values. They are not SU2's internal numerical face fluxes. The CSV keeps enough digits to avoid reporting small values as exact zeros.

## Data and uncertainty

All CFD measurements come from saved VTU files. `inspect_flow.py` reads their appended raw arrays. ParaView's VTK reader independently checked point/cell counts, finite values, and field ranges. This reader check does not prove that every physical assumption or measurement choice is correct.

The study reports absolute and relative errors. It does not report a statistical confidence interval or a formal order of accuracy. A larger sensitivity study is needed before either kind of claim would be justified.
