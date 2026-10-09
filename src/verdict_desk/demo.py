from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from verdict_desk.engine import Desk

HOST = "127.0.0.1"
PORT = 8765
ROOT = Path(__file__).resolve().parents[2]
DEMO_HTML = ROOT / "docs" / "demo.html"


def main() -> None:
    desk = Desk(corpus_dir=ROOT / "corpus" / "dineflow")
    page = DEMO_HTML.read_text(encoding="utf-8")

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args) -> None:
            print(self.address_string(), "-", fmt % args)

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path in {"/", "/demo", "/demo.html"}:
                body = page.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self.send_error(404)

        def do_POST(self) -> None:
            if urlparse(self.path).path != "/v1/verdict":
                self.send_error(404)
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            try:
                question = json.loads(raw).get("question", "")
            except json.JSONDecodeError:
                self.send_error(400)
                return
            payload = json.dumps(desk.ask(question).to_dict()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    print(f"Verdict Desk demo: http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
