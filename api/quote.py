from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import yfinance as yf

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Get symbol from query parameter (?symbol=AAPL)
        symbol = query_params.get("symbol", [""])[0].strip().upper()

        if not symbol:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing symbol"}).encode("utf-8"))
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
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": f"No data found for '{symbol}'"}).encode("utf-8"))
                    return
                price = float(hist["Close"].iloc[-1])

            change = None
            change_pct = None
            if price is not None and prev_close is not None and prev_close != 0:
                change = round(price - prev_close, 2)
                change_pct = round((change / prev_close) * 100, 2)

            response_data = {
                "symbol":      symbol,
                "price":       round(float(price), 2) if price else None,
                "prevClose":   round(float(prev_close), 2) if prev_close else None,
                "change":      change,
                "changePct":   change_pct,
                "dayHigh":     round(float(day_high), 2) if day_high else None,
                "dayLow":      round(float(day_low), 2) if day_low else None,
                "marketCap":   int(market_cap) if market_cap else None,
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return
