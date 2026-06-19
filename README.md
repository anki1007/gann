# Gann & Astro Terminal

A single-file, browser-based trading terminal implementing the **Gann** and
**financial-astrology** tools from the Optuma knowledge base
(https://www.optuma.com/kb/optuma/gann-and-astro), drawn directly on an
interactive **candlestick chart** for six indices. Built in HTML + JSX
(React via CDN). Live data via the Scrapling framework
(https://github.com/anki1007/Scrapling).

## Run it
**Double-click `GannAstroTerminal.html`** — opens in any modern browser.
No install, no build step. (First load fetches React + Babel from a CDN, so be online once.)

## Price Chart (the analysis workspace)
The default view is a candlestick chart of the selected index with the tools drawn ON the price:

- **Click any candle** to set it as the pivot — the anchor price & date then drive EVERY tool.
- Toggle overlays: **Sq9 Levels** (horizontal S/R), **Gann Fan** (rays from the pivot),
  **Time Cycles** (vertical 30–360-day lines), **Planetary Lines** (price = longitude × factor),
  **Moon Phases** (new/full markers), **Range Divisions** (1/8th retracements).
- Crosshair readout, range selector (90–400 bars), and forward projection space for cycles & fans.

Data: works out-of-the-box on a **seeded demo series** (badge shows DEMO). For real candles, run
`fetch_data.py` or load your own **CSV** (`date,open,high,low,close`) via **Load data / CSV** in the top bar.

## Layout
Collapsible sidebar (◀ Hide / ▶ TOOLS) groups: Overview · Gann Tools · Astro Tools · Gann Charts.
Top bar sets **Index**, **Anchor price**, **Date** — shared by all tools and the chart.

## Indices
`NSEI` Nifty 50 · `NSEBANK` Bank Nifty · `CNX500` Nifty 500 · `DJIA` Dow Jones ·
`NDX` Nasdaq 100 · `SPX` S&P 500.

## Tools (57)
**Gann (all 40 Optuma tools):** Square of 9 family (Calculator, Wheel, Static, Dynamic, Dates,
Intervals, Gann Fan), Gann Fan/Angles (static + dynamic), Dynamic Gann Levels, Gann Box, Gann Squares,
Hex Intervals, Wheel of 24, Divisions of 3rds/8ths (price + time), Measured/Single/High-Low/Zero
degree lines, Zero Price Fan, Seven Times the Base, Triple Octave (price + time), Pyrapoint,
Pattern of Vibration, Mass Pressure, Number Searcher, Day Count/Cycles, Time-Price Labels/Measure,
Square Range/Marker family, Top/Bottom, Overlay, Pattern Matcher.

**Gann Charts:** The Square of Nine · The Square of Four · The Hexagon Chart · The Wheel of 24.

**Astro (core 7):** Ephemeris · Planetary Aspects (+grid) · Moon Phases · Planetary Retrograde ·
Declination · Gann Planetary Lines · Square-of-9 Planetary Intervals.

> A few Gann tools that are proprietary or need full price history — **Mass Pressure** (simplified
> seasonal model), **Overlay Tool** (linear scaler), **Pattern Matcher** (placeholder) — are clearly
> labelled inside the app rather than faked.

## Live data (optional)
    pip install "scrapling[fetchers]"
    python fetch_data.py          # writes data.json: latest quote + 2y daily OHLC per index

Then serve the folder (`python -m http.server 8000`) so `data.json` auto-loads, or click
**Load data / CSV**. The chart badge shows **LIVE OHLC** when real candles are loaded, **DEMO DATA** otherwise.

## Accuracy & disclaimer
Planetary positions use Paul Schlyter's compact orbital-element method — geocentric ecliptic
longitudes accurate to ~1–2 arc-minutes for the Sun and planets, a few arc-minutes for the Moon.
Verified against equinox/solstice Sun longitudes and inner-planet elongation limits.
For educational/analytical use only; markets carry risk and no technique guarantees outcomes.
