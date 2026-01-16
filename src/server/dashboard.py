from .context import ServerContext
from datetime import datetime


def handle_dashboard(handler, ctx: ServerContext):
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
            driver_number = driver.CarNumber
            driver_license = driver.LicString
            driver_irating = driver.IRating
            driver_incidents = ir['PlayerCarMyIncidentCount']
            team_incidents = ir['PlayerCarDriverIncidentCount']
            driver_laps = ir['LapCompleted']
            total_laps = ir['RaceLaps']
            current_camera = state.current_camera(ir)
            camera_target = state.current_camera_target(ir)
            
            status_color = "#4CAF50"
            status_text = "Connected"
        else:
            driver_name = "N/A"
            driver_number = "N/A"
            driver_license = "N/A"
            driver_irating = "N/A"
            driver_incidents = "N/A"
            team_incidents = "N/A"
            driver_laps = "N/A"
            total_laps = "N/A"
            current_camera = "N/A"
            camera_target = "N/A"
            
            status_color = "#f44336"
            status_text = "Not Connected"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iRacing Telemetry Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        
        .status {{
            display: inline-block;
            padding: 8px 20px;
            background: {status_color};
            color: white;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .card h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .data-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .data-row:last-child {{
            border-bottom: none;
        }}
        
        .data-label {{
            color: #666;
            font-weight: 500;
        }}
        
        .data-value {{
            color: #333;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }}
        
        .refresh-btn {{
            background: white;
            color: #667eea;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
        }}
        
        .refresh-btn:hover {{
            transform: translateY(-2px);
        }}
        
        .refresh-btn:active {{
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏁 iRacing Telemetry Dashboard</h1>
            <div class="status">{status_text}</div>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h2>👤 Driver Information</h2>
                <div class="data-row">
                    <span class="data-label">Name:</span>
                    <span class="data-value">{driver_name}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Number:</span>
                    <span class="data-value">#{driver_number}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">License:</span>
                    <span class="data-value">{driver_license}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">iRating:</span>
                    <span class="data-value">{driver_irating}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>📊 Session Stats</h2>
                <div class="data-row">
                    <span class="data-label">Driver Incidents:</span>
                    <span class="data-value">{driver_incidents}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Team Incidents:</span>
                    <span class="data-value">{team_incidents}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Laps Completed:</span>
                    <span class="data-value">{driver_laps}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Total Laps:</span>
                    <span class="data-value">{total_laps}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>📹 Camera Info</h2>
                <div class="data-row">
                    <span class="data-label">Current Camera:</span>
                    <span class="data-value">{current_camera}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Camera Target:</span>
                    <span class="data-value">{camera_target}</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 10px;">API Endpoints: <a href="/api" style="color: white;">/api</a> | <a href="/api/driver" style="color: white;">/api/driver</a> | <a href="/api/camera" style="color: white;">/api/camera</a></p>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 seconds if connected
        {f"setTimeout(() => location.reload(), 5000);" if is_connected else ""}
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

