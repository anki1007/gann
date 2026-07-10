# Gann & Astro Terminal

A single-file, browser-based trading terminal implementing the **Gann** and
**financial-astrology** tools from the Optuma knowledge base
(https://www.optuma.com/kb/optuma/gann-and-astro), drawn directly on an
interactive **candlestick chart** for six indices. Built in HTML + JSX (React via CDN).

Live demo: **https://anki1007.github.io/gann/**

## Run it
**Double-click `GannAstroTerminal.html`** (or `index.html`) — opens in any modern browser.
No install, no build step. (First load fetches React + Babel from a CDN, so be online once.)

## Price Chart (the analysis workspace)
Default view is a candlestick chart with the tools drawn ON the price:

- **Zoom:** mouse-wheel (anchored at the cursor) or the **+ / −** buttons.
- **Pan / scroll:** click-drag the chart, or the **◀ / ▶** buttons. **⟲ Reset** restores the default view.
- **Click any candle** to set the pivot — anchor price & date then drive EVERY tool.
- Overlays: **Pivot Points** (real prev-session P/R1-3/S1-3 + CPR, on by default), **Sq9 Levels**,
  **Gann Fan**, **Time Cycles**, **Planetary Lines**, **Moon Phases**, **Range Divisions**.
- Crosshair + OHLC readout; shows today's open and previous-session close.

## Pivot Points
A dedicated **Pivot Points** tool (and chart overlay) computes the classic floor-trader pivots,
**CPR** (Top/Bottom Central + width) and **Camarilla** levels from the **previous session's
High/Low/Close** — the standard intraday reference, grounded in real OHLC (not Square-of-9 projections).
An **Extended** mode projects **R1–R10 / S1–S10**; the Square-of-9 nearest-S/R tables (chart panel &
Sq9 Calculator) are likewise extended to 10 levels each side.

## Anchor points
The top-bar **Anchor price** dropdown resolves the pivot from the loaded price history: **Prev Close**,
**Today Open**, **Prev Week/Month/Quarter/Year High & Low**, and **Major Swing High/Low** (the largest
confirmed fractal swing in the loaded range), alongside manual entry.

## Bayer Rules
A dedicated sidebar section scans the loaded price history against a curated set of testable rules
paraphrased from George Bayer's *Handbook on Trend Determination — Astrological Rules for Traders*
(planetary stations, conjunctions and sign ingresses). Matches are marked on the chart (vertical
markers + a horizontal line at each trigger's close) with a below-chart table grouping recurring
triggers by rule/parameter.

## Data sources
- **NSE indices & F&O stocks** (219 symbols ingested from `fno.csv`, including Nifty 50 `NSEI`,
  Bank Nifty `NSEBANK`, Nifty 500 `CNX500`, Finnifty, Nifty Midcap Select, Nifty Next 50, and 210
  individual F&O stocks) → **jugaad-data** (https://github.com/jugaad-py/jugaad-data) for the core
  indices, **Yahoo Finance** in-browser for the rest.
- **US indices** (Dow `DJIA`, Nasdaq 100 `NDX`, S&P 500 `SPX`) → **Yahoo Finance**.

```bash
pip install jugaad-data yfinance
python fetch_data.py        # writes data.json: ~2y daily OHLC + latest quote per index
```
Serve the folder (`python -m http.server 8000`) so `data.json` auto-loads, or click
**Load data / CSV** (accepts `date,open,high,low,close`). The chart badge shows the live source
(`LIVE · jugaad-data` / `LIVE · yahoo`) or `DEMO DATA`.

**In-browser ⟳ Fetch live:** the hosted page also tries to pull live OHLC directly via a CORS proxy
(works well for US/Yahoo; NSE in-browser is best-effort — for reliable NSE data run `fetch_data.py`,
which uses jugaad-data). If a proxy is blocked the chart falls back to a seeded **DEMO** series.

> Note: after a redeploy, hard-refresh (Ctrl/Cmd+Shift+R) to bypass the GitHub Pages / browser cache.

## Tools (59)
**Gann (all 40 Optuma tools)** + 4 Gann charts, **Pivot Points** (classic + extended R1-R10/S1-S10),
**Astro (core 7)**: Ephemeris, Planetary Aspects, Moon Phases, Retrograde, Declination, Gann Planetary
Lines, Sq9 Planetary Intervals — and the **Bayer Rules** scanner. A few proprietary/history-dependent
tools (Mass Pressure, Overlay, Pattern Matcher) are clearly labelled rather than faked.

## Accuracy & disclaimer
Planetary positions use Paul Schlyter's compact orbital-element method (~1–2 arc-minute accuracy
for Sun/planets). For educational/analytical use only; markets carry risk and no technique
guarantees outcomes.
