from pydantic import BaseModel
from typing import Optional, Union


class ResultsPosition(BaseModel):
    Position: int
    ClassPosition: int
    CarIdx: int
    Lap: int
    Time: float
    FastestLap: int
    FastestTime: float
    LastTime: float
    LapsLed: int
    LapsComplete: int
    JokerLapsComplete: int
    LapsDriven: float
    Incidents: int
    ReasonOutId: int
    ReasonOutStr: str


class ResultsFastestLap(BaseModel):
    CarIdx: int
    FastestLap: int
    FastestTime: float


class SessionInfo(BaseModel):
    SessionNum: int
    SessionLaps: Union[str, int]
    SessionTime: str
    SessionNumLapsToAvg: int
    SessionType: str
    SessionTrackRubberState: str
    SessionName: str
    SessionSubType: Optional[str]
    SessionSkipped: int
    SessionRunGroupsUsed: int
    SessionEnforceTireCompoundChange: int
    ResultsPositions: list[ResultsPosition]
    ResultsFastestLap: list[ResultsFastestLap]
    ResultsAverageLapTime: float
    ResultsNumCautionFlags: int
    ResultsNumCautionLaps: int
    ResultsNumLeadChanges: int
    ResultsLapsComplete: int
    ResultsOfficial: int


class Session(BaseModel):
    CurrentSessionNum: int
    Sessions: list[SessionInfo]

