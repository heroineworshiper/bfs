# blender script to export the raptor from raptor_flame2.blend
# don't save the file
# your job: export as a GLTF with SELECTED ONLY selected


import bpy
import library
import importlib


importlib.reload(library)


singleSidedEngine = [
    'Cylinder.001',
    'NurbsCircle',
    'NurbsCircle.001',
    'NurbsCircle.002',
    'NurbsCircle.003',
    'NurbsCircle.004',
    'NurbsCircle.005',
    'tube1',
    'tube2'
]

doubleSidedEngine = [
    'Cylinder',
    
]

seaNozzle = [
    'sea nozzle'
]

vacuumNozzle = [
    'vacuum nozzle'
]

nurbs = [
    'NurbsCircle',
    'NurbsCircle.001',
    'NurbsCircle.002',
    'NurbsCircle.003',
    'NurbsCircle.004',
    'NurbsCircle.005',
    
]

#flameCones = [
#    'Cone',
#    'Cone.001',
#    'Cone.002',
#    'Cone.003',
#    'Cone.004',
#]

exportList = [
    'singleSidedEngine',
    'doubleSidedEngine',
    'seaNozzle',
    'vacuumNozzle',
    'cones',
    'flame'
]

# should clone these in Godot
#flameSpheres = [
#    'flame'
#]

library.toMeshes(nurbs)
library.joinList(singleSidedEngine, 'singleSidedEngine')
library.joinList(doubleSidedEngine, 'doubleSidedEngine')
library.joinList(seaNozzle, 'seaNozzle')
library.joinList(vacuumNozzle, 'vacuumNozzle')
#library.joinList(flameCones, 'flameCones')
#library.joinList(flameSpheres, 'flameSpheres')

library.select(exportList)

