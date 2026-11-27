# SU2 configs (NOT EXECUTED)

Configs share geometry and physical/numerical options; only mesh filename and
output directories differ. These are independently authored from the official
SU2 wedge tutorial and SU2 option reference, **not** confirmed in an SU2
installation. Inspect solver warnings before relying on them. Run from the
project root with `SU2_CFD cfg/wedge_coarse.cfg` etc. Logs should be saved to
`results/raw/` without altering the input meshes; store the SU2 version.

The official tutorial config used 695.429076 m/s at a 300 K inlet. This
corresponds to R ~287.87 J/(kg K) at gamma 1.4, whereas the SU2 STANDARD_AIR
config template uses R = 287.058. Our generated configs deliberately compute
u = M sqrt(gamma*R*T) (~694.4476 m/s) to stay internally consistent. This
choice must be documented in the paper and tested after installing SU2.
