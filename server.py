"""
Stock Calculator - Local API Server
====================================
A lightweight HTTP server that:
  1. Serves the web UI (index.html and static files)
  2. Provides a /api/quote/<SYMBOL> endpoint using yfinance

Usage:
    py server.py
    Then open http://localhost:8000 in your browser.
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

try:
    import yfinance as yf
except ImportError:
    print("[!] yfinance is not installed. Run:  py -m pip install yfinance")
    sys.exit(1)


PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class StockHandler(SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler with an API endpoint."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # ── API route: /api/quote/<SYMBOL> ──
        if self.path.startswith("/api/quote/"):
            symbol = self.path.split("/api/quote/")[1].strip().upper()
            if not symbol:
                self._json_response(400, {"error": "Missing symbol"})
                return

            try:
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info

                price = info.get("lastPrice")
                prev_close = info.get("previousClose")
                market_cap = info.get("marketCap")
                day_high = info.get("dayHigh")
                day_low = info.get("dayLow")

                # Fallback if fast_info is empty
                if price is None:
                    hist = ticker.history(period="1d")
                    if hist.empty:
                        self._json_response(404, {
                            "error": f"No data found for '{symbol}'"
                        })
                        return
                    price = float(hist["Close"].iloc[-1])

                change = None
                change_pct = None
                if price is not None and prev_close is not None and prev_close != 0:
                    change = round(price - prev_close, 2)
                    change_pct = round((change / prev_close) * 100, 2)

                self._json_response(200, {
                    "symbol":      symbol,
                    "price":       round(float(price), 2) if price else None,
                    "prevClose":   round(float(prev_close), 2) if prev_close else None,
                    "change":      change,
                    "changePct":   change_pct,
                    "dayHigh":     round(float(day_high), 2) if day_high else None,
                    "dayLow":      round(float(day_low), 2) if day_low else None,
                    "marketCap":   int(market_cap) if market_cap else None,
                })

            except Exception as e:
                self._json_response(500, {"error": str(e)})
            return

        # ── Everything else: serve static files ──
        super().do_GET()

    def _json_response(self, status: int, data: dict):
        """Send a JSON response with CORS headers."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # Suppress noisy per-request logs
    def log_message(self, format, *args):
        if "/api/" in (args[0] if args else ""):
            super().log_message(format, *args)


if __name__ == "__main__":
    server = HTTPServer(("", PORT), StockHandler)
    print("=" * 50)
    print("  STOCK CALCULATOR - LOCAL SERVER")
    print("=" * 50)
    print(f"  Web UI  :  http://localhost:{PORT}")
    print(f"  API     :  http://localhost:{PORT}/api/quote/AAPL")
    print(f"  Stop    :  Ctrl+C")
    print("=" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()
