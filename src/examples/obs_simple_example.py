"""
Simple OBS WebSocket Examples
Demonstrates common OBS operations you can use with iRacing

Before running:
1. Enable OBS WebSocket server (Tools -> WebSocket Server Settings)
2. Update OBS_HOST, OBS_PORT, and OBS_PASSWORD below
3. Run: python obs_simple_example.py
"""

from obswebsocket import obsws, requests
import time

# Configuration
OBS_HOST = "10.0.0.6"
OBS_PORT = 4455
OBS_PASSWORD = "LQnaR5N8BMAuho6A"

def main():
    # Connect to OBS
    print(f"> Connecting to OBS {OBS_HOST}:{OBS_PORT}")

    try:
        # Try with password first
        try:
            ws = obsws(OBS_HOST, OBS_PORT)
            ws.connect()
            print("✓ Connected to OBS with password!")
        except Exception as e:
            print(f"✗ Connection with password failed: {e}")
            print("  Trying without password...")
            ws = obsws(OBS_HOST, OBS_PORT)
            ws.connect()
            print("✓ Connected to OBS without password!")
        
        # Example 1: Get OBS version
        version = ws.call(requests.GetVersion())
        print(f"OBS Version: {version.getObsVersion()}")
        
        # Example 2: List all scenes
        scenes = ws.call(requests.GetSceneList())
        print("\nAvailable scenes:")
        for scene in scenes.getScenes():
            print(f"  - {scene['sceneName']}")
        
        # Example 3: Get current scene
        current = ws.call(requests.GetCurrentProgramScene())
        print(f"\nCurrent scene: {current.getSceneName()}")
        
        # Example 4: Switch to a different scene
        # ws.call(requests.SetCurrentProgramScene(sceneName="Scene 2"))
        # print("Switched to Scene 2")
        
        # Example 5: Start/Stop recording
        # ws.call(requests.StartRecord())
        # print("Recording started")
        # time.sleep(5)
        # ws.call(requests.StopRecord())
        # print("Recording stopped")
        
        # Example 6: Update a text source
        # ws.call(requests.SetInputSettings(
        #     inputName="MyTextSource",
        #     inputSettings={"text": "Hello from Python!"}
        # ))
        
        # Example 7: Set source visibility
        # ws.call(requests.SetSceneItemEnabled(
        #     sceneName="Scene 1",
        #     sceneItemId=1,  # You need to get this ID first
        #     sceneItemEnabled=True
        # ))
        
        # Example 8: Get recording status
        status = ws.call(requests.GetRecordStatus())
        print(f"\nRecording active: {status.getOutputActive()}")
        
        # Example 9: Get streaming status
        stream_status = ws.call(requests.GetStreamStatus())
        print(f"Streaming active: {stream_status.getOutputActive()}")
        
        # Example 10: List all inputs (sources)
        inputs = ws.call(requests.GetInputList())
        print("\nAvailable inputs:")
        for input_item in inputs.getInputs():
            print(f"  - {input_item['inputName']} ({input_item['inputKind']})")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ws.disconnect()
        print("\nDisconnected from OBS")

if __name__ == "__main__":
    main()

