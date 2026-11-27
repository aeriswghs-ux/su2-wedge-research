# Verification versus validation

This study compares a **discrete numerical solution** (when available) to an
idealized analytical oblique-shock solution of the governing equations.
That is *solution verification / benchmarking*, not experimental validation
of the physical model and not a proof that SU2 is correct in all flows.

A formal numerical **code verification** claim generally needs stronger
assurance (e.g., manufactured solutions). Do not treat one agreement case or
one observed convergence slope as a general code verification certificate.

A shock is a discontinuity; near the shock, solution smoothness and classical
higher-order error assumptions fail. Do not infer formal global order from
three points without fit-quality and asymptotic-range checks.

Sources: Roy (2005), DOI:10.1016/j.jcp.2004.10.036; SU2 wedge tutorial.
