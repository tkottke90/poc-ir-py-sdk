"""
HTTP Server module for iRacing telemetry API.
"""

from server.context import ServerContext
from server.server import start_server
from server.root import handle_root
from server.driver import handle_driver
from server.camera import handle_camera
from server.set_camera import handle_set_camera
from server.toggle_pit_cams import handle_toggle_pit_cams
from server.dashboard import handle_dashboard
from server.diagnostics import handle_diagnostics

__all__ = [
    'ServerContext',
    'start_server',
    'handle_root',
    'handle_driver',
    'handle_camera',
    'handle_set_camera',
    'handle_toggle_pit_cams',
    'handle_dashboard',
    'handle_diagnostics'
]
