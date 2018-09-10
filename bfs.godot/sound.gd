var library = preload("library.gd").new()





var sound
var cutoffPlayer
const IDLE = 0
const STARTING = 1
const RUNNING = 2
var state = IDLE


var samples = [
    preload('res://assets/engine_start.wav'),
    preload('res://assets/engine_loop1.wav'),
    preload('res://assets/engine_transition1.wav'),
    preload('res://assets/engine_loop2.wav'),
    preload('res://assets/engine_transition2.wav'),
    preload('res://assets/engine_loop3.wav'),
    preload('res://assets/engine_transition3.wav')
]


func initFlames(parent):
    sound = parent.get_node('audio1')
    cutoffPlayer = parent.get_node('engineCutoff')
    # chain samples together
    sound.connect('finished', self, 'playbackFinished')

func startFlames():
    print('startFlames')
    state = STARTING
    sound.stream = samples[0]
    sound.play()
    return

func playbackFinished():
    match state:
        STARTING:
# transition from startup to loop
            print('playbackFinished STARTING')
            sound.stream = samples[1]
            sound.play()
            state = RUNNING
        RUNNING:
            print('playbackFinished RUNNING')
            sound.play()
    
    

func handleFlames(delta, commandedThrottle, currentThrottle):
    return


func handleCutoff():
    print('handleCutoff')
    sound.stop()
    cutoffPlayer.play()
    state = IDLE



