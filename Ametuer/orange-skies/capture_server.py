import http.server
import json
import datetime

log_path = r"requests.log"

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            length = 0
        body = self.rfile.read(length) if length else b''
        entry = {
            'time': datetime.datetime.utcnow().isoformat() + 'Z',
            'path': self.path,
            'headers': {k: v for k, v in self.headers.items()},
            'body': body.decode('utf-8', errors='replace'),
        }
        with open(log_path, 'a', encoding='utf-8') as log:
            log.write(json.dumps(entry) + '\n')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('0.0.0.0', 8000), Handler)
    print('Listening on 0.0.0.0:8000', flush=True)
    server.serve_forever()
