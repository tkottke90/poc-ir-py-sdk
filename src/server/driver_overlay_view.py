from .context import ServerContext
from datetime import datetime


def handle_driver_overlay_view(handler, ctx: ServerContext):
    """Handle dashboard HTML page endpoint"""
    try:
        ctx.logger.debug('Dashboard endpoint called')
        
        # Get current values
        ir = ctx.ir
        state = ctx.state
        
        # Check connection status
        is_connected = state.ir_connected
        
        # Build HTML with dynamic data
        if is_connected:
            ir.freeze_var_buffer_latest()
            driver = state.drivers

            driver_name = driver.UserName
            driver_license = driver.LicString
            driver_irating = driver.IRating
            driver_license_color = driver.lic_color_hex
            driver_license_bg = driver.lic_color_hex + '33'
            
            driver_incidents = ir['PlayerCarDriverIncidentCount']
            team_incidents = ir['PlayerCarTeamIncidentCount']
        else:
            driver_name = "N/A"
            driver_license = "N/A"
            driver_irating = "N/A"
            driver_license_color = "#444444"
            driver_license_bg = driver_license_color + '33'

            driver_incidents = "N/A"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Driver Overlay</title>
    <link rel="stylesheet" href="./overlay.css">
    <style>

      main {{
        font-size: 2rem;
        line-height: 4rem;
        display: flex;
        justify-content: space-between;
      }}

      .license {{
        margin: 0.25rem 0.5rem;

        color: {driver_license_color};
        border: 1px solid currentColor;
        background-color: {driver_license_bg};
      }}

      #driver-stats-container {{
        position: relative;
        
        min-height: 2em;
        width: 50%;
        
        display: flex;
        justify-content: flex-end;
      }}
    </style>

    <script src="./overlay-container.component.js"></script>
  </head>
  <body>
    <overlay-container>
      <main>
        <span id="driver-name">{ driver_name }</span>
        <div id="driver-stats-container">
          <span class="driver-stat" data-stat="license">
            { driver_license } - <span class="license">{ driver_irating }</span>
          </span>
          <span class="driver-stat" data-stat="incidents">
            Incidents: { driver_incidents } / { team_incidents }
          </span>
        </div>
      </main>
    </overlay-container>

    <script type="module">
      import {{ TextAnimator }} from './text-animator.js';

      // Get the stat elements
      const statElements = Array.from(document.querySelectorAll('.driver-stat'));

      // Create animator with 10 second display duration (10000ms)
      const animator = new TextAnimator(statElements, 10000, {{
        enterDuration: 600,
        exitDuration: 800
      }});

      // Start the animation
      animator.start();
    </script>
  </body>
</html>
"""
        
        # Send HTML response
        handler.send_response(200)
        handler.send_header('Content-Type', 'text/html; charset=utf-8')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.end_headers()
        handler.wfile.write(html.encode('utf-8'))
        
        ctx.logger.info('Dashboard page served')
        
    except Exception as e:
        ctx.logger.error(f'Error in dashboard endpoint: {e}')
        # Send error HTML
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 50px; text-align: center; }}
        .error {{ color: #f44336; }}
    </style>
</head>
<body>
    <h1 class="error">Error</h1>
    <p>{str(e)}</p>
    <a href="/dashboard">Try Again</a>
</body>
</html>
"""
        handler.send_response(500)
        handler.send_header('Content-Type', 'text/html; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(error_html.encode('utf-8'))

