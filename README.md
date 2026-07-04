# 📊 Stock Return Calculator

**ThinkSabio Internship 2026 — Technology Track — Project 5**

A user-friendly stock return calculator that computes investment value, current/sell value, profit or loss, and percentage return for stock trades. Includes input validation, transparent formula breakdowns, a what-if scenario table, and live stock price fetching from Yahoo Finance.

---

## 🚀 Quick Start

### Prerequisites
To use live data features locally (fetching live prices from Yahoo Finance), install the `yfinance` library:
```bash
py -m pip install yfinance
```

### Option A — Python CLI (Terminal)
Run the script to choose between Manual input, Live data, or running tests:
```bash
# Interactive mode with menu options
py stock_calculator.py

# Directly run the 5 built-in test cases
py stock_calculator.py --test
```

### Option B — Web Interface (Browser - Local)

1. **Manual Input Mode (No server needed):**
   Simply open [index.html](file:///c:/Users/drSad/OneDrive/Desktop/Project/Stock/index.html) directly in any modern web browser.

2. **Live Data Mode (Requires local backend server):**
   To fetch real-time stock prices in the web interface, start the backend server first:
   ```bash
   py server.py
   ```
   Then open [http://localhost:8000](http://localhost:8000) in your browser. Enter a symbol (e.g., `AAPL`) and click **"⚡ Fetch Price"**.

### Option C — Fully Hosted Live Web Version (Vercel)
You can deploy this project to **Vercel** with fully functioning live Yahoo Finance data using Serverless Python Functions:

1. Install the Vercel CLI (or deploy via GitHub integration):
   ```bash
   npm install -g vercel
   vercel login
   ```
2. Deploy the project from the root folder:
   ```bash
   vercel --prod
   ```
3. Open the provided `.vercel.app` URL. The Live Data mode will fetch real-time stock quotes using Vercel's cloud serverless backend!

---

## 📥 Inputs

| Input              | Required | Description                                   |
|--------------------|----------|-----------------------------------------------|
| Stock Symbol       | Optional | Ticker symbol (e.g. `AAPL`, `TSLA`)           |
| Buy Price ($)      | ✅ Yes   | Price per share at time of purchase            |
| Current Price ($)  | ✅ Yes   | Current market price or sell price per share   |
| Quantity           | ✅ Yes   | Number of shares (whole number ≥ 1)            |
| Brokerage/Fees ($) | Optional | Transaction costs; defaults to $0 if omitted  |

---

## 📤 Outputs

| Output              | Description                                          |
|---------------------|------------------------------------------------------|
| Total Investment    | Total money spent buying the shares                  |
| Current/Sell Value  | Current market value of the position                 |
| Brokerage/Fees      | Any fees deducted from profit                        |
| Profit/Loss Amount  | Dollar gain or loss after fees                       |
| Percentage Return   | Return expressed as a percentage of the investment   |
| Status              | Clear label: **Profit**, **Loss**, or **Break-Even** |

---

## 📐 Formulas

```
Investment       = Buy Price × Quantity
Current Value    = Current Price × Quantity
Profit / Loss    = Current Value − Investment − Fees
Percentage Return = (Profit / Loss ÷ Investment) × 100
```

> **Note:** Percentage return is based on total investment, not per-share price.  
> Fees are subtracted from profit, so a small gain can turn into a loss after fees.

---

## 🧪 Test Cases

The calculator ships with **5 built-in test cases** as required by the project spec:

| # | Scenario                  | Symbol | Buy ($) | Current ($) | Qty | Fees ($) | Expected  |
|---|---------------------------|--------|---------|-------------|-----|----------|-----------|
| 1 | Profit case               | AAPL   | 150.00  | 175.00      | 10  | 0.00     | Profit    |
| 2 | Loss case                 | TSLA   | 250.00  | 210.00      | 5   | 0.00     | Loss      |
| 3 | Break-even case           | MSFT   | 300.00  | 300.00      | 8   | 0.00     | Break-Even|
| 4 | Decimal price case        | AMZN   | 127.53  | 134.87      | 15  | 0.00     | Profit    |
| 5 | Fee case (profit → loss)  | GOOG   | 140.00  | 142.00      | 10  | 25.00    | Loss      |

**Run tests:**
- **Python:** `py stock_calculator.py --test`
- **Web:** Click the **"🧪 Run 5 Tests"** button in the web interface

---

## 📈 Scenario Table (Optional Extra)

Both the Python and web versions include a **what-if scenario table** that shows estimated results if the stock price moves by **±5%, ±10%, and ±20%** from the current price. This helps users visualize risk and upside potential.

---

## ✅ Validation Rules

- **Buy price** must be greater than 0.
- **Current price** must be 0 or greater.
- **Quantity** must be a positive whole number.
- **Fees** default to $0 if left empty; cannot be negative.
- All invalid inputs display a clear error message — no silent failures.

---

## 🗂 Project Files

```
Stock/
├── api/
│   └── quote.py          ← Vercel serverless Python API function (yfinance integration)
├── stock_calculator.py   ← Python CLI calculator (Manual / Live yfinance / Tests)
├── server.py             ← Local Python web/API server (for local live mode)
├── index.html            ← Web UI frontend page
├── requirements.txt      ← Python library requirements for Vercel deployment
├── vercel.json           ← Vercel rewrite configuration
└── README.md             ← This file
```

---

## ⚠️ Common Mistakes Avoided

1. **Dollar gain vs. percentage gain** — Both are shown separately with clear labels.
2. **Quantity matters** — Investment and value use `price × quantity`, not just price difference.
3. **Invalid inputs** — Validated with descriptive error messages before calculation.
4. **Transparent calculations** — Intermediate values (investment, value) are always shown, not just the final result.
5. **Fees deducted** — Fees reduce profit; a small price increase can still mean a net loss.

---

## 💻 Requirements

- **Python version:** Python 3.6+
- **Web version:** Any modern browser (Chrome, Firefox, Edge, Safari)
- **External libraries:** `yfinance` (optional, for live fetching)

---

*Built for the ThinkSabio Internship 2026 · Technology Track*


