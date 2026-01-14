from pydantic import BaseModel, Field
from typing import Optional, Union
from .telemetry import TelemetryHandler


class ResultsPosition(BaseModel):
    """Individual driver position and results data for a session"""

    Position: int = Field(description="Overall position in the session", default=0)
    ClassPosition: int = Field(description="Position within the driver's class", default=0)
    CarIdx: int = Field(description="Unique car index identifier", default=-1)
    Lap: int = Field(description="Current lap number", default=0)
    Time: float = Field(description="Total time elapsed", default=0.0)
    FastestLap: int = Field(description="Lap number of fastest lap", default=0)
    FastestTime: float = Field(description="Fastest lap time in seconds", default=0.0)
    LastTime: float = Field(description="Last lap time in seconds", default=0.0)
    LapsLed: int = Field(description="Number of laps led", default=0)
    LapsComplete: int = Field(description="Number of laps completed", default=0)
    JokerLapsComplete: int = Field(description="Number of joker laps completed", default=0)
    LapsDriven: float = Field(description="Total laps driven (including partial laps)", default=0.0)
    Incidents: int = Field(description="Number of incidents", default=0)
    ReasonOutId: int = Field(description="Reason out identifier (0 = still racing)", default=0)
    ReasonOutStr: str = Field(description="Reason out description", default='')


class ResultsFastestLap(BaseModel):
    """Fastest lap information for a driver"""

    CarIdx: int = Field(description="Unique car index identifier", default=-1)
    FastestLap: int = Field(description="Lap number of fastest lap", default=0)
    FastestTime: float = Field(description="Fastest lap time in seconds", default=0.0)


class SessionInfo(BaseModel):
    """Detailed information about a specific session (practice, qualifying, race, etc.)"""

    SessionNum: int = Field(description="Session number identifier", default=0)
    SessionLaps: Union[str, int] = Field(description="Number of laps in session or 'unlimited'", default=0)
    SessionTime: str = Field(description="Session time limit", default='00:00:00')
    SessionNumLapsToAvg: int = Field(description="Number of laps to average for timing", default=0)
    SessionType: str = Field(description="Type of session (Practice, Qualify, Race, etc.)", default='Unknown')
    SessionTrackRubberState: str = Field(description="Track rubber state", default='moderate usage')
    SessionName: str = Field(description="Display name of the session", default='Unknown')
    SessionSubType: Optional[str] = Field(default=None, description="Session subtype if applicable")
    SessionSkipped: int = Field(description="Whether session was skipped (0=no, 1=yes)", default=0)
    SessionRunGroupsUsed: int = Field(description="Whether run groups are used", default=0)
    SessionEnforceTireCompoundChange: int = Field(description="Whether tire compound change is enforced", default=0)
    ResultsPositions: list[ResultsPosition]
    ResultsFastestLap: list[ResultsFastestLap]
    ResultsAverageLapTime: float = Field(description="Average lap time in seconds", default=0.0)
    ResultsNumCautionFlags: int = Field(description="Number of caution flags", default=0)
    ResultsNumCautionLaps: int = Field(description="Number of caution laps", default=0)
    ResultsNumLeadChanges: int = Field(description="Number of lead changes", default=0)
    ResultsLapsComplete: int = Field(description="Total laps completed in session", default=0)
    ResultsOfficial: int = Field(description="Whether results are official (0=no, 1=yes)", default=0)


class Session(BaseModel):
    """Container for all session information"""

    CurrentSessionNum: int = Field(description="Currently active session number", default=0)
    Sessions: list[SessionInfo] = Field(default_factory=list, description="List of all sessions in the event")

    @staticmethod
    def from_iracing(ir: TelemetryHandler):
        """Create a Session instance from iRacing telemetry data"""
        if ir['SessionInfo'] is None:
            return Session()

        return Session(**ir['SessionInfo'])
    

    @staticmethod
    def get_session_time(ir: TelemetryHandler) -> float:
        """Get the current session time"""
        return ir['SessionTime']
    
    @staticmethod
    def get_session_flags(ir: TelemetryHandler) -> list[str]:
        """Get the current session flags"""
        return ir['SessionFlags']
    
    @staticmethod
    def get_session_flags_display(ir: TelemetryHandler) -> str:
        """Get the current session flags as a human-readable string"""
        
        f = Session.get_session_flags(ir)
        
        return f"{ir.decode_session_flags(f)} ({f})"