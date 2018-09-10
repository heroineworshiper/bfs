# failed 2 stage model




extends Node

var library = preload("library.gd").new()
var sound = preload("sound.gd").new()


var ship_raptors = Array()
var ship_raptor_names = [
    'ship raptor0', 
    'ship raptor1', 
    'ship raptor2', 
    'ship raptor3', 
    'ship raptor4', 
    'ship raptor5'
]


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

onready var booster = get_node('booster')



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
const TORQUE_FACTOR = 100
var torque_accum = Vector3()
var want_rates = Vector3()

# engine thrust 0-1
var commanded_throttle = 0.0
var prevEngineState = library.ENGINE_OFF

var camera1
var camera2

var grids = Array()
var grid_names = [
    'grid0',
    'grid1',
    'grid2',
    'grid3',
]


var ship_raptor_positions = [
    Vector3(0, 1.8, 0.82),
    Vector3(0, 1.8, -0.82),
    Vector3(2, 3.75, 2),
    Vector3(-2, 3.75, 2),
    Vector3(-2, 3.75, -2),
    Vector3(2, 3.75, -2),
]


func tabulate_nodes(array, names):
    for i in range(0, names.size()):
        var node = find_node(names[i])
        array.append(node)

#func apply_torque(want, accum, index):
#    var step = 0
#    if want != 0:
#        if want > accum:
#            step = 100
#            if accum + step > want:
#                step = want - accum
#        elif want < accum:
#            step = -100
#            if accum + step < want:
#                step = want - accum
#    return step




func _ready():
    # Called when the node is added to the scene for the first time.
    # Initialization here.
    camera1 = get_parent().get_parent().find_node('Camera2')
    camera2 = get_parent().get_parent().find_node('Camera3')
    sound.initFlames(self)



    tabulate_nodes(ship_raptors, ship_raptor_names)
    tabulate_nodes(booster_raptors, booster_raptor_names)
    tabulate_nodes(grids, grid_names)

    # position the ship engines
    for i in range(0, ship_raptors.size()):
        var raptor = ship_raptors[i]
        
        raptor.translation = ship_raptor_positions[i] - Vector3(0, 24, 0)
        
        if(i >= 2):
            var sea_nozzle = raptor.find_node('seaNozzle')
            var vacuum_nozzle = raptor.find_node('vacuumNozzle')
            sea_nozzle.hide()
            vacuum_nozzle.show()
        
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

# change camera
#        if joy_l2:
#            camera1.make_current()
#        elif joy_r2:
#            camera2.make_current()

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
    for i in range(24, 31):
        # reset the engine transformation
        booster_raptors[i].transform = booster_raptors[i].defaultTransform
        # apply pitch & yaw to X & Z axes
        var thrust_vector2 = Vector3(true_thrust_vector.y, 0, true_thrust_vector.z)
        
        
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
    if refRaptor.state != library.ENGINE_OFF && \
        prevEngineState == library.ENGINE_OFF:
        sound.startFlames()
        prevEngineState = booster_raptors[24].state
    elif refRaptor.state == library.ENGINE_OFF && \
        prevEngineState != library.ENGINE_OFF:
        prevEngineState = booster_raptors[24].state
        sound.handleCutoff()
    elif refRaptor.state != library.ENGINE_OFF:
        sound.handleFlames(delta, 
            refRaptor.commandedThrottle, 
            refRaptor.currentThrottle)




# handle thrust
    if refRaptor.currentThrottle > library.MIN_THROTTLE:
        #print('impulse %f' % refRaptor.currentThrottle)
        var thrustVector = Vector3(0.0, 0.5 * refRaptor.currentThrottle, 0.0)
        booster.apply_impulse(Vector3(0.0, 0.0, 0.0), 
            thrustVector)

    #print('rotation=%f,%f,%f' % [booster.rotation.x, booster.rotation.y, booster.rotation.z])


# handle steering
#    var step = apply_torque(-true_thrust_vector.y * 100, 
#        torque_accum.y, 
#        0)
#    booster.apply_torque_impulse(
#            Vector3(-true_thrust_vector.y * delta * TORQUE_FACTOR, 0, 0))
#    if true_thrust_vector.z != 0:
#        booster.apply_torque_impulse(
#            Vector3(0, 0, -true_thrust_vector.z * delta * TORQUE_FACTOR))
#    if true_thrust_vector.x != 0:
#        booster.apply_torque_impulse(
#            Vector3(0, -true_thrust_vector.x * delta * TORQUE_FACTOR, 0))
    


#func _input(ev):
#    print("input type=%d" % typeof(ev))
#    if ev is InputEventJoypadMotion:










