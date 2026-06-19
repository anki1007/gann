#!/usr/bin/env python3
"""
fetch_data.py  --  OHLC history for the Gann & Astro Terminal.

DATA SOURCES (as requested):
  * NSE indices (Nifty 50, Bank Nifty, Nifty 500)  ->  jugaad-data
        https://github.com/jugaad-py/jugaad-data   (NSE-native, reliable)
  * US indices  (Dow, Nasdaq 100, S&P 500)         ->  Yahoo Finance

Writes data.json (latest quote + ~2y daily OHLC per index) next to
GannAstroTerminal.html / index.html.

------------------------------------------------------------------------
INSTALL
    pip install jugaad-data yfinance
RUN
    python fetch_data.py
Then serve the folder (python -m http.server 8000) so data.json auto-loads,
or click "Load data / CSV" in the terminal's top bar.
------------------------------------------------------------------------
"""

import json
import datetime as _dt

NSE_INDICES = {                      # code -> jugaad-data index name
    "NSEI":    "NIFTY 50",
    "NSEBANK": "NIFTY BANK",
    "CNX500":  "NIFTY 500",
}
US_INDICES = {                       # code -> Yahoo symbol
    "DJIA": "^DJI",
    "NDX":  "^NDX",
    "SPX":  "^GSPC",
}


def _norm_history(df):
    """Normalise a jugaad/yfinance DataFrame into [{t,o,h,l,c}], sorted asc."""
    import pandas as pd
    cols = {str(c).lower(): c for c in df.columns}

    def pick(*names):
        for nm in names:
            if nm in cols:
                return cols[nm]
        return None

    dcol = pick("historicaldate", "date", "timestamp", "ch_timestamp")
    ocol = pick("open", "eod_open_index_val", "open_index_val")
    hcol = pick("high", "eod_high_index_val", "high_index_val")
    lcol = pick("low", "eod_low_index_val", "low_index_val")
    ccol = pick("close", "eod_close_index_val", "close_index_val")

    rows = []
    for idx, row in df.iterrows():
        try:
            raw_d = row[dcol] if dcol else idx          # yfinance: date is the index
            t = pd.to_datetime(raw_d).strftime("%Y-%m-%d")
            o = float(row[ocol]); h = float(row[hcol])
            l = float(row[lcol]); c = float(row[ccol])
        except Exception:
            continue
        rows.append({"t": t, "o": round(o, 2), "h": round(h, 2),
                     "l": round(l, 2), "c": round(c, 2)})
    rows.sort(key=lambda r: r["t"])
    # de-dup by date keeping last
    seen = {}
    for r in rows:
        seen[r["t"]] = r
    return [seen[k] for k in sorted(seen)]


def fetch_nse(code, name):
    """NSE index history via jugaad-data."""
    from jugaad_data.nse import index_df
    today = _dt.date.today()
    df = index_df(symbol=name, from_date=today - _dt.timedelta(days=760),
                  to_date=today)
    hist = _norm_history(df)
    if not hist:
        raise RuntimeError("no rows from jugaad-data")
    last = hist[-1]
    prev = hist[-2]["c"] if len(hist) > 1 else None
    return {"symbol": name, "source": "jugaad-data", "price": last["c"],
            "prevClose": prev, "date": last["t"], "currency": "INR",
            "history": hist}


def fetch_us(code, sym):
    """US index history via Yahoo Finance (yfinance, urllib fallback)."""
    try:
        import yfinance as yf
        df = yf.download(sym, period="2y", interval="1d",
                         progress=False, auto_adjust=False)
        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)
        hist = _norm_history(df)
        if not hist:
            raise RuntimeError("empty yfinance frame")
    except Exception as exc:
        print(f"    (yfinance failed: {exc}; using Yahoo chart API)")
        import urllib.request
        url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
               f"{sym}?interval=1d&range=2y")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read().decode())
        res = data["chart"]["result"][0]
        ts = res.get("timestamp") or []
        q = (res.get("indicators", {}).get("quote") or [{}])[0]
        hist = []
        for i, t in enumerate(ts):
            o, h, l, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
            if None in (o, h, l, c):
                continue
            hist.append({"t": _dt.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d"),
                         "o": round(o, 2), "h": round(h, 2),
                         "l": round(l, 2), "c": round(c, 2)})
    last = hist[-1]
    prev = hist[-2]["c"] if len(hist) > 1 else None
    return {"symbol": sym, "source": "yahoo", "price": last["c"],
            "prevClose": prev, "date": last["t"], "currency": "USD",
            "history": hist}


def main():
    out = {}
    print("Fetching NSE via jugaad-data, US via Yahoo Finance ...")
    for code, name in NSE_INDICES.items():
        try:
            out[code] = fetch_nse(code, name)
            print(f"  {code:8} {name:12} {out[code]['price']}  ({len(out[code]['history'])} candles, jugaad)")
        except Exception as exc:
            print(f"  {code:8} {name:12} FAILED: {exc}")
    for code, sym in US_INDICES.items():
        try:
            out[code] = fetch_us(code, sym)
            print(f"  {code:8} {sym:12} {out[code]['price']}  ({len(out[code]['history'])} candles, yahoo)")
        except Exception as exc:
            print(f"  {code:8} {sym:12} FAILED: {exc}")
    out["_fetched"] = _dt.datetime.utcnow().isoformat() + "Z"
    with open("data.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    n = len([k for k in out if not k.startswith("_")])
    print(f"\nWrote data.json ({n}/{len(NSE_INDICES)+len(US_INDICES)} indices).")


if __name__ == "__main__":
    main()
