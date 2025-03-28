from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/run_python':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Python script executed!')
        else:
            super().do_GET()

httpd = HTTPServer(('localhost', 8000), MyHandler)
print("Server running at http://localhost:8000")
httpd.serve_forever()