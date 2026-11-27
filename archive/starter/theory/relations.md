# Ideal attached oblique shock: exact theoretical relations

For upstream Mach number M1 > 1, wedge deflection theta, gas ratio gamma > 1,
let beta be the shock angle, and mu = asin(1/M1) the Mach angle.

The **theta–beta–Mach relation** is

\[\tan\theta = 2\cot\beta\;\frac{M_1^2\sin^2\beta-1}{M_1^2(\gamma+\cos 2\beta)+2}.\]

For fixed M1 and gamma, theta(beta) rises from zero at beta=mu to a
maximum, theta_max, and then falls to zero at beta=90 degrees. The weak
attached branch has beta between mu and the maximizing beta; find its root
with Brent's method. If theta > theta_max, report **NO_ATTACHED_SOLUTION**;
this study does not model a detached bow shock.

Define normal Mach number \(M_{n1}=M_1\sin\beta\). Across the shock,

\[\frac{p_2}{p_1}=1+\frac{2\gamma}{\gamma+1}(M_{n1}^2-1).\]
\[\frac{\rho_2}{\rho_1}=\frac{(\gamma+1)M_{n1}^2}{(\gamma-1)M_{n1}^2+2}.\]
\[\frac{T_2}{T_1}=\frac{p_2/p_1}{\rho_2/\rho_1}.\]
\[M_{n2}^2=\frac{1+(\gamma-1)M_{n1}^2/2}{\gamma M_{n1}^2-(\gamma-1)/2}.\]
\[M_2=\frac{M_{n2}}{\sin(\beta-\theta)}.\]

The shock discontinuity conserves mass and total enthalpy:
\(\rho_1 u_{n1}=\rho_2 u_{n2}\) and
\(T_1[1+(\gamma-1)M_1^2/2]=T_2[1+(\gamma-1)M_2^2/2]\).
These are tested independently of root convergence. Total *pressure* is
not conserved.

**Scope:** 2-D, steady, inviscid ideal gas with constant gamma=1.4.
The wedge case is supersonic at Mach 2; no high-temperature hypersonic
real-gas physics is implied.

Primary sources: NASA Glenn, Oblique Shock Waves
https://www.grc.nasa.gov/www/BGH/oblique.html ; Ames Research Staff,
*Equations, Tables, and Charts for Compressible Flow* (1953), NACA Report 1135:
https://digital.library.unt.edu/ark:/67531/metadc65650/ .
