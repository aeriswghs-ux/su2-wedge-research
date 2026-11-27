"""Reopen the portable ParaView state and check that all three meshes load."""
from pathlib import Path
import os,json
from paraview.simple import LoadState,GetSources
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
LoadState(str(ROOT/'paraview/wedge.pvsm'))
counts={}
for (name,_),source in GetSources().items():
    if name.endswith(' baseline'):
        source.UpdatePipeline()
        counts[name]=source.GetDataInformation().GetNumberOfCells()
assert counts=={'coarse baseline':2400,'medium baseline':9600,'fine baseline':38400},counts
(ROOT/'paraview/state_check.json').write_text(json.dumps({'loaded_cell_counts':counts,'status':'PASS'},indent=2))
print(counts)
