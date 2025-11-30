import datetime
from rich.console import Console
from rich.table import Table
from domain.Investment import Investment
from services.transaction_services import update_transaction_record
from services.transaction_services import format_timestamp
from datetime import datetime
import db 

_console = Console()


def view_all_securities() -> None:
    table = Table(title="All Securities")
    table.add_column("Ticker", style="cyan", justify="center")
    table.add_column("Issuer", style="yellow", justify="center")
    table.add_column("Name", style="white", justify="center")
    table.add_column("Price", style="green", justify="center")
    for sec in db.securities:
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
    security = next((s for s in db.securities if s["symbol"] == ticker), None)
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
   # balance requirement
    if cost > db.current_user.balance:
        _console.print(
            f"Insufficient balance to complete the purchase. Available: ${db.current_user.balance:,.2f}",
            style="red"
        )
        return
    # update balance to reflect total
    db.current_user.balance -= cost

    # ammend security to portfolio holdings 
    holdings = portfolio.get("holdings", [])

    # Check if we already own this security - if so, update quantity
    existing_investment = None
    for investment in holdings:
        if isinstance(investment, Investment) and investment.ticker == ticker:
            existing_investment = investment
            break
    
    if existing_investment:
        # Add to existing position
        existing_investment.qty += qty
        _console.print(f"Updated existing position: {existing_investment.qty} total {ticker}", style="cyan")
    else:
        # Create new Investment object
        new_investment = Investment(ticker, qty, security["price"])
        holdings.append(new_investment)
        _console.print(f"Created new position: {qty} of {ticker}", style="cyan")

    # update transaction record
    update_transaction_record(
        transaction_id=str(len(db.transactions) + 1),
        user_id=db.current_user.username,
        portfolio_id=str(portfolio["portfolio_id"]),
        security_id=ticker,
        transaction_type="BUY",
        qty=int(qty),
        price=security["price"],
        timestamp=format_timestamp(datetime.now())
    )

    _console.print(
        f"Added {qty} of {ticker} to portfolio '{portfolio['name']}'. Remaining balance: ${db.current_user.balance:,.2f}",
        style="green bold"
    )



