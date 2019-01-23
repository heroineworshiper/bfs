# the model being used when the rocket is lifting off


extends Node

var library = preload("library.gd").new()
var sound = preload("sound.gd").new()
var grid_deploy_sound
var grid_retract_sound



var booster_raptors = Array()

# the angles for the raptors, in radians.  Used to calculate roll vectoring
var booster_raptor_names = [
    'booster raptor0',
    'booster raptor1',
    'booster raptor2',
    'booster raptor3',
    'booster raptor4',
    'booster raptor5',
    'booster raptor6',
    'booster raptor7',
    'booster raptor8',
    'booster raptor9',
    'booster raptor10',
    'booster raptor11',
    'booster raptor12',
    'booster raptor13',
    'booster raptor14',
    'booster raptor15',
    'booster raptor16',
    'booster raptor17',
    'booster raptor18',
    'booster raptor19',
    'booster raptor20',
    'booster raptor21',
    'booster raptor22',
    'booster raptor23',
    'booster raptor24',
    'booster raptor25',
    'booster raptor26',
    'booster raptor27',
    'booster raptor28',
    'booster raptor29',
    'booster raptor30',
]



onready var rigid = get_node('rigid')
var bfs

# RUD states
const RUD_NONE = 0
const RUD_RUDDING = 1
var rud_state = RUD_NONE
var rud_time = 0.0
const RUD_TIME = 1.0

# roll, pitch, yaw of the center engines in rads
export var commanded_thrust_vector = Vector3()
# delayed thrust vector
var true_thrust_vector = Vector3()


# rate of gimbal in rads/second
var GIMBAL_RATE = library.toRad(45)
const TORQUE_DEADBAND = 0.005
const PITCH_TORQUE = 20000
const ROLL_TORQUE = 1000

# engine thrust 0-1
export var commanded_throttle = 0.0
var prevEngineState = library.ENGINE_JOYSTICK_INIT


# RUD

var grids = Array()
var grid_names = [
    'grid0',   # bottom right
    'grid1',   # top left
    'grid2',   # top right
    'grid3',   # bottom left
]


func tabulate_nodes(array, names):
    for i in range(0, names.size()):
        var node = find_node(names[i])
        array.append(node)


# get the highest state of any grid
func gridState():
    var highest = library.GRID_RETRACTED
    for i in range(0, grids.size()):
        if grids[i].state > highest:
            highest = grids[i].state
    return highest

func toggleGrids():
    var state = gridState()
    if state == library.GRID_RETRACTED:
        grid_deploy_sound.play()
        for i in range(0, grids.size()):
            grids[i].deploy()
    elif state == library.GRID_EXTENDED:
        grid_retract_sound.play()
        for i in range(0, grids.size()):
            grids[i].retract()




func _ready():
    # Called when the node is added to the scene for the first time.
    # Initialization here.
    sound.initFlames(self)

    # test vehicle domane rotations
    #rigid.rotate_z(PI / 2)

    bfs = find_node('ship3')

    tabulate_nodes(booster_raptors, booster_raptor_names)
    tabulate_nodes(grids, grid_names)
    grid_deploy_sound = grids[0].find_node('grid_deploy')
    grid_retract_sound = grids[0].find_node('grid_retract')

    # position the booster engines.  From booster_engines.FCMacro
    # radius of each layer in m
    var layerRadius = [
        4.1,
        3.1,
        1.4,
        0.0
    ]

    # Z of each layer in m
    var layerZ = [
        0,
        -0.3,
        -0.4,
        -0.5,
    ]

    # starting angle of each layer
    var layerAngle = [
        library.toRad(0.0),
        library.toRad(17.0),
        library.toRad(0.0),
        library.toRad(0.0)
    ]

    # engines in each layer
    var layerTotal = [
        12,
        12,
        6,
        1
    ]
    
    # engine in the current layer
    var currentEngine = 0
    var currentLayer = 0

    for i in range(0, booster_raptors.size()):
        # calculate its angle
        var angle = 0.0
        if layerTotal[currentLayer] > 1:
            angle = layerAngle[currentLayer] + \
                library.toRad(float(currentEngine) * 360.0 / layerTotal[currentLayer])
        booster_raptors[i].angle = angle
        
        # polar to XY
        var xyz = library.polarToXYZ(angle, 
            layerRadius[currentLayer], 
            layerZ[currentLayer] - 30.75)
        
        
        booster_raptors[i].translation = xyz
        booster_raptors[i].rotate_y(angle + PI)
        # reset the default transform
        booster_raptors[i].defaultTransform = booster_raptors[i].transform

        currentEngine = currentEngine + 1
        if currentEngine >= layerTotal[currentLayer]:
            currentLayer = currentLayer + 1
            currentEngine = 0
    
#    print("joy_guid=%s" % Input.get_joy_guid(0)) 






func _process(delta):
    handle_rud(delta)

# handle throttle
#    for i in range(24, 31):
    for i in range(0, 31):
        booster_raptors[i].setThrottle(commanded_throttle)

# gimbal the true thrust vector at its maximum rate
    var step = GIMBAL_RATE * delta
    true_thrust_vector.x = library.doGimbal(commanded_thrust_vector.x, true_thrust_vector.x, step)
    true_thrust_vector.y = library.doGimbal(commanded_thrust_vector.y, true_thrust_vector.y, step)
    true_thrust_vector.z = library.doGimbal(commanded_thrust_vector.z, true_thrust_vector.z, step)

    
    # move center engines
    #for i in range(24, 31):
    # looks brutal if they don't all pivot
    for i in range(0, 31):
        # reset the engine transformation
        booster_raptors[i].transform = booster_raptors[i].defaultTransform
        # apply pitch & yaw to X & Z axes
        var thrust_vector2 = Vector3(true_thrust_vector.y, 0, true_thrust_vector.z)
        
        # don't roll the center engine
        # roll direction is tangent of engine angle
        if i < 30:
            var angle2 = booster_raptors[i].angle + PI / 2
            thrust_vector2.x += true_thrust_vector.x * sin(angle2)
            thrust_vector2.z += true_thrust_vector.x * cos(angle2)

# don't gimbal if outer engines are on
        if(booster_raptors[0].currentThrottle > 0.1):
            thrust_vector2.x *= 0.5
            thrust_vector2.z *= 0.5
        booster_raptors[i].rotate_x(thrust_vector2.x)
        booster_raptors[i].rotate_z(thrust_vector2.z)

# handle engine sound based on 1 engine
    var refRaptor = booster_raptors[24]
# get out of joystick init
    if refRaptor.state != library.ENGINE_JOYSTICK_INIT && \
        prevEngineState == library.ENGINE_JOYSTICK_INIT:
        prevEngineState = refRaptor.state
        if refRaptor.state != library.ENGINE_OFF:
            sound.startFlames()
    elif refRaptor.state != library.ENGINE_OFF && \
        prevEngineState == library.ENGINE_OFF:
        sound.startFlames()
        prevEngineState = refRaptor.state
    elif refRaptor.state == library.ENGINE_OFF && \
        prevEngineState != library.ENGINE_OFF && \
        prevEngineState != library.ENGINE_JOYSTICK_INIT:
        prevEngineState = refRaptor.state
        sound.handleCutoff()
    elif refRaptor.state != library.ENGINE_OFF:
        sound.handleFlames(delta, 
            refRaptor.commandedThrottle, 
            refRaptor.currentThrottle)




# handle thrust
    var rotationMatrix = rigid.transform.basis.orthonormalized()
    if refRaptor.currentThrottle > library.MIN_THROTTLE:
        #print('impulse %f' % refRaptor.currentThrottle)
        var thrustVector = rotationMatrix * Vector3(0.0, 0.5 * refRaptor.currentThrottle, 0.0)
        rigid.apply_impulse(Vector3(0.0, 0.0, 0.0), 
            thrustVector)

# rotation rate in world domane
#    var rotationRate = rigid.get_angular_velocity()
#    var rotationDamping = -1000 * rotationRate
#    rigid.apply_torque_impulse(delta * rotationDamping)


# handle steering.  Important to set damping in the rigidbody fields.
#    print('%f, %f, %f' % [rigid.transform.origin.x,
#        rigid.transform.origin.y,
#        rigid.transform.origin.z])
    if rigid.transform.origin.y > 60:
# pitch
        if abs(commanded_thrust_vector.y) > TORQUE_DEADBAND:
            rigid.apply_torque_impulse(
                rotationMatrix * Vector3(-commanded_thrust_vector.y * delta * PITCH_TORQUE, 0, 0))

# yaw
        if abs(commanded_thrust_vector.z) > TORQUE_DEADBAND:
            rigid.apply_torque_impulse(
                rotationMatrix * Vector3(0, 0, -commanded_thrust_vector.z * delta * PITCH_TORQUE))

# roll 
        if abs(commanded_thrust_vector.x) > TORQUE_DEADBAND:
            rigid.apply_torque_impulse(
                rotationMatrix * Vector3(0, -commanded_thrust_vector.x * delta * ROLL_TORQUE, 0))


# vector the grid fins
    grids[0].commanded_angle = 0
    grids[1].commanded_angle = 0
    grids[2].commanded_angle = 0
    grids[3].commanded_angle = 0
    if abs(commanded_thrust_vector.y) > TORQUE_DEADBAND:
# pitch
        grids[0].commanded_angle -= library.toRad(4 * 45.0 * commanded_thrust_vector.y)
        grids[1].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.y)
        grids[2].commanded_angle -= library.toRad(4 * 45.0 * commanded_thrust_vector.y)
        grids[3].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.y)

    if abs(commanded_thrust_vector.z) > TORQUE_DEADBAND:
# yaw
        grids[0].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.z)
        grids[1].commanded_angle -= library.toRad(4 * 45.0 * commanded_thrust_vector.z)
        grids[2].commanded_angle -= library.toRad(4 * 45.0 * commanded_thrust_vector.z)
        grids[3].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.z)

    if abs(commanded_thrust_vector.x) > TORQUE_DEADBAND:
# roll
        grids[0].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.x)
        grids[1].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.x)
        grids[2].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.x)
        grids[3].commanded_angle += library.toRad(4 * 45.0 * commanded_thrust_vector.x)



# rapid unscheduled disassembly
func rud():
    print('single_stage.rud')
    if rud_state == RUD_NONE:
        rud_state = RUD_RUDDING
        rud_time = 0.0

    

func handle_rud(delta):
    if rud_state == RUD_RUDDING:
        rud_time += delta
        if rud_time < RUD_TIME: 
            for i in range(0, bfs.TOTAL_WINDOWS):
                bfs.windows[i].translate(Vector3(1.0 * rud_time / RUD_TIME, 0.0, 0.0))
        else:
            rud_state = RUD_NONE
        
    








