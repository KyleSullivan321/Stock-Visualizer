# Stock Heatmap

A FinViz-style stock treemap. Tiles are **grouped by sector** and **sized by the magnitude of the day's % move** (bigger move = bigger tile); color shows direction (green up / red down) and intensity. Click any tile for a detail panel with analyst buy rating, key stats, company summary, and recent headlines.

**[Live demo →](https://kylesullivan321.github.io/Stock-Visualizer/)**

## Run locally (recommended)

```bash
python server.py
```

Then open <http://localhost:8000>. The bundled Python server proxies Yahoo Finance same-origin, so quotes, the analyst-consensus buy rating, and news all work reliably.

No dependencies — Python 3 standard library only.

## Live demo (GitHub Pages)

The [GitHub Pages demo](https://kylesullivan321.github.io/Stock-Visualizer/) has no Python server, and browsers can't call Yahoo directly (CORS). So a GitHub Action runs `fetch_data.py` every 15 min during US market hours and commits a `data.json` snapshot; the page reads that. Everything — prices, buy ratings, news — works from the snapshot. The status bar shows the snapshot time. Run locally for truly live data.

## Customize

- **Tickers** — edit the box at the top (comma-separated) and press Load, or change `DEFAULT` in `index.html`.
- **Sectors** — tickers are grouped via the hardcoded `SECTOR` map in `index.html`. Add symbols there; anything unknown lands in "Other".

## Notes

Data is from Yahoo Finance. **Not investment advice.**
