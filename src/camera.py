import json
from iracing import TelemetryHandler, FileTelemetryHandler

class iRacingCamera:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class iRacingCameraGroup:
    def __init__(self, id: int, name: str, cameras: list[iRacingCamera] = []):
        self.id = id
        self.name = name
        self.cameras = cameras

    def add_camera(self, camera: iRacingCamera):
        self.cameras.append(camera)

    def from_config(config: dict):
        group = iRacingCameraGroup(config['id'], config['name'])

        for camera in config['cameras']:
            group.add_camera(iRacingCamera(camera['id'], camera['name']))
        
        return group

class CameraManager:
    def __init__(self, ir: TelemetryHandler):
        self.cameras = self.__get_cameras(ir)
        self.current_camera = self.__selected_camera(ir)
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
            json.dump(output, f, indent=4)

        pass

    def refresh(self, ir: TelemetryHandler):
        if self.isNotUsed:
            return

        self.cameras = self.__get_cameras(ir)
        self.current_camera = self.__selected_camera(ir)

    def __get_cameras(self, ir: TelemetryHandler) -> list[iRacingCameraGroup]:
      if isinstance(ir, FileTelemetryHandler):
          return []

      return iRacingCameraGroup.from_config(ir['CameraInfo'])
    
    def __selected_camera(self, ir: TelemetryHandler) -> iRacingCameraGroup | None:
      if isinstance(ir, FileTelemetryHandler):
          return None
      
      cameras = self.__get_cameras(ir)
      camId = ir['CamGroupNumber']

      if not cameras or not camId:
          return None
      
      current_camera = next((cam for cam in cameras if cam.id == camId), None)

      if current_camera:
          return current_camera
      
      return None

