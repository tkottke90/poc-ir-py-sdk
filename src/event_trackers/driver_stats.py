from irsdk import Flags
from iracing import TelemetryHandler

def getPitStatus(iracingInstance: TelemetryHandler) -> dict:
    incidents = iracingInstance['PlayerCarMyIncidentCount']
    team_incidents = iracingInstance['PlayerCarTeamIncidentCount']
    

    return dict({
        
    })