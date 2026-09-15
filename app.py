import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = {
            "message": "Hello from Docker!",
             "service": os.getenv("SERVICE_NAME", "unknown"),
            "status": "running"
        }

        data = json.dumps(response).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)


server = HTTPServer(("0.0.0.0", 3000), Handler)

print("Backend running on port 3000")

server.serve_forever()
