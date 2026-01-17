import time
from irsdk import IRSDK
from models.driver_info import Driver, DriverInfo
from models.telemetry import LiveTelemetryHandler, TelemetryHandler, FileTelemetryHandler
from camera import CameraManager

class State:
    """
    The State class provides a container for the current state of the
    iRacing connection.  It is used to track connection status, camera
    information, and other stateful information.
    """

    drivers: DriverInfo

    def __init__(self):
        self.ir_connected = False
        self.last_car_setup_tick = -1

        self.camera_manager: CameraManager | None = None

        self.camera = None
        self.last_camera = None

        self.driver_in_pits = False
        self.driver_in_stall = False
        self.driver_exit_pits = False

    # here we check if we are connected to iracing
    # so we can retrieve some data
    def check_iracing(self, ir: TelemetryHandler):
        if self.ir_connected and not ir.connected:
            self.ir_connected = False
            # don't forget to reset your State variables
            self.last_car_setup_tick = -1
            # we are shutting down ir library (clearing all internal variables)
            ir.disconnect()
            # print('irsdk disconnected')
        
        if not self.ir_connected:
            ir.connect()

        self.ir_connected = ir.connected

    def check_drivers(self, ir: TelemetryHandler):
        self.drivers = DriverInfo.from_iracing(ir)

    def current_camera(self, ir: TelemetryHandler):
        """
        Returns the currently active camera group name
        when connected to iRacing.  For replay files, returns 'Replay File'
        """

        if not isinstance(ir, LiveTelemetryHandler):
            # Not used for replays
            return 'Replay File'
        
        if not self.camera_manager:
            self.camera_manager = CameraManager(ir)

        self.camera = self.camera_manager.current_camera

        if not self.camera:
            return 'Unknown'

        return self.camera.name

    def current_camera_target(self, ir: TelemetryHandler):
        """
        Returns the currently active camera group target
        when connected to iRacing.  For replay files, returns 'Replay File'
        """

        if not isinstance(ir, LiveTelemetryHandler):
            # Not used for replays
            return 'Replay File'

        return self.camera_manager.current_camera.id

    def camera_groups(self, ir: TelemetryHandler):
        """
        Returns an array of available camera groups with their name and id.
        For replay files, returns an empty array.
        """

        if not isinstance(ir, LiveTelemetryHandler):
            # Not used for replays
            return []

        if not self.camera_manager:
            self.camera_manager = CameraManager(ir)

        return [{'id': group.id, 'name': group.name} for group in self.camera_manager.cameras]

    def set_camera_by_driver(self, driver: DriverInfo,ir: TelemetryHandler):
        """
        Docstring for set_camera_by_driver
        
        :param self: Description
        :param driver: Description
        :type driver: DriverInfo
        :param ir: Description
        :type ir: TelemetryHandler

        :returns: True if the camera was changed, False otherwise
        :rtype: bool
        """
        
        if not isinstance(ir, LiveTelemetryHandler):
            return # Not used for replays

        current_camera = self.current_camera(ir)

        # When enter pit rode, the state manager will not have detected yet
        # that the driver is in the pits.  We will want to update the camera
        # to the pit lane camera.
        if driver.driver_on_pit_road(ir) and not self.driver_in_pits:
            # Switch to Pit Lane 2
            self.driver_in_pits = True
            # Save the camera we were using before the pit stop so we can
            # return to it after the pit stop
            self.last_camera = current_camera
            ir.source.cam_switch_num(driver.CarNumber, 1)
            return True
        
        # Next the driver will go to the pit stall.  Here we will want to switch
        # to a pit stall camera to show a closeup
        if driver.driver_in_pit_stall(ir) and self.driver_in_pits and not self.driver_in_stall:
            # Switch to Pit Stall
            self.driver_in_stall = True
            ir.source.cam_switch_num(driver.CarNumber, 1)
            return True

        # After the pit stop is complete, we will want to go to the pit exit camera
        # to show the driver exiting the pits.  The drivers state goes from inPitStall back
        # to onPitRoad so we can detect this change in state.
        if self.driver_in_pits and self.driver_in_stall and not driver.driver_in_pit_stall(ir):
            # Switch to Pit Exit
            self.driver_exit_pits = True
            ir.source.cam_switch_num(driver.CarNumber, 1)
            return True

        # Once the driver is back on track, we will want to return to the camera
        # that was active before the pit stop.
        if driver.driver_on_track(ir) and self.driver_exit_pits:
            # Switch to last camera
            self.driver_in_pits = False
            self.driver_in_stall = False
            self.driver_exit_pits = False
            ir.source.cam_switch_num(driver.CarNumber, 1)
            return True
        
        return False

    def set_camera(self, cameraId: int, ir: TelemetryHandler):
        if not isinstance(ir, LiveTelemetryHandler):
            return # Not used for replays
        
        driverCarIdx = ir['PlayerCarNumber']

        ir.source.cam_switch_num(driverCarIdx, cameraId)
        return True

    def set_next_tick(self):
        self.next_tick = time.time() + 1
