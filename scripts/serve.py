#!/usr/bin/env python3
"""Simple HTTP server — avoids os.getcwd() for macOS sandbox compatibility."""
import os
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
handler = partial(SimpleHTTPRequestHandler, directory=directory)
print(f"Serving {directory} on http://localhost:{port}")
sys.stdout.flush()
HTTPServer(("", port), handler).serve_forever()
