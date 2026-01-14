import time
from models.telemetry import TelemetryHandler, FileTelemetryHandler
from camera import CameraManager

class State:
    """
    The State class provides a container for the current state of the
    iRacing connection.  It is used to track connection status, camera
    information, and other stateful information.
    """

    def __init__(self):
        self.ir_connected = False
        self.last_car_setup_tick = -1

        self.camera_manager: CameraManager | None = None

        self.camera = None
        self.last_camera = None

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

        self.ir_connected = ir.connected;
        # print(f'irsdk connected: {self.ir_connected}')

    def current_camera(self, ir: TelemetryHandler):
        """
        Returns the currently active camera group name
        when connected to iRacing.  For replay files, returns 'Replay File'
        """

        if isinstance(ir, FileTelemetryHandler):
            # Not used for replays
            return 'Replay File'
        
        if not self.camera_manager:
            self.camera_manager = CameraManager(ir)

        self.camera = self.camera_manager.current_camera

        if not self.camera:
            return 'Unknown'

        return self.camera.name

    def set_next_tick(self):
        self.next_tick = time.time() + 1
