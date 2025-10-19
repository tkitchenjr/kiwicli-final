
from rich.console import Console
from rich.table import Table

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
    import db
    portfolio = next((p for p in db.portfolios if p["portfolio_id"] == portfolio_id), None)
    if not portfolio:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
        return
    holdings = portfolio.get("holdings", [])
    table = Table(title=f"Holdings for Portfolio {portfolio['name']}")
    table.add_column("Symbol", style="yellow")
    for symbol in holdings:
        table.add_row(symbol)
    _console.print(table)

# Create a new portfolio
def create_portfolio() -> None:
    import db
    _console.print("\n   Create Portfolio   ", style="yellow")
    name = _console.input("Portfolio Name: ")
    description = _console.input("Description: ")
    new_id = max([p["portfolio_id"] for p in db.portfolios], default=0) + 1
    db.portfolios.append({
        "portfolio_id": new_id,
        "name": name,
        "description": description,
        "holdings": []
    })
    _console.print(f"Portfolio '{name}' created with ID {new_id}.", style="green")

# Delete a portfolio by ID
def delete_portfolio(portfolio_id: int) -> None:
    import db
    idx = next((i for i, p in enumerate(db.portfolios) if p["portfolio_id"] == portfolio_id), None)
    if idx is not None:
        name = db.portfolios[idx]["name"]
        del db.portfolios[idx]
        _console.print(f"Portfolio '{name}' deleted.", style="green")
    else:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")

# Liquidate holdings for a portfolio
def liquidate_holdings(portfolio_id: int) -> None:
    import db
    portfolio = next((p for p in db.portfolios if p["portfolio_id"] == portfolio_id), None)
    if not portfolio:
        _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
        return
    portfolio["holdings"] = []
    _console.print(f"All holdings liquidated for portfolio '{portfolio['name']}'.", style="green")