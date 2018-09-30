# blender functions for creating big fucking rockets


import bpy, bmesh
import math

# enter edit mode for the object & get the mesh
def edit(obj):
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.new()
    bm = bmesh.from_edit_mesh(obj.data)
    return bm

# deselect all objects
def deselect():
    #bpy.ops.object.select_all(action='DESELECT')
    for i in bpy.data.objects:
        i.select = False

def select(list):
    for i in list:
        bpy.data.objects[i].select = True

# select & activate the object
def selectByName(name):
    for i in bpy.context.scene.objects:
        #print(i.name)
        if i.name == name:
            i.select = True
            bpy.context.scene.objects.active = i
            return i

# get all selected objects in an array
def getSelected():
    result = []
    for i in bpy.context.scene.objects:
        if i.select:
            result.append(i)
    return result


def findObject(name):
    for i in bpy.context.scene.objects:
        if i.name == name:
            return i
    return None

def deleteObject(obj):
    deselect()
    obj.select = True
    obj.hide = False
    bpy.context.scene.objects.active = obj
    bpy.ops.object.delete()
    
def deleteObjectNamed(name):
    deselect()
    obj = findObject(name)
    if obj != None:
        obj.select = True
        obj.hide = False
        bpy.context.scene.objects.active = obj
        bpy.ops.object.delete()
    

# join polygons
def joinList(list, name):
    deselect()
    select(list)

    dst = bpy.data.objects[list[0]]
    bpy.context.scene.objects.active = dst
    bpy.ops.object.join()
    dst.name = name

# convert list to meshes
def toMeshes(list):
    for i in list:
        object = bpy.data.objects[i]
        object.select = True
        bpy.context.scene.objects.active = object
        bpy.ops.object.convert(target='MESH')


def toRad(angle):
    return angle * math.pi * 2.0 / 360.0


def polarToXY(angle, radius):
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return [x, y]

def XYTopolar(x, y):
    angle = math.atan2(y, x)
    radius = math.hypot(x, y)
    return [angle, radius]

def mag(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    

class VertObj:
    def __init__(self, coord, vert):
        self.coord = coord
        self.vert = vert


def deleteOverlap(obj, deleteObj=None, deleteVerts=None):
    # delete all vertices in obj which coincide between the obj & deleteObj
    mesh = edit(obj)
    
    # create arrays of the vertices in the 2 objects
    targetVerts = []
    for vert in mesh.verts:
        targetVerts.append(VertObj(obj.matrix_world * vert.co, vert))
    # sort the vertices into the scanning order
    targetVerts = sorted(targetVerts, key=lambda x: (x.coord[2]))

    if deleteVerts == None:
        print("deleteOverlap: sorting vertices from %s" % deleteObj.name)
        deleteVerts = []
        for vert in deleteObj.data.vertices:
            deleteVerts.append(VertObj(deleteObj.matrix_world * vert.co, vert))
        deleteVerts = sorted(deleteVerts, key=lambda x: (x.coord[2]))


    THRESHOLD = 0.001
    # sorted algorithm
    if True:
        #for i in range(21, 26):
        #    print("targetVert=%d %s" % (i, targetVerts[i].coord))

        #for i in range(140, 173):
        #    print("deleteVert=%d %s" % (i, deleteVerts[i].coord))
        
        i = 0
        j = 0
        # search for the fuse verts in the window verts
        for j in range(0, len(targetVerts)):
            targetVert = targetVerts[j]
            fuseCoord = targetVert.coord

            # because of rounding errors, we have to rewind & search a cube
            if i >= len(deleteVerts):
                i = len(deleteVerts) - 1
            while i > 0 and \
                i < len(deleteVerts) and \
                deleteVerts[i].coord[2] > fuseCoord[2] - THRESHOLD:
                i -= 1
            
            # search a range of Z
            while i < len(deleteVerts) and \
                deleteVerts[i].coord[2] < fuseCoord[2] - THRESHOLD:
                i += 1

            while i < len(deleteVerts) and \
                deleteVerts[i].coord[2] < fuseCoord[2] + THRESHOLD:
                
                # search a range of Y & X
                if deleteVerts[i].coord[1] >= fuseCoord[1] - THRESHOLD and \
                    deleteVerts[i].coord[1] < fuseCoord[1] + THRESHOLD and \
                    deleteVerts[i].coord[0] >= fuseCoord[0] - THRESHOLD and \
                    deleteVerts[i].coord[0] < fuseCoord[0] + THRESHOLD:
                    targetVert.vert.select = True
                    #print("targetVert=%d %s deleteVert=%d %s" % (j, fuseCoord, i, deleteVerts[i].coord))
                    break
                i += 1
            j += 1

    # british museum algorithm
    if False:
        for i in range(0, len(targetVerts)):
            targetVert = targetVerts[i]
            for j in range(0, len(deleteVerts)):
                deleteVert = deleteVerts[j]
                dist = mag(deleteVert.coord - targetVert.coord)
                if dist < THRESHOLD:
                    targetVert.vert.select = True
                    #print("targetVert=%d %s deleteVert=%d %s" % (i, targetVert.coord, j, deleteVert.coord))
                    break

    bpy.ops.mesh.delete(type='VERT')
    
    mesh.free()
    bpy.ops.object.mode_set(mode = 'OBJECT')

    
    

