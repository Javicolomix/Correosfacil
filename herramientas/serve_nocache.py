import http.server, functools, sys
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()
d = sys.argv[1]
http.server.ThreadingHTTPServer(("0.0.0.0", 5181), functools.partial(H, directory=d)).serve_forever()
