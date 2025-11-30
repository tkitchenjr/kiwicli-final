from rich.console import Console
from rich.table import Table
from domain.Investment import Investment
import db

_console = Console()


def view_all_portfolios() -> None:
    if not db.current_user:
        _console.print("Please log in to view portfolios.", style="red")
        return
    
    # Filter portfolios for current user (admin can see all)
    if db.current_user.username == "admin":
        user_portfolios = db.portfolios
    else:
        user_portfolios = [p for p in db.portfolios if p.get("owner") == db.current_user.username]
    
    if not user_portfolios:
        _console.print("You have no portfolios yet.", style="yellow")
        return
    
    # Create a summary table
    table = Table(title=f"Portfolios for {db.current_user.firstname}")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", justify="center", style="yellow", no_wrap=True)
    table.add_column("Description", justify="center", style="white", no_wrap=True)

    for portfolio in user_portfolios:
        portfolio_id = portfolio.get("portfolio_id", "N/A")
        name = portfolio.get("name", "Unnamed")
        description = portfolio.get("description", "")
        table.add_row(str(portfolio_id),name,description)
    
    _console.print(table)
    _console.print(f"Available Balance: ${db.current_user.balance:,.2f}", style="green bold")
    # Prompt to view holdings for a selected portfolio
    if user_portfolios:
        choice = _console.input("Enter a Portfolio ID to view holdings, or press Enter to skip: ").strip()
        if choice:
            try:
                pid = int(choice)
                # Only allow viewing if portfolio belongs to user (or admin)
                valid_ids = [p.get("portfolio_id") for p in user_portfolios]
                if pid in valid_ids:
                    view_holdings(pid)
                else:
                    _console.print("Invalid Portfolio ID.", style="red")
            except Exception:
                _console.print("Invalid input.", style="red")

def view_holdings(portfolio_id: int) -> None:
    portfolio = next((p for p in db.portfolios if p["portfolio_id"] == portfolio_id), None)
    if not portfolio:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
        return
    # Enforce ownership (admin can view all)
    if not db.current_user:
        _console.print("Please log in to view portfolios.", style="red")
        return
    owner = portfolio.get("owner")
    if db.current_user.username != "admin" and owner != db.current_user.username:
        _console.print("Access denied: you cannot view another user's portfolio.", style="red")
        return
    holdings = portfolio.get("holdings", [])

    # Build a price lookup for securities
    price_by_symbol = {s.get("symbol"): float(s.get("price", 0)) for s in db.Securities}
    
    # Render table
    table = Table(title=f"Holdings for Portfolio: {portfolio['name']}")
    table.add_column("Security", style="yellow", justify="center", no_wrap=True)
    table.add_column("Qty", style="cyan", justify="center", no_wrap=True)
    table.add_column("Balance", style="green", justify="center", no_wrap=True)

    if not holdings:
        _console.print("No holdings in this portfolio.", style="yellow")
        return

    total_value = 0.0

    # handle investment objects
    for holding in holdings:
        if isinstance(holding, Investment):
            sym = holding.ticker
            qty = holding.qty
            price = price_by_symbol.get(sym, 0.0)
            balance = price * qty
            total_value += balance
            table.add_row(sym, str(qty), f"${balance:,.2f}")

    # Add footer rows with subtotal, cash, and total
    if holdings:
        table.add_row("", "TOTAL", f"${total_value:,.2f}")

    _console.print(table)

def create_portfolio() -> None:
    if not db.current_user:
        _console.print("Please log in to create a portfolio.", style="red")
        return
    _console.print("\n   Create Portfolio   ", style="yellow")
    name = _console.input("Portfolio Name: ")
    description = _console.input("Description: ")
    new_id = db.next_portfolio_id()
    db.portfolios.append({
        "portfolio_id": new_id,
        "name": name,
        "description": description,
        "owner": db.current_user.username,
        "holdings": []
    })
    _console.print(f"Portfolio '{name}' created with ID {new_id}.", style="green")

def delete_portfolio(portfolio_id: int) -> None:
    if not db.current_user:
        _console.print("Please log in to delete a portfolio.", style="red")
        return
    idx = next((i for i, p in enumerate(db.portfolios) if p["portfolio_id"] == portfolio_id), None)
    if idx is None:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
        return
    portfolio = db.portfolios[idx]
    owner = portfolio.get("owner")
    if db.current_user.username != "admin" and owner != db.current_user.username:
        _console.print("Access denied: you cannot delete another user's portfolio.", style="red")
        return
    # Prevent deletion if holdings are not empty
    holdings = portfolio.get("holdings", [])
    has_investments = False
    if isinstance(holdings, dict):
        has_investments = len(holdings) > 0
    elif isinstance(holdings, (list, set, tuple)):
        has_investments = len(holdings) > 0
    elif isinstance(holdings, str):
        has_investments = bool(holdings.strip())
    if has_investments:
        _console.print("Cannot delete portfolio: investments must be liquidated before deletion.", style="red")
        return
    name = portfolio["name"]
    del db.portfolios[idx]
    _console.print(f"Portfolio '{name}' deleted.", style="green")

def partial_liquidate_holdings() -> None:
    if not db.current_user:
        _console.print("Please log in to liquidate holdings.", style="red")
        return
    _console.print("\n   Harvest Liquidation   ", style="yellow")
    try:
        pid_str = _console.input("Enter Portfolio ID: ").strip()
        pid = int(pid_str)
    except Exception:
        _console.print("Invalid Portfolio ID.", style="red")
        return
    portfolio = next((p for p in db.portfolios if p["portfolio_id"] == pid), None)
    if not portfolio:
        _console.print(f"Portfolio ID {pid} not found.", style="red")
        return
    if db.current_user.username != "admin" and portfolio.get("owner") != db.current_user.username:
        _console.print("Access denied: you cannot modify another user's portfolio.", style="red")
        return
    holdings = portfolio.get("holdings", {})

    # Normalize holdings to dict for easier handling
    if isinstance(holdings, dict):
        holdings_dict = holdings
    elif isinstance(holdings, (list, set, tuple)):
        holdings_dict = {}
        for item in holdings:
            if isinstance(item, dict) and "symbol" in item and "qty" in item:
                holdings_dict[item["symbol"]] = item["qty"]
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                holdings_dict[str(item[0])] = item[1]
            elif isinstance(item, str):
                for sym in [p.strip() for p in item.split(",") if p.strip()]:
                    holdings_dict[sym] = 1
    elif isinstance(holdings, str):
        holdings_dict = {sym: 1 for sym in [p.strip() for p in holdings.split(",") if p.strip()]}
    else:
        holdings_dict = {}

    if not holdings_dict:
        _console.print("No holdings to liquidate.", style="yellow")
        return

    full_liq = _console.input("Liquidate all holdings in this portfolio? (Y/N): ").strip().upper()
    
    if full_liq == "Y":
        # Liquidate all holdings at current market price automatically
        total_proceeds = 0.0
        for ticker, orig_qty in list(holdings_dict.items()):
            current_price = next((s["price"] for s in db.Securities if s["symbol"] == ticker), None)
            if current_price is None:
                _console.print(f"Security '{ticker}' not found in Securities list. Skipping.", style="red")
                continue
            
            proceeds = orig_qty * current_price
            total_proceeds += proceeds
            holdings_dict.pop(ticker)
            _console.print(f"Liquidated {orig_qty} of {ticker} at current market price ${current_price:,.2f} each. Proceeds: ${proceeds:,.2f}", style="green")
        
        # Update portfolio with cleared holdings and add proceeds to user balance
        portfolio["holdings"] = holdings_dict
        db.current_user.balance += total_proceeds
        _console.print(f"\nTotal proceeds: ${total_proceeds:,.2f}", style="green bold")
        _console.print(f"New balance: ${db.current_user.balance:,.2f}", style="green bold")
        return
    elif full_liq == "N":
        # Partial liquidation - ask for ONE specific security
        # Loop until valid ticker is entered
        while True:
            ticker = _console.input("Enter ticker to liquidate: ").strip().upper()
            if not ticker:
                _console.print("Ticker cannot be empty.", style="red")
                continue
            if ticker not in holdings_dict:
                _console.print(f"Security '{ticker}' not found in holdings.", style="red")
                _console.print(f"Available securities: {', '.join(holdings_dict.keys())}", style="yellow")
                continue
            break  # Valid ticker found
        
        orig_qty = holdings_dict[ticker]
        current_price = next((s["price"] for s in db.Securities if s["symbol"] == ticker), None)
        if current_price is None:
            _console.print(f"Security '{ticker}' not found in Securities list.", style="red")
            return
        
        _console.print(f"You own {orig_qty} of {ticker} (current market price: ${current_price:,.2f})")
        
        # Loop until valid quantity is entered
        while True:
            qty_str = _console.input(f"Enter quantity to liquidate (max {orig_qty}): ").strip()
            try:
                qty = float(qty_str)
                if qty <= 0:
                    _console.print("Quantity must be greater than 0.", style="red")
                    continue
                if qty > orig_qty:
                    _console.print(f"Cannot liquidate more than you own. Max available: {orig_qty}", style="red")
                    continue
                break  # Valid quantity entered
            except ValueError:
                _console.print("Invalid quantity. Please enter a numeric value.", style="red")
        
        # Loop until valid sale price is entered
        while True:
            sale_price_str = _console.input(f"Enter sale price per unit (current: ${current_price:,.2f}): ").strip()
            try:
                sale_price = float(sale_price_str)
                if sale_price <= 0:
                    _console.print("Sale price must be greater than 0.", style="red")
                    continue
                break  # Valid price entered
            except ValueError:
                _console.print("Invalid sale price. Please enter a numeric value.", style="red")
        
        proceeds = qty * sale_price
        holdings_dict[ticker] = orig_qty - qty
        if holdings_dict[ticker] == 0:
            holdings_dict.pop(ticker)
        
        # Update portfolio holdings and add proceeds to user balance
        portfolio["holdings"] = holdings_dict
        db.current_user.balance += proceeds
        _console.print(f"Liquidated {qty} of {ticker} at ${sale_price:,.2f} each. Proceeds: ${proceeds:,.2f}", style="green")
        _console.print(f"New balance: ${db.current_user.balance:,.2f}", style="green bold")
        return
    else:
        _console.print("Invalid choice. Please enter Y or N.", style="red")
        return
