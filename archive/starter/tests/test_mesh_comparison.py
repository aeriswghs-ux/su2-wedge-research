from wedgeverify.mesh import generate_mesh, GRID_LEVELS
from wedgeverify.comparison import compare_rows

def test_mesher_counts_tags_tip_and_volume(tmp_path):
    meta = generate_mesh(tmp_path / 'wedge.su2', 6, 4)
    data = (tmp_path / 'wedge.su2').read_text().splitlines()
    assert meta['cells'] == 24 and meta['points'] == 35
    assert 'NELEM= 24' in data
    assert 'NPOIN= 35' in data
    assert 'NMARK= 4' in data
    assert [x for x in data if x.startswith('MARKER_TAG=')] == [
        'MARKER_TAG= lower','MARKER_TAG= upper','MARKER_TAG= inlet','MARKER_TAG= outlet']
    nodes_at_tip = [x for x in data if x.startswith('0.5 ')]
    assert len(nodes_at_tip) == 5

def test_grid_refinement_cell_count_factor_four():
    sizes = [a*b for a,b in GRID_LEVELS.values()]
    assert sizes[1]/sizes[0] == sizes[2]/sizes[1] == 4

def test_blank_measurements_remain_unexecuted():
    rows = [{"mesh": "coarse", "cells": "2400", "h_m": "0.025", 
             "shock_angle_deg": "", "p2_p1": "", "rho2_rho1":"", "mach_2":""}]
    result = compare_rows(rows)[0]
    assert result['shock_angle_deg'] == 'NOT_EXECUTED'
    assert result['shock_angle_deg_rel_error_pct'] == 'NOT_EXECUTED'

def test_comparison_only_uses_supplied_values():
    rows = [{"mesh": "coarse", "cells": "2400", "h_m": "0.025", 
             "shock_angle_deg": "39.5", "p2_p1": "", "rho2_rho1":"", "mach_2":""}]
    r = compare_rows(rows)[0]
    assert r['shock_angle_deg_abs_error'] > 0
    assert r['p2_p1'] == 'NOT_EXECUTED'
