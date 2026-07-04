"""
Stock Return Calculator
=======================
A user-friendly calculator that computes investment value, current/sell value,
profit or loss, and percentage return for stock trades.

Supports both manual input and live price fetching via Yahoo Finance (yfinance).

Author : ThinkSabio Internship 2026
Track  : Technology Track - Project 5
"""

import sys

# ──────────────────────────────────────────────
#  Yahoo Finance helper
# ──────────────────────────────────────────────

def fetch_live_price(symbol: str) -> float | None:
    """
    Fetch the latest market price for a stock symbol using yfinance.
    Returns the price as a float, or None if the lookup fails.
    """
    try:
        import yfinance as yf
    except ImportError:
        print("  [!] yfinance is not installed.")
        print("      Run:  py -m pip install yfinance")
        return None

    try:
        ticker = yf.Ticker(symbol)
        # fast_info provides the most recent market price
        price = ticker.fast_info.get("lastPrice")
        if price is None:
            # fallback: try history
            hist = ticker.history(period="1d")
            if hist.empty:
                print(f"  [!] No data found for symbol '{symbol}'.")
                return None
            price = float(hist["Close"].iloc[-1])
        return round(float(price), 2)
    except Exception as e:
        print(f"  [!] Error fetching price for '{symbol}': {e}")
        return None


# ──────────────────────────────────────────────
#  Core calculation function
# ──────────────────────────────────────────────

def calculate_return(buy_price: float,
                     current_price: float,
                     quantity: int,
                     fees: float = 0.0) -> dict:
    """
    Calculate stock return metrics.

    Parameters
    ----------
    buy_price      : Price per share at purchase.
    current_price  : Current / sell price per share.
    quantity       : Number of shares.
    fees           : Optional brokerage or transaction fees.

    Returns
    -------
    dict with keys:
        investment, current_value, profit_loss, percentage_return, status
    """
    investment     = buy_price * quantity
    current_value  = current_price * quantity
    profit_loss    = current_value - investment - fees
    pct_return     = (profit_loss / investment) * 100 if investment != 0 else 0.0

    if profit_loss > 0:
        status = "[+] PROFIT"
    elif profit_loss < 0:
        status = "[-] LOSS"
    else:
        status = "[=] BREAK-EVEN"

    return {
        "investment":        round(investment, 2),
        "current_value":     round(current_value, 2),
        "fees":              round(fees, 2),
        "profit_loss":       round(profit_loss, 2),
        "percentage_return": round(pct_return, 2),
        "status":            status,
    }


# ──────────────────────────────────────────────
#  Pretty-print a single result
# ──────────────────────────────────────────────

def print_result(symbol: str, result: dict) -> None:
    """Display calculation results with clear labels."""
    print()
    print("=" * 50)
    print(f"  Stock Return Report -- {symbol.upper()}")
    print("=" * 50)
    print(f"  Total Investment     : ${result['investment']:>12,.2f}")
    print(f"  Current / Sell Value : ${result['current_value']:>12,.2f}")
    print(f"  Brokerage / Fees     : ${result['fees']:>12,.2f}")
    print("-" * 50)
    print(f"  Profit / Loss        : ${result['profit_loss']:>12,.2f}")
    print(f"  Percentage Return    :  {result['percentage_return']:>11,.2f}%")
    print("-" * 50)
    print(f"  Result               :  {result['status']}")
    print("=" * 50)


# ──────────────────────────────────────────────
#  Scenario table (optional extra)
# ──────────────────────────────────────────────

def print_scenario_table(buy_price: float,
                         current_price: float,
                         quantity: int,
                         fees: float = 0.0) -> None:
    """
    Show what happens if the stock moves +/-5%, +/-10%, +/-20%
    from the *current* price.
    """
    changes = [-20, -10, -5, 0, 5, 10, 20]

    print()
    print("+" + "-" * 65 + "+")
    print("|" + "  SCENARIO TABLE".center(65) + "|")
    print("+" + "-" * 11 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 22 + "+")
    print("|  Change   |  New Price   |  Profit/Loss |  Return %            |")
    print("+" + "-" * 11 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 22 + "+")

    for pct in changes:
        new_price = current_price * (1 + pct / 100)
        r = calculate_return(buy_price, new_price, quantity, fees)
        marker = " <- current" if pct == 0 else ""
        sign = "+" if pct > 0 else ""
        print(
            f"|  {sign}{pct:>4}%   |  ${new_price:>9,.2f} |  "
            f"${r['profit_loss']:>9,.2f} |  {r['percentage_return']:>8,.2f}%{marker:<11}|"
        )

    print("+" + "-" * 11 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 22 + "+")


# ──────────────────────────────────────────────
#  Input helpers with validation
# ──────────────────────────────────────────────

def get_positive_float(prompt: str, allow_zero: bool = False) -> float:
    """Keep asking until the user enters a valid non-negative number."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("  [!] Input cannot be empty. Please try again.")
            continue
        try:
            value = float(raw)
        except ValueError:
            print("  [!] Please enter a valid number.")
            continue
        if value < 0:
            print("  [!] Value cannot be negative. Please try again.")
            continue
        if value == 0 and not allow_zero:
            print("  [!] Value must be greater than zero.")
            continue
        return value


def get_positive_int(prompt: str) -> int:
    """Keep asking until the user enters a valid positive integer."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("  [!] Input cannot be empty. Please try again.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("  [!] Please enter a whole number (no decimals).")
            continue
        if value <= 0:
            print("  [!] Quantity must be at least 1.")
            continue
        return value


def get_fees() -> float:
    """Prompt for optional brokerage/fees with validation."""
    fees_input = input("  Enter brokerage / fees ($) [0 if none]: ").strip()
    fees = 0.0
    if fees_input:
        try:
            fees = float(fees_input)
            if fees < 0:
                print("  [!] Fees cannot be negative; defaulting to $0.")
                fees = 0.0
        except ValueError:
            print("  [!] Invalid fee value; defaulting to $0.")
    return fees


# ──────────────────────────────────────────────
#  Interactive mode -- MANUAL input
# ──────────────────────────────────────────────

def manual_mode() -> None:
    """Collect all inputs manually from the user."""
    print("\n" + "-" * 50)
    print("  MODE: Manual Input")
    print("-" * 50)

    symbol        = input("\n  Enter stock symbol (e.g. AAPL): ").strip() or "N/A"
    buy_price     = get_positive_float("  Enter buy price per share ($): ")
    current_price = get_positive_float("  Enter current / sell price per share ($): ")
    quantity      = get_positive_int("  Enter quantity (number of shares): ")
    fees          = get_fees()

    result = calculate_return(buy_price, current_price, quantity, fees)
    print_result(symbol, result)

    show = input("\n  Show scenario table? (y/n): ").strip().lower()
    print()
    if show in ("y", "yes"):
        print_scenario_table(buy_price, current_price, quantity, fees)


# ──────────────────────────────────────────────
#  Interactive mode -- LIVE Yahoo Finance data
# ──────────────────────────────────────────────

def live_mode() -> None:
    """Fetch the current price from Yahoo Finance; user provides the rest."""
    print("\n" + "-" * 50)
    print("  MODE: Live Data (Yahoo Finance)")
    print("-" * 50)

    symbol = input("\n  Enter stock symbol (e.g. AAPL): ").strip().upper()
    if not symbol:
        print("  [!] Symbol cannot be empty.")
        return

    print(f"  Fetching live price for {symbol}...")
    live_price = fetch_live_price(symbol)

    if live_price is None:
        print("  [!] Could not retrieve live price. Falling back to manual input.")
        current_price = get_positive_float("  Enter current / sell price per share ($): ")
    else:
        print(f"  [OK] Live price for {symbol}: ${live_price:,.2f}")
        use_it = input("  Use this price? (y/n): ").strip().lower()
        if use_it in ("n", "no"):
            current_price = get_positive_float("  Enter current / sell price per share ($): ")
        else:
            current_price = live_price

    buy_price = get_positive_float("  Enter your buy price per share ($): ")
    quantity  = get_positive_int("  Enter quantity (number of shares): ")
    fees      = get_fees()

    result = calculate_return(buy_price, current_price, quantity, fees)
    print_result(symbol, result)

    show = input("\n  Show scenario table? (y/n): ").strip().lower()
    print()
    if show in ("y", "yes"):
        print_scenario_table(buy_price, current_price, quantity, fees)


# ──────────────────────────────────────────────
#  Main menu
# ──────────────────────────────────────────────

def main_menu() -> None:
    """Display the main menu and route to the selected mode."""
    print("\n" + "=" * 50)
    print("  STOCK RETURN CALCULATOR")
    print("=" * 50)
    print()
    print("  Choose an input mode:")
    print()
    print("    [1] Manual Input   -- enter all values yourself")
    print("    [2] Live Data      -- fetch current price from Yahoo Finance")
    print("    [3] Run Tests      -- execute 5 built-in test cases")
    print("    [0] Exit")
    print()

    choice = input("  Your choice (0-3): ").strip()

    if choice == "1":
        manual_mode()
    elif choice == "2":
        live_mode()
    elif choice == "3":
        run_tests()
    elif choice == "0":
        print("  Goodbye!")
        sys.exit(0)
    else:
        print("  [!] Invalid choice. Please enter 1, 2, 3, or 0.")


# ──────────────────────────────────────────────
#  Built-in test suite (5 required test cases)
# ──────────────────────────────────────────────

def run_tests() -> None:
    """Run five test cases as required by the project spec."""

    test_cases = [
        {
            "name": "Test 1 - Profit Case",
            "symbol": "AAPL",
            "buy": 150.00,
            "current": 175.00,
            "qty": 10,
            "fees": 0.00,
            "expected_status": "[+] PROFIT",
        },
        {
            "name": "Test 2 - Loss Case",
            "symbol": "TSLA",
            "buy": 250.00,
            "current": 210.00,
            "qty": 5,
            "fees": 0.00,
            "expected_status": "[-] LOSS",
        },
        {
            "name": "Test 3 - Break-Even Case",
            "symbol": "MSFT",
            "buy": 300.00,
            "current": 300.00,
            "qty": 8,
            "fees": 0.00,
            "expected_status": "[=] BREAK-EVEN",
        },
        {
            "name": "Test 4 - Decimal Price Case",
            "symbol": "AMZN",
            "buy": 127.53,
            "current": 134.87,
            "qty": 15,
            "fees": 0.00,
            "expected_status": "[+] PROFIT",
        },
        {
            "name": "Test 5 - Fee Case (profit eaten by fees)",
            "symbol": "GOOG",
            "buy": 140.00,
            "current": 142.00,
            "qty": 10,
            "fees": 25.00,
            "expected_status": "[-] LOSS",
        },
    ]

    print("\n" + "=" * 60)
    print("  RUNNING 5 TEST CASES")
    print("=" * 60)

    all_passed = True

    for tc in test_cases:
        result = calculate_return(tc["buy"], tc["current"], tc["qty"], tc["fees"])
        passed = (result["status"] == tc["expected_status"])
        all_passed = all_passed and passed
        tag = "PASS" if passed else "FAIL"

        print(f"\n  {tag}  {tc['name']}")
        print(f"         Symbol          : {tc['symbol']}")
        print(f"         Buy Price       : ${tc['buy']:,.2f}")
        print(f"         Current Price   : ${tc['current']:,.2f}")
        print(f"         Quantity        : {tc['qty']}")
        print(f"         Fees            : ${tc['fees']:,.2f}")
        print(f"         -- Results --")
        print(f"         Investment      : ${result['investment']:,.2f}")
        print(f"         Current Value   : ${result['current_value']:,.2f}")
        print(f"         Profit/Loss     : ${result['profit_loss']:,.2f}")
        print(f"         Return %        : {result['percentage_return']:.2f}%")
        print(f"         Status          : {result['status']}")

    print("\n" + "-" * 60)
    print(f"  {'ALL 5 TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("-" * 60)


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        while True:
            try:
                main_menu()
            except KeyboardInterrupt:
                print("\n  Goodbye!")
                break
