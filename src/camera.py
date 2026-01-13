import json
from iracing import TelemetryHandler, FileTelemetryHandler


class CameraManager:
    
    def __init__(self, ir: TelemetryHandler):
        self.cameras = self.get_cameras(ir)
        self.current_camera = self.selected_camera(ir)
        self.last_camera = self.current_camera

        self.isNotUsed = isinstance(ir, FileTelemetryHandler)

    def document_cameras(self, ir: TelemetryHandler):
        """
        Creates a document from the current camera configuration
        """

        # Get the Weekend Headers
        weekend = ir['WeekendInfo']

        tId = weekend['TrackID']
        tName = weekend['TrackDisplayName']

        output = dict({
            'trackId': tId,
            'trackName': tName,
            'cameras': self.cameras
        })

        with open(f'camera_config_{tId}.json', 'w') as f:
            json.dump(self.cameras, f, indent=4)

        pass

    def refresh(self, ir: TelemetryHandler):
        if self.isNotUsed:
            return

        self.cameras = self.__get_cameras(ir)
        self.current_camera = self.__selected_camera(ir)

    def __get_cameras(self, ir: TelemetryHandler):
      if isinstance(ir, FileTelemetryHandler):
          return []

      return ir['CameraInfo']
    
    def __selected_camera(self, ir: TelemetryHandler):
      if isinstance(ir, FileTelemetryHandler):
          return 'Unused - Replay File'
      
      cameras = self.__get_cameras(ir)
      camId = ir['CamGroupNumber']

      if not cameras or not camId:
          return 'Unknown'
      
      current_camera = next((cam for cam in cameras['Groups'] if cam['GroupNum'] == camId), None)

      if current_camera:
          return current_camera['GroupName']
      
      return 'Unknown'

