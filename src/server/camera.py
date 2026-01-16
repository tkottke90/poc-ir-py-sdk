from .helpers import send_json_response, send_error_response
from .context import ServerContext
from datetime import datetime


def handle_camera(handler, ctx: ServerContext):
    """Handle camera info endpoint"""
    try:
        # Get current values on demand using context
        ir = ctx.ir
        state = ctx.state

        ctx.logger.debug('Camera endpoint called')

        if not state.ir_connected:
            ctx.logger.warning('Camera endpoint called but not connected to iRacing')
            send_error_response(handler, 'Not connected to iRacing', 503)
            return

        response = {
            'current_camera': state.current_camera(ir),
            'camera_target': state.current_camera_target(ir),
            'timestamp': datetime.now().isoformat()
        }

        ctx.logger.info(f'Camera data returned: {response["current_camera"]}')
        send_json_response(handler, response)

    except Exception as e:
        ctx.logger.error(f'Error in camera endpoint: {e}')
        send_error_response(handler, str(e))