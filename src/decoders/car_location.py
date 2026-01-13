from irsdk import TrkLoc

def decode_car_location(location: int) -> str:
    if location == TrkLoc.not_in_world:
        return 'NOT_IN_WORLD'
    if location == TrkLoc.off_track:
        return 'OFF_TRACK'
    if location == TrkLoc.in_pit_stall:
        return 'IN_PIT_STALL'
    if location == TrkLoc.aproaching_pits:
        return 'APROACHING_PITS'
    if location == TrkLoc.on_track:
        return 'ON_TRACK'
    return 'UNKNOWN'