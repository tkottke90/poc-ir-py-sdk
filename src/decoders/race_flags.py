from irsdk import Flags

# function to decode session flags from binary
def decode_session_flags(flags: int) -> list[str]:
    active_flags = []

    # Global flags
    if flags & Flags.checkered:
        active_flags.append('CHECKERED')
    if flags & Flags.white:
        active_flags.append('WHITE')
    if flags & Flags.green:
        active_flags.append('GREEN')
    if flags & Flags.yellow:
        active_flags.append('YELLOW')
    if flags & Flags.red:
        active_flags.append('RED')
    if flags & Flags.blue:
        active_flags.append('BLUE')
    if flags & Flags.debris:
        active_flags.append('DEBRIS')
    if flags & Flags.crossed:
        active_flags.append('CROSSED')
    if flags & Flags.yellow_waving:
        active_flags.append('YELLOW_WAVING')
    if flags & Flags.one_lap_to_green:
        active_flags.append('ONE_LAP_TO_GREEN')
    if flags & Flags.green_held:
        active_flags.append('GREEN_HELD')
    if flags & Flags.ten_to_go:
        active_flags.append('TEN_TO_GO')
    if flags & Flags.five_to_go:
        active_flags.append('FIVE_TO_GO')
    if flags & Flags.random_waving:
        active_flags.append('RANDOM_WAVING')
    if flags & Flags.caution:
        active_flags.append('CAUTION')
    if flags & Flags.caution_waving:
        active_flags.append('CAUTION_WAVING')

    # Driver black flags
    if flags & Flags.black:
        active_flags.append('BLACK')
    if flags & Flags.disqualify:
        active_flags.append('DISQUALIFY')
    if flags & Flags.servicible:
        active_flags.append('SERVICIBLE')
    if flags & Flags.furled:
        active_flags.append('FURLED')
    if flags & Flags.repair:
        active_flags.append('REPAIR')

    # Start lights
    if flags & Flags.start_hidden:
        active_flags.append('START_HIDDEN')
    if flags & Flags.start_ready:
        active_flags.append('START_READY')
    if flags & Flags.start_set:
        active_flags.append('START_SET')
    if flags & Flags.start_go:
        active_flags.append('START_GO')

    return active_flags if active_flags else ['NONE']