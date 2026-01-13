from iracing import TelemetryHandler, FileTelemetryHandler


def get_cameras(ir: TelemetryHandler):
    if isinstance(ir, FileTelemetryHandler):
        return 'Unused - Replay File'

    return ir['CameraInfo']

def selected_camera(ir: TelemetryHandler):
    if isinstance(ir, FileTelemetryHandler):
        return 'Unused - Replay File'
    
    cameras = get_cameras(ir)
    camId = ir['CamGroupNumber']

    if not cameras or not camId:
        return 'Unknown'
    
    current_camera = next((cam for cam in cameras['Groups'] if cam['GroupNum'] == camId), None)

    if current_camera:
        return current_camera['GroupName']
    
    return 'Unknown'

