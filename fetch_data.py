#!/usr/bin/env python3
"""
fetch_data.py  --  live index quotes + OHLC history for the Gann & Astro Terminal.

Uses the Scrapling web-scraping framework
(https://github.com/anki1007/Scrapling , a fork of D4Vinci/Scrapling)
to pull the latest quote AND ~2 years of daily candles for each index from
Yahoo Finance, and write a `data.json` file next to GannAstroTerminal.html.
The terminal's Price Chart then renders real candlesticks with the Gann/Astro
tools overlaid.

------------------------------------------------------------------------
INSTALL
    pip install "scrapling[fetchers]"
    scrapling install          # one-time: browser + stealth deps
                               # (only needed for StealthyFetcher/DynamicFetcher)
RUN
    python fetch_data.py

Then either:
  * serve the folder so the page can auto-load data.json, e.g.
        python -m http.server 8000
        # open  http://localhost:8000/GannAstroTerminal.html
  * or just open GannAstroTerminal.html and click  "Load data / CSV".
------------------------------------------------------------------------
"""

import json
import datetime

# Index code  ->  Yahoo Finance symbol
SYMBOLS = {
    "NSEI":    "^NSEI",      # Nifty 50
    "NSEBANK": "^NSEBANK",   # Bank Nifty
    "CNX500":  "^CRSLDX",    # Nifty 500  (legacy code CNX500)
    "DJIA":    "^DJI",       # Dow Jones Industrial Average
    "NDX":     "^NDX",       # Nasdaq 100
    "SPX":     "^GSPC",      # S&P 500
}

CHART = ("https://query1.finance.yahoo.com/v8/finance/chart/"
         "{sym}?interval=1d&range=2y")


def fetch_text(url: str) -> str:
    """Return the raw response text for *url*.

    Primary path uses Scrapling's Fetcher (fast, TLS-impersonating HTTP).
    Falls back to the standard library so the script still works if
    Scrapling is not installed in the current environment.
    """
    try:
        from scrapling.fetchers import Fetcher
        resp = Fetcher.get(url, stealthy_headers=True)
        for attr in ("body", "text", "html_content", "content"):
            val = getattr(resp, attr, None)
            if callable(val):
                try:
                    val = val()
                except Exception:
                    val = None
            if val:
                if isinstance(val, (bytes, bytearray)):
                    return val.decode("utf-8", "replace")
                return str(val)
        return str(resp)
    except Exception as exc:                       # pragma: no cover
        print(f"    (scrapling unavailable -> stdlib fallback: {exc})")
        import urllib.request
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (GannAstroTerminal)"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", "replace")


def parse_quote(symbol: str, raw: str) -> dict:
    """Parse Yahoo's chart JSON into a quote dict with OHLC history."""
    data = json.loads(raw)
    result = data["chart"]["result"][0]
    meta = result["meta"]

    history = []
    ts = result.get("timestamp") or []
    quote = (result.get("indicators", {}).get("quote") or [{}])[0]
    o, h, l, c = (quote.get("open"), quote.get("high"),
                  quote.get("low"), quote.get("close"))
    if ts and o and h and l and c:
        for i, t in enumerate(ts):
            oo, hh, ll, cc = o[i], h[i], l[i], c[i]
            if None in (oo, hh, ll, cc):
                continue
            history.append({
                "t": datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d"),
                "o": round(oo, 2), "h": round(hh, 2),
                "l": round(ll, 2), "c": round(cc, 2),
            })

    price = meta.get("regularMarketPrice")
    if price is None and history:
        price = history[-1]["c"]
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    date = history[-1]["t"] if history else datetime.date.today().isoformat()
    change = (price - prev) if (price is not None and prev) else None
    change_pct = (change / prev * 100.0) if (change is not None and prev) else None
    return {
        "symbol": symbol,
        "price": price,
        "prevClose": prev,
        "change": change,
        "changePct": change_pct,
        "date": date,
        "currency": meta.get("currency"),
        "history": history,
    }


def main() -> None:
    out = {}
    print("Fetching index quotes + 2y daily history via Scrapling ...")
    for code, symbol in SYMBOLS.items():
        try:
            quote = parse_quote(symbol, fetch_text(CHART.format(sym=symbol)))
            out[code] = quote
            chg = quote["changePct"]
            chg_s = f"{chg:+.2f}%" if chg is not None else "  n/a "
            print(f"  {code:8} {symbol:9} {str(quote['price']):>12}  {chg_s}  "
                  f"({len(quote['history'])} candles)")
        except Exception as exc:
            print(f"  {code:8} {symbol:9} FAILED: {exc}")

    out["_fetched"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open("data.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    n = len([k for k in out if not k.startswith("_")])
    print(f"\nWrote data.json  ({n}/{len(SYMBOLS)} indices, with OHLC history).")


if __name__ == "__main__":
    main()
