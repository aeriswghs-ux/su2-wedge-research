from pathlib import Path
import runpy
import numpy as np
import pytest
from scripts.inspect_flow import read_vtu
from wedgeverify.measure import pressure_crossings, cell_values, box_average
from wedgeverify.shock import solve_weak_shock

ROOT=Path(__file__).resolve().parents[1]
old=runpy.run_path(str(ROOT/'tests/reference_shock.py'))['shock_fit']

@pytest.mark.parametrize('mesh',['coarse','medium','fine'])
def test_optimized_detector_matches_reference(mesh):
    if not (ROOT/f'results/raw/{mesh}_flow.vtu').exists():
        pytest.skip('Download the results package for saved-flow regression checks')
    data=read_vtu(ROOT/f'results/raw/{mesh}_flow.vtu')
    fractions=np.linspace(.3,.7,9)
    for fraction,new in zip(fractions,pressure_crossings(data,solve_weak_shock(2,10).p2_p1,fractions)):
        reference=old(data,fraction)
        np.testing.assert_allclose(new[:2],reference[:2],rtol=0,atol=1e-5)
        np.testing.assert_allclose(new[2],reference[2],rtol=0,atol=1e-6)

def test_uniform_field_box_average_and_empty_box():
    centers=np.array([[0.,0.],[1.,1.]])
    means,count=box_average(centers,np.array([1.,3.]),{'Pressure':np.array([2.,6.])},(-1,2,-1,2))
    assert means['Pressure']==5 and count==2
    with pytest.raises(ValueError,match='no cell centers'):
        box_average(centers,np.ones(2),{},(4,5,4,5))

def test_missing_shock_is_not_fabricated():
    d={'Points':np.array([[.9,0,0],[.9,1,0]]),'Pressure':np.array([100000.,100000.])}
    with pytest.raises(ValueError,match='Too few'):
        pressure_crossings(d,1.7)
