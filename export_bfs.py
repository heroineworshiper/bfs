# blender script to export the BFS

# your job: export as a GLTF with SELECTED ONLY selected


import bpy


# single sided polygons
singleSided = [
        bpy.data.objects['Extrude008 Mesh'], 
        bpy.data.objects['Extrude007 Mesh'], 
        bpy.data.objects['Extrude002 Mesh'], 
        bpy.data.objects['Extrude001 Mesh'], 
        bpy.data.objects['Extrude004 Mesh'], 
        bpy.data.objects['Extrude006 Mesh'], 
        bpy.data.objects['Extrude005 Mesh'], 
        bpy.data.objects['Extrude003 Mesh'],
        bpy.data.objects['fuel line sweep002 Mesh'], 
        bpy.data.objects['fuel line cube002 Mesh'], 
        bpy.data.objects['fuel line cube003 Mesh'], 
        bpy.data.objects['fuel line sweep Mesh'], 
        bpy.data.objects['fuse revolve Mesh'], 
        bpy.data.objects['fuel line sweep004 Mesh'], 
        bpy.data.objects['fuel line cube Mesh'], 
        bpy.data.objects['fuel line sweep003 Mesh'], 
        bpy.data.objects['fuel line cube004 Mesh'],
        bpy.data.objects['nose Mesh'], 
        bpy.data.objects['tank Mesh'], 
        bpy.data.objects['tank2 Mesh'],
        bpy.data.objects['landing fairing revolve (Mirror #3) Mesh'],
        bpy.data.objects['landing fairing revolve Mesh']
    ]


doubleSidedWing = [
    bpy.data.objects['wing Mesh'], 
    bpy.data.objects['Loft Mesh']
]

doubleSidedMetal = [
    bpy.data.objects['fuel line nozzle2 revolve003 Mesh.001'], 
    bpy.data.objects['fuel line nozzle revolve Mesh.001'], 
    bpy.data.objects['fuel line nozzle2 revolve003 Mesh'], 
    bpy.data.objects['fuel line nozzle revolve Mesh'], 
]

exportList = [
    'singleSided',
    'doubleSidedWing',
    'doubleSidedMetal',
    'landing leg Mesh',
    'landing leg (Mirror #3) Mesh',
    'landing leg (Mirror #4) Mesh',
    'landing leg (Mirror #5) Mesh',
    'window mesh'
]

# deselect all
def deselect():
    for i in bpy.data.objects:
        i.select = False

def select(list):
    for i in list:
        i.select = True

def selectByName(list):
    for i in list:
        bpy.data.objects[i].select = True

# join polygons
def joinList(list, name):
    deselect()
    select(list)

    bpy.context.scene.objects.active = list[0]
    bpy.ops.object.join()
    list[0].name = name


joinList(singleSided, 'singleSided')
joinList(doubleSidedWing, 'doubleSidedWing')
joinList(doubleSidedMetal, 'doubleSidedMetal')
deselect()
selectByName(exportList)











