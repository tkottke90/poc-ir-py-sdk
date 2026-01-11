#!python3
import irsdk
import argparse

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Switch iRacing camera to a specific group')
    parser.add_argument('group', type=int, help='Camera group number to switch to')
    args = parser.parse_args()

    # initializing ir and state
    ir = irsdk.IRSDK()
    ir.startup()

    try:
        ir.cam_switch_pos(group=args.group)

    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
