import json


def send_json_response(handler, data: dict, status_code: int = 200):
    """Send JSON response"""
    handler.send_response(status_code)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.end_headers()
    handler.wfile.write(json.dumps(data, indent=2).encode())


def send_error_response(handler, message: str, status_code: int = 500):
    """Send error response"""
    send_json_response(handler, {'error': message}, status_code)