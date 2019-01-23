extends Camera


var bfr = null

func _ready():
    bfr = get_parent().find_node('bfr').find_node('rigid')
    
    
func _process(delta):
#    print("playerCam %f,%f,%f" % [follow_this.transform.origin.x, follow_this.transform.origin.y, follow_this.transform.origin.z])
    translation = bfr.transform.origin + Vector3(-100, 0, 100)
#    translation = bfr.transform.origin + Vector3(0, 0, 50)
    look_at(bfr.transform.origin + Vector3(0, 0, 0), Vector3(0, 1, 0))
