from http import server
import socketserver
import threading

def start_server(endpoints, port=8000):
    """
    Start an HTTP server with custom endpoint handlers.

    Args:
        endpoints: Dictionary mapping paths to handler functions
        port: Port number to listen on (default: 8000)

    Returns:
        The HTTP server instance
    """
    class DynamicHandler(server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            """Override to suppress default logging"""
            pass

        def do_GET(self):
            path = self.path
            handler = endpoints.get(path)
            if handler:
                handler(self)
            else:
                self.send_error(404, "Not Found")

    httpd = socketserver.TCPServer(("", port), DynamicHandler)

    # Start server in a background thread
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    print(f"HTTP server started on http://0.0.0.0:{port}")
    return httpd
