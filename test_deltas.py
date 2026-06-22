"""Self-check for the timeframe delta math mirrored from index.html. Run: python test_deltas.py"""
import datetime

DAY = 86400

def deltas(price, now_ts, daily, intraday_closes):
    """daily: list of (timestamp, close). Mirrors fetchQuote in index.html."""
    s = [(t, c) for t, c in daily if c is not None]
    same_day = lambda a, b: (datetime.datetime.utcfromtimestamp(a).date()
                             == datetime.datetime.utcfromtimestamp(b).date())
    if s and same_day(s[-1][0], now_ts):   # drop today's in-progress candle
        s = s[:-1]
    c = [x[1] for x in s]
    ic = [x for x in intraday_closes if x is not None]
    chg = lambda then: (price - then) / then * 100 if then else None
    at = lambda n: c[len(c) - n]           # n completed days back (1 = yesterday)
    return {
        "15m": chg(ic[-4]) if len(ic) > 3 else None,
        "1D":  chg(at(1)),
        "1W":  chg(at(5)),
        "1M":  chg(at(21)),
        "1Y":  chg(c[0]),
    }

if __name__ == "__main__":
    now = 1_780_000_000                                     # a realistic recent epoch
    # 252 completed prior days: 100 → 200, each on its own UTC day
    daily = [(now - (252 - i) * DAY, 100 + i * (100 / 251)) for i in range(252)]
    yest = daily[-1][1]                                     # yesterday's close ≈ 200
    price = 210.0
    intra = [205, 206, 207, 208, 209, 210]

    # case A: no today candle yet (intraday, series ends yesterday)
    a = deltas(price, now, daily, intra)
    assert round(a["1D"], 2) == round((price - yest) / yest * 100, 2), a["1D"]
    assert round(a["1Y"], 1) == 110.0, a["1Y"]
    assert round(a["15m"], 2) == round((210 - 207) / 207 * 100, 2), a["15m"]

    # case B: today's candle already appended — must be dropped, 1D identical to A
    daily_b = daily + [(now, price)]
    b = deltas(price, now, daily_b, intra)
    assert b["1D"] == a["1D"], (a["1D"], b["1D"])
    assert b["1Y"] == a["1Y"], (a["1Y"], b["1Y"])

    # the bug we fixed: 1D must be a small daily move, never the year-ago value
    assert a["1D"] < a["1Y"] / 5, f"1D ({a['1D']}) should be << 1Y ({a['1Y']})"
    print("deltas OK (today-candle drop works):", {k: round(v, 2) for k, v in b.items()})
