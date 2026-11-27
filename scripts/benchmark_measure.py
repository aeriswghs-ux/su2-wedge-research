"""Time old and shared shock measurements on the same saved fine-mesh data."""
from pathlib import Path
import json, runpy, time, statistics
import numpy as np
from scripts.inspect_flow import read_vtu
from wedgeverify.measure import pressure_crossings
from wedgeverify.shock import solve_weak_shock

ROOT=Path(__file__).resolve().parents[1]
old=runpy.run_path(str(ROOT/'tests/reference_shock.py'))['shock_fit']
d=read_vtu(ROOT/'results/raw/fine_flow.vtu');jump=solve_weak_shock(2,10).p2_p1
def before():return [old(d,f) for f in (.4,.5,.6)]
def after():return pressure_crossings(d,jump)
a,b=before(),after()
max_angle_difference=max(abs(x[0]-y[0]) for x,y in zip(a,b))
assert max_angle_difference<1e-5
samples={'before':[],'after':[]}
for repeat in range(12):
    order=[('before',before),('after',after)]
    if repeat%2:order.reverse()
    for name,func in order:
        start=time.perf_counter();func();samples[name].append(time.perf_counter()-start)
medians={k:statistics.median(v) for k,v in samples.items()}
report={'scope':'Three shock thresholds on the saved fine mesh; excludes file reading, plotting and SU2.',
        'warmup_calls_per_method':1,'samples_seconds':samples,'median_seconds':medians,
        'median_speedup':medians['before']/medians['after'],'max_angle_difference_deg':max_angle_difference,
        'numpy_version':np.__version__,'note':'Same-machine microbenchmark, not a whole-program speed claim.'}
path=ROOT/'datasets/v1.1/performance.json';path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
