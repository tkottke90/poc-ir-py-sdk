from http import server
import socketserver
import threading
from server.context import ServerContext




def start_server(endpoints, context: ServerContext, port=8000):
    """
    Start an HTTP server with custom endpoint handlers.

    Args:
        endpoints: Dictionary mapping paths to handler functions
        context: ServerContext with dependencies (ir, state, logger)
        port: Port number to listen on (default: 8000)

    Returns:
        The HTTP server instance
    """
    class DynamicHandler(server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="static", **kwargs)

        def log_message(self, format, *args):
            """Override to suppress default logging"""
            pass

        def do_GET(self):
            path = self.path
            handler = endpoints.get(path)
            if handler:
                handler(self, context)
                return
            
            super().do_GET()

        def do_POST(self):
            path = self.path
            handler = endpoints.get(path)
            if handler:
                handler(self, context)
            else:
                self.send_error(404, "Not Found")

    httpd = socketserver.TCPServer(("", port), DynamicHandler)

    # Start server in a background thread
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    print(f"HTTP server started on http://0.0.0.0:{port}")
    context.logger.info(f"HTTP server started on port {port}")
    return httpd

