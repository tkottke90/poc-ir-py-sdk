from iracing import TelemetryHandler

def get_weekend_info(ir: TelemetryHandler) -> dict:
    return ir['WeekendInfo']