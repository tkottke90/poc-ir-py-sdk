from iracing import TelemetryHandler

def getDriverStats(iracingInstance: TelemetryHandler) -> dict:
    incidents = iracingInstance['PlayerCarMyIncidentCount']
    team_incidents = iracingInstance['PlayerCarTeamIncidentCount']
    
    position = iracingInstance['PlayerCarClassPosition']

    return dict({
        'incidents': incidents,
        'team_incidents': team_incidents
    })