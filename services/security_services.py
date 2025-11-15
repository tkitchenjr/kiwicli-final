from rich.console import Console
from rich.table import Table
import db

_console = Console()


def view_all_securities() -> None:
    table = Table(title="All Securities")
    table.add_column("Ticker", style="cyan", justify="center")
    table.add_column("Issuer", style="yellow", justify="center")
    table.add_column("Name", style="white", justify="center")
    table.add_column("Price", style="green", justify="center")
    for sec in db.Securities:
        table.add_row(
            sec.get("symbol", "N/A"),
            sec.get("issuer", "N/A"),
            sec.get("name", "N/A"),
            f"${sec.get('price', 0):,.2f}"
        )
    _console.print(table)


def place_order() -> None:
    if not db.current_user:
        _console.print("Please log in to place an order.", style="red")
        return
    # Select portfolio
    user_portfolios = [p for p in db.portfolios if p.get("owner") == db.current_user.username]
    if not user_portfolios:
        _console.print("You have no portfolios. Create one first.", style="yellow")
        return
    _console.print("Your Portfolios:", style="yellow")
    for p in user_portfolios:
        _console.print(f"ID: {p['portfolio_id']} | Name: {p['name']}")
    while True:
        pid_str = _console.input("Enter Portfolio ID to invest in: ").strip()
        try:
            pid = int(pid_str)
            portfolio = next((p for p in user_portfolios if p["portfolio_id"] == pid), None)
            if not portfolio:
                _console.print("Invalid Portfolio ID.", style="red")
                continue
            break
        except Exception:
            _console.print("Invalid input.", style="red")
    # Select security
    ticker = _console.input("Enter ticker to buy: ").strip().upper()
    security = next((s for s in db.Securities if s["symbol"] == ticker), None)
    if not security:
        _console.print(f"Security '{ticker}' not found.", style="red")
        return
    # Enter quantity
    while True:
        qty_str = _console.input("Enter quantity to buy: ").strip()
        try:
            qty = float(qty_str)
            if qty <= 0:
                _console.print("Quantity must be greater than 0.", style="red")
                continue
            break
        except Exception:
            _console.print("Invalid quantity.", style="red")
    # Calculate cost
    cost = qty * security["price"]
    _console.print(f"Order: {qty} x {ticker} @ ${security['price']:,.2f} = ${cost:,.2f}", style="green")
    # Check cash balance
    cash_balance = portfolio.get("cash", 0.0)
    if cash_balance < cost:
        _console.print(f"Insufficient funds. Portfolio cash balance is ${cash_balance:,.2f}, but purchase cost is ${cost:,.2f}.", style="red")
        return
    # Deduct cost from cash and add investment to holdings
    portfolio["cash"] = cash_balance - cost
    holdings = portfolio.get("holdings", {})
    if isinstance(holdings, dict):
        holdings[ticker] = holdings.get(ticker, 0) + qty
        portfolio["holdings"] = holdings
    elif isinstance(holdings, list):
        # If holdings is a list, convert to dict
        holdings_dict = {}
        for item in holdings:
            if isinstance(item, dict) and "symbol" in item and "qty" in item:
                holdings_dict[item["symbol"]] = item["qty"]
        holdings_dict[ticker] = holdings_dict.get(ticker, 0) + qty
        portfolio["holdings"] = holdings_dict
    else:
        portfolio["holdings"] = {ticker: qty}
    _console.print(f"Added {qty} of {ticker} to portfolio '{portfolio['name']}'. New cash balance: ${portfolio['cash']:,.2f}", style="green bold")


def add_cash_to_portfolio() -> None:
    if not db.current_user:
        _console.print("Please log in to add cash.", style="red")
        return
    # Select portfolio
    user_portfolios = [p for p in db.portfolios if p.get("owner") == db.current_user.username]
    if not user_portfolios:
        _console.print("You have no portfolios. Create one first.", style="yellow")
        return
    _console.print("Your Portfolios:", style="yellow")
    for p in user_portfolios:
        _console.print(f"ID: {p['portfolio_id']} | Name: {p['name']} | Current Cash: ${p.get('cash', 0.0):,.2f}")
    while True:
        pid_str = _console.input("Enter Portfolio ID to add cash to: ").strip()
        try:
            pid = int(pid_str)
            portfolio = next((p for p in user_portfolios if p["portfolio_id"] == pid), None)
            if not portfolio:
                _console.print("Invalid Portfolio ID.", style="red")
                continue
            break
        except Exception:
            _console.print("Invalid input.", style="red")
    # Enter cash amount
    while True:
        cash_str = _console.input("Enter amount of cash to add: ").strip()
        try:
            cash_amt = float(cash_str)
            if cash_amt <= 0:
                _console.print("Amount must be greater than 0.", style="red")
                continue
            break
        except Exception:
            _console.print("Invalid amount.", style="red")
    portfolio["cash"] = portfolio.get("cash", 0.0) + cash_amt
    _console.print(f"Added ${cash_amt:,.2f} to portfolio '{portfolio['name']}'. New cash balance: ${portfolio['cash']:,.2f}", style="green bold")


__all__ = [
    "view_all_securities",
    "place_order",
    "add_cash_to_portfolio",
]
