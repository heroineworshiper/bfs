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



var USE_KEYBOARD = false

# roll, pitch, yaw of the center engines in rads
var commanded_thrust_vector = Vector3()
# delayed thrust vector
var true_thrust_vector = Vector3()
# maximum deflection in rads
var MAX_VECTOR = library.toRad(10)
# maximum roll in rads
var MAX_ROLL = library.toRad(5)
# rate of keyboard input deflection in rads/second
var KEYBOARD_RATE = library.toRad(45)


# rate of gimbal in rads/second
var GIMBAL_RATE = library.toRad(45)
const TORQUE_DEADBAND = 0.005
const PITCH_TORQUE = 20000
const ROLL_TORQUE = 1000

# engine thrust 0-1
var commanded_throttle = 0.0
var prevEngineState = library.ENGINE_JOYSTICK_INIT


var grid_cam
var engine_cam
var player_cam

var grids = Array()
var grid_names = [
    'grid0',   # bottom right
    'grid1',   # top left
    'grid2',   # top right
    'grid3',   # bottom left
]

var prev_trigger = false


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
    grid_cam = get_parent().get_parent().find_node('grid_cam')
    engine_cam = get_parent().get_parent().find_node('engine_cam')
    player_cam = get_parent().get_parent().find_node('playerCam')
    sound.initFlames(self)

    # test vehicle domane rotations
    #rigid.rotate_z(PI / 2)

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
        -0.29,
        -0.54,
        -0.94,
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
            layerZ[currentLayer] - 29.0)
        
        
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


# joystick input
    if !USE_KEYBOARD:
        var joy_x = Input.get_joy_axis(0, JOY_ANALOG_LX)
        var joy_y = Input.get_joy_axis(0, JOY_ANALOG_LY)
        var joy_throttle = Input.get_joy_axis(0, JOY_AXIS_6)
        var joy_rocker = Input.get_joy_axis(0, JOY_AXIS_7)
        var joy_rudder = Input.get_joy_axis(0, JOY_AXIS_8)
        var joy_l2 = Input.is_joy_button_pressed(0, JOY_L2)
        var joy_r2 = Input.is_joy_button_pressed(0, JOY_R2)
        # share
        var joy_l3 = Input.is_joy_button_pressed(0, JOY_L3)
        # options
        var joy_r3 = Input.is_joy_button_pressed(0, JOY_R3)
        # marked L3 on joystick
        var joy_select = Input.is_joy_button_pressed(0, JOY_SELECT)
        # nothing
        var joy_start = Input.is_joy_button_pressed(0, JOY_START)
        # marked X on throttle
        var joy_circle = Input.is_joy_button_pressed(0, JOY_SONY_CIRCLE)
        # marked square on throttle
        var joy_x_button = Input.is_joy_button_pressed(0, JOY_SONY_X)
        # marked circle on throttle
        var joy_square = Input.is_joy_button_pressed(0, JOY_SONY_SQUARE)
        # L1 on joystick
        var joy_l = Input.is_joy_button_pressed(0, JOY_L)
        # trigger on joystick
        var joy_r = Input.is_joy_button_pressed(0, JOY_R)

# deploy grid fins
        if joy_r && !prev_trigger:
            prev_trigger = joy_r
            toggleGrids()
        elif !joy_r && prev_trigger:
            prev_trigger = joy_r


# change camera
        if joy_l2:
            grid_cam.make_current()
        elif joy_r2:
            engine_cam.make_current()
        elif joy_square:
            player_cam.make_current()

# combine the rocker & rudder
        if abs(joy_rocker) > abs(joy_rudder):
            joy_rudder = joy_rocker

        commanded_throttle = joy_throttle
        commanded_thrust_vector.x = -joy_x * MAX_VECTOR
        commanded_thrust_vector.y = -joy_y * MAX_VECTOR
        commanded_thrust_vector.z = joy_rudder * MAX_VECTOR

#        print("joy=%f, %f, %f, %f, %f" % [joy_x, joy_y, joy_throttle, joy_rocker, joy_rudder])

    else:

        var angle_step = KEYBOARD_RATE * delta
        var throttle_step = library.THROTTLE_RATE * delta





        # thrust vectoring
        if Input.is_action_pressed("ui_up"):
            commanded_thrust_vector.y += angle_step
        if Input.is_action_pressed("ui_down"):
            commanded_thrust_vector.y -= angle_step
        if Input.is_action_pressed("ui_left"):
            commanded_thrust_vector.z += angle_step
        if Input.is_action_pressed("ui_right"):
            commanded_thrust_vector.z -= angle_step
        if Input.is_action_pressed("ui_yaw_left"):
            commanded_thrust_vector.x += angle_step
        if Input.is_action_pressed("ui_yaw_right"):
            commanded_thrust_vector.x -= angle_step

        if Input.is_action_pressed("ui_center"):
            commanded_thrust_vector.x = 0
            commanded_thrust_vector.y = 0
            commanded_thrust_vector.z = 0

        if Input.is_action_pressed("ui_throttle_up"):
            commanded_throttle += throttle_step
        if Input.is_action_pressed("ui_throttle_down"):
            commanded_throttle -= throttle_step

        commanded_throttle = clamp(commanded_throttle, 0, 1)

        # roll
        commanded_thrust_vector.x = clamp(commanded_thrust_vector.x, -MAX_ROLL, MAX_ROLL)
        # pitch
        commanded_thrust_vector.y = clamp(commanded_thrust_vector.y, -MAX_VECTOR, MAX_VECTOR)
        # yaw
        commanded_thrust_vector.z = clamp(commanded_thrust_vector.z, -MAX_VECTOR, MAX_VECTOR)

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


#func _input(ev):
#    print("input type=%d" % typeof(ev))
#    if ev is InputEventJoypadMotion:










