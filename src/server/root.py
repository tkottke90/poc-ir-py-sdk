from .helpers import send_json_response
from .context import ServerContext


def handle_root(handler, ctx: ServerContext):
    """Handle root endpoint"""
    ctx.logger.debug('Root endpoint called')
    send_json_response(handler, {
        'service': 'iRacing Telemetry API',
        'version': '1.0',
        'endpoints': [
            '/ - HTML dashboard with live telemetry data',
            '/api - This endpoint (API information)',
            '/api/driver - Get current driver data (JSON)',
            '/api/camera - Get current camera info with available camera groups (JSON)',
            '/api/camera/set - Set camera group by ID (POST with camera_group_id)',
            '/api/diagnostics - Server diagnostics and context validation (JSON)'
        ]
    })