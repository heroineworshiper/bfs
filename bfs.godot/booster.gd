extends Spatial

var library = preload("library.gd").new()




# material to object mapping
var materials = [
    "booster_top", "res://assets/white.material",
    "booster_bottom", "res://assets/white.material",
    "heatshield_top", 'res://assets/heatshield.tres',
    "heatshield_bottom", 'res://assets/heatshield.tres',
    "bottom_dome_001", 'res://assets/heatshield.tres',
    "fin", 'res://assets/heatshield.tres',
    "fin_001", 'res://assets/heatshield.tres',
    "fin_002", 'res://assets/heatshield.tres',
    "fin_003", 'res://assets/heatshield.tres',
    "flag1", "res://assets/flag.tres",
    "flag2", "res://assets/flag.tres",
    "logo1", "res://assets/bfr_logo.tres",
    "logo2", "res://assets/bfr_logo.tres",
    "space1", "res://assets/space.tres",
    "space2", "res://assets/space.tres",
    "top_dome", 'res://assets/heatshield.tres',
    "x1", "res://assets/x.tres",
    "x2", "res://assets/x.tres"
]


func _ready():
    library.setMaterials(self, materials)


#func _process(delta):
#    # Called every frame. Delta is time since last frame.
#    # Update game logic here.
#    pass
