from irsdk import SessionState

def decode_session_state(state: int) -> str:
    if state == SessionState.invalid:
        return 'INVALID'
    if state == SessionState.get_in_car:
        return 'GET_IN_CAR'
    if state == SessionState.warmup:
        return 'WARMUP'
    if state == SessionState.parade_laps:
        return 'PARADE_LAPS'
    if state == SessionState.racing:
        return 'RACING'
    if state == SessionState.checkered:
        return 'CHECKERED'
    if state == SessionState.cool_down:
        return 'COOL_DOWN'
    
    return 'UNKNOWN'