  # -*- coding: utf-8 -*-
  # Run this script in Abaqus to generate STL parametrically
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
  # Design parameters, unit: mm
hole_radius = 0.8
plate_thickness = 0.08
file_name = '0.15_b.stl' 
file_path = 'C:/temp/stl_task/'
final_path = file_path+file_name

p = mdb.models['Model-1'].Part(name='origin', dimensionality=THREE_D,
    type=DEFORMABLE_BODY)
p.ReferencePoint(point=(0.0, 0.0, 0.0))
p = mdb.models['Model-1'].parts['origin']
p = mdb.models['Model-1'].parts['origin']
p.DatumPointByCoordinate(coords=(4.0, 4.0, 4.0))
p = mdb.models['Model-1'].parts['origin']
p.DatumPointByCoordinate(coords=(-4.0, 4.0, -4.0))
p = mdb.models['Model-1'].parts['origin']
p.DatumPointByCoordinate(coords=(-4.0, -4.0, 4.0))
p = mdb.models['Model-1'].parts['origin']
d = p.datums
p.DatumPlaneByThreePoints(point1=d[3], point2=d[2], point3=d[4])
p = mdb.models['Model-1'].parts['origin']
d1 = p.datums
p.DatumAxisByTwoPoint(point1=d1[2], point2=d1[4])
p = mdb.models['Model-1'].parts['origin']
d = p.datums
t = p.MakeSketchTransform(sketchPlane=d[5], sketchUpEdge=d[6],
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-1.333333,
    1.333333, 1.333333))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=1018.95, gridSpacing=25.47, transform=t)
g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['origin']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.Line(point1=(-6.53197264742181, 0.0), point2=(3.2659863237109,
    5.65685424949238))
s.Line(point1=(3.2659863237109, 5.65685424949238), point2=(3.2659863237109,
    -5.65685424949238))
s.VerticalConstraint(entity=g[4], addUndoState=False)
s.Line(point1=(3.2659863237109, -5.65685424949238), point2=(-6.53197264742181,
    0.0))
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.717050845622472,
    -0.710688926135186))
s.RadialDimension(curve=g[6], textPoint=(-2.31042518534429, 0.400725492145819),
    radius=hole_radius)
p = mdb.models['Model-1'].parts['origin']
d2 = p.datums
p.SolidExtrude(sketchPlane=d2[5], sketchUpEdge=d2[6], sketchPlaneSide=SIDE1,
    sketchOrientation=RIGHT, sketch=s, depth=plate_thickness, flipExtrudeDirection=OFF)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['origin']
f, e, d = p.faces, p.edges, p.datums
p.HoleThruAllFromEdges(plane=f[5], edge1=e[8], edge2=e[2], planeSide=SIDE1,
diameter=2*hole_radius, distance1=1.6, distance2=1.6)
p = mdb.models['Model-1'].parts['origin']
f1, e1, d2 = p.faces, p.edges, p.datums
p.HoleThruAllFromEdges(plane=f1[6], edge1=e1[10], edge2=e1[8], planeSide=SIDE1,
    diameter=2*hole_radius, distance1=1.6, distance2=1.6)
p = mdb.models['Model-1'].parts['origin']
f, e, d = p.faces, p.edges, p.datums
p.HoleThruAllFromEdges(plane=f[7], edge1=e[10], edge2=e[6], planeSide=SIDE1,
    diameter=2*hole_radius, distance1=1.6, distance2=1.6)

  # Assembly
  # Create assembly frame
a = mdb.models['Model-1'].rootAssembly
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['origin']
a.Instance(name='origin-1', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(4.0, 4.0, 4.0))
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(4.0, 4.0, -4.0))
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(4.0, -4.0, 4.0))
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(4.0, -4.0, -4.0))
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(-4.0, 4.0, 4.0))
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(-4.0, 4.0, -4.0))
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(-4.0, -4.0, 4.0))
a = mdb.models['Model-1'].rootAssembly
a.DatumPointByCoordinate(coords=(-4.0, -4.0, -4.0))

a1 = mdb.models['Model-1'].rootAssembly
e11 = a1.instances['origin-1'].edges
d21 = a1.datums
a1.CoincidentPoint(fixedPoint=d21[9],
    movablePoint=a1.instances['origin-1'].InterestingPoint(edge=e11[9],
    rule=MIDDLE))
a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['origin']
a1.Instance(name='origin-2', part=p, dependent=ON)
p1 = a1.instances['origin-2']
p1.translate(vector=(11.1133468389424, 0.0, 0.0))
a1 = mdb.models['Model-1'].rootAssembly
e11 = a1.instances['origin-2'].edges
d21 = a1.datums
a1.CoincidentPoint(fixedPoint=d21[8],
    movablePoint=a1.instances['origin-2'].InterestingPoint(edge=e11[9],
    rule=MIDDLE))

a1 = mdb.models['Model-1'].rootAssembly
e1 = a1.instances['origin-2'].edges
d21 = a1.datums
a1.CoincidentPoint(fixedPoint=d21[6],
    movablePoint=a1.instances['origin-2'].InterestingPoint(edge=e1[7],
    rule=MIDDLE))

a1 = mdb.models['Model-1'].rootAssembly
e11 = a1.instances['origin-2'].edges
d21 = a1.datums
a1.CoincidentPoint(fixedPoint=d21[5],
    movablePoint=a1.instances['origin-2'].InterestingPoint(edge=e11[11],
    rule=MIDDLE))
a1 = mdb.models['Model-1'].rootAssembly
a1.LinearInstancePattern(instanceList=('origin-1', 'origin-2'), direction1=(
    1.0, 0.0, 0.0), direction2=(0.0, 1.0, 0.0), number1=1, number2=2,
    spacing1=8.09238, spacing2=10.0)
a1 = mdb.models['Model-1'].rootAssembly
a1.rotate(instanceList=('origin-1-lin-1-2', ), axisPoint=(0.0, 0.0, 0.0),
    axisDirection=(0.0, 10.0, 0.0), angle=-90.0)
a1 = mdb.models['Model-1'].rootAssembly
a1.translate(instanceList=('origin-1-lin-1-2', ), vector=(0.0, -10.0, 0.0))
a1 = mdb.models['Model-1'].rootAssembly
a1.rotate(instanceList=('origin-2-lin-1-2', ), axisPoint=(0.0, 0.0, 0.0),
    axisDirection=(0.0, 10.0, 0.0), angle=90.0)
a1 = mdb.models['Model-1'].rootAssembly
a1.translate(instanceList=('origin-2-lin-1-2', ), vector=(0.0, -10.0, 0.0))

  # Duplicate, rotate, and assemble plates 1-4
a1 = mdb.models['Model-1'].rootAssembly
a1.LinearInstancePattern(instanceList=('origin-1', 'origin-2',
    'origin-1-lin-1-2', 'origin-2-lin-1-2'), direction1=(1.0, 0.0, 0.0),
    direction2=(0.0, 1.0, 0.0), number1=1, number2=2, spacing1=8.09238,
    spacing2=10.0)
a1 = mdb.models['Model-1'].rootAssembly
a1.rotate(instanceList=('origin-1-lin-1-2-1', 'origin-2-lin-1-2-1',
    'origin-1-lin-1-2-lin-1-2', 'origin-2-lin-1-2-lin-1-2'), axisPoint=(0.0,
    0.0, 0.0), axisDirection=(10.0, 0.0, 0.0), angle=180.0)
a1 = mdb.models['Model-1'].rootAssembly
a1.translate(instanceList=('origin-1-lin-1-2-1', 'origin-2-lin-1-2-1',
    'origin-1-lin-1-2-lin-1-2', 'origin-2-lin-1-2-lin-1-2'), vector=(0.0, 10.0,
    0.0))

a1 = mdb.models['Model-1'].rootAssembly
a1.InstanceFromBooleanMerge(name='fcc_cell', instances=(
    a1.instances['origin-1'], a1.instances['origin-2'],
    a1.instances['origin-1-lin-1-2'], a1.instances['origin-2-lin-1-2'],
    a1.instances['origin-1-lin-1-2-1'], a1.instances['origin-2-lin-1-2-1'],
    a1.instances['origin-1-lin-1-2-lin-1-2'],
    a1.instances['origin-2-lin-1-2-lin-1-2'], ), originalInstances=SUPPRESS,
    domain=GEOMETRY)
p1 = mdb.models['Model-1'].parts['fcc_cell']
p = mdb.models['Model-1'].parts['fcc_cell']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=5.0)  # Offset 5 mm from principal plane
p = mdb.models['Model-1'].parts['fcc_cell']
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=5.0)
  # Draw cutting profile and perform Cut 1
p = mdb.models['Model-1'].parts['fcc_cell']
f1, e1, d2 = p.faces, p.edges, p.datums
t = p.MakeSketchTransform(sketchPlane=d2[3], sketchUpEdge=e1[443],
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(5.0, 0.0, 0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=32.11, gridSpacing=0.8, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['fcc_cell']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.rectangle(point1=(-4.0, -4.0), point2=(4.0, 4.0))  # Inner rectangle
s.rectangle(point1=(-4.6, 4.4), point2=(4.6, -4.4))  # Outer rectangle
p = mdb.models['Model-1'].parts['fcc_cell']
f, e, d1 = p.faces, p.edges, p.datums
p.CutExtrude(sketchPlane=d1[3], sketchUpEdge=e[443], sketchPlaneSide=SIDE1,
    sketchOrientation=RIGHT, sketch=s, depth=10.0, flipExtrudeDirection=OFF)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['fcc_cell']
f1, e1, d2 = p.faces, p.edges, p.datums
t = p.MakeSketchTransform(sketchPlane=d2[2], sketchUpEdge=e1[113],
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 5.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=32.11, gridSpacing=0.8, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['fcc_cell']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.rectangle(point1=(-4.0, -4.0), point2=(4.0, 4.0))
s1.rectangle(point1=(-4.6, 4.4), point2=(4.4, -4.4))
p = mdb.models['Model-1'].parts['fcc_cell']
f, e, d1 = p.faces, p.edges, p.datums
p.CutExtrude(sketchPlane=d1[2], sketchUpEdge=e[113], sketchPlaneSide=SIDE1,
    sketchOrientation=RIGHT, sketch=s1, depth=10.0, flipExtrudeDirection=OFF)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
  # Array 'fcc_cell' in the assembly
a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fcc_cell']
a1.Instance(name='fcc_cell-1', part=p, dependent=ON)
  # Array 1
a1 = mdb.models['Model-1'].rootAssembly
a1.LinearInstancePattern(instanceList=('fcc_cell-1', ), direction1=(1.0, 0.0,
    0.0), direction2=(0.0, 1.0, 0.0), number1=3, number2=3, spacing1=8.0,
    spacing2=8.0)
  # Array 2
a1 = mdb.models['Model-1'].rootAssembly
a1.LinearInstancePattern(instanceList=('fcc_cell-1', 'fcc_cell-1-lin-1-2',
    'fcc_cell-1-lin-1-3', 'fcc_cell-1-lin-2-1', 'fcc_cell-1-lin-2-2',
    'fcc_cell-1-lin-2-3', 'fcc_cell-1-lin-3-1', 'fcc_cell-1-lin-3-2',
    'fcc_cell-1-lin-3-3'), direction1=(0.0, 0.0, 1.0), direction2=(0.0, 1.0,
    0.0), number1=3, number2=1, spacing1=8.0, spacing2=24.0)

  # Export STL
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
import sys
sys.path.insert(8,
    r'c:/SIMULIA/EstProducts/2022/win_b64/code/python2.7/lib/abaqus_plugins/stlExport')
import stlExport_kernel
  # Specify path
stlExport_kernel.STLExport(moduleName='Assembly',
    stlFileName= final_path,
    stlFileType='BINARY')
