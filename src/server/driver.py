from .helpers import send_json_response, send_error_response
from .context import ServerContext
from models.driver_info import DriverInfo
from datetime import datetime

def handle_driver(handler, ctx: ServerContext):
    """Handle driver data endpoint"""
    try:
        ctx.logger.debug('Driver endpoint called')

        # Validate context has the required getters
        if not hasattr(ctx, 'get_ir') or not callable(ctx.get_ir):
            ctx.logger.error('Context missing get_ir callable')
            send_error_response(handler, 'Server configuration error: missing get_ir', 500)
            return

        if not hasattr(ctx, 'get_state') or not callable(ctx.get_state):
            ctx.logger.error('Context missing get_state callable')
            send_error_response(handler, 'Server configuration error: missing get_state', 500)
            return

        # Get current values on demand using context
        ir = ctx.ir
        state = ctx.state

        # Validate that we got valid objects back
        if ir is None:
            ctx.logger.error('Context.ir returned None - lambda may not be capturing ir correctly')
            send_error_response(handler, 'Server configuration error: ir is None', 500)
            return

        if state is None:
            ctx.logger.error('Context.state returned None - lambda may not be capturing state correctly')
            send_error_response(handler, 'Server configuration error: state is None', 500)
            return

        # Validate ir has required methods
        if not hasattr(ir, 'freeze_var_buffer_latest'):
            ctx.logger.error(f'ir object missing freeze_var_buffer_latest method. Type: {type(ir).__name__}')
            send_error_response(handler, 'Server configuration error: invalid ir object', 500)
            return

        if not hasattr(ir, '__getitem__'):
            ctx.logger.error(f'ir object missing __getitem__ method. Type: {type(ir).__name__}')
            send_error_response(handler, 'Server configuration error: invalid ir object', 500)
            return

        # Validate state has required properties
        if not hasattr(state, 'ir_connected'):
            ctx.logger.error(f'state object missing ir_connected property. Type: {type(state).__name__}')
            send_error_response(handler, 'Server configuration error: invalid state object', 500)
            return

        if not hasattr(state, 'drivers'):
            ctx.logger.error(f'state object missing drivers property. Type: {type(state).__name__}')
            send_error_response(handler, 'Server configuration error: invalid state object', 500)
            return

        # Log successful validation
        ctx.logger.debug(f'Context validation passed - ir type: {type(ir).__name__}, state type: {type(state).__name__}')
        ctx.logger.debug(f'ir.connected: {getattr(ir, "connected", "N/A")}, state.ir_connected: {state.ir_connected}')

        if not state.ir_connected:
            ctx.logger.warning('Driver endpoint called but not connected to iRacing')
            send_error_response(handler, 'Not connected to iRacing', 503)
            return

        # Freeze buffer for consistent data
        ir.freeze_var_buffer_latest()

        # Get driver info
        driver: DriverInfo = state.drivers

        # Validate driver object
        if driver is None:
            ctx.logger.error('state.drivers returned None')
            send_error_response(handler, 'Driver data not available', 500)
            return

        if driver.UserName == 'Unknown':
            ctx.logger.error('state.drivers returned Unknown driver')
            send_json_response(handler, {
              'error': 'Driver data not available',
              'info': driver.to_dict()  # Serialize the driver object
            }, 500)
            return

        ctx.logger.debug(f'Driver retrieved: {driver.UserName or "MISSING"} (type: {type(driver).__name__})')

        # Check if full driver object is requested via query parameter
        # Parse query string from path
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(handler.path)
        query_params = parse_qs(parsed.query)
        full_response = query_params.get('full', ['false'])[0].lower() == 'true'

        if full_response:
            # Return full driver object with telemetry data
            response = {
                'driver': driver.to_dict(),
                'telemetry': {
                    'player_incidents': ir['PlayerCarDriverIncidentCount'],
                    'team_incidents': ir['PlayerCarTeamIncidentCount'],
                    'laps_completed': ir['LapCompleted'],
                    'total_laps': ir['RaceLaps'],
                },
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Return simplified response (backward compatible)
            response = {
                'driver_name': driver.UserName,
                'driver_team': driver.TeamName,
                'driver_number': driver.CarNumber,
                'driver_license': driver.LicString,
                'driver_license_color': driver.lic_color_hex,
                'driver_irating': driver.IRating,
                'driver_incidents': ir['PlayerCarDriverIncidentCount'],
                'team_incidents': ir['PlayerCarTeamIncidentCount'],
                'driver_laps': ir['LapCompleted'],
                'total_laps': ir['RaceLaps'],
                'timestamp': datetime.now().isoformat()
            }

        ctx.logger.info(f'Driver data returned: {driver.UserName} (#{driver.CarNumber}), full={full_response}')
        send_json_response(handler, response)

    except Exception as e:
        ctx.logger.error(f'Error in driver endpoint: {e}')
        send_error_response(handler, str(e))