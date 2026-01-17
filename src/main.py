import argparse
from datetime import datetime
import time
import os
from server import ServerContext, start_server, handle_root, handle_driver, handle_camera, handle_set_camera, handle_toggle_pit_cams, handle_dashboard, handle_diagnostics, handle_driver_overlay_view
from iracing import State
from models.telemetry import TelemetryHandler, FileTelemetryHandler, LiveTelemetryHandler
from logger import setup_logger
from models.driver_info import DriverInfo

logger = setup_logger(console_output=False)
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
    print(f'Session Time:  {t:.4f}')
    print(f'Session Flags: {ir.decode_session_flags(f)} ({f})')
    print('')
    print(f'Lap:       {ir["Lap"]}')
    print(f'Race Laps: {ir["RaceLaps"]}')

def show_car_stats(driverInfo: DriverInfo, ir: TelemetryHandler):
    # State Boolean for car
    isOnTrack = ir['IsOnTrackCar']
    
    if not isOnTrack:
        print('')
        print('== Car Stats [OFF TRACK] ==')

        return
    
    print('')
    print('== Car Stats ==')
    i = ir['CarIdx']
    s = ir['CarIdxTrackSurface']

    print(f'Car Surface: {ir.decode_car_location(s)} ({s})')

def show_driver_stats(driver: DriverInfo, ir: TelemetryHandler):
    # State boolean for player
    isOnTrack = ir['IsOnTrack']

    if not isOnTrack:
        print('')
        print('== Player Stats [OFF TRACK] ==')

        return


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
    
    # Write Console Header
    print('iRacing Telemetry Monitor')
    print('========================')
    print('')
    # Show Current Date/Time
    print(f'Uptime: {datetime.now() - startTime}')
    print(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Connected: {state.ir_connected} [Type: {ir.name}]')
    print(f'Playback: {ir.get_playback_display()}')

    # on each tick we freeze buffer with live telemetry
    # it is optional, but useful if you use vars like CarIdxXXX
    # this way you will have consistent data from those vars inside one tick
    # because sometimes while you retrieve one CarIdxXXX variable
    # another one in next line of code could change
    # to the next iracing internal tick_count
    # and you will get incosistent data
    ir.freeze_var_buffer_latest()

    # == Driver Management ==
    driver = state.drivers

    # == Camera Management ==
    
    print('\n== Camera Management ==')
    ## Start by showing the camera in the header
    print(f'Camera: {state.current_camera(ir)}')
    
    ## Then we check if the target camera is on the player car
    ## because this means the stream is watching the player
    driverCarIdx = ir['PlayerCarIdx']
    camTargetIdx = ir['CamCarIdx']


    if camTargetIdx == driverCarIdx:
        player = driver.get_driver(driverCarIdx)
        
        print(f"Auto Camera: Yes")
        debug and print(f'Camera Target: Player/Team Car ({driverCarIdx} | {player.CarNumber})')
        state.set_camera_by_driver(player, ir)
    else:
        # If the camera is not on the player car, it is 
        # likely that the broadcast is doing something and we do not
        # want to interrupt that work.
        print(f"Auto Camera: No")
        debug and print(f'Camera Target: Other Car (Camera: {camTargetIdx}) | Player: {driverCarIdx})')

    # == Game Data Management ==
    print("\n== Game Data ==")
    print(f"Session: {ir['SessionNum']}\n")

    
    print(f"Lap: {ir['LapCompleted']} / {ir['RaceLaps']}")
    print(f"Driver: {driver.UserName} ({driver.CarNumber})")
    print(f"Incidents:")
    print(f"  Me: {ir['PlayerCarMyIncidentCount']}")
    print(f"  Driver: {ir['PlayerCarDriverIncidentCount']}")
    print(f"  Team: {ir['PlayerCarTeamIncidentCount']}")
    print(f"  Incidents: {ir['PlayerIncidents']}")
    print(f"Participation: {ir['Precipitation']}")
    print(f"Driver Change Laps: {ir['DCLapStatus']}")

    print(f"Pits:")
    print(f"  Open: {ir['PitsOpen']}")
    print(f"  On Pit Road: {state.driver_in_pits}")
    print(f"  Pitstop Active: {state.driver_in_stall}")
    print(f"  Pitstop Exit: {state.driver_exit_pits}")

    pitRepair = (ir['PitRepairLeft'] or 0) + (ir['PitOptRepairLeft'] or 0)

    print(f"  Pit Repair: {pitRepair} (Optional: {ir['PitOptRepairLeft']})")
    print(f"    Required: {ir['PitRepairLeft']}")
    print(f"    Optional: {ir['PitOptRepairLeft']}")

    if debug:
        show_session_stats(ir)
        
        show_car_stats(driver, ir)
        
        show_driver_stats(driver, ir)

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

    # Create API logger for HTTP endpoints
    api_logger = setup_logger('iracing.api', console_output=False)

    # Create server context with dependencies
    context = ServerContext(
        get_ir=lambda: ir,
        get_state=lambda: state,
        logger=api_logger
    )

    # Start HTTP Server with context
    http_server = start_server(
        endpoints={
            '/': handle_dashboard,
            '/driver-overlay': handle_driver_overlay_view,
            '/api': handle_root,
            '/api/driver': handle_driver,
            '/api/camera': handle_camera,
            '/api/camera/set': handle_set_camera,
            '/api/camera/toggle-pit-cams': handle_toggle_pit_cams,
            '/api/diagnostics': handle_diagnostics,
        },
        context=context,
        port=9000
    )

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
                # Check drivers to start
                state.check_drivers(ir)

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
        # shutting down HTTP server
        print('Shutting down HTTP server...')
        http_server.shutdown()

        # shutting down ir library
        ir.disconnect()
