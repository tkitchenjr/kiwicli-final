from __future__ import annotations
from rich.console import Console
from rich.table import Table


from app.domain.Investment import Investment
from app.domain.Portfolio import Portfolio
from app.domain.User import User
from app.domain.Security import Security

from app.services.transaction_services import update_transaction_record
from app.services.login_services import current_user

from app.db import db

import datetime


_console = Console()


def view_all_portfolios() -> None:
    with db.session as session:
        if not session.query(User).filter_by(username=current_user).first():
            _console.print("Please log in to view portfolios.", style="red")
            return
        
        # Filter portfolios for current user (admin can see all)
        if current_user == "admin":
            user_portfolios = session.query(Portfolio).all()
        else:
            user_portfolios = session.query(Portfolio).filter_by(owner=current_user).all()

        if not user_portfolios:
            _console.print("You have no portfolios yet.", style="yellow")
            return
        
        # Create a summary table
        table = Table(title=f"Portfolios for {current_user}")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Name", justify="center", style="yellow", no_wrap=True)
        table.add_column("Description", justify="center", style="white", no_wrap=True)

        for portfolio in user_portfolios:
            table.add_row(
                str(portfolio.id),
                portfolio.name,
                portfolio.description or ""
            )
        
        _console.print(table)
        _console.print(f"Available Balance: ${current_user.balance:,.2f}", style="green bold")
            # Prompt to view holdings for a selected portfolio
        if user_portfolios:
            choice = _console.input("Enter a Portfolio ID to view holdings, or press Enter to skip: ").strip()
            if choice:
                try:
                    pid = int(choice)
                    # Only allow viewing if portfolio belongs to user (or admin)
                    valid_ids = [p.portfolio_id for p in user_portfolios]
                    if pid in valid_ids:
                        view_holdings(pid, current_user)
                    else:
                        _console.print("Invalid Portfolio ID.", style="red")
                except Exception:
                    _console.print("Invalid input.", style="red")
    
def view_holdings(portfolio_id: int, current_user: str) -> None:
    with db.session as session:
        # Use provided portfolio_id when passed; otherwise prompt the user.
        if portfolio_id is None:
            portfolio_id = _console.input("Enter Portfolio ID to view holdings: ").strip()
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if not portfolio:
            _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
            return

    # Enforce ownership (admin can view all)
    if current_user != "admin" and portfolio.owner != current_user:
        _console.print("Access denied: you cannot view another user's portfolio.", style="red")
        return

    # Query investments for this portfolio
    investments = session.query(Investment).filter_by(portfolio_id=portfolio.id).all()  

    # Render table
    table = Table(title=f"Holdings for Portfolio: {portfolio.name}")
    table.add_column("Security", style="yellow", justify="center", no_wrap=True)
    table.add_column("Qty", style="cyan", justify="center", no_wrap=True)
    table.add_column("Balance", style="green", justify="center", no_wrap=True)

    if not investments:
        _console.print("No holdings in this portfolio.", style="yellow")
        return

    total_value = 0.0

    for investment in investments:
        sym = investment.Ticker
        qty = investment.Qty

        # Get current price from security (assuming Security model exists)
        security = session.query(Security).filter_by(symbol=sym).first()
        price = float(security.price) if security else 0.0
        balance = price * qty
        total_value += balance
        table.add_row(sym, str(qty), f"${balance:,.2f}")
    return
    
def create_portfolio(current_user: str, name: str = None, description: str = None) -> bool:
    with db.session as session:
        if name is None:
            _console.print("Portfolio name is required.", style="yellow")
            return False
        if description is None:
            _console.print("Portfolio description is required.", style="yellow")
            return False

        new_portfolio = Portfolio(
            id=session.query(Portfolio).count() + 1,
            name=name,
            description=description,
            owner=current_user
        )
        session.add(new_portfolio)
        session.commit()

        _console.print(f"Portfolio '{new_portfolio.id}' created with ID {new_portfolio.id}.", style="green")
        return True
    
def delete_portfolio(current_user: str, portfolio_id: int = None) -> bool:
    with db.session as session:
        if portfolio_id is None:
            _console.print("\n   Delete Portfolio   ", style="yellow")
            try:
                pid_str = _console.input("Enter Portfolio ID to delete: ").strip()
                portfolio_id = int(pid_str)
            except Exception:
                _console.print("Invalid Portfolio ID.", style="red")
                return False
        
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if not portfolio:
            if portfolio_id is None:
                _console.print(f"Portfolio ID {portfolio_id} not found.", style="red")
            return False
        
        if current_user != "admin" and portfolio.owner != current_user:
            if portfolio_id is None:
                _console.print("Access denied: you cannot delete another user's portfolio.", style="red")
            return False

        investments = session.query(Investment).filter_by(portfolio_id=portfolio.id).all()
        if investments:
            if portfolio_id is None:
                _console.print("Cannot delete portfolio: investments must be liquidated before deletion.", style="red")
            return False
        
        session.delete(portfolio)
        session.commit()
        if portfolio_id is None:
            _console.print(f"Portfolio '{portfolio.name}' deleted successfully.", style="green")
        return True

def liquidate_portfolio(current_user: str) -> None:
    with db.session as session:
        _console.print("\n   Harvest Liquidation   ", style="yellow")
        try:
            pid_str = _console.input("Enter Portfolio ID: ").strip()
            pid = int(pid_str)
        except Exception:
            _console.print("Invalid Portfolio ID.", style="red")
            return

        portfolio = session.query(Portfolio).filter_by(id=pid).first()
        if not portfolio:
            _console.print(f"Portfolio ID {pid} not found.", style="red")
            return

        if current_user != "admin" and portfolio.owner != current_user:
            _console.print("Access denied: you cannot modify another user's portfolio.", style="red")
            return

        investments = session.query(Investment).filter_by(portfolio_id=pid).all()

        if not investments:
            _console.print("No holdings to liquidate.", style="yellow")
            return

        full_liq = _console.input("Liquidate all holdings in this portfolio? (Y/N): ").strip().upper()

        if full_liq == "Y":
            # Liquidate all holdings at current market price automatically
            total_proceeds = 0.0
            investments = session.query(Investment).filter_by(portfolio_id=pid).all()
            for investment in investments:
                security = session.query(Security).filter_by(symbol=investment.Ticker).first()
                if not security:
                    _console.print(f"Security '{investment.Ticker}' not found in Securities list. Skipping.", style="red")
                    continue
                
                current_price = float(security.price)
                qty = int(investment.Qty)
                ticker = investment.Ticker
                proceeds = qty * current_price
                total_proceeds += proceeds

                update_transaction_record(
                    transaction_id=None,
                    user_id=current_user,
                    portfolio_id=str(pid),
                    security_id=ticker,
                    transaction_type="SELL",
                    qty=qty,
                    price=current_price,
                    timestamp=datetime.datetime.now()
                )
                
                _console.print(f"Liquidated {qty} of {ticker} at current market price ${current_price:,.2f} each. Proceeds: ${proceeds:,.2f}", style="green")
                
                # Remove investment
                session.delete(investment)
            
            # Update user balance
            user = session.query(User).filter_by(username=current_user).first()
            user.balance += total_proceeds
            session.commit()
            
            _console.print(f"\nTotal proceeds: ${total_proceeds:,.2f}", style="green bold")
            _console.print(f"New balance: ${user.balance:,.2f}", style="green bold")
            return

        elif full_liq == "N":
            # Partial liquidation - ask for ONE specific security
            holdings_dict = {inv.Ticker: inv.Qty for inv in investments}
            
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
            
            investment = session.query(Investment).filter_by(portfolio_id=portfolio.id, Ticker=ticker).first()
            orig_qty = investment.Qty
            
            security = session.query(Security).filter_by(ticker=ticker).first()
            if not security:
                _console.print(f"Security '{ticker}' not found in Securities list.", style="red")
                return
            
            current_price = float(security.price)
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
            investment.qty = orig_qty - qty
            
            if investment.qty == 0:
                session.delete(investment)
            
            # Record transaction
            update_transaction_record(
                transaction_id=None,
                user_id=current_user,
                portfolio_id=str(pid),
                security_id=ticker,
                transaction_type="SELL",
                qty=int(qty),
                price=sale_price,
                timestamp=datetime.datetime.now()
            )
            
            # Update user balance
            user = session.query(User).filter_by(username=current_user).first()
            user.balance += proceeds
            session.commit()
            
            _console.print(f"Liquidated {qty} of {ticker} at ${sale_price:,.2f} each. Proceeds: ${proceeds:,.2f}", style="green")
            _console.print(f"New balance: ${user.balance:,.2f}", style="green bold")
            return
        else:
            _console.print("Invalid choice. Please enter Y or N.", style="red")
            return
