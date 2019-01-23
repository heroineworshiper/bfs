# blender script to create big fucking ship
# apply to bfs6.blend


import bpy, bmesh
import importlib
import bfs
importlib.reload(bfs)
import windows
importlib.reload(windows)
import math


# shift objects in along the radius
def shiftPolar(obj):
    polar = bfs.XYToPolar(obj.location[0], obj.location[1])
    polar[1] -= 0.02
    xy = bfs.polarToXY(polar[0], polar[1])
    obj.location[0] = xy[0]
    obj.location[1] = xy[1]

    
    
# delete previous run
bfs.deselect()
windows.deleteAll()

deletedObjs = [
    "bottom_fuse",
    "bottom_heatshield",
    "canard2",
    "canard flange2",
    "flag",
    "hatch1",
    "hatch1_outline",
    "hatch2",
    "hatch2_outline",
    "spacex",
    "top_fuse",
    "top_heatshield",
    "wing2",
    "wing3",
    "wing4",
    "wing base",
    "wing base3",
    "wing base4",
    "wing cylinder3",
    "wing cylinder4",
    "wing_heatshield",
]

bfs.deleteObjectsNamed(deletedObjs)






# create the fuse mesh
print("Creating fuse")
obj = bfs.duplicateByName('top_fuse', 'fuse path')
bpy.context.scene.objects.active.hide = False
bpy.ops.object.convert(target='MESH')
bpy.ops.object.modifier_apply(apply_as='DATA')
bpy.context.scene.objects.active.data.use_auto_smooth = True
bpy.context.scene.objects.active.data.show_double_sided = True
top_fuse = bpy.context.scene.objects.active

print("Creating windows")
windows.createWindows()


# create canard

obj = bfs.duplicateByName("canard2", "canard1")
bpy.ops.transform.mirror(constraint_axis=(False, True, False), constraint_orientation='GLOBAL')
bpy.ops.transform.translate(value=(0.0, 3.43207 * 2, 0.0))


obj = bfs.duplicateByName("canard flange2", "canard flange1")
bpy.ops.transform.rotate(value=bfs.toRad(-18.1), axis=(1.0, 0.0, 0.0))
bpy.ops.transform.mirror(constraint_axis=(False, True, False), constraint_orientation='GLOBAL')
bpy.ops.transform.rotate(value=bfs.toRad(-18.1), axis=(1.0, 0.0, 0.0))


# create wings
obj = bfs.duplicateByName("wing base3", "wing base2")
obj.hide = False
r = obj.matrix_world[0][3]
bpy.ops.transform.rotate(value=bfs.toRad(-120.0), axis=(0.0, 0.0, 1.0))
bpy.ops.transform.translate(value=(-r + r * math.cos(bfs.toRad(-120)), 
    r * math.sin(bfs.toRad(-120)), 0.0))

obj = bfs.duplicateByName("wing base4", "wing base2")
obj.hide = False
r = obj.matrix_world[0][3]
bpy.ops.transform.rotate(value=bfs.toRad(120.0), axis=(0.0, 0.0, 1.0))
bpy.ops.transform.translate(value=(-r + r * math.cos(bfs.toRad(120)), 
    r * math.sin(bfs.toRad(120)), 0.0))

obj = bfs.duplicateByName("wing cylinder3", "wing cylinder")
obj.hide = False
r = obj.matrix_world[0][3]
bpy.ops.transform.rotate(value=bfs.toRad(-120.0), axis=(0.0, 0.0, 1.0))
bpy.ops.transform.translate(value=(-r + r * math.cos(bfs.toRad(-120)), 
    r * math.sin(bfs.toRad(-120)), 0.0))

obj = bfs.duplicateByName("wing cylinder4", "wing cylinder")
obj.hide = False
r = obj.matrix_world[0][3]
bpy.ops.transform.rotate(value=bfs.toRad(120.0), axis=(0.0, 0.0, 1.0))
bpy.ops.transform.translate(value=(-r + r * math.cos(bfs.toRad(120)), 
    r * math.sin(bfs.toRad(120)), 0.0))

obj = bfs.duplicateByName("wing3", "wing")
obj.hide = False
r = obj.matrix_world[0][3]
bpy.ops.transform.rotate(value=bfs.toRad(-120.0), axis=(0.0, 0.0, 1.0))
bpy.ops.transform.translate(value=(-r + r * math.cos(bfs.toRad(-120)), 
    r * math.sin(bfs.toRad(-120)), 0.0))

obj = bfs.duplicateByName("wing4", "wing")
obj.hide = False
r = obj.matrix_world[0][3]
bpy.ops.transform.rotate(value=bfs.toRad(120.0), axis=(0.0, 0.0, 1.0))
bpy.ops.transform.translate(value=(-r + r * math.cos(bfs.toRad(120)), 
    r * math.sin(bfs.toRad(120)), 0.0))



print("Creating cutouts")
hatch1_outline = bfs.cookieCut(top_fuse, bfs.findObject("hatch1 plug"), "hatch1_outline")
hatch2_outline = bfs.cookieCut(top_fuse, bfs.findObject("hatch2 plug"), "hatch2_outline")
hatch1_inner = bfs.cookieCut(hatch1_outline, bfs.findObject("hatch1 plug.001"), "hatch1")
hatch2_inner = bfs.cookieCut(hatch2_outline, bfs.findObject("hatch2 plug.001"), "hatch2")
# move hatches in
shiftPolar(hatch1_outline);
shiftPolar(hatch2_outline);
shiftPolar(hatch1_inner);
shiftPolar(hatch2_inner);


flag = bfs.cookieCut(top_fuse, bfs.findObject("flag plug"), "flag")
spacex = bfs.cookieCut(top_fuse, bfs.findObject("spacex plug"), "spacex")
bfs.cylinderUV(spacex)
top_heatshield = bfs.cookieCut(top_fuse, bfs.findObject("heatshield plug"), "top_heatshield")

bottom_fuse = bfs.cookieCut(top_fuse, bfs.findObject("tank plug"), "bottom_fuse")
bottom_heatshield = bfs.cookieCut(top_heatshield, bfs.findObject("tank plug"), "bottom_heatshield")

wing_base = bfs.duplicateByName('wing temp', 'wing base1')
wing2 = bfs.duplicateByName('wing2', 'wing')
wing_base.hide = False
wing2.hide = False
wing_base.select = True
bpy.ops.object.join()


wing_heatshield = bfs.cookieCut(wing2, bfs.findObject("heatshield plug2"), "wing_heatshield")



# apply thickness to fuse
bfs.thickness(top_fuse, 0.04)
bfs.thickness(top_heatshield, 0.04)
bfs.thickness(bottom_fuse, 0.04)
bfs.thickness(bottom_heatshield, 0.04)

# calculate UVs
bfs.cylinderUV(flag)
bfs.cylinderUV(spacex)



