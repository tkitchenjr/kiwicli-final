from rich.console import Console
from rich.table import Table

from database import SessionLocal

from domain.Transactions import Transactions

from datetime import datetime

_console = Console()

def update_transaction_record(transaction_id: str, user_id: str, portfolio_id: str,security_id: str, transaction_type: str, qty: int, price: float, timestamp: str):
    new_transaction = Transactions(
        transaction_id=transaction_id,
        user_id=user_id,
        portfolio_id=portfolio_id,
        security_id=security_id,
        transaction_type=transaction_type,
        qty=qty,
        price=price,
        timestamp=datetime.now()
    )

    with SessionLocal() as session:
        session.add(new_transaction)
        session.commit()
    _console.print(f"Transaction recorded: {transaction_type} {qty} of {security_id} at ${price:.2f}", style="green")

def format_timestamp(timestamp) -> str:
    if isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M")
    else:
        return str(timestamp)

def view_transactions():
    with SessionLocal() as session:
        transactions_list = session.query(Transactions).all()
    if not transactions_list:
        _console.print("No transactions found.", style="yellow")
        return
    #render table
    table = Table(title="Transaction History")
    table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("User ID", justify="center", style="yellow", no_wrap=True)
    table.add_column("Portfolio ID", justify="center", style="green", no_wrap=True)
    table.add_column("Security ID", justify="center", style="blue", no_wrap=True)
    table.add_column("Type", justify="center", style="magenta", no_wrap=True)
    table.add_column("Quantity", justify="center", style="white", no_wrap=True)
    table.add_column("Price", justify="center", style="green", no_wrap=True)
    table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)

    #populate table
    for t in transactions_list:
        table.add_row(
            str(t.transaction_id),
            str(t.user_id),
            str(t.portfolio_id),
            str(t.security_id),
            str(t.transaction_type),
            str(t.qty),
            f"${t.price:.2f}",
            format_timestamp(t.timestamp)
        )
    _console.print(table)

def query_transactions_by_user():
    with SessionLocal() as session:
        input_id = _console.input("Enter User ID to query: ").strip().lower()
        if not input_id:
            _console.print("User ID cannot be empty.", style="red")
            return 
        user_transactions = session.query(Transactions).filter_by(user_id=input_id).all()
        if not user_transactions:
            _console.print(f"No transactions found for User ID: {input_id}", style="yellow")
            return
        table = Table(title=f"Transactions for User ID: {input_id}")
        table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Portfolio ID", justify="center", style="green", no_wrap=True)
        table.add_column("Security ID", justify="center", style="blue", no_wrap=True)
        table.add_column("Type", justify="center", style="magenta", no_wrap=True)
        table.add_column("Quantity", justify="center", style="white", no_wrap=True)
        table.add_column("Price", justify="center", style="green", no_wrap=True)
        table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)
        for t in user_transactions:
            table.add_row(
                str(t.transaction_id),
                str(t.portfolio_id),
                str(t.security_id),
                str(t.transaction_type),
                str(t.qty),
                f"${t.price:.2f}",
                format_timestamp(t.timestamp)
            )
    _console.print(table)

def query_transactions_by_portfolio():
    with SessionLocal() as session:
        id = _console.input("Enter Portfolio ID to query: ").strip()
    if not id:
        _console.print("Portfolio ID cannot be empty.", style="red")
        return 
    transactions = session.query(Transactions).filter_by(portfolio_id=id).all()
    if not transactions:
        _console.print(f"No transactions found for Portfolio ID: {id}", style="yellow")
        return
    
    #render table
    table = Table(title=f"Transactions for Portfolio ID: {id}")
    table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("User ID", justify="center", style="green", no_wrap=True)
    table.add_column("Security ID", justify="center", style="blue", no_wrap=True)
    table.add_column("Type", justify="center", style="magenta", no_wrap=True)
    table.add_column("Quantity", justify="center", style="white", no_wrap=True)
    table.add_column("Price", justify="center", style="green", no_wrap=True)
    table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)
    
    #populate table
    for t in transactions:
        table.add_row(
            str(t.transaction_id),
            str(t.user_id),
            str(t.security_id),
            str(t.transaction_type),
            str(t.qty),
            f"${t.price:.2f}",
            format_timestamp(t.timestamp)
        )
    _console.print(table)

def query_transactions_by_security():
    with SessionLocal() as session:
        ticker = _console.input("Enter Ticker to query: ").strip().upper()
        if not ticker:
            _console.print("Ticker cannot be empty.", style="red")
            return 
        transactions = session.query(Transactions).filter_by(security_id=ticker).all()
        if not transactions:
            _console.print(f"No transactions found for Security ID: {ticker}", style="yellow")
            return
        
        #render table
        table = Table(title=f"Transactions for Security ID: {ticker}")
        table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("User ID", justify="center", style="green", no_wrap=True)
        table.add_column("Portfolio ID", justify="center", style="blue", no_wrap=True)
        table.add_column("Type", justify="center", style="magenta", no_wrap=True)
        table.add_column("Quantity", justify="center", style="white", no_wrap=True)
        table.add_column("Price", justify="center", style="green", no_wrap=True)
        table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)

        #populate table
        for t in transactions:
            table.add_row(
                str(t),
                str(t.user_id),
                str(t.portfolio_id),
                str(t.transaction_type),
                str(t.qty),
                f"${t.price:.2f}",
                format_timestamp(t.timestamp)
            )
        _console.print(table)