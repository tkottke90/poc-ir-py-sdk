import decoders
from irsdk import IRSDK, IBT
from enum import Enum

# Base telemetry handler
class TelemetryHandler:
    name = 'Base'

    source: IRSDK | IBT | None = None

    def __init__(self):
        self.connected = False

    def connect(self):
        raise NotImplementedError("Subclasses must implement connect()")

    def disconnect(self):
        raise NotImplementedError("Subclasses must implement disconnect()")

    def decode_session_flags(self, flags):
        return decoders.decode_session_flags(flags)
    
    def decode_car_location(self, location):
        return decoders.decode_car_location(location)
    
    def decode_session_state(self, state):
        return decoders.decode_session_state(state)

    def freeze_var_buffer_latest(self):
        pass

    def get_data(self, key):
        raise NotImplementedError("Subclasses must implement get_data()")
    
    def get_next_tick(self):
        return 0

    def __getitem__(self, key):
        """Enable dictionary-style access: ir['SessionTime']"""
        return self.get_data(key)
    
    def get_playback_display(self):
        return ''

    def get_playback_info(self):
        """Return current playback information"""
        return {
            'current_frame': self.get_next_tick(),
            'total_frames': 0,
            'playback_speed': 0,
            'speed_multiplier': 0,
            'tick_rate': 0,
            'progress_percent': 0
        }
    
    def get_session_name(self):
        return ''
    
    def keys(self):
        return []

# Playback speed enum for IBT file playback
class PlaybackSpeed(Enum):
    SLOW = 0.25
    NORMAL = 1.0
    FAST = 2.0

    @classmethod
    def from_string(cls, speed_str):
        """Convert string to PlaybackSpeed enum"""
        speed_str = speed_str.upper()
        try:
            return cls[speed_str]
        except KeyError:
            raise ValueError(f"Invalid playback speed: {speed_str}. Valid options: {', '.join([s.name for s in cls])}")

    @property
    def multiplier(self):
        """Get the numeric multiplier value"""
        return self.value

# Live telemetry handler
class LiveTelemetryHandler(TelemetryHandler):
    name = 'Live'

    def __init__(self):
        super().__init__()
        self.ir = IRSDK()
        self.source = self.ir

    def connect(self):
        self.ir.startup()
        self.connected = self.ir.is_initialized and self.ir.is_connected

    def disconnect(self):
        self.ir.shutdown()
        self.connected = False

    def freeze_var_buffer_latest(self):
        """Freeze the variable buffer for consistent data reads"""
        self.ir.freeze_var_buffer_latest()

    def get_data(self, key):
        return self.ir[key]

    def get_next_tick(self):
        return self.ir['SessionTime']

    def get_session_info_update_by_key(self, key):
        return self.ir.get_session_info_update_by_key(key)
    
    def get_playback_display(self):
        return 'LIVE'

    def get_playback_info(self):
        """Return current playback information"""
        return {
            'current_frame': self.get_next_tick(),
            'total_frames': -1,
            'playback_speed': 'Live',
            'speed_multiplier': 1.0,
            'tick_rate': 60,
            'progress_percent': -1
        }
    
    def keys(self):
        return self.ir.var_headers_names

# File-based telemetry handler
class FileTelemetryHandler(TelemetryHandler):
    name = 'File'

    def __init__(self, file_path, playback_speed='normal', skip_to=0.0):
        super().__init__()
        self.ibt = IBT()
        self.source = self.ibt
        self.file_path = file_path

        # Convert string to PlaybackSpeed enum if needed
        if isinstance(playback_speed, str):
            self.playback_speed = PlaybackSpeed.from_string(playback_speed)
        elif isinstance(playback_speed, PlaybackSpeed):
            self.playback_speed = playback_speed
        else:
            raise ValueError(f"playback_speed must be a string or PlaybackSpeed enum, got {type(playback_speed)}")

        # Validate skip_to is between 0 and 1
        if not 0.0 <= skip_to <= 1.0:
            raise ValueError(f"skip_to must be between 0.0 and 1.0, got {skip_to}")

        self.skip_to = skip_to
        self.current_frame = 0
        self.total_frames = 0
        self.tick_rate = 60  # Default iRacing tick rate (60 Hz)

    def connect(self):
        self.ibt.open(self.file_path)
        self.connected = self.ibt._header is not None

        if self.connected:
            # Get total number of frames in the recording
            self.total_frames = self.ibt._disk_header.session_record_count
            # Get the actual tick rate from the file header
            self.tick_rate = self.ibt._header.tick_rate
            # Calculate starting frame based on skip_to (0.0 to 1.0)
            self.current_frame = int(self.total_frames * self.skip_to)

    def disconnect(self):
        self.ibt.close()
        self.connected = False
        self.current_frame = 0
        self.total_frames = 0

    def to_json(self):
        frames = []

        for i in range(self.total_frames):
            frames.append(self.ibt.get(i, 'SessionTime'))
        
        return frames

    def get_data(self, key):
        # Get data from the current frame instead of the last frame
        if not self.connected or self.current_frame >= self.total_frames:
            return None
        return self.ibt.get(int(self.current_frame), key)

    def get_next_tick(self):
        """Increment the current frame and return the current SessionTime"""
        if not self.connected:
            return 0

        # Increment frame based on playback_speed and tick_rate
        # This normalizes behavior between Live and File telemetry
        frame_increment = self.playback_speed.multiplier * (self.tick_rate / 60.0)
        self.current_frame += frame_increment

        # Wrap around if we exceed total frames (loop playback)
        if self.current_frame >= self.total_frames:
            self.current_frame = 0

        # Return the SessionTime for the current frame
        return self.ibt.get(int(self.current_frame), 'SessionTime') or 0

    def get_playback_display(self):
        playback = self.get_playback_info()

        return f'{playback["progress_percent"]:.2f}% @ {playback["playback_speed"]} ({playback["speed_multiplier"]}x)'

    def get_playback_info(self):
        """Return current playback information"""
        return {
            'current_frame': int(self.current_frame),
            'total_frames': self.total_frames,
            'playback_speed': self.playback_speed.name,
            'speed_multiplier': self.playback_speed.multiplier,
            'tick_rate': self.tick_rate,
            'skip_to': self.skip_to,
            'progress_percent': (self.current_frame / self.total_frames * 100) if self.total_frames > 0 else 0
        }
    
    def keys(self):
        return self.ibt.var_headers_names