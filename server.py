#!/usr/bin/env python3
"""Serves index.html and proxies Yahoo Finance (same-origin, no CORS headaches).

Routes: /quote?s=SYM  (price)  ·  /summary?s=SYM  (profile+rating)  ·  /news?s=SYM
"""
import http.server, socketserver, urllib.parse, os
import yahoo

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p == "/quote":   return self.proxy(yahoo.chart_url(self.sym()))
        if p == "/intraday":return self.proxy(yahoo.intraday_url(self.sym()))
        if p == "/summary": return self.reply(yahoo.summary_bytes(self.sym()))
        if p == "/news":    return self.proxy(yahoo.news_url(self.sym()))
        if p == "/":        self.path = "/index.html"
        return super().do_GET()

    def sym(self):
        return urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("s", [""])[0].upper()

    def proxy(self, url):
        try:
            self.reply(yahoo.get(url))
        except Exception:
            self.reply(b"{}", 502)

    def reply(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), H) as httpd:
        print(f"Stock Heatmap -> http://localhost:{PORT}")
        httpd.serve_forever()
