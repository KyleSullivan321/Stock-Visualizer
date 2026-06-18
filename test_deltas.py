"""Self-check for the timeframe delta math mirrored from index.html. Run: python test_deltas.py"""

def deltas(price, daily_closes, intraday_closes):
    c = [x for x in daily_closes if x is not None]
    ic = [x for x in intraday_closes if x is not None]
    chg = lambda then: (price - then) / then * 100 if then else None
    at = lambda n: c[len(c) - 1 - n]
    return {
        "15m": chg(ic[-4]) if len(ic) > 3 else None,
        "1D":  chg(at(1)),
        "1W":  chg(at(5)),
        "1M":  chg(at(21)),
        "1Y":  chg(c[0]),
    }

if __name__ == "__main__":
    # 252 daily closes: 100 a year ago, ramping to 200 yesterday, price 210 today
    daily = [100 + i * (100 / 251) for i in range(252)]  # c[0]=100 ... c[-1]=200
    price = 210.0
    intra = [205, 206, 207, 208, 209, 210]               # last 6 5-min closes

    d = deltas(price, daily, intra)
    assert round(d["1Y"], 1) == 110.0, d["1Y"]            # 210 vs 100
    assert round(d["1D"], 2) == round((210 - daily[-2]) / daily[-2] * 100, 2), d["1D"]
    assert round(d["15m"], 2) == round((210 - 207) / 207 * 100, 2), d["15m"]  # 3 back = 207
    assert d["1W"] is not None and d["1M"] is not None
    # prior close must NOT be the year-ago value (the bug we fixed): 1D << 1Y
    assert d["1D"] < d["1Y"] / 5, f"1D ({d['1D']}) should be far smaller than 1Y ({d['1Y']})"
    print("deltas OK:", {k: round(v, 2) for k, v in d.items()})
