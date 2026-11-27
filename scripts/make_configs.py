from pathlib import Path
from math import sqrt
from wedgeverify.mesh import GRID_LEVELS

ROOT = Path(__file__).resolve().parents[1]
gamma, R, T, p, M = 1.4, 287.058, 300.0, 100000.0, 2.0
u = M*sqrt(gamma*R*T)
for level in GRID_LEVELS:
    cfg = f"""% Wedge benchmark configuration tested with SU2 8.6.0.
% Official reference: https://su2code.github.io/tutorials/Inviscid_Wedge/
% Internally consistent M=2 inlet velocity with R=287.058, gamma=1.4.
SOLVER= EULER
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
FLUID_MODEL= STANDARD_AIR
GAMMA_VALUE= {gamma}
GAS_CONSTANT= {R}
MACH_NUMBER= {M}
AOA= 0.0
FREESTREAM_PRESSURE= {p}
FREESTREAM_TEMPERATURE= {T}
MARKER_EULER= ( upper, lower )
MARKER_SUPERSONIC_INLET= ( inlet, {T}, {p}, {u:.12f}, 0.0, 0.0 )
MARKER_OUTLET= ( outlet, 10000.0 )
MARKER_PLOTTING= ( lower )
MARKER_MONITORING= ( upper, lower )
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CONV_NUM_METHOD_FLOW= HLLC
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT
CFL_NUMBER= 5.0
CFL_ADAPT= NO
ITER= 4000
LINEAR_SOLVER= BCGSTAB
LINEAR_SOLVER_ERROR= 1E-4
LINEAR_SOLVER_ITER= 10
MGLEVEL= 0
CONV_FIELD= (RMS_DENSITY, RMS_ENERGY)
CONV_RESIDUAL_MINVAL= -8
CONV_STARTITER= 10
CONV_CAUCHY_ELEMS= 100
CONV_CAUCHY_EPS= 1E-8
MESH_FILENAME= meshes/wedge_{level}.su2
MESH_FORMAT= SU2
TABULAR_FORMAT= CSV
OUTPUT_FILES= (RESTART, PARAVIEW, SURFACE_PARAVIEW)
VOLUME_OUTPUT= (COORDINATES, SOLUTION, PRIMITIVE)
HISTORY_OUTPUT= (ITER, RMS_RES)
CONV_FILENAME= results/raw/{level}_history
VOLUME_FILENAME= results/raw/{level}_flow
SURFACE_FILENAME= results/raw/{level}_surface
RESTART_FILENAME= results/raw/{level}_restart
OUTPUT_WRT_FREQ= 100
SCREEN_OUTPUT= ( INNER_ITER, RMS_DENSITY, RMS_ENERGY )
"""
    (ROOT / 'cfg' / f'wedge_{level}.cfg').write_text(cfg, encoding='utf-8')
print(f'Generated {len(GRID_LEVELS)} configs; inlet velocity {u:.12f} m/s')


