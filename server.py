#!/usr/bin/env python3
"""Serves index.html and proxies Yahoo Finance (same-origin, no CORS headaches).

Routes: /quote?s=SYM  (price)  ·  /summary?s=SYM  (profile+rating)  ·  /news?s=SYM
"""
import http.server, socketserver, urllib.request, urllib.parse, http.cookiejar, os

PORT = 8000
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Yahoo's quoteSummary needs a cookie + crumb. Fetch once, reuse, refresh on failure.
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
_crumb = None

def _get(url):
    return _opener.open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=10).read()

def _ensure_crumb(force=False):
    global _crumb
    if _crumb and not force:
        return _crumb
    try:
        _get("https://fc.yahoo.com")  # sets cookie (returns 404 but cookie still lands)
    except Exception:
        pass
    _crumb = _get("https://query1.finance.yahoo.com/v1/test/getcrumb").decode().strip()
    return _crumb

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p == "/quote":   return self.proxy(self.chart_url())
        if p == "/summary": return self.summary()
        if p == "/news":    return self.proxy(self.news_url())
        if p == "/":        self.path = "/index.html"
        return super().do_GET()

    def sym(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("s", [""])[0]
        return urllib.parse.quote(q.upper())

    def chart_url(self):
        return f"https://query1.finance.yahoo.com/v8/finance/chart/{self.sym()}?range=1d&interval=1d"

    def news_url(self):
        return f"https://query1.finance.yahoo.com/v1/finance/search?q={self.sym()}&newsCount=5&quotesCount=0"

    def proxy(self, url):
        try:
            data = _get(url); code = 200
        except Exception:
            data, code = b"{}", 502
        self.reply(data, code)

    def summary(self):
        mods = "assetProfile,financialData,summaryDetail,defaultKeyStatistics,price"
        for attempt in (0, 1):  # retry once with a fresh crumb on failure
            try:
                crumb = _ensure_crumb(force=bool(attempt))
                url = (f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self.sym()}"
                       f"?modules={mods}&crumb={urllib.parse.quote(crumb)}")
                return self.reply(_get(url), 200)
            except Exception:
                continue
        self.reply(b"{}", 502)

    def reply(self, data, code):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), H) as httpd:
        print(f"Stock Heatmap -> http://localhost:{PORT}")
        httpd.serve_forever()
