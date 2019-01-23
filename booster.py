# blender script to create big fucking booster
# apply to booster3.blend


import bpy, bmesh
import importlib
import bfs
importlib.reload(bfs)




bfs.deselect()
bfs.deleteObjectNamed("booster top")
bfs.deleteObjectNamed("booster bottom")
bfs.deleteObjectNamed("x1")
bfs.deleteObjectNamed("x2")
bfs.deleteObjectNamed("space1")
bfs.deleteObjectNamed("space2")
bfs.deleteObjectNamed("flag1")
bfs.deleteObjectNamed("flag2")
bfs.deleteObjectNamed("logo1")
bfs.deleteObjectNamed("logo2")



booster = bfs.selectByName("booster5")
booster.hide = True

bpy.ops.object.duplicate()
bpy.context.scene.objects.active = bfs.getSelected()[0]
bpy.context.scene.objects.active.hide = False
bpy.context.scene.objects.active.name = 'booster'
booster = bpy.context.scene.objects.active

xPlug = bfs.findObject('x plug')
x1 = bfs.cookieCut(booster, xPlug, "x1", "BMESH")

bfs.selectActivate(xPlug)
xPlug.location.x *= -1
# rotation applies the location change to matrix_world
bpy.ops.transform.rotate(value=bfs.toRad(180), axis=(0.0, 0.0, 1.0))

x2 = bfs.cookieCut(booster, xPlug, "x2", "BMESH")


bfs.selectActivate(xPlug)
bpy.ops.transform.rotate(value=bfs.toRad(180), axis=(0.0, 0.0, 1.0))
xPlug.location.x *= -1


spacePlug = bfs.findObject('space plug')
space1 = bfs.cookieCut(booster, spacePlug, "space1", "BMESH")

bfs.selectActivate(spacePlug)
bpy.ops.transform.translate(value=(-9.0, 0.0, 0.0))
space2 = bfs.cookieCut(booster, spacePlug, "space2", "BMESH")
bfs.selectActivate(spacePlug)
bpy.ops.transform.translate(value=(9.0, 0.0, 0.0))

flagPlug = bfs.findObject('flag plug')
flag1 = bfs.cookieCut(booster, flagPlug, "flag1", "BMESH")
bfs.selectActivate(flagPlug)
bpy.ops.transform.translate(value=(-9.0, 0.0, 0.0))
flag2 = bfs.cookieCut(booster, flagPlug, "flag2", "BMESH")
bfs.selectActivate(flagPlug)
bpy.ops.transform.translate(value=(9.0, 0.0, 0.0))





logoPlug = bfs.findObject('logo plug')
logo1 = bfs.cookieCut(booster, logoPlug, "logo1", "BMESH")
bfs.selectActivate(logoPlug)
bpy.ops.transform.translate(value=(-9.0, 0.0, 0.0))
logo2 = bfs.cookieCut(booster, logoPlug, "logo2", "BMESH")
bfs.selectActivate(logoPlug)
bpy.ops.transform.translate(value=(9.0, 0.0, 0.0))

# calculate UVs
bfs.cylinderUV(flag1, flipZ=True, flipX=True)
bfs.cylinderUV(flag2, flipZ=True, flipX=True)
bfs.cylinderUV(logo1, flipZ=True, flipX=True)
bfs.cylinderUV(logo2, flipZ=True, flipX=True)
bfs.cylinderUV(space1, flipZ=True, flipX=True)
bfs.cylinderUV(space2, flipZ=True, flipX=True)
bfs.cylinderUV(x1, flipZ=True, flipX=True)
bfs.cylinderUV(x2, flipZ=True, flipX=True)


# split booster in 2
fusePlug = bfs.findObject('fuse plug')
bottom_booster = bfs.cookieCut(booster, fusePlug, "booster bottom", "BMESH")
booster.name = "booster top"









