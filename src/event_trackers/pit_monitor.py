from irsdk import Flags
from iracing import TelemetryHandler

def getPitStatus(iracingInstance: TelemetryHandler) -> dict:
    # Check if the car has a black flag for repairs
    flags = iracingInstance['SessionFlags']

    hasRequiredRepairs = bool(flags & Flags.repair)
    isServiceable = bool(flags & Flags.servicible)

    # Check if the car is being towed
    towTimeRemaining = iracingInstance['PlayerCarTowTime']
    isTowed = towTimeRemaining > 0

    # Check if the car is in the pit lane (TrkLoc = 2)
    isInPitLane = iracingInstance['OnPitRoad']

    # Check if the car is in the pit stall (TrkLoc = 1)
    isInPitStall = iracingInstance['PitstopActive']

    # Pull the optional repair time remaining (PitOptRepairLeft)
    optionalRepairTimeRemaining = iracingInstance['PitOptRepairLeft']

    # Pull the mandatory repair time remaining (PitRepairLeft)
    mandatoryRepairTimeRemaining = iracingInstance['PitRepairLeft']

    return dict({
        'hasRequiredRepairs': hasRequiredRepairs,
        'isServiceable': isServiceable,
        'isInPitLane': isInPitLane,
        'isInPitStall': isInPitStall,
        'optionalRepairTimeRemaining': optionalRepairTimeRemaining,
        'mandatoryRepairTimeRemaining': mandatoryRepairTimeRemaining
    })
