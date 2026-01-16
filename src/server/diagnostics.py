from .helpers import send_json_response, send_error_response
from .context import ServerContext
from datetime import datetime


def handle_diagnostics(handler, ctx: ServerContext):
    """
    Handle diagnostics endpoint - provides information about the context state
    and validates that all dependencies are correctly configured.
    """
    try:
        ctx.logger.debug('Diagnostics endpoint called')
        
        diagnostics = {
            'timestamp': datetime.now().isoformat(),
            'context': {},
            'ir': {},
            'state': {},
            'validation': {
                'context_valid': True,
                'ir_valid': True,
                'state_valid': True,
                'errors': []
            }
        }
        
        # Check context
        try:
            diagnostics['context']['has_get_ir'] = hasattr(ctx, 'get_ir')
            diagnostics['context']['get_ir_callable'] = callable(getattr(ctx, 'get_ir', None))
            diagnostics['context']['has_get_state'] = hasattr(ctx, 'get_state')
            diagnostics['context']['get_state_callable'] = callable(getattr(ctx, 'get_state', None))
            diagnostics['context']['has_logger'] = hasattr(ctx, 'logger')
        except Exception as e:
            diagnostics['validation']['context_valid'] = False
            diagnostics['validation']['errors'].append(f'Context check failed: {str(e)}')
        
        # Check ir
        try:
            ir = ctx.ir
            
            if ir is None:
                diagnostics['validation']['ir_valid'] = False
                diagnostics['validation']['errors'].append('ctx.ir returned None')
                diagnostics['ir']['is_none'] = True
            else:
                diagnostics['ir']['is_none'] = False
                diagnostics['ir']['type'] = type(ir).__name__
                diagnostics['ir']['has_freeze_var_buffer_latest'] = hasattr(ir, 'freeze_var_buffer_latest')
                diagnostics['ir']['has_getitem'] = hasattr(ir, '__getitem__')
                diagnostics['ir']['has_connected'] = hasattr(ir, 'connected')
                diagnostics['ir']['has_source'] = hasattr(ir, 'source')
                diagnostics['ir']['has_name'] = hasattr(ir, 'name')
                
                if hasattr(ir, 'connected'):
                    diagnostics['ir']['connected'] = ir.connected
                    
                if hasattr(ir, 'name'):
                    diagnostics['ir']['name'] = ir.name
                    
                # Check required methods
                required_methods = ['freeze_var_buffer_latest', '__getitem__']
                for method in required_methods:
                    if not hasattr(ir, method):
                        diagnostics['validation']['ir_valid'] = False
                        diagnostics['validation']['errors'].append(f'ir missing method: {method}')
                        
        except Exception as e:
            diagnostics['validation']['ir_valid'] = False
            diagnostics['validation']['errors'].append(f'ir check failed: {str(e)}')
            diagnostics['ir']['error'] = str(e)
        
        # Check state
        try:
            state = ctx.state
            
            if state is None:
                diagnostics['validation']['state_valid'] = False
                diagnostics['validation']['errors'].append('ctx.state returned None')
                diagnostics['state']['is_none'] = True
            else:
                diagnostics['state']['is_none'] = False
                diagnostics['state']['type'] = type(state).__name__
                diagnostics['state']['has_ir_connected'] = hasattr(state, 'ir_connected')
                diagnostics['state']['has_drivers'] = hasattr(state, 'drivers')
                diagnostics['state']['has_camera_manager'] = hasattr(state, 'camera_manager')
                
                if hasattr(state, 'ir_connected'):
                    diagnostics['state']['ir_connected'] = state.ir_connected
                    
                if hasattr(state, 'drivers'):
                    try:
                        drivers = state.drivers
                        diagnostics['state']['drivers_type'] = type(drivers).__name__ if drivers else 'None'

                        if drivers:
                            # Add basic driver info
                            if hasattr(drivers, 'UserName'):
                                diagnostics['state']['driver_name'] = drivers.UserName
                            if hasattr(drivers, 'CarNumber'):
                                diagnostics['state']['driver_number'] = drivers.CarNumber
                            if hasattr(drivers, 'TeamName'):
                                diagnostics['state']['driver_team'] = drivers.TeamName
                            if hasattr(drivers, 'IRating'):
                                diagnostics['state']['driver_irating'] = drivers.IRating
                            if hasattr(drivers, 'LicString'):
                                diagnostics['state']['driver_license'] = drivers.LicString

                            # Add full driver object if serializable
                            if hasattr(drivers, 'to_dict'):
                                try:
                                    diagnostics['state']['driver_full'] = drivers.to_dict()
                                except Exception as e:
                                    diagnostics['state']['driver_serialization_error'] = str(e)

                            # Add driver list info if available
                            if hasattr(drivers, 'Drivers'):
                                try:
                                    driver_list = drivers.Drivers
                                    diagnostics['state']['total_drivers'] = len(driver_list) if driver_list else 0
                                    if driver_list:
                                        diagnostics['state']['driver_list'] = [
                                            {
                                                'CarIdx': d.CarIdx,
                                                'UserName': d.UserName,
                                                'CarNumber': d.CarNumber,
                                                'TeamName': d.TeamName
                                            } for d in driver_list[:5]  # Limit to first 5 for brevity
                                        ]
                                        if len(driver_list) > 5:
                                            diagnostics['state']['driver_list_truncated'] = True
                                except Exception as e:
                                    diagnostics['state']['driver_list_error'] = str(e)
                    except Exception as e:
                        diagnostics['state']['drivers_error'] = str(e)
                
                # Check required properties
                required_props = ['ir_connected', 'drivers']
                for prop in required_props:
                    if not hasattr(state, prop):
                        diagnostics['validation']['state_valid'] = False
                        diagnostics['validation']['errors'].append(f'state missing property: {prop}')
                        
        except Exception as e:
            diagnostics['validation']['state_valid'] = False
            diagnostics['validation']['errors'].append(f'state check failed: {str(e)}')
            diagnostics['state']['error'] = str(e)
        
        # Overall validation
        diagnostics['validation']['overall_valid'] = (
            diagnostics['validation']['context_valid'] and
            diagnostics['validation']['ir_valid'] and
            diagnostics['validation']['state_valid']
        )
        
        # Determine status code
        if diagnostics['validation']['overall_valid']:
            status_code = 200
            ctx.logger.info('Diagnostics check passed - all systems valid')
        else:
            status_code = 500
            ctx.logger.warning(f'Diagnostics check failed: {diagnostics["validation"]["errors"]}')
        
        send_json_response(handler, diagnostics, status_code)
        
    except Exception as e:
        ctx.logger.error(f'Error in diagnostics endpoint: {e}')
        send_error_response(handler, str(e))

