import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


# Swagger JSON content (auto-documentation)
swagger_content = {
    "swagger": "2.0",
    "info": {
        "title": "Simple Python HTTP Server API",
        "version": "1.0.0"
    },
    "paths": {
        "/": {
            "get": {
                "summary": "Root endpoint",
                "description": "Returns a welcome message",
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "schema": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "/greet": {
            "get": {
                "summary": "Greeting endpoint",
                "description": "Returns a custom greeting message",
                "responses": {
                    "200": {
                        "description": "Greeting message",
                        "schema": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def guess_type(self, path):
        """Helper to guess the content type of the file being served."""
        if path.endswith(".html"):
            return "text/html"
        elif path.endswith(".css"):
            return "text/css"
        elif path.endswith(".js"):
            return "application/javascript"
        elif path.endswith(".json"):
            return "application/json"
        else:
            return "application/octet-stream"
    def do_GET(self):
        if self.path == '/':
            # Root endpoint
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            message = {"message": "Hello, welcome to the Python HTTP server!"}
            self.wfile.write(json.dumps(message).encode())
        elif self.path == '/greet':
            # Greeting endpoint
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            message = {"message": "Hello from the greeting endpoint!"}
            self.wfile.write(json.dumps(message).encode())
        elif self.path == '/swagger.json':
            # Serve the Swagger JSON
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(swagger_content).encode())
        elif self.path.startswith('/docs'):
            if self.path == '/docs' or self.path == '/docs/':
                self.path = '/docs/index.html'
            try:
                file_path = os.path.join(os.getcwd(), self.path[1:])
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', self.guess_type(self.path))
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            message = {"error": "Not found"}
            self.wfile.write(json.dumps(message).encode())


def run_http_server():
    port = 8080
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"HTTP server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_http_server()
