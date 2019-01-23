# blender functions for creating big fucking rockets


import bpy, bmesh
import math

PATH="/amazon2/root/bfs/bfs.godot/"

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

def selectList(list):
    for i in list:
        obj = findObject(i)
        if obj == None:
            print(i + " not found")
        else:
            findObject(i).select = True

# deselect all, select the obj & make it the active obj
def selectActivate(obj):
    deselect()
    obj.select = True
    bpy.context.scene.objects.active = obj


# select & activate the object
def selectByName(name):
    deselect()
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

def duplicateByName(name2, name1):
    obj = selectByName(name1)
    bpy.ops.object.duplicate()
    result = getSelected()[0]
    bpy.context.scene.objects.active = result
    result.name = name2
    return result




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
    
def deleteObjectsNamed(objs):
    for i in objs:
        deleteObjectNamed(i)


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

def fromRad(angle):
    return angle * 360.0 / math.pi / 2.0

def polarToXY(angle, radius):
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return [x, y]

def XYToPolar(x, y):
    angle = math.atan2(y, x)
    radius = math.hypot(x, y)
    return [angle, radius]

def mag(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)


def thickness(obj, value):
    selectActivate(obj)
    mod = obj.modifiers.new(type="SOLIDIFY", name="mod")
    mod.thickness = value
    bpy.ops.object.modifier_apply(modifier="mod")
    

class VertObj:
    def __init__(self, coord, vert):
        self.coord = coord
        self.vert = vert


# extract sorted vertices from the object
def objToVerts(obj):
    resultVerts = []
    for vert in obj.data.vertices:
        resultVerts.append(VertObj(obj.matrix_world * vert.co, vert))
    resultVerts = sorted(resultVerts, key=lambda x: (x.coord[2]))
    return resultVerts


# delete all vertices in keepObj which are in deleteObj
# optionally, provide sorted vertices in deleteVerts to speed it up
def deleteOverlap(keepObj, deleteObj=None, deleteVerts=None):
    mesh = edit(keepObj)
    
    # create arrays of the vertices in the 2 objects
    keepVerts = []
    for vert in mesh.verts:
        keepVerts.append(VertObj(keepObj.matrix_world * vert.co, vert))
    # sort the vertices into the scanning order
    keepVerts = sorted(keepVerts, key=lambda x: (x.coord[2]))

    if deleteVerts == None:
        print("deleteOverlap: sorting vertices from %s" % deleteObj.name)
        deleteVerts = objToVerts(deleteObj)


    THRESHOLD = 0.001
    # localized british museum algorithm
    if True:
        #for i in range(0, len(keepVerts)):
        #    if keepVerts[i].coord.z < -32 and keepVerts[i].coord.z > -46:
        #        print("keepVert=%d %s" % (i, keepVerts[i].coord))

        #for i in range(0, len(deleteVerts)):
        #    if deleteVerts[i].coord.z < -32 and deleteVerts[i].coord.z > -46:
        #        print("deleteVert=%d %s" % (i, deleteVerts[i].coord))
        
        i = 0
        j = 0
        # search for the fuse verts in the window verts
        for j in range(0, len(keepVerts)):
            keepVert = keepVerts[j]
            fuseCoord = keepVert.coord

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
                    keepVert.vert.select = True
                    #print("keepVert=%d %s deleteVert=%d %s" % (j, fuseCoord, i, deleteVerts[i].coord))
                    break
                i += 1
            j += 1

    # british museum algorithm
    if False:
        for i in range(0, len(keepVerts)):
            keepVert = keepVerts[i]
            for j in range(0, len(deleteVerts)):
                deleteVert = deleteVerts[j]
                dist = mag(deleteVert.coord - keepVert.coord)
                if dist < THRESHOLD:
                    keepVert.vert.select = True
                    #print("keepVert=%d %s deleteVert=%d %s" % (i, keepVert.coord, j, deleteVert.coord))
                    break

    bpy.ops.mesh.delete(type='VERT')
    
    mesh.free()
    bpy.ops.object.mode_set(mode = 'OBJECT')





# cut cookie out of the target with a cutter
# both objects must be subdivided
# obj.location doesn't alter the matrix_world, so have to use bpy.ops.transform.translate
# returns the cookie
def cookieCut(target, cutter, cookieName, solver='CARVE'):
    result = None
    cutterVerts = objToVerts(cutter)

    selectActivate(target)
    bpy.ops.object.duplicate()
    
    # this object becomes the cookie
    result = getSelected()[0]
    result.name = cookieName
    
    # this object becomes the outline
    selectActivate(target)

    # create the outline
    bool = target.modifiers.new(type="BOOLEAN", name="bool")
    bool.operation = 'DIFFERENCE'
    bool.solver = solver
    bool.object = cutter
    bpy.ops.object.modifier_apply(modifier="bool")

    # boolean artifacts
    # delete all vertices which coincide between the windows & the plug
    deleteOverlap(target, cutter, cutterVerts)

    # create the cookie
    selectActivate(result)

    bool = result.modifiers.new(type="BOOLEAN", name="bool")
    bool.operation = 'INTERSECT'
    bool.solver = solver
    bool.object = cutter
    bpy.ops.object.modifier_apply(modifier="bool")

    # boolean artifacts
    # delete all vertices which coincide between the windows & the plug
    deleteOverlap(result, cutter, cutterVerts)

    # hide the cutter
    cutter.hide = True

    return result

def dumpUVs(obj):
    data = obj.data
    uvs = data.uv_layers[-1].data
    for i in range(0, len(uvs)):
        coord = uvs[i].uv
        print("uv %f %f" % (coord[0], coord[1]))


# map UV coords on a cylindrical object
# assume the cylinder rotates around the Z axis in world frame
def cylinderUV(obj, flipZ=False, flipX=False):
    #deselect()
    #mesh = edit(obj)
    #bpy.ops.mesh.select_all(action='SELECT')
    #bpy.ops.uv.smart_project()
    #bpy.ops.mesh.select_all(action='DESELECT')
    #bpy.ops.uv.select_all(action='SELECT')
    #bpy.ops.transform.rotate(value=angle)

    data = obj.data
    if len(data.uv_layers) < 1:
        data.uv_textures.new("big fucking UV map")
    
    uvs = data.uv_layers[-1].data
    verts = data.vertices
    
    #print("total polys=%d" % len(data.polygons))
    #print("total uvs=%d %s" % (len(uvs), uvs[0]))
    #print("total verts=%d %s" % (len(verts), verts[0]))
    
    #for poly in data.polygons:
    #    print("verts=%s uvs=%s" % (poly.vertices, poly.loop_indices))

    # discover the used quadrants
    quadrants = [ False, False, False, False ]
    for vert in verts:
        worldCoord = obj.matrix_world * vert.co
        if worldCoord.x >= 0 and worldCoord.y >= 0:
            quadrants[0] = True
        elif worldCoord.x >= 0 and worldCoord.y < 0:
            quadrants[1] = True
        elif worldCoord.x < 0 and worldCoord.y < 0:
            quadrants[2] = True
        else:
            quadrants[3] = True

    flipSign = False
    if quadrants[2] and quadrants[3]:
        flipSign = True

    #print("quadrants=%s" % quadrants)
    #for i in range(0, len(uvs)):
    #    coord = uvs[i].uv
    #    print("uv %f %f" % (coord[0], coord[1]))

    minAngle = math.pi * 2
    maxAngle = -math.pi * 2
    minZ = 10000
    maxZ = -10000
    for vert in verts:
        worldCoord = obj.matrix_world * vert.co
        if worldCoord.z > maxZ:
            maxZ = worldCoord.z
        if worldCoord.z < minZ:
            minZ = worldCoord.z
        polar = XYToPolar(worldCoord.x, worldCoord.y)
        if flipSign and polar[0] < 0:
            polar[0] += math.pi * 2
        if polar[0] > maxAngle:
            maxAngle = polar[0]
        if polar[0] < minAngle:
            minAngle= polar[0]

    #print("minAngle=%f maxAngle=%f minZ=%f maxZ=%f" % 
    #    (minAngle, maxAngle, minZ, maxZ))

    for poly in data.polygons:
        uvIndexes = poly.loop_indices
        #print("vertices=%d uvs=%d" % (len(poly.vertices), len(uvIndexes)))
        for vertIndex, uvIndex in zip(poly.vertices, uvIndexes):
            vert = verts[vertIndex]
            worldCoord = obj.matrix_world * vert.co
            polar = XYToPolar(worldCoord.x, worldCoord.y)
            if flipSign and polar[0] < 0:
                polar[0] += math.pi * 2

            uvX = (polar[0] - minAngle) / (maxAngle - minAngle)
            uvY = (worldCoord.z - minZ) / (maxZ - minZ)
            if flipZ:
                uvY = 1.0 - uvY
            if flipX:
                uvX = 1.0 - uvX
                
            uvs[uvIndex].uv[0] = uvX
            uvs[uvIndex].uv[1] = uvY
    #dumpUVs(obj)



















