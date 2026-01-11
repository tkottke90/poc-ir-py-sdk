# OBS WebSocket Troubleshooting Guide

## Quick Diagnostic Tools

### 1. Quick Connection Test
```bash
python test_connection.py
```
This performs basic network connectivity tests.

### 2. Full Troubleshooting Tool
```bash
python obs_troubleshoot.py
```
This runs comprehensive diagnostics including:
- Network connectivity
- WebSocket handshake
- OBS WebSocket library connection
- Version information

## Common Issues and Solutions

### Issue 1: "Connection refused" or "Port is closed"

**Symptoms:**
```
✗ Port 4455 is CLOSED
Connection refused
```

**Solutions:**

1. **Enable OBS WebSocket Server:**
   - Open OBS Studio
   - Go to **Tools** → **WebSocket Server Settings**
   - Check **"Enable WebSocket server"**
   - Click **Apply**

2. **Verify OBS is Running:**
   - Make sure OBS Studio is actually running on the target machine

3. **Check the Port Number:**
   - Default is 4455
   - Verify it matches in both OBS and your script

### Issue 2: "Cannot resolve hostname" or "Host unreachable"

**Symptoms:**
```
✗ Cannot resolve host: 192.168.1.105
✗ Host is not responding
```

**Solutions:**

1. **Verify IP Address:**
   ```bash
   # On Windows (OBS machine)
   ipconfig
   
   # On macOS/Linux (OBS machine)
   ifconfig
   # or
   ip addr show
   ```

2. **Test Network Connectivity:**
   ```bash
   # From your Python machine
   ping 192.168.1.105
   ```

3. **Check Same Network:**
   - Both machines must be on the same network
   - Check WiFi vs Ethernet connections

### Issue 3: "Authentication failed" or Password errors

**Symptoms:**
```
✗ Connection with password failed
Authentication error
```

**Solutions:**

1. **Verify Password:**
   - Check OBS WebSocket Settings for the correct password
   - Passwords are case-sensitive

2. **Try Without Password:**
   - In OBS: Uncheck "Enable authentication"
   - Update script to connect without password:
     ```python
     ws = obsws(OBS_HOST, OBS_PORT)  # No password parameter
     ```

3. **Check OBS WebSocket Version:**
   - This library requires OBS WebSocket v5.x
   - Update OBS if using an older version

### Issue 4: Firewall Blocking Connection

**Symptoms:**
```
Connection timeout
Port appears closed but OBS is running
```

**Solutions:**

**Windows Firewall:**
```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="OBS WebSocket" dir=in action=allow protocol=TCP localport=4455
```

**macOS Firewall:**
- System Preferences → Security & Privacy → Firewall
- Click "Firewall Options"
- Add OBS to allowed applications

**Linux (ufw):**
```bash
sudo ufw allow 4455/tcp
```

### Issue 5: "Module not found" errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'obswebsocket'
ModuleNotFoundError: No module named 'websocket'
```

**Solutions:**

```bash
# Install all dependencies
make install

# Or manually
pip install obs-websocket-py websocket-client

# Verify installation
pip list | grep obs
pip list | grep websocket
```

### Issue 6: Connection works but commands fail

**Symptoms:**
```
✓ Connected to OBS
✗ Error switching scene: Scene not found
```

**Solutions:**

1. **Check Scene Names:**
   - Scene names are case-sensitive
   - Use exact names from OBS
   - Run `obs_simple_example.py` to list all scenes

2. **Check Source Names:**
   - Source/input names must match exactly
   - List all inputs with the example script

3. **Verify OBS Version:**
   - Some features require specific OBS versions
   - Update to latest OBS Studio

## Manual Testing Steps

### Step 1: Verify OBS WebSocket is Enabled

1. Open OBS Studio
2. Tools → WebSocket Server Settings
3. Should see:
   - ✓ Enable WebSocket server (checked)
   - Server Port: 4455
   - Enable Authentication: (optional)

### Step 2: Test from Command Line

**Using curl (if available):**
```bash
curl -i -N -H "Connection: Upgrade" \
     -H "Upgrade: websocket" \
     -H "Sec-WebSocket-Version: 13" \
     -H "Sec-WebSocket-Key: test" \
     http://192.168.1.105:4455/
```

Should return: `HTTP/1.1 101 Switching Protocols`

### Step 3: Test with Python

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('192.168.1.105', 4455))
print("Open" if result == 0 else "Closed")
sock.close()
```

## Getting More Information

### Enable Verbose Logging

Add to your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check OBS Logs

OBS logs are located at:
- **Windows:** `%APPDATA%\obs-studio\logs`
- **macOS:** `~/Library/Application Support/obs-studio/logs`
- **Linux:** `~/.config/obs-studio/logs`

Look for WebSocket-related errors.

## Still Having Issues?

1. **Run the troubleshooting tool:**
   ```bash
   python obs_troubleshoot.py
   ```

2. **Check versions:**
   - OBS Studio version (Help → About)
   - Python version: `python --version`
   - Library version: `pip show obs-websocket-py`

3. **Try the simple example:**
   ```bash
   python obs_simple_example.py
   ```

4. **Check the OBS WebSocket documentation:**
   - https://github.com/obsproject/obs-websocket
   - https://github.com/Elektordi/obs-websocket-py

