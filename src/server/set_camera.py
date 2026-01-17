import json
from .helpers import send_json_response, send_error_response
from .context import ServerContext
from datetime import datetime


def handle_set_camera(handler, ctx: ServerContext):
    """Handle set camera endpoint - accepts POST with camera group ID"""
    try:
        # Get current values on demand using context
        ir = ctx.ir
        state = ctx.state

        ctx.logger.debug('Set camera endpoint called')

        if not state.ir_connected:
            ctx.logger.warning('Set camera endpoint called but not connected to iRacing')
            send_error_response(handler, 'Not connected to iRacing', 503)
            return

        # Read POST data
        content_length = int(handler.headers.get('Content-Length', 0))
        if content_length == 0:
            send_error_response(handler, 'No data provided', 400)
            return

        post_data = handler.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            send_error_response(handler, 'Invalid JSON', 400)
            return

        # Validate camera_group_id
        if 'camera_group_id' not in data:
            send_error_response(handler, 'Missing camera_group_id parameter', 400)
            return

        camera_group_id = data['camera_group_id']
        
        # Validate it's an integer
        try:
            camera_group_id = int(camera_group_id)
        except (ValueError, TypeError):
            send_error_response(handler, 'camera_group_id must be an integer', 400)
            return

        # Get the driver car number
        driver = state.drivers.get_driver(ir['PlayerCarIdx'])

        if driver is None:
            send_error_response(handler, 'Driver not found', 404)
            return

        # Call set_camera method
        result = state.set_camera(driver.car_number_int(), camera_group_id, ir)

        response = {
            'success': result,
            'camera_group_id': camera_group_id,
            'timestamp': datetime.now().isoformat()
        }

        ctx.logger.info(f'Camera set to group ID: {camera_group_id}')
        send_json_response(handler, response)

    except Exception as e:
        ctx.logger.error(f'Error in set camera endpoint: {e}')
        send_error_response(handler, str(e))

