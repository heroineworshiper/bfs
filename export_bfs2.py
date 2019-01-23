# blender script to export the BFS

# your job: export as a GLTF with SELECTED ONLY selected


import bpy



objects = [
        bpy.data.objects['canard flange'], 
        bpy.data.objects['canard1'], 
        bpy.data.objects['canard2'], 
        bpy.data.objects['fuse bottom'], 
        bpy.data.objects['fuse top vertical wing'], 
        bpy.data.objects['glass'], 
        bpy.data.objects['vertical wing'], 
        bpy.data.objects['vertical wing heatshield'], 
        bpy.data.objects['wing edge.001'], 
        bpy.data.objects['wing edge.002'], 
        bpy.data.objects['wing.001'], 
        bpy.data.objects['wing.002']
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



deselect()
select(objects)














