import math
import pytest
from wedgeverify.shock import solve_weak_shock, max_deflection_deg, NoAttachedShock

def test_independent_published_benchmark():
    # Published numerical example: https://kursatkara.github.io/MAE3293_Fundamentals_of_Aerodynamics/calculators/oblique-shock.html
    r = solve_weak_shock(2.0, 10.0)
    assert r.shock_angle_deg == pytest.approx(39.3139, abs=0.0001)
    assert r.mach_2 == pytest.approx(1.6405, abs=0.0001)
    assert r.p2_p1 == pytest.approx(1.7066, abs=0.0001)
    assert r.rho2_rho1 == pytest.approx(1.45843, abs=0.0001)
    assert r.t2_t1 == pytest.approx(1.17015, abs=0.0001)

def test_max_deflection_threshold_and_no_attached():
    limit = max_deflection_deg(2)
    assert limit == pytest.approx(22.9735, abs=0.001)
    with pytest.raises(NoAttachedShock, match="NO_ATTACHED_SOLUTION"):
        solve_weak_shock(2, limit + 0.5)
    assert solve_weak_shock(2, limit).shock_angle_deg > 60

def test_zero_turning_angle_is_mach_wave_limit():
    r = solve_weak_shock(2, 0)
    assert r.status == "MACH_WAVE_LIMIT"
    assert r.shock_angle_deg == pytest.approx(30)
    assert r.p2_p1 == pytest.approx(1)
    assert r.rho2_rho1 == pytest.approx(1)
    assert r.mach_2 == pytest.approx(2)

def test_mass_normal_and_energy_invariants():
    r = solve_weak_shock(2, 10)
    # rho_1 u_n1 = rho_2 u_n2; speed/sqrt(T) = Mach * sqrt(gamma R)
    assert r.normal_mach_1 == pytest.approx(r.rho2_rho1 * r.normal_mach_2 * math.sqrt(r.t2_t1), rel=1e-12)
    # h_t = cp*T*(1+(gamma-1)*Mach^2/2) is unchanged
    assert 1+(r.gamma-1)*r.mach_1**2/2 == pytest.approx(r.t2_t1*(1+(r.gamma-1)*r.mach_2**2/2), rel=1e-12)

def test_always_weak_branch_and_increasing_pressure():
    last = 1.0
    for theta in [1, 5, 10, 15, 20]:
        r = solve_weak_shock(2, theta)
        assert 30 < r.shock_angle_deg < 70
        assert r.p2_p1 > last
        last = r.p2_p1

def test_invalid_values():
    for mach, theta, gamma in [(1,10,1.4),(2,-1,1.4),(2,90,1.4),(2,10,1),(float("nan"),10,1.4)]:
        with pytest.raises(ValueError):
            solve_weak_shock(mach,theta,gamma)
