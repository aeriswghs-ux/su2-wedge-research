"""Run with ParaView's pvpython: native renders, editable state and line samples."""
from pathlib import Path
import csv, hashlib, json, os
import numpy as np
from paraview.simple import *
import paraview.simple as pvs
pvs._DisableFirstRenderCameraReset()
from paraview import servermanager
from vtkmodules.util.numpy_support import vtk_to_numpy

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'paraview';OUT.mkdir(exist_ok=True)
os.chdir(ROOT)
readers={};manifest={'software':'ParaView 6.2.1','source':'Existing SU2 baseline fields; no new simulations',
                     'line':{'start':[1,.12,0],'end':[1,.8,0],'segments':800},'inputs':{}}
for mesh in ['coarse','medium','fine']:
    path=ROOT/f'results/raw/{mesh}_flow.vtu'
    readers[mesh]=XMLUnstructuredGridReader(registrationName=f'{mesh} baseline',FileName=[str(path)])
    readers[mesh].UpdatePipeline()
    manifest['inputs'][mesh]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                             'points':readers[mesh].GetDataInformation().GetNumberOfPoints()}
ranges={field:[min(r.PointData[field].GetRange()[0] for r in readers.values()),
               max(r.PointData[field].GetRange()[1] for r in readers.values())] for field in ['Mach','Pressure','Density']}
manifest['color_ranges']=ranges

def view_field(reader,field,title):
    view=CreateView('RenderView');view.ViewSize=[1600,1000]
    view.UseColorPaletteForBackground=0;view.Background=[1,1,1]
    view.OrientationAxesVisibility=0;view.InteractionMode='2D'
    display=Show(reader,view);display.Representation='Surface';display.Ambient=1;display.Diffuse=0
    ColorBy(display,('POINTS',field))
    lut=GetColorTransferFunction(field);lut.RGBPoints=[0,.267,.005,.329,.25,.230,.322,.546,.5,.128,.567,.551,.75,.369,.789,.383,1,.993,.906,.144];lut.ColorSpace='RGB'
    lut.RescaleTransferFunction(*ranges[field]);lut.AutomaticRescaleRangeMode='Never'
    display.SetScalarBarVisibility(view,True)
    bar=GetScalarBar(lut,view);bar.Title={'Mach':'Mach number','Pressure':'Pressure (Pa)','Density':'Density (kg/m3)'}[field]
    bar.ComponentTitle='';bar.TitleColor=[.1,.1,.1];bar.LabelColor=[.1,.1,.1]
    bar.TitleFontSize=16;bar.LabelFontSize=14;bar.WindowLocation='Lower Center';bar.Orientation='Horizontal'
    bar.ScalarBarLength=.60;bar.WindowLocation='Any Location';bar.Position=[.20,.06]
    bar.AutomaticLabelFormat=0;bar.LabelFormat='{:.0f}' if field=='Pressure' else '{:.2f}';bar.RangeLabelFormat=bar.LabelFormat
    bar.UseCustomLabels=1;bar.CustomLabels=list(np.linspace(*ranges[field],5))
    annotation=Text(registrationName=title);annotation.Text=title
    label=Show(annotation,view);label.Color=[.1,.1,.1];label.FontSize=20;label.WindowLocation='Upper Left Corner'
    view.CameraPosition=[.75,.5,3];view.CameraFocalPoint=[.75,.5,0];view.CameraViewUp=[0,1,0]
    view.CameraParallelProjection=1;view.CameraParallelScale=.8
    view.AxesGrid.Visibility=1;view.AxesGrid.XTitle='x (m)';view.AxesGrid.YTitle=''
    view.AxesGrid.ShowGrid=0
    view.AxesGrid.XTitleColor=[.15,.15,.15];view.AxesGrid.YTitleColor=[.15,.15,.15]
    view.AxesGrid.XLabelColor=[.15,.15,.15];view.AxesGrid.YLabelColor=[.15,.15,.15]
    return view,display

for field in ['Mach','Pressure','Density']:
    view,display=view_field(readers['fine'],field,f'{field} | Mach 2, 10-degree ramp | 38,400 cells')
    Render(view)
    SaveScreenshot(str(OUT/f'fine_{field.lower()}.png'),view,ImageResolution=[1600,1000])
    if field=='Mach':
        line=Line(registrationName='Profile line x = 1 m');line.Point1=[1,.12,0];line.Point2=[1,.8,0]
        ld=Show(line,view);ld.DiffuseColor=[.9,.1,.1];ld.LineWidth=3
        SaveScreenshot(str(OUT/'sampling_location.png'),view,ImageResolution=[1600,1000])
        Hide(line,view)

layout=CreateLayout(name='Pressure comparison - common color scale')
layout.SplitHorizontal(0,1/3);layout.SplitHorizontal(2,.5)
for mesh,hint in zip(['coarse','medium','fine'],[1,5,6]):
    view,display=view_field(readers[mesh],'Pressure',mesh.capitalize()+' mesh | Pressure (Pa)')
    view.CameraParallelScale=.9
    AssignViewToLayout(view,layout,hint=hint)
layout.SetSize(2100,750)
SaveScreenshot(str(OUT/'mesh_comparison.png'),layout,ImageResolution=[2100,750])

for mesh,reader in readers.items():
    probe=PlotOverLine(registrationName=f'{mesh} profile x=1 m',Input=reader)
    probe.Point1=[1,.12,0];probe.Point2=[1,.8,0];probe.Resolution=800
    probe.SamplingPattern='Sample Uniformly';probe.UpdatePipeline()
    data=servermanager.Fetch(probe)
    mask=vtk_to_numpy(data.GetPointData().GetArray('vtkValidPointMask'))
    if not np.all(mask==1):raise RuntimeError(f'{mesh}: line leaves the valid fluid domain')
    points=vtk_to_numpy(data.GetPoints().GetData())
    values=[vtk_to_numpy(data.GetPointData().GetArray(k)) for k in ['Pressure','Density','Mach']]
    if not all(np.isfinite(a).all() for a in values):raise RuntimeError('Nonfinite profile')
    with (OUT/f'{mesh}_profile.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['x_m','y_m','pressure_pa','density_kg_m3','mach'])
        writer.writerows(zip(points[:,0],points[:,1],*values))
    manifest['inputs'][mesh]['valid_profile_points']=len(points)
SaveState(str(OUT/'wedge.pvsm'))
# Keep the distributed state free of machine-specific paths.
state=OUT/'wedge.pvsm';text=state.read_text()
text=text.replace(str(ROOT).replace('\\','/').rstrip('/')+'/', '').replace(str(ROOT)+'\\','')
state.write_text(text)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
