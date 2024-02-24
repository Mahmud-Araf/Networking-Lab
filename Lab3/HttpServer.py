from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
import os
import json

PATH = os.getcwd()+"/files"

PORT = 12349

class FileHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/list':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            files = os.listdir(PATH)
            print(files)
            self.wfile.write(json.dumps(files).encode())
        elif self.path.startswith('/download/'):
            filename = self.path[10:]
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                with open(os.path.join('files', filename), 'rb') as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/upload/'):
            filename = self.path[8:]
            content_length = int(self.headers['Content-Length'])
            file_content = self.rfile.read(content_length)
            with open(os.path.join('files', filename), 'wb') as file:
                file.write(file_content)

            self.send_response(201)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File uploaded successfully')

if __name__ == "__main__":
    os.makedirs('files', exist_ok=True)
    handler = FileHandler
    with ThreadingTCPServer(("", PORT), handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()