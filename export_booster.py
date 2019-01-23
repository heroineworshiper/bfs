# export the big fucking booster



import bpy, bmesh
import importlib
import bfs
importlib.reload(bfs)

objects = [
    "booster top",
    "booster bottom",
    "heatshield top",
    "heatshield bottom",
    "bottom dome.001",
    "fin",
    "fin.001",
    "fin.002",
    "fin.003",
    "flag1",
    "flag2",
    "logo1",
    "logo2",
    "space1",
    "space2",
    "top dome",
    "x1",
    "x2"
    ]




bfs.selectList(objects)

bpy.ops.wm.collada_export(filepath=bfs.PATH + "assets/booster2.dae", 
    apply_modifiers=True,
    selected=True,
    triangulate=False)

    
    
    
    
    
    
    
    
    
    
    
