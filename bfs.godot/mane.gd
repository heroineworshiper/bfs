extends Node

var library = preload("library.gd").new()


var prev_trigger = false
var player
var grid_cam
var engine_cam
var player_cam
var ortho_cam

# camera being moved by the mouse
var mouse_cam

# positions
var mouse_current_position
var mouse_start_position
var cam_start_transform
var cam_start_rotation = Vector3(0.0, 0.0, 0.0)
var cam_start_position = Vector3(0.0, 0.0, 0.0)
var cam_offset_rotation = Vector3(0.0, 0.0, 0.0)
var cam_offset_position = Vector3(0.0, 0.0, 0.0)

# buttons
var middle_button = false
var shift_down = false
var ctrl_down = false

var MOUSE_TO_RADS = library.toRad(45) / 200
var MOUSE_TO_XY = 1.0 / 20
var MOUSE_TO_Z = 1.0 / 20

func _ready():
    player = find_node('BFR')
    grid_cam = find_node('grid_cam')
    engine_cam = find_node('engine_cam')
    player_cam = find_node('playerCam')
    ortho_cam = find_node('ortho_cam')
    mouse_cam = engine_cam
#    mouse_cam = player_cam
    cam_start_transform = mouse_cam.transform
    mouse_cam.make_current()


func apply_cam_offset():
    mouse_cam.transform = cam_start_transform
    mouse_cam.translate(cam_start_position + cam_offset_position)
    mouse_cam.rotate_x(cam_start_rotation.x + cam_offset_rotation.x)
    mouse_cam.rotate_y(cam_start_rotation.y + cam_offset_rotation.y)


func bake_cam_offset():
    mouse_start_position = mouse_current_position
    cam_start_position = cam_start_position + cam_offset_position
    cam_offset_position = Vector3(0.0, 0.0, 0.0)
    cam_start_rotation = cam_start_rotation + cam_offset_rotation
    cam_offset_rotation = Vector3(0.0, 0.0, 0.0)


func _process(delta):

# joystick input
    if !library.USE_KEYBOARD:
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
            player.toggleGrids()
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

        player.commanded_throttle = joy_throttle
        player.commanded_thrust_vector.x = -joy_x * library.MAX_VECTOR
        player.commanded_thrust_vector.y = -joy_y * library.MAX_VECTOR
        player.commanded_thrust_vector.z = joy_rudder * library.MAX_VECTOR

#        print("joy=%f, %f, %f, %f, %f" % [joy_x, joy_y, joy_throttle, joy_rocker, joy_rudder])

    else:

        var angle_step = library.KEYBOARD_RATE * delta
        var throttle_step = library.THROTTLE_RATE * delta





        # thrust vectoring
        if Input.is_action_pressed("ui_up"):
            player.commanded_thrust_vector.y += angle_step
        if Input.is_action_pressed("ui_down"):
            player.commanded_thrust_vector.y -= angle_step
        if Input.is_action_pressed("ui_left"):
            player.commanded_thrust_vector.z += angle_step
        if Input.is_action_pressed("ui_right"):
            player.commanded_thrust_vector.z -= angle_step
        if Input.is_action_pressed("ui_yaw_left"):
            player.commanded_thrust_vector.x += angle_step
        if Input.is_action_pressed("ui_yaw_right"):
            player.commanded_thrust_vector.x -= angle_step

        if Input.is_action_pressed("ui_center"):
            player.commanded_thrust_vector.x = 0
            player.commanded_thrust_vector.y = 0
            player.commanded_thrust_vector.z = 0

        if Input.is_action_pressed("ui_throttle_up"):
            player.commanded_throttle += throttle_step
        if Input.is_action_pressed("ui_throttle_down"):
            player.commanded_throttle -= throttle_step

        player.commanded_throttle = clamp(player.commanded_throttle, 0, 1)

        # roll
        player.commanded_thrust_vector.x = clamp(player.commanded_thrust_vector.x, -library.MAX_ROLL, library.MAX_ROLL)
        # pitch
        player.commanded_thrust_vector.y = clamp(player.commanded_thrust_vector.y, -library.MAX_VECTOR, library.MAX_VECTOR)
        # yaw
        player.commanded_thrust_vector.z = clamp(player.commanded_thrust_vector.z, -library.MAX_VECTOR, library.MAX_VECTOR)


# keyboard input
    if Input.is_action_pressed("ui_cancel"):
        get_tree().quit()
    if Input.is_action_pressed("ui_select"):
        player.rud()
        
        
        

# mouse input
    if Input.is_mouse_button_pressed(BUTTON_MIDDLE):
        mouse_current_position = get_viewport().get_mouse_position()  
        if !middle_button:
            middle_button = true
            bake_cam_offset()


# in XY mode
        if Input.is_action_pressed("ui_shift"):
            if !shift_down:
                shift_down = true
                bake_cam_offset()

            var x_offset = cos(-cam_start_rotation.y) * (mouse_current_position.x - mouse_start_position.x) * MOUSE_TO_XY
            var z_offset = sin(-cam_start_rotation.y) * (mouse_current_position.x - mouse_start_position.x) * MOUSE_TO_XY
            cam_offset_position = Vector3(x_offset,
                    (mouse_current_position.y - mouse_start_position.y) * MOUSE_TO_XY,
                    z_offset)
            print("cam_offset_position=%f,%f" % [cam_offset_position.x, cam_offset_position.z])
            apply_cam_offset()

        else:
            if shift_down:
                shift_down = false
                bake_cam_offset()

# in Z mode
            if Input.is_action_pressed("ui_ctrl"):
                if !ctrl_down:
                    ctrl_down = true
                    bake_cam_offset()

                
                var x_offset = sin(cam_start_rotation.y) * -(mouse_current_position.y - mouse_start_position.y) * MOUSE_TO_XY
                var z_offset = cos(cam_start_rotation.y) * -(mouse_current_position.y - mouse_start_position.y) * MOUSE_TO_XY
                cam_offset_position = Vector3(x_offset, 
                        0.0,
                        z_offset)
                apply_cam_offset()

            else:
                if ctrl_down:
                    ctrl_down = false
                    bake_cam_offset()

# in rotate mode
                mouse_cam.transform = cam_start_transform
                cam_offset_rotation = Vector3(-(mouse_current_position.y - mouse_start_position.y) * MOUSE_TO_RADS,
                    -(mouse_current_position.x - mouse_start_position.x) * MOUSE_TO_RADS,
                    0.0)
                apply_cam_offset()



    else:
        if middle_button:
            middle_button = false
            bake_cam_offset()
        if ctrl_down:
            ctrl_down = false
        if shift_down:
            shift_down = false




