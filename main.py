import irsdk
import time
import os

# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

# function to decode session flags from binary
def decode_session_flags(flags):
    active_flags = []

    # Global flags
    if flags & irsdk.Flags.checkered:
        active_flags.append('CHECKERED')
    if flags & irsdk.Flags.white:
        active_flags.append('WHITE')
    if flags & irsdk.Flags.green:
        active_flags.append('GREEN')
    if flags & irsdk.Flags.yellow:
        active_flags.append('YELLOW')
    if flags & irsdk.Flags.red:
        active_flags.append('RED')
    if flags & irsdk.Flags.blue:
        active_flags.append('BLUE')
    if flags & irsdk.Flags.debris:
        active_flags.append('DEBRIS')
    if flags & irsdk.Flags.crossed:
        active_flags.append('CROSSED')
    if flags & irsdk.Flags.yellow_waving:
        active_flags.append('YELLOW_WAVING')
    if flags & irsdk.Flags.one_lap_to_green:
        active_flags.append('ONE_LAP_TO_GREEN')
    if flags & irsdk.Flags.green_held:
        active_flags.append('GREEN_HELD')
    if flags & irsdk.Flags.ten_to_go:
        active_flags.append('TEN_TO_GO')
    if flags & irsdk.Flags.five_to_go:
        active_flags.append('FIVE_TO_GO')
    if flags & irsdk.Flags.random_waving:
        active_flags.append('RANDOM_WAVING')
    if flags & irsdk.Flags.caution:
        active_flags.append('CAUTION')
    if flags & irsdk.Flags.caution_waving:
        active_flags.append('CAUTION_WAVING')

    # Driver black flags
    if flags & irsdk.Flags.black:
        active_flags.append('BLACK')
    if flags & irsdk.Flags.disqualify:
        active_flags.append('DISQUALIFY')
    if flags & irsdk.Flags.servicible:
        active_flags.append('SERVICIBLE')
    if flags & irsdk.Flags.furled:
        active_flags.append('FURLED')
    if flags & irsdk.Flags.repair:
        active_flags.append('REPAIR')

    # Start lights
    if flags & irsdk.Flags.start_hidden:
        active_flags.append('START_HIDDEN')
    if flags & irsdk.Flags.start_ready:
        active_flags.append('START_READY')
    if flags & irsdk.Flags.start_set:
        active_flags.append('START_SET')
    if flags & irsdk.Flags.start_go:
        active_flags.append('START_GO')

    return active_flags if active_flags else ['NONE']

# function to clear the terminal screen
def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')

# our main loop, where we retrieve data
# and do something useful with it
def loop():
    # clear the screen at the start of each loop
    clear_screen()

    # on each tick we freeze buffer with live telemetry
    # it is optional, but useful if you use vars like CarIdxXXX
    # this way you will have consistent data from those vars inside one tick
    # because sometimes while you retrieve one CarIdxXXX variable
    # another one in next line of code could change
    # to the next iracing internal tick_count
    # and you will get incosistent data
    ir.freeze_var_buffer_latest()

    # retrieve live telemetry data
    # check here for list of available variables
    # https://github.com/kutu/pyirsdk/blob/master/vars.txt
    # this is not full list, because some cars has additional
    # specific variables, like break bias, wings adjustment, etc
    t = ir['SessionTime']
    print('session time:', t)

    f = ir['SessionFlags']
    print('session flags (raw):', hex(f))
    print('session flags (decoded):', ', '.join(decode_session_flags(f)))

    # retrieve CarSetup from session data
    # we also check if CarSetup data has been updated
    # with ir.get_session_info_update_by_key(key)
    # but first you need to request data, before checking if its updated
    car_setup = ir['CarSetup']
    if car_setup:
        car_setup_tick = ir.get_session_info_update_by_key('CarSetup')
        if car_setup_tick != state.last_car_setup_tick:
            state.last_car_setup_tick = car_setup_tick
            print('car setup update count:', car_setup['UpdateCount'])
            # now you can go to garage, and do some changes with your setup
            # this line will be printed, only when you change something
            # and press apply button, but not every 1 sec
    # note about session info data
    # you should always check if data exists first
    # before do something like ir['WeekendInfo']['TeamRacing']
    # so do like this:
    # if ir['WeekendInfo']:
    #   print(ir['WeekendInfo']['TeamRacing'])

    # and just as an example
    # you can send commands to iracing
    # like switch cameras, rewind in replay mode, send chat and pit commands, etc
    # check pyirsdk.py library to see what commands are available
    # https://github.com/kutu/pyirsdk/blob/master/irsdk.py#L134 (class BroadcastMsg)
    # when you run this script, camera will be switched to P1
    # and very first camera in list of cameras in iracing
    # while script is running, change camera by yourself in iracing
    # and notice how this code changes it back every 1 sec
    ir.cam_switch_pos(0, 1)

if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                loop()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
