# Stock Heatmap

A FinViz-style stock treemap. Tiles are **grouped by sector** and **sized by the magnitude of the day's % move** (bigger move = bigger tile); color shows direction (green up / red down) and intensity. Click any tile for a detail panel with analyst buy rating, key stats, company summary, and recent headlines.

![Stock Heatmap](docs/screenshot.png)

## Run locally (recommended)

```bash
python server.py
```

Then open <http://localhost:8000>. The bundled Python server proxies Yahoo Finance same-origin, so quotes, the analyst-consensus buy rating, and news all work reliably.

No dependencies — Python 3 standard library only.

## Live demo (GitHub Pages)

The [GitHub Pages demo](https://kylesullivan321.github.io/Stock-Visualizer/) runs without the Python server by falling back to a public CORS proxy against Yahoo. Prices work; the buy-rating/company-summary panel needs Yahoo's authenticated endpoint and is only fully available in the local `server.py` mode.

## Customize

- **Tickers** — edit the box at the top (comma-separated) and press Load, or change `DEFAULT` in `index.html`.
- **Sectors** — tickers are grouped via the hardcoded `SECTOR` map in `index.html`. Add symbols there; anything unknown lands in "Other".

## Notes

Data is from Yahoo Finance. **Not investment advice.**
