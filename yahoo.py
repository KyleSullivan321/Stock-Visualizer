"""Shared Yahoo Finance fetch helpers (used by server.py and fetch_data.py)."""
import urllib.request, urllib.parse, http.cookiejar

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
_crumb = None

def get(url):
    return _opener.open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=15).read()

def ensure_crumb(force=False):
    global _crumb
    if _crumb and not force:
        return _crumb
    try:
        get("https://fc.yahoo.com")  # sets cookie (returns 404 but cookie still lands)
    except Exception:
        pass
    _crumb = get("https://query1.finance.yahoo.com/v1/test/getcrumb").decode().strip()
    return _crumb

def chart_url(sym):
    # 1y of daily candles → enough to derive 1D/1W/1M/1Y changes from one call
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range=1y&interval=1d"

def intraday_url(sym):
    # today's 5-min candles → 15-min change
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range=1d&interval=5m"

def news_url(sym):
    return f"https://query1.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(sym)}&newsCount=5&quotesCount=0"

SUMMARY_MODULES = "assetProfile,financialData,summaryDetail,defaultKeyStatistics,price"

def summary_bytes(sym):
    """quoteSummary needs a crumb; retry once with a fresh crumb on failure."""
    for attempt in (0, 1):
        try:
            crumb = ensure_crumb(force=bool(attempt))
            url = (f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(sym)}"
                   f"?modules={SUMMARY_MODULES}&crumb={urllib.parse.quote(crumb)}")
            return get(url)
        except Exception:
            continue
    return b"{}"
