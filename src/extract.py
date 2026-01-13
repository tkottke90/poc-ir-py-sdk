import irsdk
from camera import CameraManager

if __name__ == '__main__':
    
  ir = irsdk.IRSDK()
  ir.startup()

  cm = CameraManager(ir)

  cm.document_cameras()

