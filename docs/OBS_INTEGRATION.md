# OBS WebSocket Integration Guide

## Setup

### 1. Enable OBS WebSocket Server

1. Open OBS Studio
2. Go to **Tools** → **WebSocket Server Settings**
3. Check **Enable WebSocket server**
4. Note the **Server Port** (default: 4455)
5. Set a **Server Password** (recommended)
6. Click **Apply** and **OK**

### 2. Install Python Library

```bash
make install
# or
pip install obs-websocket-py
```

### 3. Configure Connection

Update the connection settings in your script:

```python
OBS_HOST = "10.0.0.6"  # IP of machine running OBS
OBS_PORT = 4455         # Default OBS WebSocket port
OBS_PASSWORD = "your_password_here"
```

## Common Use Cases

### Switch Scenes Based on Race Flags

```python
if flags & irsdk.Flags.green:
    ws.call(requests.SetCurrentProgramScene(sceneName="Racing"))
elif flags & irsdk.Flags.yellow:
    ws.call(requests.SetCurrentProgramScene(sceneName="Caution"))
elif flags & irsdk.Flags.checkered:
    ws.call(requests.SetCurrentProgramScene(sceneName="Finish"))
```

### Update Text Overlays

```python
# Update speed display
ws.call(requests.SetInputSettings(
    inputName="Speed",
    inputSettings={"text": f"{speed * 2.237:.0f} mph"}
))

# Update lap time
ws.call(requests.SetInputSettings(
    inputName="LapTime",
    inputSettings={"text": f"Lap: {lap_time:.2f}"}
))
```

### Auto Start/Stop Recording

```python
# Start recording when session begins
if session_state == "Racing":
    ws.call(requests.StartRecord())

# Stop recording when session ends
if session_state == "Finished":
    ws.call(requests.StopRecord())
```

### Show/Hide Sources

```python
# Show incident replay overlay
ws.call(requests.SetSceneItemEnabled(
    sceneName="Racing",
    sceneItemId=item_id,
    sceneItemEnabled=True
))
```

## Available Examples

### `obs_simple_example.py`
Basic OBS operations:
- Connect to OBS
- List scenes and sources
- Switch scenes
- Start/stop recording
- Update text sources

Run: `python obs_simple_example.py`

### `obs_integration_example.py`
Full iRacing + OBS integration:
- Automatic scene switching based on flags
- Real-time telemetry overlays
- Session-based recording control

Run: `python obs_integration_example.py`

## Common OBS WebSocket Commands

### Scene Management
```python
# Get all scenes
scenes = ws.call(requests.GetSceneList())

# Get current scene
current = ws.call(requests.GetCurrentProgramScene())

# Switch scene
ws.call(requests.SetCurrentProgramScene(sceneName="Scene Name"))
```

### Recording/Streaming
```python
# Start/stop recording
ws.call(requests.StartRecord())
ws.call(requests.StopRecord())

# Start/stop streaming
ws.call(requests.StartStream())
ws.call(requests.StopStream())

# Get status
status = ws.call(requests.GetRecordStatus())
```

### Source Control
```python
# Update text source
ws.call(requests.SetInputSettings(
    inputName="SourceName",
    inputSettings={"text": "New Text"}
))

# Show/hide source
ws.call(requests.SetSceneItemEnabled(
    sceneName="Scene",
    sceneItemId=1,
    sceneItemEnabled=True
))
```

## Troubleshooting

**Can't connect to OBS:**
- Verify OBS WebSocket server is enabled
- Check IP address and port are correct
- Verify password matches
- Check firewall settings

**Commands not working:**
- Ensure scene/source names match exactly (case-sensitive)
- Check OBS logs for errors
- Verify you're using OBS WebSocket v5.x

**Performance issues:**
- Reduce update frequency (increase sleep time)
- Only update when values change
- Use `freeze_var_buffer_latest()` in iRacing

## Resources

- [OBS WebSocket Protocol](https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md)
- [obs-websocket-py Documentation](https://github.com/Elektordi/obs-websocket-py)
- [iRacing SDK Variables](https://github.com/kutu/pyirsdk/blob/master/vars.txt)

