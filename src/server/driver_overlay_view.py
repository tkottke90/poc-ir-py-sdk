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
      :root {{
        --license-color: {driver_license_color};
        --license-bg: {driver_license_bg};
      }}

      main {{
        font-size: 2rem;
        line-height: 4rem;
        display: flex;
        justify-content: space-between;
      }}

      .license {{
        padding: 0.25rem 0.5rem;

        color: var(--license-color);
        border: 1px solid currentColor;
        background-color: var(--license-bg);
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
            iR:{ driver_irating } - <span class="license">{ driver_license }</span>
          </span>
          <span class="driver-stat" data-stat="incidents">
            Incidents: { driver_incidents } /{ team_incidents }
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

      // Fetch driver data from API and update the display
      async function updateDriverData() {{
        try {{
          const response = await fetch('/api/driver');
          if (!response.ok) {{
            // Fail quietly - don't show errors on stream
            return;
          }}

          const data = await response.json();

          // Update driver name
          const driverNameEl = document.getElementById('driver-name');
          if (driverNameEl && data.driver_name) {{
            driverNameEl.textContent = data.driver_name;
          }}

          // Update the stat elements content
          const licenseStatEl = document.querySelector('[data-stat="license"]');
          if (licenseStatEl && data.driver_irating && data.driver_license) {{
            licenseStatEl.innerHTML = `iR:${{data.driver_irating}} - <span class="license">${{data.driver_license}}</span>`;
          }}

          const incidentsStatEl = document.querySelector('[data-stat="incidents"]');
          if (incidentsStatEl && data.driver_incidents !== undefined && data.team_incidents !== undefined) {{
            incidentsStatEl.textContent = `Incidents: ${{data.driver_incidents}} (Team: ${{data.team_incidents}})`;
          }}
        }} catch (error) {{
          // Fail quietly - don't show errors on stream
          console.error('Failed to fetch driver data:', error);
        }}
      }}

      // Update immediately on load
      updateDriverData();

      // Update every 5 seconds
      setInterval(updateDriverData, 5000);
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

