"""Run with portable pvpython to independently read the raw VTU fields."""
from pathlib import Path
import json
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.util.numpy_support import vtk_to_numpy
import numpy as np
root=Path(__file__).resolve().parents[1]
summary={}
for level in ['coarse','medium','fine']:
    reader=vtkXMLUnstructuredGridReader()
    reader.SetFileName(str(root/'results/raw'/f'{level}_flow.vtu'))
    reader.Update()
    grid=reader.GetOutput()
    result={'points':grid.GetNumberOfPoints(),'cells':grid.GetNumberOfCells(),'arrays':{}}
    for k in ['Pressure','Density','Mach']:
        a=vtk_to_numpy(grid.GetPointData().GetArray(k))
        result['arrays'][k]={'min':float(a.min()),'max':float(a.max()),'finite':bool(np.isfinite(a).all())}
    summary[level]=result
print(json.dumps(summary,indent=2))
(root/'results/paraview_readback.json').write_text(json.dumps(summary,indent=2))
