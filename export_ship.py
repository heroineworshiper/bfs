# export the big fucking ship



import bpy, bmesh
import importlib
import bfs
importlib.reload(bfs)

objects = [
    "bottom_fuse",
    "bottom_heatshield",
    "canard flange1",
    "canard flange2",
    "canard1",
    "canard2",
    "flag",
    "hatch1",
    "hatch1_outline",
    "hatch2",
    "hatch2_outline",
    "pipes",
    "spacex",
    "tank rear",
    "top dome",
    "top_fuse",
    "top_heatshield",
    "wing base3",
    "wing base4",
    "wing cylinder3",
    "wing cylinder4",
    "wing2",
    "wing3",
    "wing4",
    "wing_heatshield"
    ]




bfs.selectList(objects)
for i in range(0, 101):
    bfs.findObject("window_" + str(i)).select = True
    

bpy.ops.wm.collada_export(filepath=bfs.PATH + "assets/bfs5.dae", 
    apply_modifiers=True,
    selected=True,
    triangulate=False)


    
    
    
    
    
    
    
    
    
    
    
