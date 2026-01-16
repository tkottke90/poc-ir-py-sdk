from .helpers import send_json_response, send_error_response
from .context import ServerContext
from models.driver_info import DriverInfo
from datetime import datetime

def handle_driver(handler, ctx: ServerContext):
    """Handle driver data endpoint"""
    try:
        # Get current values on demand using context
        ir = ctx.ir
        state = ctx.state

        ctx.logger.debug('Driver endpoint called')

        if not state.ir_connected:
            ctx.logger.warning('Driver endpoint called but not connected to iRacing')
            send_error_response(handler, 'Not connected to iRacing', 503)
            return

        # Freeze buffer for consistent data
        ir.freeze_var_buffer_latest()

        # Get driver info
        driver: DriverInfo = state.drivers

        # Build response
        response = {
            'driver_name': driver.UserName,
            'driver_team': driver.TeamName,
            'driver_number': driver.CarNumber,
            'driver_license': driver.LicString,
            'driver_irating': driver.IRating,
            'driver_incidents': ir['PlayerCarMyIncidentCount'],
            'team_incidents': ir['PlayerCarDriverIncidentCount'],
            'driver_laps': ir['LapCompleted'],
            'total_laps': ir['RaceLaps'],
            'timestamp': datetime.now().isoformat()
        }

        ctx.logger.info(f'Driver data returned: {driver.UserName} (#{driver.CarNumber})')
        send_json_response(handler, response)

    except Exception as e:
        ctx.logger.error(f'Error in driver endpoint: {e}')
        send_error_response(handler, str(e))