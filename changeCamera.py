#!python3
import irsdk

# Startup the SDK
ir = irsdk.IRSDK()
ir.startup()

ir.cam_switch_pos(0, 1)
