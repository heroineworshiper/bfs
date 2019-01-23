# blender script to create big fucking windows



import bpy, bmesh
import importlib
import bfs
importlib.reload(bfs)

# outer coordinates of the triangle windows
Z1 = 45.0
Z2 = 49.0
RADIUS1 = 3.2
RADIUS2 = 1.36125

# coordinates of the square centers
SQUARE_ANGLE1 = bfs.toRad(-70.0)
SQUARE_ANGLE2 = bfs.toRad(70.0)
SQUARE_Z1 = 36
SQUARE_Z2 = 44
SQUARE_RADIUS = 4
SQUARE_DEPTH = 1.5
SQUARE_ROWS = 6
SQUARE_COLUMNS = 8

SQUARE_W = .5
SQUARE_H = .5
PREFIX = "window_"

# limit of the boolean
TRI_W = 1.26
TRI_H = .7
TRI_RADIUS = 2.25
TRI_Z1 = 45.3
TRI_Z2 = 48.5
TRI_ROWS = 5
TRI_COLUMNS = 11
TRI_DEPTH = 2.5
TRI_ANGLE1 = bfs.toRad(-65.0)
TRI_ANGLE2 = bfs.toRad(65.0)


windows = []

def makeCube(angle, z, radius, number, xRotate):
    xy = bfs.polarToXY(angle, radius)
    cube = bpy.ops.mesh.primitive_cube_add(
        location=(xy[0], xy[1], z),
        rotation=(xRotate, 0.0, angle),
        radius=0.5)
    obj = bpy.context.object
    windows.append(obj)
    obj.name = PREFIX + str(number)
    return obj

def createSquare(angle, z, number):
    obj = makeCube(angle, z, SQUARE_RADIUS, number, 0)
    obj.scale = [ SQUARE_DEPTH, SQUARE_W, SQUARE_H ]
    # now bevel the edges
    bm = bfs.edit(obj)

    for edge in bm.edges:
        #print (str(edge.verts[0].co.x - edge.verts[1].co.x))
        if abs(edge.verts[0].co.x - edge.verts[1].co.x) > 0.5:
            edge.select = True
    bpy.ops.mesh.bevel(vertex_only=False, offset=0.1, segments=3)
    
    #bm.to_mesh(obj.data)
    bm.free()
    bpy.ops.object.mode_set(mode = 'OBJECT')


def calculateOverride(return_area = False):
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    if return_area: return region, rv3d, v3d, area
                    return {
                        'scene'  : bpy.context.scene,
                        'region' : region,
                        'area'   : area,
                        'space'  : v3d
                    }
    return {}

def createTriangle(angle, z, number, xRotate, row, column):
    if (row % 2) == 1:
        if xRotate > bfs.toRad(90):
            xRotate = 0
        else:
            xRotate = bfs.toRad(180)
            
    obj = makeCube(angle, z, TRI_RADIUS, number, xRotate)
    obj.scale = [ TRI_DEPTH, TRI_W, TRI_H ]

    # now define some edges
    bm = bfs.edit(obj)

    i = 0
    topRight = None
    topLeft = None
    bottomLeft = None
    bottomRight = None
    for edge in bm.edges:
        #print (str(edge.verts[0].co.x - edge.verts[1].co.x))
        if abs(edge.verts[0].co.x - edge.verts[1].co.x) > 0.5:
            i += 1
            if i == 1:
                bottomRight = edge
            if i == 2:
                topRight = edge
            if i == 3:
                bottomLeft = edge
            if i == 4:
                topLeft = edge

    # delete an edge
    topLeft.verts[0].select = True
    topLeft.verts[1].select = True
    bpy.ops.mesh.delete(type='VERT')
    bottomLeft.select = True
    topRight.select = True
    # make a new face
    bpy.ops.mesh.edge_face_add()
    # move the remaneing edge
    topRight.verts[0].co.y = 0
    topRight.verts[1].co.y = 0

    # narrow the bottom face
    bpy.ops.mesh.select_all(action='DESELECT')
    bottomRightVert = bottomRight.verts[1]
    bottomLeftVert = bottomLeft.verts[0]
    newW = TRI_W * (TRI_RADIUS - TRI_DEPTH / 2) / (TRI_RADIUS + TRI_DEPTH / 2)
    bottomRightVert.select = True
    bottomLeftVert.select = True
    bottomRightVert.co.y = newW / 2
    bottomLeftVert.co.y = -newW / 2
    
    # chop side windows in half
    if (row % 2) == 1:
        if column == 0:
            bottomLeft.verts[1].co.y = 0
            bottomLeft.verts[0].co.y = 0
        elif column == TRI_COLUMNS - 1:
            bottomRight.verts[1].co.y = 0
            bottomRight.verts[0].co.y = 0
    else:
        if column == 0:
            bottomRight.verts[1].co.y = 0
            bottomRight.verts[0].co.y = 0
        elif column == TRI_COLUMNS - 1:
            bottomLeft.verts[1].co.y = 0
            bottomLeft.verts[0].co.y = 0

    # subdivide
    bpy.ops.mesh.loopcut_slide(
        calculateOverride(),
        MESH_OT_loopcut = {
            "number_cuts":5,
            "smoothness"            : 0,     
            "falloff"               : 'SMOOTH',  # Was 'INVERSE_SQUARE' that does not exist
            "edge_index"            : 2,
            "mesh_select_mode_init" : (True, False, False)
        },
        TRANSFORM_OT_edge_slide = {
            "value"           : 0,
            "mirror"          : False, 
            "snap"            : False,
            "snap_target"     : 'CLOSEST',
            "snap_point"      : (0, 0, 0),
            "snap_align"      : False,
            "snap_normal"     : (0, 0, 0),
            "correct_uv"      : False,
            "release_confirm" : False
        }
    )

    bm.free()
    bpy.ops.object.mode_set(mode = 'OBJECT')

def createPlugs():
    windows.clear()
    windowNumber = 0
    for row in range(0, SQUARE_ROWS):
        for column in range(0, SQUARE_COLUMNS):
            createSquare(SQUARE_ANGLE1 + (SQUARE_ANGLE2 - SQUARE_ANGLE1) * column / (SQUARE_COLUMNS - 1), 
                SQUARE_Z1 + (SQUARE_Z2 - SQUARE_Z1) * row / (SQUARE_ROWS - 1), 
                windowNumber)
            windowNumber += 1


    for row in range(0, TRI_ROWS):
    #for row in range(0, 1):
        for column in range(0, TRI_COLUMNS):
        #for column in range(1, 2):
            # inset the front row
            if row < TRI_ROWS - 1 or \
                (column > 0 and column < TRI_COLUMNS - 1):
                xRotate = 0
                if (column % 2) == 0:
                    xRotate = bfs.toRad(180)
                createTriangle(TRI_ANGLE1 + (TRI_ANGLE2 - TRI_ANGLE1) * column / (TRI_COLUMNS - 1), 
                    TRI_Z1 + (TRI_Z2 - TRI_Z1) * row / (TRI_ROWS - 1), 
                    windowNumber, 
                    xRotate,
                    row,
                    column)
                windowNumber += 1

def createWindows():
    createPlugs()

    # combine them all into 1 object for the starting boolean
    bfs.deselect()
    for i in windows:
        i.select = True
    bpy.context.scene.objects.active = windows[0]
    windowPlug = windows[0]
    bpy.ops.object.join()
    windowPlug.name = 'window plug'
    #windowPlug.hide = True
    
    
    # this object becomes the fuse
    bfs.deselect()
    fuse = bfs.selectByName('top_fuse')
    bpy.ops.object.duplicate()
    
    # this object becomes the glass
    glass = bfs.getSelected()[0]
    glass.name = 'glass plug'

    # create the holes
    bfs.selectActivate(fuse)
    bool = fuse.modifiers.new(type="BOOLEAN", name="bool")
    bool.operation = 'DIFFERENCE'
    bool.object = windows[0]
    bool.solver = 'CARVE'
    bpy.ops.object.modifier_apply(modifier="bool")
    
    # boolean artifact
    # delete all vertices which coincide between the fuse & the windows
    bfs.deleteOverlap(fuse, windowPlug)
    
    # create glass plugs
    createPlugs()
    glass.hide = True
    
    
    # create glass objects.  Presort the delete vertices for deleteOverlap
    windowVerts = bfs.objToVerts(windowPlug)

    for i in range(0, len(windows)):
        window = windows[i]
        
        print("Creating %s" % window.name)
        bfs.selectActivate(window)
        bpy.context.scene.objects.active.data.use_auto_smooth = True
        bpy.context.scene.objects.active.data.show_double_sided = True
        bool = window.modifiers.new(type="BOOLEAN", name="bool")
        bool.operation = 'INTERSECT'
        bool.solver = 'CARVE'
        bool.object = glass
        bpy.ops.object.modifier_apply(modifier="bool")

        # boolean artifacts
        # delete all vertices which coincide between the windows & the plug
        bfs.deleteOverlap(window, windowPlug, windowVerts)

        # shift the window in along the radius
        bfs.deselect()
        polar = bfs.XYToPolar(window.location[0], window.location[1])
        polar[1] -= 0.02
        xy = bfs.polarToXY(polar[0], polar[1])
        window.location[0] = xy[0]
        window.location[1] = xy[1]

    # delete the joined window plug
    bfs.deleteObject(glass)
    bfs.deleteObject(windowPlug)

def deleteAll():
    bfs.deleteObjectNamed("glass")
    for i in range(0, 101):
        bfs.deleteObjectNamed(PREFIX + str(i))

