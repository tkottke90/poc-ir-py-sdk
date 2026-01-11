# WebSocket Integration Guide

## Overview

The `main.py` script now supports sending iRacing telemetry data to a WebSocket server in real-time.

## Setup

1. **Install dependencies:**
   ```bash
   make install
   # or manually:
   pip install -r requirements.txt
   ```

2. **Configure WebSocket URL:**
   
   Edit `main.py` and change the `WEBSOCKET_URL` variable (around line 199):
   ```python
   WEBSOCKET_URL = 'ws://localhost:8080'  # Change to your server URL
   ```

## Usage

### Option 1: Test with the Example Server

1. **Start the example WebSocket server** (in one terminal):
   ```bash
   python websocket_server_example.py
   ```
   
   You should see:
   ```
   WebSocket server started on ws://localhost:8080
   Waiting for connections...
   ```

2. **Run the main script** (in another terminal):
   ```bash
   python main.py
   ```
   
   The script will:
   - Connect to iRacing
   - Connect to the WebSocket server
   - Send telemetry data every second

3. **View the data** in the server terminal:
   ```
   Client connected from ('127.0.0.1', 54321)
   
   Received telemetry data:
     Session Time: 123.45
     Session Flags: ['GREEN']
   ```

### Option 2: Connect to Your Own Server

Change the `WEBSOCKET_URL` in `main.py` to point to your server:

```python
# Local server
WEBSOCKET_URL = 'ws://localhost:8080'

# Remote server
WEBSOCKET_URL = 'ws://10.0.0.6:8080'

# Secure WebSocket
WEBSOCKET_URL = 'wss://your-server.com/telemetry'
```

## Data Format

The telemetry data is sent as JSON:

```json
{
  "sessionTime": 123.45,
  "sessionFlags": {
    "raw": "0x0004",
    "decoded": ["GREEN"]
  }
}
```

## Customizing Data

To send additional telemetry data, edit the `loop()` function in `main.py`:

```python
telemetry_data = {
    'sessionTime': t,
    'sessionFlags': {
        'raw': hex(f),
        'decoded': decode_session_flags(f)
    },
    # Add more data here:
    'speed': ir['Speed'],
    'rpm': ir['RPM'],
    'gear': ir['Gear'],
    # etc...
}
send_to_websocket(telemetry_data)
```

## Troubleshooting

**Connection fails:**
- Make sure the WebSocket server is running
- Check the URL is correct
- Verify firewall settings allow the connection

**Data not sending:**
- Check that iRacing is running and connected
- Look for error messages in the console
- Verify the WebSocket connection is established

**Server not receiving data:**
- Check server logs for errors
- Verify the server is listening on the correct port
- Test with the example server first

