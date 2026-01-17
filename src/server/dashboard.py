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
            camera_groups = state.camera_groups(ir)
            show_pit_cams = state.show_pit_cams

            pitting =  'Yes' if state.driver_in_pits else 'No'

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
            camera_groups = []
            show_pit_cams = False

            pitting = 'N/A'

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

        .camera-controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}

        .camera-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }}

        .camera-btn:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        .camera-btn:active {{
            transform: translateY(0);
        }}

        .camera-btn.active {{
            background: #4CAF50;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
        }}

        .camera-btn:disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }}

        .toggle-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }}

        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }}

        .toggle-switch input {{
            opacity: 0;
            width: 0;
            height: 0;
        }}

        .toggle-slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }}

        .toggle-slider:before {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }}

        input:checked + .toggle-slider {{
            background-color: #4CAF50;
        }}

        input:checked + .toggle-slider:before {{
            transform: translateX(26px);
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
                <div class="data-row">
                    <span class="data-label">Pitting:</span>
                    <span class="data-value">{pitting}</span>
                </div>
                <div class="toggle-container">
                    <span class="data-label">Show iRacing UI:</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="pitCamsToggle" {"checked" if show_pit_cams else ""} onchange="togglePitCams()">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                <div class="toggle-container">
                    <span class="data-label">Auto Pit Cameras:</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="pitCamsToggle" {"checked" if show_pit_cams else ""} onchange="togglePitCams()">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
            </div>
        </div>

        {"" if not is_connected or not camera_groups else f'''
        <div class="card">
            <h2>🎥 Camera Controls</h2>
            <div class="camera-controls">
                {"".join([f'<button class="camera-btn{"" if camera_target != group["id"] else " active"}" onclick="switchCamera({group["id"]})">{group["name"]}</button>' for group in camera_groups])}
            </div>
        </div>
        '''}
        
        <div class="footer">
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 10px;">API Endpoints: <a href="/api" style="color: white;">/api</a> | <a href="/api/diagnostics" style="color: white;">/api/diagnostics</a> | <a href="/api/driver" style="color: white;">/api/driver</a> | <a href="/api/camera" style="color: white;">/api/camera</a></p>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 seconds if connected
        {f"setTimeout(() => location.reload(), 5000);" if is_connected else ""}

        // Function to switch camera
        async function switchCamera(cameraGroupId) {{
            try {{
                const response = await fetch('/api/camera/set', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{ camera_group_id: cameraGroupId }})
                }});

                const data = await response.json();

                if (data.success) {{
                    // Reload page to show updated camera
                    location.reload();
                }} else {{
                    alert('Failed to switch camera');
                }}
            }} catch (error) {{
                console.error('Error switching camera:', error);
                alert('Error switching camera: ' + error.message);
            }}
        }}

        // Function to toggle pit cams
        async function togglePitCams() {{
            try {{
                const response = await fetch('/api/camera/toggle-pit-cams', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }}
                }});

                const data = await response.json();

                if (data.show_pit_cams !== undefined) {{
                    // Update checkbox state
                    document.getElementById('pitCamsToggle').checked = data.show_pit_cams;
                    console.log('Pit cams toggled to:', data.show_pit_cams);
                }} else {{
                    alert('Failed to toggle pit cams');
                }}
            }} catch (error) {{
                console.error('Error toggling pit cams:', error);
                alert('Error toggling pit cams: ' + error.message);
            }}
        }}
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

