import numpy as np
import pytest
from wedgeverify.measure import gradient_shock

def field():
    x,y=np.meshgrid(np.linspace(.8,1.25,31),np.linspace(0,1,501))
    line=(x-.5)*.8
    pressure=100000+70000*(1-np.tanh((y-line)/.008))/2
    return {'Points':np.column_stack((x.ravel(),y.ravel(),np.zeros(x.size))), 'Pressure':pressure.ravel()}

def test_gradient_recovers_known_synthetic_angle():
    data=field()
    beta,_,_=gradient_shock(data)
    assert abs(beta-np.degrees(np.arctan(.8)))<.01
    order=np.random.default_rng(1).permutation(len(data['Pressure']))
    shuffled={key:values[order] for key,values in data.items()}
    assert gradient_shock(shuffled)[0]==pytest.approx(beta,abs=1e-10)

def test_uniform_pressure_has_no_shock():
    data=field();data['Pressure'][:]=100000
    with pytest.raises(ValueError,match='Too few'):gradient_shock(data)
