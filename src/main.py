import argparse
from datetime import datetime
import sys
import irsdk
import time
import os
from event_trackers import pit_monitor
from decoders.race_flags import decode_session_flags
from iracing import State, TelemetryHandler, LiveTelemetryHandler, FileTelemetryHandler
from logger import setup_logger
from camera import get_cameras

logger = setup_logger( console_output=False )
debug = False

lastCamera = None
startTime = datetime.now()

# function to clear the terminal screen
def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

def show_session_stats(ir: TelemetryHandler):
    print('')
    print('== Session Stats ==')
    t = ir['SessionTime']
    f = ir['SessionFlags']
    n = ir['SessionNum']
    s = ir['SessionState']

    print(f'Session State: {ir.decode_session_state(s)} ({s})')
    print(f'Session Time:  {t}')
    print(f'Session Flags: {ir.decode_session_flags(f)} ({f})')
    print('')
    print(f'Lap:       {ir["Lap"]}')
    print(f'Race Laps: {ir["RaceLaps"]}')

def show_car_stats(ir: TelemetryHandler):
    isOnTrack = ir['IsOnTrackCar']
    
    if not isOnTrack:
        print('')
        print('== Car Stats [OFF TRACK] ==')

        return
    
    print('')
    print('== Car Stats ==')
    s = ir['CarIdxTrackSurface']
    pits = pit_monitor.getPitStatus(ir)

    print(f'Car Surface: {ir.decode_car_location(s)} ({s})')

def show_driver_stats(ir: TelemetryHandler):
    isOnTrack = ir['IsOnTrack']
    isInGarage = ir['IsInGarage']

    print('')
    print('== Player Stats ==')
    p = ir['PlayerTrackSurface']
    
    print(f'Player Surface: {ir.decode_car_location(p)} ({p})')

    lapCompleted = ir['LapCompleted']
    lapDist = ir['LapDistPct']

    print('')
    print(f'On Track:      {isOnTrack}')
    print(f'Lap Completed: {lapCompleted} (+{lapDist:.2f}%)')
    
    i = ir['PlayerCarMyIncidentCount']
    iT = ir['PlayerCarDriverIncidentCount']

    print('')
    print(f'Incidents:       {i} (Team: {iT})')


# our main loop, where we retrieve data
# and do something useful with it
def loop(ir: TelemetryHandler, state: State):
    # clear the screen at the start of each loop
    clear_screen()
    
    # Get the next tick or session time
    next_tick = ir.get_next_tick()

    # Write Console Header
    print('iRacing Telemetry Monitor')
    print('========================')
    print('')
    # Show Current Date/Time
    print(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Connected: {state.ir_connected} [Type: {ir.name}]')
    print(f'Playback: {ir.get_playback_display()}')

    # Check Camera
    cameras = get_cameras(ir)

    print(f'Cameras: {cameras}')

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

    if debug:
        show_session_stats(ir)
        
        show_car_stats(ir)
        
        show_driver_stats(ir)

    # retrieve CarSetup from session data
    # we also check if CarSetup data has been updated
    # with ir.get_session_info_update_by_key(key)
    # but first you need to request data, before checking if its updated
    # car_setup = ir['CarSetup']
    # logger.debug('Loop:', extra={'car_setup': car_setup})
    # if car_setup:
    #     car_setup_tick = ir.get_session_info_update_by_key('CarSetup')
    #     if car_setup_tick != state.last_car_setup_tick:
    #         state.last_car_setup_tick = car_setup_tick
    #         print('car setup update count:', car_setup['UpdateCount'])
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
    # ir.cam_switch_pos(0, 1)

if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='iRacing telemetry parser and monitor')
    parser.add_argument('--file', help='Path to iRacing telemetry file (e.g., replay.ibt)')
    parser.add_argument('--debug', help='Enable debugging', action='store_true')
    parser.add_argument('--playback-speed',
                        type=str,
                        default='normal',
                        choices=['slow', 'normal', 'fast'],
                        help='Playback speed for IBT files. Default: normal')
    parser.add_argument('--skip',
                        type=float,
                        default=0.0,
                        help='Skip to position in replay (0.0 = start, 0.5 = middle, 1.0 = end). Default: 0.0')
    args = parser.parse_args()

    # Validate skip argument
    if not 0.0 <= args.skip <= 1.0:
        parser.error('--skip must be between 0.0 and 1.0')

    logger.debug('Setup: Arguments Parsed')

    # Initializing State
    state = State()
    debug = args.debug

    logger.debug('Setup: State Created')

    # initializing ir and state
    if args.file:
        print(f'Loading telemetry from file: {args.file}')
        print(f'Playback speed: {args.playback_speed}')
        if args.skip > 0.0:
            print(f'Skipping to: {args.skip * 100:.1f}% of replay')
        ir = FileTelemetryHandler(args.file, playback_speed=args.playback_speed, skip_to=args.skip)

        logger.info('FileTelemetryHandler: SessionTime', extra={'data': ir.ibt.get_all('SessionTime')})
        ir.connect()

        
    else:
        print('Connecting to live iRacing session...')
        ir = LiveTelemetryHandler()

    logger.debug('Setup: Telemetry Handler Created', extra={'file': args.file})

    try:
        retry = 0

        # application loop
        logger.debug('Setup: Starting Loop')
        while True:
            # check if we are connected to iracing
            logger.debug('Loop: Checking iRacing Connection')
            state.check_iracing(ir)
            # if we are, then process data
            if state.ir_connected:
                # Reset retry
                retry = 0

                # Loop over data
                logger.debug('Loop: iRacing Connected')
                loop(
                  ir = ir,
                  state = state
                )
            else:
                logger.debug('Loop: iRacing Not Connected')
                retry += 1
                if retry > 5:
                    raise Exception('Failed to connect to iRacing after 5 retries')
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(1)

    except KeyboardInterrupt:
        # press ctrl+c to exit
        print('User Triggered Shutdown....')
        pass
    
    except Exception as e:
        # catch any other exceptions
        print(f'Error: {e}')
        print('Unexpected Error, Shutting Down....')
    
    finally:
        # shutting down ir library
        ir.disconnect()
