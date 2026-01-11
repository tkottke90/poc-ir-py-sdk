"""
OBS WebSocket Integration Example
This shows how to control OBS based on iRacing telemetry

Features:
- Switch scenes based on race flags
- Update text sources with telemetry data
- Control recording/streaming based on session state

Setup:
1. Install OBS Studio: https://obsproject.com/
2. Enable WebSocket server in OBS:
   - Tools -> WebSocket Server Settings
   - Enable WebSocket server
   - Set port (default: 4455)
   - Set password (optional but recommended)
3. Install dependencies: pip install obs-websocket-py
"""

import irsdk
import time
import os
from obswebsocket import obsws, requests

# OBS WebSocket connection settings
OBS_HOST = "10.0.0.6"  # Change to your OBS machine IP
OBS_PORT = 4455        # Default OBS WebSocket port
OBS_PASSWORD = "your_password_here"  # Set in OBS WebSocket settings

class State:
    ir_connected = False
    obs_connected = False
    last_flags = 0

def connect_obs():
    """Connect to OBS WebSocket server"""
    try:
        ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        ws.connect()
        print(f"Connected to OBS at {OBS_HOST}:{OBS_PORT}")
        return ws
    except Exception as e:
        print(f"Failed to connect to OBS: {e}")
        return None

def switch_scene_on_flag(ws, flags):
    """Switch OBS scenes based on race flags"""
    try:
        # Example: Switch to different scenes based on flags
        if flags & irsdk.Flags.green:
            ws.call(requests.SetCurrentProgramScene(sceneName="Racing"))
        elif flags & irsdk.Flags.yellow or flags & irsdk.Flags.caution:
            ws.call(requests.SetCurrentProgramScene(sceneName="Caution"))
        elif flags & irsdk.Flags.checkered:
            ws.call(requests.SetCurrentProgramScene(sceneName="Finish"))
    except Exception as e:
        print(f"Error switching scene: {e}")

def update_text_source(ws, source_name, text):
    """Update a text source in OBS with telemetry data"""
    try:
        # Get the current scene
        current_scene = ws.call(requests.GetCurrentProgramScene())
        scene_name = current_scene.getSceneName()
        
        # Update text source settings
        ws.call(requests.SetInputSettings(
            inputName=source_name,
            inputSettings={"text": text}
        ))
    except Exception as e:
        print(f"Error updating text source: {e}")

def decode_session_flags(flags):
    """Decode session flags to readable format"""
    active_flags = []
    if flags & irsdk.Flags.green:
        active_flags.append('GREEN')
    if flags & irsdk.Flags.yellow:
        active_flags.append('YELLOW')
    if flags & irsdk.Flags.checkered:
        active_flags.append('CHECKERED')
    if flags & irsdk.Flags.caution:
        active_flags.append('CAUTION')
    return ', '.join(active_flags) if active_flags else 'NONE'

def main():
    # Initialize iRacing SDK
    ir = irsdk.IRSDK()
    state = State()
    
    # Connect to OBS
    obs_ws = connect_obs()
    if obs_ws:
        state.obs_connected = True
    
    try:
        while True:
            # Check iRacing connection
            if not state.ir_connected and ir.startup():
                state.ir_connected = True
                print("Connected to iRacing")
            elif state.ir_connected and not ir.is_connected:
                state.ir_connected = False
                ir.shutdown()
                print("Disconnected from iRacing")
            
            # Process telemetry if connected
            if state.ir_connected and state.obs_connected:
                ir.freeze_var_buffer_latest()
                
                # Get telemetry data
                session_time = ir['SessionTime']
                session_flags = ir['SessionFlags']
                speed = ir['Speed']
                
                # Switch scenes when flags change
                if session_flags != state.last_flags:
                    switch_scene_on_flag(obs_ws, session_flags)
                    state.last_flags = session_flags
                
                # Update text overlays with telemetry
                # (You need to create these text sources in OBS first)
                update_text_source(obs_ws, "SessionTime", f"Time: {session_time:.1f}s")
                update_text_source(obs_ws, "Speed", f"Speed: {speed * 2.237:.0f} mph")
                update_text_source(obs_ws, "Flags", decode_session_flags(session_flags))
                
                print(f"Time: {session_time:.1f}s | Flags: {decode_session_flags(session_flags)}")
            
            time.sleep(0.5)  # Update 2 times per second
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if obs_ws:
            obs_ws.disconnect()
            print("Disconnected from OBS")
        if ir:
            ir.shutdown()

if __name__ == "__main__":
    main()

