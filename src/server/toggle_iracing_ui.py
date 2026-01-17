from .helpers import send_json_response, send_error_response
from .context import ServerContext
from datetime import datetime


def handle_toggle_iracing_ui(handler, ctx: ServerContext):
    """Handle toggle pit cams endpoint - toggles the show_pit_cams flag"""
    try:
        # Get current values on demand using context
        state = ctx.state

        ctx.logger.debug('Toggle pit cams endpoint called')

        # Toggle the flag
        new_state = state.toggle_pit_cams()

        response = {
            'show_pit_cams': new_state,
            'timestamp': datetime.now().isoformat()
        }

        ctx.logger.info(f'Pit cams toggled to: {new_state}')
        send_json_response(handler, response)

    except Exception as e:
        ctx.logger.error(f'Error in toggle pit cams endpoint: {e}')
        send_error_response(handler, str(e))
