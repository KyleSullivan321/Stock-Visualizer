#!/usr/bin/env python3
"""Builds data.json — a snapshot of quote/summary/news for the default tickers.

Run by the GitHub Action so the Pages demo has real data without a live server.
"""
import json, time, re, datetime
import yahoo

# keep in sync with DEFAULT in index.html
TICKERS = "GOOG,AAPL,MSFT,TSLA,SPCX,PLTR,NOW,TSM,QQQ,SPY,VRT,CRWV,LLY,CEG,VST,META,RKLB,QCOM,MU".split(",")

def jget(url):
    try:
        return json.loads(yahoo.get(url))
    except Exception:
        return {}

def main():
    out = {"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes"), "stocks": {}}
    for sym in TICKERS:
        out["stocks"][sym] = {
            "quote":    jget(yahoo.chart_url(sym)),
            "intraday": jget(yahoo.intraday_url(sym)),
            "summary":  json.loads(yahoo.summary_bytes(sym) or b"{}"),
            "news":     jget(yahoo.news_url(sym)),
        }
        time.sleep(0.3)  # be polite to Yahoo
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))
    ok = sum(1 for s in out["stocks"].values()
             if s["quote"].get("chart", {}).get("result"))
    print(f"wrote data.json — {ok}/{len(TICKERS)} quotes at {out['updated']}")

if __name__ == "__main__":
    main()
