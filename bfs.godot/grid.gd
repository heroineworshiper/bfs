extends Spatial

# rotation notes:
# x = 90 when level 
# y = -90 when fully extended 0 when retracted
# piston is 0, 0, 0 translation when retracted
#           -.24, 0, .24 when extended
# 4.700000, 0.000000, 0.000000

var library = preload("library.gd").new()
var grid
var grid_shaft
var grid_piston

var gridBasis
var rootBasis
var pistonOrigin

var state = library.GRID_RETRACTED
const DEPLOY_TIME = 1
var current_time = 0

var commanded_angle = library.toRad(0)
var current_angle = library.toRad(0)
const piston_retracted = Vector3(0.0, 0.0, 0.0)
const piston_deployed = Vector3(-.24, 0.0, .24)

func _ready():
    grid = find_node('grid')
    grid_shaft = find_node('grid_shaft')
    grid_piston = find_node('grid_piston')
    gridBasis = grid.transform.basis
    rootBasis = transform.basis
    pistonOrigin = grid_piston.transform.origin

func deploy():
    state = library.GRID_EXTENDING
    current_angle = commanded_angle
    current_time = 0
    return

func retract():
    state = library.GRID_RETRACTING
    current_time = 0
    return


func _process(delta):
    commanded_angle = library.clamp(commanded_angle, 
        library.toRad(-45), 
        library.toRad(45))
    current_angle = library.clamp(current_angle, 
        library.toRad(-45), 
        library.toRad(45))
    var step = library.toRad(90) * delta


    match state:
        library.GRID_EXTENDING:
            current_time += delta
            if current_time >= DEPLOY_TIME:
                current_time = DEPLOY_TIME
                state = library.GRID_EXTENDED
            grid.transform.basis = gridBasis
            transform.basis = rootBasis
            current_angle = library.doGimbal(commanded_angle, current_angle, step)
            
            var fraction = current_time / DEPLOY_TIME
            rotate_object_local(Vector3(1, 0, 0), current_angle * fraction)

            grid.rotate_y(library.toRad(-90 * fraction))
            grid_piston.transform.origin = fraction * piston_deployed

        library.GRID_EXTENDED:
            current_angle = library.doGimbal(commanded_angle, current_angle, step)
            transform.basis = rootBasis
            rotate_object_local(Vector3(1, 0, 0), current_angle)


        library.GRID_RETRACTING:
            current_time += delta
            if current_time >= DEPLOY_TIME:
                current_time = DEPLOY_TIME
                state = library.GRID_RETRACTED
            grid.transform.basis = gridBasis
            
            var fraction = 1.0 - current_time / DEPLOY_TIME
            transform.basis = rootBasis
            rotate_object_local(Vector3(1, 0, 0), current_angle * fraction)

            grid.rotate_y(library.toRad(-90 * fraction))
            grid_piston.transform.origin = piston_deployed * fraction
            if state == library.GRID_RETRACTED:
                current_angle = library.toRad(0)

    return





