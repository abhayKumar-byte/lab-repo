from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import psycopg


def get_db_password():
    with open("/run/secrets/db_password", "r") as f:
        return f.read().strip()


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=get_db_password(),
    )

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy",
                "service": "docker-backend"
            }

            data = json.dumps(response).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            self.wfile.write(data)
            return

        try:
            conn = get_db_connection()

            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users ORDER BY id")
                users = cursor.fetchall()

            conn.close()

            response = {
                "status": "success",
                "users": [
                    {
                        "id": user[0],
                        "name": user[1],
                        "email": user[2]
                    }
                    for user in users
                ]
            }

            data = json.dumps(response).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            self.wfile.write(data)

        except Exception as e:
            response = {
                "status": "error",
                "message": str(e)
            }

            data = json.dumps(response).encode()

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            self.wfile.write(data)


server = HTTPServer(("0.0.0.0", 3000), Handler)

print("Backend running on port 3000 - Docker Lab")

server.serve_forever()
