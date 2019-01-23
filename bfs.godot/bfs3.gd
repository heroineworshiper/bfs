extends Spatial

var library = preload("library.gd").new()
var windows = Array()
export var TOTAL_WINDOWS = 101

# material to object mapping
var materials = [
    "bottom_fuse", "res://assets/white.material",
    "bottom_heatshield", "res://assets/heatshield.tres",
    "canard_flange1", "res://assets/heatshield.tres",
    "canard_flange2", "res://assets/heatshield.tres",
    "canard1", "res://assets/heatshield.tres",
    "canard2", "res://assets/heatshield.tres",
    "flag", "res://assets/flag.tres",
    "hatch1",  "res://assets/white.material",
    "hatch1_outline", "res://assets/black.tres",
    "hatch2", "res://assets/white.material",
    "hatch2_outline", "res://assets/black.tres",
    "pipes", "res://assets/heatshield.tres",
    "spacex", "res://assets/spacex.tres",
    "tank_rear", "res://assets/heatshield.tres",
    "top_dome",  "res://assets/white.material",
    "top_fuse", "res://assets/white.material",
    "top_heatshield", "res://assets/heatshield.tres",
    "wing_base3", "res://assets/heatshield.tres",
    "wing_base4", "res://assets/heatshield.tres",
    "wing_cylinder3", "res://assets/heatshield.tres",
    "wing_cylinder4", "res://assets/heatshield.tres",
    "wing2", "res://assets/white.material",
    "wing3", "res://assets/heatshield.tres",
    "wing4", "res://assets/heatshield.tres",
    "wing_heatshield", "res://assets/heatshield.tres",

]

func _ready():
    # Called when the node is added to the scene for the first time.
    # Initialization here.
    for i in range(0, TOTAL_WINDOWS):
        var node = find_node("window_" + str(i))
        windows.append(node)
        node.set_surface_material(0, load("res://assets/window.material"))
    library.setMaterials(self, materials)
    
    
    
#func _process(delta):
#    # Called every frame. Delta is time since last frame.
#    # Update game logic here.
#    pass
