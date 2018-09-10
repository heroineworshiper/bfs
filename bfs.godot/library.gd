
# rate of throttle change per second
export var THROTTLE_RATE = 0.75

# shutdown with hysterisis
export var CUTOFF_THROTTLE1 = 0.25
export var CUTOFF_THROTTLE2 = 0.15
# min to produce thrust
export var MIN_THROTTLE = 0.5

# engine states
const ENGINE_JOYSTICK_INIT = -1
const ENGINE_OFF = 0
const ENGINE_STARTING1 = 1
const ENGINE_STARTING2 = 2
const ENGINE_RUNNING = 3
const ENGINE_SHUTDOWN1 = 4
const ENGINE_SHUTDOWN2 = 5


# grid states
const GRID_RETRACTED = 0
const GRID_EXTENDING = 1
const GRID_EXTENDED = 2
const GRID_RETRACTING = 3

    
func toRad(angle):
    return angle * PI * 2.0 / 360.0


# swap y & z
func polarToXYZ(angle, radius, y):
    var x = radius * cos(angle)
    var z = -radius * sin(angle)
    return Vector3(x, y, z)



func clamp(angle, min_, max_):
    if angle < min_:
        return min_
    if angle > max_:
        return max_
    return angle

    
func doGimbal(target, current, step):
    if current < target:
        current += step
        if current > target:
            current = target
    elif current > target:
        current -= step
        if current < target:
            current = target
    return current



