from __future__ import annotations
from rich.console import Console
from rich.table import Table
from datetime import datetime

from domain.Transactions import Transactions
from domain.Portfolio import Portfolio
from domain.Investment import Investment
from domain.Security import Security
from domain.User import User

from services.transaction_services import update_transaction_record
from services.transaction_services import format_timestamp

from database import get_session 

_console = Console()


def view_all_securities() -> None:
    table = Table(title="All Securities")
    table.add_column("Ticker", style="cyan", justify="center")
    table.add_column("Issuer", style="yellow", justify="center")
    table.add_column("Name", style="white", justify="center")
    table.add_column("Price", style="green", justify="center")
    with get_session() as session:
        securities = session.query(Security).all()
        for sec in securities:
            table.add_row(
                sec.symbol,
                sec.issuer,
                sec.name,
                f"${sec.price:,.2f}"
        )
    _console.print(table)

def place_order(portfolio_id: int = None, ticker: str = None, quantity: float = None) -> bool:
    from services.login_services import current_user
    with get_session() as session:
        user_portfolios = session.query(Portfolio).filter_by(owner=current_user).all()
        if not user_portfolios:
            _console.print("You have no portfolios. Create one first.", style="yellow")
            return False
        
        if portfolio_id is None:
            _console.print("Your Portfolios:", style="yellow")
            for p in user_portfolios:
                _console.print(f"ID: {p.id} | Name: {p.name}")
            while True:
                pid_str = _console.input("Enter Portfolio ID to invest in: ").strip()
                try:
                    portfolio_id = int(pid_str)
                    portfolio = next((p for p in user_portfolios if p.id == portfolio_id), None)
                    if not portfolio:
                        _console.print("Invalid Portfolio ID.", style="red")
                        continue
                    break
                except Exception:
                    _console.print("Invalid input.", style="red")
        else:
            portfolio = next((p for p in user_portfolios if p.id == portfolio_id), None)
            if not portfolio:
                return False

        if ticker is None:
            ticker = _console.input("Enter ticker to buy: ").strip().upper()
        security = session.query(Security).filter_by(symbol=ticker).first()
        if not security:
            if ticker is None:
                _console.print(f"Security '{ticker}' not found.", style="red")
            return False
        
        if quantity is None:
            while True:
                qty_str = _console.input("Enter quantity to buy: ").strip()
                try:
                    quantity = float(qty_str)
                    if quantity <= 0:
                        _console.print("Quantity must be greater than 0.", style="red")
                        continue
                    break
                except Exception:
                    _console.print("Invalid quantity.", style="red")
        
        cost = quantity * security.price
        if ticker is None or quantity is None:
            _console.print(f"Order: {quantity} x {ticker} @ ${security.price:,.2f} = ${cost:,.2f}", style="green")

        user = session.query(User).filter_by(username=current_user.username).first()
        if cost > user.balance:
            if ticker is None or quantity is None:
                _console.print(
                    f"Insufficient balance to complete the purchase. Available: ${user.balance:,.2f}",
                    style="red"
                )
            return False
        
        user.balance -= cost

        existing_investment = session.query(Investment).filter_by(portfolio_id=portfolio.id, Ticker=ticker).first()
        
        if existing_investment:
            existing_investment.Qty += quantity
            if ticker is None or quantity is None:
                _console.print(f"Updated existing position: {existing_investment.Qty} total {ticker}", style="cyan")
        else:
            new_investment = Investment(Ticker=ticker, portfolio_id=portfolio.id, Qty=int(quantity), purchase_price=security.price)
            session.add(new_investment)
            if ticker is None or quantity is None:
                _console.print(f"Created new position: {quantity} of {ticker}", style="cyan")

        update_transaction_record(
            transaction_id=session.query(Transactions).count() + 1,
            user_id=current_user.username,
            portfolio_id=str(portfolio.id),
            security_id=ticker,
            transaction_type="BUY",
            qty=int(quantity),
            price=security.price,
            timestamp=format_timestamp(datetime.now())
        )

        session.commit()

        if ticker is None or quantity is None:
            _console.print(
                f"Added {quantity} of {ticker} to portfolio '{portfolio.name}'. Remaining balance: ${user.balance:,.2f}",
                style="green bold"
            )
        
        return True



