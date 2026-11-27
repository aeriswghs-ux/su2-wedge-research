from pathlib import Path
import math
from wedgeverify.mesh import generate_mesh


def read_mesh(path):
    rows = Path(path).read_text().splitlines()
    assert rows.pop(0) == 'NDIME= 2'
    n = int(rows.pop(0).split('=')[1]); quads=[list(map(int,rows.pop(0).split())) for _ in range(n)]
    npoints = int(rows.pop(0).split('=')[1]); pts=[]
    for _ in range(npoints):
        x,y,i=rows.pop(0).split()
        assert int(i) == len(pts)
        pts.append((float(x),float(y)))
    markers={}
    assert rows.pop(0) == 'NMARK= 4'
    for _ in range(4):
        key=rows.pop(0).split('=')[1].strip()
        nedge=int(rows.pop(0).split('=')[1])
        markers[key] = [tuple(map(int,rows.pop(0).split())) for _ in range(nedge)]
    assert not rows
    return quads, pts, markers


def test_positive_quad_areas_all_markers_and_integrated_domain(tmp_path):
    mesh = tmp_path/'test.su2'
    generate_mesh(mesh,60,40)
    quads, points, markers = read_mesh(mesh)
    for quad in quads:
        assert quad[0] == 9 and len(quad)==5
        xy = [points[i] for i in quad[1:]]
        twice_area=sum(xy[k][0]*xy[(k+1)%4][1]-xy[(k+1)%4][0]*xy[k][1] for k in range(4))
        assert twice_area > 0
    assert len(markers['lower']) == len(markers['upper']) == 60
    assert len(markers['inlet']) == len(markers['outlet']) == 40
    assert all(edge[0]==3 and len(edge)==3 for edges in markers.values() for edge in edges)
    assert points[0]==(0.0,0.0)
    assert points[-1]==(1.5,1.0)
