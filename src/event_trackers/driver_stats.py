from pydantic import BaseModel
from iracing import TelemetryHandler

class DriverStats(BaseModel):
    idx: int
    position: int
    class_position: int
    incidents: int
    team_incidents: int
    isOnTrack: bool
    isInGarage: bool

def getDriverStats(ir: TelemetryHandler) -> dict:
    idx = ir['PlayerCarIdx']

    incidents = ir['PlayerCarMyIncidentCount']
    team_incidents = ir['PlayerCarTeamIncidentCount']
    
    position = ir['PlayerCarPosition']
    class_position = ir['PlayerCarClassPosition']

    isOnTrack = ir['IsOnTrack']
    isInGarage = ir['IsInGarage']

    return DriverStats({
        'idx': idx,
        'position': position,
        'classPosition': class_position,
        'incidents': incidents,
        'team_incidents': team_incidents,
        'isOnTrack': isOnTrack,
        'isInGarage': isInGarage
    })