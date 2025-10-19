
from rich.console import Console
from rich.table import Table
import db
import session

#Define Portfolio class
class Portfolio():
    def __init__(self, id: int, name:str, description:str, holdings:dict):
        self.id = id
        self.name = name
        self.description = description
        self.holdings = holdings

_console = Console()

# View holdings for a given portfolio
def view_holdings(portfolio_id: int) -> None:
    portfolio = next((p for p in db.portfolios if p["portfolio_id"] == portfolio_id), None)
    if not portfolio:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
        return
    
    # Enforce ownership (admin can view all)
    if not session.current_user:
        _console.print("Please log in to view portfolios.", style="red")
        return
    owner = portfolio.get("owner")
    if session.current_user.username != "admin" and owner != session.current_user.username:
        _console.print("Access denied: you cannot view another user's portfolio.", style="red")
        return
    
    holdings_raw = portfolio.get("holdings", [])

    # Build a price lookup for securities
    price_by_symbol = {s.get("symbol"): float(s.get("price", 0)) for s in getattr(db, "Securities", [])}

    # Normalize holdings into a list of (symbol, qty) tuples
    normalized: list[tuple[str, int]] = []

    def add_pair(sym: str, qty_val) -> None:
        try:
            qty = int(qty_val)
        except Exception:
            qty = 1
        if sym:
            normalized.append((sym.strip(), qty))

    if isinstance(holdings_raw, dict):
        # {"AAPL": 10, "MSFT": 5}
        for sym, qty in holdings_raw.items():
            add_pair(sym, qty)
    elif isinstance(holdings_raw, (list, set, tuple)):
        for item in holdings_raw:
            if isinstance(item, dict):
                # {"symbol": "AAPL", "qty": 10}
                add_pair(item.get("symbol"), item.get("qty", 1))
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                add_pair(str(item[0]), item[1])
            elif isinstance(item, str):
                # Could be "AAPL" or "AAPL,MSFT" (comma-separated)
                parts = [p.strip() for p in item.split(",") if p.strip()]
                if len(parts) > 1:
                    for sym in parts:
                        add_pair(sym, 1)
                else:
                    add_pair(item, 1)
            else:
                # Fallback: string conversion
                add_pair(str(item), 1)
    elif isinstance(holdings_raw, str):
        # Single string possibly comma-separated
        for sym in [p.strip() for p in holdings_raw.split(",") if p.strip()]:
            add_pair(sym, 1)

    # Render table
    table = Table(title=f"Holdings for Portfolio {portfolio['name']}")
    table.add_column("Security", style="yellow", justify="center", no_wrap=True)
    table.add_column("Qty", style="cyan", justify="center", no_wrap=True)
    table.add_column("Balance", style="green", justify="center", no_wrap=True)

    total_value = 0.0
    for sym, qty in normalized:
        price = price_by_symbol.get(sym, 0.0)
        balance = price * qty
        total_value += balance
        table.add_row(sym, str(qty), f"${balance:,.2f}")

    # Add a footer row with total
    if normalized:
        table.add_row("", "", f"${total_value:,.2f}")

    _console.print(table)

# Create a new portfolio
def create_portfolio() -> None:
    if not session.current_user:
        _console.print("Please log in to create a portfolio.", style="red")
        return
    _console.print("\n   Create Portfolio   ", style="yellow")
    name = _console.input("Portfolio Name: ")
    description = _console.input("Description: ")
    new_id = max([p["portfolio_id"] for p in db.portfolios], default=0) + 1
    db.portfolios.append({
        "portfolio_id": new_id,
        "name": name,
        "description": description,
        "owner": session.current_user.username,
        "holdings": []
    })
    _console.print(f"Portfolio '{name}' created with ID {new_id}.", style="green")

# Delete a portfolio by ID
def delete_portfolio(portfolio_id: int) -> None:
    if not session.current_user:
        _console.print("Please log in to delete a portfolio.", style="red")
        return
    idx = next((i for i, p in enumerate(db.portfolios) if p["portfolio_id"] == portfolio_id), None)
    if idx is None:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
        return
    portfolio = db.portfolios[idx]
    owner = portfolio.get("owner")
    if session.current_user.username != "admin" and owner != session.current_user.username:
        _console.print("Access denied: you cannot delete another user's portfolio.", style="red")
        return
    name = portfolio["name"]
    del db.portfolios[idx]
    _console.print(f"Portfolio '{name}' deleted.", style="green")

# Liquidate holdings for a portfolio
def liquidate_holdings(portfolio_id: int) -> None:
    if not session.current_user:
        _console.print("Please log in to liquidate holdings.", style="red")
        return
    portfolio = next((p for p in db.portfolios if p["portfolio_id"] == portfolio_id), None)
    if not portfolio:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
        return
    owner = portfolio.get("owner")
    if session.current_user.username != "admin" and owner != session.current_user.username:
        _console.print("Access denied: you cannot modify another user's portfolio.", style="red")
        return
    portfolio["holdings"] = []
    _console.print(f"All holdings liquidated for portfolio '{portfolio['name']}'.", style="green")